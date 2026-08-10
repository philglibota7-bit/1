using KioskSender.Core.Content;
using Xunit;

namespace KioskSender.Core.Tests;

public class NaturalComparerTests
{
    [Fact]
    public void Sorts_numbers_the_way_people_expect()
    {
        var names = new[] { "Bild10.jpg", "Bild2.jpg", "Bild1.jpg" };
        Array.Sort(names, NaturalComparer.Instance);

        Assert.Equal(new[] { "Bild1.jpg", "Bild2.jpg", "Bild10.jpg" }, names);
    }

    [Fact]
    public void Leading_zeros_do_not_change_the_order()
    {
        var names = new[] { "Folie007.png", "Folie7b.png", "Folie2.png" };
        Array.Sort(names, NaturalComparer.Instance);

        Assert.Equal("Folie2.png", names[0]);
    }

    [Fact]
    public void Falls_back_to_case_insensitive_text()
    {
        var names = new[] { "banner.mp4", "Anfang.jpg", "Cafe.png" };
        Array.Sort(names, NaturalComparer.Instance);

        Assert.Equal(new[] { "Anfang.jpg", "banner.mp4", "Cafe.png" }, names);
    }

    [Fact]
    public void Handles_null_and_equal_values()
    {
        Assert.Equal(0, NaturalComparer.Instance.Compare("a", "a"));
        Assert.True(NaturalComparer.Instance.Compare(null, "a") < 0);
        Assert.True(NaturalComparer.Instance.Compare("a", null) > 0);
    }

    [Fact]
    public void Longer_number_wins()
    {
        Assert.True(NaturalComparer.Instance.Compare("teil9", "teil100") < 0);
    }
}

public class MediaKindTests
{
    [Theory]
    [InlineData("foto.jpg", MediaKind.Image)]
    [InlineData("FOTO.JPEG", MediaKind.Image)]
    [InlineData("logo.png", MediaKind.Image)]
    [InlineData("clip.mp4", MediaKind.Video)]
    [InlineData("alt.wmv", MediaKind.Video)]
    [InlineData("folien.pptx", MediaKind.Presentation)]
    [InlineData("folien.pps", MediaKind.Presentation)]
    [InlineData("liste.txt", MediaKind.Unsupported)]
    [InlineData("ohne-endung", MediaKind.Unsupported)]
    [InlineData("", MediaKind.Unsupported)]
    public void Detects_the_kind_from_the_extension(string fileName, MediaKind expected) =>
        Assert.Equal(expected, MediaKinds.FromFileName(fileName));

    [Fact]
    public void Size_is_formatted_readably()
    {
        Assert.Equal("512 B", MediaItem.FormatSize(512));
        Assert.Equal("1,5 KB".Replace(',', '.'), MediaItem.FormatSize(1536).Replace(',', '.'));
        Assert.Contains("MB", MediaItem.FormatSize(5 * 1024 * 1024));
        Assert.Contains("GB", MediaItem.FormatSize(3L * 1024 * 1024 * 1024));
    }
}

public class MediaLibraryTests : IDisposable
{
    private readonly string _root =
        Path.Combine(Path.GetTempPath(), "kiosk-library-" + Guid.NewGuid().ToString("N"));

    public MediaLibraryTests() => Directory.CreateDirectory(_root);

    public void Dispose()
    {
        try
        {
            Directory.Delete(_root, recursive: true);
        }
        catch
        {
            // Aufräumen darf den Test nicht kippen.
        }
    }

    private void Write(string relativePath, int bytes = 16)
    {
        var full = Path.Combine(_root, relativePath);
        Directory.CreateDirectory(Path.GetDirectoryName(full)!);
        File.WriteAllBytes(full, new byte[bytes]);
    }

    [Fact]
    public void Missing_folder_reports_an_error_instead_of_throwing()
    {
        var result = new MediaLibrary().Scan(Path.Combine(_root, "gibtsnicht"));

        Assert.False(result.Success);
        Assert.Contains("nicht gefunden", result.Error);
    }

    [Fact]
    public void Empty_path_reports_an_error()
    {
        Assert.False(new MediaLibrary().Scan("").Success);
    }

    [Fact]
    public void Reads_files_in_natural_order()
    {
        Write("Bild10.jpg");
        Write("Bild2.jpg");
        Write("Bild1.jpg");

        var root = new MediaLibrary().Scan(_root).Root!;

        Assert.Equal(new[] { "Bild1.jpg", "Bild2.jpg", "Bild10.jpg" },
            root.Items.Select(i => i.FileName).ToArray());
    }

    [Fact]
    public void Subfolders_become_their_own_playlists()
    {
        Write("Foyer/a.jpg");
        Write("Foyer/b.mp4");
        Write("Kantine/c.pptx");

        var root = new MediaLibrary().Scan(_root).Root!;

        Assert.Equal(2, root.Folders.Count);
        Assert.Equal("Foyer", root.Folders[0].Name);
        Assert.Equal(2, root.Folders[0].Items.Count);
        Assert.Equal("Kantine", root.Folders[1].Name);
    }

    [Fact]
    public void Unsupported_files_are_listed_separately()
    {
        Write("gut.jpg");
        Write("liesmich.txt");

        var root = new MediaLibrary().Scan(_root).Root!;

        Assert.Single(root.Items);
        Assert.Equal("liesmich.txt", Assert.Single(root.SkippedFiles));
    }

    [Fact]
    public void Images_get_the_default_duration_videos_do_not()
    {
        Write("bild.jpg");
        Write("film.mp4");

        var root = new MediaLibrary { DefaultImageSeconds = 7 }.Scan(_root).Root!;

        Assert.Equal(7, root.Items.Single(i => i.Kind == MediaKind.Image).Seconds);
        Assert.Equal(0, root.Items.Single(i => i.Kind == MediaKind.Video).Seconds);
    }

    [Fact]
    public void Depth_limit_is_respected()
    {
        Write("a/b/c/d/e/tief.jpg");

        var root = new MediaLibrary { MaxDepth = 2 }.Scan(_root).Root!;

        var depth = 0;
        var current = root;
        while (current.Folders.Count > 0)
        {
            current = current.Folders[0];
            depth++;
        }

        Assert.Equal(2, depth);
    }

    [Fact]
    public void File_limit_stops_the_scan_and_warns()
    {
        for (var i = 0; i < 12; i++)
        {
            Write($"bild{i}.jpg");
        }

        var result = new MediaLibrary { MaxFiles = 5 }.Scan(_root);

        Assert.Equal(5, result.Root!.Items.Count);
        Assert.Contains("sehr groß", result.Error);
    }

    [Fact]
    public void Totals_add_up_across_subfolders()
    {
        Write("a.jpg", 100);
        Write("unter/b.jpg", 50);

        var root = new MediaLibrary().Scan(_root).Root!;

        Assert.Equal(150, root.TotalBytes);
        Assert.Equal(2, root.TotalItemCount);
    }

    [Fact]
    public void Flatten_returns_every_folder()
    {
        Write("a/x.jpg");
        Write("b/y.jpg");

        var root = new MediaLibrary().Scan(_root).Root!;

        Assert.Equal(3, MediaLibrary.Flatten(root).Count());
    }
}

public class PlaylistTests
{
    private static LibraryFolder SampleFolder() => new()
    {
        Name = "Foyer",
        FullPath = @"C:\Medien\Foyer",
        Items =
        {
            new MediaItem { FileName = "a.jpg", Kind = MediaKind.Image, SizeBytes = 100, SourcePath = @"C:\Medien\Foyer\a.jpg" },
            new MediaItem { FileName = "b.mp4", Kind = MediaKind.Video, SizeBytes = 900, SourcePath = @"C:\Medien\Foyer\b.mp4" }
        }
    };

    [Fact]
    public void FromFolder_gives_images_the_default_duration()
    {
        var playlist = Playlist.FromFolder(SampleFolder(), defaultImageSeconds: 12);

        Assert.Equal("Foyer", playlist.Name);
        Assert.Equal(12, playlist.Items[0].Seconds);
        Assert.Equal(0, playlist.Items[1].Seconds);
    }

    [Fact]
    public void Json_roundtrips()
    {
        var playlist = Playlist.FromFolder(SampleFolder());
        playlist.Shuffle = true;

        var restored = Playlist.FromJson(playlist.ToJson());

        Assert.NotNull(restored);
        Assert.Equal("Foyer", restored!.Name);
        Assert.True(restored.Shuffle);
        Assert.Equal(2, restored.Items.Count);
        Assert.Equal(MediaKind.Video, restored.Items[1].Kind);
    }

    [Fact]
    public void Kind_is_stored_as_readable_text()
    {
        Assert.Contains("\"Video\"", Playlist.FromFolder(SampleFolder()).ToJson());
    }

    [Fact]
    public void Broken_json_returns_null_instead_of_throwing()
    {
        Assert.Null(Playlist.FromJson("{ kaputt"));
    }

    [Fact]
    public void Delivery_copy_drops_unsupported_items_and_local_paths()
    {
        var playlist = Playlist.FromFolder(SampleFolder());
        playlist.Items.Add(new MediaItem { FileName = "x.txt", Kind = MediaKind.Unsupported });

        var delivery = playlist.ForDelivery();

        Assert.Equal(2, delivery.Items.Count);
        Assert.All(delivery.Items, i => Assert.Equal(string.Empty, i.SourcePath));
    }

    [Fact]
    public void Duration_marks_unknown_video_length()
    {
        var playlist = Playlist.FromFolder(SampleFolder(), 10);

        Assert.True(playlist.HasUnknownDuration);
        Assert.Contains("Videolaufzeiten", playlist.DurationText);
    }

    [Fact]
    public void Duration_is_exact_without_videos()
    {
        var folder = new LibraryFolder
        {
            Name = "Bilder",
            Items = { new MediaItem { FileName = "a.jpg", Kind = MediaKind.Image } }
        };

        var playlist = Playlist.FromFolder(folder, 30);

        Assert.False(playlist.HasUnknownDuration);
        Assert.Equal(TimeSpan.FromSeconds(30), playlist.KnownDuration);
    }
}

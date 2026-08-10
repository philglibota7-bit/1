using KioskSender.Core.Content;
using Xunit;

namespace KioskSender.Core.Tests;

public class PlaylistCursorTests
{
    private static Playlist Make(bool loop = true, bool shuffle = false, params string[] files)
    {
        var playlist = new Playlist { Loop = loop, Shuffle = shuffle, DefaultImageSeconds = 10 };

        foreach (var file in files)
        {
            playlist.Items.Add(new MediaItem
            {
                FileName = file,
                Kind = MediaKinds.FromFileName(file)
            });
        }

        return playlist;
    }

    [Fact]
    public void Plays_in_order()
    {
        var cursor = new PlaylistCursor(Make(false, false, "a.jpg", "b.jpg", "c.jpg"));

        Assert.Equal("a.jpg", cursor.Next()!.FileName);
        Assert.Equal("b.jpg", cursor.Next()!.FileName);
        Assert.Equal("c.jpg", cursor.Next()!.FileName);
    }

    [Fact]
    public void Without_loop_it_ends()
    {
        var cursor = new PlaylistCursor(Make(false, false, "a.jpg"));

        Assert.NotNull(cursor.Next());
        Assert.Null(cursor.Next());
        Assert.Equal(1, cursor.CompletedRounds);
    }

    [Fact]
    public void With_loop_it_starts_over()
    {
        var cursor = new PlaylistCursor(Make(true, false, "a.jpg", "b.jpg"));

        cursor.Next();
        cursor.Next();
        Assert.Equal("a.jpg", cursor.Next()!.FileName);
        Assert.Equal(1, cursor.CompletedRounds);
    }

    [Fact]
    public void Empty_playlist_yields_nothing()
    {
        var cursor = new PlaylistCursor(Make(true, false));

        Assert.True(cursor.IsEmpty);
        Assert.Null(cursor.Next());
        Assert.Null(cursor.Current);
    }

    [Fact]
    public void Unsupported_items_are_left_out()
    {
        var cursor = new PlaylistCursor(Make(false, false, "a.jpg", "liesmich.txt", "b.mp4"));

        Assert.Equal(2, cursor.Items.Count);
        Assert.Equal("a.jpg", cursor.Next()!.FileName);
        Assert.Equal("b.mp4", cursor.Next()!.FileName);
    }

    [Fact]
    public void Current_follows_next()
    {
        var cursor = new PlaylistCursor(Make(true, false, "a.jpg", "b.jpg"));

        Assert.Null(cursor.Current);
        cursor.Next();
        Assert.Equal("a.jpg", cursor.Current!.FileName);
    }

    [Fact]
    public void Shuffle_keeps_every_item_exactly_once_per_round()
    {
        var cursor = new PlaylistCursor(Make(true, true, "a.jpg", "b.jpg", "c.jpg", "d.jpg"), randomSeed: 42);

        var round = new[] { cursor.Next()!, cursor.Next()!, cursor.Next()!, cursor.Next()! }
            .Select(i => i.FileName)
            .OrderBy(n => n)
            .ToArray();

        Assert.Equal(new[] { "a.jpg", "b.jpg", "c.jpg", "d.jpg" }, round);
    }

    [Fact]
    public void Shuffle_is_reproducible_for_a_given_seed()
    {
        var first = new PlaylistCursor(Make(true, true, "a.jpg", "b.jpg", "c.jpg"), randomSeed: 7);
        var second = new PlaylistCursor(Make(true, true, "a.jpg", "b.jpg", "c.jpg"), randomSeed: 7);

        for (var i = 0; i < 3; i++)
        {
            Assert.Equal(first.Next()!.FileName, second.Next()!.FileName);
        }
    }

    [Fact]
    public void Reset_starts_from_the_beginning()
    {
        var cursor = new PlaylistCursor(Make(true, false, "a.jpg", "b.jpg"));

        cursor.Next();
        cursor.Reset();

        Assert.Null(cursor.Current);
        Assert.Equal(0, cursor.CompletedRounds);
        Assert.Equal("a.jpg", cursor.Next()!.FileName);
    }

    [Fact]
    public void Images_fall_back_to_the_default_duration()
    {
        var playlist = Make(true, false, "a.jpg");
        var cursor = new PlaylistCursor(playlist);

        Assert.Equal(10, cursor.SecondsFor(cursor.Next()!));
    }

    [Fact]
    public void Own_duration_wins_over_the_default()
    {
        var playlist = Make(true, false, "a.jpg");
        playlist.Items[0].Seconds = 3;

        var cursor = new PlaylistCursor(playlist);

        Assert.Equal(3, cursor.SecondsFor(cursor.Next()!));
    }

    [Fact]
    public void Videos_report_zero_meaning_play_to_the_end()
    {
        var cursor = new PlaylistCursor(Make(true, false, "film.mp4"));

        Assert.Equal(0, cursor.SecondsFor(cursor.Next()!));
    }
}

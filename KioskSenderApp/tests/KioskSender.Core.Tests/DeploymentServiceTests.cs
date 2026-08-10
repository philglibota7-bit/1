using KioskSender.Core.Content;
using KioskSender.Core.Model;
using Xunit;

namespace KioskSender.Core.Tests;

/// <summary>Merkt sich Übertragungen im Speicher, statt Rechner zu beschreiben.</summary>
file sealed class FakeTransfer : IFileTransfer
{
    public Dictionary<string, string> Written { get; } = new(StringComparer.OrdinalIgnoreCase);

    public List<string> Copied { get; } = new();

    public List<string> Deleted { get; } = new();

    public List<string> Directories { get; } = new();

    /// <summary>Dateien, die auf dem Ziel schon aktuell sind.</summary>
    public HashSet<string> UpToDate { get; } = new(StringComparer.OrdinalIgnoreCase);

    /// <summary>Dateien, die im Zielordner bereits liegen.</summary>
    public Dictionary<string, List<string>> ExistingFiles { get; } = new(StringComparer.OrdinalIgnoreCase);

    public Exception? ThrowOnCopy { get; set; }

    public Task EnsureDirectoryAsync(string directory, CancellationToken cancellationToken = default)
    {
        Directories.Add(directory);
        return Task.CompletedTask;
    }

    public Task<bool> IsUpToDateAsync(string sourceFile, string targetFile, CancellationToken cancellationToken = default) =>
        Task.FromResult(UpToDate.Contains(targetFile));

    public Task CopyAsync(string sourceFile, string targetFile, CancellationToken cancellationToken = default)
    {
        if (ThrowOnCopy is not null)
        {
            throw ThrowOnCopy;
        }

        Copied.Add(targetFile);
        return Task.CompletedTask;
    }

    public Task WriteAllTextAsync(string targetFile, string content, CancellationToken cancellationToken = default)
    {
        Written[targetFile] = content;
        return Task.CompletedTask;
    }

    public Task<IReadOnlyList<string>> ListFilesAsync(string directory, CancellationToken cancellationToken = default) =>
        Task.FromResult<IReadOnlyList<string>>(
            ExistingFiles.TryGetValue(directory, out var files) ? files : new List<string>());

    public Task DeleteAsync(string targetFile, CancellationToken cancellationToken = default)
    {
        Deleted.Add(targetFile);
        return Task.CompletedTask;
    }
}

public class DeploymentServiceTests
{
    private static Playlist SamplePlaylist() => new()
    {
        Name = "Foyer",
        Items =
        {
            new MediaItem { FileName = "a.jpg", Kind = MediaKind.Image, Seconds = 10, SizeBytes = 100, SourcePath = @"C:\M\a.jpg" },
            new MediaItem { FileName = "b.mp4", Kind = MediaKind.Video, SizeBytes = 900, SourcePath = @"C:\M\b.mp4" }
        }
    };

    private static KioskPc Pc(string name = "T1", string host = "PC-01") =>
        new() { Name = name, Host = host };

    private const string DefaultTarget = @"\\PC-01\C$\ProgramData\KioskPlayer";

    /// <summary>
    /// Zielpfade über Path.Combine bilden — der Trenner ist plattformabhängig,
    /// die Tests laufen aber auch auf Nicht-Windows-Systemen.
    /// </summary>
    private static string TargetFile(string fileName) => Path.Combine(DefaultTarget, fileName);

    [Fact]
    public async Task Copies_every_file_and_writes_the_playlist_last()
    {
        var transfer = new FakeTransfer();
        var service = new DeploymentService(transfer);

        var results = await service.DeployAsync(SamplePlaylist(), new[] { Pc() });

        var result = Assert.Single(results);
        Assert.True(result.Success);
        Assert.Equal(2, result.Copied);
        Assert.Equal(2, transfer.Copied.Count);
        Assert.Contains(transfer.Written.Keys, k => k.EndsWith(Playlist.FileName, StringComparison.Ordinal));
    }

    [Fact]
    public async Task Target_path_uses_the_admin_share_by_default()
    {
        var transfer = new FakeTransfer();
        var service = new DeploymentService(transfer);

        await service.DeployAsync(SamplePlaylist(), new[] { Pc(host: "PC-07") });

        Assert.Equal(@"\\PC-07\C$\ProgramData\KioskPlayer", Assert.Single(transfer.Directories));
    }

    [Fact]
    public void Target_path_template_replaces_the_placeholder()
    {
        var service = new DeploymentService(new FakeTransfer())
        {
            TargetPathTemplate = @"\\medienserver\kiosk\{host}"
        };

        Assert.Equal(@"\\medienserver\kiosk\PC-03", service.ResolveTarget("PC-03"));
    }

    [Fact]
    public async Task Unchanged_files_are_not_transferred_again()
    {
        var transfer = new FakeTransfer();
        transfer.UpToDate.Add(TargetFile("a.jpg"));
        var service = new DeploymentService(transfer);

        var result = Assert.Single(await service.DeployAsync(SamplePlaylist(), new[] { Pc() }));

        Assert.Equal(1, result.Copied);
        Assert.Equal(1, result.Skipped);
        Assert.Equal(900, result.BytesCopied);
    }

    [Fact]
    public async Task Obsolete_files_on_the_target_are_removed()
    {
        var transfer = new FakeTransfer();
        transfer.ExistingFiles[DefaultTarget] =
            new List<string> { "a.jpg", "alt.jpg", Playlist.FileName };

        var service = new DeploymentService(transfer);
        var result = Assert.Single(await service.DeployAsync(SamplePlaylist(), new[] { Pc() }));

        Assert.Equal(1, result.Removed);
        Assert.Equal(TargetFile("alt.jpg"), Assert.Single(transfer.Deleted));
    }

    [Fact]
    public async Task Cleanup_can_be_switched_off()
    {
        var transfer = new FakeTransfer();
        transfer.ExistingFiles[DefaultTarget] = new List<string> { "alt.jpg" };

        var service = new DeploymentService(transfer) { RemoveObsoleteFiles = false };
        await service.DeployAsync(SamplePlaylist(), new[] { Pc() });

        Assert.Empty(transfer.Deleted);
    }

    [Fact]
    public async Task Invalid_host_is_refused_before_anything_is_written()
    {
        var transfer = new FakeTransfer();
        var service = new DeploymentService(transfer);

        var result = Assert.Single(
            await service.DeployAsync(SamplePlaylist(), new[] { Pc(host: "pc 01; del") }));

        Assert.False(result.Success);
        Assert.Empty(transfer.Copied);
        Assert.Empty(transfer.Written);
    }

    [Fact]
    public async Task Dry_run_transfers_nothing()
    {
        var transfer = new FakeTransfer();
        var service = new DeploymentService(transfer) { DryRun = true };

        var result = Assert.Single(await service.DeployAsync(SamplePlaylist(), new[] { Pc() }));

        Assert.True(result.Success);
        Assert.Contains("Testbetrieb", result.Message);
        Assert.Empty(transfer.Copied);
        Assert.Empty(transfer.Written);
    }

    [Fact]
    public async Task Access_denied_becomes_a_readable_message()
    {
        var transfer = new FakeTransfer { ThrowOnCopy = new UnauthorizedAccessException("nope") };
        var service = new DeploymentService(transfer);

        var result = Assert.Single(await service.DeployAsync(SamplePlaylist(), new[] { Pc() }));

        Assert.False(result.Success);
        Assert.Contains("Administratorrechte", result.Message);
    }

    [Fact]
    public async Task Offline_pc_becomes_a_readable_message()
    {
        var transfer = new FakeTransfer { ThrowOnCopy = new DirectoryNotFoundException() };
        var service = new DeploymentService(transfer);

        var result = Assert.Single(await service.DeployAsync(SamplePlaylist(), new[] { Pc() }));

        Assert.False(result.Success);
        Assert.Contains("offline", result.Message);
    }

    [Fact]
    public async Task A_failing_pc_does_not_stop_the_others()
    {
        var transfer = new FakeTransfer();
        var service = new DeploymentService(transfer);

        var results = await service.DeployAsync(
            SamplePlaylist(),
            new[] { Pc("T1", "PC-01"), Pc("T2", "kein host!"), Pc("T3", "PC-03") });

        Assert.Equal(3, results.Count);
        Assert.Equal(2, results.Count(r => r.Success));
    }

    [Fact]
    public async Task Playlist_written_to_the_target_has_no_local_paths()
    {
        var transfer = new FakeTransfer();
        var service = new DeploymentService(transfer);

        await service.DeployAsync(SamplePlaylist(), new[] { Pc() });

        var json = transfer.Written.Values.Single();
        Assert.DoesNotContain(@"C:\M", json);

        var restored = Playlist.FromJson(json);
        Assert.Equal(2, restored!.Items.Count);
    }

    [Fact]
    public async Task Progress_is_reported_for_every_file()
    {
        var transfer = new FakeTransfer();
        var service = new DeploymentService(transfer);
        var seen = new List<DeployProgress>();

        await service.DeployAsync(SamplePlaylist(), new[] { Pc() },
            new Progress<DeployProgress>(p => { lock (seen) { seen.Add(p); } }));

        // Progress<T> meldet über den Synchronisationskontext — kurz nachfassen.
        await Task.Delay(50);

        Assert.NotEmpty(seen);
        Assert.All(seen, p => Assert.Equal("T1", p.PcName));
    }

    [Fact]
    public async Task Empty_target_list_does_nothing()
    {
        var transfer = new FakeTransfer();
        var service = new DeploymentService(transfer);

        Assert.Empty(await service.DeployAsync(SamplePlaylist(), Array.Empty<KioskPc>()));
        Assert.Empty(transfer.Directories);
    }

    [Fact]
    public void Progress_percentage_stays_in_range()
    {
        Assert.Equal(0, new DeployProgress("a", "f", 0, 1, 0, 0).Percent);
        Assert.Equal(50, new DeployProgress("a", "f", 1, 2, 50, 100).Percent);
        Assert.Equal(100, new DeployProgress("a", "f", 2, 2, 500, 100).Percent);
    }
}

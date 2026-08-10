using KioskSender.Core.Content;
using KioskSender.Core.Logging;
using KioskSender.Core.Model;
using KioskSender.Core.Remote;
using KioskSender.Core.Services;
using KioskSender.Core.Status;
using Xunit;

namespace KioskSender.Core.Tests;

internal sealed class AssignmentTransfer : IFileTransfer
{
    /// <summary>Zielordner -> geschriebene playlist.json</summary>
    public Dictionary<string, string> Playlists { get; } = new(StringComparer.OrdinalIgnoreCase);

    public List<string> Copied { get; } = new();

    public Task EnsureDirectoryAsync(string directory, CancellationToken cancellationToken = default) =>
        Task.CompletedTask;

    public Task<bool> IsUpToDateAsync(string sourceFile, string targetFile, CancellationToken cancellationToken = default) =>
        Task.FromResult(false);

    public Task CopyAsync(string sourceFile, string targetFile, CancellationToken cancellationToken = default)
    {
        Copied.Add(targetFile);
        return Task.CompletedTask;
    }

    public Task WriteAllTextAsync(string targetFile, string content, CancellationToken cancellationToken = default)
    {
        Playlists[targetFile] = content;
        return Task.CompletedTask;
    }

    public Task<IReadOnlyList<string>> ListFilesAsync(string directory, CancellationToken cancellationToken = default) =>
        Task.FromResult<IReadOnlyList<string>>(Array.Empty<string>());

    public Task DeleteAsync(string targetFile, CancellationToken cancellationToken = default) =>
        Task.CompletedTask;
}

internal sealed class AssignmentProbe : IHostProbe
{
    public Task<HostStatus> ProbeAsync(string host, int timeoutMs, CancellationToken cancellationToken = default) =>
        Task.FromResult(HostStatus.Unknown(host));
}

public class ContentAssignmentTests
{
    private static (KioskManager Manager, AssignmentTransfer Transfer, AppConfig Config) Create()
    {
        var transfer = new AssignmentTransfer();
        var config = new AppConfig();

        var manager = new KioskManager(
            config,
            new RemoteCommandService(new FakeProcessRunner()),
            new StatusMonitor(new AssignmentProbe()),
            new LogService(),
            new DeploymentService(transfer));

        return (manager, transfer, config);
    }

    private static LibraryFolder Library() => new()
    {
        Name = "Medien",
        FullPath = @"C:\Medien",
        Folders =
        {
            new LibraryFolder
            {
                Name = "Foyer",
                FullPath = @"C:\Medien\Foyer",
                Items = { new MediaItem { FileName = "foyer.jpg", Kind = MediaKind.Image, SourcePath = @"C:\Medien\Foyer\foyer.jpg", SizeBytes = 10 } }
            },
            new LibraryFolder
            {
                Name = "Kantine",
                FullPath = @"C:\Medien\Kantine",
                Items = { new MediaItem { FileName = "essen.jpg", Kind = MediaKind.Image, SourcePath = @"C:\Medien\Kantine\essen.jpg", SizeBytes = 20 } }
            }
        }
    };

    [Fact]
    public void Pc_assignment_beats_group_assignment()
    {
        var config = new AppConfig();
        var group = new PcGroup { ContentFolder = "Kantine" };
        var pc = new KioskPc { Host = "PC-01", GroupId = group.Id, ContentFolder = "Foyer" };
        config.Groups.Add(group);
        config.Pcs.Add(pc);

        Assert.Equal("Foyer", config.EffectiveContentFolder(pc));

        pc.ContentFolder = string.Empty;
        Assert.Equal("Kantine", config.EffectiveContentFolder(pc));

        group.ContentFolder = string.Empty;
        Assert.Equal(string.Empty, config.EffectiveContentFolder(pc));
    }

    [Fact]
    public void PcsWithContent_skips_disabled_and_unassigned()
    {
        var config = new AppConfig();
        config.Pcs.Add(new KioskPc { Host = "PC-01", ContentFolder = "Foyer" });
        config.Pcs.Add(new KioskPc { Host = "PC-02" });
        config.Pcs.Add(new KioskPc { Host = "PC-03", ContentFolder = "Foyer", Enabled = false });
        config.Pcs.Add(new KioskPc { Host = "", ContentFolder = "Foyer" });

        Assert.Equal(new[] { "PC-01" }, config.PcsWithContent().Select(p => p.Host).ToArray());
    }

    [Fact]
    public async Task Each_pc_receives_its_own_assigned_content()
    {
        var (manager, transfer, config) = Create();

        var foyer = new KioskPc { Name = "Foyer-PC", Host = "PC-01", ContentFolder = "Foyer" };
        var kantine = new KioskPc { Name = "Kantine-PC", Host = "PC-02", ContentFolder = "Kantine" };
        config.Pcs.Add(foyer);
        config.Pcs.Add(kantine);

        var results = await manager.DeployAssignedAsync(Library(), new[] { foyer, kantine });

        Assert.Equal(2, results.Count);
        Assert.All(results, r => Assert.True(r.Success));

        var foyerJson = transfer.Playlists.Single(p => p.Key.Contains("PC-01", StringComparison.Ordinal)).Value;
        var kantineJson = transfer.Playlists.Single(p => p.Key.Contains("PC-02", StringComparison.Ordinal)).Value;

        Assert.Contains("foyer.jpg", foyerJson);
        Assert.Contains("essen.jpg", kantineJson);
        Assert.DoesNotContain("essen.jpg", foyerJson);
    }

    [Fact]
    public async Task Pcs_sharing_an_assignment_are_handled_together()
    {
        var (manager, transfer, config) = Create();

        var a = new KioskPc { Host = "PC-01", ContentFolder = "Foyer" };
        var b = new KioskPc { Host = "PC-02", ContentFolder = "Foyer" };
        config.Pcs.Add(a);
        config.Pcs.Add(b);

        var results = await manager.DeployAssignedAsync(Library(), new[] { a, b });

        Assert.Equal(2, results.Count);
        Assert.Equal(2, transfer.Playlists.Count);
        Assert.All(transfer.Playlists.Values, json => Assert.Contains("foyer.jpg", json));
    }

    [Fact]
    public async Task Group_assignment_reaches_every_member()
    {
        var (manager, _, config) = Create();

        var group = new PcGroup { Name = "Erdgeschoss", ContentFolder = "Kantine" };
        var a = new KioskPc { Host = "PC-01", GroupId = group.Id };
        var b = new KioskPc { Host = "PC-02", GroupId = group.Id };
        config.Groups.Add(group);
        config.Pcs.Add(a);
        config.Pcs.Add(b);

        var results = await manager.DeployAssignedAsync(Library(), new[] { a, b });

        Assert.Equal(2, results.Count);
        Assert.All(results, r => Assert.True(r.Success));
    }

    [Fact]
    public async Task Pcs_without_an_assignment_are_skipped_quietly()
    {
        var (manager, transfer, config) = Create();

        var assigned = new KioskPc { Host = "PC-01", ContentFolder = "Foyer" };
        var unassigned = new KioskPc { Host = "PC-02" };
        config.Pcs.Add(assigned);
        config.Pcs.Add(unassigned);

        var results = await manager.DeployAssignedAsync(Library(), new[] { assigned, unassigned });

        Assert.Single(results);
        Assert.Single(transfer.Playlists);
    }

    [Fact]
    public async Task Nothing_assigned_at_all_reports_a_hint_instead_of_failing()
    {
        var (manager, transfer, config) = Create();
        var pc = new KioskPc { Host = "PC-01" };
        config.Pcs.Add(pc);

        var results = await manager.DeployAssignedAsync(Library(), new[] { pc });

        Assert.Empty(results);
        Assert.Empty(transfer.Playlists);
        Assert.Contains(manager.Log.Snapshot(), e => e.Message.Contains("zugeordnet"));
    }

    [Fact]
    public async Task Missing_folder_reports_per_pc_without_stopping_the_others()
    {
        var (manager, transfer, config) = Create();

        var broken = new KioskPc { Name = "Alt", Host = "PC-01", ContentFolder = "Geloescht" };
        var fine = new KioskPc { Name = "Gut", Host = "PC-02", ContentFolder = "Foyer" };
        config.Pcs.Add(broken);
        config.Pcs.Add(fine);

        var results = await manager.DeployAssignedAsync(Library(), new[] { broken, fine });

        Assert.Equal(2, results.Count);
        Assert.Single(results.Where(r => !r.Success));
        Assert.Contains("nicht gefunden", results.Single(r => !r.Success).Message);
        Assert.Single(transfer.Playlists);
    }

    [Fact]
    public async Task Successful_delivery_is_noted_on_the_pc()
    {
        var (manager, _, config) = Create();
        var pc = new KioskPc { Host = "PC-01", ContentFolder = "Foyer" };
        config.Pcs.Add(pc);

        await manager.DeployAssignedAsync(Library(), new[] { pc });

        Assert.Equal("Foyer", pc.LastContentName);
        Assert.NotNull(pc.LastContentSentAt);
    }

    [Fact]
    public async Task Dry_run_does_not_pretend_content_was_delivered()
    {
        var (manager, _, config) = Create();
        config.Settings.DryRun = true;
        manager.ApplySettings();

        var pc = new KioskPc { Host = "PC-01", ContentFolder = "Foyer" };
        config.Pcs.Add(pc);

        await manager.DeployAssignedAsync(Library(), new[] { pc });

        Assert.Null(pc.LastContentSentAt);
        Assert.Equal(string.Empty, pc.LastContentName);
    }

    [Fact]
    public void Assignments_survive_saving_and_loading()
    {
        var config = new AppConfig();
        var group = new PcGroup { ContentFolder = "Kantine" };
        config.Groups.Add(group);
        config.Pcs.Add(new KioskPc { Host = "PC-01", GroupId = group.Id, ContentFolder = "Foyer" });

        config.Normalize();

        Assert.Equal("Foyer", config.Pcs[0].ContentFolder);
        Assert.Equal("Kantine", config.Groups[0].ContentFolder);
    }
}

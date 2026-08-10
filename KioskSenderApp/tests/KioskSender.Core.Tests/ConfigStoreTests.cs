using KioskSender.Core.Model;
using KioskSender.Core.Storage;
using Xunit;

namespace KioskSender.Core.Tests;

public class ConfigStoreTests : IDisposable
{
    private readonly string _directory =
        Path.Combine(Path.GetTempPath(), "kiosksender-tests-" + Guid.NewGuid().ToString("N"));

    private string ConfigPath => Path.Combine(_directory, "config.json");

    public ConfigStoreTests() => Directory.CreateDirectory(_directory);

    public void Dispose()
    {
        try
        {
            Directory.Delete(_directory, recursive: true);
        }
        catch
        {
            // Aufräumen darf den Test nicht zum Scheitern bringen.
        }
    }

    [Fact]
    public async Task Missing_file_yields_the_sample_configuration()
    {
        var store = new ConfigStore(ConfigPath);

        var (config, warning) = await store.LoadAsync();

        Assert.Null(warning);
        Assert.NotEmpty(config.Groups);
        Assert.NotEmpty(config.Schedules);
    }

    [Fact]
    public async Task Save_and_load_roundtrip_keeps_everything()
    {
        var store = new ConfigStore(ConfigPath);
        var schedule = WeeklySchedule.CreateOfficeDefault();
        schedule.Exceptions.Add(new ScheduleException
        {
            Date = new DateOnly(2026, 12, 24),
            Closed = true,
            Note = "Heiligabend"
        });

        var group = new PcGroup { Name = "Foyer", ScheduleId = schedule.Id, ColorHex = "#FF8800" };
        var pc = new KioskPc { Name = "Terminal 1", Host = "PC-01", GroupId = group.Id };

        var original = new AppConfig
        {
            Schedules = { schedule },
            Groups = { group },
            Pcs = { pc }
        };
        original.Settings.DryRun = true;
        original.Settings.CustomCommand = @"psexec \\{host} -s cmd";

        await store.SaveAsync(original);
        var (loaded, warning) = await store.LoadAsync();

        Assert.Null(warning);
        Assert.Equal("Foyer", Assert.Single(loaded.Groups).Name);
        Assert.Equal("PC-01", Assert.Single(loaded.Pcs).Host);
        Assert.True(loaded.Settings.DryRun);
        Assert.Equal(@"psexec \\{host} -s cmd", loaded.Settings.CustomCommand);

        var loadedSchedule = Assert.Single(loaded.Schedules);
        Assert.Equal(5, loadedSchedule.Days.Count(d => d.Ranges.Count > 0));
        Assert.Equal(new DateOnly(2026, 12, 24), Assert.Single(loadedSchedule.Exceptions).Date);
        Assert.Equal(loadedSchedule.Id, Assert.Single(loaded.Groups).ScheduleId);
    }

    [Fact]
    public async Task Enums_are_stored_as_readable_text()
    {
        var store = new ConfigStore(ConfigPath);
        var schedule = WeeklySchedule.CreateOfficeDefault();
        schedule.CloseAction = KioskActionKind.Restart;

        await store.SaveAsync(new AppConfig { Schedules = { schedule } });

        var json = await File.ReadAllTextAsync(ConfigPath);
        Assert.Contains("\"Restart\"", json);
        Assert.Contains("\"Monday\"", json);
    }

    [Fact]
    public async Task Broken_file_is_quarantined_and_the_app_still_starts()
    {
        await File.WriteAllTextAsync(ConfigPath, "{ das ist kein JSON");
        var store = new ConfigStore(ConfigPath);

        var (config, warning) = await store.LoadAsync();

        Assert.NotNull(warning);
        Assert.NotNull(config);
        Assert.False(File.Exists(ConfigPath));
        Assert.NotEmpty(Directory.GetFiles(_directory, "*.broken-*"));
    }

    [Fact]
    public async Task Saving_twice_keeps_a_backup()
    {
        var store = new ConfigStore(ConfigPath);

        await store.SaveAsync(new AppConfig());
        await store.SaveAsync(new AppConfig { Pcs = { new KioskPc { Host = "PC-9" } } });

        Assert.True(File.Exists(store.BackupPath));
    }

    [Fact]
    public async Task Export_and_import_move_the_whole_configuration()
    {
        var store = new ConfigStore(ConfigPath);
        var exportPath = Path.Combine(_directory, "export.json");
        var config = new AppConfig { Pcs = { new KioskPc { Name = "T1", Host = "PC-01" } } };

        await store.ExportAsync(config, exportPath);
        var imported = await ConfigStore.ImportAsync(exportPath);

        Assert.Equal("PC-01", Assert.Single(imported!.Pcs).Host);
    }
}

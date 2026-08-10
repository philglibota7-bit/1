using KioskSender.Core.Model;
using Xunit;

namespace KioskSender.Core.Tests;

public class AppConfigTests
{
    [Fact]
    public void Normalize_clears_references_to_deleted_groups()
    {
        var config = new AppConfig
        {
            Pcs = { new KioskPc { Host = "PC-01", GroupId = Guid.NewGuid() } }
        };

        var fixes = config.Normalize();

        Assert.Equal(1, fixes);
        Assert.Null(config.Pcs[0].GroupId);
    }

    [Fact]
    public void Normalize_clears_references_to_deleted_schedules()
    {
        var group = new PcGroup { ScheduleId = Guid.NewGuid() };
        var config = new AppConfig
        {
            Groups = { group },
            Pcs = { new KioskPc { Host = "PC-01", ScheduleId = Guid.NewGuid() } }
        };

        config.Normalize();

        Assert.Null(config.Groups[0].ScheduleId);
        Assert.Null(config.Pcs[0].ScheduleId);
    }

    [Fact]
    public void Normalize_completes_missing_weekdays()
    {
        var schedule = new WeeklySchedule { Days = new List<DayPlan> { new() { Day = DayOfWeek.Monday } } };
        var config = new AppConfig { Schedules = { schedule } };

        config.Normalize();

        Assert.Equal(7, schedule.Days.Count);
    }

    [Fact]
    public void Normalize_drops_invalid_ranges()
    {
        var schedule = new WeeklySchedule();
        schedule.GetDay(DayOfWeek.Monday).Ranges.Add(new TimeRange(600, 500));
        schedule.GetDay(DayOfWeek.Monday).Ranges.Add(new TimeRange(600, 700));
        var config = new AppConfig { Schedules = { schedule } };

        config.Normalize();

        Assert.Single(schedule.GetDay(DayOfWeek.Monday).Ranges);
    }

    [Fact]
    public void Normalize_sorts_and_deduplicates_warning_minutes()
    {
        var schedule = new WeeklySchedule { WarnMinutes = new List<int> { 5, 15, 5, 0, -3 } };
        var config = new AppConfig { Schedules = { schedule } };

        config.Normalize();

        Assert.Equal(new[] { 15, 5 }, schedule.WarnMinutes);
    }

    [Fact]
    public void Normalize_clamps_unreasonable_settings()
    {
        var config = new AppConfig();
        config.Settings.StatusIntervalSeconds = 0;
        config.Settings.MaxParallelPings = 9999;
        config.Settings.PingTimeoutMs = 1;

        config.Normalize();

        Assert.Equal(5, config.Settings.StatusIntervalSeconds);
        Assert.Equal(256, config.Settings.MaxParallelPings);
        Assert.Equal(100, config.Settings.PingTimeoutMs);
    }

    [Fact]
    public void Effective_schedule_prefers_the_pc_over_the_group()
    {
        var groupSchedule = new WeeklySchedule { Name = "Gruppe" };
        var pcSchedule = new WeeklySchedule { Name = "PC" };
        var group = new PcGroup { ScheduleId = groupSchedule.Id };
        var pc = new KioskPc { Host = "PC-01", GroupId = group.Id, ScheduleId = pcSchedule.Id };

        var config = new AppConfig
        {
            Schedules = { groupSchedule, pcSchedule },
            Groups = { group },
            Pcs = { pc }
        };

        Assert.Equal("PC", config.EffectiveSchedule(pc)!.Name);

        pc.ScheduleId = null;
        Assert.Equal("Gruppe", config.EffectiveSchedule(pc)!.Name);

        pc.GroupId = null;
        Assert.Null(config.EffectiveSchedule(pc));
    }

    [Fact]
    public void DisplayName_falls_back_to_the_host()
    {
        Assert.Equal("PC-01", new KioskPc { Host = "PC-01" }.DisplayName);
        Assert.Equal("Foyer", new KioskPc { Name = "Foyer", Host = "PC-01" }.DisplayName);
    }
}

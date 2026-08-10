using KioskSender.Core.Logging;
using KioskSender.Core.Model;
using KioskSender.Core.Remote;
using KioskSender.Core.Services;
using KioskSender.Core.Status;
using Xunit;

namespace KioskSender.Core.Tests;

file sealed class NullProbe : IHostProbe
{
    public Task<HostStatus> ProbeAsync(string host, int timeoutMs, CancellationToken cancellationToken = default) =>
        Task.FromResult(HostStatus.Unknown(host));
}

public class KioskManagerTests
{
    private static (KioskManager Manager, FakeProcessRunner Runner, AppConfig Config) Create()
    {
        var runner = new FakeProcessRunner();
        var config = new AppConfig();
        var manager = new KioskManager(
            config,
            new RemoteCommandService(runner),
            new StatusMonitor(new NullProbe()),
            new LogService());

        return (manager, runner, config);
    }

    private static WeeklySchedule MondaySchedule()
    {
        var schedule = new WeeklySchedule
        {
            Name = "Montag",
            WarnMinutes = new List<int> { 15 },
            CloseAction = KioskActionKind.Shutdown,
            CloseGraceMinutes = 0
        };

        schedule.GetDay(DayOfWeek.Monday).Ranges.Add(new TimeRange(8 * 60, 17 * 60));
        return schedule;
    }

    [Fact]
    public async Task Scheduler_shuts_down_every_pc_of_the_group()
    {
        var (manager, runner, config) = Create();

        var schedule = MondaySchedule();
        var group = new PcGroup { Name = "Foyer", ScheduleId = schedule.Id };
        config.Schedules.Add(schedule);
        config.Groups.Add(group);
        config.Pcs.Add(new KioskPc { Name = "T1", Host = "PC-01", GroupId = group.Id });
        config.Pcs.Add(new KioskPc { Name = "T2", Host = "PC-02", GroupId = group.Id });

        await manager.TickAsync(new DateTime(2026, 8, 10, 16, 59, 0));
        await manager.TickAsync(new DateTime(2026, 8, 10, 17, 0, 30));

        Assert.Equal(2, runner.Calls.Count);
        Assert.All(runner.Calls, c => Assert.Equal("shutdown.exe", c.FileName));
        Assert.Contains(runner.Calls, c => c.Arguments.Contains(@"\\PC-01"));
        Assert.Contains(runner.Calls, c => c.Arguments.Contains(@"\\PC-02"));
    }

    [Fact]
    public async Task Disabled_pcs_are_skipped()
    {
        var (manager, runner, config) = Create();

        var schedule = MondaySchedule();
        var group = new PcGroup { ScheduleId = schedule.Id };
        config.Schedules.Add(schedule);
        config.Groups.Add(group);
        config.Pcs.Add(new KioskPc { Host = "PC-01", GroupId = group.Id, Enabled = false });
        config.Pcs.Add(new KioskPc { Host = "PC-02", GroupId = group.Id });

        await manager.TickAsync(new DateTime(2026, 8, 10, 16, 59, 0));
        await manager.TickAsync(new DateTime(2026, 8, 10, 17, 0, 30));

        var call = Assert.Single(runner.Calls);
        Assert.Contains(@"\\PC-02", call.Arguments);
    }

    [Fact]
    public async Task A_pc_with_its_own_schedule_ignores_the_group_schedule()
    {
        var (manager, runner, config) = Create();

        var groupSchedule = MondaySchedule();
        var ownSchedule = MondaySchedule();
        ownSchedule.Name = "Eigen";
        ownSchedule.Days[0].Ranges.Clear();
        ownSchedule.GetDay(DayOfWeek.Monday).Ranges.Add(new TimeRange(8 * 60, 12 * 60));

        var group = new PcGroup { ScheduleId = groupSchedule.Id };
        config.Schedules.Add(groupSchedule);
        config.Schedules.Add(ownSchedule);
        config.Groups.Add(group);
        config.Pcs.Add(new KioskPc { Host = "PC-01", GroupId = group.Id, ScheduleId = ownSchedule.Id });

        // 12:00 ist das Ende des eigenen Plans, nicht des Gruppenplans.
        await manager.TickAsync(new DateTime(2026, 8, 10, 11, 59, 0));
        await manager.TickAsync(new DateTime(2026, 8, 10, 12, 0, 30));

        var call = Assert.Single(runner.Calls);
        Assert.Equal("shutdown.exe", call.FileName);
    }

    [Fact]
    public async Task Scheduler_can_be_switched_off()
    {
        var (manager, runner, config) = Create();
        config.Settings.SchedulerEnabled = false;

        var schedule = MondaySchedule();
        var group = new PcGroup { ScheduleId = schedule.Id };
        config.Schedules.Add(schedule);
        config.Groups.Add(group);
        config.Pcs.Add(new KioskPc { Host = "PC-01", GroupId = group.Id });

        await manager.TickAsync(new DateTime(2026, 8, 10, 16, 59, 0));
        await manager.TickAsync(new DateTime(2026, 8, 10, 17, 0, 30));

        Assert.Empty(runner.Calls);
    }

    [Fact]
    public async Task Dry_run_only_logs()
    {
        var (manager, runner, config) = Create();
        config.Settings.DryRun = true;
        manager.ApplySettings();

        var schedule = MondaySchedule();
        var group = new PcGroup { ScheduleId = schedule.Id };
        config.Schedules.Add(schedule);
        config.Groups.Add(group);
        config.Pcs.Add(new KioskPc { Host = "PC-01", GroupId = group.Id });

        await manager.TickAsync(new DateTime(2026, 8, 10, 16, 59, 0));
        await manager.TickAsync(new DateTime(2026, 8, 10, 17, 0, 30));

        Assert.Empty(runner.Calls);
        Assert.Contains(manager.Log.Snapshot(), e => e.Message.Contains("Testbetrieb"));
    }

    [Fact]
    public async Task Warning_sends_a_message_with_the_remaining_minutes()
    {
        var (manager, runner, config) = Create();

        var schedule = MondaySchedule();
        schedule.WarnText = "Noch {minutes} Minuten!";
        var group = new PcGroup { ScheduleId = schedule.Id };
        config.Schedules.Add(schedule);
        config.Groups.Add(group);
        config.Pcs.Add(new KioskPc { Host = "PC-01", GroupId = group.Id });

        await manager.TickAsync(new DateTime(2026, 8, 10, 16, 44, 0));
        await manager.TickAsync(new DateTime(2026, 8, 10, 16, 45, 30));

        var call = Assert.Single(runner.Calls);
        Assert.Equal("msg.exe", call.FileName);
        Assert.Contains("Noch 15 Minuten!", call.Arguments);
    }

    [Fact]
    public async Task Group_without_a_schedule_produces_no_events()
    {
        var (manager, runner, config) = Create();

        var group = new PcGroup { Name = "Ohne Plan" };
        config.Groups.Add(group);
        config.Pcs.Add(new KioskPc { Host = "PC-01", GroupId = group.Id });

        await manager.TickAsync(new DateTime(2026, 8, 10, 16, 59, 0));
        await manager.TickAsync(new DateTime(2026, 8, 10, 17, 0, 30));

        Assert.Empty(runner.Calls);
        Assert.Empty(manager.BuildScheduleTargets());
    }

    [Fact]
    public async Task Manual_send_reaches_the_selected_pcs_only()
    {
        var (manager, runner, config) = Create();
        var pc1 = new KioskPc { Host = "PC-01" };
        var pc2 = new KioskPc { Host = "PC-02" };
        config.Pcs.Add(pc1);
        config.Pcs.Add(pc2);

        var results = await manager.SendAsync(new[] { pc1 }, KioskActionKind.Message, "Hallo", 30, 60);

        Assert.Single(results);
        var call = Assert.Single(runner.Calls);
        Assert.Contains("/server:PC-01", call.Arguments);
    }

    [Fact]
    public async Task Failed_commands_land_in_the_log_as_errors()
    {
        var (manager, runner, config) = Create();
        runner.Responses["msg.exe"] = new ProcessResult(1, "", "Der Netzwerkpfad wurde nicht gefunden. 53", false);
        var pc = new KioskPc { Name = "T1", Host = "PC-01" };
        config.Pcs.Add(pc);

        await manager.SendAsync(new[] { pc }, KioskActionKind.Message, "x", 30, 60);

        Assert.Contains(manager.Log.Snapshot(), e => e.Level == LogLevel.Error && e.Target == "T1");
    }

    [Fact]
    public void State_of_a_pc_uses_its_effective_schedule()
    {
        var (manager, _, config) = Create();

        var schedule = MondaySchedule();
        var group = new PcGroup { ScheduleId = schedule.Id };
        var pc = new KioskPc { Host = "PC-01", GroupId = group.Id };
        config.Schedules.Add(schedule);
        config.Groups.Add(group);
        config.Pcs.Add(pc);

        Assert.True(manager.StateOf(pc, new DateTime(2026, 8, 10, 12, 0, 0)).IsOpen);
        Assert.False(manager.StateOf(pc, new DateTime(2026, 8, 10, 20, 0, 0)).IsOpen);
    }
}

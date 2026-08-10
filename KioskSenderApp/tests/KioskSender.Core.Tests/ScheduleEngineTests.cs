using KioskSender.Core.Model;
using KioskSender.Core.Scheduling;
using Xunit;

namespace KioskSender.Core.Tests;

public class ScheduleEngineTests
{
    private static WeeklySchedule MondayOnly()
    {
        var schedule = new WeeklySchedule
        {
            Name = "Montag 08–17",
            WarnMinutes = new List<int> { 15, 5 },
            CloseAction = KioskActionKind.Shutdown,
            CloseGraceMinutes = 2
        };

        schedule.GetDay(DayOfWeek.Monday).Ranges.Add(new TimeRange(8 * 60, 17 * 60));
        return schedule;
    }

    private static ScheduleTarget Target(WeeklySchedule schedule) =>
        new("group:" + Guid.Empty, "Testgruppe", schedule);

    [Fact]
    public void First_advance_only_sets_the_baseline()
    {
        var engine = new ScheduleEngine();
        var target = Target(MondayOnly());

        var events = engine.Advance(new[] { target }, new DateTime(2026, 8, 10, 16, 44, 0));

        Assert.Empty(events);
        Assert.NotNull(engine.LastTick);
    }

    [Fact]
    public void Warning_fires_once_in_the_interval_that_contains_it()
    {
        var engine = new ScheduleEngine();
        var target = Target(MondayOnly());

        engine.Advance(new[] { target }, new DateTime(2026, 8, 10, 16, 44, 30));
        var events = engine.Advance(new[] { target }, new DateTime(2026, 8, 10, 16, 45, 30));

        var warning = Assert.Single(events);
        Assert.Equal(ScheduleEventKind.Warning, warning.Kind);
        Assert.Equal(15, warning.MinutesBefore);
        Assert.Equal(KioskActionKind.Message, warning.Action);
        Assert.Contains("15", warning.Text);

        // Der nächste Takt darf dieselbe Warnung nicht erneut auslösen.
        var again = engine.Advance(new[] { target }, new DateTime(2026, 8, 10, 16, 46, 30));
        Assert.Empty(again);
    }

    [Fact]
    public void Close_action_fires_after_the_grace_period()
    {
        var engine = new ScheduleEngine();
        var target = Target(MondayOnly());

        engine.Advance(new[] { target }, new DateTime(2026, 8, 10, 17, 1, 0));
        var events = engine.Advance(new[] { target }, new DateTime(2026, 8, 10, 17, 2, 30));

        var close = Assert.Single(events);
        Assert.Equal(ScheduleEventKind.Close, close.Kind);
        Assert.Equal(KioskActionKind.Shutdown, close.Action);
    }

    [Fact]
    public void Open_event_only_when_an_opening_text_is_configured()
    {
        var schedule = MondayOnly();
        var engine = new ScheduleEngine();

        engine.Advance(new[] { Target(schedule) }, new DateTime(2026, 8, 10, 7, 59, 0));
        Assert.Empty(engine.Advance(new[] { Target(schedule) }, new DateTime(2026, 8, 10, 8, 0, 30)));

        schedule.OpenText = "Guten Morgen";
        var engine2 = new ScheduleEngine();
        engine2.Advance(new[] { Target(schedule) }, new DateTime(2026, 8, 10, 7, 59, 0));
        var events = engine2.Advance(new[] { Target(schedule) }, new DateTime(2026, 8, 10, 8, 0, 30));

        var open = Assert.Single(events);
        Assert.Equal(ScheduleEventKind.Open, open.Kind);
        Assert.Equal("Guten Morgen", open.Text);
    }

    [Fact]
    public void Long_gap_does_not_replay_old_events()
    {
        var engine = new ScheduleEngine { MaxCatchUp = TimeSpan.FromMinutes(10) };
        var target = Target(MondayOnly());

        engine.Advance(new[] { target }, new DateTime(2026, 8, 10, 8, 0, 0));

        // Rechner war im Standby und meldet sich Stunden später zurück:
        // nur Ereignisse der letzten 10 Minuten dürfen noch kommen.
        var events = engine.Advance(new[] { target }, new DateTime(2026, 8, 10, 20, 0, 0));

        Assert.Empty(events);
    }

    [Fact]
    public void Catch_up_still_delivers_recent_events()
    {
        var engine = new ScheduleEngine { MaxCatchUp = TimeSpan.FromMinutes(10) };
        var target = Target(MondayOnly());

        engine.Advance(new[] { target }, new DateTime(2026, 8, 10, 16, 30, 0));
        var events = engine.Advance(new[] { target }, new DateTime(2026, 8, 10, 16, 50, 0));

        // 16:45 (15 Min. Vorwarnung) liegt in den letzten 10 Minuten vor 16:50.
        var warning = Assert.Single(events);
        Assert.Equal(15, warning.MinutesBefore);
    }

    [Fact]
    public void Warning_longer_than_the_window_is_skipped()
    {
        var schedule = new WeeklySchedule { WarnMinutes = new List<int> { 600 } };
        schedule.GetDay(DayOfWeek.Monday).Ranges.Add(new TimeRange(8 * 60, 9 * 60));

        var engine = new ScheduleEngine();
        var target = Target(schedule);

        engine.Advance(new[] { target }, new DateTime(2026, 8, 9, 0, 0, 0));
        var events = engine.Advance(new[] { target }, new DateTime(2026, 8, 10, 9, 0, 0));

        Assert.DoesNotContain(events, e => e.Kind == ScheduleEventKind.Warning);
    }

    [Fact]
    public void Disabled_schedule_produces_nothing()
    {
        var schedule = MondayOnly();
        schedule.Enabled = false;

        var engine = new ScheduleEngine();
        engine.Advance(new[] { Target(schedule) }, new DateTime(2026, 8, 10, 16, 44, 0));
        var events = engine.Advance(new[] { Target(schedule) }, new DateTime(2026, 8, 10, 17, 10, 0));

        Assert.Empty(events);
    }

    [Fact]
    public void Both_warnings_fire_when_the_interval_spans_them()
    {
        var engine = new ScheduleEngine { MaxCatchUp = TimeSpan.FromMinutes(30) };
        var target = Target(MondayOnly());

        engine.Advance(new[] { target }, new DateTime(2026, 8, 10, 16, 40, 0));
        var events = engine.Advance(new[] { target }, new DateTime(2026, 8, 10, 16, 56, 0));

        Assert.Equal(2, events.Count);
        Assert.Equal(new[] { 15, 5 }, events.Select(e => e.MinutesBefore).ToArray());
    }

    [Fact]
    public void Events_are_sorted_by_due_time()
    {
        var engine = new ScheduleEngine { MaxCatchUp = TimeSpan.FromHours(2) };
        var target = Target(MondayOnly());

        engine.Advance(new[] { target }, new DateTime(2026, 8, 10, 16, 0, 0));
        var events = engine.Advance(new[] { target }, new DateTime(2026, 8, 10, 17, 30, 0));

        var times = events.Select(e => e.DueAt).ToList();
        Assert.Equal(times.OrderBy(t => t).ToList(), times);
    }

    [Fact]
    public void FormatWarnText_replaces_the_placeholder()
    {
        Assert.Equal("noch 5 Minuten", ScheduleEngine.FormatWarnText("noch {minutes} Minuten", 5));
        Assert.Equal("noch 5 Minuten", ScheduleEngine.FormatWarnText("noch {minuten} Minuten", 5));
        Assert.Contains("7", ScheduleEngine.FormatWarnText("", 7));
    }
}

using KioskSender.Core.Model;
using KioskSender.Core.Scheduling;
using Xunit;

namespace KioskSender.Core.Tests;

public class ScheduleEvaluatorTests
{
    private static WeeklySchedule Weekdays8To17()
    {
        var schedule = new WeeklySchedule { Name = "Test" };
        foreach (var day in new[] { DayOfWeek.Monday, DayOfWeek.Tuesday, DayOfWeek.Wednesday, DayOfWeek.Thursday, DayOfWeek.Friday })
        {
            schedule.GetDay(day).Ranges.Add(new TimeRange(8 * 60, 17 * 60));
        }

        return schedule;
    }

    // 2026-08-10 ist ein Montag.
    private static readonly DateTime MondayNoon = new(2026, 8, 10, 12, 0, 0);

    [Fact]
    public void Open_during_window()
    {
        var state = ScheduleEvaluator.Evaluate(Weekdays8To17(), MondayNoon);

        Assert.True(state.IsOpen);
        Assert.NotNull(state.Current);
        Assert.Equal(new DateTime(2026, 8, 10, 8, 0, 0), state.Current!.Start);
        Assert.Equal(new DateTime(2026, 8, 10, 17, 0, 0), state.Current.End);
        Assert.Equal(300, state.MinutesUntilClose(MondayNoon));
    }

    [Fact]
    public void Closed_before_window_and_reports_next_opening()
    {
        var early = new DateTime(2026, 8, 10, 6, 30, 0);
        var state = ScheduleEvaluator.Evaluate(Weekdays8To17(), early);

        Assert.False(state.IsOpen);
        Assert.Equal(new DateTime(2026, 8, 10, 8, 0, 0), state.Next!.Start);
        Assert.Equal(90, state.MinutesUntilOpen(early));
    }

    [Fact]
    public void Weekend_jumps_to_monday()
    {
        var saturday = new DateTime(2026, 8, 15, 12, 0, 0);
        var state = ScheduleEvaluator.Evaluate(Weekdays8To17(), saturday);

        Assert.False(state.IsOpen);
        Assert.Equal(new DateTime(2026, 8, 17, 8, 0, 0), state.Next!.Start);
    }

    [Fact]
    public void Window_across_midnight_is_still_open_after_midnight()
    {
        var schedule = new WeeklySchedule();
        schedule.GetDay(DayOfWeek.Monday).Ranges.Add(new TimeRange(20 * 60, 26 * 60)); // 20:00–02:00

        var tuesdayNight = new DateTime(2026, 8, 11, 1, 30, 0);
        var state = ScheduleEvaluator.Evaluate(schedule, tuesdayNight);

        Assert.True(state.IsOpen);
        Assert.Equal(new DateTime(2026, 8, 11, 2, 0, 0), state.Current!.End);
    }

    [Fact]
    public void Overlapping_ranges_are_merged_into_one_window()
    {
        var schedule = new WeeklySchedule();
        var monday = schedule.GetDay(DayOfWeek.Monday);
        monday.Ranges.Add(new TimeRange(8 * 60, 12 * 60));
        monday.Ranges.Add(new TimeRange(11 * 60, 17 * 60));

        var windows = ScheduleEvaluator.GetWindows(
            schedule,
            new DateTime(2026, 8, 10),
            new DateTime(2026, 8, 11));

        Assert.Single(windows);
        Assert.Equal(new DateTime(2026, 8, 10, 8, 0, 0), windows[0].Start);
        Assert.Equal(new DateTime(2026, 8, 10, 17, 0, 0), windows[0].End);
    }

    [Fact]
    public void Adjacent_ranges_are_merged()
    {
        var schedule = new WeeklySchedule();
        var monday = schedule.GetDay(DayOfWeek.Monday);
        monday.Ranges.Add(new TimeRange(8 * 60, 12 * 60));
        monday.Ranges.Add(new TimeRange(12 * 60, 17 * 60));

        var windows = ScheduleEvaluator.GetWindows(
            schedule,
            new DateTime(2026, 8, 10),
            new DateTime(2026, 8, 11));

        Assert.Single(windows);
    }

    [Fact]
    public void Separate_ranges_stay_separate()
    {
        var schedule = new WeeklySchedule();
        var monday = schedule.GetDay(DayOfWeek.Monday);
        monday.Ranges.Add(new TimeRange(8 * 60, 12 * 60));
        monday.Ranges.Add(new TimeRange(13 * 60, 17 * 60));

        var windows = ScheduleEvaluator.GetWindows(
            schedule,
            new DateTime(2026, 8, 10),
            new DateTime(2026, 8, 11));

        Assert.Equal(2, windows.Count);
    }

    [Fact]
    public void Closed_exception_removes_the_day()
    {
        var schedule = Weekdays8To17();
        schedule.Exceptions.Add(new ScheduleException
        {
            Date = new DateOnly(2026, 8, 10),
            Closed = true,
            Note = "Feiertag"
        });

        var state = ScheduleEvaluator.Evaluate(schedule, MondayNoon);

        Assert.False(state.IsOpen);
        Assert.Equal(new DateTime(2026, 8, 11, 8, 0, 0), state.Next!.Start);
    }

    [Fact]
    public void Special_hours_exception_replaces_the_day()
    {
        var schedule = Weekdays8To17();
        schedule.Exceptions.Add(new ScheduleException
        {
            Date = new DateOnly(2026, 8, 10),
            Closed = false,
            Ranges = { new TimeRange(10 * 60, 13 * 60) },
            Note = "Kurztag"
        });

        var state = ScheduleEvaluator.Evaluate(schedule, MondayNoon);

        Assert.True(state.IsOpen);
        Assert.Equal(new DateTime(2026, 8, 10, 13, 0, 0), state.Current!.End);
    }

    [Fact]
    public void Disabled_schedule_is_never_open()
    {
        var schedule = Weekdays8To17();
        schedule.Enabled = false;

        Assert.False(ScheduleEvaluator.Evaluate(schedule, MondayNoon).IsOpen);
    }

    [Fact]
    public void Null_schedule_is_closed()
    {
        Assert.False(ScheduleEvaluator.Evaluate(null, MondayNoon).IsOpen);
    }
}

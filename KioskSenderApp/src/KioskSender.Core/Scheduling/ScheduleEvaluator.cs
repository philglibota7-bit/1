using KioskSender.Core.Model;

namespace KioskSender.Core.Scheduling;

/// <summary>Ein konkretes Zeitfenster mit absoluten Zeitpunkten.</summary>
public sealed record ScheduleWindow(DateTime Start, DateTime End)
{
    public bool Contains(DateTime moment) => moment >= Start && moment < End;

    public TimeSpan Duration => End - Start;

    public override string ToString() => $"{Start:dd.MM. HH:mm} – {End:dd.MM. HH:mm}";
}

/// <summary>Der Zustand eines Zeitplans zu einem Zeitpunkt.</summary>
public sealed record ScheduleState(
    bool IsOpen,
    ScheduleWindow? Current,
    ScheduleWindow? Next)
{
    public static readonly ScheduleState Closed = new(false, null, null);

    /// <summary>Minuten bis zur Schließung, wenn gerade geöffnet ist.</summary>
    public double? MinutesUntilClose(DateTime now) =>
        IsOpen && Current is not null ? (Current.End - now).TotalMinutes : null;

    /// <summary>Minuten bis zur nächsten Öffnung, wenn gerade geschlossen ist.</summary>
    public double? MinutesUntilOpen(DateTime now) =>
        !IsOpen && Next is not null ? (Next.Start - now).TotalMinutes : null;
}

/// <summary>
/// Rechnet ein Wochenraster samt Ausnahmetagen in absolute Zeitfenster um.
/// Bewusst zustandslos und ohne Systemuhr, damit alles testbar bleibt.
/// </summary>
public static class ScheduleEvaluator
{
    /// <summary>
    /// Alle Zeitfenster, die sich mit [from, to) überschneiden — zusammengefasst,
    /// falls sie sich berühren oder überlappen.
    /// </summary>
    public static IReadOnlyList<ScheduleWindow> GetWindows(WeeklySchedule schedule, DateTime from, DateTime to)
    {
        if (schedule is null || to <= from)
        {
            return Array.Empty<ScheduleWindow>();
        }

        // Ein Tag Vorlauf, damit Fenster über Mitternacht (z. B. 20:00–02:00)
        // auch dann gefunden werden, wenn sie am Vortag beginnen.
        var firstDay = DateOnly.FromDateTime(from.Date.AddDays(-1));
        var lastDay = DateOnly.FromDateTime(to.Date);

        var windows = new List<ScheduleWindow>();
        for (var day = firstDay; day <= lastDay; day = day.AddDays(1))
        {
            foreach (var range in RangesForDate(schedule, day))
            {
                if (!range.IsValid)
                {
                    continue;
                }

                var dayStart = day.ToDateTime(TimeOnly.MinValue);
                var start = dayStart.AddMinutes(range.StartMinutes);
                var end = dayStart.AddMinutes(range.EndMinutes);

                if (end > from && start < to)
                {
                    windows.Add(new ScheduleWindow(start, end));
                }
            }
        }

        return Merge(windows);
    }

    /// <summary>Die für ein Datum gültigen Zeitspannen (Ausnahme schlägt Wochentag).</summary>
    public static IReadOnlyList<TimeRange> RangesForDate(WeeklySchedule schedule, DateOnly date)
    {
        var exception = schedule.FindException(date);
        if (exception is not null)
        {
            return exception.Closed ? Array.Empty<TimeRange>() : exception.Ranges;
        }

        var day = schedule.Days.FirstOrDefault(d => d.Day == date.DayOfWeek);
        return day?.Ranges ?? (IReadOnlyList<TimeRange>)Array.Empty<TimeRange>();
    }

    /// <summary>Zustand des Zeitplans zum Zeitpunkt <paramref name="now"/>.</summary>
    public static ScheduleState Evaluate(WeeklySchedule? schedule, DateTime now, int lookaheadDays = 14)
    {
        if (schedule is null || !schedule.Enabled)
        {
            return ScheduleState.Closed;
        }

        var windows = GetWindows(schedule, now.AddDays(-1), now.AddDays(lookaheadDays));

        var current = windows.FirstOrDefault(w => w.Contains(now));
        var next = windows.FirstOrDefault(w => w.Start > now);

        return new ScheduleState(current is not null, current, next);
    }

    /// <summary>Überlappende oder direkt aneinandergrenzende Fenster verschmelzen.</summary>
    private static List<ScheduleWindow> Merge(List<ScheduleWindow> windows)
    {
        if (windows.Count <= 1)
        {
            return windows;
        }

        windows.Sort((a, b) => a.Start.CompareTo(b.Start));

        var merged = new List<ScheduleWindow>(windows.Count) { windows[0] };
        foreach (var window in windows.Skip(1))
        {
            var last = merged[^1];
            if (window.Start <= last.End)
            {
                if (window.End > last.End)
                {
                    merged[^1] = last with { End = window.End };
                }
            }
            else
            {
                merged.Add(window);
            }
        }

        return merged;
    }
}

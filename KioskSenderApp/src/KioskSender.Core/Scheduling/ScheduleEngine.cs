using KioskSender.Core.Model;

namespace KioskSender.Core.Scheduling;

public enum ScheduleEventKind
{
    /// <summary>Zeitfenster hat begonnen.</summary>
    Open,

    /// <summary>Vorwarnung vor der Schließung.</summary>
    Warning,

    /// <summary>Zeitfenster ist zu Ende — Schließ-Aktion fällig.</summary>
    Close
}

/// <summary>Ein Ziel, für das der Zeitmanager Ereignisse erzeugt (Gruppe oder Einzel-PC).</summary>
public sealed record ScheduleTarget(string Id, string DisplayName, WeeklySchedule Schedule);

/// <summary>Ein fälliges Ereignis, das die Anwendung nun ausführen soll.</summary>
public sealed record ScheduleEvent(
    ScheduleTarget Target,
    ScheduleEventKind Kind,
    DateTime DueAt,
    ScheduleWindow Window,
    int MinutesBefore,
    KioskActionKind Action,
    string Text)
{
    public override string ToString() =>
        $"{DueAt:HH:mm} {Kind} {Target.DisplayName} ({Action.ToDisplayName()})";
}

/// <summary>
/// Erzeugt aus Zeitplänen die fälligen Ereignisse zwischen zwei Takten.
/// Rein funktional gehalten: die Klasse merkt sich nur den letzten Takt und
/// ruft nie die Systemuhr auf — dadurch vollständig testbar.
/// </summary>
public sealed class ScheduleEngine
{
    private DateTime? _lastTick;

    /// <summary>
    /// Verhindert, dass nach längerem Stillstand (Standby, App war zu) alte
    /// Ereignisse nachträglich ausgelöst werden.
    /// </summary>
    public TimeSpan MaxCatchUp { get; set; } = TimeSpan.FromMinutes(10);

    public DateTime? LastTick => _lastTick;

    /// <summary>Setzt die Uhr, ohne Ereignisse auszulösen (z. B. nach Konfigurationswechsel).</summary>
    public void Reset(DateTime now) => _lastTick = now;

    /// <summary>
    /// Liefert alle Ereignisse, die seit dem letzten Aufruf fällig geworden sind.
    /// Der erste Aufruf liefert nie Ereignisse, sondern setzt nur den Startpunkt.
    /// </summary>
    public IReadOnlyList<ScheduleEvent> Advance(IEnumerable<ScheduleTarget> targets, DateTime now)
    {
        var previous = _lastTick;
        _lastTick = now;

        if (previous is null || now <= previous.Value)
        {
            return Array.Empty<ScheduleEvent>();
        }

        var from = previous.Value;
        if (now - from > MaxCatchUp)
        {
            from = now - MaxCatchUp;
        }

        var due = new List<ScheduleEvent>();

        foreach (var target in targets)
        {
            var schedule = target.Schedule;
            if (schedule is null || !schedule.Enabled)
            {
                continue;
            }

            // Etwas Puffer nach vorn und hinten, damit Fenster, deren Warnung oder
            // Karenzzeit in das Intervall fällt, sicher erfasst werden.
            var windows = ScheduleEvaluator.GetWindows(
                schedule,
                from.AddDays(-1),
                now.AddDays(1));

            foreach (var window in windows)
            {
                AddIfDue(due, target, ScheduleEventKind.Open, window.Start, window, 0,
                    string.IsNullOrWhiteSpace(schedule.OpenText) ? KioskActionKind.None : KioskActionKind.Message,
                    schedule.OpenText, from, now);

                foreach (var minutes in schedule.WarnMinutes)
                {
                    if (minutes <= 0)
                    {
                        continue;
                    }

                    var dueAt = window.End.AddMinutes(-minutes);
                    if (dueAt <= window.Start)
                    {
                        // Warnung läge vor dem Fensterbeginn — überspringen.
                        continue;
                    }

                    AddIfDue(due, target, ScheduleEventKind.Warning, dueAt, window, minutes,
                        KioskActionKind.Message, FormatWarnText(schedule.WarnText, minutes), from, now);
                }

                AddIfDue(due, target, ScheduleEventKind.Close,
                    window.End.AddMinutes(Math.Max(0, schedule.CloseGraceMinutes)), window, 0,
                    schedule.CloseAction, string.Empty, from, now);
            }
        }

        due.Sort((a, b) => a.DueAt.CompareTo(b.DueAt));
        return due;
    }

    private static void AddIfDue(
        List<ScheduleEvent> sink,
        ScheduleTarget target,
        ScheduleEventKind kind,
        DateTime dueAt,
        ScheduleWindow window,
        int minutesBefore,
        KioskActionKind action,
        string text,
        DateTime from,
        DateTime to)
    {
        if (action == KioskActionKind.None)
        {
            return;
        }

        if (dueAt > from && dueAt <= to)
        {
            sink.Add(new ScheduleEvent(target, kind, dueAt, window, minutesBefore, action, text));
        }
    }

    public static string FormatWarnText(string template, int minutes)
    {
        if (string.IsNullOrWhiteSpace(template))
        {
            return $"Dieser PC wird in {minutes} Minuten heruntergefahren.";
        }

        return template
            .Replace("{minutes}", minutes.ToString())
            .Replace("{minuten}", minutes.ToString());
    }
}

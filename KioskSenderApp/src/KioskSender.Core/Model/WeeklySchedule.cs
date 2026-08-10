namespace KioskSender.Core.Model;

/// <summary>Öffnungszeiten eines Wochentags.</summary>
public sealed class DayPlan
{
    public DayOfWeek Day { get; set; }

    public List<TimeRange> Ranges { get; set; } = new();

    public DayPlan Clone() => new()
    {
        Day = Day,
        Ranges = Ranges.Select(r => r.Clone()).ToList()
    };
}

/// <summary>Ausnahme für ein konkretes Datum (Feiertag, Sondertermin).</summary>
public sealed class ScheduleException
{
    public DateOnly Date { get; set; }

    /// <summary>An diesem Tag ist komplett geschlossen.</summary>
    public bool Closed { get; set; } = true;

    /// <summary>Ersetzt die Zeiten des Wochentags, wenn <see cref="Closed"/> false ist.</summary>
    public List<TimeRange> Ranges { get; set; } = new();

    public string Note { get; set; } = string.Empty;

    public ScheduleException Clone() => new()
    {
        Date = Date,
        Closed = Closed,
        Ranges = Ranges.Select(r => r.Clone()).ToList(),
        Note = Note
    };
}

/// <summary>
/// Ein Zeitplan des Zeitmanagers: Wochenraster, Ausnahmetage, Vorwarnungen und
/// die Aktion, die beim Schließen ausgeführt wird.
/// </summary>
public sealed class WeeklySchedule
{
    public Guid Id { get; set; } = Guid.NewGuid();

    public string Name { get; set; } = "Neuer Zeitplan";

    public bool Enabled { get; set; } = true;

    public List<DayPlan> Days { get; set; } = CreateEmptyWeek();

    public List<ScheduleException> Exceptions { get; set; } = new();

    /// <summary>Minuten vor Schließung, zu denen eine Warnmeldung gesendet wird.</summary>
    public List<int> WarnMinutes { get; set; } = new() { 15, 5 };

    public string WarnText { get; set; } = "Achtung: Dieser PC wird in {minutes} Minuten heruntergefahren. Bitte jetzt speichern.";

    public KioskActionKind CloseAction { get; set; } = KioskActionKind.Shutdown;

    /// <summary>Karenzzeit nach Fensterende, bevor die Schließ-Aktion läuft.</summary>
    public int CloseGraceMinutes { get; set; } = 2;

    /// <summary>Sekunden Countdown, den shutdown.exe dem Benutzer noch lässt.</summary>
    public int CloseCountdownSeconds { get; set; } = 60;

    /// <summary>Meldung beim Öffnen des Zeitfensters (leer = keine Meldung).</summary>
    public string OpenText { get; set; } = string.Empty;

    public static List<DayPlan> CreateEmptyWeek() =>
        WeekDaysInOrder.Select(d => new DayPlan { Day = d }).ToList();

    /// <summary>Montag zuerst — so wie ein deutscher Kalender gelesen wird.</summary>
    public static readonly DayOfWeek[] WeekDaysInOrder =
    {
        DayOfWeek.Monday,
        DayOfWeek.Tuesday,
        DayOfWeek.Wednesday,
        DayOfWeek.Thursday,
        DayOfWeek.Friday,
        DayOfWeek.Saturday,
        DayOfWeek.Sunday
    };

    public DayPlan GetDay(DayOfWeek day)
    {
        var plan = Days.FirstOrDefault(d => d.Day == day);
        if (plan is null)
        {
            plan = new DayPlan { Day = day };
            Days.Add(plan);
        }

        return plan;
    }

    public ScheduleException? FindException(DateOnly date) =>
        Exceptions.FirstOrDefault(e => e.Date == date);

    public WeeklySchedule Clone() => new()
    {
        Id = Id,
        Name = Name,
        Enabled = Enabled,
        Days = Days.Select(d => d.Clone()).ToList(),
        Exceptions = Exceptions.Select(e => e.Clone()).ToList(),
        WarnMinutes = WarnMinutes.ToList(),
        WarnText = WarnText,
        CloseAction = CloseAction,
        CloseGraceMinutes = CloseGraceMinutes,
        CloseCountdownSeconds = CloseCountdownSeconds,
        OpenText = OpenText
    };

    /// <summary>Vorlage: Mo–Fr 08:00–17:00.</summary>
    public static WeeklySchedule CreateOfficeDefault()
    {
        var schedule = new WeeklySchedule { Name = "Bürozeiten (Mo–Fr 08–17)" };
        foreach (var day in new[] { DayOfWeek.Monday, DayOfWeek.Tuesday, DayOfWeek.Wednesday, DayOfWeek.Thursday, DayOfWeek.Friday })
        {
            schedule.GetDay(day).Ranges.Add(new TimeRange(8 * 60, 17 * 60));
        }

        return schedule;
    }
}

namespace KioskSender.Core.Model;

/// <summary>Der komplette persistierte Zustand der Anwendung.</summary>
public sealed class AppConfig
{
    /// <summary>Schemaversion — erlaubt spätere Migrationen.</summary>
    public int Version { get; set; } = 1;

    public AppSettings Settings { get; set; } = new();

    public List<PcGroup> Groups { get; set; } = new();

    public List<KioskPc> Pcs { get; set; } = new();

    public List<WeeklySchedule> Schedules { get; set; } = new();

    public PcGroup? FindGroup(Guid? id) =>
        id is null ? null : Groups.FirstOrDefault(g => g.Id == id.Value);

    public WeeklySchedule? FindSchedule(Guid? id) =>
        id is null ? null : Schedules.FirstOrDefault(s => s.Id == id.Value);

    public KioskPc? FindPc(Guid id) => Pcs.FirstOrDefault(p => p.Id == id);

    public IEnumerable<KioskPc> PcsInGroup(Guid groupId) =>
        Pcs.Where(p => p.GroupId == groupId);

    /// <summary>
    /// Der wirksame Zeitplan eines PCs: eigener Plan vor Gruppenplan.
    /// </summary>
    public WeeklySchedule? EffectiveSchedule(KioskPc pc)
    {
        var own = FindSchedule(pc.ScheduleId);
        if (own is not null)
        {
            return own;
        }

        var group = FindGroup(pc.GroupId);
        return group is null ? null : FindSchedule(group.ScheduleId);
    }

    /// <summary>
    /// Welchen Inhalt ein PC zeigen soll: eigene Zuordnung vor Gruppenzuordnung.
    /// Leer heißt, dass für diesen PC nichts festgelegt ist.
    /// </summary>
    public string EffectiveContentFolder(KioskPc pc)
    {
        if (!string.IsNullOrWhiteSpace(pc.ContentFolder))
        {
            return pc.ContentFolder.Trim();
        }

        var group = FindGroup(pc.GroupId);
        return string.IsNullOrWhiteSpace(group?.ContentFolder)
            ? string.Empty
            : group!.ContentFolder.Trim();
    }

    /// <summary>Alle aktiven PCs, denen ein Inhalt zugeordnet ist.</summary>
    public IEnumerable<KioskPc> PcsWithContent() =>
        Pcs.Where(p => p.Enabled
                       && !string.IsNullOrWhiteSpace(p.Host)
                       && !string.IsNullOrWhiteSpace(EffectiveContentFolder(p)));

    /// <summary>
    /// Repariert verwaiste Verweise (gelöschte Gruppe/Zeitplan) und ergänzt
    /// fehlende Wochentage. Gibt die Anzahl der Korrekturen zurück.
    /// </summary>
    public int Normalize()
    {
        var fixes = 0;

        var groupIds = Groups.Select(g => g.Id).ToHashSet();
        var scheduleIds = Schedules.Select(s => s.Id).ToHashSet();

        foreach (var pc in Pcs)
        {
            if (pc.GroupId is { } gid && !groupIds.Contains(gid))
            {
                pc.GroupId = null;
                fixes++;
            }

            if (pc.ScheduleId is { } sid && !scheduleIds.Contains(sid))
            {
                pc.ScheduleId = null;
                fixes++;
            }
        }

        foreach (var group in Groups)
        {
            if (group.ScheduleId is { } sid && !scheduleIds.Contains(sid))
            {
                group.ScheduleId = null;
                fixes++;
            }
        }

        foreach (var schedule in Schedules)
        {
            foreach (var day in WeeklySchedule.WeekDaysInOrder)
            {
                if (schedule.Days.All(d => d.Day != day))
                {
                    schedule.Days.Add(new DayPlan { Day = day });
                    fixes++;
                }
            }

            var invalid = schedule.Days
                .SelectMany(d => d.Ranges)
                .Count(r => !r.IsValid);
            if (invalid > 0)
            {
                foreach (var day in schedule.Days)
                {
                    day.Ranges.RemoveAll(r => !r.IsValid);
                }

                fixes += invalid;
            }

            schedule.WarnMinutes = schedule.WarnMinutes
                .Where(m => m > 0)
                .Distinct()
                .OrderByDescending(m => m)
                .ToList();
        }

        var index = 0;
        foreach (var group in Groups.OrderBy(g => g.SortIndex).ThenBy(g => g.Name, StringComparer.CurrentCultureIgnoreCase))
        {
            group.SortIndex = index++;
        }

        Settings.StatusIntervalSeconds = Math.Clamp(Settings.StatusIntervalSeconds, 5, 3600);
        Settings.SchedulerTickSeconds = Math.Clamp(Settings.SchedulerTickSeconds, 5, 300);
        Settings.PingTimeoutMs = Math.Clamp(Settings.PingTimeoutMs, 100, 10_000);
        Settings.MaxParallelPings = Math.Clamp(Settings.MaxParallelPings, 1, 256);
        Settings.CommandTimeoutSeconds = Math.Clamp(Settings.CommandTimeoutSeconds, 5, 300);
        Settings.LogCapacity = Math.Clamp(Settings.LogCapacity, 100, 100_000);
        Settings.DefaultImageSeconds = Math.Clamp(Settings.DefaultImageSeconds, 1, 3600);
        Settings.MaxParallelTransfers = Math.Clamp(Settings.MaxParallelTransfers, 1, 16);

        if (string.IsNullOrWhiteSpace(Settings.ContentTargetTemplate))
        {
            Settings.ContentTargetTemplate = @"\\{host}\C$\ProgramData\KioskPlayer";
        }

        return fixes;
    }

    /// <summary>Startkonfiguration für den ersten Programmstart.</summary>
    public static AppConfig CreateSample()
    {
        var schedule = WeeklySchedule.CreateOfficeDefault();
        var group = new PcGroup
        {
            Name = "Beispiel-Gruppe",
            ColorHex = "#4C8DFF",
            ScheduleId = schedule.Id,
            Note = "Gruppen anlegen, PCs zuordnen, Zeitplan wählen."
        };

        return new AppConfig
        {
            Schedules = { schedule },
            Groups = { group }
        };
    }
}

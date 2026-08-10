using KioskSender.Core.Logging;
using KioskSender.Core.Model;
using KioskSender.Core.Remote;
using KioskSender.Core.Scheduling;
using KioskSender.Core.Status;

namespace KioskSender.Core.Services;

/// <summary>
/// Klammert Konfiguration, Zeitmanager, Sender und Statusprüfung zusammen.
/// Enthält keine Oberflächen- und keine Timer-Logik: die Takte kommen von außen,
/// damit sich alles ohne laufende Uhr testen lässt.
/// </summary>
public sealed class KioskManager
{
    private readonly ScheduleEngine _engine = new();
    private readonly RemoteCommandService _remote;
    private readonly StatusMonitor _monitor;
    private readonly LogService _log;

    public KioskManager(
        AppConfig config,
        RemoteCommandService remote,
        StatusMonitor monitor,
        LogService log)
    {
        Config = config;
        _remote = remote;
        _monitor = monitor;
        _log = log;
        ApplySettings();
    }

    public AppConfig Config { get; private set; }

    public StatusMonitor Monitor => _monitor;

    public LogService Log => _log;

    /// <summary>Wird nach jedem Zeitmanager-Ereignis ausgelöst (für die Oberfläche).</summary>
    public event EventHandler<ScheduleEvent>? ScheduleEventFired;

    public void ReplaceConfig(AppConfig config)
    {
        Config = config;
        ApplySettings();
        _engine.Reset(DateTime.Now);
    }

    /// <summary>Überträgt die Einstellungen an die beteiligten Dienste.</summary>
    public void ApplySettings()
    {
        var settings = Config.Settings;
        _remote.DryRun = settings.DryRun;
        _remote.Timeout = TimeSpan.FromSeconds(settings.CommandTimeoutSeconds);
        _remote.CustomCommandTemplate = settings.CustomCommand;
        _monitor.TimeoutMs = settings.PingTimeoutMs;
        _monitor.MaxParallel = settings.MaxParallelPings;
        _log.Capacity = settings.LogCapacity;
    }

    // ---------------------------------------------------------------- Ziele

    /// <summary>Alle aktiven PCs mit gültigem Host.</summary>
    public IReadOnlyList<KioskPc> ActivePcs() =>
        Config.Pcs.Where(p => p.Enabled && !string.IsNullOrWhiteSpace(p.Host)).ToList();

    /// <summary>
    /// Die Ziele des Zeitmanagers: jede Gruppe mit Zeitplan sowie jeder PC,
    /// der einen eigenen Zeitplan hat.
    /// </summary>
    public IReadOnlyList<ScheduleTarget> BuildScheduleTargets()
    {
        var targets = new List<ScheduleTarget>();

        foreach (var group in Config.Groups)
        {
            var schedule = Config.FindSchedule(group.ScheduleId);
            if (schedule is null)
            {
                continue;
            }

            var hasMembers = Config.Pcs.Any(p => p.Enabled && p.GroupId == group.Id && p.ScheduleId is null);
            if (hasMembers)
            {
                targets.Add(new ScheduleTarget("group:" + group.Id, group.Name, schedule));
            }
        }

        foreach (var pc in Config.Pcs.Where(p => p.Enabled && p.ScheduleId is not null))
        {
            var schedule = Config.FindSchedule(pc.ScheduleId);
            if (schedule is not null)
            {
                targets.Add(new ScheduleTarget("pc:" + pc.Id, pc.DisplayName, schedule));
            }
        }

        return targets;
    }

    /// <summary>Löst ein Zeitmanager-Ziel in die betroffenen PCs auf.</summary>
    public IReadOnlyList<KioskPc> ResolveTarget(ScheduleTarget target)
    {
        var parts = target.Id.Split(':', 2);
        if (parts.Length != 2 || !Guid.TryParse(parts[1], out var id))
        {
            return Array.Empty<KioskPc>();
        }

        return parts[0] switch
        {
            "group" => Config.Pcs
                .Where(p => p.Enabled && p.GroupId == id && p.ScheduleId is null && !string.IsNullOrWhiteSpace(p.Host))
                .ToList(),
            "pc" => Config.Pcs
                .Where(p => p.Enabled && p.Id == id && !string.IsNullOrWhiteSpace(p.Host))
                .ToList(),
            _ => Array.Empty<KioskPc>()
        };
    }

    /// <summary>Zustand eines PCs laut seinem wirksamen Zeitplan.</summary>
    public ScheduleState StateOf(KioskPc pc, DateTime now) =>
        ScheduleEvaluator.Evaluate(Config.EffectiveSchedule(pc), now);

    // ----------------------------------------------------------- Zeitmanager

    /// <summary>Verhindert doppelte Ausführung, falls ein Takt länger dauert als das Intervall.</summary>
    private int _tickRunning;

    /// <summary>
    /// Ein Takt des Zeitmanagers: fällige Ereignisse ermitteln und ausführen.
    /// Der erste Aufruf setzt nur den Startpunkt.
    /// </summary>
    public async Task<IReadOnlyList<ScheduleEvent>> TickAsync(DateTime now, CancellationToken cancellationToken = default)
    {
        if (Interlocked.Exchange(ref _tickRunning, 1) == 1)
        {
            return Array.Empty<ScheduleEvent>();
        }

        try
        {
            if (!Config.Settings.SchedulerEnabled)
            {
                _engine.Reset(now);
                return Array.Empty<ScheduleEvent>();
            }

            var events = _engine.Advance(BuildScheduleTargets(), now);

            foreach (var scheduleEvent in events)
            {
                cancellationToken.ThrowIfCancellationRequested();
                await ExecuteScheduleEventAsync(scheduleEvent, cancellationToken).ConfigureAwait(false);
            }

            return events;
        }
        finally
        {
            Interlocked.Exchange(ref _tickRunning, 0);
        }
    }

    private async Task ExecuteScheduleEventAsync(ScheduleEvent scheduleEvent, CancellationToken cancellationToken)
    {
        var pcs = ResolveTarget(scheduleEvent.Target);
        if (pcs.Count == 0)
        {
            return;
        }

        var schedule = scheduleEvent.Target.Schedule;
        var label = scheduleEvent.Kind switch
        {
            ScheduleEventKind.Open => "Zeitfenster geöffnet",
            ScheduleEventKind.Warning => $"Vorwarnung {scheduleEvent.MinutesBefore} Min.",
            _ => "Zeitfenster beendet"
        };

        _log.Info("Zeitmanager",
            $"{label} – {scheduleEvent.Action.ToDisplayName()} für {pcs.Count} PC(s), Fenster {scheduleEvent.Window}.",
            scheduleEvent.Target.DisplayName);

        var text = scheduleEvent.Kind == ScheduleEventKind.Close
            ? $"Betriebszeit beendet ({schedule.Name})."
            : scheduleEvent.Text;

        var results = await SendAsync(
            pcs,
            scheduleEvent.Action,
            text,
            schedule.CloseCountdownSeconds,
            Config.Settings.MessageDisplaySeconds,
            "Zeitmanager",
            cancellationToken).ConfigureAwait(false);

        _ = results;
        ScheduleEventFired?.Invoke(this, scheduleEvent);
    }

    // ---------------------------------------------------------------- Sender

    /// <summary>Führt eine Aktion auf mehreren PCs aus und protokolliert jedes Ergebnis.</summary>
    public async Task<IReadOnlyList<RemoteResult>> SendAsync(
        IEnumerable<KioskPc> targets,
        KioskActionKind action,
        string text,
        int countdownSeconds,
        int messageSeconds,
        string source = "Sender",
        CancellationToken cancellationToken = default)
    {
        var list = targets.Where(p => !string.IsNullOrWhiteSpace(p.Host)).ToList();
        if (list.Count == 0)
        {
            return Array.Empty<RemoteResult>();
        }

        var results = new List<RemoteResult>(list.Count);
        using var gate = new SemaphoreSlim(Math.Max(1, Math.Min(16, list.Count)));

        var tasks = list.Select(async pc =>
        {
            await gate.WaitAsync(cancellationToken).ConfigureAwait(false);
            try
            {
                var result = await _remote
                    .ExecuteAsync(pc.Host, action, text, countdownSeconds, messageSeconds, cancellationToken)
                    .ConfigureAwait(false);

                lock (results)
                {
                    results.Add(result);
                }

                if (result.Success)
                {
                    _log.Add(result.WasDryRun ? LogLevel.Info : LogLevel.Success,
                        source, pc.DisplayName, result.Message);
                }
                else
                {
                    _log.Error(source, $"{action.ToDisplayName()} fehlgeschlagen: {result.Message}", pc.DisplayName);
                }
            }
            finally
            {
                gate.Release();
            }
        });

        await Task.WhenAll(tasks).ConfigureAwait(false);
        return results;
    }

    // ---------------------------------------------------------------- Status

    public async Task<IReadOnlyList<HostStatus>> RefreshStatusAsync(CancellationToken cancellationToken = default)
    {
        var hosts = ActivePcs().Select(p => p.Host);
        var changed = await _monitor.RefreshAsync(hosts, cancellationToken).ConfigureAwait(false);

        foreach (var status in changed.Where(s => s.State == HostState.Offline))
        {
            var pc = Config.Pcs.FirstOrDefault(p =>
                string.Equals(p.Host, status.Host, StringComparison.OrdinalIgnoreCase));
            _log.Warning("Status", "Rechner nicht mehr erreichbar.", pc?.DisplayName ?? status.Host);
        }

        return changed;
    }
}

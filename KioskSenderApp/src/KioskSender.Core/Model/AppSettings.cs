namespace KioskSender.Core.Model;

/// <summary>Globale Einstellungen der Anwendung.</summary>
public sealed class AppSettings
{
    /// <summary>Abstand zwischen zwei Ping-Durchläufen in Sekunden.</summary>
    public int StatusIntervalSeconds { get; set; } = 30;

    /// <summary>Timeout eines einzelnen Pings in Millisekunden.</summary>
    public int PingTimeoutMs { get; set; } = 1200;

    /// <summary>Wie viele Hosts gleichzeitig gepingt werden.</summary>
    public int MaxParallelPings { get; set; } = 32;

    /// <summary>Taktrate des Zeitmanagers in Sekunden.</summary>
    public int SchedulerTickSeconds { get; set; } = 20;

    /// <summary>Zeitmanager aktiv — bei false werden keine Aktionen ausgelöst.</summary>
    public bool SchedulerEnabled { get; set; } = true;

    /// <summary>
    /// Testbetrieb: Der Zeitmanager protokolliert nur, was er tun würde,
    /// führt aber keine Befehle aus.
    /// </summary>
    public bool DryRun { get; set; }

    /// <summary>Sekunden, die eine Nachricht auf dem Zielrechner stehen bleibt.</summary>
    public int MessageDisplaySeconds { get; set; } = 60;

    /// <summary>Sekunden Countdown bei manuell ausgelöstem Herunterfahren/Neustart.</summary>
    public int ManualCountdownSeconds { get; set; } = 30;

    /// <summary>
    /// Befehlsvorlage für <see cref="KioskActionKind.Custom"/>.
    /// {host} wird durch den Zielrechner ersetzt.
    /// Beispiel: PsExec.exe \\{host} -s -d rundll32.exe user32.dll,LockWorkStation
    /// </summary>
    public string CustomCommand { get; set; } = string.Empty;

    /// <summary>Timeout für einen einzelnen Fernbefehl in Sekunden.</summary>
    public int CommandTimeoutSeconds { get; set; } = 25;

    /// <summary>Maximale Anzahl Protokolleinträge im Speicher.</summary>
    public int LogCapacity { get; set; } = 2000;

    /// <summary>Fenster beim Start minimiert in den Infobereich legen.</summary>
    public bool StartMinimized { get; set; }

    public AppSettings Clone() => (AppSettings)MemberwiseClone();
}

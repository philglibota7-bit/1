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

    // ------------------------------------------------------------- Inhalte

    /// <summary>
    /// Ordner mit den Medien. Jeder Unterordner darin ist eine Wiedergabeliste.
    /// </summary>
    public string MediaRootPath { get; set; } = string.Empty;

    /// <summary>
    /// Wohin die Inhalte auf dem Kiosk-PC kopiert werden. {host} wird ersetzt.
    /// Vorgabe ist die Verwaltungsfreigabe C$ — dorthin darf, wer auf dem
    /// Zielrechner Administrator ist.
    /// </summary>
    public string ContentTargetTemplate { get; set; } = @"\\{host}\C$\ProgramData\KioskPlayer";

    /// <summary>Anzeigedauer für Bilder in Sekunden.</summary>
    public int DefaultImageSeconds { get; set; } = 10;

    /// <summary>Nach dem letzten Element wieder von vorn beginnen.</summary>
    public bool PlaylistLoop { get; set; } = true;

    /// <summary>Reihenfolge bei jedem Durchlauf mischen.</summary>
    public bool PlaylistShuffle { get; set; }

    /// <summary>Beim Senden Dateien auf dem Zielrechner löschen, die nicht mehr dazugehören.</summary>
    public bool RemoveObsoleteContent { get; set; } = true;

    /// <summary>Wie viele Rechner gleichzeitig beliefert werden.</summary>
    public int MaxParallelTransfers { get; set; } = 4;

    public AppSettings Clone() => (AppSettings)MemberwiseClone();
}

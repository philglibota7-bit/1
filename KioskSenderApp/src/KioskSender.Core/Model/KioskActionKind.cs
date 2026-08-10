namespace KioskSender.Core.Model;

/// <summary>Fernaktionen, die der Sender auf Kiosk-PCs auslösen kann.</summary>
public enum KioskActionKind
{
    /// <summary>Nur eine Meldung anzeigen (msg.exe).</summary>
    Message = 0,

    /// <summary>Angemeldete Sitzungen abmelden (quser + logoff).</summary>
    Logoff = 1,

    /// <summary>Neustart (shutdown.exe /r).</summary>
    Restart = 2,

    /// <summary>Herunterfahren (shutdown.exe /s).</summary>
    Shutdown = 3,

    /// <summary>Laufenden Countdown abbrechen (shutdown.exe /a).</summary>
    AbortShutdown = 4,

    /// <summary>Frei konfigurierbarer Befehl mit {host}-Platzhalter.</summary>
    Custom = 5,

    /// <summary>Keine Aktion — nur protokollieren.</summary>
    None = 6
}

public static class KioskActionKindExtensions
{
    public static string ToDisplayName(this KioskActionKind kind) => kind switch
    {
        KioskActionKind.Message => "Nachricht senden",
        KioskActionKind.Logoff => "Benutzer abmelden",
        KioskActionKind.Restart => "Neu starten",
        KioskActionKind.Shutdown => "Herunterfahren",
        KioskActionKind.AbortShutdown => "Countdown abbrechen",
        KioskActionKind.Custom => "Eigener Befehl",
        KioskActionKind.None => "Keine Aktion",
        _ => kind.ToString()
    };

    /// <summary>Aktionen, die ohne Rückfrage ausgeführt werden dürfen.</summary>
    public static bool IsHarmless(this KioskActionKind kind) =>
        kind is KioskActionKind.Message or KioskActionKind.AbortShutdown or KioskActionKind.None;
}

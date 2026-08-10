namespace KioskSender.Core.Model;

/// <summary>Ein verwalteter Kiosk-PC.</summary>
public sealed class KioskPc
{
    public Guid Id { get; set; } = Guid.NewGuid();

    /// <summary>Anzeigename, z. B. "Info-Terminal Eingang".</summary>
    public string Name { get; set; } = string.Empty;

    /// <summary>Hostname oder IP-Adresse für Ping und Fernbefehle.</summary>
    public string Host { get; set; } = string.Empty;

    public Guid? GroupId { get; set; }

    /// <summary>Deaktivierte PCs werden weder überwacht noch vom Zeitplan erfasst.</summary>
    public bool Enabled { get; set; } = true;

    /// <summary>Eigener Zeitplan; überschreibt den Zeitplan der Gruppe.</summary>
    public Guid? ScheduleId { get; set; }

    public string Note { get; set; } = string.Empty;

    /// <summary>
    /// Welchen Inhalt dieser PC zeigt — der Ordnername aus der Medienbibliothek.
    /// Leer heißt: den Inhalt der Gruppe verwenden.
    /// </summary>
    public string ContentFolder { get; set; } = string.Empty;

    /// <summary>Name des zuletzt übertragenen Inhalts.</summary>
    public string LastContentName { get; set; } = string.Empty;

    /// <summary>Wann zuletzt Inhalte an diesen PC gegangen sind.</summary>
    public DateTime? LastContentSentAt { get; set; }

    /// <summary>Anzeigename mit Rückfall auf den Host.</summary>
    public string DisplayName => string.IsNullOrWhiteSpace(Name) ? Host : Name;

    public KioskPc Clone() => new()
    {
        Id = Id,
        Name = Name,
        Host = Host,
        GroupId = GroupId,
        Enabled = Enabled,
        ScheduleId = ScheduleId,
        Note = Note,
        ContentFolder = ContentFolder,
        LastContentName = LastContentName,
        LastContentSentAt = LastContentSentAt
    };
}

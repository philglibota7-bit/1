namespace KioskSender.Core.Model;

/// <summary>Eine Gruppe von Kiosk-PCs (Gruppenmanager).</summary>
public sealed class PcGroup
{
    public Guid Id { get; set; } = Guid.NewGuid();

    public string Name { get; set; } = "Neue Gruppe";

    /// <summary>Farbe für die Oberfläche, Format #RRGGBB.</summary>
    public string ColorHex { get; set; } = "#4C8DFF";

    /// <summary>Zeitplan, der für alle PCs der Gruppe gilt.</summary>
    public Guid? ScheduleId { get; set; }

    public int SortIndex { get; set; }

    public string Note { get; set; } = string.Empty;

    public PcGroup Clone() => new()
    {
        Id = Id,
        Name = Name,
        ColorHex = ColorHex,
        ScheduleId = ScheduleId,
        SortIndex = SortIndex,
        Note = Note
    };
}

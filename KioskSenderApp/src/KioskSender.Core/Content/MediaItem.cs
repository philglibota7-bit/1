using System.Text.Json.Serialization;

namespace KioskSender.Core.Content;

/// <summary>Art einer Mediendatei — bestimmt, wie der Player sie abspielt.</summary>
public enum MediaKind
{
    /// <summary>Wird für eine feste Dauer angezeigt.</summary>
    Image = 0,

    /// <summary>Läuft bis zum Ende, danach geht es weiter.</summary>
    Video = 1,

    /// <summary>PowerPoint — wird als Bildschirmpräsentation gestartet.</summary>
    Presentation = 2,

    /// <summary>Erkannt, aber nicht abspielbar.</summary>
    Unsupported = 3
}

/// <summary>Eine Datei in einer Wiedergabeliste.</summary>
public sealed class MediaItem
{
    /// <summary>Dateiname ohne Pfad — der Player sucht relativ zu seinem Inhaltsordner.</summary>
    public string FileName { get; set; } = string.Empty;

    public MediaKind Kind { get; set; } = MediaKind.Image;

    /// <summary>
    /// Anzeigedauer in Sekunden. 0 bedeutet: bis zum natürlichen Ende
    /// (Video zu Ende, PowerPoint beendet).
    /// </summary>
    public int Seconds { get; set; }

    public long SizeBytes { get; set; }

    /// <summary>Nur im Manager gefüllt; wird nicht mit ausgeliefert.</summary>
    public string SourcePath { get; set; } = string.Empty;

    /// <summary>
    /// Laufende Nummer für die Anzeige. Steht bewusst nicht in der Datei —
    /// die Reihenfolge ergibt sich dort aus der Liste selbst.
    /// </summary>
    [JsonIgnore]
    public int Position { get; set; }

    public MediaItem Clone() => new()
    {
        FileName = FileName,
        Kind = Kind,
        Seconds = Seconds,
        SizeBytes = SizeBytes,
        SourcePath = SourcePath
    };

    public string SizeText => FormatSize(SizeBytes);

    public string KindText => Kind switch
    {
        MediaKind.Image => "Bild",
        MediaKind.Video => "Video",
        MediaKind.Presentation => "PowerPoint",
        _ => "nicht unterstützt"
    };

    public string DurationText => Kind switch
    {
        MediaKind.Video => Seconds > 0 ? $"max. {Seconds} s" : "bis Ende",
        MediaKind.Presentation => Seconds > 0 ? $"max. {Seconds} s" : "bis Ende",
        MediaKind.Image => $"{Seconds} s",
        _ => "—"
    };

    public static string FormatSize(long bytes)
    {
        if (bytes < 1024)
        {
            return $"{bytes} B";
        }

        if (bytes < 1024 * 1024)
        {
            return $"{bytes / 1024.0:0.#} KB";
        }

        if (bytes < 1024L * 1024 * 1024)
        {
            return $"{bytes / (1024.0 * 1024):0.#} MB";
        }

        return $"{bytes / (1024.0 * 1024 * 1024):0.##} GB";
    }

    public override string ToString() => $"{FileName} ({KindText}, {DurationText})";
}

/// <summary>Ordnet Dateiendungen einer Medienart zu.</summary>
public static class MediaKinds
{
    private static readonly HashSet<string> ImageExtensions = new(StringComparer.OrdinalIgnoreCase)
    {
        ".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".tif", ".tiff"
    };

    private static readonly HashSet<string> VideoExtensions = new(StringComparer.OrdinalIgnoreCase)
    {
        ".mp4", ".m4v", ".wmv", ".avi", ".mov", ".mkv", ".mpg", ".mpeg"
    };

    private static readonly HashSet<string> PresentationExtensions = new(StringComparer.OrdinalIgnoreCase)
    {
        ".ppt", ".pptx", ".pps", ".ppsx"
    };

    /// <summary>Alle Endungen, die im Ordner überhaupt aufgesammelt werden.</summary>
    public static IEnumerable<string> AllExtensions =>
        ImageExtensions.Concat(VideoExtensions).Concat(PresentationExtensions);

    public static MediaKind FromFileName(string? fileName)
    {
        if (string.IsNullOrWhiteSpace(fileName))
        {
            return MediaKind.Unsupported;
        }

        var extension = Path.GetExtension(fileName);
        if (string.IsNullOrEmpty(extension))
        {
            return MediaKind.Unsupported;
        }

        if (ImageExtensions.Contains(extension))
        {
            return MediaKind.Image;
        }

        if (VideoExtensions.Contains(extension))
        {
            return MediaKind.Video;
        }

        return PresentationExtensions.Contains(extension)
            ? MediaKind.Presentation
            : MediaKind.Unsupported;
    }

    public static bool IsPlayable(string? fileName) => FromFileName(fileName) != MediaKind.Unsupported;
}

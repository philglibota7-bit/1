using System.Text.Json;
using System.Text.Json.Serialization;

namespace KioskSender.Core.Content;

/// <summary>
/// Eine Wiedergabeliste. Wird als playlist.json neben die Mediendateien gelegt;
/// der Player auf dem Kiosk-PC liest genau diese Datei.
/// </summary>
public sealed class Playlist
{
    /// <summary>Format der Datei — der Player kann so ältere Stände erkennen.</summary>
    public int Version { get; set; } = 1;

    public string Name { get; set; } = "Wiedergabeliste";

    /// <summary>Wann die Liste zusammengestellt wurde.</summary>
    public DateTime CreatedAt { get; set; } = DateTime.Now;

    /// <summary>Anzeigedauer für Bilder, wenn am Element nichts anderes steht.</summary>
    public int DefaultImageSeconds { get; set; } = 10;

    /// <summary>Nach dem letzten Element wieder von vorn beginnen.</summary>
    public bool Loop { get; set; } = true;

    /// <summary>Reihenfolge bei jedem Durchlauf mischen.</summary>
    public bool Shuffle { get; set; }

    /// <summary>Nur der Vollständigkeit halber — hilft beim Suchen von Fehlern.</summary>
    public string SourceFolder { get; set; } = string.Empty;

    public List<MediaItem> Items { get; set; } = new();

    public const string FileName = "playlist.json";

    private static readonly JsonSerializerOptions Options = new()
    {
        WriteIndented = true,
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
        Converters = { new JsonStringEnumConverter() }
    };

    public long TotalBytes => Items.Sum(i => i.SizeBytes);

    public int PlayableCount => Items.Count(i => i.Kind != MediaKind.Unsupported);

    /// <summary>
    /// Gesamtdauer eines Durchlaufs, soweit sie sich vorher sagen lässt.
    /// Videos und Präsentationen ohne Zeitlimit fließen nicht ein.
    /// </summary>
    public TimeSpan KnownDuration =>
        TimeSpan.FromSeconds(Items.Where(i => i.Seconds > 0).Sum(i => i.Seconds));

    public bool HasUnknownDuration => Items.Any(i => i.Seconds <= 0 && i.Kind != MediaKind.Unsupported);

    public string DurationText
    {
        get
        {
            var known = KnownDuration;
            var text = known.TotalHours >= 1
                ? $"{(int)known.TotalHours} h {known.Minutes} min"
                : known.TotalMinutes >= 1
                    ? $"{(int)known.TotalMinutes} min {known.Seconds} s"
                    : $"{known.Seconds} s";

            return HasUnknownDuration ? text + " + Videolaufzeiten" : text;
        }
    }

    /// <summary>Nur die Elemente, die der Player tatsächlich abspielen kann.</summary>
    public Playlist ForDelivery()
    {
        var copy = new Playlist
        {
            Version = Version,
            Name = Name,
            CreatedAt = DateTime.Now,
            DefaultImageSeconds = DefaultImageSeconds,
            Loop = Loop,
            Shuffle = Shuffle,
            SourceFolder = SourceFolder,
            Items = Items
                .Where(i => i.Kind != MediaKind.Unsupported)
                .Select(i =>
                {
                    var item = i.Clone();
                    item.SourcePath = string.Empty;
                    return item;
                })
                .ToList()
        };

        return copy;
    }

    public string ToJson() => JsonSerializer.Serialize(this, Options);

    public static Playlist? FromJson(string json)
    {
        try
        {
            return JsonSerializer.Deserialize<Playlist>(json, Options);
        }
        catch (JsonException)
        {
            return null;
        }
    }

    public static async Task<Playlist?> LoadAsync(string path, CancellationToken cancellationToken = default)
    {
        try
        {
            var json = await File.ReadAllTextAsync(path, cancellationToken).ConfigureAwait(false);
            return FromJson(json);
        }
        catch (Exception ex) when (ex is IOException or UnauthorizedAccessException)
        {
            return null;
        }
    }

    /// <summary>
    /// Baut aus einem Ordner eine Wiedergabeliste: Dateien natürlich sortiert,
    /// Bilder bekommen die Standarddauer.
    /// </summary>
    public static Playlist FromFolder(LibraryFolder folder, int defaultImageSeconds = 10)
    {
        var playlist = new Playlist
        {
            Name = folder.Name,
            SourceFolder = folder.FullPath,
            DefaultImageSeconds = defaultImageSeconds,
            Items = folder.Items.Select(i => i.Clone()).ToList()
        };

        foreach (var item in playlist.Items.Where(i => i.Kind == MediaKind.Image && i.Seconds <= 0))
        {
            item.Seconds = defaultImageSeconds;
        }

        return playlist;
    }
}

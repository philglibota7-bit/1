namespace KioskSender.Core.Model;

/// <summary>
/// Wandelt eine Zeile wie "08:00-12:00, 13:00-17:00" in Zeitspannen um und
/// zurück. Damit lässt sich ein Wochentag als einfaches Textfeld bearbeiten.
/// </summary>
public static class RangeListParser
{
    private static readonly char[] Separators = { ',', ';', '|' };

    /// <summary>
    /// Parst eine Liste von Zeitspannen. Leerer Text bedeutet "geschlossen"
    /// und ist gültig.
    /// </summary>
    public static bool TryParse(string? text, out List<TimeRange> ranges, out string error)
    {
        ranges = new List<TimeRange>();
        error = string.Empty;

        if (string.IsNullOrWhiteSpace(text))
        {
            return true;
        }

        foreach (var part in text.Split(Separators, StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries))
        {
            if (!TimeRange.TryParse(part, out var range))
            {
                error = $"'{part}' ist keine gültige Zeitspanne. Erwartet wird z. B. 08:00-17:00.";
                ranges.Clear();
                return false;
            }

            ranges.Add(range);
        }

        ranges.Sort((a, b) => a.StartMinutes.CompareTo(b.StartMinutes));

        for (var i = 1; i < ranges.Count; i++)
        {
            if (ranges[i].StartMinutes < ranges[i - 1].EndMinutes)
            {
                error = $"Die Zeitspannen {ranges[i - 1]} und {ranges[i]} überschneiden sich.";
                ranges.Clear();
                return false;
            }
        }

        return true;
    }

    public static string Format(IEnumerable<TimeRange>? ranges) =>
        ranges is null ? string.Empty : string.Join(", ", ranges.Select(r => r.ToString()));

    /// <summary>Gesamtdauer aller Zeitspannen — für die Wochenübersicht.</summary>
    public static TimeSpan TotalDuration(IEnumerable<TimeRange>? ranges) =>
        ranges is null
            ? TimeSpan.Zero
            : TimeSpan.FromMinutes(ranges.Sum(r => r.DurationMinutes));
}

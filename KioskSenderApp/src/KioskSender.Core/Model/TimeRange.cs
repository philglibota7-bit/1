using System.Globalization;

namespace KioskSender.Core.Model;

/// <summary>
/// Ein Zeitfenster innerhalb eines Tages, gespeichert als Minuten ab Mitternacht.
/// <see cref="EndMinutes"/> darf bis 2880 gehen, damit Fenster über Mitternacht
/// hinaus reichen können (z. B. 20:00–02:00 = 1200–1560).
/// </summary>
public sealed class TimeRange
{
    public const int MinutesPerDay = 24 * 60;
    public const int MaxEndMinutes = 2 * MinutesPerDay;

    public int StartMinutes { get; set; }
    public int EndMinutes { get; set; }

    public TimeRange()
    {
    }

    public TimeRange(int startMinutes, int endMinutes)
    {
        StartMinutes = startMinutes;
        EndMinutes = endMinutes;
    }

    public TimeSpan Start => TimeSpan.FromMinutes(StartMinutes);

    public TimeSpan End => TimeSpan.FromMinutes(EndMinutes);

    public int DurationMinutes => EndMinutes - StartMinutes;

    /// <summary>Fenster endet erst am Folgetag.</summary>
    public bool CrossesMidnight => EndMinutes > MinutesPerDay;

    public bool IsValid =>
        StartMinutes >= 0 &&
        StartMinutes < MinutesPerDay &&
        EndMinutes > StartMinutes &&
        EndMinutes <= MaxEndMinutes;

    public TimeRange Clone() => new(StartMinutes, EndMinutes);

    /// <summary>
    /// Parst "08:00-17:30". Werte wie "24:00" oder "02:00" als Ende werden
    /// automatisch auf den Folgetag geschoben, wenn das Ende sonst vor dem Start läge.
    /// </summary>
    public static bool TryParse(string? text, out TimeRange range)
    {
        range = new TimeRange();
        if (string.IsNullOrWhiteSpace(text))
        {
            return false;
        }

        var parts = text.Split('-', 2, StringSplitOptions.TrimEntries);
        if (parts.Length != 2)
        {
            return false;
        }

        if (!TryParseClock(parts[0], out var start) || !TryParseClock(parts[1], out var end))
        {
            return false;
        }

        if (start >= MinutesPerDay)
        {
            return false;
        }

        if (end <= start)
        {
            // "20:00-02:00" bedeutet: bis 02:00 des Folgetages.
            end += MinutesPerDay;
        }

        var candidate = new TimeRange(start, end);
        if (!candidate.IsValid)
        {
            return false;
        }

        range = candidate;
        return true;
    }

    private static bool TryParseClock(string text, out int minutes)
    {
        minutes = 0;
        var parts = text.Split(':', StringSplitOptions.TrimEntries);
        if (parts.Length is < 1 or > 2)
        {
            return false;
        }

        if (!int.TryParse(parts[0], NumberStyles.None, CultureInfo.InvariantCulture, out var hours))
        {
            return false;
        }

        var mins = 0;
        if (parts.Length == 2 && !int.TryParse(parts[1], NumberStyles.None, CultureInfo.InvariantCulture, out mins))
        {
            return false;
        }

        if (hours is < 0 or > 48 || mins is < 0 or > 59)
        {
            return false;
        }

        minutes = (hours * 60) + mins;
        return true;
    }

    public override string ToString() => $"{Format(StartMinutes)}-{Format(EndMinutes)}";

    public static string Format(int minutes)
    {
        var normalized = minutes % MinutesPerDay;
        if (minutes > 0 && normalized == 0)
        {
            // 1440 soll als "24:00" und nicht als "00:00" erscheinen.
            return minutes == MinutesPerDay ? "24:00" : "00:00";
        }

        return string.Create(CultureInfo.InvariantCulture, $"{normalized / 60:00}:{normalized % 60:00}");
    }
}

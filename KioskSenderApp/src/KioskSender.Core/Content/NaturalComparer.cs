using System.Globalization;

namespace KioskSender.Core.Content;

/// <summary>
/// Sortiert Namen so, wie ein Mensch es erwartet: "Bild2" kommt vor "Bild10".
/// Ein reiner Textvergleich würde "Bild10" vor "Bild2" einsortieren — bei
/// durchnummerierten Folien und Bildern wäre die Wiedergabe dann durcheinander.
/// </summary>
public sealed class NaturalComparer : IComparer<string>
{
    public static readonly NaturalComparer Instance = new();

    public int Compare(string? x, string? y)
    {
        if (ReferenceEquals(x, y))
        {
            return 0;
        }

        if (x is null)
        {
            return -1;
        }

        if (y is null)
        {
            return 1;
        }

        var i = 0;
        var j = 0;

        while (i < x.Length && j < y.Length)
        {
            if (char.IsAsciiDigit(x[i]) && char.IsAsciiDigit(y[j]))
            {
                // Führende Nullen überspringen, damit "007" und "7" gleich groß sind.
                while (i < x.Length - 1 && x[i] == '0' && char.IsAsciiDigit(x[i + 1]))
                {
                    i++;
                }

                while (j < y.Length - 1 && y[j] == '0' && char.IsAsciiDigit(y[j + 1]))
                {
                    j++;
                }

                var startX = i;
                var startY = j;

                while (i < x.Length && char.IsAsciiDigit(x[i]))
                {
                    i++;
                }

                while (j < y.Length && char.IsAsciiDigit(y[j]))
                {
                    j++;
                }

                var lengthX = i - startX;
                var lengthY = j - startY;

                if (lengthX != lengthY)
                {
                    // Die längere Ziffernfolge ist die größere Zahl.
                    return lengthX.CompareTo(lengthY);
                }

                var digits = string.CompareOrdinal(x, startX, y, startY, lengthX);
                if (digits != 0)
                {
                    return digits;
                }

                continue;
            }

            var comparison = char.ToLower(x[i], CultureInfo.CurrentCulture)
                .CompareTo(char.ToLower(y[j], CultureInfo.CurrentCulture));

            if (comparison != 0)
            {
                return comparison;
            }

            i++;
            j++;
        }

        return (x.Length - i).CompareTo(y.Length - j);
    }
}

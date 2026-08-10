namespace KioskSender.Core.Remote;

/// <summary>Eine angemeldete Sitzung auf einem Zielrechner.</summary>
public sealed record UserSession(string UserName, string SessionName, int SessionId, string State)
{
    public bool IsActive => State.StartsWith("Akt", StringComparison.OrdinalIgnoreCase)
                            || State.StartsWith("Act", StringComparison.OrdinalIgnoreCase);

    public override string ToString() =>
        string.IsNullOrEmpty(SessionName)
            ? $"{UserName} (ID {SessionId}, {State})"
            : $"{UserName}@{SessionName} (ID {SessionId}, {State})";
}

/// <summary>
/// Liest die Ausgabe von quser.exe. Die Spaltenüberschriften sind
/// sprachabhängig, deshalb wird der Inhalt und nicht die Überschrift ausgewertet:
/// die erste rein numerische Spalte ist die Sitzungs-ID.
/// </summary>
public static class QuserParser
{
    public static IReadOnlyList<UserSession> Parse(string? output)
    {
        var sessions = new List<UserSession>();
        if (string.IsNullOrWhiteSpace(output))
        {
            return sessions;
        }

        var lines = output.Split('\n', StringSplitOptions.RemoveEmptyEntries);
        var isFirstLine = true;

        foreach (var rawLine in lines)
        {
            var line = rawLine.TrimEnd('\r').TrimEnd();
            if (string.IsNullOrWhiteSpace(line))
            {
                continue;
            }

            // Die aktuelle Sitzung ist mit ">" markiert.
            var content = line.TrimStart();
            var isCurrent = content.StartsWith('>');
            if (isCurrent)
            {
                content = content[1..];
            }

            var tokens = content.Split((char[]?)null, StringSplitOptions.RemoveEmptyEntries);
            if (tokens.Length < 3)
            {
                continue;
            }

            var idIndex = FindSessionIdIndex(tokens);
            if (idIndex < 0)
            {
                // Erste Zeile ohne ID ist die Überschrift — still überspringen.
                isFirstLine = false;
                continue;
            }

            isFirstLine = false;

            var userName = tokens[0];
            var sessionName = idIndex >= 2 ? tokens[1] : string.Empty;
            var state = idIndex + 1 < tokens.Length ? tokens[idIndex + 1] : string.Empty;

            sessions.Add(new UserSession(userName, sessionName, int.Parse(tokens[idIndex]), state));
        }

        _ = isFirstLine;
        return sessions;
    }

    private static int FindSessionIdIndex(IReadOnlyList<string> tokens)
    {
        // Ab Index 1 suchen: der Benutzername steht immer vorn und käme
        // sonst bei rein numerischen Kontennamen fälschlich als ID durch.
        for (var i = 1; i < tokens.Count; i++)
        {
            var token = tokens[i];
            if (token.Length is > 0 and <= 5 && token.All(char.IsAsciiDigit))
            {
                return i;
            }
        }

        return -1;
    }
}

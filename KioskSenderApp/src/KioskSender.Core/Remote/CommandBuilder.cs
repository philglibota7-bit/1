using System.Text.RegularExpressions;

namespace KioskSender.Core.Remote;

/// <summary>Ein fertig zusammengebauter Befehl (Programm + Argumentliste).</summary>
public sealed record CommandSpec(string FileName, IReadOnlyList<string> Arguments)
{
    /// <summary>Nur für Anzeige und Protokoll — nicht zum Ausführen verwenden.</summary>
    public string ToDisplayString()
    {
        static string Show(string arg) =>
            arg.Contains(' ') || arg.Length == 0 ? "\"" + arg.Replace("\"", "\\\"") + "\"" : arg;

        return Arguments.Count == 0
            ? FileName
            : FileName + " " + string.Join(' ', Arguments.Select(Show));
    }
}

/// <summary>
/// Baut die Kommandozeilen für die Windows-Bordmittel msg.exe, shutdown.exe,
/// quser.exe und logoff.exe. Bewusst ohne Seiteneffekte, damit jeder erzeugte
/// Befehl in Tests geprüft werden kann.
/// </summary>
public static class CommandBuilder
{
    /// <summary>
    /// Hostname, IPv4/IPv6 oder FQDN. Alles andere wird abgewiesen, damit keine
    /// krummen Werte in Befehle geraten.
    /// </summary>
    private static readonly Regex HostPattern = new(
        @"^[A-Za-z0-9]([A-Za-z0-9\-\._:]*[A-Za-z0-9])?$",
        RegexOptions.Compiled);

    /// <summary>shutdown.exe schneidet den Kommentar nach 512 Zeichen ab.</summary>
    public const int MaxCommentLength = 500;

    public static bool IsValidHost(string? host) =>
        !string.IsNullOrWhiteSpace(host) && host.Length <= 253 && HostPattern.IsMatch(host.Trim());

    public static string NormalizeHost(string host) => host.Trim();

    /// <summary>UNC-Schreibweise für shutdown /m.</summary>
    public static string ToUncHost(string host) => @"\\" + NormalizeHost(host);

    /// <summary>msg * /server:HOST /time:SEK "Text"</summary>
    public static CommandSpec Message(string host, string text, int displaySeconds)
    {
        var seconds = Math.Clamp(displaySeconds, 1, 99_999);
        return new CommandSpec("msg.exe", new[]
        {
            "*",
            "/server:" + NormalizeHost(host),
            "/time:" + seconds.ToString(),
            Truncate(text, 1000)
        });
    }

    /// <summary>shutdown /s /f /m \\HOST /t SEK /c "Text"</summary>
    public static CommandSpec Shutdown(string host, int countdownSeconds, string comment) =>
        ShutdownCore("/s", host, countdownSeconds, comment);

    /// <summary>shutdown /r /f /m \\HOST /t SEK /c "Text"</summary>
    public static CommandSpec Restart(string host, int countdownSeconds, string comment) =>
        ShutdownCore("/r", host, countdownSeconds, comment);

    /// <summary>shutdown /a /m \\HOST</summary>
    public static CommandSpec AbortShutdown(string host) =>
        new("shutdown.exe", new[] { "/a", "/m", ToUncHost(host) });

    private static CommandSpec ShutdownCore(string mode, string host, int countdownSeconds, string comment)
    {
        var seconds = Math.Clamp(countdownSeconds, 0, 315_360_000);

        var args = new List<string>
        {
            mode,
            "/f",
            "/m", ToUncHost(host),
            "/t", seconds.ToString()
        };

        var text = Truncate(comment, MaxCommentLength);
        if (!string.IsNullOrWhiteSpace(text))
        {
            args.Add("/c");
            args.Add(text);
        }

        return new CommandSpec("shutdown.exe", args);
    }

    /// <summary>quser /server:HOST — listet die angemeldeten Sitzungen.</summary>
    public static CommandSpec QuerySessions(string host) =>
        new("quser.exe", new[] { "/server:" + NormalizeHost(host) });

    /// <summary>logoff SESSIONID /server:HOST</summary>
    public static CommandSpec Logoff(string host, int sessionId) =>
        new("logoff.exe", new[] { sessionId.ToString(), "/server:" + NormalizeHost(host) });

    /// <summary>
    /// Zerlegt eine frei konfigurierte Befehlszeile und ersetzt {host}.
    /// Anführungszeichen gruppieren Argumente wie in der Eingabeaufforderung.
    /// </summary>
    public static CommandSpec? Custom(string template, string host)
    {
        if (string.IsNullOrWhiteSpace(template))
        {
            return null;
        }

        var tokens = Tokenize(template);
        if (tokens.Count == 0)
        {
            return null;
        }

        var replaced = tokens
            .Select(t => t
                .Replace("{host}", NormalizeHost(host), StringComparison.OrdinalIgnoreCase)
                .Replace("{pc}", NormalizeHost(host), StringComparison.OrdinalIgnoreCase))
            .ToList();

        return new CommandSpec(replaced[0], replaced.Skip(1).ToList());
    }

    /// <summary>Einfacher Zerleger für Befehlszeilen mit "..."-Gruppierung.</summary>
    public static List<string> Tokenize(string commandLine)
    {
        var tokens = new List<string>();
        var current = new System.Text.StringBuilder();
        var inQuotes = false;
        var hasContent = false;

        foreach (var c in commandLine)
        {
            if (c == '"')
            {
                inQuotes = !inQuotes;
                hasContent = true;
                continue;
            }

            if (!inQuotes && char.IsWhiteSpace(c))
            {
                if (hasContent)
                {
                    tokens.Add(current.ToString());
                    current.Clear();
                    hasContent = false;
                }

                continue;
            }

            current.Append(c);
            hasContent = true;
        }

        if (hasContent)
        {
            tokens.Add(current.ToString());
        }

        return tokens;
    }

    private static string Truncate(string? text, int max)
    {
        text ??= string.Empty;
        text = text.Replace("\r", " ").Replace("\n", " ").Trim();
        return text.Length <= max ? text : text[..max];
    }
}

namespace KioskSender.Core.Model;

public enum LogLevel
{
    Debug = 0,
    Info = 1,
    Success = 2,
    Warning = 3,
    Error = 4
}

/// <summary>Ein Eintrag im Protokoll.</summary>
public sealed class LogEntry
{
    public DateTime Timestamp { get; init; } = DateTime.Now;

    public LogLevel Level { get; init; } = LogLevel.Info;

    /// <summary>Quelle, z. B. "Zeitmanager", "Sender", "Status".</summary>
    public string Source { get; init; } = string.Empty;

    /// <summary>Betroffener PC oder Gruppe (optional).</summary>
    public string Target { get; init; } = string.Empty;

    public string Message { get; init; } = string.Empty;

    public string ToCsvLine()
    {
        static string Quote(string value) => "\"" + value.Replace("\"", "\"\"") + "\"";

        return string.Join(';',
            Quote(Timestamp.ToString("yyyy-MM-dd HH:mm:ss")),
            Quote(Level.ToString()),
            Quote(Source),
            Quote(Target),
            Quote(Message));
    }

    public const string CsvHeader = "\"Zeit\";\"Ebene\";\"Quelle\";\"Ziel\";\"Meldung\"";

    public override string ToString() =>
        $"{Timestamp:HH:mm:ss} [{Level}] {Source} {Target}: {Message}".Replace("  ", " ");
}

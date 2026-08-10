using System.Text;
using KioskSender.Core.Model;

namespace KioskSender.Core.Logging;

/// <summary>
/// Protokoll im Arbeitsspeicher plus tagesweise Datei. Thread-sicher, weil
/// Zeitmanager, Statusprüfung und Oberfläche gleichzeitig schreiben.
/// </summary>
public sealed class LogService
{
    private readonly object _sync = new();
    private readonly LinkedList<LogEntry> _entries = new();
    private readonly string? _logDirectory;

    public LogService(string? logDirectory = null, int capacity = 2000)
    {
        _logDirectory = logDirectory;
        Capacity = capacity;
    }

    public int Capacity { get; set; }

    /// <summary>Ab dieser Ebene wird zusätzlich in die Datei geschrieben.</summary>
    public LogLevel FileLevel { get; set; } = LogLevel.Info;

    /// <summary>Wird für jeden neuen Eintrag ausgelöst (für die Oberfläche).</summary>
    public event EventHandler<LogEntry>? EntryAdded;

    public LogEntry Add(LogLevel level, string source, string target, string message)
    {
        var entry = new LogEntry
        {
            Level = level,
            Source = source,
            Target = target,
            Message = message
        };

        lock (_sync)
        {
            _entries.AddLast(entry);
            while (_entries.Count > Capacity && _entries.First is not null)
            {
                _entries.RemoveFirst();
            }
        }

        if (level >= FileLevel)
        {
            TryWriteToFile(entry);
        }

        EntryAdded?.Invoke(this, entry);
        return entry;
    }

    public LogEntry Info(string source, string message, string target = "") =>
        Add(LogLevel.Info, source, target, message);

    public LogEntry Success(string source, string message, string target = "") =>
        Add(LogLevel.Success, source, target, message);

    public LogEntry Warning(string source, string message, string target = "") =>
        Add(LogLevel.Warning, source, target, message);

    public LogEntry Error(string source, string message, string target = "") =>
        Add(LogLevel.Error, source, target, message);

    public IReadOnlyList<LogEntry> Snapshot()
    {
        lock (_sync)
        {
            return _entries.ToList();
        }
    }

    public void Clear()
    {
        lock (_sync)
        {
            _entries.Clear();
        }
    }

    public string ToCsv()
    {
        var builder = new StringBuilder();
        builder.AppendLine(LogEntry.CsvHeader);
        foreach (var entry in Snapshot())
        {
            builder.AppendLine(entry.ToCsvLine());
        }

        return builder.ToString();
    }

    public string? CurrentLogFilePath =>
        _logDirectory is null
            ? null
            : Path.Combine(_logDirectory, $"kiosksender-{DateTime.Now:yyyy-MM-dd}.log");

    private void TryWriteToFile(LogEntry entry)
    {
        var path = CurrentLogFilePath;
        if (path is null)
        {
            return;
        }

        try
        {
            Directory.CreateDirectory(_logDirectory!);
            var line = $"{entry.Timestamp:yyyy-MM-dd HH:mm:ss}\t{entry.Level}\t{entry.Source}\t{entry.Target}\t{entry.Message}";
            lock (_sync)
            {
                File.AppendAllText(path, line + Environment.NewLine, Encoding.UTF8);
            }
        }
        catch
        {
            // Protokollieren darf die Anwendung nie zum Absturz bringen.
        }
    }

    /// <summary>Löscht Protokolldateien, die älter als <paramref name="days"/> Tage sind.</summary>
    public void PurgeOldFiles(int days = 30)
    {
        if (_logDirectory is null || !Directory.Exists(_logDirectory))
        {
            return;
        }

        try
        {
            var limit = DateTime.Now.AddDays(-Math.Max(1, days));
            foreach (var file in Directory.EnumerateFiles(_logDirectory, "kiosksender-*.log"))
            {
                if (File.GetLastWriteTime(file) < limit)
                {
                    File.Delete(file);
                }
            }
        }
        catch
        {
            // Aufräumen ist optional.
        }
    }
}

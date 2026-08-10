namespace KioskSender.Core.Remote;

/// <summary>Ergebnis eines externen Prozessaufrufs.</summary>
public sealed record ProcessResult(int ExitCode, string StandardOutput, string StandardError, bool TimedOut)
{
    public bool Success => !TimedOut && ExitCode == 0;

    /// <summary>Die aussagekräftigste Fehlermeldung des Aufrufs.</summary>
    public string BestErrorText()
    {
        if (TimedOut)
        {
            return "Zeitüberschreitung — der Zielrechner hat nicht geantwortet.";
        }

        var text = string.IsNullOrWhiteSpace(StandardError) ? StandardOutput : StandardError;
        text = text.Trim();
        return string.IsNullOrEmpty(text) ? $"Fehlercode {ExitCode}." : text;
    }
}

/// <summary>Startet externe Programme. Abstrahiert für Tests und Trockenlauf.</summary>
public interface IProcessRunner
{
    Task<ProcessResult> RunAsync(
        string fileName,
        IReadOnlyList<string> arguments,
        TimeSpan timeout,
        CancellationToken cancellationToken = default);
}

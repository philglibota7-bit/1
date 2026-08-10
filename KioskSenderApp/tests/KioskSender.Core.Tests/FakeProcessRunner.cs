using KioskSender.Core.Remote;

namespace KioskSender.Core.Tests;

/// <summary>Prozessaufrufe aufzeichnen statt ausführen.</summary>
public sealed class FakeProcessRunner : IProcessRunner
{
    public List<(string FileName, string[] Arguments)> Calls { get; } = new();

    /// <summary>Antwort je Programmname; ohne Eintrag wird Erfolg gemeldet.</summary>
    public Dictionary<string, ProcessResult> Responses { get; } = new(StringComparer.OrdinalIgnoreCase);

    public Func<string, string[], ProcessResult>? Handler { get; set; }

    public Task<ProcessResult> RunAsync(
        string fileName,
        IReadOnlyList<string> arguments,
        TimeSpan timeout,
        CancellationToken cancellationToken = default)
    {
        var args = arguments.ToArray();
        Calls.Add((fileName, args));

        if (Handler is not null)
        {
            return Task.FromResult(Handler(fileName, args));
        }

        return Task.FromResult(Responses.TryGetValue(fileName, out var response)
            ? response
            : new ProcessResult(0, string.Empty, string.Empty, false));
    }
}

using System.Diagnostics;
using System.Text;

namespace KioskSender.Core.Remote;

/// <summary>Führt externe Programme aus und fängt Ausgabe, Timeout und Abbruch sauber ab.</summary>
public sealed class ProcessRunner : IProcessRunner
{
    public async Task<ProcessResult> RunAsync(
        string fileName,
        IReadOnlyList<string> arguments,
        TimeSpan timeout,
        CancellationToken cancellationToken = default)
    {
        var startInfo = new ProcessStartInfo
        {
            FileName = fileName,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true,
            StandardOutputEncoding = Encoding.UTF8,
            StandardErrorEncoding = Encoding.UTF8
        };

        foreach (var argument in arguments)
        {
            // ArgumentList übernimmt das korrekte Quoting — kein manuelles
            // Zusammenbauen der Kommandozeile, damit Anführungszeichen in
            // Nachrichtentexten nichts kaputt machen können.
            startInfo.ArgumentList.Add(argument);
        }

        using var process = new Process { StartInfo = startInfo };

        var stdout = new StringBuilder();
        var stderr = new StringBuilder();
        using var outputDone = new SemaphoreSlim(0, 2);

        process.OutputDataReceived += (_, e) =>
        {
            if (e.Data is null)
            {
                outputDone.Release();
            }
            else
            {
                stdout.AppendLine(e.Data);
            }
        };

        process.ErrorDataReceived += (_, e) =>
        {
            if (e.Data is null)
            {
                outputDone.Release();
            }
            else
            {
                stderr.AppendLine(e.Data);
            }
        };

        try
        {
            process.Start();
        }
        catch (Exception ex)
        {
            return new ProcessResult(-1, string.Empty, ex.Message, false);
        }

        process.BeginOutputReadLine();
        process.BeginErrorReadLine();

        using var timeoutCts = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken);
        timeoutCts.CancelAfter(timeout);

        var timedOut = false;
        try
        {
            await process.WaitForExitAsync(timeoutCts.Token).ConfigureAwait(false);

            // Warten, bis beide Ausgabeströme geschlossen sind, sonst fehlen die letzten Zeilen.
            await outputDone.WaitAsync(TimeSpan.FromSeconds(2), CancellationToken.None).ConfigureAwait(false);
            await outputDone.WaitAsync(TimeSpan.FromSeconds(2), CancellationToken.None).ConfigureAwait(false);
        }
        catch (OperationCanceledException)
        {
            timedOut = !cancellationToken.IsCancellationRequested;
            TryKill(process);
        }

        var exitCode = timedOut ? -1 : SafeExitCode(process);
        return new ProcessResult(exitCode, stdout.ToString(), stderr.ToString(), timedOut);
    }

    private static int SafeExitCode(Process process)
    {
        try
        {
            return process.ExitCode;
        }
        catch
        {
            return -1;
        }
    }

    private static void TryKill(Process process)
    {
        try
        {
            if (!process.HasExited)
            {
                process.Kill(entireProcessTree: true);
            }
        }
        catch
        {
            // Prozess ist bereits beendet — nichts zu tun.
        }
    }
}

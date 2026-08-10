using KioskSender.Core.Model;

namespace KioskSender.Core.Remote;

/// <summary>Ergebnis einer Fernaktion auf genau einem Rechner.</summary>
public sealed record RemoteResult(
    string Host,
    KioskActionKind Action,
    bool Success,
    string Message,
    bool WasDryRun = false)
{
    public static RemoteResult Ok(string host, KioskActionKind action, string message, bool dryRun = false) =>
        new(host, action, true, message, dryRun);

    public static RemoteResult Fail(string host, KioskActionKind action, string message) =>
        new(host, action, false, message);
}

/// <summary>
/// Führt Fernaktionen auf Kiosk-PCs aus — ohne eigenen Agenten, nur mit
/// Windows-Bordmitteln. Voraussetzung ist, dass der ausführende Benutzer
/// Administrator auf dem Zielrechner ist.
/// </summary>
public sealed class RemoteCommandService
{
    private readonly IProcessRunner _runner;

    public RemoteCommandService(IProcessRunner runner) => _runner = runner;

    /// <summary>Wenn true, wird nichts ausgeführt, sondern nur gemeldet, was passieren würde.</summary>
    public bool DryRun { get; set; }

    public TimeSpan Timeout { get; set; } = TimeSpan.FromSeconds(25);

    /// <summary>Vorlage für <see cref="KioskActionKind.Custom"/>.</summary>
    public string CustomCommandTemplate { get; set; } = string.Empty;

    public async Task<RemoteResult> ExecuteAsync(
        string host,
        KioskActionKind action,
        string text,
        int countdownSeconds,
        int messageSeconds,
        CancellationToken cancellationToken = default)
    {
        if (!CommandBuilder.IsValidHost(host))
        {
            return RemoteResult.Fail(host ?? string.Empty, action,
                "Ungültiger Hostname oder ungültige IP-Adresse.");
        }

        host = CommandBuilder.NormalizeHost(host);

        return action switch
        {
            KioskActionKind.None =>
                RemoteResult.Ok(host, action, "Keine Aktion konfiguriert."),

            KioskActionKind.Message =>
                await RunSingleAsync(host, action, CommandBuilder.Message(host, text, messageSeconds),
                    "Nachricht zugestellt.", cancellationToken).ConfigureAwait(false),

            KioskActionKind.Shutdown =>
                await RunSingleAsync(host, action, CommandBuilder.Shutdown(host, countdownSeconds, text),
                    $"Herunterfahren in {countdownSeconds} s ausgelöst.", cancellationToken).ConfigureAwait(false),

            KioskActionKind.Restart =>
                await RunSingleAsync(host, action, CommandBuilder.Restart(host, countdownSeconds, text),
                    $"Neustart in {countdownSeconds} s ausgelöst.", cancellationToken).ConfigureAwait(false),

            KioskActionKind.AbortShutdown =>
                await RunSingleAsync(host, action, CommandBuilder.AbortShutdown(host),
                    "Countdown abgebrochen.", cancellationToken).ConfigureAwait(false),

            KioskActionKind.Logoff =>
                await LogoffAsync(host, cancellationToken).ConfigureAwait(false),

            KioskActionKind.Custom =>
                await RunCustomAsync(host, cancellationToken).ConfigureAwait(false),

            _ => RemoteResult.Fail(host, action, "Unbekannte Aktion.")
        };
    }

    /// <summary>Sitzungen abfragen, ohne etwas zu verändern.</summary>
    public async Task<IReadOnlyList<UserSession>> GetSessionsAsync(
        string host,
        CancellationToken cancellationToken = default)
    {
        if (!CommandBuilder.IsValidHost(host))
        {
            return Array.Empty<UserSession>();
        }

        var spec = CommandBuilder.QuerySessions(host);
        var result = await _runner
            .RunAsync(spec.FileName, spec.Arguments, Timeout, cancellationToken)
            .ConfigureAwait(false);

        // quser meldet "Kein Benutzer angemeldet" mit Exitcode 1 — das ist kein Fehler.
        return QuserParser.Parse(result.StandardOutput);
    }

    private async Task<RemoteResult> LogoffAsync(string host, CancellationToken cancellationToken)
    {
        var sessions = await GetSessionsAsync(host, cancellationToken).ConfigureAwait(false);
        if (sessions.Count == 0)
        {
            return RemoteResult.Ok(host, KioskActionKind.Logoff, "Kein Benutzer angemeldet.");
        }

        if (DryRun)
        {
            var names = string.Join(", ", sessions.Select(s => s.ToString()));
            return RemoteResult.Ok(host, KioskActionKind.Logoff,
                $"Testbetrieb: würde abmelden — {names}", dryRun: true);
        }

        var failures = new List<string>();
        foreach (var session in sessions)
        {
            var spec = CommandBuilder.Logoff(host, session.SessionId);
            var result = await _runner
                .RunAsync(spec.FileName, spec.Arguments, Timeout, cancellationToken)
                .ConfigureAwait(false);

            if (!result.Success)
            {
                failures.Add($"{session.UserName}: {result.BestErrorText()}");
            }
        }

        return failures.Count == 0
            ? RemoteResult.Ok(host, KioskActionKind.Logoff,
                $"{sessions.Count} Sitzung(en) abgemeldet.")
            : RemoteResult.Fail(host, KioskActionKind.Logoff, string.Join(" | ", failures));
    }

    private async Task<RemoteResult> RunCustomAsync(string host, CancellationToken cancellationToken)
    {
        var spec = CommandBuilder.Custom(CustomCommandTemplate, host);
        if (spec is null)
        {
            return RemoteResult.Fail(host, KioskActionKind.Custom,
                "Kein eigener Befehl hinterlegt (Einstellungen → Eigener Befehl).");
        }

        return await RunSingleAsync(host, KioskActionKind.Custom, spec,
            "Eigener Befehl ausgeführt.", cancellationToken).ConfigureAwait(false);
    }

    private async Task<RemoteResult> RunSingleAsync(
        string host,
        KioskActionKind action,
        CommandSpec spec,
        string successText,
        CancellationToken cancellationToken)
    {
        if (DryRun)
        {
            return RemoteResult.Ok(host, action, "Testbetrieb: " + spec.ToDisplayString(), dryRun: true);
        }

        ProcessResult result;
        try
        {
            result = await _runner
                .RunAsync(spec.FileName, spec.Arguments, Timeout, cancellationToken)
                .ConfigureAwait(false);
        }
        catch (OperationCanceledException)
        {
            throw;
        }
        catch (Exception ex)
        {
            return RemoteResult.Fail(host, action, ex.Message);
        }

        return result.Success
            ? RemoteResult.Ok(host, action, successText)
            : RemoteResult.Fail(host, action, Explain(result));
    }

    /// <summary>Übersetzt die häufigsten Windows-Fehler in verständlichen Klartext.</summary>
    public static string Explain(ProcessResult result)
    {
        var text = result.BestErrorText();

        if (text.Contains("53", StringComparison.Ordinal) && text.Contains("Netzwerkpfad", StringComparison.OrdinalIgnoreCase))
        {
            return text + " — Rechner offline oder Datei- und Druckerfreigabe deaktiviert.";
        }

        if (text.Contains("Zugriff verweigert", StringComparison.OrdinalIgnoreCase)
            || text.Contains("Access is denied", StringComparison.OrdinalIgnoreCase)
            || text.Contains("(5)", StringComparison.Ordinal))
        {
            return text + " — Es werden Administratorrechte auf dem Zielrechner benötigt.";
        }

        if (text.Contains("1722", StringComparison.Ordinal)
            || text.Contains("RPC", StringComparison.OrdinalIgnoreCase))
        {
            return text + " — RPC nicht erreichbar (Firewall/Remoteverwaltung prüfen).";
        }

        return text;
    }
}

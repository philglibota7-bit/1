namespace KioskSender.Core.Status;

public enum HostState
{
    Unknown = 0,
    Online = 1,
    Offline = 2,
    Disabled = 3
}

/// <summary>Erreichbarkeit eines Rechners zum Zeitpunkt der letzten Prüfung.</summary>
public sealed record HostStatus(
    string Host,
    HostState State,
    long RoundtripMs,
    DateTime CheckedAt,
    DateTime? LastSeen)
{
    public static HostStatus Unknown(string host) =>
        new(host, HostState.Unknown, 0, DateTime.MinValue, null);

    public string ToDisplayText() => State switch
    {
        HostState.Online => $"Online ({RoundtripMs} ms)",
        HostState.Offline => LastSeen is null
            ? "Offline"
            : $"Offline (zuletzt {LastSeen.Value:dd.MM. HH:mm})",
        HostState.Disabled => "Deaktiviert",
        _ => "Unbekannt"
    };
}

/// <summary>Prüft die Erreichbarkeit eines Hosts. Abstrahiert für Tests.</summary>
public interface IHostProbe
{
    Task<HostStatus> ProbeAsync(string host, int timeoutMs, CancellationToken cancellationToken = default);
}

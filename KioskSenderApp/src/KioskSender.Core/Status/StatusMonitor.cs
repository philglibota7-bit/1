using System.Collections.Concurrent;

namespace KioskSender.Core.Status;

/// <summary>
/// Prüft eine Liste von Hosts parallel und merkt sich den letzten bekannten
/// Zustand samt "zuletzt gesehen"-Zeitpunkt.
/// </summary>
public sealed class StatusMonitor
{
    private readonly IHostProbe _probe;
    private readonly ConcurrentDictionary<string, HostStatus> _states =
        new(StringComparer.OrdinalIgnoreCase);

    public StatusMonitor(IHostProbe probe) => _probe = probe;

    public int TimeoutMs { get; set; } = 1200;

    public int MaxParallel { get; set; } = 32;

    public HostStatus Get(string host) =>
        _states.TryGetValue(host, out var status) ? status : HostStatus.Unknown(host);

    public IReadOnlyDictionary<string, HostStatus> Snapshot() =>
        new Dictionary<string, HostStatus>(_states, StringComparer.OrdinalIgnoreCase);

    public void Forget(string host) => _states.TryRemove(host, out _);

    public void Clear() => _states.Clear();

    /// <summary>Prüft alle Hosts und liefert nur die Einträge, deren Zustand sich geändert hat.</summary>
    public async Task<IReadOnlyList<HostStatus>> RefreshAsync(
        IEnumerable<string> hosts,
        CancellationToken cancellationToken = default)
    {
        var distinct = hosts
            .Where(h => !string.IsNullOrWhiteSpace(h))
            .Select(h => h.Trim())
            .Distinct(StringComparer.OrdinalIgnoreCase)
            .ToList();

        if (distinct.Count == 0)
        {
            return Array.Empty<HostStatus>();
        }

        var changed = new ConcurrentBag<HostStatus>();
        using var gate = new SemaphoreSlim(Math.Max(1, MaxParallel));

        var tasks = distinct.Select(async host =>
        {
            await gate.WaitAsync(cancellationToken).ConfigureAwait(false);
            try
            {
                var status = await _probe.ProbeAsync(host, TimeoutMs, cancellationToken).ConfigureAwait(false);
                var previous = _states.TryGetValue(host, out var p) ? p : null;

                // "Zuletzt gesehen" über Offline-Phasen hinweg mitnehmen.
                if (status.LastSeen is null && previous?.LastSeen is not null)
                {
                    status = status with { LastSeen = previous.LastSeen };
                }

                _states[host] = status;

                if (previous is null || previous.State != status.State)
                {
                    changed.Add(status);
                }
            }
            finally
            {
                gate.Release();
            }
        });

        await Task.WhenAll(tasks).ConfigureAwait(false);
        return changed.ToList();
    }
}

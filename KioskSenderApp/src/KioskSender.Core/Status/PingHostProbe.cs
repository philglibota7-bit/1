using System.Net.NetworkInformation;

namespace KioskSender.Core.Status;

/// <summary>Erreichbarkeitsprüfung per ICMP-Ping.</summary>
public sealed class PingHostProbe : IHostProbe
{
    public async Task<HostStatus> ProbeAsync(string host, int timeoutMs, CancellationToken cancellationToken = default)
    {
        var now = DateTime.Now;
        if (string.IsNullOrWhiteSpace(host))
        {
            return new HostStatus(host ?? string.Empty, HostState.Unknown, 0, now, null);
        }

        using var ping = new Ping();
        try
        {
            var reply = await ping.SendPingAsync(host.Trim(), timeoutMs).ConfigureAwait(false);
            cancellationToken.ThrowIfCancellationRequested();

            return reply.Status == IPStatus.Success
                ? new HostStatus(host, HostState.Online, reply.RoundtripTime, now, now)
                : new HostStatus(host, HostState.Offline, 0, now, null);
        }
        catch (OperationCanceledException)
        {
            throw;
        }
        catch (PingException)
        {
            // Namensauflösung fehlgeschlagen oder Netzwerk nicht verfügbar.
            return new HostStatus(host, HostState.Offline, 0, now, null);
        }
        catch (Exception)
        {
            return new HostStatus(host, HostState.Unknown, 0, now, null);
        }
    }
}

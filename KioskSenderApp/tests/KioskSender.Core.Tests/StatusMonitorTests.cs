using KioskSender.Core.Status;
using Xunit;

namespace KioskSender.Core.Tests;

file sealed class FakeProbe : IHostProbe
{
    public Dictionary<string, HostState> States { get; } = new(StringComparer.OrdinalIgnoreCase);

    public int Calls { get; private set; }

    public Task<HostStatus> ProbeAsync(string host, int timeoutMs, CancellationToken cancellationToken = default)
    {
        Calls++;
        var state = States.TryGetValue(host, out var s) ? s : HostState.Offline;
        var now = DateTime.Now;

        return Task.FromResult(new HostStatus(
            host,
            state,
            state == HostState.Online ? 5 : 0,
            now,
            state == HostState.Online ? now : null));
    }
}

public class StatusMonitorTests
{
    [Fact]
    public async Task First_refresh_reports_every_host_as_changed()
    {
        var probe = new FakeProbe();
        probe.States["a"] = HostState.Online;
        var monitor = new StatusMonitor(probe);

        var changed = await monitor.RefreshAsync(new[] { "a", "b" });

        Assert.Equal(2, changed.Count);
    }

    [Fact]
    public async Task Unchanged_hosts_are_not_reported_again()
    {
        var probe = new FakeProbe();
        probe.States["a"] = HostState.Online;
        var monitor = new StatusMonitor(probe);

        await monitor.RefreshAsync(new[] { "a" });
        var changed = await monitor.RefreshAsync(new[] { "a" });

        Assert.Empty(changed);
        Assert.Equal(HostState.Online, monitor.Get("a").State);
    }

    [Fact]
    public async Task State_change_is_reported()
    {
        var probe = new FakeProbe();
        probe.States["a"] = HostState.Online;
        var monitor = new StatusMonitor(probe);

        await monitor.RefreshAsync(new[] { "a" });
        probe.States["a"] = HostState.Offline;
        var changed = await monitor.RefreshAsync(new[] { "a" });

        Assert.Single(changed);
        Assert.Equal(HostState.Offline, changed[0].State);
    }

    [Fact]
    public async Task Last_seen_survives_going_offline()
    {
        var probe = new FakeProbe();
        probe.States["a"] = HostState.Online;
        var monitor = new StatusMonitor(probe);

        await monitor.RefreshAsync(new[] { "a" });
        var seenAt = monitor.Get("a").LastSeen;
        probe.States["a"] = HostState.Offline;
        await monitor.RefreshAsync(new[] { "a" });

        Assert.NotNull(seenAt);
        Assert.Equal(seenAt, monitor.Get("a").LastSeen);
        Assert.Equal(HostState.Offline, monitor.Get("a").State);
    }

    [Fact]
    public async Task Duplicate_and_blank_hosts_are_probed_once()
    {
        var probe = new FakeProbe();
        var monitor = new StatusMonitor(probe);

        await monitor.RefreshAsync(new[] { "a", "A", " a ", "", "   " });

        Assert.Equal(1, probe.Calls);
    }

    [Fact]
    public void Unknown_host_reports_unknown()
    {
        var monitor = new StatusMonitor(new FakeProbe());

        Assert.Equal(HostState.Unknown, monitor.Get("nie-geprüft").State);
    }
}

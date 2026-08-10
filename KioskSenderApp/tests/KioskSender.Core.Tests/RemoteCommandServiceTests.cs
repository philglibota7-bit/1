using KioskSender.Core.Model;
using KioskSender.Core.Remote;
using Xunit;

namespace KioskSender.Core.Tests;

public class RemoteCommandServiceTests
{
    private static (RemoteCommandService Service, FakeProcessRunner Runner) Create()
    {
        var runner = new FakeProcessRunner();
        return (new RemoteCommandService(runner), runner);
    }

    [Fact]
    public async Task Invalid_host_is_refused_before_anything_runs()
    {
        var (service, runner) = Create();

        var result = await service.ExecuteAsync("pc 01; del", KioskActionKind.Shutdown, "", 30, 60);

        Assert.False(result.Success);
        Assert.Empty(runner.Calls);
        Assert.Contains("Ungültig", result.Message);
    }

    [Fact]
    public async Task Message_runs_msg_exe()
    {
        var (service, runner) = Create();

        var result = await service.ExecuteAsync("PC-01", KioskActionKind.Message, "Hallo", 30, 45);

        Assert.True(result.Success);
        var call = Assert.Single(runner.Calls);
        Assert.Equal("msg.exe", call.FileName);
        Assert.Contains("/time:45", call.Arguments);
        Assert.Contains("Hallo", call.Arguments);
    }

    [Fact]
    public async Task Dry_run_executes_nothing()
    {
        var (service, runner) = Create();
        service.DryRun = true;

        var result = await service.ExecuteAsync("PC-01", KioskActionKind.Shutdown, "", 30, 60);

        Assert.True(result.Success);
        Assert.True(result.WasDryRun);
        Assert.Empty(runner.Calls);
        Assert.Contains("Testbetrieb", result.Message);
    }

    [Fact]
    public async Task Failure_is_reported_with_the_process_output()
    {
        var (service, runner) = Create();
        runner.Responses["shutdown.exe"] = new ProcessResult(1, "", "Zugriff verweigert.(5)", false);

        var result = await service.ExecuteAsync("PC-01", KioskActionKind.Shutdown, "", 30, 60);

        Assert.False(result.Success);
        Assert.Contains("Administratorrechte", result.Message);
    }

    [Fact]
    public async Task Timeout_is_reported_in_plain_language()
    {
        var (service, runner) = Create();
        runner.Responses["msg.exe"] = new ProcessResult(-1, "", "", true);

        var result = await service.ExecuteAsync("PC-01", KioskActionKind.Message, "x", 30, 60);

        Assert.False(result.Success);
        Assert.Contains("Zeitüberschreitung", result.Message);
    }

    [Fact]
    public async Task Logoff_queries_sessions_then_logs_each_one_off()
    {
        var (service, runner) = Create();
        runner.Handler = (file, _) => file.Equals("quser.exe", StringComparison.OrdinalIgnoreCase)
            ? new ProcessResult(0, """
                 USERNAME              SESSIONNAME        ID  STATE   IDLE TIME  LOGON TIME
                >admin                 console             1  Active      none   8/10/2026 7:00 AM
                 kiosk                                     3  Disc       1:20   8/10/2026 6:11 AM
                """, "", false)
            : new ProcessResult(0, "", "", false);

        var result = await service.ExecuteAsync("PC-01", KioskActionKind.Logoff, "", 30, 60);

        Assert.True(result.Success);
        Assert.Equal(3, runner.Calls.Count);
        Assert.Equal("quser.exe", runner.Calls[0].FileName);
        Assert.Equal("logoff.exe", runner.Calls[1].FileName);
        Assert.Equal("1", runner.Calls[1].Arguments[0]);
        Assert.Equal("3", runner.Calls[2].Arguments[0]);
    }

    [Fact]
    public async Task Logoff_without_sessions_does_nothing()
    {
        var (service, runner) = Create();
        runner.Responses["quser.exe"] = new ProcessResult(1, "Es ist kein Benutzer angemeldet.", "", false);

        var result = await service.ExecuteAsync("PC-01", KioskActionKind.Logoff, "", 30, 60);

        Assert.True(result.Success);
        Assert.Single(runner.Calls);
        Assert.Contains("Kein Benutzer", result.Message);
    }

    [Fact]
    public async Task Logoff_dry_run_queries_but_never_logs_off()
    {
        var (service, runner) = Create();
        service.DryRun = true;
        runner.Responses["quser.exe"] = new ProcessResult(0, """
             USERNAME              SESSIONNAME        ID  STATE   IDLE TIME  LOGON TIME
            >admin                 console             1  Active      none   8/10/2026 7:00 AM
            """, "", false);

        var result = await service.ExecuteAsync("PC-01", KioskActionKind.Logoff, "", 30, 60);

        Assert.True(result.WasDryRun);
        Assert.Single(runner.Calls);
        Assert.Equal("quser.exe", runner.Calls[0].FileName);
    }

    [Fact]
    public async Task Custom_without_a_template_fails_with_a_hint()
    {
        var (service, runner) = Create();

        var result = await service.ExecuteAsync("PC-01", KioskActionKind.Custom, "", 30, 60);

        Assert.False(result.Success);
        Assert.Empty(runner.Calls);
        Assert.Contains("Eigener Befehl", result.Message);
    }

    [Fact]
    public async Task Custom_uses_the_configured_template()
    {
        var (service, runner) = Create();
        service.CustomCommandTemplate = @"psexec.exe \\{host} -s -d cmd";

        var result = await service.ExecuteAsync("PC-01", KioskActionKind.Custom, "", 30, 60);

        Assert.True(result.Success);
        var call = Assert.Single(runner.Calls);
        Assert.Equal("psexec.exe", call.FileName);
        Assert.Equal(@"\\PC-01", call.Arguments[0]);
    }

    [Fact]
    public async Task None_action_does_nothing()
    {
        var (service, runner) = Create();

        var result = await service.ExecuteAsync("PC-01", KioskActionKind.None, "", 30, 60);

        Assert.True(result.Success);
        Assert.Empty(runner.Calls);
    }
}

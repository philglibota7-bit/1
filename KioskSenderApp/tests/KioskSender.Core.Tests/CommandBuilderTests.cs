using KioskSender.Core.Remote;
using Xunit;

namespace KioskSender.Core.Tests;

public class CommandBuilderTests
{
    [Theory]
    [InlineData("PC-01")]
    [InlineData("kiosk.firma.local")]
    [InlineData("192.168.1.50")]
    [InlineData("fe80::1")]
    public void Valid_hosts_are_accepted(string host) =>
        Assert.True(CommandBuilder.IsValidHost(host));

    [Theory]
    [InlineData("")]
    [InlineData("   ")]
    [InlineData("pc 01")]
    [InlineData("pc&calc")]
    [InlineData("\\\\pc01")]
    [InlineData("pc01;shutdown")]
    [InlineData("-pc01")]
    public void Invalid_hosts_are_rejected(string host) =>
        Assert.False(CommandBuilder.IsValidHost(host));

    [Fact]
    public void Message_builds_msg_arguments()
    {
        var spec = CommandBuilder.Message("PC-01", "Bitte speichern", 60);

        Assert.Equal("msg.exe", spec.FileName);
        Assert.Equal(new[] { "*", "/server:PC-01", "/time:60", "Bitte speichern" }, spec.Arguments);
    }

    [Fact]
    public void Message_keeps_quotes_as_a_single_argument()
    {
        var spec = CommandBuilder.Message("PC-01", "Er sagte \"jetzt\" bitte", 60);

        Assert.Equal("Er sagte \"jetzt\" bitte", spec.Arguments[3]);
        Assert.Equal(4, spec.Arguments.Count);
    }

    [Fact]
    public void Message_flattens_line_breaks()
    {
        var spec = CommandBuilder.Message("PC-01", "Zeile1\r\nZeile2", 60);

        Assert.DoesNotContain('\n', spec.Arguments[3]);
        Assert.DoesNotContain('\r', spec.Arguments[3]);
    }

    [Fact]
    public void Shutdown_uses_unc_host_and_force_flag()
    {
        var spec = CommandBuilder.Shutdown("PC-01", 60, "Feierabend");

        Assert.Equal("shutdown.exe", spec.FileName);
        Assert.Equal(new[] { "/s", "/f", "/m", @"\\PC-01", "/t", "60", "/c", "Feierabend" }, spec.Arguments);
    }

    [Fact]
    public void Restart_uses_the_r_switch()
    {
        var spec = CommandBuilder.Restart("PC-01", 30, "");

        Assert.Equal("/r", spec.Arguments[0]);
        Assert.DoesNotContain("/c", spec.Arguments);
    }

    [Fact]
    public void Shutdown_comment_is_truncated_to_the_windows_limit()
    {
        var spec = CommandBuilder.Shutdown("PC-01", 0, new string('x', 900));

        Assert.Equal(CommandBuilder.MaxCommentLength, spec.Arguments[^1].Length);
    }

    [Fact]
    public void Abort_targets_the_host()
    {
        var spec = CommandBuilder.AbortShutdown("PC-01");

        Assert.Equal(new[] { "/a", "/m", @"\\PC-01" }, spec.Arguments);
    }

    [Fact]
    public void Logoff_passes_session_id_and_server()
    {
        var spec = CommandBuilder.Logoff("PC-01", 3);

        Assert.Equal("logoff.exe", spec.FileName);
        Assert.Equal(new[] { "3", "/server:PC-01" }, spec.Arguments);
    }

    [Fact]
    public void Custom_replaces_the_host_placeholder()
    {
        var spec = CommandBuilder.Custom(@"C:\Tools\PsExec.exe \\{host} -s -d rundll32.exe user32.dll,LockWorkStation", "PC-01");

        Assert.NotNull(spec);
        Assert.Equal(@"C:\Tools\PsExec.exe", spec!.FileName);
        Assert.Equal(@"\\PC-01", spec.Arguments[0]);
        Assert.Contains("user32.dll,LockWorkStation", spec.Arguments);
    }

    [Fact]
    public void Custom_handles_quoted_paths()
    {
        var spec = CommandBuilder.Custom("\"C:\\Program Files\\Tools\\t.exe\" -h {host}", "PC-01");

        Assert.Equal(@"C:\Program Files\Tools\t.exe", spec!.FileName);
        Assert.Equal(new[] { "-h", "PC-01" }, spec.Arguments);
    }

    [Fact]
    public void Custom_returns_null_for_empty_template()
    {
        Assert.Null(CommandBuilder.Custom("", "PC-01"));
        Assert.Null(CommandBuilder.Custom("   ", "PC-01"));
    }

    [Fact]
    public void Tokenize_splits_on_whitespace_outside_quotes()
    {
        var tokens = CommandBuilder.Tokenize("a  \"b c\" d");

        Assert.Equal(new[] { "a", "b c", "d" }, tokens);
    }

    [Fact]
    public void Tokenize_keeps_empty_quoted_argument()
    {
        var tokens = CommandBuilder.Tokenize("tool \"\" x");

        Assert.Equal(new[] { "tool", "", "x" }, tokens);
    }
}

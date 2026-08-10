using KioskSender.Core.Remote;
using Xunit;

namespace KioskSender.Core.Tests;

public class QuserParserTests
{
    [Fact]
    public void Parses_english_output()
    {
        const string output = """
             USERNAME              SESSIONNAME        ID  STATE   IDLE TIME  LOGON TIME
            >admin                 console             1  Active      none   8/10/2026 7:00 AM
             kiosk                                     3  Disc       1:20   8/10/2026 6:11 AM
            """;

        var sessions = QuserParser.Parse(output);

        Assert.Equal(2, sessions.Count);

        Assert.Equal("admin", sessions[0].UserName);
        Assert.Equal("console", sessions[0].SessionName);
        Assert.Equal(1, sessions[0].SessionId);
        Assert.True(sessions[0].IsActive);

        Assert.Equal("kiosk", sessions[1].UserName);
        Assert.Equal(string.Empty, sessions[1].SessionName);
        Assert.Equal(3, sessions[1].SessionId);
        Assert.False(sessions[1].IsActive);
    }

    [Fact]
    public void Parses_german_output()
    {
        const string output = """
             BENUTZERNAME          SITZUNGSNAME       ID  STATUS  LEERLAUF  ANMELDEZEIT
            >kiosk                 console             1  Aktiv       keine  10.08.2026 07:00
            """;

        var session = Assert.Single(QuserParser.Parse(output));

        Assert.Equal("kiosk", session.UserName);
        Assert.Equal(1, session.SessionId);
        Assert.True(session.IsActive);
    }

    [Fact]
    public void Parses_rdp_session_names()
    {
        const string output = """
             USERNAME              SESSIONNAME        ID  STATE   IDLE TIME  LOGON TIME
             remote                rdp-tcp#0           2  Active        .    8/10/2026 7:00 AM
            """;

        var session = Assert.Single(QuserParser.Parse(output));

        Assert.Equal("rdp-tcp#0", session.SessionName);
        Assert.Equal(2, session.SessionId);
    }

    [Fact]
    public void Numeric_user_name_is_not_mistaken_for_the_id()
    {
        const string output = """
             USERNAME              SESSIONNAME        ID  STATE   IDLE TIME  LOGON TIME
             12345                 console             4  Active      none   8/10/2026 7:00 AM
            """;

        var session = Assert.Single(QuserParser.Parse(output));

        Assert.Equal("12345", session.UserName);
        Assert.Equal(4, session.SessionId);
    }

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("   ")]
    [InlineData("Es ist kein Benutzer angemeldet.")]
    public void Returns_empty_for_no_sessions(string? output) =>
        Assert.Empty(QuserParser.Parse(output));

    [Fact]
    public void Header_alone_yields_no_sessions()
    {
        const string output = " USERNAME              SESSIONNAME        ID  STATE   IDLE TIME  LOGON TIME";

        Assert.Empty(QuserParser.Parse(output));
    }
}

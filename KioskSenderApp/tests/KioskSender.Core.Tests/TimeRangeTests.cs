using KioskSender.Core.Model;
using Xunit;

namespace KioskSender.Core.Tests;

public class TimeRangeTests
{
    [Theory]
    [InlineData("08:00-17:00", 480, 1020)]
    [InlineData(" 8:00 - 17:30 ", 480, 1050)]
    [InlineData("08:00-24:00", 480, 1440)]
    public void TryParse_reads_normal_ranges(string text, int start, int end)
    {
        Assert.True(TimeRange.TryParse(text, out var range));
        Assert.Equal(start, range.StartMinutes);
        Assert.Equal(end, range.EndMinutes);
    }

    [Fact]
    public void TryParse_shifts_end_past_midnight()
    {
        Assert.True(TimeRange.TryParse("20:00-02:00", out var range));
        Assert.Equal(20 * 60, range.StartMinutes);
        Assert.Equal((24 + 2) * 60, range.EndMinutes);
        Assert.True(range.CrossesMidnight);
    }

    [Theory]
    [InlineData("")]
    [InlineData("kaputt")]
    [InlineData("08:00")]
    [InlineData("25:00-26:00")]
    [InlineData("08:70-09:00")]
    public void TryParse_rejects_invalid_text(string text)
    {
        Assert.False(TimeRange.TryParse(text, out _));
    }

    [Fact]
    public void ToString_roundtrips()
    {
        Assert.True(TimeRange.TryParse("08:05-17:45", out var range));
        Assert.Equal("08:05-17:45", range.ToString());
    }

    [Fact]
    public void Format_shows_midnight_end_as_24()
    {
        Assert.Equal("24:00", TimeRange.Format(1440));
        Assert.Equal("00:00", TimeRange.Format(0));
        Assert.Equal("02:00", TimeRange.Format(26 * 60));
    }

    [Fact]
    public void IsValid_requires_positive_duration()
    {
        Assert.False(new TimeRange(600, 600).IsValid);
        Assert.False(new TimeRange(600, 500).IsValid);
        Assert.True(new TimeRange(600, 601).IsValid);
    }
}

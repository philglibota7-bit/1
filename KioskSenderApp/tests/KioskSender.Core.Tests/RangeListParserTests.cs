using KioskSender.Core.Model;
using Xunit;

namespace KioskSender.Core.Tests;

public class RangeListParserTests
{
    [Fact]
    public void Parses_several_ranges()
    {
        Assert.True(RangeListParser.TryParse("08:00-12:00, 13:00-17:00", out var ranges, out var error));

        Assert.Equal(string.Empty, error);
        Assert.Equal(2, ranges.Count);
        Assert.Equal(480, ranges[0].StartMinutes);
        Assert.Equal(1020, ranges[1].EndMinutes);
    }

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("   ")]
    public void Empty_text_means_closed(string? text)
    {
        Assert.True(RangeListParser.TryParse(text, out var ranges, out _));
        Assert.Empty(ranges);
    }

    [Fact]
    public void Ranges_are_sorted()
    {
        Assert.True(RangeListParser.TryParse("13:00-17:00; 08:00-12:00", out var ranges, out _));

        Assert.Equal(480, ranges[0].StartMinutes);
    }

    [Fact]
    public void Overlapping_ranges_are_rejected_with_a_readable_message()
    {
        Assert.False(RangeListParser.TryParse("08:00-12:00, 11:00-17:00", out var ranges, out var error));

        Assert.Empty(ranges);
        Assert.Contains("überschneiden", error);
    }

    [Fact]
    public void Invalid_text_names_the_offending_part()
    {
        Assert.False(RangeListParser.TryParse("08:00-12:00, kaputt", out _, out var error));

        Assert.Contains("kaputt", error);
    }

    [Fact]
    public void Format_roundtrips()
    {
        Assert.True(RangeListParser.TryParse("08:00-12:00, 13:00-17:00", out var ranges, out _));

        Assert.Equal("08:00-12:00, 13:00-17:00", RangeListParser.Format(ranges));
    }

    [Fact]
    public void Total_duration_adds_up()
    {
        Assert.True(RangeListParser.TryParse("08:00-12:00, 13:00-17:00", out var ranges, out _));

        Assert.Equal(TimeSpan.FromHours(8), RangeListParser.TotalDuration(ranges));
    }

    [Fact]
    public void Touching_ranges_are_allowed()
    {
        Assert.True(RangeListParser.TryParse("08:00-12:00, 12:00-17:00", out var ranges, out _));

        Assert.Equal(2, ranges.Count);
    }
}

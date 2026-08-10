using System;
using System.Globalization;
using System.Windows;
using System.Windows.Data;
using System.Windows.Media;
using KioskSender.Core.Model;
using KioskSender.Core.Status;

namespace KioskSender.App.Infrastructure;

/// <summary>Erreichbarkeit -> Farbe.</summary>
public sealed class HostStateToBrushConverter : IValueConverter
{
    public object Convert(object? value, Type targetType, object? parameter, CultureInfo culture)
    {
        var state = value as HostState? ?? HostState.Unknown;
        return state switch
        {
            HostState.Online => Palette.Online,
            HostState.Offline => Palette.Offline,
            HostState.Disabled => Palette.Muted,
            _ => Palette.Unknown
        };
    }

    public object ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture) =>
        Binding.DoNothing;
}

/// <summary>Protokollebene -> Farbe.</summary>
public sealed class LogLevelToBrushConverter : IValueConverter
{
    public object Convert(object? value, Type targetType, object? parameter, CultureInfo culture)
    {
        var level = value as LogLevel? ?? LogLevel.Info;
        return level switch
        {
            LogLevel.Error => Palette.Offline,
            LogLevel.Warning => Palette.Warning,
            LogLevel.Success => Palette.Online,
            LogLevel.Debug => Palette.Muted,
            _ => Palette.Text
        };
    }

    public object ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture) =>
        Binding.DoNothing;
}

/// <summary>"#RRGGBB" -> Pinsel, mit Rückfall auf Grau bei ungültigem Wert.</summary>
public sealed class HexToBrushConverter : IValueConverter
{
    public object Convert(object? value, Type targetType, object? parameter, CultureInfo culture)
    {
        var hex = value as string;
        if (string.IsNullOrWhiteSpace(hex))
        {
            return Palette.Muted;
        }

        try
        {
            var color = (Color)ColorConverter.ConvertFromString(hex.Trim());
            var brush = new SolidColorBrush(color);
            brush.Freeze();
            return brush;
        }
        catch
        {
            return Palette.Muted;
        }
    }

    public object ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture) =>
        Binding.DoNothing;
}

/// <summary>true -> Visible. Parameter "invert" dreht die Bedeutung um.</summary>
public sealed class BoolToVisibilityConverter : IValueConverter
{
    public object Convert(object? value, Type targetType, object? parameter, CultureInfo culture)
    {
        var flag = value as bool? ?? false;
        if (string.Equals(parameter as string, "invert", StringComparison.OrdinalIgnoreCase))
        {
            flag = !flag;
        }

        return flag ? Visibility.Visible : Visibility.Collapsed;
    }

    public object ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture) =>
        value is Visibility.Visible;
}

/// <summary>Nicht-leerer Text -> Visible.</summary>
public sealed class StringToVisibilityConverter : IValueConverter
{
    public object Convert(object? value, Type targetType, object? parameter, CultureInfo culture) =>
        string.IsNullOrWhiteSpace(value as string) ? Visibility.Collapsed : Visibility.Visible;

    public object ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture) =>
        Binding.DoNothing;
}

/// <summary>true -> grün, false -> rot. Für Erfolgs-/Fehlerpunkte in Listen.</summary>
public sealed class BoolToBrushConverter : IValueConverter
{
    public object Convert(object? value, Type targetType, object? parameter, CultureInfo culture) =>
        value as bool? ?? false ? Palette.Online : Palette.Offline;

    public object ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture) =>
        Binding.DoNothing;
}

/// <summary>Kehrt einen Wahrheitswert um (z. B. für IsEnabled).</summary>
public sealed class InverseBooleanConverter : IValueConverter
{
    public object Convert(object? value, Type targetType, object? parameter, CultureInfo culture) =>
        !(value as bool? ?? false);

    public object ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture) =>
        !(value as bool? ?? false);
}

/// <summary>Die Farben der Oberfläche an einer Stelle.</summary>
public static class Palette
{
    public static readonly SolidColorBrush Online = Frozen("#3FBF6F");
    public static readonly SolidColorBrush Offline = Frozen("#E5484D");
    public static readonly SolidColorBrush Warning = Frozen("#F5A524");
    public static readonly SolidColorBrush Unknown = Frozen("#8B93A7");
    public static readonly SolidColorBrush Muted = Frozen("#6A7285");
    public static readonly SolidColorBrush Text = Frozen("#E6E9F0");
    public static readonly SolidColorBrush Accent = Frozen("#4C8DFF");

    private static SolidColorBrush Frozen(string hex)
    {
        var brush = new SolidColorBrush((Color)ColorConverter.ConvertFromString(hex));
        brush.Freeze();
        return brush;
    }
}

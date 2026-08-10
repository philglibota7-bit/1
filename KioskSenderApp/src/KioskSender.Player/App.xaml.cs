using System;
using System.IO;
using System.Threading;
using System.Windows;

namespace KioskSender.Player;

public partial class App : Application
{
    /// <summary>Standardordner, in den der Manager die Inhalte legt.</summary>
    public const string DefaultContentPath = @"C:\ProgramData\KioskPlayer";

    private Mutex? _singleInstance;

    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);

        _singleInstance = new Mutex(true, @"Local\KioskPlayer", out var isFirst);
        if (!isFirst)
        {
            // Zwei Player auf einem Bildschirm wären nur Flackern.
            Shutdown();
            return;
        }

        var options = PlayerOptions.Parse(e.Args);

        // Ein Fehler beim Abspielen darf den Kiosk nie in einen Fehlerdialog schicken.
        DispatcherUnhandledException += (_, args) =>
        {
            args.Handled = true;
            TryLog(args.Exception);
        };

        AppDomain.CurrentDomain.UnhandledException += (_, args) =>
        {
            if (args.ExceptionObject is Exception ex)
            {
                TryLog(ex);
            }
        };

        new PlayerWindow(options).Show();
    }

    protected override void OnExit(ExitEventArgs e)
    {
        _singleInstance?.Dispose();
        base.OnExit(e);
    }

    private static void TryLog(Exception ex)
    {
        try
        {
            File.AppendAllText(
                Path.Combine(DefaultContentPath, "player.log"),
                $"{DateTime.Now:u}\t{ex}{Environment.NewLine}");
        }
        catch
        {
            // Protokollieren ist auf einem Kiosk zweitrangig.
        }
    }
}

/// <summary>Startparameter des Players.</summary>
public sealed class PlayerOptions
{
    public string ContentPath { get; init; } = App.DefaultContentPath;

    /// <summary>Vollbild ohne Rahmen. Mit --fenster zum Einrichten abschaltbar.</summary>
    public bool FullScreen { get; init; } = true;

    /// <summary>Beenden mit Esc erlauben.</summary>
    public bool AllowExit { get; init; } = true;

    /// <summary>
    /// Liest die Kommandozeile:
    ///   KioskPlayer.exe [Ordner] [--fenster] [--kein-beenden]
    /// </summary>
    public static PlayerOptions Parse(string[] args)
    {
        var path = App.DefaultContentPath;
        var fullScreen = true;
        var allowExit = true;

        foreach (var arg in args)
        {
            switch (arg.ToLowerInvariant())
            {
                case "--fenster":
                case "--window":
                    fullScreen = false;
                    break;

                case "--kein-beenden":
                case "--no-exit":
                    allowExit = false;
                    break;

                default:
                    if (!arg.StartsWith("--", StringComparison.Ordinal))
                    {
                        path = arg;
                    }

                    break;
            }
        }

        return new PlayerOptions
        {
            ContentPath = path,
            FullScreen = fullScreen,
            AllowExit = allowExit
        };
    }
}

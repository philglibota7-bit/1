using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Windows;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Threading;
using KioskSender.Core.Content;

namespace KioskSender.Player;

public partial class PlayerWindow : Window
{
    private readonly PlayerOptions _options;
    private readonly DispatcherTimer _itemTimer = new();
    private readonly DispatcherTimer _reloadTimer = new();
    private readonly DispatcherTimer _hintTimer = new();

    private FileSystemWatcher? _watcher;
    private PlaylistCursor? _cursor;
    private Process? _presentation;

    /// <summary>
    /// Zählt jeden Elementwechsel. Späte Rückmeldungen (Video zu Ende,
    /// PowerPoint beendet) einer bereits abgelösten Wiedergabe werden damit
    /// erkannt und verworfen — sonst würde die Liste doppelt weiterspringen.
    /// </summary>
    private int _generation;

    public PlayerWindow(PlayerOptions options)
    {
        _options = options;
        InitializeComponent();

        if (options.FullScreen)
        {
            WindowStyle = WindowStyle.None;
            ResizeMode = ResizeMode.NoResize;
            WindowState = WindowState.Maximized;
            Topmost = true;
            Cursor = Cursors.None;
        }

        _itemTimer.Tick += (_, _) => ShowNext();

        // Der Manager schreibt playlist.json zuletzt; trotzdem kurz abwarten,
        // damit nicht mitten im Schreiben gelesen wird.
        _reloadTimer.Interval = TimeSpan.FromSeconds(2);
        _reloadTimer.Tick += (_, _) =>
        {
            _reloadTimer.Stop();
            LoadPlaylist(restart: true);
        };

        _hintTimer.Interval = TimeSpan.FromSeconds(6);
        _hintTimer.Tick += (_, _) =>
        {
            _hintTimer.Stop();
            HintPanel.Visibility = Visibility.Collapsed;
        };

        VideoStage.MediaEnded += OnVideoEnded;
        VideoStage.MediaFailed += OnVideoFailed;

        Loaded += OnLoaded;
        Closed += OnClosed;
        KeyDown += OnKeyDown;
        MouseMove += (_, _) => ShowHint();
    }

    private void OnLoaded(object sender, RoutedEventArgs e)
    {
        ShowHint();
        StartWatching();
        LoadPlaylist(restart: true);
    }

    private void OnClosed(object? sender, EventArgs e)
    {
        _itemTimer.Stop();
        _reloadTimer.Stop();
        _watcher?.Dispose();
        StopPresentation();
        StopVideo();
    }

    // ------------------------------------------------------------ Liste laden

    private void StartWatching()
    {
        try
        {
            Directory.CreateDirectory(_options.ContentPath);

            _watcher = new FileSystemWatcher(_options.ContentPath, Playlist.FileName)
            {
                NotifyFilter = NotifyFilters.LastWrite | NotifyFilters.FileName | NotifyFilters.Size,
                EnableRaisingEvents = true
            };

            void Changed(object? _, FileSystemEventArgs __) =>
                Dispatcher.BeginInvoke(() =>
                {
                    _reloadTimer.Stop();
                    _reloadTimer.Start();
                });

            _watcher.Changed += Changed;
            _watcher.Created += Changed;
            _watcher.Renamed += (_, _) => Dispatcher.BeginInvoke(() =>
            {
                _reloadTimer.Stop();
                _reloadTimer.Start();
            });
        }
        catch (Exception ex)
        {
            // Ohne Überwachung läuft der Player weiter — er merkt neue Inhalte
            // dann erst beim nächsten Start.
            ShowInfo("Inhalte werden nicht automatisch aktualisiert.", ex.Message);
        }
    }

    private void LoadPlaylist(bool restart)
    {
        var path = Path.Combine(_options.ContentPath, Playlist.FileName);

        if (!File.Exists(path))
        {
            _cursor = null;
            ShowInfo(
                "Warte auf Inhalte…",
                $"Dieser Rechner heißt {Environment.MachineName}.\n" +
                $"Der Manager legt die Inhalte hier ab:\n{_options.ContentPath}");
            return;
        }

        Playlist? playlist = null;
        try
        {
            playlist = Playlist.FromJson(File.ReadAllText(path));
        }
        catch (IOException)
        {
            // Datei wird gerade geschrieben — gleich noch einmal versuchen.
            _reloadTimer.Stop();
            _reloadTimer.Start();
            return;
        }

        if (playlist is null)
        {
            ShowInfo("Die Wiedergabeliste ist beschädigt.",
                "Bitte die Inhalte im Manager erneut senden.");
            return;
        }

        var missing = playlist.Items
            .Where(i => !File.Exists(Path.Combine(_options.ContentPath, i.FileName)))
            .Select(i => i.FileName)
            .ToList();

        if (missing.Count > 0)
        {
            // Fehlende Dateien überspringen statt schwarz zu bleiben.
            playlist.Items.RemoveAll(i => missing.Contains(i.FileName));
        }

        _cursor = new PlaylistCursor(playlist);

        if (_cursor.IsEmpty)
        {
            ShowInfo($"„{playlist.Name}“ enthält nichts Abspielbares.",
                missing.Count > 0
                    ? $"{missing.Count} Datei(en) fehlen im Ordner."
                    : "Im Manager Inhalte auswählen und erneut senden.");
            return;
        }

        if (restart)
        {
            _itemTimer.Stop();
            StopVideo();
            ShowNext();

            // Beim Wechsel kurz einblenden, was angekommen ist.
            ShowHint();
        }
    }

    // ------------------------------------------------------------ Abspielen

    private void ShowNext()
    {
        _itemTimer.Stop();
        StopVideo();

        var item = _cursor?.Next();
        if (item is null)
        {
            ShowInfo("Wiedergabe beendet.", "Es sind keine weiteren Inhalte vorhanden.");
            return;
        }

        var generation = ++_generation;
        var file = Path.Combine(_options.ContentPath, item.FileName);

        try
        {
            switch (item.Kind)
            {
                case MediaKind.Image:
                    ShowImage(file);
                    StartTimer(_cursor!.SecondsFor(item));
                    break;

                case MediaKind.Video:
                    ShowVideo(file, item.Seconds);
                    break;

                case MediaKind.Presentation:
                    ShowPresentation(file, item.Seconds, generation);
                    break;

                default:
                    ShowNext();
                    break;
            }
        }
        catch (Exception ex)
        {
            // Ein kaputtes Element darf die Wiedergabe nicht anhalten.
            ShowInfo($"„{item.FileName}“ konnte nicht angezeigt werden.", ex.Message);
            StartTimer(5);
        }
    }

    private void ShowImage(string file)
    {
        var bitmap = new BitmapImage();
        bitmap.BeginInit();
        bitmap.UriSource = new Uri(file);
        // OnLoad: Datei sofort komplett lesen und wieder freigeben, damit der
        // Manager sie beim nächsten Senden überschreiben kann.
        bitmap.CacheOption = BitmapCacheOption.OnLoad;
        bitmap.EndInit();
        bitmap.Freeze();

        ImageStage.Source = bitmap;
        SetStage(image: true, video: false, info: false);
    }

    private void ShowVideo(string file, int maxSeconds)
    {
        VideoStage.Source = new Uri(file);
        SetStage(image: false, video: true, info: false);
        VideoStage.Play();

        // Nur als Notbremse, falls das Ende nie gemeldet wird.
        if (maxSeconds > 0)
        {
            StartTimer(maxSeconds);
        }
    }

    private void ShowPresentation(string file, int maxSeconds, int generation)
    {
        SetStage(image: false, video: false, info: true);
        InfoHeadline.Text = "Präsentation wird geöffnet…";
        InfoDetail.Text = Path.GetFileName(file);

        var powerPoint = FindPowerPoint();
        var startInfo = powerPoint is null
            ? new ProcessStartInfo(file) { UseShellExecute = true }
            : new ProcessStartInfo(powerPoint) { UseShellExecute = false };

        if (powerPoint is not null)
        {
            // /S startet direkt die Bildschirmpräsentation.
            startInfo.ArgumentList.Add("/S");
            startInfo.ArgumentList.Add(file);
        }

        StopPresentation();

        // Vollbild kurz abgeben, sonst liegt der Player über der Präsentation.
        var wasTopmost = Topmost;
        Topmost = false;

        try
        {
            _presentation = Process.Start(startInfo);
        }
        catch (Exception ex)
        {
            Topmost = wasTopmost;
            ShowInfo("PowerPoint konnte nicht gestartet werden.",
                ex.Message + "\nIst PowerPoint auf diesem Rechner installiert?");
            StartTimer(8);
            return;
        }

        if (_presentation is null)
        {
            Topmost = wasTopmost;
            ShowNext();
            return;
        }

        _presentation.EnableRaisingEvents = true;
        _presentation.Exited += (_, _) => Dispatcher.BeginInvoke(() =>
        {
            if (generation != _generation)
            {
                return;
            }

            Topmost = wasTopmost;
            Activate();
            ShowNext();
        });

        if (maxSeconds > 0)
        {
            StartTimer(maxSeconds);
        }
    }

    private void StartTimer(int seconds)
    {
        if (seconds <= 0)
        {
            return;
        }

        _itemTimer.Interval = TimeSpan.FromSeconds(seconds);
        _itemTimer.Start();
    }

    private void OnVideoEnded(object sender, RoutedEventArgs e) => ShowNext();

    private void OnVideoFailed(object? sender, ExceptionRoutedEventArgs e)
    {
        ShowInfo("Video konnte nicht abgespielt werden.",
            e.ErrorException?.Message ?? "Fehlt auf diesem Rechner der passende Codec?");
        StartTimer(5);
    }

    private void StopVideo()
    {
        try
        {
            VideoStage.Stop();
            VideoStage.Source = null;
        }
        catch
        {
            // Beim Beenden nicht weiter beachten.
        }
    }

    private void StopPresentation()
    {
        var process = _presentation;
        _presentation = null;

        if (process is null)
        {
            return;
        }

        try
        {
            if (!process.HasExited)
            {
                process.Kill(entireProcessTree: true);
            }
        }
        catch
        {
            // Bereits beendet.
        }
        finally
        {
            process.Dispose();
        }
    }

    /// <summary>Sucht PowerPoint an den üblichen Stellen.</summary>
    private static string? FindPowerPoint()
    {
        var roots = new[]
        {
            Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles),
            Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86)
        };

        var relativePaths = new[]
        {
            @"Microsoft Office\root\Office16\POWERPNT.EXE",
            @"Microsoft Office\Office16\POWERPNT.EXE",
            @"Microsoft Office\root\Office15\POWERPNT.EXE",
            @"Microsoft Office\Office15\POWERPNT.EXE"
        };

        return (from root in roots
                where !string.IsNullOrEmpty(root)
                from relative in relativePaths
                select Path.Combine(root, relative))
            .FirstOrDefault(File.Exists);
    }

    // ------------------------------------------------------------ Anzeige

    private void SetStage(bool image, bool video, bool info)
    {
        ImageStage.Visibility = image ? Visibility.Visible : Visibility.Collapsed;
        VideoStage.Visibility = video ? Visibility.Visible : Visibility.Collapsed;
        InfoPanel.Visibility = info ? Visibility.Visible : Visibility.Collapsed;
    }

    private void ShowInfo(string headline, string detail)
    {
        InfoHeadline.Text = headline;
        InfoDetail.Text = detail;
        SetStage(image: false, video: false, info: true);
    }

    /// <summary>
    /// Kurze Einblendung: welcher Rechner, welche Wiedergabeliste, welche Taste.
    /// Damit sieht man beim Einrichten sofort, ob der richtige PC den richtigen
    /// Inhalt bekommen hat.
    /// </summary>
    private void ShowHint()
    {
        var playlist = _cursor?.Playlist;

        var what = playlist is null
            ? "keine Inhalte"
            : $"{playlist.Name} · {_cursor!.Items.Count} Datei(en)";

        var keys = _options.AllowExit
            ? "Esc beendet · Leertaste weiter · F5 neu laden"
            : "Leertaste weiter · F5 neu laden";

        HintText.Text = $"{Environment.MachineName}   |   {what}\n{keys}";

        HintPanel.Visibility = Visibility.Visible;
        _hintTimer.Stop();
        _hintTimer.Start();
    }

    private void OnKeyDown(object sender, KeyEventArgs e)
    {
        switch (e.Key)
        {
            case Key.Escape when _options.AllowExit:
                Close();
                break;

            case Key.Space or Key.Right or Key.PageDown:
                ShowNext();
                break;

            case Key.F5:
                LoadPlaylist(restart: true);
                break;

            case Key.Q when Keyboard.Modifiers.HasFlag(ModifierKeys.Control | ModifierKeys.Alt):
                // Notausstieg, auch wenn Esc gesperrt ist.
                Close();
                break;
        }
    }
}

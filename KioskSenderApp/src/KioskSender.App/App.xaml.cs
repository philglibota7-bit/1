using System;
using System.Globalization;
using System.IO;
using System.Threading;
using System.Windows;
using System.Windows.Markup;
using System.Windows.Threading;
using KioskSender.App.ViewModels;
using KioskSender.App.Views;
using KioskSender.Core.Logging;
using KioskSender.Core.Remote;
using KioskSender.Core.Services;
using KioskSender.Core.Status;
using KioskSender.Core.Storage;

namespace KioskSender.App;

public partial class App : Application
{
    private MainViewModel? _viewModel;

    /// <summary>Verhindert, dass die Anwendung mehrfach läuft und zwei Zeitmanager gegeneinander arbeiten.</summary>
    private Mutex? _singleInstance;

    protected override async void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);

        _singleInstance = new Mutex(true, @"Local\KioskSenderApp", out var isFirstInstance);
        if (!isFirstInstance)
        {
            MessageBox.Show(
                "KioskSenderApp läuft bereits. Es kann immer nur eine Instanz laufen, " +
                "damit sich nicht zwei Zeitmanager gegenseitig in die Quere kommen.",
                "KioskSenderApp",
                MessageBoxButton.OK,
                MessageBoxImage.Information);

            Shutdown();
            return;
        }

        // Datums- und Zeitformate der Oberfläche an die Windows-Einstellung koppeln.
        FrameworkElement.LanguageProperty.OverrideMetadata(
            typeof(FrameworkElement),
            new FrameworkPropertyMetadata(XmlLanguage.GetLanguage(CultureInfo.CurrentCulture.IetfLanguageTag)));

        DispatcherUnhandledException += OnDispatcherUnhandledException;
        AppDomain.CurrentDomain.UnhandledException += OnDomainUnhandledException;

        try
        {
            await StartAsync().ConfigureAwait(true);
        }
        catch (Exception ex)
        {
            MessageBox.Show(
                "Die Anwendung konnte nicht gestartet werden:\n\n" + ex,
                "KioskSenderApp",
                MessageBoxButton.OK,
                MessageBoxImage.Error);

            Shutdown(1);
        }
    }

    private async System.Threading.Tasks.Task StartAsync()
    {
        var store = new ConfigStore();
        var (config, warning) = await store.LoadAsync().ConfigureAwait(true);

        var log = new LogService(
            Path.Combine(ConfigStore.DefaultDirectory(), "logs"),
            config.Settings.LogCapacity);

        log.PurgeOldFiles(30);

        if (warning is not null)
        {
            log.Warning("Konfiguration", warning);
        }

        var manager = new KioskManager(
            config,
            new RemoteCommandService(new ProcessRunner()),
            new StatusMonitor(new PingHostProbe()),
            log);

        _viewModel = new MainViewModel(store, manager);

        var window = new MainWindow(_viewModel);
        MainWindow = window;

        if (config.Settings.StartMinimized)
        {
            window.WindowState = WindowState.Minimized;
        }

        window.Show();

        await _viewModel.InitializeAsync().ConfigureAwait(true);
    }

    protected override void OnExit(ExitEventArgs e)
    {
        _viewModel?.Dispose();
        _singleInstance?.Dispose();
        base.OnExit(e);
    }

    private void OnDispatcherUnhandledException(object sender, DispatcherUnhandledExceptionEventArgs e)
    {
        // Ein Fehler in der Oberfläche darf den Zeitmanager nicht mitreißen.
        e.Handled = true;

        MessageBox.Show(
            "Es ist ein Fehler aufgetreten:\n\n" + e.Exception.Message,
            "KioskSenderApp",
            MessageBoxButton.OK,
            MessageBoxImage.Warning);
    }

    private void OnDomainUnhandledException(object sender, UnhandledExceptionEventArgs e)
    {
        if (e.ExceptionObject is Exception ex)
        {
            try
            {
                File.AppendAllText(
                    Path.Combine(ConfigStore.DefaultDirectory(), "crash.log"),
                    $"{DateTime.Now:u}\t{ex}{Environment.NewLine}");
            }
            catch
            {
                // Im Absturzfall ist nichts mehr zu retten.
            }
        }
    }
}

using System;
using System.ComponentModel;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using KioskSender.App.ViewModels;

namespace KioskSender.App.Views;

public partial class MainWindow : Window
{
    private readonly MainViewModel _viewModel;
    private bool _closeConfirmed;

    public MainWindow(MainViewModel viewModel)
    {
        _viewModel = viewModel;
        InitializeComponent();

        DataContext = viewModel;

        viewModel.Confirm = (title, message) =>
            MessageBox.Show(this, message, title, MessageBoxButton.YesNo, MessageBoxImage.Question)
                == MessageBoxResult.Yes;

        viewModel.ShowError = (title, message) =>
            MessageBox.Show(this, message, title, MessageBoxButton.OK, MessageBoxImage.Warning);

        viewModel.PickFolder = startPath =>
        {
            var dialog = new Microsoft.Win32.OpenFolderDialog
            {
                Title = "Ordner mit den Medien wählen",
                Multiselect = false
            };

            if (!string.IsNullOrWhiteSpace(startPath) && System.IO.Directory.Exists(startPath))
            {
                dialog.InitialDirectory = startPath;
            }

            return dialog.ShowDialog(this) == true ? dialog.FolderName : null;
        };
    }

    /// <summary>
    /// Die Mehrfachauswahl einer DataGrid ist nicht bindbar, deshalb wird sie
    /// hier in das Ansichtsmodell gespiegelt.
    /// </summary>
    private void OnPcSelectionChanged(object sender, SelectionChangedEventArgs e)
    {
        if (sender is not DataGrid grid)
        {
            return;
        }

        _viewModel.SelectedPcs.Clear();
        foreach (var item in grid.SelectedItems.OfType<PcItemViewModel>())
        {
            _viewModel.SelectedPcs.Add(item);
        }

        _viewModel.NotifyTargetsChanged();
    }

    private void OnScopeChanged(object sender, RoutedEventArgs e)
    {
        if (sender is not RadioButton { Tag: string tag })
        {
            return;
        }

        _viewModel.SendScope = tag switch
        {
            "Group" => SendScope.Group,
            "All" => SendScope.All,
            _ => SendScope.Selection
        };
    }

    protected override void OnClosing(CancelEventArgs e)
    {
        base.OnClosing(e);

        if (_closeConfirmed)
        {
            return;
        }

        if (_viewModel.SchedulerEnabled && !AskAboutRunningScheduler())
        {
            e.Cancel = true;
            return;
        }

        // Schließen kurz aufhalten, bis die Konfiguration sicher auf der Platte liegt.
        e.Cancel = true;
        _ = CloseAfterShutdownAsync();
    }

    private bool AskAboutRunningScheduler() =>
        MessageBox.Show(
            this,
            "Der Zeitmanager ist aktiv. Wenn die Anwendung geschlossen wird, werden keine " +
            "geplanten Aktionen mehr ausgeführt.\n\nTrotzdem beenden?",
            "KioskSenderApp beenden",
            MessageBoxButton.YesNo,
            MessageBoxImage.Question) == MessageBoxResult.Yes;

    private async System.Threading.Tasks.Task CloseAfterShutdownAsync()
    {
        try
        {
            await _viewModel.ShutdownAsync().ConfigureAwait(true);
        }
        catch (Exception ex)
        {
            MessageBox.Show(this, ex.Message, "Beenden", MessageBoxButton.OK, MessageBoxImage.Warning);
        }

        _closeConfirmed = true;
        Close();
    }
}

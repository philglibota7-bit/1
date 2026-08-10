using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Diagnostics;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using KioskSender.App.Infrastructure;
using KioskSender.Core.Content;

namespace KioskSender.App.ViewModels;

/// <summary>Ein Ordner der Medienbibliothek in der Auswahlliste.</summary>
public sealed class LibraryFolderViewModel
{
    public LibraryFolderViewModel(LibraryFolder folder, int level)
    {
        Folder = folder;
        Level = level;
    }

    public LibraryFolder Folder { get; }

    public int Level { get; }

    public string Name => Folder.Name;

    public string Summary => Folder.Summary;

    /// <summary>Einrückung, die die Ordnertiefe sichtbar macht.</summary>
    public System.Windows.Thickness Indent => new(Level * 18, 0, 0, 0);

    public bool HasContent => Folder.Items.Count > 0;

    public override string ToString() => Name;
}

public sealed partial class MainViewModel
{
    private LibraryFolderViewModel? _selectedLibraryFolder;
    private Playlist? _currentPlaylist;
    private string _libraryStatus = "Noch kein Medienordner gewählt.";
    private string _deployStatus = string.Empty;
    private double _deployPercent;
    private bool _isDeploying;
    private CancellationTokenSource? _deployCancel;

    // ------------------------------------------------------------ Sammlungen

    public ObservableCollection<LibraryFolderViewModel> LibraryFolders { get; } = new();

    /// <summary>Die Elemente der gerade gewählten Wiedergabeliste.</summary>
    public ObservableCollection<MediaItem> PlaylistItems { get; } = new();

    /// <summary>Ordnerauswahl per Dialog — wird vom Fenster gesetzt.</summary>
    public Func<string?, string?> PickFolder { get; set; } = _ => null;

    // ------------------------------------------------------------ Zustand

    public string MediaRootPath
    {
        get => Settings.MediaRootPath;
        set
        {
            if (Settings.MediaRootPath == value)
            {
                return;
            }

            Settings.MediaRootPath = value ?? string.Empty;
            OnPropertyChanged();
            MarkDirty();
            RefreshLibrary();
        }
    }

    public string ContentTargetTemplate
    {
        get => Settings.ContentTargetTemplate;
        set
        {
            var text = string.IsNullOrWhiteSpace(value)
                ? @"\\{host}\C$\ProgramData\KioskPlayer"
                : value.Trim();

            if (Settings.ContentTargetTemplate == text)
            {
                return;
            }

            Settings.ContentTargetTemplate = text;
            ApplyContentSettings();
            OnPropertyChanged();
            MarkDirty();
        }
    }

    public int DefaultImageSeconds
    {
        get => Settings.DefaultImageSeconds;
        set
        {
            var clamped = Math.Clamp(value, 1, 3600);
            if (Settings.DefaultImageSeconds == clamped)
            {
                return;
            }

            Settings.DefaultImageSeconds = clamped;
            ApplyContentSettings();
            OnPropertyChanged();
            MarkDirty();
            RebuildPlaylist();
        }
    }

    public bool PlaylistLoop
    {
        get => Settings.PlaylistLoop;
        set
        {
            if (Settings.PlaylistLoop == value)
            {
                return;
            }

            Settings.PlaylistLoop = value;
            OnPropertyChanged();
            MarkDirty();
            RebuildPlaylist();
        }
    }

    public bool PlaylistShuffle
    {
        get => Settings.PlaylistShuffle;
        set
        {
            if (Settings.PlaylistShuffle == value)
            {
                return;
            }

            Settings.PlaylistShuffle = value;
            OnPropertyChanged();
            MarkDirty();
            RebuildPlaylist();
        }
    }

    public bool RemoveObsoleteContent
    {
        get => Settings.RemoveObsoleteContent;
        set
        {
            if (Settings.RemoveObsoleteContent == value)
            {
                return;
            }

            Settings.RemoveObsoleteContent = value;
            ApplyContentSettings();
            OnPropertyChanged();
            MarkDirty();
        }
    }

    public LibraryFolderViewModel? SelectedLibraryFolder
    {
        get => _selectedLibraryFolder;
        set
        {
            if (SetProperty(ref _selectedLibraryFolder, value))
            {
                RebuildPlaylist();
            }
        }
    }

    public Playlist? CurrentPlaylist
    {
        get => _currentPlaylist;
        private set
        {
            if (SetProperty(ref _currentPlaylist, value))
            {
                OnPropertyChanged(nameof(HasPlaylist), nameof(PlaylistSummary), nameof(PlaylistName));
            }
        }
    }

    public bool HasPlaylist => _currentPlaylist is not null && _currentPlaylist.PlayableCount > 0;

    public string PlaylistName => _currentPlaylist?.Name ?? "—";

    public string PlaylistSummary
    {
        get
        {
            if (_currentPlaylist is null)
            {
                return "Links einen Ordner wählen.";
            }

            if (_currentPlaylist.PlayableCount == 0)
            {
                return "Dieser Ordner enthält keine Bilder, Videos oder Präsentationen.";
            }

            return $"{_currentPlaylist.PlayableCount} Datei(en) · " +
                   $"{MediaItem.FormatSize(_currentPlaylist.TotalBytes)} · " +
                   $"Durchlauf {_currentPlaylist.DurationText}";
        }
    }

    public string LibraryStatus
    {
        get => _libraryStatus;
        private set => SetProperty(ref _libraryStatus, value);
    }

    /// <summary>Die für den Versand angehakten PCs.</summary>
    public IReadOnlyList<PcItemViewModel> ChosenPcs =>
        Pcs.Where(p => p.IsChosen && p.Enabled).ToList();

    public int ChosenPcCount => ChosenPcs.Count;

    public string ChosenPcSummary
    {
        get
        {
            var chosen = ChosenPcs;
            if (chosen.Count == 0)
            {
                return "Noch kein Empfänger angehakt.";
            }

            var offline = chosen.Count(p => p.State == Core.Status.HostState.Offline);
            return offline == 0
                ? $"{chosen.Count} PC(s) ausgewählt."
                : $"{chosen.Count} PC(s) ausgewählt — davon {offline} gerade offline.";
        }
    }

    public bool IsDeploying
    {
        get => _isDeploying;
        private set
        {
            if (SetProperty(ref _isDeploying, value))
            {
                OnPropertyChanged(nameof(CanSendContent));
                RelayCommand.RaiseCanExecuteChanged();
            }
        }
    }

    public bool CanSendContent => !IsDeploying && HasPlaylist && ChosenPcCount > 0;

    public double DeployPercent
    {
        get => _deployPercent;
        private set => SetProperty(ref _deployPercent, value);
    }

    public string DeployStatus
    {
        get => _deployStatus;
        private set => SetProperty(ref _deployStatus, value);
    }

    // ------------------------------------------------------------ Befehle

    public RelayCommand BrowseMediaFolderCommand { get; private set; } = null!;
    public RelayCommand RefreshLibraryCommand { get; private set; } = null!;
    public RelayCommand OpenMediaFolderCommand { get; private set; } = null!;
    public RelayCommand ChooseAllPcsCommand { get; private set; } = null!;
    public RelayCommand ChooseNoPcsCommand { get; private set; } = null!;
    public RelayCommand ChooseGroupPcsCommand { get; private set; } = null!;
    public AsyncRelayCommand SendContentCommand { get; private set; } = null!;
    public RelayCommand CancelSendContentCommand { get; private set; } = null!;

    private void BuildContentCommands(Action<Exception> onError)
    {
        BrowseMediaFolderCommand = new RelayCommand(() =>
        {
            var picked = PickFolder(Settings.MediaRootPath);
            if (!string.IsNullOrWhiteSpace(picked))
            {
                MediaRootPath = picked;
            }
        });

        RefreshLibraryCommand = new RelayCommand(RefreshLibrary);

        OpenMediaFolderCommand = new RelayCommand(() =>
        {
            if (string.IsNullOrWhiteSpace(Settings.MediaRootPath))
            {
                return;
            }

            try
            {
                Process.Start(new ProcessStartInfo(Settings.MediaRootPath) { UseShellExecute = true });
            }
            catch (Exception ex)
            {
                ShowError("Ordner öffnen", ex.Message);
            }
        }, () => !string.IsNullOrWhiteSpace(Settings.MediaRootPath));

        ChooseAllPcsCommand = new RelayCommand(() => SetChosen(Pcs.Where(p => p.Enabled), true));
        ChooseNoPcsCommand = new RelayCommand(() => SetChosen(Pcs, false));

        ChooseGroupPcsCommand = new RelayCommand(() =>
        {
            if (SelectedGroup is null)
            {
                return;
            }

            SetChosen(Pcs, false);
            SetChosen(Pcs.Where(p => p.Enabled && p.Model.GroupId == SelectedGroup.Id), true);
        }, () => SelectedGroup is not null);

        SendContentCommand = new AsyncRelayCommand(SendContentAsync, () => CanSendContent, onError);

        CancelSendContentCommand = new RelayCommand(
            () => _deployCancel?.Cancel(),
            () => IsDeploying);
    }

    private void SetChosen(IEnumerable<PcItemViewModel> pcs, bool chosen)
    {
        foreach (var pc in pcs)
        {
            pc.IsChosen = chosen;
        }

        NotifyChosenChanged();
    }

    public void NotifyChosenChanged()
    {
        OnPropertyChanged(nameof(ChosenPcCount), nameof(ChosenPcSummary), nameof(CanSendContent));
        RelayCommand.RaiseCanExecuteChanged();
    }

    private void ApplyContentSettings() => _manager.ApplySettings();

    // ------------------------------------------------------------ Bibliothek

    /// <summary>Liest den Medienordner neu ein und füllt die Ordnerliste.</summary>
    public void RefreshLibrary()
    {
        var previousPath = _selectedLibraryFolder?.Folder.FullPath;

        LibraryFolders.Clear();

        if (string.IsNullOrWhiteSpace(Settings.MediaRootPath))
        {
            LibraryStatus = "Noch kein Medienordner gewählt — oben auf „Ordner wählen“ klicken.";
            SelectedLibraryFolder = null;
            return;
        }

        var result = _manager.ScanLibrary();

        if (!result.Success)
        {
            LibraryStatus = result.Error ?? "Der Medienordner konnte nicht gelesen werden.";
            SelectedLibraryFolder = null;
            return;
        }

        AddFolder(result.Root!, 0);

        LibraryStatus = result.Error
                        ?? $"{LibraryFolders.Count} Ordner · {result.Root!.TotalItemCount} Datei(en) · " +
                        MediaItem.FormatSize(result.Root.TotalBytes);

        // Die vorherige Auswahl möglichst wiederherstellen.
        SelectedLibraryFolder =
            LibraryFolders.FirstOrDefault(f => f.Folder.FullPath == previousPath)
            ?? LibraryFolders.FirstOrDefault(f => f.HasContent)
            ?? LibraryFolders.FirstOrDefault();
    }

    private void AddFolder(LibraryFolder folder, int level)
    {
        LibraryFolders.Add(new LibraryFolderViewModel(folder, level));

        foreach (var child in folder.Folders)
        {
            AddFolder(child, level + 1);
        }
    }

    private void RebuildPlaylist()
    {
        PlaylistItems.Clear();

        if (_selectedLibraryFolder is null)
        {
            CurrentPlaylist = null;
            return;
        }

        var playlist = _manager.BuildPlaylist(_selectedLibraryFolder.Folder);
        CurrentPlaylist = playlist;

        var position = 1;
        foreach (var item in playlist.Items)
        {
            item.Position = position++;
            PlaylistItems.Add(item);
        }

        OnPropertyChanged(nameof(PlaylistSummary), nameof(CanSendContent));
        RelayCommand.RaiseCanExecuteChanged();
    }

    // ------------------------------------------------------------ Senden

    private async Task SendContentAsync()
    {
        var playlist = _currentPlaylist;
        var targets = ChosenPcs.Select(p => p.Model).ToList();

        if (playlist is null || targets.Count == 0)
        {
            return;
        }

        if (!Settings.DryRun)
        {
            var names = string.Join(", ", targets.Take(8).Select(t => t.DisplayName));
            if (targets.Count > 8)
            {
                names += $" … (+{targets.Count - 8})";
            }

            var question =
                $"„{playlist.Name}“ mit {playlist.PlayableCount} Datei(en) " +
                $"({MediaItem.FormatSize(playlist.TotalBytes)}) an {targets.Count} PC(s) senden?\n\n{names}\n\n" +
                "Vorhandene Inhalte auf diesen PCs werden ersetzt.";

            if (!Confirm("Inhalte senden", question))
            {
                DeployStatus = "Abgebrochen.";
                return;
            }
        }

        _deployCancel?.Dispose();
        _deployCancel = CancellationTokenSource.CreateLinkedTokenSource(_shutdown.Token);

        IsDeploying = true;
        DeployPercent = 0;
        DeployStatus = "Übertragung läuft…";

        var progress = new Progress<DeployProgress>(p =>
        {
            DeployPercent = p.Percent;
            DeployStatus = p.Text;
        });

        try
        {
            var results = await _manager
                .DeployContentAsync(playlist, targets, progress, _deployCancel.Token)
                .ConfigureAwait(true);

            var ok = results.Count(r => r.Success);
            var failed = results.Count - ok;

            DeployPercent = 100;
            DeployStatus = failed == 0
                ? $"Fertig — an {ok} PC(s) gesendet."
                : $"{ok} von {results.Count} PC(s) erfolgreich, {failed} fehlgeschlagen (siehe Protokoll).";

            StatusMessage = DeployStatus;
        }
        catch (OperationCanceledException)
        {
            DeployStatus = "Übertragung abgebrochen.";
        }
        finally
        {
            IsDeploying = false;
        }
    }
}

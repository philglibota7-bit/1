using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Data;
using System.Windows.Threading;
using KioskSender.App.Infrastructure;
using KioskSender.Core.Logging;
using KioskSender.Core.Model;
using KioskSender.Core.Remote;
using KioskSender.Core.Services;
using KioskSender.Core.Status;
using KioskSender.Core.Storage;

namespace KioskSender.App.ViewModels;

/// <summary>Eintrag für Auswahllisten (Gruppe / Zeitplan), inklusive "keine".</summary>
public sealed class ChoiceItem
{
    public ChoiceItem(Guid? id, string name)
    {
        Id = id;
        Name = name;
    }

    public Guid? Id { get; }

    public string Name { get; }

    public override string ToString() => Name;
}

/// <summary>Eintrag für die Aktionsauswahl mit deutschem Anzeigetext.</summary>
public sealed class ActionChoice
{
    public ActionChoice(KioskActionKind kind)
    {
        Kind = kind;
        Name = kind.ToDisplayName();
    }

    public KioskActionKind Kind { get; }

    public string Name { get; }

    public override string ToString() => Name;
}

public enum SendScope
{
    Selection,
    Group,
    All
}

/// <summary>Das Ansichtsmodell des Hauptfensters.</summary>
public sealed class MainViewModel : ObservableObject, IDisposable
{
    private readonly ConfigStore _store;
    private readonly KioskManager _manager;
    private readonly LogService _log;

    private readonly DispatcherTimer _schedulerTimer = new();
    private readonly DispatcherTimer _statusTimer = new();
    private readonly DispatcherTimer _uiTimer = new();
    private readonly DispatcherTimer _saveTimer = new();

    private readonly CancellationTokenSource _shutdown = new();

    private PcItemViewModel? _selectedPc;
    private GroupItemViewModel? _selectedGroup;
    private ScheduleItemViewModel? _selectedSchedule;
    private ScheduleExceptionViewModel? _selectedException;

    private string _pcFilter = string.Empty;
    private string _statusMessage = "Bereit.";
    private string _messageText = "Bitte speichern Sie Ihre Arbeit.";
    private SendScope _sendScope = SendScope.Selection;
    private bool _isBusy;
    private bool _isDirty;
    private string _clockText = string.Empty;

    /// <summary>Sperrt die Zuordnungs-Setter, während die Auswahllisten neu aufgebaut werden.</summary>
    private bool _suspendChoiceBinding;

    public MainViewModel(ConfigStore store, KioskManager manager)
    {
        _store = store;
        _manager = manager;
        _log = manager.Log;

        Pcs = new ObservableCollection<PcItemViewModel>();
        Groups = new ObservableCollection<GroupItemViewModel>();
        Schedules = new ObservableCollection<ScheduleItemViewModel>();
        LogEntries = new ObservableCollection<LogEntry>();
        GroupChoices = new ObservableCollection<ChoiceItem>();
        ScheduleChoices = new ObservableCollection<ChoiceItem>();
        SelectedPcs = new ObservableCollection<PcItemViewModel>();

        PcsView = CollectionViewSource.GetDefaultView(Pcs);
        PcsView.Filter = FilterPc;

        // Zweite, eigenständige Sicht: Zwei DataGrids dürfen sich keine Sicht
        // teilen, sonst reißen sie sich gegenseitig die Auswahl weg.
        ManagedPcsView = new CollectionViewSource { Source = Pcs }.View;
        ManagedPcsView.Filter = FilterPc;

        CloseActions = new[]
        {
            new ActionChoice(KioskActionKind.Shutdown),
            new ActionChoice(KioskActionKind.Restart),
            new ActionChoice(KioskActionKind.Logoff),
            new ActionChoice(KioskActionKind.Message),
            new ActionChoice(KioskActionKind.Custom),
            new ActionChoice(KioskActionKind.None)
        };

        _log.EntryAdded += OnLogEntryAdded;

        BuildCommands();
        SetupTimers();
    }

    // ------------------------------------------------------------ Sammlungen

    public ObservableCollection<PcItemViewModel> Pcs { get; }

    public ICollectionView PcsView { get; }

    /// <summary>Eigene Sicht für die Tabelle auf der Registerkarte „Gruppen &amp; PCs“.</summary>
    public ICollectionView ManagedPcsView { get; }

    public ObservableCollection<GroupItemViewModel> Groups { get; }

    public ObservableCollection<ScheduleItemViewModel> Schedules { get; }

    public ObservableCollection<LogEntry> LogEntries { get; }

    public ObservableCollection<ChoiceItem> GroupChoices { get; }

    public ObservableCollection<ChoiceItem> ScheduleChoices { get; }

    /// <summary>Wird vom Fenster aus der Mehrfachauswahl der Tabelle gefüllt.</summary>
    public ObservableCollection<PcItemViewModel> SelectedPcs { get; }

    public IReadOnlyList<ActionChoice> CloseActions { get; }

    public AppSettings Settings => _manager.Config.Settings;

    /// <summary>Rückfrage beim Benutzer — wird vom Fenster gesetzt.</summary>
    public Func<string, string, bool> Confirm { get; set; } = (_, _) => true;

    /// <summary>Fehlermeldung anzeigen — wird vom Fenster gesetzt.</summary>
    public Action<string, string> ShowError { get; set; } = (_, _) => { };

    // ------------------------------------------------------------ Zustand

    public PcItemViewModel? SelectedPc
    {
        get => _selectedPc;
        set
        {
            if (SetProperty(ref _selectedPc, value))
            {
                OnPropertyChanged(nameof(HasSelectedPc), nameof(SelectedPcGroupId), nameof(SelectedPcScheduleId));
            }
        }
    }

    public bool HasSelectedPc => _selectedPc is not null;

    public Guid? SelectedPcGroupId
    {
        get => _selectedPc?.Model.GroupId;
        set
        {
            if (_suspendChoiceBinding || _selectedPc is null || _selectedPc.Model.GroupId == value)
            {
                return;
            }

            _selectedPc.Model.GroupId = value;
            OnPropertyChanged();
            RefreshDerivedData();
            MarkDirty();
        }
    }

    public Guid? SelectedPcScheduleId
    {
        get => _selectedPc?.Model.ScheduleId;
        set
        {
            if (_suspendChoiceBinding || _selectedPc is null || _selectedPc.Model.ScheduleId == value)
            {
                return;
            }

            _selectedPc.Model.ScheduleId = value;
            OnPropertyChanged();
            RefreshDerivedData();
            MarkDirty();
        }
    }

    public GroupItemViewModel? SelectedGroup
    {
        get => _selectedGroup;
        set
        {
            if (SetProperty(ref _selectedGroup, value))
            {
                OnPropertyChanged(nameof(HasSelectedGroup), nameof(SelectedGroupScheduleId));
                RefreshViews();
            }
        }
    }

    public bool HasSelectedGroup => _selectedGroup is not null;

    public Guid? SelectedGroupScheduleId
    {
        get => _selectedGroup?.Model.ScheduleId;
        set
        {
            if (_suspendChoiceBinding || _selectedGroup is null || _selectedGroup.Model.ScheduleId == value)
            {
                return;
            }

            _selectedGroup.Model.ScheduleId = value;
            OnPropertyChanged();
            RefreshDerivedData();
            MarkDirty();
        }
    }

    public ScheduleItemViewModel? SelectedSchedule
    {
        get => _selectedSchedule;
        set
        {
            if (SetProperty(ref _selectedSchedule, value))
            {
                OnPropertyChanged(nameof(HasSelectedSchedule));
            }
        }
    }

    public bool HasSelectedSchedule => _selectedSchedule is not null;

    public ScheduleExceptionViewModel? SelectedException
    {
        get => _selectedException;
        set => SetProperty(ref _selectedException, value);
    }

    public string PcFilter
    {
        get => _pcFilter;
        set
        {
            if (SetProperty(ref _pcFilter, value))
            {
                RefreshViews();
            }
        }
    }

    public string MessageText
    {
        get => _messageText;
        set => SetProperty(ref _messageText, value);
    }

    public SendScope SendScope
    {
        get => _sendScope;
        set
        {
            if (SetProperty(ref _sendScope, value))
            {
                OnPropertyChanged(nameof(TargetSummary));
            }
        }
    }

    public string StatusMessage
    {
        get => _statusMessage;
        set => SetProperty(ref _statusMessage, value);
    }

    public string ClockText
    {
        get => _clockText;
        private set => SetProperty(ref _clockText, value);
    }

    public bool IsBusy
    {
        get => _isBusy;
        private set => SetProperty(ref _isBusy, value);
    }

    public bool IsDirty
    {
        get => _isDirty;
        private set
        {
            if (SetProperty(ref _isDirty, value))
            {
                OnPropertyChanged(nameof(SaveStateText));
            }
        }
    }

    public string SaveStateText => IsDirty ? "Nicht gespeicherte Änderungen" : "Gespeichert";

    public bool DryRun
    {
        get => Settings.DryRun;
        set
        {
            if (Settings.DryRun == value)
            {
                return;
            }

            Settings.DryRun = value;
            _manager.ApplySettings();
            OnPropertyChanged();
            _log.Info("Einstellungen", value
                ? "Testbetrieb eingeschaltet — es werden keine Befehle mehr ausgeführt."
                : "Testbetrieb ausgeschaltet — Befehle werden wieder ausgeführt.");
            MarkDirty();
        }
    }

    public bool SchedulerEnabled
    {
        get => Settings.SchedulerEnabled;
        set
        {
            if (Settings.SchedulerEnabled == value)
            {
                return;
            }

            Settings.SchedulerEnabled = value;
            OnPropertyChanged();
            _log.Info("Zeitmanager", value ? "Zeitmanager aktiviert." : "Zeitmanager angehalten.");
            MarkDirty();
        }
    }

    public string CustomCommand
    {
        get => Settings.CustomCommand;
        set
        {
            if (Settings.CustomCommand == value)
            {
                return;
            }

            Settings.CustomCommand = value ?? string.Empty;
            _manager.ApplySettings();
            OnPropertyChanged();
            MarkDirty();
        }
    }

    public int StatusIntervalSeconds
    {
        get => Settings.StatusIntervalSeconds;
        set
        {
            var clamped = Math.Clamp(value, 5, 3600);
            if (Settings.StatusIntervalSeconds == clamped)
            {
                return;
            }

            Settings.StatusIntervalSeconds = clamped;
            _statusTimer.Interval = TimeSpan.FromSeconds(clamped);
            OnPropertyChanged();
            MarkDirty();
        }
    }

    public int ManualCountdownSeconds
    {
        get => Settings.ManualCountdownSeconds;
        set
        {
            var clamped = Math.Clamp(value, 0, 3600);
            if (Settings.ManualCountdownSeconds == clamped)
            {
                return;
            }

            Settings.ManualCountdownSeconds = clamped;
            OnPropertyChanged();
            MarkDirty();
        }
    }

    public int MessageDisplaySeconds
    {
        get => Settings.MessageDisplaySeconds;
        set
        {
            var clamped = Math.Clamp(value, 5, 3600);
            if (Settings.MessageDisplaySeconds == clamped)
            {
                return;
            }

            Settings.MessageDisplaySeconds = clamped;
            OnPropertyChanged();
            MarkDirty();
        }
    }

    public string ConfigPath => _store.FilePath;

    /// <summary>Beschreibt, wen ein Sendebefehl treffen würde.</summary>
    public string TargetSummary
    {
        get
        {
            var targets = ResolveSendTargets();
            return SendScope switch
            {
                SendScope.Selection => $"{targets.Count} ausgewählte(r) PC(s)",
                SendScope.Group => _selectedGroup is null
                    ? "Keine Gruppe gewählt"
                    : $"Gruppe „{_selectedGroup.Name}“ ({targets.Count} PCs)",
                _ => $"Alle aktiven PCs ({targets.Count})"
            };
        }
    }

    // ------------------------------------------------------------ Befehle

    public AsyncRelayCommand SaveCommand { get; private set; } = null!;
    public AsyncRelayCommand RefreshStatusCommand { get; private set; } = null!;
    public RelayCommand AddPcCommand { get; private set; } = null!;
    public RelayCommand RemovePcCommand { get; private set; } = null!;
    public RelayCommand DuplicatePcCommand { get; private set; } = null!;
    public RelayCommand AddGroupCommand { get; private set; } = null!;
    public RelayCommand RemoveGroupCommand { get; private set; } = null!;
    public RelayCommand AddScheduleCommand { get; private set; } = null!;
    public RelayCommand RemoveScheduleCommand { get; private set; } = null!;
    public RelayCommand DuplicateScheduleCommand { get; private set; } = null!;
    public RelayCommand AddExceptionCommand { get; private set; } = null!;
    public RelayCommand RemoveExceptionCommand { get; private set; } = null!;
    public RelayCommand ClearLogCommand { get; private set; } = null!;
    public RelayCommand ExportLogCommand { get; private set; } = null!;
    public RelayCommand AssignSelectedToGroupCommand { get; private set; } = null!;

    public AsyncRelayCommand SendMessageCommand { get; private set; } = null!;
    public AsyncRelayCommand SendShutdownCommand { get; private set; } = null!;
    public AsyncRelayCommand SendRestartCommand { get; private set; } = null!;
    public AsyncRelayCommand SendLogoffCommand { get; private set; } = null!;
    public AsyncRelayCommand SendAbortCommand { get; private set; } = null!;
    public AsyncRelayCommand SendCustomCommand { get; private set; } = null!;

    private void BuildCommands()
    {
        void OnError(Exception ex)
        {
            _log.Error("Anwendung", ex.Message);
            ShowError("Fehler", ex.Message);
        }

        SaveCommand = new AsyncRelayCommand(SaveAsync, onError: OnError);
        RefreshStatusCommand = new AsyncRelayCommand(RefreshStatusAsync, () => !IsBusy, OnError);

        AddPcCommand = new RelayCommand(AddPc);
        RemovePcCommand = new RelayCommand(RemovePc, () => SelectedPcs.Count > 0 || _selectedPc is not null);
        DuplicatePcCommand = new RelayCommand(DuplicatePc, () => _selectedPc is not null);

        AddGroupCommand = new RelayCommand(AddGroup);
        RemoveGroupCommand = new RelayCommand(RemoveGroup, () => _selectedGroup is not null);

        AddScheduleCommand = new RelayCommand(AddSchedule);
        RemoveScheduleCommand = new RelayCommand(RemoveSchedule, () => _selectedSchedule is not null);
        DuplicateScheduleCommand = new RelayCommand(DuplicateSchedule, () => _selectedSchedule is not null);

        AddExceptionCommand = new RelayCommand(AddException, () => _selectedSchedule is not null);
        RemoveExceptionCommand = new RelayCommand(RemoveException, () => _selectedException is not null);

        ClearLogCommand = new RelayCommand(() =>
        {
            _log.Clear();
            LogEntries.Clear();
        });

        ExportLogCommand = new RelayCommand(ExportLog);
        AssignSelectedToGroupCommand = new RelayCommand(AssignSelectedToGroup, () => SelectedPcs.Count > 0);

        SendMessageCommand = new AsyncRelayCommand(
            () => SendAsync(KioskActionKind.Message, MessageText), () => !IsBusy, OnError);

        SendShutdownCommand = new AsyncRelayCommand(
            () => SendAsync(KioskActionKind.Shutdown, MessageText), () => !IsBusy, OnError);

        SendRestartCommand = new AsyncRelayCommand(
            () => SendAsync(KioskActionKind.Restart, MessageText), () => !IsBusy, OnError);

        SendLogoffCommand = new AsyncRelayCommand(
            () => SendAsync(KioskActionKind.Logoff, string.Empty), () => !IsBusy, OnError);

        SendAbortCommand = new AsyncRelayCommand(
            () => SendAsync(KioskActionKind.AbortShutdown, string.Empty), () => !IsBusy, OnError);

        SendCustomCommand = new AsyncRelayCommand(
            () => SendAsync(KioskActionKind.Custom, string.Empty), () => !IsBusy, OnError);
    }

    // ------------------------------------------------------------ Zeitgeber

    private void SetupTimers()
    {
        _schedulerTimer.Interval = TimeSpan.FromSeconds(Math.Clamp(Settings.SchedulerTickSeconds, 5, 300));
        _schedulerTimer.Tick += OnSchedulerTick;

        _statusTimer.Interval = TimeSpan.FromSeconds(Math.Clamp(Settings.StatusIntervalSeconds, 5, 3600));
        _statusTimer.Tick += OnStatusTick;

        _uiTimer.Interval = TimeSpan.FromSeconds(5);
        _uiTimer.Tick += OnUiTick;

        _saveTimer.Interval = TimeSpan.FromSeconds(8);
        _saveTimer.Tick += OnSaveTick;
    }

    public void StartTimers()
    {
        _schedulerTimer.Start();
        _statusTimer.Start();
        _uiTimer.Start();
        _saveTimer.Start();
    }

    private async void OnSchedulerTick(object? sender, EventArgs e)
    {
        try
        {
            await _manager.TickAsync(DateTime.Now, _shutdown.Token).ConfigureAwait(true);
            UpdateScheduleStates();
        }
        catch (OperationCanceledException)
        {
            // Anwendung wird beendet.
        }
        catch (Exception ex)
        {
            _log.Error("Zeitmanager", "Takt fehlgeschlagen: " + ex.Message);
        }
    }

    private async void OnStatusTick(object? sender, EventArgs e) => await RefreshStatusAsync().ConfigureAwait(true);

    private void OnUiTick(object? sender, EventArgs e)
    {
        ClockText = DateTime.Now.ToString("dddd, dd.MM.yyyy  HH:mm");
        UpdateScheduleStates();
    }

    private async void OnSaveTick(object? sender, EventArgs e)
    {
        if (!IsDirty)
        {
            return;
        }

        try
        {
            await SaveAsync().ConfigureAwait(true);
        }
        catch (Exception ex)
        {
            _log.Error("Speichern", ex.Message);
        }
    }

    // ------------------------------------------------------------ Laden / Speichern

    public async Task InitializeAsync()
    {
        ClockText = DateTime.Now.ToString("dddd, dd.MM.yyyy  HH:mm");

        foreach (var entry in _log.Snapshot())
        {
            LogEntries.Add(entry);
        }

        RebuildFromConfig();
        _log.Info("Anwendung", $"Konfiguration geladen: {_store.FilePath}");

        await RefreshStatusAsync().ConfigureAwait(true);
        StartTimers();
    }

    /// <summary>Baut alle Ansichtsmodelle aus der aktuellen Konfiguration neu auf.</summary>
    public void RebuildFromConfig()
    {
        var config = _manager.Config;

        Pcs.Clear();
        foreach (var pc in config.Pcs.OrderBy(p => p.DisplayName, StringComparer.CurrentCultureIgnoreCase))
        {
            var item = new PcItemViewModel(pc);
            Track(item);
            Pcs.Add(item);
        }

        Groups.Clear();
        foreach (var group in config.Groups.OrderBy(g => g.SortIndex))
        {
            var item = new GroupItemViewModel(group);
            Track(item);
            Groups.Add(item);
        }

        Schedules.Clear();
        foreach (var schedule in config.Schedules.OrderBy(s => s.Name, StringComparer.CurrentCultureIgnoreCase))
        {
            var item = new ScheduleItemViewModel(schedule);
            TrackSchedule(item);
            Schedules.Add(item);
        }

        RefreshChoices();
        RefreshDerivedData();
    }

    /// <summary>
    /// Baut die Auswahllisten für Gruppe und Zeitplan neu auf.
    /// Nur aufrufen, wenn sich Bestand oder Namen geändert haben: Während des
    /// Neuaufbaus setzt WPF die gebundene Auswahl kurzzeitig auf null, deshalb
    /// sind die betroffenen Setter währenddessen gesperrt.
    /// </summary>
    public void RefreshChoices()
    {
        var config = _manager.Config;
        _suspendChoiceBinding = true;
        try
        {
            GroupChoices.Clear();
            GroupChoices.Add(new ChoiceItem(null, "(keine Gruppe)"));
            foreach (var group in config.Groups.OrderBy(g => g.SortIndex))
            {
                GroupChoices.Add(new ChoiceItem(group.Id, group.Name));
            }

            ScheduleChoices.Clear();
            ScheduleChoices.Add(new ChoiceItem(null, "(kein Zeitplan)"));
            foreach (var schedule in config.Schedules.OrderBy(s => s.Name, StringComparer.CurrentCultureIgnoreCase))
            {
                ScheduleChoices.Add(new ChoiceItem(schedule.Id, schedule.Name));
            }
        }
        finally
        {
            _suspendChoiceBinding = false;
        }

        // Die Auswahl erst nach dem Neuaufbau wieder an die Oberfläche melden.
        OnPropertyChanged(nameof(SelectedPcGroupId), nameof(SelectedPcScheduleId), nameof(SelectedGroupScheduleId));
    }

    /// <summary>Gruppenname, Farbe, Zeitplanname und Erreichbarkeit je PC — günstig.</summary>
    private void RefreshPcMetadata()
    {
        var config = _manager.Config;

        foreach (var pc in Pcs)
        {
            var group = config.FindGroup(pc.Model.GroupId);
            pc.GroupName = group?.Name ?? "—";
            pc.GroupColor = group?.ColorHex ?? "#6A7285";
            pc.ScheduleName = config.EffectiveSchedule(pc.Model)?.Name ?? "—";
            pc.Status = _manager.Monitor.Get(pc.Host);
        }
    }

    /// <summary>Kennzahlen der Gruppen — günstig.</summary>
    private void RefreshGroupCounts()
    {
        var config = _manager.Config;

        foreach (var group in Groups)
        {
            var members = Pcs.Where(p => p.Model.GroupId == group.Id).ToList();
            group.PcCount = members.Count;
            group.OnlineCount = members.Count(p => p.State == HostState.Online);
            group.ScheduleName = config.FindSchedule(group.Model.ScheduleId)?.Name ?? "Kein Zeitplan";
        }
    }

    /// <summary>
    /// Alles auffrischen, einschließlich der Zeitplanauswertung.
    /// Die Auswertung rechnet je PC ein Zwei-Wochen-Fenster durch — deshalb wird
    /// sie beim Tippen bewusst nicht angestoßen (siehe RefreshAfterEdit).
    /// </summary>
    public void RefreshDerivedData()
    {
        RefreshPcMetadata();
        RefreshGroupCounts();
        UpdateScheduleStates();
        OnPropertyChanged(nameof(TargetSummary));
        RefreshViews();
    }

    /// <summary>Schlanke Variante für Änderungen beim Tippen.</summary>
    private void RefreshAfterEdit()
    {
        RefreshPcMetadata();
        RefreshGroupCounts();
        OnPropertyChanged(nameof(TargetSummary));
        RefreshViews();
    }

    private void RefreshViews()
    {
        PcsView.Refresh();
        ManagedPcsView.Refresh();
    }

    private string DescribeGroupWindow(GroupItemViewModel group)
    {
        var schedule = _manager.Config.FindSchedule(group.Model.ScheduleId);
        if (schedule is null)
        {
            return "Ohne Zeitplan — der Zeitmanager greift hier nicht ein.";
        }

        var now = DateTime.Now;
        var state = Core.Scheduling.ScheduleEvaluator.Evaluate(schedule, now);

        if (state.IsOpen && state.Current is not null)
        {
            return $"Geöffnet bis {state.Current.End:HH:mm} Uhr.";
        }

        return state.Next is not null
            ? $"Geschlossen — nächste Öffnung {state.Next.Start:ddd, dd.MM. HH:mm} Uhr."
            : "Geschlossen — keine weitere Öffnung geplant.";
    }

    private void UpdateScheduleStates()
    {
        var now = DateTime.Now;
        foreach (var pc in Pcs)
        {
            pc.ScheduleState = _manager.StateOf(pc.Model, now);
        }

        foreach (var group in Groups)
        {
            group.WindowText = DescribeGroupWindow(group);
        }
    }

    public void MarkDirty()
    {
        IsDirty = true;
        RelayCommand.RaiseCanExecuteChanged();
    }

    /// <summary>
    /// Wird vom Fenster gerufen, wenn sich die Mehrfachauswahl der Tabelle
    /// geändert hat: Zielbeschreibung und Befehlsverfügbarkeit auffrischen.
    /// </summary>
    public void NotifyTargetsChanged()
    {
        OnPropertyChanged(nameof(TargetSummary));
        RelayCommand.RaiseCanExecuteChanged();
    }

    // ---------------------------------------------------- Änderungsverfolgung

    /// <summary>
    /// Eigenschaften, deren Änderung wirklich eine Konfigurationsänderung ist.
    /// Abgeleitete Anzeigewerte (Status, Zeitfenster, Kennzahlen) stehen bewusst
    /// nicht darin — sonst würde die Anwendung im Sekundentakt speichern.
    /// </summary>
    private static readonly HashSet<string> EditableProperties = new(StringComparer.Ordinal)
    {
        nameof(PcItemViewModel.Name),
        nameof(PcItemViewModel.Host),
        nameof(PcItemViewModel.Enabled),
        nameof(PcItemViewModel.Note),
        nameof(GroupItemViewModel.ColorHex),
        nameof(ScheduleItemViewModel.WarnText),
        nameof(ScheduleItemViewModel.OpenText),
        nameof(ScheduleItemViewModel.WarnMinutesText),
        nameof(ScheduleItemViewModel.CloseAction),
        nameof(ScheduleItemViewModel.CloseGraceMinutes),
        nameof(ScheduleItemViewModel.CloseCountdownSeconds),
        nameof(DayPlanViewModel.RangesText),
        nameof(ScheduleExceptionViewModel.Date),
        nameof(ScheduleExceptionViewModel.Closed)
    };

    private void Track(INotifyPropertyChanged item)
    {
        item.PropertyChanged -= OnTrackedPropertyChanged;
        item.PropertyChanged += OnTrackedPropertyChanged;
    }

    private void TrackSchedule(ScheduleItemViewModel schedule)
    {
        Track(schedule);

        foreach (var day in schedule.Days)
        {
            Track(day);
        }

        foreach (var exception in schedule.Exceptions)
        {
            Track(exception);
        }

        schedule.Exceptions.CollectionChanged += (_, e) =>
        {
            if (e.NewItems is not null)
            {
                foreach (ScheduleExceptionViewModel item in e.NewItems)
                {
                    Track(item);
                }
            }

            MarkDirty();
        };
    }

    private void OnTrackedPropertyChanged(object? sender, PropertyChangedEventArgs e)
    {
        if (e.PropertyName is null || !EditableProperties.Contains(e.PropertyName))
        {
            return;
        }

        MarkDirty();

        // Name, Host, Aktiv-Kennzeichen und Farbe wirken sich auf andere Ansichten aus.
        if (e.PropertyName is nameof(PcItemViewModel.Name)
            or nameof(PcItemViewModel.Host)
            or nameof(PcItemViewModel.Enabled)
            or nameof(GroupItemViewModel.ColorHex))
        {
            RefreshAfterEdit();
        }

        // Eine umbenannte Gruppe oder ein umbenannter Zeitplan muss auch in den
        // Auswahllisten neu beschriftet werden.
        if (e.PropertyName == nameof(GroupItemViewModel.Name)
            && sender is GroupItemViewModel or ScheduleItemViewModel)
        {
            RefreshChoices();
        }
    }

    public async Task SaveAsync()
    {
        foreach (var schedule in Schedules)
        {
            schedule.SyncExceptions();
        }

        await _store.SaveAsync(_manager.Config, _shutdown.Token).ConfigureAwait(true);
        _manager.ApplySettings();
        IsDirty = false;
        StatusMessage = $"Gespeichert um {DateTime.Now:HH:mm:ss}.";
    }

    // ------------------------------------------------------------ Status

    public async Task RefreshStatusAsync()
    {
        if (IsBusy)
        {
            return;
        }

        IsBusy = true;
        try
        {
            await _manager.RefreshStatusAsync(_shutdown.Token).ConfigureAwait(true);

            foreach (var pc in Pcs)
            {
                pc.Status = _manager.Monitor.Get(pc.Host);
            }

            foreach (var group in Groups)
            {
                var members = Pcs.Where(p => p.Model.GroupId == group.Id).ToList();
                group.PcCount = members.Count;
                group.OnlineCount = members.Count(p => p.State == HostState.Online);
            }

            var online = Pcs.Count(p => p.State == HostState.Online);
            StatusMessage = $"{online} von {Pcs.Count(p => p.Enabled)} aktiven PCs erreichbar " +
                            $"(geprüft {DateTime.Now:HH:mm:ss}).";
        }
        catch (OperationCanceledException)
        {
            // Anwendung wird beendet.
        }
        finally
        {
            IsBusy = false;
        }
    }

    // ------------------------------------------------------------ Senden

    private IReadOnlyList<KioskPc> ResolveSendTargets() => SendScope switch
    {
        SendScope.Selection => SelectedPcs
            .Where(p => p.Enabled)
            .Select(p => p.Model)
            .ToList(),

        SendScope.Group => _selectedGroup is null
            ? Array.Empty<KioskPc>()
            : Pcs.Where(p => p.Enabled && p.Model.GroupId == _selectedGroup.Id)
                 .Select(p => p.Model)
                 .ToList(),

        _ => Pcs.Where(p => p.Enabled).Select(p => p.Model).ToList()
    };

    private async Task SendAsync(KioskActionKind action, string text)
    {
        var targets = ResolveSendTargets();
        if (targets.Count == 0)
        {
            StatusMessage = "Kein Ziel ausgewählt.";
            return;
        }

        if (action == KioskActionKind.Message && string.IsNullOrWhiteSpace(text))
        {
            StatusMessage = "Bitte zuerst einen Nachrichtentext eingeben.";
            return;
        }

        if (!action.IsHarmless() && !Settings.DryRun)
        {
            var names = string.Join(", ", targets.Take(8).Select(t => t.DisplayName));
            if (targets.Count > 8)
            {
                names += $" … (+{targets.Count - 8})";
            }

            var question = $"{action.ToDisplayName()} für {targets.Count} PC(s) wirklich ausführen?\n\n{names}";
            if (!Confirm("Aktion bestätigen", question))
            {
                StatusMessage = "Abgebrochen.";
                return;
            }
        }

        IsBusy = true;
        try
        {
            var results = await _manager.SendAsync(
                targets,
                action,
                text,
                Settings.ManualCountdownSeconds,
                Settings.MessageDisplaySeconds,
                "Sender",
                _shutdown.Token).ConfigureAwait(true);

            var ok = results.Count(r => r.Success);
            StatusMessage = $"{action.ToDisplayName()}: {ok} von {results.Count} erfolgreich.";
        }
        finally
        {
            IsBusy = false;
        }
    }

    // ------------------------------------------------------------ PCs

    private void AddPc()
    {
        var pc = new KioskPc
        {
            Name = "Neuer PC",
            Host = string.Empty,
            GroupId = _selectedGroup?.Id
        };

        _manager.Config.Pcs.Add(pc);
        var item = new PcItemViewModel(pc);
        Track(item);
        Pcs.Add(item);
        SelectedPc = item;
        RefreshDerivedData();
        MarkDirty();
        StatusMessage = "PC angelegt — bitte Namen und Hostnamen eintragen.";
    }

    private void RemovePc()
    {
        var toRemove = SelectedPcs.Count > 0
            ? SelectedPcs.ToList()
            : _selectedPc is null ? new List<PcItemViewModel>() : new List<PcItemViewModel> { _selectedPc };

        if (toRemove.Count == 0)
        {
            return;
        }

        var names = string.Join(", ", toRemove.Take(6).Select(p => p.DisplayName));
        if (!Confirm("PC entfernen", $"{toRemove.Count} PC(s) wirklich entfernen?\n\n{names}"))
        {
            return;
        }

        foreach (var item in toRemove)
        {
            _manager.Config.Pcs.Remove(item.Model);
            _manager.Monitor.Forget(item.Host);
            Pcs.Remove(item);
        }

        SelectedPcs.Clear();
        SelectedPc = null;
        RefreshDerivedData();
        MarkDirty();
        StatusMessage = $"{toRemove.Count} PC(s) entfernt.";
    }

    private void DuplicatePc()
    {
        if (_selectedPc is null)
        {
            return;
        }

        var copy = _selectedPc.Model.Clone();
        copy.Id = Guid.NewGuid();
        copy.Name = _selectedPc.Model.DisplayName + " (Kopie)";
        copy.Host = string.Empty;

        _manager.Config.Pcs.Add(copy);
        var item = new PcItemViewModel(copy);
        Track(item);
        Pcs.Add(item);
        SelectedPc = item;
        RefreshDerivedData();
        MarkDirty();
    }

    private void AssignSelectedToGroup()
    {
        if (SelectedPcs.Count == 0)
        {
            return;
        }

        var groupId = _selectedGroup?.Id;
        foreach (var pc in SelectedPcs)
        {
            pc.Model.GroupId = groupId;
        }

        RefreshDerivedData();
        MarkDirty();
        StatusMessage = groupId is null
            ? $"{SelectedPcs.Count} PC(s) aus der Gruppe entfernt."
            : $"{SelectedPcs.Count} PC(s) der Gruppe „{_selectedGroup!.Name}“ zugeordnet.";
    }

    // ------------------------------------------------------------ Gruppen

    private static readonly string[] GroupPalette =
    {
        "#4C8DFF", "#3FBF6F", "#F5A524", "#E5484D", "#A46BFF", "#22C1C3", "#FF7AB6", "#8B93A7"
    };

    private void AddGroup()
    {
        var group = new PcGroup
        {
            Name = "Neue Gruppe",
            ColorHex = GroupPalette[_manager.Config.Groups.Count % GroupPalette.Length],
            SortIndex = _manager.Config.Groups.Count
        };

        _manager.Config.Groups.Add(group);
        var item = new GroupItemViewModel(group);
        Track(item);
        Groups.Add(item);
        SelectedGroup = item;
        RefreshChoices();
        RefreshDerivedData();
        MarkDirty();
    }

    private void RemoveGroup()
    {
        if (_selectedGroup is null)
        {
            return;
        }

        var members = Pcs.Count(p => p.Model.GroupId == _selectedGroup.Id);
        var question = members == 0
            ? $"Gruppe „{_selectedGroup.Name}“ entfernen?"
            : $"Gruppe „{_selectedGroup.Name}“ entfernen?\n\n{members} PC(s) bleiben erhalten und stehen " +
              "anschließend ohne Gruppe und ohne Zeitplan da.";

        if (!Confirm("Gruppe entfernen", question))
        {
            return;
        }

        foreach (var pc in Pcs.Where(p => p.Model.GroupId == _selectedGroup.Id))
        {
            pc.Model.GroupId = null;
        }

        _manager.Config.Groups.Remove(_selectedGroup.Model);
        Groups.Remove(_selectedGroup);
        SelectedGroup = null;
        RefreshChoices();
        RefreshDerivedData();
        MarkDirty();
    }

    // ------------------------------------------------------------ Zeitpläne

    private void AddSchedule()
    {
        var schedule = WeeklySchedule.CreateOfficeDefault();
        schedule.Name = "Neuer Zeitplan";

        _manager.Config.Schedules.Add(schedule);
        var item = new ScheduleItemViewModel(schedule);
        TrackSchedule(item);
        Schedules.Add(item);
        SelectedSchedule = item;
        RefreshChoices();
        RefreshDerivedData();
        MarkDirty();
    }

    private void DuplicateSchedule()
    {
        if (_selectedSchedule is null)
        {
            return;
        }

        _selectedSchedule.SyncExceptions();
        var copy = _selectedSchedule.Model.Clone();
        copy.Id = Guid.NewGuid();
        copy.Name = _selectedSchedule.Name + " (Kopie)";

        _manager.Config.Schedules.Add(copy);
        var item = new ScheduleItemViewModel(copy);
        TrackSchedule(item);
        Schedules.Add(item);
        SelectedSchedule = item;
        RefreshChoices();
        RefreshDerivedData();
        MarkDirty();
    }

    private void RemoveSchedule()
    {
        if (_selectedSchedule is null)
        {
            return;
        }

        var id = _selectedSchedule.Id;
        var users = _manager.Config.Groups.Count(g => g.ScheduleId == id) +
                    _manager.Config.Pcs.Count(p => p.ScheduleId == id);

        var question = users == 0
            ? $"Zeitplan „{_selectedSchedule.Name}“ entfernen?"
            : $"Zeitplan „{_selectedSchedule.Name}“ entfernen?\n\n" +
              $"Er wird von {users} Gruppe(n)/PC(s) verwendet. Diese laufen anschließend ohne Zeitplan.";

        if (!Confirm("Zeitplan entfernen", question))
        {
            return;
        }

        foreach (var group in _manager.Config.Groups.Where(g => g.ScheduleId == id))
        {
            group.ScheduleId = null;
        }

        foreach (var pc in _manager.Config.Pcs.Where(p => p.ScheduleId == id))
        {
            pc.ScheduleId = null;
        }

        _manager.Config.Schedules.Remove(_selectedSchedule.Model);
        Schedules.Remove(_selectedSchedule);
        SelectedSchedule = null;
        RefreshChoices();
        RefreshDerivedData();
        MarkDirty();
    }

    private void AddException()
    {
        if (_selectedSchedule is null)
        {
            return;
        }

        var exception = new ScheduleException
        {
            Date = DateOnly.FromDateTime(DateTime.Today),
            Closed = true,
            Note = "Feiertag"
        };

        var item = new ScheduleExceptionViewModel(exception);
        _selectedSchedule.Exceptions.Add(item);
        _selectedSchedule.SyncExceptions();
        SelectedException = item;
        MarkDirty();
    }

    private void RemoveException()
    {
        if (_selectedSchedule is null || _selectedException is null)
        {
            return;
        }

        _selectedSchedule.Exceptions.Remove(_selectedException);
        _selectedSchedule.SyncExceptions();
        SelectedException = null;
        MarkDirty();
    }

    // ------------------------------------------------------------ Protokoll

    private void OnLogEntryAdded(object? sender, LogEntry entry)
    {
        void Append()
        {
            LogEntries.Add(entry);
            while (LogEntries.Count > Settings.LogCapacity)
            {
                LogEntries.RemoveAt(0);
            }
        }

        var dispatcher = System.Windows.Application.Current?.Dispatcher;
        if (dispatcher is null || dispatcher.CheckAccess())
        {
            Append();
        }
        else
        {
            dispatcher.BeginInvoke(Append);
        }
    }

    private void ExportLog()
    {
        try
        {
            var path = Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments),
                $"kiosksender-protokoll-{DateTime.Now:yyyyMMdd-HHmmss}.csv");

            File.WriteAllText(path, _log.ToCsv(), System.Text.Encoding.UTF8);
            StatusMessage = "Protokoll gespeichert: " + path;
            _log.Info("Protokoll", "Export nach " + path);
        }
        catch (Exception ex)
        {
            ShowError("Export fehlgeschlagen", ex.Message);
        }
    }

    // ------------------------------------------------------------ Filter

    private bool FilterPc(object item)
    {
        if (item is not PcItemViewModel pc)
        {
            return false;
        }

        if (string.IsNullOrWhiteSpace(_pcFilter))
        {
            return true;
        }

        var needle = _pcFilter.Trim();
        return pc.DisplayName.Contains(needle, StringComparison.CurrentCultureIgnoreCase)
               || pc.Host.Contains(needle, StringComparison.CurrentCultureIgnoreCase)
               || pc.GroupName.Contains(needle, StringComparison.CurrentCultureIgnoreCase)
               || pc.Note.Contains(needle, StringComparison.CurrentCultureIgnoreCase);
    }

    // ------------------------------------------------------------ Abschluss

    /// <summary>Beim Schließen: Timer anhalten und ungespeicherte Änderungen sichern.</summary>
    public async Task ShutdownAsync()
    {
        _schedulerTimer.Stop();
        _statusTimer.Stop();
        _uiTimer.Stop();
        _saveTimer.Stop();

        try
        {
            if (IsDirty)
            {
                await SaveAsync().ConfigureAwait(true);
            }
        }
        catch (Exception ex)
        {
            ShowError("Speichern fehlgeschlagen", ex.Message);
        }

        _shutdown.Cancel();
    }

    public void Dispose()
    {
        _log.EntryAdded -= OnLogEntryAdded;
        _shutdown.Dispose();
    }
}

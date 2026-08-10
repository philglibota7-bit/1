using System;
using KioskSender.App.Infrastructure;
using KioskSender.Core.Model;
using KioskSender.Core.Remote;
using KioskSender.Core.Scheduling;
using KioskSender.Core.Status;

namespace KioskSender.App.ViewModels;

/// <summary>Ein PC in der Liste — Stammdaten, Erreichbarkeit und Zeitplan-Zustand.</summary>
public sealed class PcItemViewModel : ObservableObject
{
    private HostStatus _status;
    private ScheduleState _scheduleState = ScheduleState.Closed;
    private string _groupName = "—";
    private string _scheduleName = "—";
    private string _groupColor = "#6A7285";
    private string _effectiveContent = string.Empty;
    private bool _isChosen;

    public PcItemViewModel(KioskPc model)
    {
        Model = model;
        _status = HostStatus.Unknown(model.Host);
    }

    public KioskPc Model { get; }

    public Guid Id => Model.Id;

    public string Name
    {
        get => Model.Name;
        set
        {
            if (Model.Name != value)
            {
                Model.Name = value;
                OnPropertyChanged(nameof(Name), nameof(DisplayName));
            }
        }
    }

    public string Host
    {
        get => Model.Host;
        set
        {
            if (Model.Host != value)
            {
                Model.Host = value;
                OnPropertyChanged(nameof(Host), nameof(DisplayName), nameof(HostIsValid), nameof(HostHint));
            }
        }
    }

    public bool Enabled
    {
        get => Model.Enabled;
        set
        {
            if (Model.Enabled != value)
            {
                Model.Enabled = value;
                OnPropertyChanged(nameof(Enabled), nameof(StatusText), nameof(State));
            }
        }
    }

    public string Note
    {
        get => Model.Note;
        set
        {
            if (Model.Note != value)
            {
                Model.Note = value;
                OnPropertyChanged();
            }
        }
    }

    public string DisplayName => Model.DisplayName;

    /// <summary>
    /// Häkchen in der Empfängerliste beim Senden von Inhalten.
    /// Gehört bewusst nicht zur gespeicherten Konfiguration — es ist eine
    /// Auswahl für den Moment, kein Merkmal des PCs.
    /// </summary>
    public bool IsChosen
    {
        get => _isChosen;
        set
        {
            if (_isChosen != value)
            {
                _isChosen = value;
                OnPropertyChanged();
                ChosenChanged?.Invoke(this, EventArgs.Empty);
            }
        }
    }

    public event EventHandler? ChosenChanged;

    public bool HostIsValid => CommandBuilder.IsValidHost(Model.Host);

    public string HostHint => HostIsValid
        ? string.Empty
        : "Kein gültiger Hostname / keine gültige IP-Adresse — dieser PC wird übersprungen.";

    public string GroupName
    {
        get => _groupName;
        set => SetProperty(ref _groupName, value);
    }

    public string GroupColor
    {
        get => _groupColor;
        set => SetProperty(ref _groupColor, value);
    }

    public string ScheduleName
    {
        get => _scheduleName;
        set => SetProperty(ref _scheduleName, value);
    }

    /// <summary>Zugeordneter Inhalt dieses PCs (leer = den der Gruppe verwenden).</summary>
    public string ContentFolder
    {
        get => Model.ContentFolder;
        set
        {
            var text = value ?? string.Empty;
            if (Model.ContentFolder != text)
            {
                Model.ContentFolder = text;
                OnPropertyChanged(nameof(ContentFolder));
            }
        }
    }

    /// <summary>Der wirklich gültige Inhalt — eigener oder der der Gruppe.</summary>
    public string EffectiveContent
    {
        get => _effectiveContent;
        set
        {
            if (SetProperty(ref _effectiveContent, value))
            {
                OnPropertyChanged(nameof(ContentText));
            }
        }
    }

    public string ContentText
    {
        get
        {
            if (string.IsNullOrWhiteSpace(_effectiveContent))
            {
                return "kein Inhalt zugeordnet";
            }

            var own = !string.IsNullOrWhiteSpace(Model.ContentFolder);
            return own ? _effectiveContent : _effectiveContent + " (von der Gruppe)";
        }
    }

    /// <summary>Wann dieser PC zuletzt Inhalte bekommen hat.</summary>
    public string LastSentText
    {
        get
        {
            if (Model.LastContentSentAt is not { } sent)
            {
                return "noch nie gesendet";
            }

            var name = string.IsNullOrWhiteSpace(Model.LastContentName)
                ? string.Empty
                : Model.LastContentName + " · ";

            return sent.Date == DateTime.Today
                ? $"{name}heute {sent:HH:mm}"
                : $"{name}{sent:dd.MM.yy HH:mm}";
        }
    }

    /// <summary>
    /// True, wenn der zugeordnete Inhalt nicht dem zuletzt gesendeten entspricht —
    /// dieser PC hängt also hinterher.
    /// </summary>
    public bool ContentIsStale =>
        !string.IsNullOrWhiteSpace(_effectiveContent) &&
        !string.Equals(_effectiveContent, Model.LastContentName, StringComparison.OrdinalIgnoreCase);

    public HostStatus Status
    {
        get => _status;
        set
        {
            _status = value;
            OnPropertyChanged(nameof(Status), nameof(State), nameof(StatusText));
        }
    }

    public HostState State => Model.Enabled ? _status.State : HostState.Disabled;

    public string StatusText => Model.Enabled ? _status.ToDisplayText() : "Deaktiviert";

    public ScheduleState ScheduleState
    {
        get => _scheduleState;
        set
        {
            _scheduleState = value;
            OnPropertyChanged(nameof(ScheduleState), nameof(ScheduleText));
        }
    }

    /// <summary>Klartext für die Spalte "Zeitfenster".</summary>
    public string ScheduleText
    {
        get
        {
            if (ScheduleName == "—")
            {
                return "Kein Zeitplan";
            }

            var now = DateTime.Now;
            if (_scheduleState.IsOpen && _scheduleState.Current is not null)
            {
                var minutes = _scheduleState.MinutesUntilClose(now) ?? 0;
                return minutes < 60
                    ? $"Offen — noch {Math.Max(0, (int)minutes)} Min."
                    : $"Offen bis {_scheduleState.Current.End:HH:mm}";
            }

            if (_scheduleState.Next is not null)
            {
                var start = _scheduleState.Next.Start;
                return start.Date == now.Date
                    ? $"Geschlossen — öffnet {start:HH:mm}"
                    : $"Geschlossen — öffnet {start:ddd HH:mm}";
            }

            return "Geschlossen";
        }
    }

    /// <summary>Nach einer Änderung von außen die Anzeige auffrischen.</summary>
    public void Refresh() => OnPropertyChanged(
        nameof(Name), nameof(Host), nameof(DisplayName), nameof(Enabled),
        nameof(Note), nameof(StatusText), nameof(State), nameof(ScheduleText),
        nameof(HostIsValid), nameof(HostHint), nameof(ContentFolder),
        nameof(ContentText), nameof(LastSentText), nameof(ContentIsStale));
}

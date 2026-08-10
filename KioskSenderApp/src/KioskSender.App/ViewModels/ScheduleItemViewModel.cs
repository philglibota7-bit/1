using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Globalization;
using System.Linq;
using KioskSender.App.Infrastructure;
using KioskSender.Core.Model;

namespace KioskSender.App.ViewModels;

/// <summary>Ein Wochentag als bearbeitbare Textzeile ("08:00-12:00, 13:00-17:00").</summary>
public sealed class DayPlanViewModel : ObservableObject
{
    private readonly DayPlan _model;
    private string _rangesText;
    private string _error = string.Empty;

    public DayPlanViewModel(DayPlan model)
    {
        _model = model;
        _rangesText = RangeListParser.Format(model.Ranges);
    }

    public DayOfWeek Day => _model.Day;

    public string DayName => CultureInfo.CurrentCulture.DateTimeFormat.GetDayName(_model.Day);

    public string ShortDayName => CultureInfo.CurrentCulture.DateTimeFormat.GetAbbreviatedDayName(_model.Day);

    /// <summary>
    /// Der Text wird bei jeder Änderung geprüft. Nur gültige Eingaben landen im
    /// Modell — so kann der Zeitplan nie in einem kaputten Zustand gespeichert werden.
    /// </summary>
    public string RangesText
    {
        get => _rangesText;
        set
        {
            if (_rangesText == value)
            {
                return;
            }

            _rangesText = value;
            OnPropertyChanged();

            if (RangeListParser.TryParse(value, out var ranges, out var error))
            {
                _model.Ranges = ranges;
                Error = string.Empty;
                Changed?.Invoke(this, EventArgs.Empty);
            }
            else
            {
                Error = error;
            }

            OnPropertyChanged(nameof(DurationText), nameof(IsClosed));
        }
    }

    public string Error
    {
        get => _error;
        private set
        {
            if (SetProperty(ref _error, value))
            {
                OnPropertyChanged(nameof(HasError));
            }
        }
    }

    public bool HasError => !string.IsNullOrEmpty(_error);

    public bool IsClosed => _model.Ranges.Count == 0;

    public string DurationText
    {
        get
        {
            if (_model.Ranges.Count == 0)
            {
                return "geschlossen";
            }

            var total = RangeListParser.TotalDuration(_model.Ranges);
            return total.Minutes == 0
                ? $"{(int)total.TotalHours} h"
                : $"{(int)total.TotalHours} h {total.Minutes} min";
        }
    }

    /// <summary>Wird ausgelöst, wenn eine gültige Änderung ins Modell übernommen wurde.</summary>
    public event EventHandler? Changed;

    public void SetRanges(IEnumerable<TimeRange> ranges)
    {
        _model.Ranges = ranges.Select(r => r.Clone()).ToList();
        _rangesText = RangeListParser.Format(_model.Ranges);
        Error = string.Empty;
        OnPropertyChanged(nameof(RangesText), nameof(DurationText), nameof(IsClosed));
    }
}

/// <summary>Ein Zeitplan im Zeitmanager.</summary>
public sealed class ScheduleItemViewModel : ObservableObject
{
    public ScheduleItemViewModel(WeeklySchedule model)
    {
        Model = model;
        Days = new ObservableCollection<DayPlanViewModel>(
            WeeklySchedule.WeekDaysInOrder.Select(d => new DayPlanViewModel(model.GetDay(d))));

        foreach (var day in Days)
        {
            day.Changed += (_, _) => OnPropertyChanged(nameof(WeekSummary));
        }

        Exceptions = new ObservableCollection<ScheduleExceptionViewModel>(
            model.Exceptions
                .OrderBy(e => e.Date)
                .Select(e => new ScheduleExceptionViewModel(e)));
    }

    public WeeklySchedule Model { get; }

    public Guid Id => Model.Id;

    public ObservableCollection<DayPlanViewModel> Days { get; }

    public ObservableCollection<ScheduleExceptionViewModel> Exceptions { get; }

    public string Name
    {
        get => Model.Name;
        set
        {
            if (Model.Name != value)
            {
                Model.Name = value;
                OnPropertyChanged();
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
                OnPropertyChanged();
            }
        }
    }

    public string WarnText
    {
        get => Model.WarnText;
        set
        {
            if (Model.WarnText != value)
            {
                Model.WarnText = value;
                OnPropertyChanged();
            }
        }
    }

    public string OpenText
    {
        get => Model.OpenText;
        set
        {
            if (Model.OpenText != value)
            {
                Model.OpenText = value;
                OnPropertyChanged();
            }
        }
    }

    /// <summary>Vorwarnzeiten als Text, z. B. "15, 5".</summary>
    public string WarnMinutesText
    {
        get => string.Join(", ", Model.WarnMinutes);
        set
        {
            var minutes = (value ?? string.Empty)
                .Split(new[] { ',', ';', ' ' }, StringSplitOptions.RemoveEmptyEntries)
                .Select(part => int.TryParse(part.Trim(), out var m) ? m : -1)
                .Where(m => m > 0)
                .Distinct()
                .OrderByDescending(m => m)
                .ToList();

            Model.WarnMinutes = minutes;
            OnPropertyChanged();
        }
    }

    public KioskActionKind CloseAction
    {
        get => Model.CloseAction;
        set
        {
            if (Model.CloseAction != value)
            {
                Model.CloseAction = value;
                OnPropertyChanged();
            }
        }
    }

    public int CloseGraceMinutes
    {
        get => Model.CloseGraceMinutes;
        set
        {
            var clamped = Math.Clamp(value, 0, 240);
            if (Model.CloseGraceMinutes != clamped)
            {
                Model.CloseGraceMinutes = clamped;
                OnPropertyChanged();
            }
        }
    }

    public int CloseCountdownSeconds
    {
        get => Model.CloseCountdownSeconds;
        set
        {
            var clamped = Math.Clamp(value, 0, 3600);
            if (Model.CloseCountdownSeconds != clamped)
            {
                Model.CloseCountdownSeconds = clamped;
                OnPropertyChanged();
            }
        }
    }

    public string WeekSummary
    {
        get
        {
            var openDays = Days.Count(d => !d.IsClosed);
            var total = TimeSpan.FromMinutes(
                Model.Days.Sum(d => RangeListParser.TotalDuration(d.Ranges).TotalMinutes));

            return openDays == 0
                ? "Keine Öffnungszeiten hinterlegt"
                : $"{openDays} Tag(e) · {total.TotalHours:0.#} Stunden pro Woche";
        }
    }

    /// <summary>Übernimmt die Ausnahmen aus der Oberfläche zurück ins Modell.</summary>
    public void SyncExceptions()
    {
        Model.Exceptions = Exceptions
            .Select(e => e.Model)
            .Where(e => e.Closed || e.Ranges.Count > 0)
            .OrderBy(e => e.Date)
            .ToList();
    }

    public void RefreshAll()
    {
        OnPropertyChanged(nameof(Name), nameof(Enabled), nameof(WarnMinutesText),
            nameof(CloseAction), nameof(WeekSummary), nameof(WarnText), nameof(OpenText));

        foreach (var day in Days)
        {
            day.SetRanges(Model.GetDay(day.Day).Ranges);
        }
    }
}

/// <summary>Ein Ausnahmetag (Feiertag oder Sonderöffnungszeit).</summary>
public sealed class ScheduleExceptionViewModel : ObservableObject
{
    private string _rangesText;
    private string _error = string.Empty;

    public ScheduleExceptionViewModel(ScheduleException model)
    {
        Model = model;
        _rangesText = RangeListParser.Format(model.Ranges);
    }

    public ScheduleException Model { get; }

    public DateTime Date
    {
        get => Model.Date.ToDateTime(TimeOnly.MinValue);
        set
        {
            var date = DateOnly.FromDateTime(value);
            if (Model.Date != date)
            {
                Model.Date = date;
                OnPropertyChanged();
            }
        }
    }

    public bool Closed
    {
        get => Model.Closed;
        set
        {
            if (Model.Closed != value)
            {
                Model.Closed = value;
                OnPropertyChanged(nameof(Closed), nameof(Summary));
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

    public string RangesText
    {
        get => _rangesText;
        set
        {
            if (_rangesText == value)
            {
                return;
            }

            _rangesText = value;
            OnPropertyChanged();

            if (RangeListParser.TryParse(value, out var ranges, out var error))
            {
                Model.Ranges = ranges;
                Error = string.Empty;
            }
            else
            {
                Error = error;
            }

            OnPropertyChanged(nameof(Summary));
        }
    }

    public string Error
    {
        get => _error;
        private set
        {
            if (SetProperty(ref _error, value))
            {
                OnPropertyChanged(nameof(HasError));
            }
        }
    }

    public bool HasError => !string.IsNullOrEmpty(_error);

    public string Summary => Closed
        ? "ganztägig geschlossen"
        : (Model.Ranges.Count == 0 ? "keine Zeiten — wird ignoriert" : RangeListParser.Format(Model.Ranges));
}

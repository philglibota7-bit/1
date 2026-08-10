using System;
using KioskSender.App.Infrastructure;
using KioskSender.Core.Model;

namespace KioskSender.App.ViewModels;

/// <summary>Eine Gruppe im Gruppenmanager.</summary>
public sealed class GroupItemViewModel : ObservableObject
{
    private int _pcCount;
    private int _onlineCount;
    private string _scheduleName = "Kein Zeitplan";
    private string _windowText = string.Empty;

    public GroupItemViewModel(PcGroup model) => Model = model;

    public PcGroup Model { get; }

    public Guid Id => Model.Id;

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

    public string ColorHex
    {
        get => Model.ColorHex;
        set
        {
            if (Model.ColorHex != value)
            {
                Model.ColorHex = value;
                OnPropertyChanged();
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

    public int PcCount
    {
        get => _pcCount;
        set
        {
            if (SetProperty(ref _pcCount, value))
            {
                OnPropertyChanged(nameof(Summary));
            }
        }
    }

    public int OnlineCount
    {
        get => _onlineCount;
        set
        {
            if (SetProperty(ref _onlineCount, value))
            {
                OnPropertyChanged(nameof(Summary));
            }
        }
    }

    public string ScheduleName
    {
        get => _scheduleName;
        set
        {
            if (SetProperty(ref _scheduleName, value))
            {
                OnPropertyChanged(nameof(Summary));
            }
        }
    }

    /// <summary>Aktuelles Zeitfenster der Gruppe im Klartext.</summary>
    public string WindowText
    {
        get => _windowText;
        set => SetProperty(ref _windowText, value);
    }

    public string Summary => $"{OnlineCount}/{PcCount} online · {ScheduleName}";

    public void Refresh() => OnPropertyChanged(nameof(Name), nameof(ColorHex), nameof(Note), nameof(Summary));
}

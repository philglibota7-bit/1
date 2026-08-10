namespace KioskSender.Core.Content;

/// <summary>
/// Bestimmt, welches Element als nächstes an der Reihe ist — inklusive
/// Wiederholung und Mischen. Ohne Oberfläche und ohne Zufall von außen,
/// damit sich die Reihenfolge testen lässt.
/// </summary>
public sealed class PlaylistCursor
{
    private readonly Random _random;
    private List<int> _order = new();
    private int _position = -1;

    public PlaylistCursor(Playlist playlist, int? randomSeed = null)
    {
        Playlist = playlist;
        _random = randomSeed is null ? new Random() : new Random(randomSeed.Value);
        BuildOrder();
    }

    public Playlist Playlist { get; }

    /// <summary>Abspielbare Elemente in der Reihenfolge der Liste.</summary>
    public IReadOnlyList<MediaItem> Items { get; private set; } = Array.Empty<MediaItem>();

    public bool IsEmpty => Items.Count == 0;

    /// <summary>Wie oft die Liste vollständig durchgelaufen ist.</summary>
    public int CompletedRounds { get; private set; }

    /// <summary>Das gerade laufende Element, oder null vor dem ersten Aufruf.</summary>
    public MediaItem? Current =>
        _position >= 0 && _position < _order.Count ? Items[_order[_position]] : null;

    /// <summary>
    /// Nächstes Element. Gibt null zurück, wenn die Liste leer ist oder
    /// vollständig durchgelaufen ist und nicht wiederholt werden soll.
    /// </summary>
    public MediaItem? Next()
    {
        if (Items.Count == 0)
        {
            return null;
        }

        _position++;

        if (_position >= _order.Count)
        {
            CompletedRounds++;

            if (!Playlist.Loop)
            {
                _position = _order.Count;
                return null;
            }

            // Beim Mischen für jeden Durchlauf neu würfeln.
            if (Playlist.Shuffle)
            {
                Shuffle();
            }

            _position = 0;
        }

        return Items[_order[_position]];
    }

    public void Reset()
    {
        BuildOrder();
        _position = -1;
        CompletedRounds = 0;
    }

    /// <summary>Anzeigedauer eines Elements; 0 bedeutet "bis zum natürlichen Ende".</summary>
    public int SecondsFor(MediaItem item)
    {
        if (item.Seconds > 0)
        {
            return item.Seconds;
        }

        return item.Kind == MediaKind.Image
            ? Math.Max(1, Playlist.DefaultImageSeconds)
            : 0;
    }

    private void BuildOrder()
    {
        Items = Playlist.Items
            .Where(i => i.Kind != MediaKind.Unsupported && !string.IsNullOrWhiteSpace(i.FileName))
            .ToList();

        _order = Enumerable.Range(0, Items.Count).ToList();

        if (Playlist.Shuffle)
        {
            Shuffle();
        }
    }

    private void Shuffle()
    {
        for (var i = _order.Count - 1; i > 0; i--)
        {
            var j = _random.Next(i + 1);
            (_order[i], _order[j]) = (_order[j], _order[i]);
        }
    }
}

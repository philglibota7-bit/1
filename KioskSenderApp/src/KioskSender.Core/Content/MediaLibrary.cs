namespace KioskSender.Core.Content;

/// <summary>Ein Ordner der Medienbibliothek — entspricht einer Wiedergabeliste.</summary>
public sealed class LibraryFolder
{
    public string Name { get; set; } = string.Empty;

    public string FullPath { get; set; } = string.Empty;

    /// <summary>Abspielbare Dateien direkt in diesem Ordner, natürlich sortiert.</summary>
    public List<MediaItem> Items { get; set; } = new();

    /// <summary>Unterordner, ebenfalls sortiert.</summary>
    public List<LibraryFolder> Folders { get; set; } = new();

    /// <summary>Dateien, die übersprungen wurden — für einen Hinweis in der Oberfläche.</summary>
    public List<string> SkippedFiles { get; set; } = new();

    public long TotalBytes => Items.Sum(i => i.SizeBytes) + Folders.Sum(f => f.TotalBytes);

    public int TotalItemCount => Items.Count + Folders.Sum(f => f.TotalItemCount);

    /// <summary>Kurzbeschreibung für die Ordnerliste.</summary>
    public string Summary
    {
        get
        {
            if (Items.Count == 0 && Folders.Count == 0)
            {
                return "leer";
            }

            var parts = new List<string>();
            if (Items.Count > 0)
            {
                parts.Add($"{Items.Count} Datei(en)");
            }

            if (Folders.Count > 0)
            {
                parts.Add($"{Folders.Count} Unterordner");
            }

            parts.Add(MediaItem.FormatSize(TotalBytes));
            return string.Join(" · ", parts);
        }
    }

    public override string ToString() => $"{Name} ({Summary})";
}

/// <summary>Ergebnis eines Bibliothek-Einlesevorgangs.</summary>
public sealed record LibraryScanResult(LibraryFolder? Root, string? Error)
{
    public bool Success => Root is not null;
}

/// <summary>
/// Liest eine Ordnerstruktur ein und macht daraus Wiedergabelisten:
/// jeder Ordner ist eine Liste, seine Dateien sind die Elemente.
/// </summary>
public sealed class MediaLibrary
{
    /// <summary>Wie tief Unterordner verfolgt werden.</summary>
    public int MaxDepth { get; set; } = 4;

    /// <summary>Sicherheitsnetz gegen versehentlich riesige Ordner.</summary>
    public int MaxFiles { get; set; } = 5000;

    public int DefaultImageSeconds { get; set; } = 10;

    public LibraryScanResult Scan(string rootPath)
    {
        if (string.IsNullOrWhiteSpace(rootPath))
        {
            return new LibraryScanResult(null, "Es ist kein Medienordner eingestellt.");
        }

        DirectoryInfo root;
        try
        {
            root = new DirectoryInfo(rootPath);
            if (!root.Exists)
            {
                return new LibraryScanResult(null, $"Der Ordner „{rootPath}“ wurde nicht gefunden.");
            }
        }
        catch (Exception ex) when (ex is IOException or UnauthorizedAccessException or ArgumentException)
        {
            return new LibraryScanResult(null, $"Der Ordner „{rootPath}“ ist nicht lesbar: {ex.Message}");
        }

        var budget = MaxFiles;
        var folder = ScanFolder(root, 0, ref budget);

        return new LibraryScanResult(folder, budget <= 0
            ? $"Es wurden nur die ersten {MaxFiles} Dateien eingelesen — der Ordner ist sehr groß."
            : null);
    }

    private LibraryFolder ScanFolder(DirectoryInfo directory, int depth, ref int budget)
    {
        var folder = new LibraryFolder
        {
            Name = directory.Name,
            FullPath = directory.FullName
        };

        try
        {
            foreach (var file in directory.EnumerateFiles().OrderBy(f => f.Name, NaturalComparer.Instance))
            {
                if (budget <= 0)
                {
                    break;
                }

                if (file.Attributes.HasFlag(FileAttributes.Hidden) ||
                    file.Attributes.HasFlag(FileAttributes.System))
                {
                    continue;
                }

                var kind = MediaKinds.FromFileName(file.Name);
                if (kind == MediaKind.Unsupported)
                {
                    if (folder.SkippedFiles.Count < 20)
                    {
                        folder.SkippedFiles.Add(file.Name);
                    }

                    continue;
                }

                folder.Items.Add(new MediaItem
                {
                    FileName = file.Name,
                    SourcePath = file.FullName,
                    Kind = kind,
                    SizeBytes = file.Length,
                    Seconds = kind == MediaKind.Image ? DefaultImageSeconds : 0
                });

                budget--;
            }

            if (depth < MaxDepth)
            {
                foreach (var sub in directory.EnumerateDirectories().OrderBy(d => d.Name, NaturalComparer.Instance))
                {
                    if (budget <= 0)
                    {
                        break;
                    }

                    if (sub.Attributes.HasFlag(FileAttributes.Hidden) ||
                        sub.Attributes.HasFlag(FileAttributes.System))
                    {
                        continue;
                    }

                    folder.Folders.Add(ScanFolder(sub, depth + 1, ref budget));
                }
            }
        }
        catch (UnauthorizedAccessException)
        {
            // Gesperrte Unterordner werden übersprungen statt den Einlesevorgang abzubrechen.
        }
        catch (IOException)
        {
            // Ebenso bei Netzwerkproblemen mitten im Einlesen.
        }

        return folder;
    }

    /// <summary>Alle Ordner der Struktur flach, in Anzeigereihenfolge.</summary>
    public static IEnumerable<LibraryFolder> Flatten(LibraryFolder? root)
    {
        if (root is null)
        {
            yield break;
        }

        yield return root;

        foreach (var child in root.Folders.SelectMany(Flatten))
        {
            yield return child;
        }
    }
}

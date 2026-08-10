using KioskSender.Core.Model;
using KioskSender.Core.Remote;

namespace KioskSender.Core.Content;

/// <summary>Fortschrittsmeldung während des Verteilens.</summary>
public sealed record DeployProgress(
    string PcName,
    string FileName,
    int FileIndex,
    int FileCount,
    long BytesDone,
    long BytesTotal)
{
    public double Percent => BytesTotal <= 0 ? 0 : Math.Clamp(BytesDone * 100.0 / BytesTotal, 0, 100);

    public string Text => $"{PcName}: {FileName} ({FileIndex}/{FileCount})";
}

/// <summary>Ergebnis für genau einen Rechner.</summary>
public sealed record DeployResult(
    string PcName,
    string Host,
    bool Success,
    int Copied,
    int Skipped,
    int Removed,
    long BytesCopied,
    string Message)
{
    public string Summary => Success
        ? $"{Copied} übertragen, {Skipped} unverändert, {Removed} entfernt ({MediaItem.FormatSize(BytesCopied)})"
        : Message;
}

/// <summary>
/// Bringt eine Wiedergabeliste samt Dateien auf die Kiosk-PCs.
///
/// Ablauf je Rechner: Zielordner anlegen, geänderte Dateien übertragen,
/// nicht mehr benötigte entfernen, zuletzt playlist.json schreiben.
/// Die Reihenfolge ist Absicht — der Player wechselt erst, wenn die Liste da
/// ist, und findet dann alle Dateien bereits vor.
/// </summary>
public sealed class DeploymentService
{
    private readonly IFileTransfer _transfer;

    public DeploymentService(IFileTransfer transfer) => _transfer = transfer;

    /// <summary>
    /// Zielpfad je Rechner. {host} wird ersetzt.
    /// Vorgabe: die Verwaltungsfreigabe C$ des Zielrechners.
    /// </summary>
    public string TargetPathTemplate { get; set; } = @"\\{host}\C$\ProgramData\KioskPlayer";

    /// <summary>Dateien im Zielordner löschen, die nicht mehr zur Liste gehören.</summary>
    public bool RemoveObsoleteFiles { get; set; } = true;

    /// <summary>Wie viele Rechner gleichzeitig beliefert werden.</summary>
    public int MaxParallel { get; set; } = 4;

    /// <summary>Nur zeigen, was passieren würde.</summary>
    public bool DryRun { get; set; }

    public string ResolveTarget(string host) =>
        TargetPathTemplate
            .Replace("{host}", host, StringComparison.OrdinalIgnoreCase)
            .Replace("{pc}", host, StringComparison.OrdinalIgnoreCase);

    public async Task<IReadOnlyList<DeployResult>> DeployAsync(
        Playlist playlist,
        IEnumerable<KioskPc> targets,
        IProgress<DeployProgress>? progress = null,
        CancellationToken cancellationToken = default)
    {
        var pcs = targets
            .Where(p => !string.IsNullOrWhiteSpace(p.Host))
            .ToList();

        if (pcs.Count == 0)
        {
            return Array.Empty<DeployResult>();
        }

        var delivery = playlist.ForDelivery();
        var results = new List<DeployResult>(pcs.Count);
        using var gate = new SemaphoreSlim(Math.Max(1, MaxParallel));

        var tasks = pcs.Select(async pc =>
        {
            await gate.WaitAsync(cancellationToken).ConfigureAwait(false);
            try
            {
                var result = await DeployToOneAsync(delivery, playlist, pc, progress, cancellationToken)
                    .ConfigureAwait(false);

                lock (results)
                {
                    results.Add(result);
                }
            }
            finally
            {
                gate.Release();
            }
        });

        await Task.WhenAll(tasks).ConfigureAwait(false);

        return results
            .OrderBy(r => r.PcName, StringComparer.CurrentCultureIgnoreCase)
            .ToList();
    }

    private async Task<DeployResult> DeployToOneAsync(
        Playlist delivery,
        Playlist source,
        KioskPc pc,
        IProgress<DeployProgress>? progress,
        CancellationToken cancellationToken)
    {
        if (!CommandBuilder.IsValidHost(pc.Host))
        {
            return new DeployResult(pc.DisplayName, pc.Host, false, 0, 0, 0, 0,
                "Ungültiger Hostname oder ungültige IP-Adresse.");
        }

        var target = ResolveTarget(CommandBuilder.NormalizeHost(pc.Host));
        var items = delivery.Items;
        var bytesTotal = items.Sum(i => i.SizeBytes);

        if (DryRun)
        {
            return new DeployResult(pc.DisplayName, pc.Host, true, 0, items.Count, 0, 0,
                $"Testbetrieb: würde {items.Count} Datei(en) nach {target} übertragen.");
        }

        var copied = 0;
        var skipped = 0;
        var removed = 0;
        long bytesCopied = 0;
        long bytesDone = 0;

        try
        {
            await _transfer.EnsureDirectoryAsync(target, cancellationToken).ConfigureAwait(false);

            for (var index = 0; index < items.Count; index++)
            {
                cancellationToken.ThrowIfCancellationRequested();

                var item = items[index];
                var sourceItem = source.Items.FirstOrDefault(i => i.FileName == item.FileName);
                var sourcePath = sourceItem?.SourcePath;

                if (string.IsNullOrWhiteSpace(sourcePath))
                {
                    continue;
                }

                var targetPath = Path.Combine(target, item.FileName);

                progress?.Report(new DeployProgress(
                    pc.DisplayName, item.FileName, index + 1, items.Count, bytesDone, bytesTotal));

                if (await _transfer.IsUpToDateAsync(sourcePath, targetPath, cancellationToken).ConfigureAwait(false))
                {
                    skipped++;
                }
                else
                {
                    await _transfer.CopyAsync(sourcePath, targetPath, cancellationToken).ConfigureAwait(false);
                    copied++;
                    bytesCopied += item.SizeBytes;
                }

                bytesDone += item.SizeBytes;
            }

            if (RemoveObsoleteFiles)
            {
                removed = await RemoveObsoleteAsync(target, items, cancellationToken).ConfigureAwait(false);
            }

            // Zuletzt die Liste — erst dadurch wechselt der Player auf die neuen Inhalte.
            await _transfer
                .WriteAllTextAsync(Path.Combine(target, Playlist.FileName), delivery.ToJson(), cancellationToken)
                .ConfigureAwait(false);

            progress?.Report(new DeployProgress(
                pc.DisplayName, Playlist.FileName, items.Count, items.Count, bytesTotal, bytesTotal));

            return new DeployResult(pc.DisplayName, pc.Host, true, copied, skipped, removed, bytesCopied,
                "Inhalte übertragen.");
        }
        catch (OperationCanceledException)
        {
            throw;
        }
        catch (Exception ex)
        {
            return new DeployResult(pc.DisplayName, pc.Host, false, copied, skipped, removed, bytesCopied,
                Explain(ex, target));
        }
    }

    private async Task<int> RemoveObsoleteAsync(
        string target,
        IReadOnlyList<MediaItem> items,
        CancellationToken cancellationToken)
    {
        var keep = items
            .Select(i => i.FileName)
            .Append(Playlist.FileName)
            .ToHashSet(StringComparer.OrdinalIgnoreCase);

        var existing = await _transfer.ListFilesAsync(target, cancellationToken).ConfigureAwait(false);
        var removed = 0;

        foreach (var file in existing)
        {
            cancellationToken.ThrowIfCancellationRequested();

            if (keep.Contains(file))
            {
                continue;
            }

            // Abgebrochene Übertragungen ebenfalls aufräumen.
            await _transfer.DeleteAsync(Path.Combine(target, file), cancellationToken).ConfigureAwait(false);
            removed++;
        }

        return removed;
    }

    /// <summary>Übersetzt die üblichen Netzwerkfehler in Klartext.</summary>
    public static string Explain(Exception ex, string target) => ex switch
    {
        UnauthorizedAccessException =>
            $"Kein Zugriff auf {target} — es werden Administratorrechte auf dem Zielrechner benötigt.",

        DirectoryNotFoundException =>
            $"{target} nicht gefunden — Rechner offline oder die Verwaltungsfreigabe C$ ist deaktiviert.",

        IOException io =>
            $"Übertragung nach {target} fehlgeschlagen: {io.Message}",

        _ => $"Übertragung nach {target} fehlgeschlagen: {ex.Message}"
    };
}

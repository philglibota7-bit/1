namespace KioskSender.Core.Content;

/// <summary>
/// Dateizugriff auf dem Zielrechner. Als Schnittstelle, damit das Verteilen
/// getestet werden kann, ohne echte Rechner zu beschreiben.
/// </summary>
public interface IFileTransfer
{
    Task EnsureDirectoryAsync(string directory, CancellationToken cancellationToken = default);

    /// <summary>Liegt die Datei dort bereits in derselben Größe und Zeit?</summary>
    Task<bool> IsUpToDateAsync(string sourceFile, string targetFile, CancellationToken cancellationToken = default);

    Task CopyAsync(string sourceFile, string targetFile, CancellationToken cancellationToken = default);

    Task WriteAllTextAsync(string targetFile, string content, CancellationToken cancellationToken = default);

    Task<IReadOnlyList<string>> ListFilesAsync(string directory, CancellationToken cancellationToken = default);

    Task DeleteAsync(string targetFile, CancellationToken cancellationToken = default);
}

/// <summary>
/// Zugriff über das Dateisystem — auch auf UNC-Pfade wie
/// \\PC-01\C$\ProgramData\KioskPlayer.
/// </summary>
public sealed class FileSystemTransfer : IFileTransfer
{
    public Task EnsureDirectoryAsync(string directory, CancellationToken cancellationToken = default)
    {
        Directory.CreateDirectory(directory);
        return Task.CompletedTask;
    }

    public Task<bool> IsUpToDateAsync(string sourceFile, string targetFile, CancellationToken cancellationToken = default)
    {
        var source = new FileInfo(sourceFile);
        var target = new FileInfo(targetFile);

        if (!target.Exists || !source.Exists)
        {
            return Task.FromResult(false);
        }

        // Gleiche Größe und Änderungszeit: dann muss nicht erneut übertragen
        // werden. Die Sekunde Toleranz gleicht unterschiedliche Dateisysteme aus.
        var sameSize = source.Length == target.Length;
        var sameTime = Math.Abs((source.LastWriteTimeUtc - target.LastWriteTimeUtc).TotalSeconds) < 2;

        return Task.FromResult(sameSize && sameTime);
    }

    public async Task CopyAsync(string sourceFile, string targetFile, CancellationToken cancellationToken = default)
    {
        var directory = Path.GetDirectoryName(targetFile);
        if (!string.IsNullOrEmpty(directory))
        {
            Directory.CreateDirectory(directory);
        }

        // Erst neben das Ziel schreiben, dann umbenennen: Bricht die Übertragung
        // ab, findet der Player keine halbe Datei vor.
        var tempFile = targetFile + ".part";

        await using (var source = new FileStream(sourceFile, FileMode.Open, FileAccess.Read, FileShare.Read, 81920, useAsync: true))
        await using (var target = new FileStream(tempFile, FileMode.Create, FileAccess.Write, FileShare.None, 81920, useAsync: true))
        {
            await source.CopyToAsync(target, 81920, cancellationToken).ConfigureAwait(false);
        }

        File.SetLastWriteTimeUtc(tempFile, File.GetLastWriteTimeUtc(sourceFile));

        if (File.Exists(targetFile))
        {
            File.Delete(targetFile);
        }

        File.Move(tempFile, targetFile);
    }

    public Task WriteAllTextAsync(string targetFile, string content, CancellationToken cancellationToken = default)
    {
        var directory = Path.GetDirectoryName(targetFile);
        if (!string.IsNullOrEmpty(directory))
        {
            Directory.CreateDirectory(directory);
        }

        return File.WriteAllTextAsync(targetFile, content, System.Text.Encoding.UTF8, cancellationToken);
    }

    public Task<IReadOnlyList<string>> ListFilesAsync(string directory, CancellationToken cancellationToken = default)
    {
        if (!Directory.Exists(directory))
        {
            return Task.FromResult<IReadOnlyList<string>>(Array.Empty<string>());
        }

        IReadOnlyList<string> files = Directory
            .EnumerateFiles(directory)
            .Select(Path.GetFileName)
            .Where(name => !string.IsNullOrEmpty(name))
            .Select(name => name!)
            .ToList();

        return Task.FromResult(files);
    }

    public Task DeleteAsync(string targetFile, CancellationToken cancellationToken = default)
    {
        if (File.Exists(targetFile))
        {
            File.Delete(targetFile);
        }

        return Task.CompletedTask;
    }
}

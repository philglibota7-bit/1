using System.Text.Json;
using System.Text.Json.Serialization;
using KioskSender.Core.Model;

namespace KioskSender.Core.Storage;

/// <summary>
/// Lädt und speichert die Konfiguration als JSON. Das Schreiben läuft über eine
/// temporäre Datei plus Ersetzen, damit ein Absturz mitten im Speichern die
/// bestehende Konfiguration nicht zerstört.
/// </summary>
public sealed class ConfigStore
{
    private static readonly JsonSerializerOptions Options = new()
    {
        WriteIndented = true,
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
        Converters = { new JsonStringEnumConverter() }
    };

    private readonly SemaphoreSlim _writeLock = new(1, 1);

    public ConfigStore(string? path = null)
    {
        FilePath = path ?? DefaultPath();
    }

    public string FilePath { get; }

    public string BackupPath => FilePath + ".bak";

    public static string DefaultDirectory() =>
        Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
            "KioskSenderApp");

    public static string DefaultPath() => Path.Combine(DefaultDirectory(), "config.json");

    /// <summary>
    /// Lädt die Konfiguration. Ist die Datei kaputt, wird sie beiseitegelegt und
    /// eine Startkonfiguration erzeugt — die Anwendung startet dann trotzdem.
    /// </summary>
    public async Task<(AppConfig Config, string? Warning)> LoadAsync(CancellationToken cancellationToken = default)
    {
        if (!File.Exists(FilePath))
        {
            return (AppConfig.CreateSample(), null);
        }

        try
        {
            await using var stream = File.OpenRead(FilePath);
            var config = await JsonSerializer
                .DeserializeAsync<AppConfig>(stream, Options, cancellationToken)
                .ConfigureAwait(false);

            if (config is null)
            {
                return (AppConfig.CreateSample(), "Konfiguration war leer — Startkonfiguration geladen.");
            }

            config.Normalize();
            return (config, null);
        }
        catch (Exception ex) when (ex is JsonException or IOException or UnauthorizedAccessException)
        {
            var warning = TryQuarantine(ex);
            return (AppConfig.CreateSample(), warning);
        }
    }

    public async Task SaveAsync(AppConfig config, CancellationToken cancellationToken = default)
    {
        config.Normalize();

        await _writeLock.WaitAsync(cancellationToken).ConfigureAwait(false);
        try
        {
            var directory = Path.GetDirectoryName(FilePath);
            if (!string.IsNullOrEmpty(directory))
            {
                Directory.CreateDirectory(directory);
            }

            var tempPath = FilePath + ".tmp";

            await using (var stream = File.Create(tempPath))
            {
                await JsonSerializer
                    .SerializeAsync(stream, config, Options, cancellationToken)
                    .ConfigureAwait(false);
            }

            if (File.Exists(FilePath))
            {
                File.Replace(tempPath, FilePath, BackupPath, ignoreMetadataErrors: true);
            }
            else
            {
                File.Move(tempPath, FilePath);
            }
        }
        finally
        {
            _writeLock.Release();
        }
    }

    /// <summary>Konfiguration exportieren (Sicherung / Übertragung auf einen anderen Arbeitsplatz).</summary>
    public async Task ExportAsync(AppConfig config, string targetPath, CancellationToken cancellationToken = default)
    {
        await using var stream = File.Create(targetPath);
        await JsonSerializer.SerializeAsync(stream, config, Options, cancellationToken).ConfigureAwait(false);
    }

    public static async Task<AppConfig?> ImportAsync(string sourcePath, CancellationToken cancellationToken = default)
    {
        await using var stream = File.OpenRead(sourcePath);
        var config = await JsonSerializer
            .DeserializeAsync<AppConfig>(stream, Options, cancellationToken)
            .ConfigureAwait(false);

        config?.Normalize();
        return config;
    }

    private string TryQuarantine(Exception ex)
    {
        try
        {
            var brokenPath = FilePath + ".broken-" + DateTime.Now.ToString("yyyyMMdd-HHmmss");
            File.Move(FilePath, brokenPath, overwrite: true);
            return $"Konfiguration konnte nicht gelesen werden ({ex.Message}). " +
                   $"Die Datei wurde nach '{Path.GetFileName(brokenPath)}' verschoben, " +
                   "es wurde eine Startkonfiguration angelegt.";
        }
        catch
        {
            return $"Konfiguration konnte nicht gelesen werden ({ex.Message}). " +
                   "Es wurde eine Startkonfiguration im Speicher angelegt — bitte vor dem Speichern prüfen.";
        }
    }
}

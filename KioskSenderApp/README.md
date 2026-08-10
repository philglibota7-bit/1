# KioskSenderApp

Windows-Werkzeug zur Verwaltung von Kiosk-PCs: **Gruppenmanager**, **Zeitmanager**
und **Sender** in einer Anwendung.

Die Fernsteuerung läuft ausschließlich über Windows-Bordmittel
(`msg.exe`, `shutdown.exe`, `quser.exe`, `logoff.exe`, ICMP-Ping) — auf den
Kiosk-PCs muss **nichts installiert** werden.

---

## Was die Anwendung kann

### Gruppenmanager
- PCs anlegen (Anzeigename, Hostname oder IP, Notiz) und aktiv/inaktiv schalten
- Gruppen mit eigener Farbe anlegen und PCs zuordnen — auch mehrere auf einmal
  über die Mehrfachauswahl in der Tabelle
- Je Gruppe: Anzahl der Mitglieder, wie viele davon online sind, welcher
  Zeitplan gilt und ob gerade geöffnet ist
- Ein PC kann einen **eigenen Zeitplan** bekommen, der den Gruppenplan übersteuert

### Zeitmanager
- Wochenraster je Zeitplan: pro Wochentag beliebig viele Zeitspannen
  (`08:00-12:00, 13:00-17:00`), leer bedeutet geschlossen
- Zeitfenster **über Mitternacht** werden unterstützt (`20:00-02:00`)
- **Ausnahmetage** für Feiertage (ganztägig geschlossen) oder Sonderzeiten
  (ersetzen den Wochentag für dieses eine Datum)
- **Vorwarnungen** vor der Schließung (z. B. 15 und 5 Minuten vorher) als
  Bildschirmmeldung; `{minutes}` im Text wird durch die Restzeit ersetzt
- Frei wählbare **Schließ-Aktion**: Herunterfahren, Neustart, Abmelden,
  nur Meldung, eigener Befehl oder nichts
- **Karenzzeit** nach Fensterende und **Countdown**, den Windows dem Benutzer
  vor dem Herunterfahren noch lässt
- Nach längerem Stillstand (Standby, Anwendung war zu) werden **keine alten
  Aktionen nachgeholt** — nur was in den letzten 10 Minuten fällig war

### Sender
- Ziel wählen: markierte PCs, die gewählte Gruppe oder alle aktiven PCs
- Nachricht senden, Benutzer abmelden, Neustart, Herunterfahren, laufenden
  Countdown abbrechen, eigener Befehl
- Eingriffe (Herunterfahren, Neustart, Abmelden) fragen vorher nach und nennen
  die betroffenen Rechner beim Namen

### Betrieb
- **Testbetrieb**: Es wird nur protokolliert, was passieren würde — nichts wird
  ausgeführt. Ideal, um einen neuen Zeitplan gefahrlos zu prüfen.
- **Erreichbarkeitsprüfung** aller PCs im Hintergrund (paralleler Ping)
- **Protokoll** in der Oberfläche, zusätzlich tageweise als Datei, Export als CSV
- Konfiguration wird automatisch gespeichert (und beim Beenden), Schreiben
  erfolgt über eine temporäre Datei — ein Absturz beim Speichern kann die
  bestehende Konfiguration nicht zerstören
- Nur **eine Instanz** gleichzeitig, damit sich nicht zwei Zeitmanager
  gegenseitig in die Quere kommen

---

## Fertige EXE bekommen

**Ohne selbst zu bauen:** Bei jedem Push baut GitHub Actions die EXE.
→ Reiter **Actions** → Lauf *KioskSenderApp* öffnen → unten unter *Artifacts*:

| Artefakt | Größe | Voraussetzung |
|---|---|---|
| `KioskSenderApp-win-x64-eigenstaendig` | ca. 65 MB | keine — läuft direkt |
| `KioskSenderApp-win-x64-klein` | ca. 350 KB | [.NET 8 Desktop Runtime](https://dotnet.microsoft.com/download/dotnet/8.0) |

## Selbst bauen

Voraussetzung: [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0)

```powershell
# Tests
dotnet test KioskSenderApp/KioskSenderApp.sln

# EXE, läuft ohne .NET-Installation
dotnet publish KioskSenderApp/src/KioskSender.App/KioskSender.App.csproj `
  -c Release -r win-x64 --self-contained true `
  -p:PublishSingleFile=true -p:IncludeNativeLibrariesForSelfExtract=true `
  -o publish

# EXE, klein — benötigt die .NET 8 Desktop Runtime
dotnet publish KioskSenderApp/src/KioskSender.App/KioskSender.App.csproj `
  -c Release -r win-x64 --self-contained false `
  -p:PublishSingleFile=true -o publish-klein
```

Ergebnis: `publish\KioskSenderApp.exe`

---

## Voraussetzungen auf den Kiosk-PCs

Es wird nichts installiert, aber Windows muss die Fernbefehle zulassen:

1. Alle Rechner in derselben **Domäne oder Arbeitsgruppe**
2. Der Benutzer, unter dem KioskSenderApp läuft, ist auf den Zielrechnern
   **Administrator**
   (sonst: `Zugriff verweigert (5)` — dann die Anwendung mit
   Umschalt + Rechtsklick → *Als anderer Benutzer ausführen* starten)
3. In der Windows-Firewall der Zielrechner freigeben:
   - **Datei- und Druckerfreigabe** (für `shutdown /m`)
   - **Windows-Verwaltungsinstrumentation (WMI)**
4. Für Bildschirmmeldungen muss auf den Zielrechnern der Dienst
   **Remotedesktopdienste** laufen (`msg.exe` nutzt ihn)
5. Für Ping: **ICMP (Echoanforderung)** eingehend erlauben

### Bildschirm sperren
Windows kann einen fremden Rechner nicht ohne Hilfsmittel sperren. Dafür gibt es
die Aktion **Eigener Befehl** — unter *Einstellungen* z. B. hinterlegen:

```
C:\Tools\PsExec.exe \\{host} -s -d rundll32.exe user32.dll,LockWorkStation
```

`{host}` wird durch den jeweiligen Zielrechner ersetzt.

---

## Wo liegen die Daten

```
%AppData%\KioskSenderApp\config.json          Konfiguration
%AppData%\KioskSenderApp\config.json.bak      letzte Fassung
%AppData%\KioskSenderApp\logs\                Protokolle, tageweise
```

Lässt sich die Konfiguration nicht lesen, wird sie als `config.json.broken-<Zeit>`
beiseitegelegt und die Anwendung startet mit einer Startkonfiguration — sie
verweigert nie den Dienst wegen einer kaputten Datei.

---

## Aufbau des Quelltextes

```
KioskSenderApp/
├─ src/
│  ├─ KioskSender.Core/          Logik ohne Oberfläche (net8.0, plattformneutral)
│  │  ├─ Model/                  Datenmodell, Zeitspannen-Parser
│  │  ├─ Scheduling/             Zeitplan-Auswertung und Ereignis-Erzeugung
│  │  ├─ Remote/                 Befehlsaufbau, Prozessausführung, quser-Auswertung
│  │  ├─ Status/                 Erreichbarkeitsprüfung
│  │  ├─ Storage/                Laden/Speichern der Konfiguration
│  │  ├─ Logging/                Protokoll
│  │  └─ Services/               KioskManager — klammert alles zusammen
│  └─ KioskSender.App/           WPF-Oberfläche (net8.0-windows)
│     ├─ ViewModels/             MVVM ohne Fremdpakete
│     ├─ Views/                  Hauptfenster
│     ├─ Theme/                  dunkles Design
│     └─ Infrastructure/         Basisklassen, Befehle, Konverter
└─ tests/
   └─ KioskSender.Core.Tests/    118 Tests (xUnit)
```

Die gesamte Logik steckt bewusst in `KioskSender.Core` und kennt weder WPF noch
die Systemuhr: Zeitpunkte werden hineingereicht, Prozessaufrufe laufen über eine
Schnittstelle. Deshalb ist der Zeitmanager vollständig testbar, ohne zu warten
und ohne echte Rechner herunterzufahren.

Es werden **keine Fremdpakete** verwendet (außer xUnit in den Tests).

---

## Bedienung in Kurzform

1. **Gruppen & PCs** → *Neue Gruppe* anlegen, benennen, Farbe wählen
2. *PC hinzufügen* → Anzeigename und Hostname/IP eintragen
3. Mehrere PCs in der Tabelle markieren → *Auswahl dieser Gruppe zuordnen*
4. **Zeitmanager** → *Neuer Zeitplan*, Wochenzeiten eintragen, Schließ-Aktion
   und Vorwarnungen festlegen, Feiertage als Ausnahmetage ergänzen
5. Zurück zu **Gruppen & PCs** → der Gruppe den Zeitplan zuweisen
6. Oben **Testbetrieb** einschalten und im **Protokoll** prüfen, was der
   Zeitmanager tun würde — erst danach scharf schalten

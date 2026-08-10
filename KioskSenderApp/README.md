# KioskSenderApp

Windows-Werkzeug zur Verwaltung von Kiosk-PCs: **Gruppenmanager**, **Zeitmanager**,
**Inhalte senden** und **Sender** in einer Anwendung.

Es gehören zwei Programme dazu:

| Programm | Läuft wo | Wofür |
|---|---|---|
| **KioskSenderApp.exe** | am Arbeitsplatz | verwalten, planen, Inhalte verteilen |
| **KioskPlayer.exe** | auf jedem Kiosk-PC | zeigt die gesendeten Inhalte im Vollbild |

Fernsteuerung (Meldung, Neustart, Herunterfahren, Abmelden) läuft über
Windows-Bordmittel und braucht **nichts** auf den Kiosk-PCs. Zum **Abspielen**
von Bildern, Videos und Präsentationen wird der Player benötigt — Windows kann
Medien nicht von sich aus auf einem fremden Rechner starten.

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

### Inhalte senden
- Ein **Medienordner** wird eingelesen; jeder Unterordner darin ist eine
  eigene Wiedergabeliste — die Struktur im Explorer ist die Struktur im Programm
- Unterstützt **Bilder** (jpg, png, bmp, gif, webp, tif),
  **Videos** (mp4, wmv, avi, mov, mkv, mpg) und
  **PowerPoint** (ppt, pptx, pps, ppsx)
- Dateien laufen in natürlicher Reihenfolge: `Bild1`, `Bild2`, `Bild10` —
  nicht `Bild1`, `Bild10`, `Bild2`
- Anzeigedauer für Bilder einstellbar, Videos laufen bis zum Ende,
  PowerPoint startet als Bildschirmpräsentation
- Endlos wiederholen und Reihenfolge mischen jeweils an- und abschaltbar
- Empfänger einfach anhaken — einzeln, alle oder eine ganze Gruppe
- **Feste Zuordnung je PC oder Gruppe**: „dieser PC zeigt diesen Ordner“.
  Danach genügt *Alle Zuordnungen senden* — jeder Rechner bekommt seinen
  eigenen Inhalt, ohne dass vorher etwas angehakt werden muss
- Die Übersicht zeigt je PC, was er zeigen soll und wann er zuletzt
  beliefert wurde
- Übertragung mit Fortschrittsanzeige und Abbrechen-Schaltfläche
- Es werden nur **geänderte** Dateien übertragen; nicht mehr benötigte werden
  auf dem Kiosk-PC entfernt
- Die Wiedergabeliste wird **zuletzt** geschrieben — der Player wechselt erst,
  wenn wirklich alle Dateien angekommen sind

### Sender
- Ein Konzept für alles: **angehakte PCs sind das Ziel**. Ist nichts angehakt,
  gilt die markierte Zeile — keine getrennte Ziel-Auswahl mehr
- Nachricht senden, Benutzer abmelden, Neustart, Herunterfahren, laufenden
  Countdown abbrechen, eigener Befehl
- Eingriffe (Herunterfahren, Neustart, Abmelden) fragen vorher nach und nennen
  die betroffenen Rechner beim Namen
- Nach jeder Aktion steht **je Rechner eine Zeile** mit grünem oder rotem Punkt
  da — man sieht sofort, wer erreicht wurde und woran es sonst lag

### Oberfläche
- **Klinik-Design**: helle, ruhige Flächen, klinisches Blau als einzige
  Akzentfarbe, kräftige Signalfarben nur für Zustände. Helle Oberflächen sind
  in hell beleuchteten Räumen besser lesbar als dunkle.
- **Kennzahlen am Kopf der Übersicht**: erreichbare PCs, Inhalte auf aktuellem
  Stand, offene Zeitfenster, Fehler des Tages — der Zustand der Anlage in einer
  Sekunde erfassbar
- Seitenleiste links mit festen Plätzen für jeden Arbeitsschritt
- Legende unter der Tabelle: kein Ratespiel, wofür die farbigen Punkte stehen
- Große Schaltflächen und Schrift, hoher Kontrast

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
- **Keine Fehlerdialoge**: Probleme erscheinen als Hinweisbalken im Fenster
  und im Protokoll. Nichts blockiert die Arbeit, nichts muss weggeklickt
  werden, der Zeitmanager läuft weiter. Rückfragen gibt es nur dort, wo
  wirklich etwas Folgenschweres passiert (Herunterfahren, Inhalte ersetzen).

---

## Fertige EXE bekommen

**Ohne selbst zu bauen:** Bei jedem Push baut GitHub Actions die EXE.
→ Reiter **Actions** → Lauf *KioskSenderApp* öffnen → unten unter *Artifacts*:

| Artefakt | Größe | Voraussetzung |
|---|---|---|
| `KioskSenderApp-win-x64-eigenstaendig` | ca. 65 MB | keine — läuft direkt |
| `KioskSenderApp-win-x64-klein` | ca. 400 KB | [.NET 8 Desktop Runtime](https://dotnet.microsoft.com/download/dotnet/8.0) |
| `KioskPlayer-win-x64` | ca. 65 MB | keine — für die Kiosk-PCs |

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

# Player für die Kiosk-PCs
dotnet publish KioskSenderApp/src/KioskSender.Player/KioskSender.Player.csproj `
  -c Release -r win-x64 --self-contained true `
  -p:PublishSingleFile=true -p:IncludeNativeLibrariesForSelfExtract=true `
  -o publish-player
```

Ergebnis: `publish\KioskSenderApp.exe` und `publish-player\KioskPlayer.exe`

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

### KioskPlayer auf einem Kiosk-PC einrichten

1. `KioskPlayer.exe` auf den Kiosk-PC kopieren, z. B. nach `C:\KioskPlayer\`
2. Einmal starten — er legt `C:\ProgramData\KioskPlayer` an und zeigt
   „Warte auf Inhalte…“ samt Rechnername
3. Für den Dauerbetrieb in den Autostart legen: Verknüpfung nach
   `shell:startup` (Win + R) oder als geplante Aufgabe „Bei Anmeldung“
4. Im Manager unter **Inhalte senden** den Rechner anhaken und senden

Tasten am Kiosk-PC: **Esc** beendet, **Leertaste** springt weiter,
**F5** liest die Liste neu ein, **Strg + Alt + Q** ist der Notausstieg.

Bei Tastendruck oder Mausbewegung blendet der Player kurz ein, **welcher
Rechner** er ist und **welche Wiedergabeliste** gerade läuft — praktisch, um
beim Einrichten zu prüfen, ob der richtige PC den richtigen Inhalt hat.

Der Wartebildschirm ist im selben Klinik-Design gehalten und passt damit zur
Beschilderung im Haus. Medien selbst laufen auf schwarzem Grund, damit nichts
vom Bild ablenkt und Ränder nicht auffallen.

Startparameter:

```
KioskPlayer.exe                    Vollbild, Standardordner
KioskPlayer.exe D:\Inhalte         anderer Inhaltsordner
KioskPlayer.exe --fenster          im Fenster (zum Einrichten)
KioskPlayer.exe --kein-beenden     Esc gesperrt (echter Kiosk)
```

Für PowerPoint muss auf dem Kiosk-PC PowerPoint installiert sein. Ohne
PowerPoint einfach vorher als Video oder Bilderfolge exportieren — das ist
für den Dauerbetrieb ohnehin die robustere Variante.

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

Auf jedem Kiosk-PC:

```
C:\ProgramData\KioskPlayer\                   gesendete Dateien
C:\ProgramData\KioskPlayer\playlist.json      die Wiedergabeliste
C:\ProgramData\KioskPlayer\player.log         Fehler des Players
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
│  │  ├─ Content/                Medienbibliothek, Wiedergabeliste, Verteilen
│  │  ├─ Model/                  Datenmodell, Zeitspannen-Parser
│  │  ├─ Scheduling/             Zeitplan-Auswertung und Ereignis-Erzeugung
│  │  ├─ Remote/                 Befehlsaufbau, Prozessausführung, quser-Auswertung
│  │  ├─ Status/                 Erreichbarkeitsprüfung
│  │  ├─ Storage/                Laden/Speichern der Konfiguration
│  │  ├─ Logging/                Protokoll
│  │  └─ Services/               KioskManager — klammert alles zusammen
│  ├─ KioskSender.App/           WPF-Oberfläche des Managers (net8.0-windows)
│  │  ├─ ViewModels/             MVVM ohne Fremdpakete
│  │  ├─ Views/                  Hauptfenster
│  │  ├─ Theme/Clinic.xaml       Klinik-Design an einer Stelle
│  │  └─ Infrastructure/         Basisklassen, Befehle, Konverter
│  └─ KioskSender.Player/        Vollbild-Player für die Kiosk-PCs
└─ tests/
   └─ KioskSender.Core.Tests/    189 Tests (xUnit)
```

Die gesamte Logik steckt bewusst in `KioskSender.Core` und kennt weder WPF noch
die Systemuhr: Zeitpunkte werden hineingereicht, Prozessaufrufe laufen über eine
Schnittstelle. Deshalb ist der Zeitmanager vollständig testbar, ohne zu warten
und ohne echte Rechner herunterzufahren.

Es werden **keine Fremdpakete** verwendet (außer xUnit in den Tests).

---

## Bedienung in Kurzform

Die Seitenleiste links führt durch die Arbeitsschritte.

**PCs einrichten**
1. **Gruppen & PCs** → *Neue Gruppe* anlegen, benennen, Farbe wählen
2. *PC hinzufügen* → Anzeigename und Hostname/IP eintragen
3. Mehrere PCs in der Tabelle markieren → *Auswahl dieser Gruppe zuordnen*

**Inhalte senden**
4. **Inhalte senden** → ① *Ordner wählen* — den Ordner mit den Medien angeben
5. ② Ordner in der Liste anklicken, Inhalt und Reihenfolge prüfen,
   Anzeigedauer einstellen
6. ③ Empfänger anhaken → *Jetzt an die angehakten PCs senden*

**Oder dauerhaft zuordnen** (empfehlenswert, wenn die PCs verschiedene
Inhalte zeigen sollen): Ordner wählen, PCs anhaken, auf *Angehakten zuordnen*
klicken. Von da an genügt **Alle Zuordnungen senden** — jeder Rechner bekommt
seinen eigenen Inhalt, ganz ohne Anhaken.

**Zeitplan**
7. **Zeitmanager** → *Neuer Zeitplan*, Wochenzeiten eintragen, Schließ-Aktion
   und Vorwarnungen festlegen, Feiertage als Ausnahmetage ergänzen
8. Zurück zu **Gruppen & PCs** → der Gruppe den Zeitplan zuweisen
9. Oben **Testbetrieb** einschalten und im **Protokoll** prüfen, was der
   Zeitmanager tun würde — erst danach scharf schalten

# LDPlayer Game-Bot

Ein Python-Grundgeruest, das den **LDPlayer**-Emulator ueber **ADB** steuert:
Screenshot holen → Bild-Elemente per OpenCV erkennen → tippen / wischen /
Tasten senden. Spiel-unabhaengig, ueber `config.json` erweiterbar.

> ⚠️ **Hinweis:** Automatisierung/Bots verstossen bei vielen Spielen gegen die
> Nutzungsbedingungen und koennen zu einer Sperre fuehren. Nur fuer eigene
> Projekte, Lern-/Testzwecke oder ausdruecklich erlaubte Faelle verwenden.

## 1. Voraussetzungen

- **Windows** mit installiertem **LDPlayer**
- **Python 3.9+**
- **ADB** (Android Debug Bridge). LDPlayer bringt eine eigene `adb.exe` im
  Installationsordner mit (z. B. `C:\LDPlayer\LDPlayer9\adb.exe`).
  Entweder ADB in den PATH aufnehmen oder in `config.json` unter `adb_path`
  den vollen Pfad angeben.

## 2. LDPlayer vorbereiten

1. LDPlayer starten.
2. **Einstellungen → Andere Einstellungen → ADB-Debugging →
   „Lokale Verbindung aktivieren"** anhaken, dann LDPlayer neu starten.
3. Merke dir den ADB-Port. Bei einer Instanz ist das meist **5555**.
   Weitere Instanzen: 5557, 5559, … (immer +2).

## 3. Installation

```bash
cd gamebot
pip install -r requirements.txt
cp config.example.json config.json      # Windows: copy config.example.json config.json
```

## 4. Templates erstellen

Der Bot erkennt Elemente anhand kleiner Referenzbilder im Ordner `templates/`.

1. Mache einen Screenshot im Spiel (z. B. `adb exec-out screencap -p > shot.png`).
2. Schneide daraus den gewuenschten Button/Bereich aus (Windows „Ausschneiden
   & Skizzieren" o. Ae.) und speichere ihn z. B. als `templates/start_button.png`.
3. Trage in `config.json` eine Regel mit diesem Dateinamen ein.

Wichtig: Templates in **derselben Aufloesung** wie der LDPlayer aufnehmen,
sonst passt das Matching nicht.

## 5. Starten

```bash
python bot.py --dry-run    # nur erkennen, NICHTS antippen -> zum Testen
python bot.py              # echter Betrieb
```

Beenden mit **Strg+C**.

## 6. Regeln (config.json)

Jede Regel:

| Feld        | Bedeutung                                                        |
|-------------|------------------------------------------------------------------|
| `name`      | Nur zur Anzeige im Log                                            |
| `template`  | Dateiname in `templates/`                                        |
| `action`    | `tap`, `swipe`, `key` oder `wait`                               |
| `threshold` | Ab welcher Trefferguete (0..1) die Regel greift (Standard 0.85) |
| `swipe`     | Nur bei `swipe`: `[x1, y1, x2, y2, ms]`                          |
| `keycode`   | Nur bei `key`: z. B. `KEYCODE_BACK`                             |
| `cooldown`  | Sekunden Pause nach einem Treffer                                |

Die Regeln werden pro Durchlauf von oben nach unten geprueft; die **erste**
zutreffende Regel wird ausgefuehrt.

## 7. Dateien

- `ldplayer.py` – ADB-Wrapper (connect, screenshot, tap, swipe, key, text)
- `vision.py` – Template-Matching mit OpenCV
- `bot.py` – Hauptschleife + Regel-Auswertung
- `config.example.json` – Beispiel-Konfiguration
- `templates/` – deine Referenzbilder

## Brawl Stars – Multi-Instanz-Bot

> 🚫 **Sehr wichtig:** Brawl Stars gehoert **Supercell**. Bots verstossen gegen
> deren Nutzungsbedingungen. Supercell erkennt Emulator-Botting aktiv und
> **sperrt Accounts dauerhaft** (oft die ganze Supercell-ID). **Nur mit
> Wegwerf-Accounts nutzen – niemals mit deinem Hauptaccount.** Verwendung auf
> eigenes Risiko.

Dateien:
- `brawl.py` – Ablauflogik pro Instanz: Play druecken → Match abwarten →
  einfache Spiel-Routine (laufen + schiessen) → Ende wegtippen →
  **automatisch wieder anstellen**. Optional **Account-Wechsel** nach N Matches.
- `multi.py` – startet **mehrere LDPlayer-Fenster gleichzeitig** (ein Thread
  pro Instanz).

### Realistische Grenzen
Der Bot bedient **Menues zuverlaessig** (anstellen, bestaetigen, Account
wechseln). Das **eigentliche Spielen im Match** ist bewusst simpel
(zufaellig laufen + schiessen) – ein Screenshot-Bot spielt nicht clever und
gewinnt nicht gezielt. Das ist eine technische Grenze, keine Faulheit.

### Einrichtung
1. Mehrere LDPlayer-Instanzen anlegen (LDPlayer Multi-Player-Manager) und in
   **jeder** Brawl Stars installieren + **je einen anderen Account** einloggen.
   In **jeder** Instanz ADB-Debugging aktivieren. ADB-Ports: `5555`, `5557`,
   `5559`, `5561` … (pro Instanz +2) – die genauen Ports mit dem Scanner
   ermitteln:
   ```bash
   python scan.py
   ```
   Der Scanner listet alle erreichbaren Instanzen mit Port und gibt einen
   fertigen `"instances"`-Block zum Einfuegen in die Config aus. So verbindest
   du jeden Account/jedes Fenster mit dem Bot.
2. Config anlegen:
   ```bash
   copy config.brawlstars.example.json config.brawlstars.json
   ```
   Ports/Namen der Instanzen eintragen. Fuer automatischen Fensterstart den
   Pfad zu `ldconsole.exe` unter `ldconsole` setzen (sonst leer lassen und
   Fenster manuell starten).
3. **Templates aufnehmen + Koordinaten finden** – dafuer gibt es den
   Aufnahme-Helfer (Pflichtschritt, fertige Templates gibt es nicht):
   ```bash
   python capture.py --port 5555
   ```
   Im Bildfenster: **Linksklick** zeigt die Koordinate (fuer `joystick` /
   `attack`), Taste **c** zieht ein Rechteck auf und speichert es nach
   Namenseingabe als Template in `templates/` (z. B. `play_button`,
   `in_match`, `proceed`, `reward`, `victory`, `defeat`; fuer den
   Account-Wechsel zusaetzlich `settings_button`, `supercell_id`, …).
   Taste **r** holt einen neuen Screenshot (z. B. nach Menuewechsel),
   **q** beendet.
4. In `config.brawlstars.json` die abgelesenen Werte eintragen:
   `joystick` = Mittelpunkt (cx, cy) + Radius des Bewegungs-Sticks,
   `attack` = Tap-Position zum Schiessen. Die Template-Namen muessen zu den
   gespeicherten Dateien passen.

### Ein-Klick-Start (Windows)
Einfach **Doppelklick auf `start.bat`**. Das Skript sucht die LDPlayer-adb,
installiert die Abhaengigkeiten, legt die Config an, scannt die Instanz-Ports
und oeffnet dann die Oberflaeche. Ideal fuer den taeglichen Start.

### Start – grafische Oberflaeche (manuell)
```bash
python gui.py
```
Fenster mit **Start/Stop pro Instanz**, **Alle starten/stoppen**,
**Dry-Run-Schalter** und **Live-Status** (Verbindung, Zustand, Match-Zahl)
plus Log. `tkinter` ist beim Windows-Python-Installer standardmaessig dabei.

### Start – Konsole
```bash
python multi.py                     # alle Instanzen aus der Config
python multi.py --dry-run           # nur erkennen, keine Eingaben
```
Erst mit **einer** Instanz und **Dry-Run** die Templates/Positionen testen,
dann auf mehrere Fenster hochskalieren.

### Aufbau (fuer Brawl Stars)
- `gui.py` – grafische Startflaeche (tkinter)
- `controller.py` – verwaltet die Instanz-Threads, Status, Start/Stop, Reconnect
- `brawl.py` – Ablauflogik pro Instanz (Stop-Signal, Status-/Log-Callbacks, Dry-Run)
- `multi.py` – Konsolen-Starter (nutzt denselben Controller)

`matches_per_account` in der Config: `0` = nie wechseln; `>0` = nach so vielen
Matches den Account-Wechsel ausfuehren.

## Anbindung an Jarvis (optional)

Die Jarvis-Web-App (`jarvis.html`) laeuft im Browser und kann aus der Sandbox
heraus **nicht** direkt Windows-Programme steuern. Wer Jarvis mit dem Bot
koppeln will, laesst diesen Python-Bot als lokalen Dienst laufen und spricht
ihn ueber eine kleine lokale HTTP-Schnittstelle an (z. B. Flask), die Jarvis
per `fetch` auf `http://localhost:...` aufruft.

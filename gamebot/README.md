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

## Anbindung an Jarvis (optional)

Die Jarvis-Web-App (`jarvis.html`) laeuft im Browser und kann aus der Sandbox
heraus **nicht** direkt Windows-Programme steuern. Wer Jarvis mit dem Bot
koppeln will, laesst diesen Python-Bot als lokalen Dienst laufen und spricht
ihn ueber eine kleine lokale HTTP-Schnittstelle an (z. B. Flask), die Jarvis
per `fetch` auf `http://localhost:...` aufruft.

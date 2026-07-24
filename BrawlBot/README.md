# BrawlBot

Ein Python-Projekt, das den **LDPlayer**-Emulator ueber **ADB** steuert:
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
cd BrawlBot
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

### Gruppen-Steuerpult (die Oberflaeche)
```bash
python gui.py
```
Zeigt die **Gruppen WIN und LOSE** nebeneinander. Pro Gruppe:
- Liste der Instanzen mit Live-Status (verbunden · Zustand · Klicks)
- **▶ Gruppe starten / ■ stoppen** – alle Instanzen der Gruppe laufen
  **synchron mit derselben Aufgabenliste** (gleiche Bewegung, gleiche Klicks)
- **Aufgabenliste** (zeitgesteuert): `🖼 Bild einfuegen` fuegt einen Button
  hinzu, der automatisch erkannt und alle *N* Sekunden geklickt wird;
  `↔ Bewegung` fuegt einen synchronen Swipe hinzu; `🗑 Entfernen` loescht.
- **Fenster** je Instanz: oeffnet ein Live-Bild. Dort **2× klicken** = Button
  ausschneiden und direkt als Bild-Aufgabe der Gruppe speichern.

Oben: **Profil-Auswahl**, **Dry-Run** (nur testen) und **💾 Profil speichern**.

#### Mehrere Configs (Profile)
Oben links waehlst du im **Profil**-Feld, welche Config gerade aktiv ist.
Jedes Profil ist eine eigene Datei in `configs/<name>.json` mit eigenen
Gruppen, Ports, Buttons und Aufgaben.
- **Profil-Dropdown**: zwischen `config1`, `config2`, … umschalten (laufende
  Instanzen werden vorher gestoppt).
- **＋ Neu**: neues Profil anlegen (aktuelles als Vorlage kopieren oder leer).
- **✎ Umbenennen**: aktuelles Profil umbenennen.
- **💾 Profil speichern**: aktuelles Profil sichern.

Beim ersten Start wird eine vorhandene `config.brawlstars.json` (bzw. die
Beispiel-Config) automatisch als Profil `standard` uebernommen.
**🗑 Loeschen** entfernt das aktuelle Profil (mindestens eins bleibt bestehen).

#### Weitere Bedien-Optionen
- **▶▶ Alle Gruppen starten** / **■ NOT-AUS** – alle Gruppen auf einmal
  starten bzw. sofort alles stoppen.
- **🔍 Ports scannen** – zeigt im Log, welche LDPlayer-Instanzen erreichbar
  sind (welche Ports du eintragen kannst).
- **Aufgabe bearbeiten** – Doppelklick auf eine Aufgabe: Intervall (und bei
  Bild-Aufgaben die Erkennungs-Schwelle) aendern.
- **Log: Leeren / Speichern** – Log-Fenster leeren oder als Textdatei sichern.
- **Instanz-Fenster: 💾 Screenshot** – aktuelles Emulatorbild als PNG speichern.

#### 🔁 Vollautomatik (kompletter Zyklus)
Der Knopf **🔁 Vollautomatik (Zyklus)** oben startet den ganzen Ablauf
selbststaendig und in Schleife (`cycle` in der Config):
1. **Accounts wechseln** – jede Instanz nimmt einen anderen, noch nicht
   benutzten Account (nach Name).
2. **Teams bilden** – in WIN und LOOSE erstellt je ein Host eine Lobby, die
   anderen treten per Team-Code bei.
3. **WIN geht in die Runde**, **LOOSE wartet `loose_delay` Sekunden** (Standard
   35) und geht dann auch rein (Timing, damit beide im selben Match landen).
4. **Spielphase**: WIN spielt + schiesst, LOOSE bewegt sich nur. Das Ende wird
   am **Endscreen erkannt** (`match_end_template`, z. B. `match_end.png`) –
   der Host achtet waehrend des Spielens nebenbei darauf. Kommt kein Endscreen,
   greift `match_timeout`. Ohne `match_end_template` wird stattdessen fest
   `match_duration` Sekunden gewartet.
5. **Team verlassen** → zurueck zu Schritt 1.

`rounds: 0` = endlos; `>0` = so viele Runden. **■ Stop Automatik** beendet den
Zyklus. Fuer diesen Modus sollten die Gruppen-`tasks` nur das **In-Match-
Verhalten** enthalten (WIN: bewegen+schiessen, LOOSE: nur bewegen) – die
Menue-Schritte (Lobby erstellen, Runde starten, Team verlassen) macht der
Zyklus ueber `start_match_steps` / `leave_steps` / `team`.

> ⚠️ **Ehrlich:** Ob WIN und LOOSE wirklich im **selben** Match landen, haengt
> an Supercells Matchmaking und am `loose_delay`-Timing – garantiert ist es
> nicht. Und ob WIN „gewinnt", haengt davon ab, dass LOOSE nicht schiesst und
> beide zusammen sind – der Bot spielt mechanisch, nicht clever. Sperr-Risiko
> ist hoch; nur Wegwerf-Accounts.

#### Account-Manager & Team-Lobby (👥 / 🔀 / 🏁)
- **👥 Accounts** – Liste der Accounts einer Gruppe pflegen (Name + Position
  im Konto-Menue). Der Bot **merkt sich benutzte** Accounts und waehlt beim
  Wechsel fuer **jede Instanz einen anderen**.
- **🔀 Accounts wechseln** – pausiert die Gruppe, jede Instanz wechselt ihren
  Account (fester Ablauf `switch_flow`) und die Steuerung laeuft weiter, sobald
  **alle** wieder in der Lobby sind.
- **🏁 Team-Lobby** – eine Instanz (Host, `team.host_index`) **erstellt eine
  Lobby**, der **Team-Code wird per OCR gelesen** (`team.code_region`) und an
  die anderen verteilt; die tippen ihn ein und **treten bei**. Erst wenn alle
  in der Lobby sind, laeuft die synchrone Steuerung weiter.
  - Braucht **Tesseract-OCR** (Windows-Installer von
    github.com/UB-Mannheim/tesseract). Pfad ggf. in der Config unter
    `tesseract_cmd` angeben, z. B.
    `C:\\Program Files\\Tesseract-OCR\\tesseract.exe`.
  - `code_region` = `[x, y, breite, hoehe]` des Bereichs, in dem der Code
    steht (im Instanz-Fenster ablesen).

Alle noetigen Buttons (Menue, Team, Beitreten, Bestaetigen …) nimmst du einmal
per Instanz-Fenster auf; die Ablaeufe stehen in der Config unter `switch_flow`
und `team` und lassen sich frei anpassen.

#### Menschlicheres Verhalten & Robustheit
- `humanize`: `pos_jitter` (zufaellige Klick-Abweichung in Pixeln),
  `interval_jitter` (zufaellige +/-% beim Timing) – damit die Instanzen nicht
  exakt gleich/gleichzeitig klicken.
- `detection.multi_scale`: erkennt Buttons auch bei leicht abweichender
  Aufloesung.
- **Auto-Reconnect (Watchdog)**: haengt/abgebrochen? Der Bot verbindet neu und
  macht weiter.

#### Chat pro Gruppe (💬) – in normaler Sprache steuern + lernen
Jede Gruppe hat einen **💬 Chat**-Knopf. Dort sagst du in normaler Sprache,
was die Gruppe tun soll:
- `starte` / `stopp` – Gruppe starten/stoppen
- `klicke play alle 5 sekunden` – Button-**Bild** automatisch klicken
- `klicke bei 500,700 alle 3 sekunden` – feste **Position** klicken (wo)
- `alle 3 sekunden` – alle Klick-Intervalle setzen
- `bewege 220,780,220,650 alle 1 sekunde` – **Bewegung** (von→nach, wie)
- `entferne play` – Aufgabe loeschen
- `nimm den play knopf auf` – oeffnet das Instanz-Fenster zum Ausschneiden
- `status` / `hilfe`

**Dazulernen:** `lerne "deine worte" = STARTE` merkt sich deine Formulierung
(gespeichert unter `groups.<Gruppe>.learned`). `vergiss deine worte` loescht sie.

**Optionale echte KI:** Hinterlegst du in der Config einen OpenAI-kompatiblen
Server, versteht der Chat auch freie Saetze – und **lernt** erfolgreiche
Uebersetzungen automatisch (danach ohne KI):
```json
"ai": {
  "server_url": "https://api.openai.com",
  "api_key": "sk-...",
  "model": "gpt-4o-mini"
}
```
(Funktioniert mit jedem OpenAI-kompatiblen Endpunkt – auch eigener/lokaler
Server wie Ollama/LM Studio.)

`tkinter` ist beim Windows-Python-Installer standardmaessig dabei.

#### Gruppen anpassen (config.brawlstars.json)
```json
"groups": {
  "WIN":  { "ports": [5555, 5557, 5559], "tasks": [ ... ] },
  "LOSE": { "ports": [5561, 5563, 5565], "tasks": [ ... ] }
}
```
`ports` = welche Instanzen zur Gruppe gehoeren (mit `python scan.py` ermitteln).
`tasks` kannst du komplett ueber die Oberflaeche pflegen. Aufgabentypen:
`tap_template` (Button per Bild, `interval` Sekunden), `swipe` (Bewegung),
`tap` (feste Position).

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

### Account-Wechsel: fest definierter Ablauf
Der Wechsel ist ein **von dir festgelegter Ablauf** aus einzelnen Schritten
(`account_switch.steps`). Jeder Schritt hat einen `type`:

| `type`           | Bedeutung                          | Felder                              |
|------------------|------------------------------------|-------------------------------------|
| `tap_template`   | Button per Bild erkennen + tippen  | `template`, `timeout`               |
| `tap`            | **feste Koordinate** antippen      | `x`, `y`                            |
| `swipe`          | wischen                            | `from:[x,y]`, `to:[x,y]`, `ms`      |
| `key`            | Hardware-Taste                     | `code` (z. B. `KEYCODE_BACK`)       |
| `wait`           | nur warten                         | –                                   |
| `select_account` | naechsten Account aus `accounts` waehlen | –                             |

Jeder Schritt kann `wait` (Sekunden Pause danach) setzen. Die Schritte werden
**strikt der Reihe nach** abgearbeitet – genau dein festgelegter Ablauf.

`accounts` ist die Liste, durch die `select_account` **reihum** schaltet. Ein
Eintrag waehlt den Account entweder ueber eine **feste Position**
(`"slot": [x, y]`, z. B. der Kontoeintrag in der Supercell-ID-Liste) oder ueber
ein Bild (`"template": "..."`).

Zwei Betriebsarten – frei kombinierbar:
- **Rein koordinatenbasiert** (keine Templates noetig): alles mit `tap`/`swipe`/
  `wait`. Robust, solange die Menues immer an derselben Stelle sind. Koordinaten
  mit `python capture.py --port ...` per Linksklick ablesen.
- **Bildbasiert** (`tap_template`): unempfindlicher gegen kleine Layout-
  verschiebungen, braucht aber die Templates.

Beispiel eines koordinatenbasierten Ablaufs (ohne Templates):
```json
"account_switch": {
  "steps": [
    { "type": "tap",  "x": 40,  "y": 40,  "wait": 1.5 },
    { "type": "tap",  "x": 900, "y": 120, "wait": 1.5 },
    { "type": "tap",  "x": 640, "y": 500, "wait": 2.0 },
    { "type": "select_account",           "wait": 2.0 },
    { "type": "tap",  "x": 640, "y": 620, "wait": 3.0 }
  ]
}
```

## Anbindung an Jarvis (optional)

Die Jarvis-Web-App (`jarvis.html`) laeuft im Browser und kann aus der Sandbox
heraus **nicht** direkt Windows-Programme steuern. Wer Jarvis mit dem Bot
koppeln will, laesst diesen Python-Bot als lokalen Dienst laufen und spricht
ihn ueber eine kleine lokale HTTP-Schnittstelle an (z. B. Flask), die Jarvis
per `fetch` auf `http://localhost:...` aufruft.

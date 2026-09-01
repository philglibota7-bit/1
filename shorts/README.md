# Shorts

Aus einem langen Video hochkantige Kurzclips machen: transkribieren,
interessante Abschnitte vorschlagen, auf 9:16 bringen, Untertitel einbrennen.

Alles laeuft auf deinem Rechner. Kein Dienst, kein Konto, keine Uploads.

---

## Was mache ich mit den heruntergeladenen Dateien?

Kurz: **nichts von Hand** – das Einrichtungsskript uebernimmt das.

```bash
bash shorts/einrichten.sh
```

Es durchsucht `~/Downloads`, `~/Desktop` und `~/Documents` nach `ffmpeg`,
`ffprobe` und entpackt gefundene Archive, legt die Programme nach
`shorts/bin/` und **entfernt die Quarantaenemarkierung von macOS**. Genau
daran scheitern heruntergeladene Programme sonst: macOS blockiert sie mit
„kann nicht geoeffnet werden, da der Entwickler nicht verifiziert werden
kann“. Danach richtet es eine Python-Umgebung ein und installiert
faster-whisper.

### Zwei Stolpersteine, die du kennen solltest

**ffprobe wird oft vergessen.** Wenn du ffmpeg als einzelne Datei
heruntergeladen hast (etwa von evermeet.cx), ist `ffprobe` ein **getrennter**
Download. Ohne ffprobe kennt das Werkzeug die Laenge deines Videos nicht.
Bequemer ist:

```bash
brew install ffmpeg     # bringt ffmpeg und ffprobe zusammen mit
```

**Apple Silicon oder Intel.** Eine Intel-Datei laeuft auf einem M-Mac nur
mit Rosetta, eine ARM-Datei gar nicht auf Intel. Das Skript merkt das und
sagt es dir, statt dich raten zu lassen.

**faster-whisper ist ein Python-Paket, kein Programm zum Anklicken.** Falls
du eine ZIP-Datei von GitHub geladen hast: die brauchst du nicht. Das Skript
installiert es ueber pip. Beim ersten Lauf laedt es zusaetzlich das
Sprachmodell (beim Modell `small` rund 500 MB) und legt es in
`~/.cache/huggingface` ab – das passiert genau einmal.

---

## Loslegen

```bash
bash shorts/einrichten.sh                       # einmalig
source shorts/.venv/bin/activate

# Video nach shorts/eingang/ legen, dann:
python3 shorts/shorts.py machen shorts/eingang/deinvideo.mp4
```

Die fertigen Clips liegen in `shorts/ausgabe/`, daneben je eine `.txt` mit
dem gesprochenen Text – daraus schreibst du Titel und Beschreibung.

## Die Befehle

| Befehl | Was er tut |
|---|---|
| `pruefen` | Sagt dir, was noch fehlt |
| `abschrift video.mp4` | Nur transkribieren. Der langsame Teil, einmal noetig |
| `vorschlaege video.mp4` | Kandidaten mit Zeit, Punktzahl und Text |
| `schneiden video.mp4 --von 61 --bis 95` | Genau einen Abschnitt schneiden |
| `machen video.mp4` | Alles zusammen: Abschrift, Auswahl, Schnitt |

Die Abschrift wird in `shorts/zwischenstand/` gespeichert. Ab dann kostet
jeder weitere Schnitt nur noch Sekunden – rechne beim ersten Durchgang mit
etwa einem Drittel der Videolaenge, danach mit fast nichts.

**Empfohlener Ablauf:** erst `vorschlaege`, dann selbst entscheiden und mit
`schneiden` genau die Stellen nehmen, die wirklich etwas taugen. Die
automatische Auswahl ist eine Vorsortierung, kein Urteil.

## Zwei Bildmodi

- `--modus unschaerfe` (Vorgabe): das Video mittig, dahinter dasselbe Bild
  unscharf und abgedunkelt. Nichts wird abgeschnitten. Richtig fuer
  Bildschirmaufnahmen, Gameplay, alles mit Text im Bild.
- `--modus zuschnitt`: die Mitte wird formatfuellend beschnitten. Wirkt
  staerker, verliert aber links und rechts. Richtig, wenn eine Person mittig
  im Bild ist.

## Einstellungen

Alles in `shorts/konfig.json`:

| Feld | Bedeutung |
|---|---|
| `clips.min_sekunden` / `max_sekunden` | Laenge der Clips (Shorts: bis 59 s) |
| `clips.anzahl` | Wie viele Clips `machen` erzeugt |
| `abschrift.modell` | `tiny`, `base`, `small`, `medium`, `large-v3` – groesser ist genauer und langsamer |
| `abschrift.sprache` | `de`, `en`, oder leer zum Erkennen |
| `untertitel.schrift` | Vorgabe `Helvetica`. Kraeftiger wirken `Impact` oder `Arial Black` |
| `untertitel.woerter_pro_zeile` | 3 ist ein guter Wert; mehr wird unruhig |
| `untertitel.position_von_unten` | 420 haelt die Untertitel ueber der Bedienleiste von YouTube |

## Was hier absichtlich nicht passiert

Nichts wird hochgeladen, nichts wird verschickt, es gibt keine
Schnittstelle zu YouTube. Das Hochladen machst du selbst – schon deshalb,
weil du vor der Veroeffentlichung ohnehin draufschauen solltest.

`shorts/eingang/`, `shorts/ausgabe/`, `shorts/zwischenstand/` und
`shorts/bin/` sind von Git ausgenommen. Das ist wichtig: dieses Repository
wird oeffentlich ins Netz gestellt, ein versehentlich mitgeschicktes
Rohvideo waere sofort fuer alle sichtbar.

## Rechtliches in einem Absatz

Kurzclips aus **fremden** Videos zu schneiden und hochzuladen ist eine
Urheberrechtsverletzung, auch mit Quellenangabe, auch bei kurzen
Ausschnitten. Fuer eigenes Material, lizenziertes Material oder Inhalte
unter einer passenden freien Lizenz gilt das nicht. Wenn du eigene Videos
zerlegst, ist alles unproblematisch.

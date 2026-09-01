"""Videoteil: analysieren, Kandidaten finden, schneiden, hochkant machen."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

SATZENDE = re.compile(r"[.!?…]$")


# ---------------------------------------------------------------- Werkzeuge
HIER = Path(__file__).resolve().parent
EIGENES_BIN = HIER / "bin"


def _finden(name: str) -> str:
    """Erst im projekteigenen bin/, dann im PATH.

    So funktioniert eine von Hand heruntergeladene ffmpeg-Datei sofort, ohne
    dass sie ins System kopiert oder eine PATH-Variable gesetzt werden muss.
    """
    eigen = EIGENES_BIN / name
    if eigen.is_file():
        return str(eigen)
    return shutil.which(name) or name


def ffmpeg_pfad() -> str:
    return _finden("ffmpeg")


def ffprobe_pfad() -> str:
    return _finden("ffprobe")


def lauf(befehl: list[str], still: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(befehl, capture_output=still, text=True)


def pruefe_werkzeuge() -> dict:
    """Was fehlt, damit die Kette laeuft?"""
    ergebnis = {"ffmpeg": None, "ffprobe": None, "encoder": [], "filter": [], "fehlt": []}
    ff = shutil.which("ffmpeg")
    fp = shutil.which("ffprobe")
    ergebnis["ffmpeg"] = ff
    ergebnis["ffprobe"] = fp
    if not ff:
        ergebnis["fehlt"].append("ffmpeg ist nicht im PATH")
        return ergebnis
    if not fp:
        ergebnis["fehlt"].append("ffprobe ist nicht im PATH (gehoert zu ffmpeg dazu)")

    enc = lauf([ff, "-hide_banner", "-encoders"]).stdout or ""
    fil = lauf([ff, "-hide_banner", "-filters"]).stdout or ""
    for name in ("libx264", "aac"):
        if re.search(rf"\b{name}\b", enc):
            ergebnis["encoder"].append(name)
        else:
            ergebnis["fehlt"].append(f"Encoder {name} fehlt in deinem ffmpeg")
    for name in ("subtitles", "gblur", "loudnorm", "silencedetect"):
        if re.search(rf"\b{name}\b", fil):
            ergebnis["filter"].append(name)
        else:
            ergebnis["fehlt"].append(f"Filter {name} fehlt in deinem ffmpeg")
    return ergebnis


def schrift_vorhanden(name: str) -> bool | None:
    """None = nicht pruefbar. Eine stillschweigend ersetzte Schrift ist der
    haeufigste Grund dafuer, dass Untertitel anders aussehen als gedacht."""
    fc = shutil.which("fc-match")
    if not fc:
        return None
    aus = lauf([fc, name]).stdout or ""
    return name.split()[0].lower() in aus.lower()


# ---------------------------------------------------------------- Analyse
def daten(video: Path) -> dict:
    roh = lauf([ffprobe_pfad(), "-v", "error", "-print_format", "json",
                "-show_format", "-show_streams", str(video)]).stdout
    d = json.loads(roh or "{}")
    bild = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), {})
    ton = next((s for s in d.get("streams", []) if s.get("codec_type") == "audio"), None)
    zaehler, nenner = (bild.get("r_frame_rate", "30/1").split("/") + ["1"])[:2]
    try:
        rate = float(zaehler) / float(nenner or 1)
    except (ValueError, ZeroDivisionError):
        rate = 30.0
    return {
        "dauer": float(d.get("format", {}).get("duration", 0) or 0),
        "breite": int(bild.get("width", 0) or 0),
        "hoehe": int(bild.get("height", 0) or 0),
        "bildrate": round(rate, 3),
        "hat_ton": ton is not None,
    }


def tonspur_ziehen(video: Path, ziel: Path) -> Path:
    """16 kHz Mono - genau das, was Whisper braucht, und viel kleiner."""
    ziel.parent.mkdir(parents=True, exist_ok=True)
    lauf([ffmpeg_pfad(), "-y", "-i", str(video), "-vn",
          "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(ziel)])
    return ziel


# ---------------------------------------------------------------- Kandidaten
def kandidaten(abschrift: dict, konfig: dict) -> list[dict]:
    """Zusammenhaengende Abschnitte finden, die als Clip taugen.

    Die Bewertung ist bewusst schlicht: sie schlaegt vor, sie entscheidet
    nicht. Welcher Moment wirklich traegt, sieht ein Mensch in zehn Sekunden
    besser als jede Heuristik - deshalb gibt `shorts.py vorschlaege` den Text
    mit aus, statt nur Zeitmarken.
    """
    c = konfig["clips"]
    min_s, max_s = float(c["min_sekunden"]), float(c["max_sekunden"])
    abstand = float(c.get("abstand_sekunden", 10))

    segmente = [s for s in abschrift.get("segmente", []) if str(s.get("text", "")).strip()]
    if not segmente:
        return []

    roh = []
    for i, start_seg in enumerate(segmente):
        von = float(start_seg["start"])
        text = ""
        for j in range(i, len(segmente)):
            text = (text + " " + str(segmente[j]["text"]).strip()).strip()
            bis = float(segmente[j]["ende"])
            laenge = bis - von
            if laenge < min_s:
                continue
            if laenge > max_s:
                break
            # Nur an einem Satzende aufhoeren - ein Clip, der mitten im Wort
            # abbricht, wird sofort weggewischt.
            if not SATZENDE.search(text.strip()):
                continue
            roh.append({"von": round(von, 2), "bis": round(bis, 2),
                        "dauer": round(laenge, 2), "text": text,
                        "punkte": bewerten(text, laenge, von)})
    roh.sort(key=lambda k: -k["punkte"])

    # Ueberschneidungen aussortieren: zwei fast gleiche Clips bringen nichts
    gewaehlt: list[dict] = []
    for k in roh:
        if all(k["bis"] + abstand <= g["von"] or k["von"] >= g["bis"] + abstand
               for g in gewaehlt):
            gewaehlt.append(k)
        if len(gewaehlt) >= int(c.get("anzahl", 5)):
            break
    gewaehlt.sort(key=lambda k: k["von"])
    return gewaehlt


HAKEN = ("warum", "wie", "was", "nie", "immer", "fehler", "wichtig", "geheim",
         "niemand", "die meisten", "das problem", "achtung", "trick", "besser",
         "schlecht", "verboten", "kostenlos", "sofort", "eigentlich")


def bewerten(text: str, dauer: float, von: float) -> int:
    """0-100. Grob, aber besser als die Reihenfolge im Video."""
    t = text.lower()
    punkte = 40

    # Ein Aufhaenger in den ersten Woertern entscheidet ueber die ersten
    # drei Sekunden - und die entscheiden ueber alles Weitere.
    anfang = " ".join(t.split()[:12])
    if any(h in anfang for h in HAKEN):
        punkte += 20
    if "?" in text[:120]:
        punkte += 10

    woerter = len(t.split())
    tempo = woerter / dauer if dauer else 0
    if 2.0 <= tempo <= 3.6:          # ruhig genug zum Folgen, schnell genug
        punkte += 15
    elif tempo < 1.2:
        punkte -= 15                  # zu viel Stille

    if 25 <= dauer <= 45:
        punkte += 10
    if any(z.isdigit() for z in text[:80]):
        punkte += 5                   # konkrete Zahlen halten Aufmerksamkeit
    if von < 15:
        punkte -= 10                  # Intro und Begruessung taugen selten
    return max(0, min(100, punkte))


# ---------------------------------------------------------------- Schneiden
def filterkette(modus: str, konfig: dict, ass: Path | None) -> str:
    """Baut die Videofilter-Kette fuer 9:16."""
    b = konfig["video"]["breite"]
    h = konfig["video"]["hoehe"]

    if modus == "zuschnitt":
        kette = (f"[0:v]scale={b}:{h}:force_original_aspect_ratio=increase,"
                 f"crop={b}:{h},setsar=1[v]")
    else:  # unschaerfe: unscharfer Hintergrund, Video mittig darauf
        kette = (
            f"[0:v]split=2[bg][fg];"
            f"[bg]scale={b}:{h}:force_original_aspect_ratio=increase,"
            f"crop={b}:{h},gblur=sigma=32,eq=brightness=-0.12[bgb];"
            f"[fg]scale={b}:{h}:force_original_aspect_ratio=decrease[fgs];"
            f"[bgb][fgs]overlay=(W-w)/2:(H-h)/2,setsar=1[v]"
        )

    if ass:
        # Doppelpunkt und Backslash muessen im Filterargument entwertet werden,
        # sonst bricht die Kette bei jedem Pfad mit Sonderzeichen.
        pfad = str(ass).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
        kette = kette.replace("[v]", "[vp]") + f";[vp]subtitles='{pfad}'[v]"
    return kette


def clip(quelle: Path, ziel: Path, von: float, bis: float, konfig: dict,
         ass: Path | None = None, modus: str = "unschaerfe",
         hat_ton: bool = True) -> subprocess.CompletedProcess:
    v = konfig["video"]
    a = konfig["audio"]
    ziel.parent.mkdir(parents=True, exist_ok=True)

    befehl = [ffmpeg_pfad(), "-y", "-hide_banner", "-loglevel", "error",
              "-ss", f"{von:.3f}", "-i", str(quelle), "-t", f"{bis - von:.3f}",
              "-filter_complex", filterkette(modus, konfig, ass),
              "-map", "[v]"]
    if hat_ton:
        befehl += ["-map", "0:a:0",
                   "-af", f"loudnorm=I={a['lautheit_lufs']}:TP=-1.5:LRA=11",
                   "-c:a", "aac", "-b:a", a["bitrate"], "-ar", "48000"]
    else:
        befehl += ["-an"]
    befehl += ["-c:v", "libx264", "-preset", "medium", "-crf", str(v["crf"]),
               "-profile:v", "high", "-pix_fmt", "yuv420p",
               "-r", str(v["bildrate"]), "-g", str(int(v["bildrate"]) * 2),
               "-movflags", "+faststart", str(ziel)]
    return lauf(befehl)

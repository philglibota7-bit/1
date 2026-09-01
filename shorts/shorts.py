#!/usr/bin/env python3
"""shorts - aus langen Videos hochkantige Kurzclips machen.

    python3 shorts.py pruefen                  Laeuft alles, was gebraucht wird?
    python3 shorts.py abschrift video.mp4      Nur transkribieren (einmal noetig)
    python3 shorts.py vorschlaege video.mp4    Kandidaten mit Text anzeigen
    python3 shorts.py schneiden video.mp4 --von 61 --bis 95
    python3 shorts.py machen video.mp4         Alles auf einmal

Die Abschrift wird zwischengespeichert. Sie ist der langsame Teil - danach
kostet jeder weitere Schnitt nur noch Sekunden.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER))

import schnitt          # noqa: E402
import untertitel       # noqa: E402


def konfig_laden(pfad: Path | None = None) -> dict:
    p = pfad or HIER / "konfig.json"
    with p.open(encoding="utf-8") as f:
        return json.load(f)


def zwischenstand(video: Path) -> Path:
    d = HIER / "zwischenstand"
    d.mkdir(parents=True, exist_ok=True)
    return d / (video.stem + ".json")


def mmss(sekunden: float) -> str:
    m, s = divmod(int(sekunden), 60)
    return f"{m}:{s:02d}"


# --------------------------------------------------------------- pruefen
def befehl_pruefen(args) -> int:
    konfig = konfig_laden(args.konfig)
    p = schnitt.pruefe_werkzeuge()

    print("\n\033[1mVideo\033[0m")
    print(f"  ffmpeg    {p['ffmpeg'] or 'FEHLT'}")
    print(f"  ffprobe   {p['ffprobe'] or 'FEHLT'}")

    print("\n\033[1mAbschrift\033[0m")
    try:
        import faster_whisper  # noqa: F401
        print("  faster-whisper ist installiert")
    except ImportError:
        p["fehlt"].append("faster-whisper fehlt: pip install faster-whisper")
        print("  faster-whisper FEHLT")

    print("\n\033[1mSchrift fuer Untertitel\033[0m")
    name = konfig["untertitel"]["schrift"]
    da = schnitt.schrift_vorhanden(name)
    if da is True:
        print(f"  {name}: gefunden")
    elif da is False:
        print(f"  {name}: NICHT gefunden - es wird stillschweigend eine andere "
              "genommen. Trag in konfig.json eine vorhandene Schrift ein.")
    else:
        print(f"  {name}: nicht pruefbar (fc-match fehlt). Sieht der erste Clip "
              "falsch aus, liegt es vermutlich hier.")

    if p["fehlt"]:
        print("\n\033[1mDas fehlt noch\033[0m")
        for f in p["fehlt"]:
            print(f"  - {f}")
        print("\n  Hilfe dazu: shorts/README.md\n")
        return 1
    print("\n  Alles da. Leg ein Video in shorts/eingang/ und starte "
          "`python3 shorts.py machen eingang/deinvideo.mp4`\n")
    return 0


# --------------------------------------------------------------- abschrift
def abschrift_erstellen(video: Path, konfig: dict, neu: bool = False) -> dict:
    ziel = zwischenstand(video)
    if ziel.exists() and not neu:
        with ziel.open(encoding="utf-8") as f:
            return json.load(f)

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("faster-whisper fehlt. Installieren mit: pip install faster-whisper")

    a = konfig["abschrift"]
    ton = HIER / "zwischenstand" / (video.stem + ".wav")
    print(f"  Tonspur wird gezogen …")
    schnitt.tonspur_ziehen(video, ton)

    print(f"  Modell {a['modell']} wird geladen (beim ersten Mal wird es "
          "heruntergeladen) …")
    modell = WhisperModel(a["modell"], device="cpu", compute_type=a.get("rechenart", "int8"))

    print("  Abschrift laeuft. Das dauert etwa ein Drittel der Videolaenge.")
    begonnen = time.time()
    segmente, info = modell.transcribe(
        str(ton),
        language=a.get("sprache") or None,
        word_timestamps=True,
        vad_filter=True,       # Stille ueberspringen: schneller und genauer
    )

    daten = {"sprache": info.language, "dauer": info.duration, "segmente": []}
    for s in segmente:
        daten["segmente"].append({
            "start": round(s.start, 3),
            "ende": round(s.end, 3),
            "text": s.text.strip(),
            "woerter": [{"wort": w.word, "start": round(w.start, 3),
                         "ende": round(w.end, 3)} for w in (s.words or [])],
        })
        print(f"\r  {mmss(s.end)} / {mmss(info.duration)}", end="", flush=True)

    print(f"\n  Fertig in {time.time() - begonnen:.0f} s, "
          f"{len(daten['segmente'])} Abschnitte.")
    with ziel.open("w", encoding="utf-8") as f:
        json.dump(daten, f, ensure_ascii=False, indent=1)
    ton.unlink(missing_ok=True)
    return daten


def befehl_abschrift(args) -> int:
    konfig = konfig_laden(args.konfig)
    video = Path(args.video)
    if not video.exists():
        sys.exit(f"Video nicht gefunden: {video}")
    abschrift_erstellen(video, konfig, neu=args.neu)
    print(f"  Gespeichert: {zwischenstand(video)}")
    return 0


# --------------------------------------------------------------- vorschlaege
def befehl_vorschlaege(args) -> int:
    konfig = konfig_laden(args.konfig)
    video = Path(args.video)
    if not video.exists():
        sys.exit(f"Video nicht gefunden: {video}")
    daten = abschrift_erstellen(video, konfig)
    liste = schnitt.kandidaten(daten, konfig)
    if not liste:
        print("\n  Keine passenden Abschnitte gefunden. Vielleicht ist das Video "
              "zu kurz, oder die Mindestlaenge in konfig.json ist zu hoch.\n")
        return 1

    print(f"\n\033[1m{len(liste)} Vorschlaege\033[0m\n")
    for i, k in enumerate(liste, 1):
        text = k["text"]
        if len(text) > 300:
            text = text[:297] + "…"
        print(f"\033[1m{i}. {mmss(k['von'])}–{mmss(k['bis'])}  "
              f"({k['dauer']:.0f} s, {k['punkte']} Punkte)\033[0m")
        print(f"   {text}\n")
    print("  Einen davon schneiden:")
    print(f"    python3 shorts.py schneiden {args.video} "
          f"--von {liste[0]['von']} --bis {liste[0]['bis']}\n")
    return 0


# --------------------------------------------------------------- schneiden
def einen_clip(video: Path, daten: dict, konfig: dict, von: float, bis: float,
               nummer: int, modus: str, info: dict) -> Path | None:
    woerter = untertitel.ausschnitt(untertitel.aus_abschrift(daten), von, bis)
    ass = None
    if woerter:
        ass = HIER / "zwischenstand" / f"{video.stem}-{nummer:02d}.ass"
        ass.write_text(
            untertitel.ass_erzeugen(woerter, konfig["untertitel"],
                                    konfig["video"]["breite"],
                                    konfig["video"]["hoehe"], versatz=von),
            encoding="utf-8")

    ziel = HIER / "ausgabe" / f"{video.stem}-{nummer:02d}.mp4"
    ergebnis = schnitt.clip(video, ziel, von, bis, konfig, ass, modus,
                            hat_ton=info.get("hat_ton", True))
    if ergebnis.returncode != 0:
        print(f"  Fehler bei Clip {nummer}:")
        print("   ", (ergebnis.stderr or "").strip().splitlines()[-1:] or "unbekannt")
        return None

    text = " ".join(w.text for w in woerter).strip()
    (ziel.with_suffix(".txt")).write_text(
        f"Quelle: {video.name}\nAbschnitt: {mmss(von)}–{mmss(bis)} "
        f"({bis - von:.0f} s)\n\nGesprochener Text:\n{text}\n",
        encoding="utf-8")
    return ziel


def befehl_schneiden(args) -> int:
    konfig = konfig_laden(args.konfig)
    video = Path(args.video)
    if not video.exists():
        sys.exit(f"Video nicht gefunden: {video}")
    info = schnitt.daten(video)
    if args.bis <= args.von:
        sys.exit("--bis muss groesser als --von sein.")
    if info["dauer"] and args.bis > info["dauer"] + 1:
        sys.exit(f"Das Video ist nur {mmss(info['dauer'])} lang.")

    daten = abschrift_erstellen(video, konfig) if not args.ohne_untertitel else {"segmente": []}
    print(f"  Schneide {mmss(args.von)}–{mmss(args.bis)} …")
    ziel = einen_clip(video, daten, konfig, args.von, args.bis, args.nummer,
                      args.modus, info)
    if not ziel:
        return 1
    print(f"  Fertig: {ziel}  ({ziel.stat().st_size / 1048576:.1f} MB)")
    return 0


# --------------------------------------------------------------- machen
def befehl_machen(args) -> int:
    konfig = konfig_laden(args.konfig)
    video = Path(args.video)
    if not video.exists():
        sys.exit(f"Video nicht gefunden: {video}")

    info = schnitt.daten(video)
    print(f"\n  {video.name}: {mmss(info['dauer'])}, "
          f"{info['breite']}x{info['hoehe']}, {info['bildrate']:g} fps"
          f"{'' if info['hat_ton'] else ', OHNE TON'}")

    daten = abschrift_erstellen(video, konfig)
    liste = schnitt.kandidaten(daten, konfig)
    if not liste:
        print("\n  Keine passenden Abschnitte gefunden.\n")
        return 1

    print(f"\n  {len(liste)} Clips werden erzeugt …\n")
    fertig = []
    for i, k in enumerate(liste, 1):
        print(f"  {i}/{len(liste)}  {mmss(k['von'])}–{mmss(k['bis'])} "
              f"({k['punkte']} Punkte)")
        ziel = einen_clip(video, daten, konfig, k["von"], k["bis"], i,
                          args.modus, info)
        if ziel:
            fertig.append(ziel)

    print(f"\n\033[1m{len(fertig)} von {len(liste)} Clips fertig\033[0m")
    for z in fertig:
        print(f"  {z.relative_to(HIER)}  ({z.stat().st_size / 1048576:.1f} MB)")
    print(f"\n  Neben jedem Clip liegt eine .txt mit dem gesprochenen Text -\n"
          f"  daraus schreibst du Titel und Beschreibung.\n")
    return 0


# --------------------------------------------------------------- CLI
def parser_bauen() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="shorts", description="Aus langen Videos hochkantige Kurzclips machen.")
    p.add_argument("--konfig", type=Path, help="andere Konfigurationsdatei")
    u = p.add_subparsers(dest="befehl", required=True)

    u.add_parser("pruefen", help="Laeuft alles, was gebraucht wird?"
                 ).set_defaults(funktion=befehl_pruefen)

    a = u.add_parser("abschrift", help="Video transkribieren")
    a.add_argument("video")
    a.add_argument("--neu", action="store_true", help="vorhandene Abschrift verwerfen")
    a.set_defaults(funktion=befehl_abschrift)

    v = u.add_parser("vorschlaege", help="Kandidaten mit Text anzeigen")
    v.add_argument("video")
    v.set_defaults(funktion=befehl_vorschlaege)

    s = u.add_parser("schneiden", help="Einen bestimmten Abschnitt schneiden")
    s.add_argument("video")
    s.add_argument("--von", type=float, required=True, help="Startsekunde")
    s.add_argument("--bis", type=float, required=True, help="Endsekunde")
    s.add_argument("--nummer", type=int, default=1, help="Nummer im Dateinamen")
    s.add_argument("--modus", choices=["unschaerfe", "zuschnitt"], default="unschaerfe")
    s.add_argument("--ohne-untertitel", action="store_true")
    s.set_defaults(funktion=befehl_schneiden)

    m = u.add_parser("machen", help="Abschrift, Auswahl und Schnitt in einem")
    m.add_argument("video")
    m.add_argument("--modus", choices=["unschaerfe", "zuschnitt"], default="unschaerfe")
    m.set_defaults(funktion=befehl_machen)
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser_bauen().parse_args(argv)
    try:
        return args.funktion(args)
    except BrokenPipeError:
        # Passiert bei `shorts.py vorschlaege … | head`. Ohne diese Behandlung
        # wirft Python beim Beenden zusaetzlich einen haesslichen Traceback.
        try:
            sys.stdout.close()
        except Exception:
            pass
        return 0
    except KeyboardInterrupt:
        print("\n  Abgebrochen.")
        return 130


if __name__ == "__main__":
    sys.exit(main())

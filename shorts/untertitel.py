"""Untertitel im Shorts-Stil erzeugen.

Nicht die klassische Fassung mit ganzen Saetzen unten im Bild, sondern das,
was auf Shorts und TikTok tatsaechlich funktioniert: zwei bis vier Woerter
gleichzeitig, gross, mittig, und das gerade gesprochene Wort farbig
hervorgehoben. Das haelt den Blick auf dem Bild, auch ohne Ton - und ohne
Ton schauen die meisten.

Ausgabe ist ASS, weil dieses Format Farbwechsel innerhalb einer Zeile kann.
SRT kann das nicht.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Wort:
    text: str
    start: float
    ende: float


def zeit(sekunden: float) -> str:
    """ASS erwartet H:MM:SS.hh - Hundertstel, nicht Millisekunden."""
    sekunden = max(0.0, sekunden)
    stunden, rest = divmod(sekunden, 3600)
    minuten, sek = divmod(rest, 60)
    return f"{int(stunden)}:{int(minuten):02d}:{sek:05.2f}"


def farbe(hex_rgb: str) -> str:
    """'00E5FF' -> '&H00FFE500' - ASS speichert BGR, nicht RGB.

    Das ist die haeufigste Fehlerquelle bei ASS: die Farbe kommt falsch heraus
    und niemand weiss warum.
    """
    h = hex_rgb.strip().lstrip("#").upper()
    if len(h) != 6:
        raise ValueError(f"Farbe muss sechs Hexstellen haben: {hex_rgb!r}")
    return f"&H00{h[4:6]}{h[2:4]}{h[0:2]}"


def schuetzen(text: str) -> str:
    """Geschweifte Klammern sind in ASS Steuerzeichen."""
    return text.replace("{", "(").replace("}", ")").replace("\n", " ")


def gruppieren(woerter: list[Wort], pro_zeile: int, max_pause: float = 0.9) -> list[list[Wort]]:
    """Woerter zu Anzeigegruppen buendeln.

    Eine laengere Sprechpause beendet die Gruppe auch dann, wenn sie noch
    nicht voll ist - sonst steht ein Wort von vor der Pause noch im Bild,
    waehrend schon das naechste gesprochen wird.
    """
    gruppen: list[list[Wort]] = []
    aktuell: list[Wort] = []
    for w in woerter:
        if aktuell:
            pause = w.start - aktuell[-1].ende
            if len(aktuell) >= pro_zeile or pause > max_pause:
                gruppen.append(aktuell)
                aktuell = []
        aktuell.append(w)
    if aktuell:
        gruppen.append(aktuell)
    return gruppen


def ass_erzeugen(woerter: list[Wort], einst: dict, breite: int, hoehe: int,
                 versatz: float = 0.0) -> str:
    """Vollstaendige ASS-Datei. `versatz` verschiebt alle Zeiten (fuer Clips)."""
    pro_zeile = int(einst.get("woerter_pro_zeile", 3))
    groesse = int(einst.get("groesse", 78))
    rand = int(einst.get("rand", 6))
    unten = int(einst.get("position_von_unten", 420))
    schrift = einst.get("schrift", "DejaVu Sans")
    normal = farbe(einst.get("farbe", "FFFFFF"))
    aktiv = farbe(einst.get("farbe_aktiv", "00E5FF"))

    kopf = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {breite}
PlayResY: {hoehe}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Haupt,{schrift},{groesse},{normal},{normal},&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,{rand},3,2,60,60,{unten},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    zeilen = []
    for gruppe in gruppieren(woerter, pro_zeile):
        if not gruppe:
            continue
        for i, w in enumerate(gruppe):
            # Je gesprochenem Wort ein eigener Eintrag: dieselbe Gruppe wird
            # erneut gezeigt, nur die Hervorhebung wandert weiter.
            start = w.start - versatz
            ende = (gruppe[i + 1].start if i + 1 < len(gruppe) else w.ende) - versatz
            if ende <= start:
                ende = start + 0.08
            if ende <= 0:
                continue
            teile = []
            for j, g in enumerate(gruppe):
                t = schuetzen(g.text.strip())
                if not t:
                    continue
                teile.append(f"{{\\c{aktiv}}}{t}" if j == i else f"{{\\c{normal}}}{t}")
            if not teile:
                continue
            zeilen.append(
                f"Dialogue: 0,{zeit(max(0.0, start))},{zeit(ende)},Haupt,,0,0,0,,"
                + " ".join(teile)
            )

    return kopf + "\n".join(zeilen) + "\n"


def aus_abschrift(daten: dict) -> list[Wort]:
    """Wortliste aus der von shorts.py gespeicherten Abschrift lesen."""
    woerter = []
    for s in daten.get("segmente", []):
        for w in s.get("woerter", []):
            text = str(w.get("wort", "")).strip()
            if text:
                woerter.append(Wort(text, float(w["start"]), float(w["ende"])))
    return woerter


def ausschnitt(woerter: list[Wort], von: float, bis: float) -> list[Wort]:
    """Nur die Woerter, die in den Clip fallen - an den Raendern beschnitten."""
    drin = []
    for w in woerter:
        if w.ende <= von or w.start >= bis:
            continue
        drin.append(Wort(w.text, max(w.start, von), min(w.ende, bis)))
    return drin

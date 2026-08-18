"""
Bild-Erkennung fuer den Bot.

Ein Bot muss "sehen", was auf dem Bildschirm ist. Hier per Template-Matching:
Wir suchen ein kleines Referenzbild (z. B. einen Button) im Screenshot und
bekommen dessen Position + Trefferguete zurueck.

Referenzbilder (Templates) legst du im Ordner 'templates/' ab -- am besten
Ausschnitte aus einem echten LDPlayer-Screenshot in derselben Aufloesung.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

TEMPLATE_DIR = Path(__file__).parent / "templates"


@dataclass
class Match:
    found: bool
    x: int          # Mittelpunkt X (fuer tap)
    y: int          # Mittelpunkt Y
    score: float    # 0..1, je hoeher desto sicherer


def load_template(name: str) -> np.ndarray:
    path = TEMPLATE_DIR / name
    tmpl = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if tmpl is None:
        raise FileNotFoundError(f"Template nicht gefunden: {path}")
    return tmpl


def find(screen: np.ndarray, template_name: str, threshold: float = 0.85,
         scales=None) -> Match:
    """
    Sucht ein Template im Screenshot; gibt den besten Treffer zurueck.
    Mit 'scales' (Liste von Faktoren) wird das Template in mehreren Groessen
    probiert -> robuster, wenn die Aufloesung leicht abweicht (Multi-Scale).
    """
    tmpl = load_template(template_name)
    sh, sw = screen.shape[:2]
    best = Match(found=False, x=0, y=0, score=0.0)
    for s in (scales or [1.0]):
        if s == 1.0:
            t = tmpl
        else:
            th, tw = tmpl.shape[:2]
            t = cv2.resize(tmpl, (max(1, int(tw * s)), max(1, int(th * s))))
        h, w = t.shape[:2]
        if h > sh or w > sw:
            continue
        result = cv2.matchTemplate(screen, t, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if max_val > best.score:
            best = Match(found=False, x=int(max_loc[0] + w / 2),
                         y=int(max_loc[1] + h / 2), score=float(max_val))
    best.found = best.score >= threshold
    return best


def read_text(screen: np.ndarray, region, tesseract_cmd: str = "",
              whitelist: str = "") -> str:
    """
    Liest Text aus einem Bildbereich (z. B. den Team-Code) per OCR.
    Benoetigt 'pytesseract' + installiertes Tesseract-OCR. Ist es nicht
    vorhanden, wird "" zurueckgegeben (Feature einfach nicht verfuegbar).
    region = [x, y, w, h].
    """
    try:
        import pytesseract
    except ImportError:
        return ""
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    x, y, w, h = region
    crop = screen[y:y + h, x:x + w]
    if crop.size == 0:
        return ""
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    config = "--psm 7"
    if whitelist:
        config += f" -c tessedit_char_whitelist={whitelist}"
    try:
        text = pytesseract.image_to_string(gray, config=config)
    except Exception:  # noqa: BLE001
        return ""
    return text.strip()

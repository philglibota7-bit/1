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


def find(screen: np.ndarray, template_name: str, threshold: float = 0.85) -> Match:
    """Sucht ein Template im Screenshot. Gibt den besten Treffer zurueck."""
    tmpl = load_template(template_name)
    result = cv2.matchTemplate(screen, tmpl, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    h, w = tmpl.shape[:2]
    cx = int(max_loc[0] + w / 2)
    cy = int(max_loc[1] + h / 2)
    return Match(found=max_val >= threshold, x=cx, y=cy, score=float(max_val))

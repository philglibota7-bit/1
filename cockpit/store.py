"""Datenhaltung fuer die Werkbank-Steuerung.

Die Daten liegen bewusst AUSSERHALB des Repos (Standard: ~/.werkbank/), weil
dieses Repo per GitHub Pages oeffentlich ausgeliefert wird. Geschaeftszahlen
haben dort nichts zu suchen. Ueberschreibbar per WERKBANK_HOME.

Die Liste der Tools selbst steht in tools.json im Repo - eine Quelle, kein
Abgleich von Hand.
"""

from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path

VERSION = 2

IDEE_STATUS = ["neu", "geprueft", "gebaut", "verworfen"]


def repo() -> Path:
    return Path(__file__).resolve().parent.parent


def home() -> Path:
    return Path(os.environ.get("WERKBANK_HOME", Path.home() / ".werkbank"))


def db_pfad() -> Path:
    return home() / "daten.json"


def leer() -> dict:
    return {
        "version": VERSION,
        "einstellungen": {
            "ziel_monat_cent": 50000,
            "gestartet_am": date.today().isoformat(),
        },
        "ideen": [],
        "monate": [],
        "zaehler": {"idee": 0},
    }


def migriere(db: dict) -> dict:
    basis = leer()
    for k, v in basis.items():
        db.setdefault(k, v)
    for k, v in basis["einstellungen"].items():
        db["einstellungen"].setdefault(k, v)
    db["zaehler"].setdefault("idee", 0)
    db["version"] = VERSION
    return db


def laden() -> dict:
    p = db_pfad()
    if not p.exists():
        return leer()
    with p.open(encoding="utf-8") as f:
        return migriere(json.load(f))


def speichern(db: dict) -> None:
    p = db_pfad()
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    tmp.replace(p)  # atomar: nie ein halb geschriebener Datenbestand


def naechste_id(db: dict, art: str) -> int:
    db["zaehler"][art] = db["zaehler"].get(art, 0) + 1
    return db["zaehler"][art]


def idee_finden(db: dict, kennung: str) -> dict | None:
    if kennung.isdigit():
        nr = int(kennung)
        return next((i for i in db["ideen"] if i["id"] == nr), None)
    klein = kennung.lower()
    treffer = [i for i in db["ideen"] if klein in i["titel"].lower()]
    return treffer[0] if len(treffer) == 1 else None


def registry() -> dict:
    """tools.json aus dem Repo lesen - die eine Wahrheit ueber die Tools."""
    p = repo() / "tools.json"
    if not p.exists():
        return {"marke": {}, "tools": []}
    with p.open(encoding="utf-8") as f:
        return json.load(f)


def monat_eintrag(db: dict, monat: str, slug: str) -> dict:
    for m in db["monate"]:
        if m["monat"] == monat and m["slug"] == slug:
            return m
    neu = {"monat": monat, "slug": slug, "besucher": 0, "kaeufe": 0, "umsatz_cent": 0}
    db["monate"].append(neu)
    return neu

"""Geldbetraege. Intern immer in Cent (int) - Fliesskomma verliert Geld."""

from __future__ import annotations


def zu_cent(text: str | int | float) -> int:
    """'800' -> 80000, '1.250,50' -> 125050, '99.90' -> 9990."""
    if isinstance(text, int):
        return text * 100
    if isinstance(text, float):
        return round(text * 100)
    s = str(text).strip().replace("€", "").replace(" ", "")
    if not s:
        raise ValueError("leerer Betrag")
    if "," in s:
        # deutsches Format: Punkt ist Tausendertrenner
        s = s.replace(".", "").replace(",", ".")
    negativ = s.startswith("-")
    s = s.lstrip("-+")
    if not s.replace(".", "", 1).isdigit():
        raise ValueError(f"kein gueltiger Betrag: {text!r}")
    cent = round(float(s) * 100)
    return -cent if negativ else cent


def eur(cent: int) -> str:
    """80000 -> '800,00 EUR'"""
    return f"{fmt(cent)} EUR"


def fmt(cent: int) -> str:
    """80000 -> '800,00' (deutsche Schreibweise)"""
    vorzeichen = "-" if cent < 0 else ""
    cent = abs(int(cent))
    ganz, rest = divmod(cent, 100)
    return f"{vorzeichen}{ganz:,}".replace(",", ".") + f",{rest:02d}"

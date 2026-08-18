"""Welche Idee wird gebaut?

Der Engpass dieses Modells ist nicht das Bauen - es ist die Nachfrage. Ein
technisch schoenes Tool, das niemand sucht, ist verlorene Zeit. Diese Bewertung
zwingt dazu, vor dem Bauen sechs Fragen ehrlich zu beantworten.

Jede Frage 0-5. Die Gewichte spiegeln, was tatsaechlich ueber Erfolg entscheidet:
Nachfrage und Zahlungsbereitschaft schlagen alles andere.
"""

from __future__ import annotations

KRITERIEN = {
    "nachfrage": {
        "gewicht": 2.5, "invers": False,
        "frage": "Suchen genug Leute aktiv danach?",
        "hilfe": "0 = niemand · 3 = ein paar hundert im Monat · 5 = zehntausende",
    },
    "absicht": {
        "gewicht": 2.5, "invers": False,
        "frage": "Steckt Geld hinter der Suche?",
        "hilfe": "0 = reine Neugier · 3 = beruflicher Bedarf · 5 = akutes Problem, das Geld kostet",
    },
    "pro_hebel": {
        "gewicht": 2.0, "invers": False,
        "frage": "Gibt es eine glaubwuerdige Pro-Funktion?",
        "hilfe": "0 = keine denkbar · 3 = Komfort · 5 = ohne sie ist es beruflich unbrauchbar",
    },
    "wettbewerb": {
        "gewicht": 1.5, "invers": True,
        "frage": "Wie stark ist der Wettbewerb?",
        "hilfe": "0 = frei · 3 = etliche mittelmaessige · 5 = grosse Anbieter mit viel Geld",
    },
    "wiederkehr": {
        "gewicht": 1.5, "invers": False,
        "frage": "Wird es wiederholt gebraucht?",
        "hilfe": "0 = einmal im Leben · 3 = ein paar Mal im Jahr · 5 = woechentlich",
    },
    "aufwand": {
        "gewicht": 1.0, "invers": True,
        "frage": "Wie viel Arbeit bis zur ersten Fassung?",
        "hilfe": "0 = ein Nachmittag · 3 = eine Woche · 5 = Monate",
    },
}

GRENZE_BAUEN = 65      # ab hier lohnt der Bau
GRENZE_VIELLEICHT = 50  # darunter: liegen lassen


def punkte(bewertung: dict) -> int:
    """0-100.

    Ein nicht eingetragenes Kriterium bringt null Punkte - auch ein inverses.
    Sonst wuerde "Wettbewerb unbekannt" wie "kein Wettbewerb" zaehlen und jede
    unbewertete Idee saehe besser aus, als sie ist.
    """
    erreicht = summe = 0.0
    for name, k in KRITERIEN.items():
        summe += 5 * k["gewicht"]
        if name not in bewertung or bewertung[name] is None:
            continue
        wert = max(0, min(5, float(bewertung[name])))
        if k["invers"]:
            wert = 5 - wert
        erreicht += wert * k["gewicht"]
    return round(erreicht / summe * 100)


def urteil(p: int) -> str:
    if p >= GRENZE_BAUEN:
        return "bauen"
    if p >= GRENZE_VIELLEICHT:
        return "vielleicht"
    return "liegen lassen"


def begruendung(bewertung: dict) -> str:
    """Die eine Zahl, die das Urteil am staerksten zieht - hoch wie runter."""
    beitraege = []
    for name, k in KRITERIEN.items():
        if name not in bewertung or bewertung[name] is None:
            continue
        wert = max(0, min(5, float(bewertung[name])))
        roh = (5 - wert) if k["invers"] else wert
        # Abweichung vom Mittelwert 2.5, mit Gewicht
        beitraege.append(((roh - 2.5) * k["gewicht"], name, roh))
    if not beitraege:
        return "noch nicht bewertet"
    beitraege.sort(key=lambda x: abs(x[0]), reverse=True)
    abw, name, roh = beitraege[0]
    richtung = "traegt" if abw > 0 else "bremst"
    return f"{name} ({roh:.0f}/5) {richtung} am staerksten"

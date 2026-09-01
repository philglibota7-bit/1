"""Der Betriebsrhythmus.

Kein Tagesplan mit 90 Eintraegen - das haelt niemand durch. Stattdessen: ein
fester Wochentakt, der sich wiederholt, plus ein Schwerpunkt je Woche fuer die
ersten zwoelf Wochen. Danach laeuft der Takt einfach weiter.

`naechster_schritt` liest die echten Daten und sagt, woran es gerade hakt -
das ist ehrlicher als jeder starre Plan.
"""

from __future__ import annotations

from datetime import date

from . import bewertung, store

TAKT = [
    ("Montag", "Zahlen des Vormonats eintragen (nur am Monatsanfang), Bericht lesen"),
    ("Dienstag bis Donnerstag", "Am aktuellen Tool bauen - drei Bloecke, nicht mehr"),
    ("Freitag", "Inhaltstext des Tools schreiben oder verbessern"),
    ("Samstag", "Fuenf neue Ideen sammeln und bewerten"),
    ("Sonntag", "Frei. Ohne Ausnahme."),
]

WOCHEN = [
    (1, "Fundament", "tools.json mit echten Daten fuellen, build.py laufen lassen, "
                     "Impressum und Datenschutz pruefen"),
    (2, "Erstes Tool live", "bilder-verkleinern veroeffentlichen, bei Google Search "
                            "Console anmelden, Sitemap einreichen"),
    (3, "Ideen auf Vorrat", "20 Ideen sammeln und bewerten - nur so entsteht Auswahl"),
    (4, "Tool zwei", "Bestbewertete Idee bauen, gleiche Struktur wie Tool eins"),
    (5, "Sichtbarkeit", "Inhaltsteile aller Tools ueberarbeiten, untereinander verlinken"),
    (6, "Tool drei", "Bauen. Der Kern kostet inzwischen fast keine Zeit mehr"),
    (7, "Erste Zahlen", "Search Console auswerten: welche Suchbegriffe kommen an?"),
    (8, "Nachschaerfen", "Das Tool mit den meisten Aufrufen gezielt verbessern"),
    (9, "Bezahlung einrichten", "docs/BEZAHLUNG.md abarbeiten, Pro-Kauflink setzen"),
    (10, "Pro scharf schalten", "Pro-Funktionen im staerksten Tool aktivieren"),
    (11, "Tool vier", "Weiterbauen. Das Portfolio traegt, nicht das Einzelstueck"),
    (12, "Bilanz", "Was bringt Aufrufe? Was bringt Geld? Danach entscheiden"),
]


def woche_nummer(gestartet_am: str) -> int:
    try:
        start = date.fromisoformat(gestartet_am)
    except (ValueError, TypeError):
        return 1
    return max(1, (date.today() - start).days // 7 + 1)


def woche(nummer: int) -> tuple[int, str, str]:
    if nummer <= len(WOCHEN):
        return WOCHEN[nummer - 1]
    return (nummer, "Laufender Betrieb",
            "Alle zwei Wochen ein Tool, jede Woche fuenf Ideen, "
            "jeden Monat Zahlen und Entscheidung")


def naechster_schritt(db: dict) -> str:
    """Der ehrlichste Satz, den die Daten hergeben."""
    reg = store.registry()
    live = [t for t in reg.get("tools", []) if t.get("status") == "live"]
    marke = reg.get("marke", {})

    if "DEIN" in str(marke.get("betreiber", "")):
        return ("Impressum enthaelt noch Platzhalter. In tools.json eintragen und "
                "`python3 build.py` ausfuehren - ohne Impressum darf die Seite "
                "nicht oeffentlich sein.")

    bewertet = [i for i in db["ideen"] if i.get("status") in ("neu", "geprueft")]
    reif = [i for i in bewertet if i.get("punkte", 0) >= bewertung.GRENZE_BAUEN]

    if len(live) < 2:
        return ("Zweites Tool fehlt. Ein Portfolio faengt bei drei an - "
                "vorher ist es ein Einzelstueck und traegt kein Risiko.")
    if not reif:
        return (f"Keine Idee ueber {bewertung.GRENZE_BAUEN} Punkten in der Liste. "
                "Sammle fuenf neue und bewerte sie, bevor du weiterbaust.")

    if not db["monate"]:
        return ("Noch keine Zahlen erfasst. Ohne Messung raetst du - trage die "
                "Aufrufe des letzten Monats ein: `werkbank zahlen <slug> --besucher N`.")

    if "BEZAHLANBIETER" in str(marke.get("pro_kauflink", "")):
        umsatz = sum(m["umsatz_cent"] for m in db["monate"])
        besucher = sum(m["besucher"] for m in db["monate"])
        if besucher > 500 and umsatz == 0:
            return (f"{besucher} Aufrufe und kein Kauflink. Jetzt Bezahlung "
                    "einrichten - siehe docs/BEZAHLUNG.md.")

    beste = max(reif, key=lambda i: i["punkte"])
    return (f"Naechstes Tool bauen: \"{beste['titel']}\" "
            f"({beste['punkte']} Punkte, Idee {beste['id']}).")

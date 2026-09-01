"""Auswertung: was traegt, was kostet nur Zeit."""

from __future__ import annotations

from collections import defaultdict
from datetime import date
from html import escape

from . import store
from .geld import fmt

# Ab wann ein Tool als gescheitert gilt. Bewusst grosszuegig - SEO braucht
# Monate. Aber irgendwann muss man ein totes Tool auch tot nennen.
MINDEST_BESUCHER = 150
GNADENFRIST_MONATE = 6


def tausend(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def monat_heute() -> str:
    return date.today().strftime("%Y-%m")


def je_tool(db: dict) -> dict[str, dict]:
    """Summen je Tool ueber alle erfassten Monate."""
    summe: dict[str, dict] = defaultdict(
        lambda: {"besucher": 0, "kaeufe": 0, "umsatz_cent": 0, "monate": 0}
    )
    for m in db["monate"]:
        s = summe[m["slug"]]
        s["besucher"] += m["besucher"]
        s["kaeufe"] += m["kaeufe"]
        s["umsatz_cent"] += m["umsatz_cent"]
        s["monate"] += 1
    return dict(summe)


def empfehlung(werte: dict) -> str:
    """Skalieren, halten oder einstellen - die einzige Entscheidung, die zaehlt."""
    if werte["monate"] == 0:
        return "keine Daten"
    schnitt = werte["besucher"] / werte["monate"]
    if werte["umsatz_cent"] > 0 and schnitt >= MINDEST_BESUCHER:
        return "ausbauen"
    if schnitt >= MINDEST_BESUCHER:
        return "monetarisieren"
    if werte["monate"] >= GNADENFRIST_MONATE:
        return "einstellen"
    return "abwarten"


def letzter_monat(db: dict, monat: str) -> dict:
    eintraege = [m for m in db["monate"] if m["monat"] == monat]
    return {
        "besucher": sum(m["besucher"] for m in eintraege),
        "kaeufe": sum(m["kaeufe"] for m in eintraege),
        "umsatz_cent": sum(m["umsatz_cent"] for m in eintraege),
    }


def tafel_html(db: dict) -> str:
    """Eigenstaendige HTML-Datei. Landet in ~/.werkbank/, nicht im Repo."""
    reg = store.registry()
    titel = {t["slug"]: t["titel"] for t in reg.get("tools", [])}
    werte = je_tool(db)
    monat = monat_heute()
    aktuell = letzter_monat(db, monat)
    ziel = db["einstellungen"]["ziel_monat_cent"]
    anteil = min(100, round(aktuell["umsatz_cent"] / ziel * 100)) if ziel else 0

    farbe = {"ausbauen": "var(--gut)", "monetarisieren": "var(--warnung)",
             "einstellen": "var(--fehler)", "abwarten": "var(--text-leise)",
             "keine Daten": "var(--text-leise)"}

    zeilen = []
    for slug, w in sorted(werte.items(), key=lambda x: -x[1]["umsatz_cent"]):
        e = empfehlung(w)
        quote = f"{w['kaeufe'] / w['besucher'] * 100:.2f} %".replace(".", ",") if w["besucher"] else "–"
        zeilen.append(
            f"<tr><td>{escape(titel.get(slug, slug))}</td>"
            f"<td class='r'>{tausend(w['besucher'])}</td>"
            f"<td class='r'>{w['kaeufe']}</td>"
            f"<td class='r'>{quote}</td>"
            f"<td class='r'>{fmt(w['umsatz_cent'])}</td>"
            f"<td style='color:{farbe[e]};font-weight:600'>{e}</td></tr>"
        )
    if not zeilen:
        zeilen.append("<tr><td colspan='6' class='leise'>Noch keine Zahlen erfasst.</td></tr>")

    ideen = sorted(
        [i for i in db["ideen"] if i.get("status") in ("neu", "geprueft")],
        key=lambda i: -i.get("punkte", 0),
    )[:8]
    ideen_html = "".join(
        f"<tr><td>{i['id']}</td><td>{escape(i['titel'])}</td>"
        f"<td class='r'>{i.get('punkte', 0)}</td></tr>"
        for i in ideen
    ) or "<tr><td colspan='3' class='leise'>Keine offenen Ideen.</td></tr>"

    css = (store.repo() / "platform" / "werkbank.css").read_text(encoding="utf-8")

    return f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Werkbank – Tafel</title><style>{css}</style></head>
<body><main class="huelle" style="padding:2.5rem 1.25rem">
<h1>Tafel</h1>
<p class="fuehrung">Stand {date.today().strftime('%d.%m.%Y')} · Monat {monat}</p>

<div class="gitter" style="margin-bottom:2rem">
  <div class="karte"><span class="leise">Umsatz {monat}</span>
    <div style="font-size:1.8rem;font-weight:700">{fmt(aktuell['umsatz_cent'])} &euro;</div>
    <div style="height:6px;background:var(--flaeche-2);border-radius:3px;margin-top:.6rem">
      <div style="height:100%;width:{anteil}%;background:var(--akzent);border-radius:3px"></div>
    </div>
    <span class="leise">{anteil} % von {fmt(ziel)} &euro; Ziel</span></div>
  <div class="karte"><span class="leise">Aufrufe {monat}</span>
    <div style="font-size:1.8rem;font-weight:700">{tausend(aktuell['besucher'])}</div></div>
  <div class="karte"><span class="leise">Kaeufe {monat}</span>
    <div style="font-size:1.8rem;font-weight:700">{aktuell['kaeufe']}</div></div>
  <div class="karte"><span class="leise">Tools live</span>
    <div style="font-size:1.8rem;font-weight:700">
      {len([t for t in reg.get('tools', []) if t.get('status') == 'live'])}</div></div>
</div>

<h2>Portfolio</h2>
<table><thead><tr><th>Tool</th><th class="r">Aufrufe</th><th class="r">Kaeufe</th>
<th class="r">Quote</th><th class="r">Umsatz</th><th>Entscheidung</th></tr></thead>
<tbody>{''.join(zeilen)}</tbody></table>

<h2>Beste offene Ideen</h2>
<table><thead><tr><th>Nr.</th><th>Idee</th><th class="r">Punkte</th></tr></thead>
<tbody>{ideen_html}</tbody></table>
</main></body></html>
"""

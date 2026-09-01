#!/usr/bin/env python3
"""Baut aus tools.json alle Seiten, die sich aus der Registry ergeben.

    python3 build.py

Erzeugt: werkbank.html (Katalog), pro.html, impressum.html, datenschutz.html,
sitemap.xml, robots.txt.

Warum generiert statt handgeschrieben: Tool Nummer 20 soll nichts kosten.
Neues Tool -> Eintrag in tools.json -> build -> Katalog, Sitemap, Querverweise
und Pro-Seite sind aktuell. Genau das macht das Modell skalierbar.
"""

from __future__ import annotations

import json
import sys
from html import escape
from pathlib import Path

WURZEL = Path(__file__).parent
REGISTRY = WURZEL / "tools.json"

FAVICON = ("data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 32 32%27%3E"
           "%3Crect width=%2732%27 height=%2732%27 rx=%277%27 fill=%27%232b5cff%27/%3E"
           "%3Ctext x=%2716%27 y=%2723%27 font-size=%2719%27 font-family=%27sans-serif%27 "
           "font-weight=%27700%27 fill=%27white%27 text-anchor=%27middle%27%3EW%3C/text%3E%3C/svg%3E")



def laden() -> dict:
    if not REGISTRY.exists():
        sys.exit("tools.json fehlt.")
    with REGISTRY.open(encoding="utf-8") as f:
        d = json.load(f)
    for pflicht in ("marke", "tools"):
        if pflicht not in d:
            sys.exit(f"tools.json: '{pflicht}' fehlt.")
    return d


def live(tools: list[dict]) -> list[dict]:
    return [t for t in tools if t.get("status") == "live"]


def seite(marke: dict, titel: str, beschreibung: str, inhalt: str,
          slug: str = "", jsonld: str = "", kanonisch: str = "") -> str:
    """Gemeinsames HTML-Geruest fuer alle generierten Seiten (Tiefe 0)."""
    e = escape
    ld = f'<script type="application/ld+json">{jsonld}</script>' if jsonld else ""
    kan = f'<link rel="canonical" href="{e(kanonisch)}">' if kanonisch else ""
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titel)}</title>
<meta name="description" content="{e(beschreibung)}">
{kan}
<meta property="og:title" content="{e(titel)}">
<meta property="og:description" content="{e(beschreibung)}">
<meta property="og:type" content="website">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 32 32%27%3E%3Crect width=%2732%27 height=%2732%27 rx=%277%27 fill=%27%232b5cff%27/%3E%3Ctext x=%2716%27 y=%2723%27 font-size=%2719%27 font-family=%27sans-serif%27 font-weight=%27700%27 fill=%27white%27 text-anchor=%27middle%27%3EW%3C/text%3E%3C/svg%3E">\n<link rel="stylesheet" href="platform/werkbank.css">
{ld}
</head>
<body>
<main class="huelle" style="padding-top:2.5rem">
{inhalt}
</main>
<script src="platform/werkbank.js"></script>
<script>Werkbank.start({{ slug: {json.dumps(slug)} }});</script>
</body>
</html>
"""


def basispfad(marke: dict) -> str:
    """'https://name.github.io/1' -> '/1/'  ·  'https://eigene.de' -> '/'

    Die 404-Seite kann unter jeder beliebigen Tiefe ausgeliefert werden,
    relative Pfade greifen dort nicht. Deshalb wird der Basispfad hier aus
    der Domain abgeleitet, statt ihn irgendwo von Hand einzutragen.
    """
    ohne = marke["domain"].split("//", 1)[-1]
    rest = ohne.split("/", 1)
    return "/" + rest[1].strip("/") + "/" if len(rest) > 1 and rest[1].strip("/") else "/"


def nicht_gefunden(d: dict) -> str:
    m, b = d["marke"], basispfad(d["marke"])
    e = escape
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Seite nicht gefunden – {e(m['name'])}</title>
<meta name="robots" content="noindex">
<link rel="icon" href="{FAVICON}">
<link rel="stylesheet" href="{b}platform/werkbank.css">
</head>
<body>
<main class="huelle" style="padding-top:4rem">
  <h1>Diese Seite gibt es nicht</h1>
  <p class="fuehrung">Vielleicht wurde sie umbenannt, vielleicht hat sich ein
  Tippfehler in die Adresse geschlichen.</p>
  <p><a class="knopf" href="{b}werkbank.html">Zu allen Werkzeugen</a></p>
</main>
<script src="{b}platform/werkbank.js"></script>
<script>Werkbank.start({{ slug: "404" }});</script>
</body>
</html>
"""


def katalog(d: dict) -> str:
    marke, e = d["marke"], escape
    karten = []
    for t in live(d["tools"]):
        pro = ('<span class="marke-pro">Pro</span>' if t.get("pro") else "")
        karten.append(
            f'<a class="karte" href="{e(t["pfad"])}" '
            f'style="text-decoration:none;color:inherit;display:block">'
            f'<h3 style="margin:0 0 .4rem">{e(t["titel"])} {pro}</h3>'
            f'<p class="leise" style="margin:0">{e(t["kurz"])}</p></a>'
        )
    geplant = [t for t in d["tools"] if t.get("status") in ("idee", "gebaut")]
    geplant_html = ""
    if geplant:
        namen = ", ".join(e(t["titel"]) for t in geplant)
        geplant_html = (
            f'<h2>In Arbeit</h2><p class="leise">{namen}</p>'
        )

    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": marke["name"],
        "url": marke["domain"],
        "description": marke["beschreibung"],
    }, ensure_ascii=False)

    inhalt = f"""
<h1>{e(marke['name'])}</h1>
<p class="fuehrung">{e(marke['beschreibung'])} Keine Anmeldung, keine Uploads,
kein Warten – jedes Werkzeug arbeitet direkt auf deinem Rechner.</p>
<div class="gitter">{''.join(karten)}</div>
{geplant_html}
<div class="inhalt">
<h2>Warum ohne Upload?</h2>
<p>Die meisten Online-Werkzeuge schicken deine Datei auf einen fremden Server.
Das ist langsam, und du weisst nie, was dort damit passiert. Alle Werkbank-Tools
rechnen im Browser: die Datei verlaesst dein Geraet nicht. Das ist schneller,
funktioniert auch offline und du behaeltst die Kontrolle.</p>
<h2>Was kostet das?</h2>
<p>Die Werkzeuge selbst sind kostenlos und bleiben es. Wer sie beruflich nutzt
und die Zusatzfunktionen braucht – Stapelverarbeitung, zusaetzliche Formate,
Voreinstellungen – kauft einmal <a href="pro.html">Pro</a> fuer alle Tools.</p>
</div>
"""
    return seite(marke, f"{marke['name']} – {marke['beschreibung']}",
                 marke["beschreibung"], inhalt, "katalog", jsonld,
                 marke["domain"] + "/werkbank.html")


def pro_seite(d: dict) -> str:
    marke, e = d["marke"], escape
    zeilen = []
    for t in live(d["tools"]):
        if not t.get("pro"):
            continue
        punkte = "".join(f"<li>{e(p)}</li>" for p in t["pro"])
        zeilen.append(f'<h3>{e(t["titel"])}</h3><ul>{punkte}</ul>')
    if not zeilen:
        zeilen.append("<p class='leise'>Noch keine Pro-Funktionen veroeffentlicht.</p>")

    inhalt = f"""
<h1>Werkbank Pro</h1>
<p class="fuehrung">Einmal zahlen. Alle Pro-Funktionen in allen Werkzeugen,
auch in denen, die es noch gar nicht gibt.</p>

<div class="karte" style="max-width:26rem">
  <div style="font-size:2.5rem;font-weight:700;letter-spacing:-.03em">
    {e(marke.get('pro_preis','19'))} &euro;
    <span class="leise" style="font-size:1rem;font-weight:400">einmalig</span>
  </div>
  <p class="leise">Kein Abo. Keine Verlaengerung. Kein Konto noetig.</p>
  <a class="knopf" style="width:100%" href="{e(marke.get('pro_kauflink','#'))}">Pro kaufen</a>
  <p class="leise" style="margin-bottom:0">Du bekommst deinen Schluessel per E-Mail
  und traegst ihn im Tool ein.</p>
</div>

<h2>Enthalten</h2>
{''.join(zeilen)}

<div class="inhalt">
<h2>Schluessel eintragen</h2>
<p>Oeffne ein beliebiges Tool, klicke auf eine Pro-Funktion und trage den
Schluessel im Fenster ein. Er wird lokal in deinem Browser gespeichert.</p>
<details><summary>Auf mehreren Geraeten nutzbar?</summary>
<p>Ja. Trage denselben Schluessel auf jedem Geraet ein, das du selbst nutzt.</p></details>
<details><summary>Was, wenn ein Tool eingestellt wird?</summary>
<p>Die Datei laeuft ohne Server. Speichere die Seite lokal ab und sie
funktioniert weiter – auch ohne Internet.</p></details>
<details><summary>Rueckgabe</summary>
<p>Schreib innerhalb von 14 Tagen an
<a href="mailto:{e(marke['email'])}">{e(marke['email'])}</a>, du bekommst das Geld zurueck.</p></details>
</div>
"""
    return seite(marke, f"Pro – {marke['name']}",
                 f"Alle Pro-Funktionen aller {marke['name']}-Werkzeuge, einmalig "
                 f"{marke.get('pro_preis','19')} Euro.", inhalt, "pro", "",
                 marke["domain"] + "/pro.html")


def impressum(d: dict) -> str:
    m, e = d["marke"], escape
    ust = f"<p>Umsatzsteuer-Identifikationsnummer: {e(m['ust_id'])}</p>" if m.get("ust_id") else ""
    inhalt = f"""
<h1>Impressum</h1>
<p>Angaben gemaess &sect; 5 DDG (frueher &sect; 5 TMG).</p>
<h2>Diensteanbieter</h2>
<p>{e(m['betreiber'])}<br>{e(m['strasse'])}<br>{e(m['plz_ort'])}</p>
<h2>Kontakt</h2>
<p>E-Mail: <a href="mailto:{e(m['email'])}">{e(m['email'])}</a></p>
{ust}
<h2>Verantwortlich fuer den Inhalt</h2>
<p>{e(m['betreiber'])}, Anschrift wie oben.</p>
<h2>Streitbeilegung</h2>
<p>Wir sind nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren
vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
<p class="leise">Diese Seite wird aus <code>tools.json</code> erzeugt. Trage dort
deine echten Daten ein und fuehre <code>python3 build.py</code> aus.
Das ist eine Vorlage und keine Rechtsberatung.</p>
"""
    return seite(m, f"Impressum – {m['name']}", "Impressum und Anbieterkennzeichnung.",
                 inhalt, "impressum")


def datenschutz(d: dict) -> str:
    m, e = d["marke"], escape
    inhalt = f"""
<h1>Datenschutzerklaerung</h1>
<h2>Kurzfassung</h2>
<p>Alle Werkzeuge auf dieser Seite rechnen ausschliesslich in deinem Browser.
Dateien, die du hier oeffnest, werden <strong>nicht hochgeladen</strong> und
verlassen dein Geraet nicht.</p>

<h2>Verantwortlicher</h2>
<p>{e(m['betreiber'])}<br>{e(m['strasse'])}<br>{e(m['plz_ort'])}<br>
<a href="mailto:{e(m['email'])}">{e(m['email'])}</a></p>

<h2>Hosting</h2>
<p>Diese Seite wird bei GitHub Pages (GitHub, Inc.) gehostet. Beim Aufruf
uebertraegt dein Browser technisch notwendige Daten wie IP-Adresse, Zeitpunkt
und aufgerufene Seite an den Server. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f
DSGVO (berechtigtes Interesse am sicheren Betrieb der Seite).</p>

<h2>Lokale Speicherung</h2>
<p>Wir speichern in deinem Browser (localStorage): die gewaehlte Darstellung
(hell/dunkel), einen eventuell eingetragenen Pro-Schluessel sowie anonyme
Nutzungszaehler. Diese Angaben werden nicht an uns uebertragen. Du kannst sie
jederzeit ueber die Einstellungen deines Browsers loeschen.</p>

<h2>Keine Analyse-Dienste</h2>
<p>Es sind keine Analyse- oder Werbedienste eingebunden. Es werden keine Cookies
zu Analyse- oder Marketingzwecken gesetzt.</p>

<h2>Deine Rechte</h2>
<p>Du hast das Recht auf Auskunft, Berichtigung, Loeschung, Einschraenkung der
Verarbeitung, Datenuebertragbarkeit und Widerspruch sowie ein Beschwerderecht
bei einer Aufsichtsbehoerde.</p>

<p class="leise">Diese Seite wird aus <code>tools.json</code> erzeugt. Sie ist eine
Vorlage und keine Rechtsberatung. Sobald du Bezahldienste, Newsletter oder
Analysewerkzeuge einbindest, muss sie erweitert werden.</p>
"""
    return seite(m, f"Datenschutz – {m['name']}",
                 "Datenschutzerklaerung. Alle Werkzeuge rechnen im Browser.",
                 inhalt, "datenschutz")


def sitemap(d: dict) -> str:
    """Bewusst ohne lastmod.

    Ein Datum vom Tag des Erzeugens waere jeden Tag ein anderes - die
    Pruefung "erzeugte Seiten sind aktuell" wuerde dann taeglich fehlschlagen,
    ohne dass sich etwas geaendert hat. Suchmaschinen werten lastmod ohnehin
    nur schwach.
    """
    basis = d["marke"]["domain"].rstrip("/")
    eintraege = ["werkbank.html", "pro.html", "impressum.html", "datenschutz.html"]
    eintraege += [t["pfad"] for t in live(d["tools"])]
    zeilen = "".join(f"  <url><loc>{basis}/{p}</loc></url>\n" for p in eintraege)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{zeilen}</urlset>\n")


def robots(d: dict) -> str:
    basis = d["marke"]["domain"].rstrip("/")
    return f"User-agent: *\nAllow: /\n\nSitemap: {basis}/sitemap.xml\n"


def main() -> None:
    d = laden()
    dateien = {
        "werkbank.html": katalog(d),
        "pro.html": pro_seite(d),
        "impressum.html": impressum(d),
        "datenschutz.html": datenschutz(d),
        "404.html": nicht_gefunden(d),
        "sitemap.xml": sitemap(d),
        "robots.txt": robots(d),
    }
    for name, text in dateien.items():
        (WURZEL / name).write_text(text, encoding="utf-8")
        print(f"  geschrieben  {name}")
    print(f"\n{len(live(d['tools']))} Tools im Katalog.")
    if "DEIN" in d["marke"]["betreiber"]:
        print("\nACHTUNG: Impressum enthaelt noch Platzhalter. In Deutschland ist "
              "ein vollstaendiges Impressum Pflicht, sobald die Seite oeffentlich ist.")


if __name__ == "__main__":
    main()

"""Baut squelly-v2.html aus Vorlage, Skript, Schriften und Bildern.

Die Bilder und alle Zahlen kommen unverändert aus squelly.html — v2 ist ein
anderer Aufbau derselben geprüften Angaben, keine neue Behauptung. Neu sind
nur Kategorie und Akzentfarbe je Produkt; beide beschreiben nichts am
Produkt, sie sortieren und färben nur.
"""
import json
import os
import re

HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.abspath(os.path.join(HIER, '..', '..'))
V1 = open(os.path.join(WURZEL, 'squelly.html'), encoding='utf-8').read()

# Schriften und Produktfotos kommen unveraendert aus v1 — beide sind dort
# schon als Daten eingebettet, ein zweites Mal beschaffen waere Unsinn.
SCHRIFTEN = "\n".join(re.findall(r'@font-face\{[^}]*\}', V1))
_blk = V1[V1.find('const PRODUKTE'):V1.find('\n];', V1.find('const PRODUKTE'))]
BILDER = dict(zip(re.findall(r'kuerzel:\s*"([^"]+)"', _blk),
                  re.findall(r'bild:\s*"(data:[^"]+)"', _blk)))
assert len(BILDER) == 4, BILDER.keys()

LOGO = ('<g clip-path="url(#lc)"><rect width="200" height="360" fill="#fff"/>'
        '<g fill="none" stroke="#3a8ccd" stroke-linecap="round">'
        '<use href="#la" x="18" stroke-width="26"/><use href="#lb" x="72" stroke-width="17"/>'
        '<use href="#la" x="118" stroke-width="34"/><use href="#lb" x="176" stroke-width="21"/></g>'
        '<g fill="none" stroke="#14315c" stroke-width="5">'
        '<use href="#la" x="2"/><use href="#lb" x="38"/><use href="#la" x="72"/>'
        '<use href="#lb" x="110"/><use href="#la" x="146"/><use href="#lb" x="184"/></g></g>'
        '<rect x="1" y="1" width="198" height="358" rx="2" fill="none" stroke="#14315c" '
        'stroke-width="4"/>'
        '<defs><clipPath id="lc"><rect x="1" y="1" width="198" height="358" rx="2"/></clipPath>'
        '<path id="la" d="M0,-30 C40,52 -32,104 14,168 C56,230 -16,276 20,340 C38,376 6,388 '
        '12,412"/><path id="lb" d="M0,-30 C22,60 -44,96 8,164 C44,226 -28,268 14,336 C30,372 '
        '-2,384 6,412"/></defs>')

HAKEN = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>')
SIEGEL = "".join('<span>%s%s</span>' % (HAKEN, t) for t in [
    "Angaben der Hersteller, nichts erfunden",
    "Preisverlauf und Tiefpreis-Marke",
    "Wunschpreis-Alarm im Browser",
    "Anzeige · Amazon-Partner",
])

PRODUKTE = [
    dict(
        name="Kabelloser Handvakuumierer mit 30 Beuteln",
        marke="Küchenhelfer", kat="Küche", kuerzel="vakuumierer",
        suche="kabelloser Handvakuumierer Beutel USB-C", asin="",
        akzent="#4aa3e0", wirkung="sog",
        alt="Weißer Handvakuumierer neben zwei vakuumierten Beuteln mit Mandeln und "
            "Limettenscheiben sowie frischem Gemüse",
        fakten=["Hält Lebensmittel laut Hersteller bis zu fünfmal länger frisch",
                "Ein Knopf, ein Beutel — versiegelt in etwa fünf Sekunden",
                "30 wiederverwendbare, BPA-freie Beutel und ein Clip liegen bei",
                "Akkubetrieben, wird per USB-C geladen"],
        warum="Der Nutzen ist sofort sichtbar: angebrochenes Gemüse hält, statt zu welken.",
        verlauf=[("2026-05-16", 39.99), ("2026-06-05", 39.99), ("2026-06-24", 37.49),
                 ("2026-07-08", 34.99), ("2026-07-21", 36.99), ("2026-08-01", 34.99),
                 ("2026-08-08", 32.99), ("2026-08-13", 29.99)],
    ),
    dict(
        name="Mini-Massagepistole mit neun Aufsätzen",
        marke="Erholung", kat="Erholung", kuerzel="massagepistole",
        suche="Mini Massagepistole Massage Gun Aufsätze USB-C", asin="",
        akzent="#8b94f7", wirkung="impuls",
        alt="Graue Mini-Massagepistole mit Kugelaufsatz, daneben neun weitere Aufsätze "
            "und die Verpackung",
        fakten=["Neun Aufsätze für Nacken, Schultern, Rücken, Waden und Arme",
                "Ladestandsanzeige am Boden, Anschluss per USB-C",
                "Klein genug für Schreibtischschublade oder Sporttasche",
                "Mehrere Intensitätsstufen über eine einzige Taste"],
        warum="Die großen Geräte kennt jeder. Die Taschenversion für den Büronacken kaum jemand.",
        verlauf=[("2026-05-16", 54.99), ("2026-06-05", 52.99), ("2026-06-24", 49.99),
                 ("2026-07-08", 49.99), ("2026-07-21", 47.99), ("2026-08-01", 46.99),
                 ("2026-08-08", 47.99), ("2026-08-13", 49.99)],
    ),
    dict(
        name="Sunset Projector — Tischlampe mit Sonnenuntergangs-Licht",
        marke="Pursonic", kat="Zuhause", kuerzel="lampe",
        suche="Pursonic Sunset Projector Table Lamp Sonnenuntergang Lampe", asin="",
        akzent="#ff9d55", wirkung="licht",
        farben=["#ff7a3d", "#ff4d6d", "#c94bd0", "#7a5cf0", "#3aa0ff", "#2fd0c4"],
        alt="Schwarze Sunset-Projektor-Tischlampe neben ihrer Verpackung",
        fakten=["16 Farben zur Auswahl, vier Lichtmodi",
                "Fernbedienung liegt bei",
                "Kopf um 180 Grad schwenkbar — Licht an Wand oder Decke",
                "Stromversorgung über USB"],
        warum="Kostet wenig, verändert einen Raum sofort — und sieht auf Fotos "
              "außergewöhnlich gut aus.",
        verlauf=[("2026-05-16", 29.99), ("2026-06-05", 27.99), ("2026-06-24", 26.99),
                 ("2026-07-08", 24.99), ("2026-07-21", 24.99), ("2026-08-01", 23.99),
                 ("2026-08-08", 22.99), ("2026-08-13", 22.99)],
    ),
    dict(
        name="Kompakte elektrische Luftpumpe mit Digitalanzeige",
        marke="AstroAI", kat="Fahrrad", kuerzel="pumpe",
        suche="AstroAI elektrische Luftpumpe kompakt Fahrrad E-Bike Auto", asin="",
        akzent="#3fcfb4", wirkung="druck",
        alt="Kompakte schwarze elektrische Luftpumpe von AstroAI mit Digitalanzeige "
            "und Bedienkreuz",
        fakten=["Wunschdruck vorwählen — sie schaltet beim Zielwert selbst ab",
                "Für Fahrrad, E-Bike und Auto",
                "LED-Licht eingebaut, für die Panne nach Sonnenuntergang",
                "439 g, 13,4 x 6,6 x 5 cm — passt in jede Satteltasche"],
        warum="Die Standpumpe steht im Keller. Der platte Reifen steht am Bahnhof.",
        verlauf=[("2026-05-16", 30.99), ("2026-06-05", 30.99), ("2026-06-24", 28.99),
                 ("2026-07-08", 27.49), ("2026-07-21", 28.99), ("2026-08-01", 26.99),
                 ("2026-08-08", 25.49), ("2026-08-13", 23.86)],
    ),
]

for p in PRODUKTE:
    p["bild"] = BILDER[p["kuerzel"]]
    p["verlauf"] = [{"d": t, "p": w} for t, w in p["verlauf"]]

TEXTE = {
    "affiliate": ["Affiliate-Hinweis",
        "<p><b>Als Amazon-Partner verdienen wir an qualifizierten Verkäufen.</b></p>"
        "<p>Diese Seite enthält Werbelinks. Kaufst du über einen solchen Link bei Amazon ein, "
        "erhalten wir eine Provision vom Händler. <b>Für dich ändert sich der Preis nicht</b> — "
        "du zahlst denselben Betrag wie ohne Link.</p>"
        "<p>Welche Produkte hier stehen, entscheiden wir nach eigener Einschätzung, nicht nach "
        "der Höhe der Provision. Amazon und das Amazon-Logo sind Marken von Amazon.com, Inc. "
        "oder seinen verbundenen Unternehmen.</p>"],
    "quellen": ["Woher die Angaben stammen",
        "<p>Die Merkmale stammen aus den Angaben der Hersteller und von den Produkt"
        "verpackungen. Wir haben die Geräte nicht selbst getestet — wo wir eine Hersteller"
        "angabe wiedergeben, steht das ausdrücklich dabei.</p>"
        "<p><b>Zu den Preisen.</b> Neben jedem Produkt steht der Preis der letzten Messung "
        "samt Datum, dazu die Veränderung zur Messung davor und der Verlauf der letzten "
        "Monate. Amazon ändert Preise oft mehrmals am Tag — zwischen unserer Messung und "
        "deinem Klick kann sich der Betrag also geändert haben.</p>"
        "<p>Wer als Partner Preise anzeigt, muss sie über die offizielle Produkt-Schnittstelle "
        "beziehen und regelmäßig erneuern. Solange auf der Seite <b>Beispielpreis</b> steht, "
        "sind die Zahlen Platzhalter zum Ausprobieren der Funktion und keine echten "
        "Marktpreise.</p>"
        "<p><b>Zur Tiefpreis-Marke.</b> „Tiefpreis“ heißt: der aktuelle Wert ist der "
        "niedrigste im gezeigten Verlauf. Über die Zeit davor sagt er nichts.</p>"],
    "datenschutz": ["Datenschutz",
        "<p>Diese Seite läuft ohne Server und ohne Konto. Es gibt keine Zählpixel und keine "
        "Werbenetzwerke.</p>"
        "<p><b>Wunschpreise</b> legen wir in <b>localStorage</b> deines Browsers ab, damit sie "
        "einen Neustart überstehen. Sie verlassen dein Gerät nicht.</p>"
        "<p><b>Herkunft.</b> Rufst du die Seite über eine Anzeige auf, stehen Angaben wie "
        "<b>utm_source</b> in der Adresse. Wir merken sie uns im <b>sessionStorage</b> deines "
        "Browsers und hängen sie an den Amazon-Link an, damit wir sehen, welche Anzeige "
        "gewirkt hat. Mit dem Schließen des Tabs ist das weg.</p>"
        "<p><b>Benachrichtigungen</b> fragen wir erst, wenn du einen Wunschpreis setzt. Sagst "
        "du nein, funktioniert alles weiter — die Meldung erscheint dann nur auf der Seite.</p>"
        "<p>Beim Klick auf Amazon gelten deren Bestimmungen.</p>"],
    "impressum": ["Impressum",
        "<p><b>Angaben gemäß § 5 DDG</b></p>"
        "<p>Vorname Nachname<br>Straße Hausnummer<br>PLZ Ort<br>Deutschland</p>"
        "<p>E-Mail: kontakt@example.de</p>"
        "<p><b>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV:</b> wie oben.</p>"
        "<p>Diese Felder sind Platzhalter und müssen vor einer Veröffentlichung durch echte "
        "Angaben ersetzt werden.</p>"],
}

fonts = SCHRIFTEN
skript = open(os.path.join(HIER, 'skript.js'), encoding='utf-8').read()
skript = skript.replace('/*DATEN*/', json.dumps(PRODUKTE, ensure_ascii=False))
skript = skript.replace('/*TEXTE*/', json.dumps(TEXTE, ensure_ascii=False))

seite = open(os.path.join(HIER, 'vorlage.html'), encoding='utf-8').read()
seite = (seite.replace('/*FONTS*/', fonts)
              .replace('<!--LOGO-->', LOGO)
              .replace('<!--SIEGEL-->', SIEGEL)
              .replace('/*SKRIPT*/', skript))

# Kontrolle: keine Platzhalter mehr, kein Bild vergessen
for rest in ('/*FONTS*/', '<!--LOGO-->', '<!--SIEGEL-->', '/*SKRIPT*/', '/*DATEN*/', '/*TEXTE*/'):
    assert rest not in seite, 'Platzhalter geblieben: ' + rest
assert seite.count('data:image/webp') >= 4, 'Bild fehlt'

open(os.path.join(WURZEL, 'squelly-v2.html'), 'w', encoding='utf-8').write(seite)
print('squelly-v2.html', round(len(seite) / 1024), 'KB,', len(PRODUKTE), 'Produkte')

"""Baut den Ausspielplan aus den vorhandenen Motiven.

Der Plan ist die einzige Wahrheit für das Posten: welche Datei, auf welchen
Kanal, mit welchem Text und unter welcher Adresse. Motive ohne Text kommen
mit rein, aber als unfertig markiert — posten.mjs weigert sich dann, sie
auszuspielen, statt eine leere Beschreibung hochzuladen.
"""
import json
import os

HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.abspath(os.path.join(HIER, '..', '..'))

# Wohin die Bilder zeigen, sobald sie öffentlich liegen. Instagram und
# Pinterest laden die Datei selbst herunter — ein Pfad auf der Festplatte
# nützt ihnen nichts, die Adresse muss von außen erreichbar sein.
BILDBASIS = "https://philglibota7-bit.github.io/1/"
SEITE = "https://philglibota7-bit.github.io/1/squelly.html"
KAMPAGNE = "Herbst Start"

HINWEIS = "Anzeige · Als Amazon-Partner verdienen wir an qualifizierten Verkäufen."


def kurz(v, n=12):
    s = "".join(c for c in str(v or "").lower() if c.isalnum())
    return s[:n]


def adresse(inhalt, quelle, medium):
    return (SEITE + "?utm_source=" + quelle + "&utm_medium=" + medium +
            "&utm_campaign=" + KAMPAGNE.replace(" ", "%20") +
            "&utm_content=" + inhalt)


def subid(inhalt, quelle, kuerzel):
    return "-".join(["sq", kurz(quelle), kurz(KAMPAGNE, 16) or "ohne",
                     kurz(inhalt, 22), kuerzel])[:100]


# ── Die neun Pumpen-Pins: Texte stehen schon, aus pin-texte.html ──────────
PUMPE = [
    (1, "nachtfahrt", "Fahrrad & Pendeln",
     "Panne um halb zehn? Diese Mini-Luftpumpe hat ihr Licht schon dabei",
     "Im Dunkeln hilft kein Gefühl im Daumen. Die kompakte elektrische Luftpumpe von "
     "AstroAI hat ein LED eingebaut und leuchtet dir das Ventil aus, während sie pumpt. "
     "Wunschdruck vorher einstellen — beim Zielwert schaltet sie von allein ab. 439 g, "
     "13,4 x 6,6 x 5 cm, für Fahrrad, E-Bike und Auto.",
     "Kompakte schwarze elektrische Luftpumpe mit leuchtender Digitalanzeige in einem "
     "Lichtkegel vor dunkelblauem Hintergrund"),
    (2, "riss", "Fahrradzubehör",
     "13,4 x 6,6 x 5 cm: die Luftpumpe, die in jede Satteltasche passt",
     "Maßblatt statt Werbespruch: 13,4 cm lang, 6,6 cm breit, 5 cm tief, 439 g schwer. "
     "Das ist die ganze elektrische Luftpumpe — mit Digitalanzeige, Druckvorwahl und "
     "eingebautem LED-Licht. Sie ersetzt die Standpumpe im Keller und nimmt in der "
     "Satteltasche kaum Platz weg.",
     "Technische Zeichnung einer kompakten elektrischen Luftpumpe mit Maßlinien für 13,4 "
     "mal 6,6 mal 5 Zentimeter auf blauem Millimeterraster"),
    (3, "schnitt", "Fahrrad & Pendeln",
     "Nie wieder treten: Knopf drücken statt Standpumpe schleppen",
     "Treten, bis der Arm brennt — das war die alte Art, den Reifen vollzukriegen. Bei "
     "dieser elektrischen Luftpumpe stellst du den Wunschdruck ein, drückst einen Knopf "
     "und sie schaltet beim Zielwert selbst ab. Der Motor macht die Arbeit, du hältst "
     "nur. Für Fahrrad, E-Bike und Auto.",
     "Geteiltes Bild: oben durchgestrichen die alte Handpumpen-Mühe, unten die "
     "elektrische Luftpumpe auf blauem Grund"),
    (4, "plakat", "Fahrradzubehör",
     "439 Gramm — so wenig wiegt der Ersatz für deine Standpumpe",
     "Weniger als eine volle Trinkflasche, und trotzdem pumpt sie Fahrrad, E-Bike und "
     "Auto auf. 13,4 cm lang, Digitalanzeige mit Druckvorwahl, LED-Licht eingebaut, "
     "4,5 Sterne bei über 10.000 Käufen. Die Standpumpe darf im Keller bleiben.",
     "Plakat mit der großen Zahl 439 Gramm und der kompakten elektrischen Luftpumpe in "
     "einem dünnen Kreis auf cremefarbenem Grund"),
    (5, "anleitung", "Fahrrad reparieren",
     "Reifen voll in drei Schritten — ohne Muskelkraft",
     "1. Ventilkopf aufschrauben, egal ob Fahrrad, E-Bike oder Auto. 2. Wunschdruck an "
     "der Digitalanzeige vorwählen. 3. Knopf drücken — sie pumpt und schaltet beim "
     "Zielwert selbst ab. Kein Nachmessen, kein Treten. 439 g, passt in die "
     "Satteltasche, LED-Licht ist eingebaut.",
     "Anleitung in drei nummerierten Schritten neben einem Foto der kompakten "
     "elektrischen Luftpumpe"),
    (6, "plaetze", "Fahrrad & Pendeln",
     "Drei Plätze, an denen die Mini-Luftpumpe einfach mitfährt",
     "Am Rahmen in der Halterung, in der Satteltasche, im Rucksack — bei 13,4 cm und "
     "439 g stört sie nirgends. Genau deshalb ist sie dabei, wenn der Reifen leer ist, "
     "und nicht zu Hause im Keller. Digitalanzeige mit Druckvorwahl, Abschaltautomatik, "
     "LED-Licht, für Fahrrad, E-Bike und Auto.",
     "Drei Fotos untereinander: die Luftpumpe in der Rahmenhalterung, auf dem Weg in "
     "eine Satteltasche und in einen Rucksack"),
    (7, "groesse", "Fahrradzubehör",
     "Kaum größer als dein Handy: elektrische Luftpumpe für unterwegs",
     "Ein Foto beantwortet die Größenfrage schneller als jede Zahl — die Pumpe steht "
     "neben einem Smartphone und überragt es kaum. 13,4 x 6,6 x 5 cm, 439 g. Und sie "
     "ersetzt trotzdem die Standpumpe: Wunschdruck einstellen, sie pumpt und schaltet "
     "beim Zielwert selbst ab.",
     "Die kompakte elektrische Luftpumpe steht neben einem Smartphone und ist kaum "
     "größer als dieses"),
    (8, "szene", "Fahrrad & Pendeln",
     "Sie wartet am Rad, nicht im Keller",
     "In der Halterung am Rahmen fährt die elektrische Luftpumpe einfach mit — dort, wo "
     "der platte Reifen passiert, und nicht dort, wo die Standpumpe steht. Druck "
     "vorwählen, sie schaltet beim Zielwert selbst ab. LED-Licht eingebaut, für "
     "Fahrrad, E-Bike und Auto, 439 g.",
     "Die kompakte elektrische Luftpumpe steckt in ihrer Halterung am Rahmen eines "
     "Fahrrads"),
    (9, "tafel", "Fahrrad reparieren",
     "Was eine elektrische Mini-Luftpumpe dir im Alltag abnimmt",
     "Ein Gerät statt drei Pumpen im Haus: Fahrrad, E-Bike und Auto. Wunschdruck "
     "vorwählen, sie schaltet beim Zielwert selbst ab — kein Nachmessen. LED-Licht für "
     "die Panne im Dunkeln. 439 Gramm, weniger als eine volle Trinkflasche, und sie "
     "verschwindet in der Satteltasche.",
     "Foto einer Hand, die die Luftpumpe in eine Satteltasche steckt, darunter vier "
     "Kacheln mit ihren Aufgaben"),
]

# ── Motive ohne fertigen Text: kommen als unfertig in den Plan ───────────
OFFEN = [
    ("werbemittel/pinterest/squelly-%s-pin-%s-1000x1500.png" % (p, b),
     "%s-pin-%s" % (p, b), k, "pin")
    for p, k in [("vakuumierer", "vakuumierer"), ("massagepistole", "massagepistole"),
                 ("lampe", "lampe")]
    for b in ["plakat", "anleitung", "karte"]
] + [
    ("werbemittel/fahrradpumpe/squelly-fahrradpumpe-%s-1080x1080.png" % v,
     "fahrradpumpe-%s" % v, "pumpe", "feed")
    for v in ["a-tempo", "b-lieferumfang", "c-ventile", "d-gespiegelt", "e-zahlen"]
] + [
    ("werbemittel/squelly-%s-%s.png" % (d, m), "%s-%s" % (d, f), k, "feed")
    for d, k in [("vakuumierer", "vakuumierer"), ("massagepistole", "massagepistole"),
                 ("sunset-lampe", "lampe")]
    for m, f in [("1080x1080", "quad"), ("1080x1350", "hoch")]
]

PLAN = []

for nr, name, brett, titel, text, alt in PUMPE:
    datei = "werbemittel/fahrradpumpe/pinterest/squelly-pumpe-pin-%d-%s-1000x1500.png" % (nr, name)
    inhalt = "pumpe-pin-%d-%s" % (nr, name)
    PLAN.append({
        "id": inhalt,
        "datei": datei,
        "bild": BILDBASIS + datei,
        "kanaele": ["pinterest"],
        "brett": brett,
        "titel": titel,
        "text": text + " " + HINWEIS,
        "alt": alt,
        "link": adresse(inhalt, "pinterest", "pin"),
        "subid": subid(inhalt, "pinterest", "pumpe"),
        "fertig": True,
    })

for datei, inhalt, kuerzel, art in OFFEN:
    quelle, medium = ("pinterest", "pin") if art == "pin" else ("instagram", "organisch")
    PLAN.append({
        "id": inhalt,
        "datei": datei,
        "bild": BILDBASIS + datei,
        "kanaele": ["pinterest"] if art == "pin" else ["instagram", "facebook"],
        "brett": None,
        "titel": None,
        "text": None,
        "alt": None,
        "link": adresse(inhalt, quelle, medium),
        "subid": subid(inhalt, quelle, kuerzel),
        "fertig": False,
    })

fehlt = [e["datei"] for e in PLAN if not os.path.exists(os.path.join(WURZEL, e["datei"]))]
assert not fehlt, "Diese Dateien gibt es nicht: " + ", ".join(fehlt)

with open(os.path.join(HIER, 'plan.json'), 'w', encoding='utf-8') as f:
    json.dump(PLAN, f, ensure_ascii=False, indent=2)
    f.write("\n")

fertig = sum(1 for e in PLAN if e["fertig"])
print("plan.json:", len(PLAN), "Motive,", fertig, "mit Text,", len(PLAN) - fertig, "noch ohne")

import json
d = '/tmp/claude-0/-home-user-1/d9dd5cf6-a597-547e-95fb-a98c3cc3ca25/scratchpad/'
N = json.load(open(d + 'pumpe-nutzung.json'))

# Ausschnitte aus der A+-Tafel des Herstellers. Alle Angaben stammen von der
# amazon.de-Produktseite: 439 g, 13,4 x 6,6 x 5 cm, Digitalanzeige mit
# Druckvorwahl und Abschaltautomatik, eingebautes LED-Licht, passt an den
# Fahrradrahmen, fuer Fahrrad, E-Bike und Auto, 4,5 Sterne, 10.000+ gekauft.
ALT = {
    'rahmen':  "Die Luftpumpe steckt in der Halterung am Fahrradrahmen",
    'tasche':  "Eine Hand steckt die Luftpumpe in die Satteltasche am Rad",
    'rucksack': "Eine Hand steckt die Luftpumpe in einen Rucksack",
    'groesse': "Die Luftpumpe steht neben einem Smartphone und ist kaum größer",
}


def logo(hell=False):
    strich = "#fff" if hell else "#14315c"
    return ('<svg class="logo" viewBox="0 0 200 360" aria-hidden="true">'
            '<g clip-path="url(#lc)"><rect width="200" height="360" fill="#fff"/>'
            '<g fill="none" stroke="#3a8ccd" stroke-linecap="round">'
            '<use href="#la" x="18" stroke-width="26"/><use href="#lb" x="72" stroke-width="17"/>'
            '<use href="#la" x="118" stroke-width="34"/><use href="#lb" x="176" stroke-width="21"/></g>'
            '<g fill="none" stroke="#14315c" stroke-width="5">'
            '<use href="#la" x="2"/><use href="#lb" x="38"/><use href="#la" x="72"/>'
            '<use href="#lb" x="110"/><use href="#la" x="146"/><use href="#lb" x="184"/></g></g>'
            '<rect x="1" y="1" width="198" height="358" rx="2" fill="none" stroke="%s" '
            'stroke-width="4"/></svg>' % strich)


DEFS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
        '<clipPath id="lc"><rect x="1" y="1" width="198" height="358" rx="2"/></clipPath>'
        '<path id="la" d="M0,-30 C40,52 -32,104 14,168 C56,230 -16,276 20,340 C38,376 6,388 12,412"/>'
        '<path id="lb" d="M0,-30 C22,60 -44,96 8,164 C44,226 -28,268 14,336 C30,372 -2,384 6,412"/>'
        '</defs></svg>')

PFEIL = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')
HAKEN = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>')
HINWEIS = "Anzeige · Als Amazon-Partner verdienen wir an qualifizierten Verkäufen."
KNOPF = 'Preis auf Amazon prüfen ' + PFEIL


def foto(name, klasse="foto"):
    return '<img class="%s" src="%s" alt="%s">' % (klasse, N[name], ALT[name])


PINS = []

# ── 6 · Drei Plätze ─────────────────────────────────────────────────────────
plaetze = "".join(
    '<div class="platz">%s<div><b>%s</b><p>%s</p></div></div>' % (foto(bild), titel, text)
    for bild, titel, text in [
        ("rahmen", "Am Rahmen",
         "In der Halterung fährt sie einfach mit — du musst nie daran denken."),
        ("tasche", "In der Satteltasche",
         "13,4 cm lang, 439 g schwer. Sie nimmt kaum Platz weg."),
        ("rucksack", "Im Rucksack",
         "Für den Weg zur Arbeit, ins Wochenende, in den Urlaub."),
    ])
PINS.append(('u1', '''
  <div class="kopf">%(logo)s<span class="wm">SQUELLY</span><span class="marke">Fahrrad</span></div>
  <h1>Drei Plätze, an<br>denen sie <em>mitfährt.</em></h1>
  %(plaetze)s
  <div class="fuss">
    <div class="knopf">%(knopf)s</div>
    <p class="klein">%(hinweis)s</p>
  </div>''' % dict(logo=logo(), plaetze=plaetze, knopf=KNOPF, hinweis=HINWEIS)))

# ── 7 · Größenvergleich ─────────────────────────────────────────────────────
PINS.append(('u2', '''
  %(bild)s
  <div class="kopf">%(logo)s<span class="wm">SQUELLY</span></div>
  <span class="marke">GRÖSSENVERGLEICH</span>
  <h1>Kaum größer<br>als dein <em>Handy.</em></h1>
  <p class="unter">13,4 × 6,6 × 5 cm, 439 g — und sie ersetzt die Standpumpe,
     die im Keller steht.</p>
  <div class="fuss">
    <span class="knopf">%(knopf)s</span>
    <p class="klein">%(hinweis)s</p>
  </div>''' % dict(bild=foto('groesse'), logo=logo(True), knopf=KNOPF, hinweis=HINWEIS)))

# ── 8 · Szene am Rad ────────────────────────────────────────────────────────
zeilen = "".join('<div>%s<span>%s</span></div>' % (HAKEN, z) for z in [
    "Druck vorwählen — sie schaltet beim Zielwert selbst ab",
    "LED-Licht eingebaut, für die Panne nach Sonnenuntergang",
    "Ein Gerät für Fahrrad, E-Bike und Auto",
])
PINS.append(('u3', '''
  <div class="buehne">%(bild)s</div>
  <div class="schleier"></div><div class="oben"></div>
  <div class="kopf">%(logo)s<span class="wm">SQUELLY</span><span class="marke">Fahrrad</span></div>
  <h1>Sie wartet am Rad,<br>nicht <em>im Keller.</em></h1>
  <div class="zeilen">%(zeilen)s</div>
  <div class="fuss">
    <div class="knopf">%(knopf)s</div>
    <p class="klein">%(hinweis)s</p>
  </div>''' % dict(bild=foto('rahmen'), logo=logo(True), zeilen=zeilen,
                   knopf=KNOPF, hinweis=HINWEIS)))

# ── 9 · Was sie tut ─────────────────────────────────────────────────────────
kacheln = "".join('<div><b>%s</b><span>%s</span></div>' % (k, v) for k, v in [
    ("Fahrrad, E-Bike, Auto", "Ein Gerät statt drei Pumpen im Haus"),
    ("Druck vorwählen", "Wert einstellen, sie schaltet selbst ab"),
    ("LED-Licht", "Eingebaut, für die Panne im Dunkeln"),
    ("439 Gramm", "Weniger als eine volle Trinkflasche"),
])
PINS.append(('u4', '''
  <div class="kopf">%(logo)s<span class="wm">SQUELLY</span><span class="marke">Fahrrad</span></div>
  <h1>Was sie im<br><em>Alltag</em> abnimmt.</h1>
  <div class="bild">%(bild)s</div>
  <div class="kacheln">%(kacheln)s</div>
  <div class="fuss">
    <span class="knopf">%(knopf)s</span>
    <p class="klein">%(hinweis)s</p>
  </div>''' % dict(logo=logo(), bild=foto('tasche'), kacheln=kacheln,
                   knopf=KNOPF, hinweis=HINWEIS)))

teile = [DEFS]
for pid, inhalt in PINS:
    teile.append('<div class="cap">%s</div><div class="pin" id="%s">%s</div>' % (pid, pid, inhalt))

tpl = open(d + 'pin4.template.html', encoding='utf-8').read()
out = tpl.replace('/*FONTS*/', open(d + 'fonts.css', encoding='utf-8').read()) \
         .replace('<!--PINS-->', "\n".join(teile))
open(d + 'pin4.html', 'w', encoding='utf-8').write(out)
print('pin4.html', round(len(out) / 1024), 'KB')

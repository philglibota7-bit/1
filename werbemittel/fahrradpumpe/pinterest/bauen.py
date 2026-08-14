import json
d = '/tmp/claude-0/-home-user-1/d9dd5cf6-a597-547e-95fb-a98c3cc3ca25/scratchpad/'
BILD = json.load(open(d + 'pumpe-bilder.json'))['hand']
ALT = "Kompakte elektrische Luftpumpe von AstroAI mit Digitalanzeige"

# Alle Angaben stammen von der amazon.de-Produktseite dieses Geraets:
# 439 g, 13,4 x 6,6 x 5 cm, Digitalanzeige mit Druckvorwahl und
# Abschaltautomatik, eingebautes LED-Licht, Fahrrad/E-Bike/Auto,
# 4,5 Sterne, 10.000+ gekauft, Bestseller Nr. 1 bei Reifendruckkompressoren.


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
HINWEIS = "Anzeige · Als Amazon-Partner verdienen wir an qualifizierten Verkäufen."
KNOPF = 'Preis auf Amazon prüfen ' + PFEIL

PINS = []

# ── 1 · Nachtfahrt ──────────────────────────────────────────────────────────
PINS.append(('e1', '''
  <div class="strahl"></div><div class="pool"></div><div class="boden"></div>
  <img class="ware" src="%(bild)s" alt="%(alt)s">
  <div class="inner">
    <div class="kopf">%(logo)s<span class="wm">SQUELLY</span><span class="marke">Fahrrad</span></div>
    <h1>Panne um<br><em>halb zehn.</em></h1>
    <p class="unter">Das eingebaute LED-Licht leuchtet dir das Ventil aus, während sie pumpt.</p>
    <div class="fuss">
      <span class="knopf">%(knopf)s</span>
      <span class="klein">%(hinweis)s</span>
    </div>
  </div>''' % dict(bild=BILD, alt=ALT, logo=logo(True), knopf=KNOPF, hinweis=HINWEIS)))

# ── 2 · Riss ────────────────────────────────────────────────────────────────
# Die Bemaszungslinien sitzen eng am sichtbaren Geraet, nicht am Bildrahmen:
# im Bildkasten fuellt die Pumpe rund 43 % der Breite und 87 % der Hoehe.
BX, BY, BW, BH = 440, 350, 460, 460          # Mitte und Kasten des Bildes
PW, PH = BW * .43, BH * .87                  # sichtbares Geraet
L, R = BX - PW / 2, BX + PW / 2
O, U = BY - PH / 2, BY + PH / 2
TIEF = L + PW * (5 / 6.6)                    # 5 cm im Verhaeltnis zu 6,6 cm


def masz(x1, y1, x2, y2, quer):
    """Masslinie mit zwei Pfeilspitzen und zwei Hilfslinien."""
    if quer:
        h = ('M%.0f %.0f L%.0f %.0f M%.0f %.0f L%.0f %.0f'
             % (x1, y1 + 16, x1, y1 - 34, x2, y1 + 16, x2, y1 - 34))
        s = ('M%.0f %.0f L%.0f %.0f L%.0f %.0f M%.0f %.0f L%.0f %.0f L%.0f %.0f'
             % (x1 + 9, y1 - 6, x1, y1, x1 + 9, y1 + 6,
                x2 - 9, y1 - 6, x2, y1, x2 - 9, y1 + 6))
        return '<path d="M%.0f %.0f L%.0f %.0f"/><path d="%s"/><path d="%s"/>' % (x1, y1, x2, y1, h, s)
    h = ('M%.0f %.0f L%.0f %.0f M%.0f %.0f L%.0f %.0f'
         % (x1 - 16, y1, x1 + 34, y1, x1 - 16, y2, x1 + 34, y2))
    s = ('M%.0f %.0f L%.0f %.0f L%.0f %.0f M%.0f %.0f L%.0f %.0f L%.0f %.0f'
         % (x1 - 6, y1 + 9, x1, y1, x1 + 6, y1 + 9,
            x1 - 6, y2 - 9, x1, y2, x1 + 6, y2 - 9))
    return '<path d="M%.0f %.0f L%.0f %.0f"/><path d="%s"/><path d="%s"/>' % (x1, y1, x1, y2, h, s)


riss = '''<svg viewBox="0 0 880 700">
  <g fill="none" stroke="#8fc4ee" stroke-width="1.6" stroke-opacity=".9"
     stroke-linecap="round" stroke-linejoin="round">%s%s%s</g>
  <g font-family="ui-monospace,Menlo,monospace" font-size="22" fill="#bfe0f7" letter-spacing="1">
    <text x="%.0f" y="%.0f" text-anchor="middle">6,6 cm</text>
    <text x="%.0f" y="%.0f">13,4 cm</text>
    <text x="%.0f" y="%.0f" text-anchor="middle">5 cm</text>
  </g>
</svg>''' % (masz(L, O - 74, R, 0, True),
             masz(R + 132, O, 0, U, False),
             masz(L, U + 78, TIEF, 0, True),
             BX, O - 94,
             R + 152, BY + 8,
             (L + TIEF) / 2, U + 118)

werte = "".join('<div><b>%s</b><span>%s</span></div>' % (k, v) for k, v in
                [("GEWICHT", "439 g"), ("ANZEIGE", "digital"), ("LICHT", "LED")])
PINS.append(('e2', '''
  <div class="rahmen"></div>
  <i class="kreuz k1"></i><i class="kreuz k2"></i><i class="kreuz k3"></i><i class="kreuz k4"></i>
  <div class="riss">%(riss)s<img class="ware" src="%(bild)s" alt="%(alt)s"></div>
  <div class="inner">
    <div class="kopf">%(logo)s<span class="wm">SQUELLY</span><span class="marke">MASSBLATT</span></div>
    <h1>Passt in jede<br><em>Satteltasche.</em></h1>
    <div class="werte">%(werte)s</div>
    <div class="knopf">%(knopf)s</div>
    <div class="klein">%(hinweis)s</div>
  </div>''' % dict(riss=riss, bild=BILD, alt=ALT, logo=logo(True), werte=werte,
                   knopf=KNOPF, hinweis=HINWEIS)))

# ── 3 · Schnitt ─────────────────────────────────────────────────────────────
PINS.append(('e3', '''
  <div class="blau"></div><div class="kante"></div>
  <div class="kopf">%(logo)s<span class="wm">SQUELLY</span><span class="marke">Fahrrad</span></div>
  <div class="alt"><b>Bisher</b><p>Treten, bis der Arm brennt</p></div>
  <img class="ware" src="%(bild)s" alt="%(alt)s">
  <div class="neu"><b>Ab jetzt</b><h1>Knopf drücken,<br>fertig.</h1></div>
  <div class="fuss">
    <span class="knopf">%(knopf)s</span>
    <p class="klein">%(hinweis)s</p>
  </div>''' % dict(logo=logo(), bild=BILD, alt=ALT, knopf=KNOPF, hinweis=HINWEIS)))

# ── 4 · Plakat ──────────────────────────────────────────────────────────────
daten = "".join('<div><span>%s</span><b>%s</b></div>' % (l, w) for l, w in
                [("Länge", "13,4 cm"), ("Sterne", "4,5"), ("Verkauft", "10.000+")])
PINS.append(('e4', '''
  <div class="inner">
    <div class="kopf">%(logo)s<span class="wm">SQUELLY</span><span class="marke">Fahrrad</span></div>
    <div class="riese">439<sup>g</sup></div>
    <p class="unter">So wenig wiegt die Pumpe, die deine Standpumpe ersetzt.</p>
    <div class="daten">%(daten)s</div>
    <div class="kreis"></div>
    <img class="ware" src="%(bild)s" alt="%(alt)s">
    <div class="fuss">
      <span class="knopf">%(knopf)s</span>
      <p class="klein">%(hinweis)s</p>
    </div>
  </div>''' % dict(logo=logo(), daten=daten, bild=BILD, alt=ALT,
                   knopf=KNOPF, hinweis=HINWEIS)))

# ── 5 · Anleitung ───────────────────────────────────────────────────────────
schritte = "".join('<div class="schritt"><b>%d</b><div><h3>%s</h3><p>%s</p></div></div>'
                   % (i + 1, t, u) for i, (t, u) in enumerate([
                       ("Aufsetzen", "Ventilkopf aufschrauben — Fahrrad, E-Bike oder Auto."),
                       ("Druck wählen", "Wunschdruck an der Digitalanzeige vorwählen."),
                       ("Knopf drücken", "Sie pumpt und schaltet beim Zielwert selbst ab."),
                   ]))
PINS.append(('e5', '''
  <div class="kopf">%(logo)s<span class="wm">SQUELLY</span><span class="marke">Bestseller Nr. 1</span></div>
  <h1>Reifen voll in<br><em>drei Schritten.</em></h1>
  <div class="band"><img class="ware" src="%(bild)s" alt="%(alt)s"></div>
  <div class="schritte">%(schritte)s</div>
  <div class="beleg"><span class="st">★★★★★</span><b>4,5</b><span>· 10.000+ gekauft</span></div>
  <div class="fuss">
    <div class="knopf">%(knopf)s</div>
    <p class="klein">%(hinweis)s</p>
  </div>''' % dict(logo=logo(), bild=BILD, alt=ALT, schritte=schritte,
                   knopf=KNOPF, hinweis=HINWEIS)))

teile = [DEFS]
for pid, inhalt in PINS:
    teile.append('<div class="cap">%s</div><div class="pin" id="%s">%s</div>' % (pid, pid, inhalt))

tpl = open(d + 'pin3.template.html', encoding='utf-8').read()
out = tpl.replace('/*FONTS*/', open(d + 'fonts.css', encoding='utf-8').read()) \
         .replace('<!--PINS-->', "\n".join(teile))
open(d + 'pin3.html', 'w', encoding='utf-8').write(out)
print('pin3.html', round(len(out) / 1024), 'KB')

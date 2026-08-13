import json, math
d = '/tmp/claude-0/-home-user-1/d9dd5cf6-a597-547e-95fb-a98c3cc3ca25/scratchpad/'

LOGO = '''<svg class="logo" viewBox="0 0 200 360" aria-hidden="true">
        <g clip-path="url(#lc)"><rect width="200" height="360" fill="#fff"/>
          <g fill="none" stroke="#3a8ccd" stroke-linecap="round">
            <use href="#la" x="18" stroke-width="26"/><use href="#lb" x="72" stroke-width="17"/>
            <use href="#la" x="118" stroke-width="34"/><use href="#lb" x="176" stroke-width="21"/></g>
          <g fill="none" stroke="#14315c" stroke-width="5">
            <use href="#la" x="2"/><use href="#lb" x="38"/><use href="#la" x="72"/>
            <use href="#lb" x="110"/><use href="#la" x="146"/><use href="#lb" x="184"/></g></g>
        <rect x="1" y="1" width="198" height="358" rx="2" fill="none" stroke="#14315c" stroke-width="4"/></svg>'''

DEFS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
  <clipPath id="lc"><rect x="1" y="1" width="198" height="358" rx="2"/></clipPath>
  <path id="la" d="M0,-30 C40,52 -32,104 14,168 C56,230 -16,276 20,340 C38,376 6,388 12,412"/>
  <path id="lb" d="M0,-30 C22,60 -44,96 8,164 C44,226 -28,268 14,336 C30,372 -2,384 6,412"/>
  <path id="t1" d="M0,-60 C120,250 -110,500 40,830 C180,1150 -50,1330 60,1640"/></defs></svg>'''

TEX = ('<div class="tex"><svg viewBox="0 0 1000 1500" preserveAspectRatio="none">'
       '<g fill="none" stroke="#3a8ccd" stroke-width="1.6">'
       + "".join('<use href="#t1" x="%d"/>' % x for x in range(-60, 1120, 76)) + '</g></svg></div>')

HAKEN = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>')
PFEIL = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')

def bogen(anteil=0.72):
    """Manometer — dasselbe Wirkzeichen wie in den Feed-Motiven."""
    cx = cy = 200
    start, ende = 140, 400
    def punkt(r, g):
        a = math.radians(g); return cx + math.cos(a)*r, cy + math.sin(a)*r
    def pfad(r, g1, g2):
        x1,y1 = punkt(r,g1); x2,y2 = punkt(r,g2)
        gross = 1 if (g2-g1) % 360 > 180 else 0
        return 'M%.1f,%.1f A%d,%d 0 %d 1 %.1f,%.1f' % (x1,y1,r,r,gross,x2,y2)
    t = ['<path d="%s" fill="none" stroke="#2f7ec0" stroke-opacity=".15" stroke-width="3" '
         'stroke-linecap="round"/>' % pfad(168, start, ende),
         '<path d="%s" fill="none" stroke="#2f7ec0" stroke-opacity=".48" stroke-width="7" '
         'stroke-linecap="round"/>' % pfad(168, start, start + (ende-start)*anteil)]
    for i in range(13):
        g = start + (ende-start)*i/12; lang = (i % 3 == 0)
        x1,y1 = punkt(146 if lang else 154, g); x2,y2 = punkt(134 if lang else 140, g)
        t.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#2f7ec0" '
                 'stroke-opacity="%s" stroke-width="%s" stroke-linecap="round"/>'
                 % (x1,y1,x2,y2, ".4" if lang else ".22", "3.4" if lang else "2"))
    zx,zy = punkt(120, start + (ende-start)*anteil)
    t.append('<line x1="%d" y1="%d" x2="%.1f" y2="%.1f" stroke="#2f7ec0" stroke-opacity=".48" '
             'stroke-width="4" stroke-linecap="round"/>' % (cx,cy,zx,zy))
    t.append('<circle cx="%d" cy="%d" r="7" fill="#2f7ec0" fill-opacity=".42"/>' % (cx,cy))
    return ('<div class="fx"><div class="aura"></div>'
            '<svg viewBox="0 0 400 400">%s</svg></div>' % "".join(t))

BILD = json.load(open(d + 'pumpe-bilder.json'))['hand']
MARKE = '<div class="top">%s<span class="wm">SQUELLY</span><span class="tag">Fahrrad</span></div>' % LOGO
ABBINDER = ('<div class="foot"><span class="cta">Preis auf Amazon prüfen %s</span>'
            '<span class="note">Anzeige · Als Amazon-Partner verdienen wir an qualifizierten '
            'Verkäufen.</span></div>' % PFEIL)
BUEHNE = ('<div class="surface"></div>%s<div class="sun"></div><div class="cool"></div>'
          '<div class="contact"></div><div class="stage"><img src="%s" alt="%s"></div>'
          '<div class="vig"></div>')
ALT = "Kompakte elektrische Luftpumpe von AstroAI mit Digitalanzeige"

def belege(*zeilen):
    return ('<div class="proof">' +
            "".join('<span class="pf">%s%s</span>' % (HAKEN, z) for z in zeilen) + '</div>')

PINS = []

# --- P1: klassisch -------------------------------------------------------
PINS.append(('p1', '''
  %(buehne)s
  %(bogen)s
  <div class="inner">
    %(marke)s
    <p class="said">Die Standpumpe steht im Keller. Der platte Reifen steht am Bahnhof.</p>
    <h1 class="head">439 Gramm.<br><span class="big">Passt überall.</span></h1>
    %(belege)s
    %(abbinder)s
  </div>''' % dict(buehne=BUEHNE % (TEX, BILD, ALT), bogen=bogen(0.78), marke=MARKE,
                   belege=belege("13,4 × 6,6 × 5 cm", "Wiegt weniger als eine Trinkflasche",
                                 "LED-Licht eingebaut"),
                   abbinder=ABBINDER)))

# --- P2: Titelband -------------------------------------------------------
PINS.append(('p2', '''
  %(buehne)s
  %(bogen)s
  <div class="band">
    %(marke)s
    <h1 class="head">Klein genug<br><span class="big">für die Satteltasche.</span></h1>
  </div>
  <div class="inner">
    <p class="said">Am Rahmen, im Rucksack oder im Handschuhfach — sie ist einfach dabei.</p>
    %(belege)s
    %(abbinder)s
  </div>''' % dict(buehne=BUEHNE % (TEX, BILD, ALT), bogen=bogen(0.62), marke=MARKE,
                   belege=belege("13,4 × 6,6 × 5 cm", "439 Gramm",
                                 "Für Fahrrad, E-Bike und Auto"),
                   abbinder=ABBINDER)))

# --- P3: Zahlen ----------------------------------------------------------
zahlen = "".join('<div><b>%s</b><span>%s</span></div>' % (w, l) for w, l in
                 [("439", "Gramm"), ("13,4", "Zentimeter lang"), ("4,5", "Sterne bei Amazon")])
PINS.append(('p3', '''
  %(buehne)s
  %(bogen)s
  <div class="inner">
    %(marke)s
    <h1 class="head">Die Zahlen,<br>die zählen.</h1>
    <div class="zahlen">%(zahlen)s</div>
    %(abbinder)s
  </div>''' % dict(buehne=BUEHNE % (TEX, BILD, ALT), bogen=bogen(0.85), marke=MARKE,
                   zahlen=zahlen, abbinder=ABBINDER)))

# --- P4: Produkt im Rahmen ----------------------------------------------
PINS.append(('p4', '''
  <div class="surface"></div>%(tex)s<div class="sun"></div><div class="cool"></div>
  <div class="vig"></div>
  <div class="inner">
    %(marke)s
    <p class="said">Über zehntausend Leute haben sie schon gekauft.</p>
    <h1 class="head">4,5 Sterne.<br><span class="big">10.000+ verkauft.</span></h1>
    <div class="rahmen">%(bogen)s<img src="%(bild)s" alt="%(alt)s"></div>
    %(belege)s
    %(abbinder)s
  </div>''' % dict(tex=TEX, marke=MARKE, bogen=bogen(0.7), bild=BILD, alt=ALT,
                   belege=belege("Bestseller Nr. 1 bei Reifendruckkompressoren",
                                 "Digitalanzeige mit Druckvorwahl"),
                   abbinder=ABBINDER)))

# --- P5: Checkliste ------------------------------------------------------
liste = "".join('<div><b>%s</b><span>%s</span></div>' % (n, t) for n, t in
                [("1", "Passt an den Rahmen, in die Satteltasche oder in den Rucksack"),
                 ("2", "Motor macht die Arbeit — kein Treten, kein Nachmessen"),
                 ("3", "LED-Licht für die Panne, wenn es schon dunkel ist")])
PINS.append(('p5', '''
  %(buehne)s
  %(bogen)s
  <div class="inner">
    %(marke)s
    <h1 class="head">Drei Gründe<br><span class="big">für die Kleine.</span></h1>
    <div class="liste">%(liste)s</div>
    %(abbinder)s
  </div>''' % dict(buehne=BUEHNE % (TEX, BILD, ALT), bogen=bogen(0.55), marke=MARKE,
                   liste=liste, abbinder=ABBINDER)))

teile = [DEFS]
for pid, inhalt in PINS:
    teile.append('<div class="cap">%s</div><div class="pin" id="%s">%s</div>' % (pid, pid, inhalt))

tpl = open(d + 'pin.template.html', encoding='utf-8').read()
out = tpl.replace('/*FONTS*/', open(d + 'fonts.css', encoding='utf-8').read()) \
         .replace('<!--PINS-->', "\n".join(teile))
open(d + 'pin.html', 'w', encoding='utf-8').write(out)
print('pin.html', round(len(out)/1024), 'KB')

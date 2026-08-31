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
  <path id="t1" d="M0,-60 C120,180 -110,360 40,600 C180,830 -50,960 60,1180"/></defs></svg>'''

TEX = ('<div class="tex"><svg viewBox="0 0 1080 1080" preserveAspectRatio="none">'
       '<g fill="none" stroke="#3a8ccd" stroke-width="1.5">'
       + "".join('<use href="#t1" x="%d"/>' % x for x in range(-40, 1180, 78)) + '</g></svg></div>')

HAKEN = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>')
PFEIL = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')

def bogen(anteil=0.72):
    """Manometer: ein offener Bogen mit Skalenstrichen, der bis zum
    eingestellten Anteil gefüllt ist. Der Druck steigt — das Gegenstück
    zu Sog, Impuls und Licht bei den anderen Produkten."""
    cx = cy = 200
    start, ende = 140, 400            # Grad, offen nach unten
    def punkt(r, grad):
        a = math.radians(grad)
        return cx + math.cos(a) * r, cy + math.sin(a) * r
    def pfad(r, g1, g2):
        x1, y1 = punkt(r, g1); x2, y2 = punkt(r, g2)
        gross = 1 if (g2 - g1) % 360 > 180 else 0
        return 'M%.1f,%.1f A%d,%d 0 %d 1 %.1f,%.1f' % (x1, y1, r, r, gross, x2, y2)

    teile = []
    # Grundbogen
    teile.append('<path d="%s" fill="none" stroke="#2f7ec0" stroke-opacity=".16" '
                 'stroke-width="3" stroke-linecap="round"/>' % pfad(168, start, ende))
    # gefüllter Anteil
    teile.append('<path d="%s" fill="none" stroke="#2f7ec0" stroke-opacity=".5" '
                 'stroke-width="7" stroke-linecap="round"/>'
                 % pfad(168, start, start + (ende - start) * anteil))
    # Skalenstriche
    for i in range(13):
        g = start + (ende - start) * i / 12
        lang = (i % 3 == 0)
        x1, y1 = punkt(146 if lang else 154, g)
        x2, y2 = punkt(134 if lang else 140, g)
        teile.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#2f7ec0" '
                     'stroke-opacity="%s" stroke-width="%s" stroke-linecap="round"/>'
                     % (x1, y1, x2, y2, ".42" if lang else ".24", "3.4" if lang else "2"))
    # Zeiger
    zx, zy = punkt(120, start + (ende - start) * anteil)
    teile.append('<line x1="%d" y1="%d" x2="%.1f" y2="%.1f" stroke="#2f7ec0" '
                 'stroke-opacity=".5" stroke-width="4" stroke-linecap="round"/>' % (cx, cy, zx, zy))
    teile.append('<circle cx="%d" cy="%d" r="7" fill="#2f7ec0" fill-opacity=".45"/>' % (cx, cy))
    return ('<div class="fx"><div class="aura"></div>'
            '<svg viewBox="0 0 400 400">%s</svg></div>' % "".join(teile))

def zahlenblock(werte):
    if not werte: return ""
    return ('<div class="zahlen">' +
            "".join('<div><b>%s</b><span>%s</span></div>' % (w, l) for w, l in werte) +
            '</div>')

BILDER = json.load(open(d + 'pumpe-bilder.json'))

VARIANTEN = [
  # Alle Angaben stammen von der amazon.de-Produktseite dieses Geräts
  # (439 g, 13,4 x 6,6 x 5 cm, 4,5 Sterne, Bestseller Nr. 1, 10.000+ gekauft,
  # UVP 30,99 EUR, -23 %). Die Werte des schlanken Stab-Modells - 35 Sekunden,
  # 25 Reifen, 150 PSI - gelten hier NICHT und wurden entfernt.
  dict(id="va", tag="Fahrrad", bild="hand", anteil=0.78,
       alt="Kompakte elektrische Luftpumpe von AstroAI mit Digitalanzeige",
       said='Die Standpumpe steht im Keller. Der platte Reifen steht am Bahnhof.',
       kopf='439 Gramm.<br><span class="big">Passt überall.</span>',
       belege=["13,4 x 6,6 x 5 cm — Satteltasche, Rucksack, Handschuhfach",
               "Digitalanzeige mit Druckvorwahl",
               "LED-Licht für die Panne im Dunkeln"]),
  dict(id="vb", tag="Fahrrad", bild="set", anteil=0.6,
       alt="Kompakte elektrische Luftpumpe von AstroAI mit Zubehör",
       said='Über zehntausend Leute haben sie schon gekauft.',
       kopf='4,5 Sterne.<br><span class="big">10.000+ verkauft.</span>',
       belege=["Bestseller Nr. 1 bei Reifendruckkompressoren",
               "Für Fahrrad, E-Bike und Auto",
               "LED-Licht ist eingebaut"]),
  dict(id="vc", tag="Fahrrad", bild="hand", anteil=0.5,
       alt="Kompakte elektrische Luftpumpe von AstroAI mit Digitalanzeige",
       said='Am Rahmen, in der Satteltasche oder im Rucksack.',
       kopf='<span>Mobil.</span><span class="b2">Kompakt.</span><span>Dabei.</span>',
       belege=["Passt an den Fahrradrahmen",
               "Verschwindet in jeder Satteltasche",
               "Wiegt weniger als eine volle Trinkflasche"]),
  dict(id="vd", tag="Fahrrad", bild="hand", anteil=0.66,
       alt="Kompakte elektrische Luftpumpe von AstroAI mit Digitalanzeige",
       said='Die Standpumpe im Keller hat ihren letzten Einsatz hinter sich.',
       kopf='Kein Treten<br><span class="big">mehr nötig.</span>',
       belege=["Motor macht die Arbeit, du hältst nur",
               "Druck einstellen, Gerät schaltet selbst ab",
               "Anzeige zeigt mit — kein Nachmessen"]),
  dict(id="ve", tag="Fahrrad", bild="hand", anteil=0.85,
       alt="Kompakte elektrische Luftpumpe von AstroAI mit Digitalanzeige",
       said='Wenn du schon weißt, was du suchst:',
       kopf='Die Zahlen, die zählen.',
       zahlen=[("439", "Gramm"), ("13,4", "Zentimeter lang"),
               ("4,5", "Sterne bei Amazon")],
       belege=["Bestseller Nr. 1 in seiner Kategorie",
               "Digitalanzeige mit Druckvorwahl"]),
]

teile = [DEFS]
for v in VARIANTEN:
    belege = "".join('<span class="pf">%s%s</span>' % (HAKEN, b) for b in v["belege"])
    teile.append('''<div class="cap">%(id)s</div>
<div class="ad" id="%(id)s">
  <div class="surface"></div>
  %(bogen)s
  %(tex)s
  <div class="sun"></div><div class="cool"></div>
  <div class="contact"></div>
  <div class="stage"><img src="%(img)s" alt="%(alt)s"></div>
  <div class="vig"></div>
  <div class="inner">
    <div class="top">%(logo)s<span class="wm">SQUELLY</span><span class="tag">%(tag)s</span></div>
    <p class="said">%(said)s</p>
    <h1 class="head">%(kopf)s</h1>
    %(zahlen)s
    <div class="proof">%(belege)s</div>
    <div class="foot">
      <span class="cta">Preis auf Amazon prüfen %(pfeil)s</span>
      <span class="note">Anzeige · Als Amazon-Partner verdienen wir an qualifizierten Verkäufen.</span>
    </div>
  </div>
</div>''' % dict(id=v["id"], tag=v["tag"], tex=TEX, bogen=bogen(v["anteil"]),
                 img=BILDER[v["bild"]], alt=v["alt"], logo=LOGO,
                 said=v["said"], kopf=v["kopf"], belege=belege, pfeil=PFEIL,
                 zahlen=zahlenblock(v.get("zahlen"))))

tpl = open(d + 'pumpe.template.html', encoding='utf-8').read()
out = tpl.replace('/*FONTS*/', open(d + 'fonts.css', encoding='utf-8').read()) \
         .replace('<!--ADS-->', "\n".join(teile))
open(d + 'pumpe.html', 'w', encoding='utf-8').write(out)
print('pumpe.html', round(len(out) / 1024), 'KB')

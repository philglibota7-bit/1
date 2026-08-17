import json
d = '/tmp/claude-0/-home-user-1/d9dd5cf6-a597-547e-95fb-a98c3cc3ca25/scratchpad/'
BILDER = json.load(open(d + 'bilder-ad.json'))

# Keine Sterne auf diesen Blaettern: fuer die drei Produkte liegt kein
# Bewertungswert vor, und funf gemalte Sterne liest jeder als Note.
# Alle Angaben stammen aus den Produktkarten auf squelly.html, die ihrerseits
# von den Herstellerangaben und den Verpackungen auf den Fotos kommen. Was
# der Hersteller behauptet statt misst, steht als seine Behauptung da.


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

WARE = [
    dict(
        kuerzel="vakuumierer", familie="kueche", bild="vakuumierer", tag="Küche",
        name="Kabelloser Handvakuumierer mit 30 Beuteln",
        alt="Weißer Handvakuumierer neben vakuumierten Beuteln mit Mandeln und "
            "Limettenscheiben sowie frischem Gemüse",
        riese="30", einheit="Beutel",
        unter="wiederverwendbare Beutel liegen bei — BPA-frei, und der Clip auch.",
        zahlen=[("Versiegeln", "5 Sek."), ("Beutel", "30 Stück"), ("Laden", "USB-C")],
        titel="Reste halten<br><em>länger.</em>",
        schritte=[("Beutel füllen", "Angebrochenes hinein, Beutel flach hinlegen."),
                  ("Gerät aufsetzen", "Der Vakuumierer greift das Ventil des Beutels."),
                  ("Knopf drücken", "In etwa fünf Sekunden ist der Beutel versiegelt.")],
        tabelle=[("Beutel", "30, wiederverwendbar"), ("Versiegeln", "etwa 5 Sekunden"),
                 ("Material", "BPA-frei"), ("Laden", "Akku, USB-C"),
                 ("Haltbarkeit", "bis 5x länger, laut Hersteller")],
    ),
    dict(
        kuerzel="massagepistole", familie="erholung", bild="massager", tag="Erholung",
        name="Mini-Massagepistole mit neun Aufsätzen",
        alt="Graue Mini-Massagepistole mit Kugelaufsatz, daneben neun weitere Aufsätze "
            "und die Verpackung",
        riese="9", einheit="Aufsätze",
        unter="für Nacken, Schultern, Rücken, Waden und Arme — in einer Hand.",
        zahlen=[("Aufsätze", "9 Stück"), ("Bedienung", "eine Taste"), ("Laden", "USB-C")],
        titel="Der Nacken<br>nach acht <em>Stunden.</em>",
        schritte=[("Aufsatz wählen", "Neun liegen bei — Kugel, Gabel, Kegel und mehr."),
                  ("Stufe wählen", "Mehrere Intensitätsstufen über eine einzige Taste."),
                  ("Ansetzen", "Auf die verspannte Stelle halten, das Gerät macht den Rest.")],
        tabelle=[("Aufsätze", "9 im Set"), ("Stufen", "mehrere, eine Taste"),
                 ("Anzeige", "Ladestand am Boden"), ("Laden", "USB-C"),
                 ("Größe", "passt in Schublade und Sporttasche")],
    ),
    dict(
        kuerzel="lampe", familie="licht", bild="lampe", tag="Zuhause",
        name="Sunset Projector — Tischlampe mit Sonnenuntergangs-Licht",
        alt="Schwarze Sunset-Projektor-Tischlampe neben ihrer Verpackung",
        riese="16", einheit="Farben",
        unter="und vier Lichtmodi. Ein Schalter verändert den ganzen Raum.",
        zahlen=[("Farben", "16"), ("Modi", "4"), ("Schwenkbar", "180°")],
        titel="Weißes Deckenlicht<br>kann <em>weg.</em>",
        schritte=[("Einstecken", "Strom kommt über USB — Steckdose oder Powerbank."),
                  ("Farbe wählen", "16 Farben und vier Modi, die Fernbedienung liegt bei."),
                  ("Kopf schwenken", "Um 180 Grad drehbar: Licht an die Wand oder an die Decke.")],
        tabelle=[("Farben", "16"), ("Lichtmodi", "4"), ("Fernbedienung", "liegt bei"),
                 ("Kopf", "180° schwenkbar"), ("Strom", "über USB")],
    ),
]

PINS = []
for w in WARE:
    bild = BILDER[w["bild"]]
    img = '<img src="%s" alt="%s">' % (bild, w["alt"])
    grund = dict(logo=logo(), img=img, knopf=KNOPF, hinweis=HINWEIS, tag=w["tag"])

    # ── A · Plakat ─────────────────────────────────────────────────────────
    zahlen = "".join('<div><span>%s</span><b>%s</b></div>' % (k, v) for k, v in w["zahlen"])
    PINS.append((w["kuerzel"] + "-plakat", w["familie"] + " plakat", '''
      <div class="inner">
        <div class="kopf">%(logo)s<span class="wm">SQUELLY</span><span class="marke">%(tag)s</span></div>
        <div class="riese">%(riese)s</div>
        <div class="einheit">%(einheit)s</div>
        <p class="unter">%(unter)s</p>
        <div class="zahl">%(zahlen)s</div>
        <div class="kreis"></div>
        %(img)s
        <div class="fuss">
          <span class="knopf">%(knopf)s</span>
          <p class="klein">%(hinweis)s</p>
        </div>
      </div>''' % dict(grund, riese=w["riese"], einheit=w["einheit"],
                       unter=w["unter"], zahlen=zahlen)))

    # ── B · Anleitung ──────────────────────────────────────────────────────
    schritte = "".join('<div class="schritt"><b>%d</b><div><h3>%s</h3><p>%s</p></div></div>'
                       % (i + 1, t, u) for i, (t, u) in enumerate(w["schritte"]))
    PINS.append((w["kuerzel"] + "-anleitung", w["familie"] + " anleitung", '''
      <div class="kopf">%(logo)s<span class="wm">SQUELLY</span><span class="marke">%(tag)s</span></div>
      <h1>%(titel)s</h1>
      <div class="band">%(img)s</div>
      <div class="schritte">%(schritte)s</div>
      <div class="beleg"><i></i><b>Drei Schritte</b><span>· mehr braucht es nicht</span></div>
      <div class="fuss">
        <div class="knopf">%(knopf)s</div>
        <p class="klein">%(hinweis)s</p>
      </div>''' % dict(grund, titel=w["titel"], schritte=schritte)))

    # ── C · Karte ──────────────────────────────────────────────────────────
    tab = "".join('<div><span>%s</span><span>%s</span></div>' % (k, v) for k, v in w["tabelle"])
    PINS.append((w["kuerzel"] + "-karte", w["familie"] + " karte", '''
      <div class="blatt">
        <div class="kopf">%(logo)s<span class="wm">SQUELLY</span><span class="marke">%(tag)s</span></div>
        <div class="bild">%(img)s</div>
        <div class="titel"><h2>%(name)s</h2>
          <div class="sterne"><i></i><b>Von SQUELLY empfohlen</b></div>
        </div>
        <div class="tab">%(tab)s</div>
        <div class="fuss">
          <div class="knopf">%(knopf)s</div>
          <p class="klein">%(hinweis)s</p>
        </div>
      </div>''' % dict(grund, name=w["name"], tab=tab)))

teile = [DEFS]
for pid, klassen, inhalt in PINS:
    teile.append('<div class="cap">%s</div><div class="pin %s" id="%s">%s</div>'
                 % (pid, klassen, pid, inhalt))

tpl = open(d + 'pin5.template.html', encoding='utf-8').read()
out = tpl.replace('/*FONTS*/', open(d + 'fonts.css', encoding='utf-8').read()) \
         .replace('<!--PINS-->', "\n".join(teile))
open(d + 'pin5.html', 'w', encoding='utf-8').write(out)
print('pin5.html', round(len(out) / 1024), 'KB,', len(PINS), 'Pins')

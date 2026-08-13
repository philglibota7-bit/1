import json
d='/tmp/claude-0/-home-user-1/d9dd5cf6-a597-547e-95fb-a98c3cc3ca25/scratchpad/'
LOGO='''<svg class="logo" viewBox="0 0 200 360" aria-hidden="true">
        <g clip-path="url(#lc)"><rect width="200" height="360" fill="#fff"/>
          <g fill="none" stroke="#3a8ccd" stroke-linecap="round">
            <use href="#la" x="18" stroke-width="26"/><use href="#lb" x="72" stroke-width="17"/>
            <use href="#la" x="118" stroke-width="34"/><use href="#lb" x="176" stroke-width="21"/></g>
          <g fill="none" stroke="#14315c" stroke-width="5">
            <use href="#la" x="2"/><use href="#lb" x="38"/><use href="#la" x="72"/>
            <use href="#lb" x="110"/><use href="#la" x="146"/><use href="#lb" x="184"/></g></g>
        <rect x="1" y="1" width="198" height="358" rx="2" fill="none" stroke="#14315c" stroke-width="4"/></svg>'''
DEFS='''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
  <clipPath id="lc"><rect x="1" y="1" width="198" height="358" rx="2"/></clipPath>
  <path id="la" d="M0,-30 C40,52 -32,104 14,168 C56,230 -16,276 20,340 C38,376 6,388 12,412"/>
  <path id="lb" d="M0,-30 C22,60 -44,96 8,164 C44,226 -28,268 14,336 C30,372 -2,384 6,412"/>
  <path id="t1" d="M0,-60 C120,180 -110,360 40,600 C180,830 -50,960 60,1180"/></defs></svg>'''
TEX=('<div class="tex"><svg viewBox="0 0 1080 1080" preserveAspectRatio="none">'
     '<g fill="none" stroke="#3a8ccd" stroke-width="1.5">'
     +"".join('<use href="#t1" x="%d"/>'%x for x in range(-40,1180,78))+'</g></svg></div>')
HAKEN=('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" '
       'stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>')
PFEIL=('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" '
       'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')
ADS=[
 dict(id="ad1",tag="Küche",bild="vakuumierer",
   alt="Weißer Handvakuumierer neben vakuumierten Beuteln und frischem Gemüse",
   said='Die halbe Avocado. Der Rest Hackfleisch. Der Salat von Dienstag.',
   kopf='Alles hält<br><span class="big">fünfmal länger.</span>',
   belege=["In 5 Sekunden versiegelt","30 wiederverwendbare Beutel dabei","Akku, lädt per USB-C"]),
 dict(id="ad2",tag="Erholung",bild="massager",
   alt="Graue Mini-Massagepistole mit neun Aufsätzen",
   said='Acht Stunden Schreibtisch. Der Nacken merkt sich jede einzelne Stunde.',
   kopf='Neun Aufsätze,<br><span class="big">eine Hand.</span>',
   belege=["Neun Aufsätze im Set","Ladestandsanzeige am Boden","Lädt per USB-C"]),
 dict(id="ad3",tag="Zuhause",bild="lampe",
   alt="Schwarze Sunset-Projektor-Tischlampe mit farbig leuchtender Linse",
   said='Weißes Deckenlicht macht aus jedem Zimmer ein Wartezimmer.',
   kopf='16 Farben,<br><span class="big">ein Schalter.</span>',
   belege=["16 Farben, vier Lichtmodi","Fernbedienung liegt bei","Kopf um 180° schwenkbar"]),
]
bilder=json.load(open(d+'bilder-ad.json'))
teile=[DEFS]
for a in ADS:
    FARBEN = ["#ff7a3d","#ff4d6d","#c94bd0","#7a5cf0","#3aa0ff","#2fd0c4","#ffd23d","#ff9a3d"]
    def chip(i, b):
        if a["id"] == "ad3" and i == 0:
            punkte = '<span class="dots">' + "".join('<i style="--c:%s"></i>' % c for c in FARBEN) + '</span>'
            return '<span class="pf">%s%s</span>' % (punkte, b)
        return '<span class="pf">%s%s</span>' % (HAKEN, b)
    belege="".join(chip(i,b) for i,b in enumerate(a["belege"]))
    img=bilder[a["bild"]]
    glow = ('<div class="glow"></div><div class="glowfloor"></div>' if a["id"]=="ad3" else "")
    teile.append('''<div class="cap">%(id)s — %(tag)s</div>
<div class="ad" id="%(id)s">
  <div class="surface"></div>
  %(glow)s
  %(tex)s
  <div class="sun"></div><div class="cool"></div>
  <div class="contact"></div>
  <div class="stage"><img src="%(img)s" alt="%(alt)s"></div>
  <div class="vig"></div>
  <div class="inner">
    <div class="top">%(logo)s<span class="wm">SQUELLY</span><span class="tag">%(tag)s</span></div>
    <p class="said">%(said)s</p>
    <h1 class="head">%(kopf)s</h1>
    <div class="proof">%(belege)s</div>
    <div class="foot">
      <span class="cta">Preis auf Amazon prüfen %(pfeil)s</span>
      <span class="note">Anzeige · Als Amazon-Partner verdienen wir an qualifizierten Verkäufen.</span>
    </div>
  </div>
</div>'''%dict(id=a["id"],tag=a["tag"],tex=TEX,img=img,alt=a["alt"],logo=LOGO,
               said=a["said"],kopf=a["kopf"],belege=belege,pfeil=PFEIL,glow=glow))
tpl=open(d+'ads4.template.html',encoding='utf-8').read()
out=tpl.replace('/*FONTS*/',open(d+'fonts.css',encoding='utf-8').read()).replace('<!--ADS-->',"\n".join(teile))
open(d+'ads4.html','w',encoding='utf-8').write(out)
open(d+'ads4-hoch.html','w',encoding='utf-8').write(out.replace('<body>','<body class="hoch">'))
print('ads4.html',round(len(out)/1024),'KB  +  ads4-hoch.html')

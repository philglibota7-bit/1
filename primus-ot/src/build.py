"""Baut primus-ot.html aus template.html: Bilder als WebP, Schriften und Symbole eingebettet."""
import base64, html, io, json, os, re
from PIL import Image

import sys
D = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = '--artifact' in sys.argv
EMBED = '--embed' in sys.argv or ARTIFACT
ROOT = os.path.normpath(os.path.join(D, '..', '..'))
OUT = (sys.argv[sys.argv.index('--out')+1] if '--out' in sys.argv else
       os.path.join(ROOT, 'primus-ot-artifact.html' if ARTIFACT else 'primus-ot.html'))
ASSET_DIR = os.path.join(ROOT, 'primus-ot', 'img')
ASSET_URL = 'primus-ot/img/'

# ---------- Bilder ----------
KEEP_PNG = {'primus-ot-logo.png', 'primus-ot-logo-dark.png', 'icon.png'}
MAXW = {'slide_1.jpg': 1200, 'slide_2-marc.jpg': 900, 'slider_3-marc.jpg': 900}
cache = {}
def img(name):
    if name in cache:
        return cache[name]
    path = os.path.join(D, 'img', name)
    if name in KEEP_PNG:
        data, ext = open(path, 'rb').read(), 'png'
    else:
        im = Image.open(path)
        im = im.convert('RGBA' if im.mode in ('RGBA', 'LA', 'P') else 'RGB')
        mw = MAXW.get(name, 700)
        if im.width > mw:
            im = im.resize((mw, round(im.height * mw / im.width)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, 'WEBP', quality=78, method=6)
        data, ext = buf.getvalue(), 'webp'
    if EMBED:
        uri = 'data:image/%s;base64,' % ext + base64.b64encode(data).decode()
    else:
        fname = os.path.splitext(name)[0] + '.' + ext
        os.makedirs(ASSET_DIR, exist_ok=True)
        open(os.path.join(ASSET_DIR, fname), 'wb').write(data)
        uri = ASSET_URL + fname
    cache[name] = uri
    return uri

def font(name):
    return base64.b64encode(open(os.path.join(D, 'fonts', name), 'rb').read()).decode()

# ---------- Symbole ----------
S = ('<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.6" '
     'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{}</svg>')
ICONS = {
    'pin':   S.format('<path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11Z"/><circle cx="12" cy="10" r="2.6"/>'),
    'phone': S.format('<path d="M6.5 3.5h3l1.4 3.6-1.9 1.4a12 12 0 0 0 5.5 5.5l1.4-1.9 3.6 1.4v3a2 2 0 0 1-2.2 2A16.5 16.5 0 0 1 4.5 5.7a2 2 0 0 1 2-2.2Z"/>'),
    'fax':   S.format('<path d="M7 8V4h10v4"/><rect x="3" y="8" width="18" height="8" rx="1.5"/><path d="M7 16h10v5H7z"/>'),
    'mail':  S.format('<rect x="3" y="5" width="18" height="14" rx="1.5"/><path d="m3.5 7 8.5 6 8.5-6"/>'),
    'route': S.format('<circle cx="6" cy="18" r="2.2"/><circle cx="18" cy="6" r="2.2"/><path d="M8 18h7a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h7"/>'),
    'doc':   S.format('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8Z"/><path d="M14 3v5h5M9 13h6M9 17h4"/>'),
    'cert':  S.format('<circle cx="12" cy="9" r="5.5"/><path d="M8.5 13.8 7 21l5-2.4L17 21l-1.5-7.2"/>'),
}

# ---------- Bedingungen aus dem Original ----------
def clean_terms(content, fix=()):
    c = re.sub(r'<script.*?</script>|<style.*?</style>', '', content, flags=re.S)
    c = re.sub(r'</(p|div|h[1-6]|li|tr)>', '\n', c)
    c = re.sub(r'<br\s*/?>', '\n', c)
    c = html.unescape(re.sub(r'<[^>]+>', ' ', c))
    for a, b in fix:
        c = c.replace(a, b)
    out, seen = [], set()
    for line in (re.sub(r'[ \t]+', ' ', l).strip() for l in c.split('\n')):
        if not line:
            continue
        letters = re.sub(r'[^A-ZÄÖÜa-zäöüß]', '', line)
        head = (len(line) < 70 and letters and letters == letters.upper() and len(letters) > 4)
        key = line.lower()
        # Doppelte Absätze (im Original z. B. „VERSAND“ zweimal) nur einmal übernehmen
        if key in seen and (head or len(line) > 40):
            continue
        seen.add(key)
        out.append(('<h4>%s</h4>' if head else '<p>%s</p>') % html.escape(line))
    return '\n    '.join(out)

pages = json.load(open(os.path.join(D, 'pages.json')))
def page(key):
    return next(p['content']['rendered'] for p in pages if key in p['link'])
EKB = clean_terms(page('einkaufsbedingungen'))
VKB = clean_terms(page('verkaufsbedingungen'), fix=[('(VBK)', '(VKB)')])
# Einleitende Zeilen, die schon in der Überschrift des Datenblatts stehen, entfernen
EKB = re.sub(r'^<p>Einkaufsbedingungen der Primus[^<]*</p>\s*', '', EKB)
VKB = re.sub(r'^<p>Verkaufsbedingungen der Primus[^<]*</p>\s*', '', VKB)

# ---------- Zusammensetzen ----------
t = open(os.path.join(D, 'template.html'), encoding='utf-8').read()
t = t.replace('{{EKB}}', EKB).replace('{{VKB}}', VKB)
t = re.sub(r'\{\{IMG:([^}]+)\}\}', lambda m: img(m.group(1)), t)
t = re.sub(r'\{\{FONT:([^}]+)\}\}', lambda m: font(m.group(1)), t)
t = re.sub(r'\{\{ICON:([^}]+)\}\}', lambda m: ICONS[m.group(1)], t)
left = re.findall(r'\{\{[A-Z]+:[^}]+\}\}', t)
assert not left, left
if ARTIFACT:
    # Claude-Vorschau liefert ein eigenes Seitengerüst: nur Titel, Stil, Startskript und Inhalt übergeben
    head = re.search(r'<head>(.*?)</head>', t, re.S).group(1)
    parts = [re.search(r'<title>.*?</title>', head, re.S).group(0),
             re.search(r'<style>.*?</style>', head, re.S).group(0),
             re.search(r'<script>.*?</script>', head, re.S).group(0),
             """<script>(function(){var de=document.documentElement;de.lang='de';
var m=document.querySelector('meta[name="viewport"]');if(!m){m=document.createElement('meta');m.name='viewport';document.head.appendChild(m);}
m.content='width=device-width, initial-scale=1.0, viewport-fit=cover';})();</script>""",
             re.search(r'<body>(.*?)</body>', t, re.S).group(1).strip()]
    t = '\n'.join(parts)
    for bad in ['<!DOCTYPE', '<html', '<body', '<head>', ASSET_URL]:
        assert bad not in t, bad
open(OUT, 'w', encoding='utf-8').write(t)
print(f'gebaut: {len(t)//1024} KB, {len(cache)} Bilder')
print('  VERSAND in EKB:', EKB.count('>VERSAND<'), '| (VKB):', '(VKB)' in VKB, '| (VBK):', '(VBK)' in VKB)

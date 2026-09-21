#!/usr/bin/env bash
# Baut PULSE.app aus info-hub.html — ein Befehl, fertiges Mac-Programm.
#   Voraussetzung: node + npm, dann einmalig:  npm i -g @neutralinojs/neu
#   Aufruf:                                    ./desktop/build-app.sh
set -euo pipefail
cd "$(dirname "$0")"

echo "1/4  App-Dateien einsammeln…"
mkdir -p resources/js
cp ../info-hub.html resources/index.html
for f in fussball.html jarvis.html bodyscan.html ip-rechner.html primus-ot.html; do
  [ -f "../$f" ] && cp "../$f" resources/ || true
done
# index.html heisst hier schon so (das ist PULSE selbst) — daher umbenennen
[ -f ../index.html ] && cp ../index.html resources/marwa.html || true

echo "2/4  Desktop-Start einbauen…"
python3 - <<'PY'
p = 'resources/index.html'
h = open(p).read()
if 'js/neutralino.js' not in h:
    boot = '''<script src="js/neutralino.js"></script>
<script>
/* --- Desktop-App: Start, externe Links, Fenster --- */
(function(){
  document.documentElement.classList.add('desktop-app');
  try { Neutralino.init(); } catch(e){}
  document.addEventListener('click', function(ev){
    var a = ev.target.closest && ev.target.closest('a[href]');
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (/^https?:/i.test(href)) {
      ev.preventDefault();
      try { Neutralino.os.open(href); } catch(e){ window.open(href, '_blank'); }
    }
  }, true);
  try { Neutralino.events.on('windowClose', function(){ Neutralino.app.exit(); }); } catch(e){}
})();
</script>
</head>'''
    h = h.replace('</head>', boot, 1)
    open(p, 'w').write(h)
    print('   Desktop-Start eingefuegt')
else:
    print('   war schon drin')
PY

echo "3/4  Programm bauen…"
[ -d bin ] || neu update
neu build --release >/dev/null

echo "4/4  PULSE.app zusammensetzen…"
./make-mac-app.sh

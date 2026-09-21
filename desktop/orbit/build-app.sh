#!/usr/bin/env bash
# Baut ORBIT.app aus orbit.html — ein Befehl, fertiges Mac-Programm.
#   Voraussetzung: node + npm, dann einmalig:  npm i -g @neutralinojs/neu
#   Aufruf:                                    ./desktop/orbit/build-app.sh
set -euo pipefail
cd "$(dirname "$0")"

echo "1/4  App-Datei einsammeln…"
mkdir -p resources/js
cp ../../orbit.html resources/index.html

echo "2/4  Programm-Start einbauen…"
python3 - <<'PY'
p = 'resources/index.html'
h = open(p, encoding='utf-8').read()
if 'js/neutralino.js' not in h:
    boot = '''<script src="js/neutralino.js"></script>
<script>
/* --- Start als Mac-Programm: Verbindung aufbauen, Links extern oeffnen --- */
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
    open(p, 'w', encoding='utf-8').write(h)
    print('   Programm-Start eingefuegt')
else:
    print('   war schon drin')
PY

echo "3/4  Programm bauen…"
[ -d bin ] || neu update
neu build --release >/dev/null

echo "4/4  ORBIT.app zusammensetzen…"
./make-mac-app.sh

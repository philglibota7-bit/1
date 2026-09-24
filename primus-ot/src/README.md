# Primus-Website: Quellen

Hier wird bearbeitet, nicht in `primus-ot.html` selbst.

- `template.html`: Datenblatt-Fassung (ergibt `primus-ot.html`).
- `template-klassisch.html`: klassische Fassung im Stil der ersten Seite (ergibt `primus-ot-klassisch.html`).
- `search.js`: Menüsuche, wird in beide Seiten eingesetzt.
- In beiden Vorlagen: Platzhalter wie `{{IMG:name}}`, `{{FONT:name}}` und `{{ICON:name}}` setzt das Bauskript ein.
- `img/`: Originalbilder. Sie werden beim Bauen als WebP nach `primus-ot/img/` geschrieben.
- `fonts/`: IBM Plex Sans und Plex Mono (Datenblatt-Fassung), Roboto und Open Sans (klassische Fassung), werden eingebettet.
- `pages.json`: Einkaufs- und Verkaufsbedingungen von der Originalseite.

Bauen (benötigt Python 3 und Pillow, `pip install pillow`):

```sh
python3 primus-ot/src/build.py              # erzeugt primus-ot.html
python3 primus-ot/src/build.py --artifact   # erzeugt primus-ot-artifact.html (alles eingebettet)
python3 primus-ot/src/build.py --tpl template-klassisch.html             # erzeugt primus-ot-klassisch.html
python3 primus-ot/src/build.py --tpl template-klassisch.html --artifact  # erzeugt primus-ot-klassisch-artifact.html
```

Lokal ansehen: `python3 -m http.server 8765` im Repo-Ordner, dann http://127.0.0.1:8765/primus-ot.html öffnen.

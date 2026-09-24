# Primus-Website: Quellen

Hier wird bearbeitet, nicht in `primus-ot.html` selbst.

- `template.html`: Seite mit Stil und Skript. Platzhalter wie `{{IMG:name}}`, `{{FONT:name}}` und `{{ICON:name}}` setzt das Bauskript ein.
- `img/`: Originalbilder. Sie werden beim Bauen als WebP nach `primus-ot/img/` geschrieben.
- `fonts/`: IBM Plex Sans und Plex Mono (woff2), werden in die Seite eingebettet.
- `pages.json`: Einkaufs- und Verkaufsbedingungen von der Originalseite.

Bauen (benötigt Python 3 und Pillow, `pip install pillow`):

```sh
python3 primus-ot/src/build.py              # erzeugt primus-ot.html
python3 primus-ot/src/build.py --artifact   # erzeugt primus-ot-artifact.html (alles eingebettet)
```

Lokal ansehen: `python3 -m http.server 8765` im Repo-Ordner, dann http://127.0.0.1:8765/primus-ot.html öffnen.

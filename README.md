# Werkbank

Ein Portfolio kleiner Web-Werkzeuge, die im Browser laufen, ueber die Suche
gefunden werden und sich ueber eine Pro-Stufe finanzieren.

**Die Strategie steht in [MODELL.md](MODELL.md).** Lies das zuerst – der Code
hier ergibt nur zusammen mit der Ueberlegung dahinter Sinn.

---

## In fuenf Minuten startklar

```bash
# 1. Deine Daten eintragen (Impressum ist in Deutschland Pflicht)
$EDITOR tools.json          # betreiber, strasse, plz_ort, email

# 2. Seiten erzeugen
python3 build.py

# 3. Was heute ansteht
alias werkbank='python3 -m cockpit'
werkbank heute
```

Lokal ansehen:

```bash
python3 -m http.server 8000     # dann http://localhost:8000/werkbank.html
```

Veroeffentlichen: `git push` auf `main` – GitHub Pages uebernimmt den Rest.

---

## Was hier liegt

| Pfad | Zweck |
|---|---|
| `MODELL.md` | Das Geschaeftsmodell: warum es traegt, wie es skaliert, was es kostet |
| `tools.json` | Die eine Wahrheit ueber alle Werkzeuge. Alles andere wird daraus erzeugt |
| `build.py` | Erzeugt Katalog, Pro-Seite, Impressum, Datenschutz, Sitemap, robots.txt |
| `platform/werkbank.css` | Gemeinsames Design. Ein neues Werkzeug erbt es vollstaendig |
| `platform/werkbank.js` | Kopf, Fuss, Querverweise, Messung, Bezahlschranke |
| `platform/vorlage.html` | Ausgangspunkt fuer jedes neue Werkzeug |
| `tools/bilder-verkleinern/` | Referenzwerkzeug – zeigt, wie alles zusammenspielt |
| `cockpit/` | Steuerung: Ideen bewerten, Zahlen erfassen, entscheiden |
| `docs/NEUES-TOOL.md` | Der wiederholbare Vorgang, ein Werkzeug zu bauen |
| `docs/BEZAHLUNG.md` | Wie Geld ankommt, und warum die Schranke im Browser sitzt |
| `docs/RECHT-UND-STEUERN.md` | Gewerbe, Kleinunternehmer, Impressum, DSGVO |

Erzeugte Dateien (`werkbank.html`, `pro.html`, `impressum.html`,
`datenschutz.html`, `sitemap.xml`, `robots.txt`) werden von `build.py`
geschrieben – nicht von Hand aendern, die Aenderung waere beim naechsten Lauf weg.

---

## Die Steuerung

```bash
werkbank heute                    # Wochenschwerpunkt, Tagesaufgabe, woran es hakt
werkbank idee add "PDF zusammenfuegen" --nachfrage 5 --absicht 4 \
    --pro_hebel 4 --wettbewerb 4 --wiederkehr 3 --aufwand 2
werkbank idee bewerten 3          # ohne Angaben: fragt nacheinander
werkbank idee liste               # sortiert nach Punkten
werkbank zahlen bilder-verkleinern --besucher 1240 --kaeufe 3 --umsatz 57
werkbank bericht                  # Auswertung mit Entscheidung je Werkzeug
werkbank tafel                    # dasselbe als HTML
werkbank schluessel --anzahl 1    # Lizenzschluessel nach einem Kauf
werkbank ziel 500                 # Monatsziel
```

Ab 65 Punkten wird eine Idee gebaut, darunter nicht. Diese Regel ist der
eigentliche Wert der Steuerung – sie verhindert die haeufigste Art, Zeit zu
verlieren: ein gutes Werkzeug fuer ein Problem zu bauen, das niemand hat.

**Deine Zahlen liegen in `~/.werkbank/`, nicht im Repository.** Das ist
Absicht: dieses Repository wird oeffentlich ausgeliefert. Anderer Ort per
`WERKBANK_HOME`.

---

## Ein neues Werkzeug

```bash
mkdir -p tools/mein-werkzeug
cp platform/vorlage.html tools/mein-werkzeug/index.html
$EDITOR tools.json          # Eintrag ergaenzen
python3 build.py
```

Vollstaendiger Ablauf inklusive Checkliste: [docs/NEUES-TOOL.md](docs/NEUES-TOOL.md).

---

## Tests

```bash
python3 -m unittest discover -s tests -v
```

Geprueft werden unter anderem: die Geldrechnung (in Cent, damit nichts
wegrundet), die Ideenbewertung, die Entscheidungsregeln, die Vollstaendigkeit
von `tools.json` – und dass die im Terminal erzeugten Lizenzschluessel
tatsaechlich dieselbe Pruefziffer verwenden wie die Pruefung im Browser.

---

## Die drei Regeln

1. **Alles laeuft im Browser.** Keine Server, keine Uploads. Das ist gleichzeitig
   das staerkste Verkaufsargument, die schnellste Variante und die einzige, bei
   der tausend Nutzer genauso viel kosten wie einer: nichts.
2. **Ein Werkzeug, eine Aufgabe.** Wer zwei Dinge sucht, findet zwei Eintraege.
3. **Erst Nachfrage pruefen, dann bauen.** Ohne Ausnahme.

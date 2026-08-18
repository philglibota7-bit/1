# Ein neues Werkzeug bauen

Das ist der Vorgang, der sich wiederholt. Er ist absichtlich kurz: wenn das
Anlegen eines Werkzeugs aufwendig waere, wuerde das Modell nicht funktionieren.

---

## 1. Idee bewerten (15 Minuten)

    werkbank idee add "PDF zusammenfuegen" --nachfrage 5 --absicht 4 \
        --pro_hebel 4 --wettbewerb 4 --wiederkehr 3 --aufwand 2

Unter 65 Punkten wird nicht gebaut. Die Regel gilt auch dann, wenn die Idee
Spass macht – besonders dann.

Woran du die Nachfrage schaetzt, ohne Geld fuer Werkzeuge auszugeben:

- Suchvorschlaege beim Tippen: viele Vorschlaege = viele Suchen
- "Ähnliche Suchanfragen" am Ende der Trefferseite
- Foren und Frageportale: dieselbe Frage seit Jahren = echter Bedarf
- Die vorhandenen Treffer: nur schlechte Seiten mit Werbebannern = Luecke

### Die Punktzahl ersetzt die Recherche nicht

Ein Beispiel aus der Praxis, das genau diese Luecke zeigt.

Die Idee &bdquo;biometrisches Passfoto&ldquo; bekommt **72 Punkte** – klares
&bdquo;bauen&ldquo;. Hohe Nachfrage, hohe Zahlungsbereitschaft (ein Fotostudio
kostet 15 bis 20 Euro), gute Pro-Funktion, rein im Browser machbar.

Eine einzige Suche haette dieses Werkzeug verhindert: **Seit dem 1. Mai 2025
sind selbst erstellte Passfotos fuer Personalausweis und Reisepass in
Deutschland nicht mehr zulaessig.** Das Bild muss digital aus einem
zertifizierten Fotostudio oder vom Terminal der Behoerde kommen. Wer das
Werkzeug baut, bedient einen Markt, den es so nicht mehr gibt – und schickt
Leute mit einem Ergebnis los, das im Buergeramt abgelehnt wird.

Die Bewertung kann so etwas nicht wissen. Sie misst, ob eine Idee es wert
waere, gebaut zu werden – nicht, ob die Welt sie noch erlaubt. Deshalb gilt
vor jedem Bau zusaetzlich:

- Gibt es seit Kurzem eine Regel, die den Anwendungsfall abschafft?
- Loesen Betriebssystem oder Browser das Problem inzwischen selbst?
- Was schreiben die Treffer aus den letzten zwoelf Monaten – nicht die von 2019?

Fuenf Minuten Recherche gegen mehrere Tage Bauzeit. Das ist der beste Tausch
in diesem ganzen Modell.

## 2. Ordner anlegen

    mkdir -p tools/pdf-zusammenfuegen
    cp platform/vorlage.html tools/pdf-zusammenfuegen/index.html

Die Vorlage bringt Kopf, Fuss, Bezahlschranke, Darstellung hell/dunkel,
Messung und die Struktur des Inhaltsteils bereits mit.

## 3. In die Registry eintragen

`tools.json` ergaenzen:

```json
{
  "slug": "pdf-zusammenfuegen",
  "titel": "PDF zusammenfuegen",
  "kurz": "Mehrere PDF-Dateien zu einer verbinden - im Browser, ohne Upload.",
  "pfad": "tools/pdf-zusammenfuegen/index.html",
  "status": "live",
  "seit": "2026-09",
  "stichworte": ["pdf zusammenfuegen", "pdf verbinden", "pdf zusammenfassen"],
  "pro": ["Mehr als 5 Dateien", "Seitenreihenfolge frei waehlbar"]
}
```

Dann:

    python3 build.py

Katalog, Sitemap, Pro-Seite und die Querverweise im Fuss sind damit aktuell.
Von Hand wird nichts nachgetragen.

## 4. Bauen

Drei Regeln, die den Unterschied machen:

**Alles im Browser.** Kein Upload, kein Server. Das ist gleichzeitig das
staerkste Verkaufsargument ("deine Datei verlaesst deinen Rechner nicht"),
die schnellste Variante und die einzige, die nichts kostet.

**Eine Sache.** Kein Werkzeug bekommt einen zweiten Zweck. "PDF zusammenfuegen"
komprimiert keine Bilder. Wer beides sucht, findet zwei Eintraege im Katalog –
das ist besser fuer die Auffindbarkeit und fuer die Bedienung.

**Sofort benutzbar.** Keine Anmeldung, kein Hinweisfenster, kein Zwang zur
E-Mail-Adresse. Der Besucher muss innerhalb von drei Sekunden arbeiten koennen.

Die Bezahlschranke setzt du an genau einer Stelle:

```js
if (!Werkbank.pro("stapel", "Mit Pro verarbeitest du beliebig viele Dateien.")) {
  return;   // Werkbank zeigt das Kauffenster selbst
}
```

## 5. Den Inhaltsteil schreiben

Das ist **kein Beiwerk.** Der Textteil unter dem Werkzeug ist der Grund, warum
die Seite ueberhaupt gefunden wird. Er gehoert in `<div class="inhalt">` und
beantwortet die Fragen, die Leute tatsaechlich stellen:

- Wie funktioniert das? (kurze Erklaerung der Sache selbst)
- Welche Variante soll ich waehlen? (Format, Einstellung, Vorgehen)
- Warum ohne Upload? (dein Unterschied zu allen anderen)
- Fuenf bis sieben haeufige Fragen als aufklappbare Abschnitte

600 bis 900 Woerter reichen. Geschrieben fuer einen Menschen, der ein Problem
hat – nicht fuer eine Suchmaschine. Der Unterschied ist deutlich sichtbar.

## 6. Veroeffentlichen

    git add . && git commit -m "Neues Werkzeug: PDF zusammenfuegen"
    git push

GitHub Pages veroeffentlicht automatisch. Danach in der Google Search Console
die Adresse zur Indexierung anmelden – sonst dauert es Wochen statt Tagen.

## 7. Nach vier Wochen messen

    werkbank zahlen pdf-zusammenfuegen --besucher 340 --kaeufe 2 --umsatz 38
    werkbank bericht

Die Entscheidung faellt nicht nach Gefuehl, sondern nach der Spalte
"Entscheidung".

---

## Checkliste vor dem Veroeffentlichen

- [ ] Funktioniert auf dem Handy (nicht nur schmal – wirklich bedienbar)
- [ ] `<title>` und `<meta name="description">` enthalten den Suchbegriff
- [ ] `<link rel="canonical">` zeigt auf die richtige Adresse
- [ ] Inhaltsteil vorhanden, mindestens 600 Woerter
- [ ] Ohne Anmeldung sofort benutzbar
- [ ] Pro-Schranke greift erst, wenn das Gratis-Limit wirklich erreicht ist
- [ ] In `tools.json` eingetragen und `build.py` ausgefuehrt
- [ ] Keine externen Skripte, keine fremden Schriftarten (Datenschutz, Tempo)

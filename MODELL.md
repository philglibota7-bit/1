# Das Modell

Ein Portfolio kleiner Web-Werkzeuge auf gemeinsamer Infrastruktur.
Jedes Werkzeug loest genau eine Aufgabe, laeuft vollstaendig im Browser des
Nutzers und wird ueber die Suche gefunden. Kostenlos in der Grundfunktion,
kostenpflichtig fuer die Funktionen, die beruflich gebraucht werden.

---

## Warum genau dieses Modell

Es gibt vier Eigenschaften, die ein Modell haben muss, damit es langfristig
traegt und skaliert. Die meisten Online-Geschaeftsmodelle haben zwei davon.

**1. Die Grenzkosten pro Nutzer sind null.**
Alles rechnet im Browser des Besuchers. Kein Server, keine Datenbank, keine
Rechenzeit. Ob zehn oder zehntausend Leute ein Werkzeug benutzen, kostet
denselben Betrag: nichts. Hosting ueber GitHub Pages ist kostenlos. Das ist
der Unterschied zwischen einem Geschaeft, das mit Erfolg teurer wird, und
einem, das mit Erfolg profitabler wird.

**2. Die Grenzkosten pro Produkt sinken.**
Werkzeug Nummer eins kostet mehrere Tage. Werkzeug Nummer zwanzig kostet ein
Wochenende, weil Design, Kopf, Fuss, Bezahlschranke, Katalog, Sitemap und
Messung schon existieren und automatisch mitwachsen. Genau dafuer ist
`platform/` und `build.py` da. Ohne diese gemeinsame Basis waere es kein
Portfolio, sondern zwanzig einzelne Baustellen.

**3. Der Umsatz ist von deiner Zeit entkoppelt.**
Ein Werkzeug, das einmal steht, verdient weiter, waehrend du am naechsten
baust oder schlaefst. Das ist der Unterschied zu jeder Dienstleistung:
Freelancing skaliert nur ueber mehr Stunden oder hoehere Stundensaetze, und
beides ist gedeckelt.

**4. Das Risiko ist verteilt.**
Ein einzelner Kunde kann 40 % deines Umsatzes mitnehmen, wenn er kuendigt.
Zwanzig Werkzeuge mit je ein paar tausend Besuchern koennen das nicht. Und
wenn eines nicht laeuft, hast du eine Information gewonnen, keine Existenz
verloren.

---

## Was das Modell **nicht** ist

Damit klar ist, wogegen entschieden wurde:

| Nicht gewaehlt | Warum nicht |
|---|---|
| Freelancing / Agentur | Zeit gegen Geld. Skaliert nur ueber Mitarbeiter, und dann bist du Arbeitgeber, nicht Entwickler. |
| Dropshipping | Marge unter 10 %, Werbekosten steigen jaehrlich, kein Vermoegenswert entsteht. Du mietest Umsatz. |
| Print-on-Demand | Dieselben Probleme, plus Abhaengigkeit von einer Plattform, die dich morgen sperren kann. |
| Affiliate-Blog | Reine Textseiten sind austauschbar geworden. Ein funktionierendes Werkzeug ist es nicht. |
| Kurse / Infoprodukte | Funktioniert erst, wenn du etwas vorzuweisen hast. Genau das baust du hier gerade. |
| Ein grosses SaaS | Monate bis zum ersten Euro, Serverkosten ab Tag eins, und du wettest alles auf eine Idee. |

Das Portfolio-Modell ist bewusst der langsamere, aber der stabilere Weg.
Es gibt hier kein schnelles Geld. Es gibt einen Vermoegenswert, der jeden
Monat ein Stueck groesser wird und den dir niemand abschalten kann.

---

## Der Engpass: Nachfrage, nicht Technik

Das ist der Punkt, an dem die meisten scheitern, und der Grund fuer
`cockpit/bewertung.py`.

Ein Werkzeug zu bauen ist der einfache Teil – besonders mit KI-Unterstuetzung.
Der schwere Teil ist, dass jemand danach sucht. Ein technisch perfektes
Werkzeug fuer ein Problem, das niemand hat, ist verlorene Zeit, egal wie gut
der Code ist.

Deshalb gilt hier eine harte Regel: **Erst die Nachfrage pruefen, dann bauen.**
Sechs Fragen, jede von 0 bis 5:

| Kriterium | Gewicht | Frage |
|---|---|---|
| Nachfrage | 2,5 | Suchen genug Leute aktiv danach? |
| Absicht | 2,5 | Steckt Geld hinter der Suche? |
| Pro-Hebel | 2,0 | Gibt es eine glaubwuerdige kostenpflichtige Funktion? |
| Wettbewerb | 1,5 | Wie stark ist der Wettbewerb? (invers) |
| Wiederkehr | 1,5 | Wird es wiederholt gebraucht? |
| Aufwand | 1,0 | Wie viel Arbeit bis zur ersten Fassung? (invers) |

Ab 65 Punkten wird gebaut. Zwischen 50 und 65 bleibt die Idee liegen.
Darunter wird sie verworfen. Ohne Ausnahme, auch wenn die Idee Spass macht –
besonders dann.

    werkbank idee add "PDF zusammenfuegen" --nachfrage 5 --absicht 4 \
        --pro_hebel 4 --wettbewerb 4 --wiederkehr 3 --aufwand 2

Nachfrage schaetzt du ueber die Vorschlaege der Suchmaschine, ueber
"Ähnliche Suchanfragen" und ueber Foren: Wenn dieselbe Frage seit Jahren
gestellt wird, ist die Nachfrage echt.

---

## Die vier Stufen der Monetarisierung

Nicht alle gleichzeitig. In dieser Reihenfolge.

**Stufe 0 – kostenlos, aber gemessen.**
Das Werkzeug ist vollstaendig benutzbar. Du misst nur, ob ueberhaupt jemand
kommt. Ohne Nachfrage ist jede Bezahlschranke sinnlos.

**Stufe 1 – Pro als Einmalzahlung.**
Sobald ein Werkzeug regelmaessig Besucher hat, kommen die Funktionen dazu,
die beruflich gebraucht werden: Stapelverarbeitung, zusaetzliche Formate,
Voreinstellungen, keine Mengenbegrenzung. Einmal zahlen, alle Werkzeuge.
Eine Einmalzahlung verkauft sich deutlich leichter als ein Abo, wenn niemand
deine Marke kennt.

**Stufe 2 – Abo, wo es ehrlich ist.**
Nur bei Werkzeugen mit wiederkehrendem Nutzen und laufenden Kosten. Ein Abo
fuer etwas, das man zweimal im Jahr braucht, ist Kundenverbrennung.

**Stufe 3 – Firmen.**
Der groesste Hebel und der letzte Schritt: dasselbe Werkzeug als
einbettbares Feld auf fremden Websites, als API oder mit fremdem Logo.
Ein einziger Firmenkunde ersetzt hier hunderte Einzelkaeufe.

Ergaenzend, aber nie als Fundament: Empfehlungslinks bei Werkzeugen mit
klarer Kaufabsicht. Sie sind ein Zubrot und machen dich von fremden
Programmen abhaengig.

---

## Ehrliche Zahlen

Die wichtigste Eigenschaft dieses Modells ist zugleich die unangenehmste:
**die Ertraege verteilen sich extrem ungleich.** Von zehn Werkzeugen ist die
realistische Erwartung:

- fuenf bringen praktisch nichts
- drei bringen 10 bis 50 € im Monat
- ein bis zwei bringen 100 bis 500 € im Monat

Das ist kein Scheitern, das ist die Funktionsweise. Du kannst nicht
vorhersagen, welches Werkzeug der Treffer wird – deshalb baust du viele und
laesst die Zahlen entscheiden. Wer nach drei erfolglosen Werkzeugen aufhoert,
hat das Modell nicht widerlegt, sondern nur zu frueh abgebrochen.

**Zeitachse, nuechtern:**

| Zeitraum | Realistisch |
|---|---|
| Monat 1–3 | 3–4 Werkzeuge live, erste Besucher, 0 € Umsatz |
| Monat 4–6 | Suchmaschinen fangen an zu liefern, erste Kaeufe, zweistellig |
| Monat 7–12 | 8–12 Werkzeuge, ein bis zwei Gewinner erkennbar, niedrig dreistellig |
| Jahr 2 | Das Portfolio traegt. Hier entscheidet sich, ob daraus ein Einkommen wird |

Suchmaschinen brauchen Monate, bis sie einer neuen Seite vertrauen. Das ist
der Preis dafuer, dass dieser Kanal danach fast von selbst laeuft.

---

## Wie skaliert das nach oben?

Vier Hebel, in der Reihenfolge ihres Ertrags:

1. **Mehr Werkzeuge.** Linear und verlaesslich. Zwei pro Monat sind machbar.
2. **Das beste Werkzeug ausbauen.** Ueberlinear. Wenn eines 60 % der Besucher
   bringt, ist eine Woche Arbeit dort mehr wert als drei neue Werkzeuge.
3. **Andere Sprachen.** Multiplikativ. Dieselbe Datei auf Englisch
   vervielfacht den erreichbaren Markt, ohne dass neue Logik entsteht.
4. **Firmenkunden.** Der groesste Sprung – und erst sinnvoll, wenn Stufe 1
   nachweislich funktioniert.

Was hier bewusst **nicht** skaliert wird: Mitarbeiter. Solange die
Grenzkosten null sind, ist jede zusaetzliche Person ein Rueckschritt.

---

## Die Risiken, benannt

**Abhaengigkeit von Suchmaschinen.** Das ist das reale Hauptrisiko. Ein
Algorithmuswechsel kann Besucherzahlen halbieren. Gegenmittel: viele
Werkzeuge statt eines, Direktaufrufe aufbauen (Lesezeichen, Weiterempfehlung),
und mindestens ein zweiter Kanal (Fachforen, Verzeichnisse, Mundpropaganda).

**Nachahmer.** Ein gutes Werkzeug ist in einem Tag kopiert. Verteidigt wird
nicht ueber Code, sondern ueber Breite (zwanzig Werkzeuge kopiert niemand),
ueber Vertrauen und ueber das Alter der Domain.

**Durchhalten.** Das groesste Risiko. Monat 3 ist der Punkt, an dem Arbeit
sichtbar ist und Umsatz nicht. Genau dafuer gibt es `werkbank heute` und
`werkbank bericht`: nicht Motivation, sondern die naechste konkrete Handlung.

**Bezahlschranke im Browser.** Sie ist umgehbar, und das ist bewusst so
(siehe `docs/BEZAHLUNG.md`). Wer sie umgeht, haette ohnehin nicht bezahlt.
Sobald es sich lohnt, wird sie serverseitig geprueft – eine Funktion, eine
Aenderung.

---

## Wann etwas eingestellt wird

Ein Werkzeug, das nach **sechs Monaten** unter 150 Besuchern im Monat liegt,
wird eingestellt oder mit einem anderen zusammengelegt. Nicht aus Haerte,
sondern weil deine Zeit der einzige knappe Rohstoff hier ist.

`werkbank bericht` faellt dieses Urteil automatisch:

| Urteil | Bedeutung |
|---|---|
| `ausbauen` | Besucher **und** Umsatz. Hier investierst du. |
| `monetarisieren` | Besucher ohne Umsatz. Pro-Funktion fehlt. |
| `abwarten` | Noch zu jung fuer ein Urteil. |
| `einstellen` | Sechs Monate, keine Nachfrage. Loslassen. |

---

## Der Startvorteil, den du schon hast

Das ist kein Modell aus dem Nichts. Es existiert bereits:

- ein Repository mit funktionierender Veroeffentlichung ueber GitHub Pages
- mehrere gebaute Werkzeuge, darunter zwei mit echter Suchnachfrage
  (IP-/Subnetz-Rechner und Koerpermass-Rechner)
- der Beweis, dass du Werkzeuge fertig bekommst – der Teil, an dem die
  meisten scheitern

Was gefehlt hat, war nicht die Faehigkeit zu bauen, sondern die Struktur
darum herum: eine Auswahl nach Nachfrage, eine gemeinsame Basis, ein Weg,
Geld zu nehmen, und eine Messung, die entscheidet. Genau das ist jetzt da.

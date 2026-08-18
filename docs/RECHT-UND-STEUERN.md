# Recht und Steuern in Deutschland

**Das hier ist keine Rechts- oder Steuerberatung.** Es ist eine Uebersicht der
Punkte, die dich bei diesem Modell betreffen, damit du weisst, wonach du
fragst. Bei Unsicherheit: Steuerberatung. Die erste Beratung kostet weniger
als der erste Fehler.

---

## Vor dem ersten Euro

**Gewerbeanmeldung.** Sobald du mit Gewinnerzielungsabsicht dauerhaft taetig
bist, ist das ein Gewerbe – auch nebenberuflich, auch bei kleinen Betraegen.
Anmeldung beim Gewerbeamt deiner Stadt, meist 20 bis 60 €, oft online. Das
Finanzamt schickt danach einen Fragebogen zur steuerlichen Erfassung.

Reine Softwareentwicklung kann auch freiberuflich sein (§ 18 EStG) – die
Abgrenzung ist im Einzelfall knifflig. Beim Verkauf fertiger Produkte an
Endkunden ist Gewerbe der Regelfall.

**Kleinunternehmerregelung (§ 19 UStG).** Unterhalb der gesetzlichen
Umsatzgrenzen kannst du darauf verzichten, Umsatzsteuer auszuweisen. Das
vereinfacht den Anfang erheblich. Zwei Dinge dazu:

- Die Grenzbetraege werden gelegentlich angepasst – den aktuellen Stand beim
  Finanzamt oder in der Beratung erfragen, nicht aus dem Netz uebernehmen.
- Du darfst dann auch keine Vorsteuer ziehen. Bei diesem Modell fallen kaum
  Ausgaben an, deshalb ist das hier fast immer der bessere Weg.

**Wichtig:** Verkaufst du ueber einen Haendler im eigenen Namen (siehe
`docs/BEZAHLUNG.md`), verkauft dieser an den Endkunden – nicht du. Deine
Einnahme ist dann eine Zahlung dieses Anbieters an dich. Das vereinfacht die
Umsatzsteuer erheblich, muss aber sauber verbucht werden. Genau hierzu lohnt
die eine Beratungsstunde.

---

## Sobald die Seite oeffentlich ist

**Impressum (§ 5 DDG, frueher TMG).** Pflicht fuer geschaeftsmaessige
Online-Angebote. Vollstaendiger Name, ladungsfaehige Anschrift (kein Postfach),
E-Mail-Adresse. Fehlt es, drohen Abmahnungen – und das ist der haeufigste und
unnoetigste Fehler beim Start.

Die Seite wird aus `tools.json` erzeugt:

```json
"betreiber": "Vorname Nachname",
"strasse": "Musterweg 1",
"plz_ort": "12345 Musterstadt",
"email": "kontakt@deine-domain.de"
```

    python3 build.py

`werkbank heute` weist dich so lange darauf hin, wie dort noch Platzhalter
stehen.

**Datenschutzerklaerung (Art. 13 DSGVO).** Ebenfalls Pflicht. Die erzeugte
Fassung deckt den aktuellen Zustand ab: Hosting bei GitHub Pages, lokale
Speicherung im Browser, keine Analysedienste.

**Sie muss erweitert werden, sobald du** einen Zahlungsanbieter einbindest,
Analysewerkzeuge einsetzt, einen Newsletter startest oder Schriftarten von
fremden Servern laedst. Der letzte Punkt ist der Grund, warum in diesem Projekt
ausschliesslich Systemschriften verwendet werden.

**Cookie-Hinweis.** Brauchst du hier **nicht**. Es werden keine Cookies zu
Analyse- oder Werbezwecken gesetzt, und die Speicherung von Darstellung und
Lizenzschluessel im Browser ist fuer den ausdruecklich gewuenschten Dienst
erforderlich. Das ist einer der angenehmen Nebeneffekte davon, alles lokal
rechnen zu lassen.

---

## Laufend

**Aufzeichnungen.** Einnahmen und Ausgaben sammeln, Belege aufbewahren. Bei
Kleinunternehmern reicht in der Regel die Einnahmenueberschussrechnung – eine
Tabelle genuegt am Anfang.

**Was du aufbewahren musst:** Abrechnungen des Zahlungsanbieters, Belege fuer
Domain und Werkzeuge, und eine Liste der verkauften Lizenzschluessel.

**Steuererklaerung.** Bei nebenberuflicher Taetigkeit kommt die Anlage G (oder
S bei Freiberuflichkeit) und die EUeR dazu. Ab dem ersten Umsatz relevant.

---

## Die kurze Liste

- [ ] Gewerbe angemeldet
- [ ] Fragebogen zur steuerlichen Erfassung ausgefuellt
- [ ] Entscheidung zur Kleinunternehmerregelung getroffen
- [ ] `tools.json` mit echten Daten gefuellt, `build.py` ausgefuehrt
- [ ] Impressum und Datenschutz auf der Seite erreichbar
- [ ] Getrenntes Konto fuer Einnahmen (kein Muss, aber es erspart viel Sortieren)
- [ ] Eine Stunde Steuerberatung, bevor der erste Euro fliesst

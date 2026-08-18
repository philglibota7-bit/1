# Geld annehmen

Die Entscheidung faellt frueh und ist schwer zu aendern. Deshalb hier
ausfuehrlich – und mit einer klaren Empfehlung.

---

## Die eine wichtige Entscheidung: wer verkauft?

Wenn du aus Deutschland an Privatpersonen in der EU verkaufst, faellt
Umsatzsteuer im **Land des Kaeufers** an. Verkaufst du digitale Produkte an
Kunden in acht Laendern, betrifft dich das grundsaetzlich in acht Steuersaetzen.
Dafuer gibt es das OSS-Verfahren beim Bundeszentralamt fuer Steuern – aber
melden, berechnen und abfuehren musst du selbst.

Es sei denn, jemand anderes ist der Verkaeufer.

**Haendler im eigenen Namen (Merchant of Record).** Anbieter wie Paddle, Polar
oder Lemon Squeezy verkaufen das Produkt rechtlich selbst an den Kunden und
zahlen dir den Erloes aus. Sie kuemmern sich um Umsatzsteuer in allen Laendern,
um Rechnungen an den Kunden und um Rueckbuchungen. Du bekommst eine einzige
Gutschrift.

**Reiner Zahlungsdienstleister.** Stripe wickelt nur die Zahlung ab. Steuer,
Rechnungen und Meldungen bleiben komplett bei dir.

| | Haendler im eigenen Namen | Stripe |
|---|---|---|
| Gebuehr | ca. 5 % + 0,50 € | ca. 1,5 % + 0,25 € |
| Umsatzsteuer EU | uebernimmt der Anbieter | deine Aufgabe |
| Rechnung an Kunden | uebernimmt der Anbieter | deine Aufgabe |
| Buchhaltung | eine Gutschrift im Monat | jede Zahlung einzeln |
| Aufwand am Anfang | ein Nachmittag | mehrere Tage |

**Empfehlung fuer den Start: Haendler im eigenen Namen.** Die drei Prozent
Mehrkosten sind das Guenstigste, was du je fuer gesparte Buchhaltung bezahlt
hast. Bei nennenswertem Umsatz kann sich der Wechsel zu Stripe rechnen – dann
aber mit Steuerberatung.

---

## Einrichtung in vier Schritten

**1. Konto anlegen** und Produkt erstellen: "Werkbank Pro", Einmalzahlung,
Preis wie in `tools.json` unter `pro_preis`.

**2. Kauflink eintragen** in `tools.json`:

```json
"pro_kauflink": "https://dein-anbieter.com/checkout/xyz"
```

Danach `python3 build.py` – die Pro-Seite und alle Kauffenster zeigen den Link.

**3. Schluessel ausliefern.** Nach jedem Kauf einen Schluessel erzeugen:

    werkbank schluessel --anzahl 1

und per E-Mail schicken. Bei den ersten Kaeufen von Hand – das dauert zwei
Minuten und du erfaehrst dabei mehr ueber deine Kunden als aus jeder Statistik.
Ab etwa zehn Kaeufen im Monat lohnt die Automatisierung ueber die
Bestaetigungs-E-Mail des Anbieters.

**4. Preis waehlen.** 19 € ist ein guter Startpunkt: hoch genug, dass sich der
Aufwand lohnt, niedrig genug fuer eine Entscheidung ohne Nachdenken. Erhoehe
erst, wenn regelmaessig gekauft wird. Zu niedrige Preise sind schwerer zu
korrigieren als zu hohe.

---

## Warum die Schranke im Browser sitzt

`Werkbank.lizenz.istPro()` prueft den Schluessel lokal. Das ist mit etwas
Wissen umgehbar, und das ist eine bewusste Entscheidung:

- Es kostet null Infrastruktur und funktioniert ab dem ersten Tag.
- Wer sie umgeht, haette ohnehin nicht bezahlt – dieser Umsatz ist nicht real.
- Ehrliche Kunden – und das sind fast alle, besonders Firmenkunden – zahlen.
- Ein Sicherungssystem zu bauen, bevor der erste Euro geflossen ist, ist die
  klassische Art, Monate zu verlieren.

**Wann es sich aendert:** sobald der Umsatz die Arbeit rechtfertigt. Dann
zeigt eine Variable auf einen kleinen Pruefdienst, und nur diese eine Funktion
aendert sich:

```js
window.WERKBANK_LIZENZ_ENDPUNKT = "https://dein-dienst/pruefe";
```

Der Dienst schlaegt den Schluessel in einer Liste nach und antwortet
`{"gueltig": true}`. Das laeuft kostenlos auf jeder der ueblichen
Funktionsplattformen. Alles andere im Code bleibt unveraendert – dafuer ist
die Abstraktion in `platform/werkbank.js` da.

---

## Rueckgaben

Bei digitalen Produkten erlischt das Widerrufsrecht nur, wenn der Kunde
ausdruecklich zustimmt und bestaetigt, dass er es dadurch verliert. Der
Haendler im eigenen Namen holt diese Zustimmung ueblicherweise selbst ein.

Unabhaengig davon: Gib das Geld anstandslos zurueck, wenn jemand fragt. Bei
19 € kostet dich jede Diskussion mehr, als der Betrag wert ist, und ein
zufriedener Nicht-Kunde erzaehlt anderen davon.

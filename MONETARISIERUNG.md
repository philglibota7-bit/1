# 💰 RechnungFix – So verdienst du Geld mit der Rechnungs-Website

Die Seite `rechnung.html` ist komplett betriebsfähig und wird nach dem Merge
automatisch über GitHub Pages veröffentlicht:

**Live-URL:** `https://philglibota7-bit.github.io/1/rechnung.html`

Alle Werbe- und Einnahme-Flächen sind eingebaut, aber **unsichtbar, solange du
keine IDs einträgst**. So wirkt die Seite für Besucher immer professionell.
Zum Aktivieren öffnest du `rechnung.html` und füllst oben den Block
`MONETIZATION` aus:

```js
const MONETIZATION = {
  adsenseClient: "",      // ← Google AdSense Publisher-ID
  paypalLink: "",         // ← dein PayPal.me-Link
  affiliateUrl: "",       // ← Affiliate-Link (z. B. sevDesk/Lexware)
  affiliateLabel: "Buchhaltung automatisieren – Software-Empfehlung ansehen",
  contactEmail: "philglibota7@gmail.com",
  imprintName: "",        // ← dein Name (Pflicht!)
  imprintAddress: ""      // ← deine Anschrift (Pflicht!)
};
```

---

## ⚠️ Zuerst: Impressum ausfüllen (Pflicht in Deutschland)

Eine geschäftlich betriebene Website – und das ist sie, sobald Werbung läuft –
braucht in Deutschland ein Impressum mit Name und ladungsfähiger Anschrift
(§ 5 DDG). Trage `imprintName` und `imprintAddress` ein, **bevor** du Werbung
aktivierst. Solange die Felder leer sind, zeigt die Impressum-Seite einen
Warnhinweis an.

---

## Einnahmequelle 1: Google AdSense (Werbung) – der Hauptweg

1. Konto erstellen auf https://adsense.google.com (kostenlos).
2. Website-URL angeben. *Tipp: Mit eigener Domain (siehe unten) wird die
   Freigabe deutlich leichter – AdSense akzeptiert `github.io`-Adressen oft nicht.*
3. Nach der Freigabe bekommst du eine Publisher-ID im Format `ca-pub-1234567890123456`.
4. Diese ID bei `adsenseClient` eintragen, committen, fertig. Die zwei
   vorbereiteten Anzeigenflächen (oben und unter dem Generator) werden aktiv.

**Wichtig – Einwilligung für EU-Besucher:** Für Nutzer aus dem EWR und
Großbritannien verlangt Google einen zertifizierten Consent-Banner. Baue dafür
**keinen eigenen** – aktiviere stattdessen in AdSense unter
*Datenschutz und Meldungen → DSGVO-Meldung* die Google-eigene Meldung. Sie ist
kostenlos, zertifiziert und erscheint automatisch. Ein selbstgebauter Banner
würde nur doppelt angezeigt und wäre trotzdem nicht ausreichend.

**Verdienst:** typischerweise 1–5 € pro 1.000 Besucher, bei Finanz- und
Business-Themen oft mehr.

## Einnahmequelle 2: Affiliate-Links (höchstes Potenzial)

Buchhaltungssoftware-Anbieter zahlen hohe Provisionen pro vermitteltem Kunden
(oft 20–50 € oder mehr). Die Seite hat dafür bereits eine Empfehlungs-Box
unter der Vorschau eingebaut.

1. Bei einem Partnerprogramm anmelden, z. B. **sevDesk**, **Lexware Office**
   (über Netzwerke wie AWIN), **Billomat** oder **FastBill**.
2. Deinen persönlichen Affiliate-Link bei `affiliateUrl` eintragen.
3. Optional den Button-Text über `affiliateLabel` anpassen.

Der Link ist bereits korrekt mit `rel="sponsored"` ausgezeichnet, wie Google es
für Werbelinks verlangt.

## Einnahmequelle 3: Freiwillige Unterstützung (PayPal)

1. Kostenlosen Link erstellen auf https://paypal.me
2. Link (z. B. `https://paypal.me/deinname`) bei `paypalLink` eintragen.
3. Unter der Vorschau erscheint automatisch eine dezente „Unterstützen“-Box.

Alternativ funktionieren auch Links von https://ko-fi.com oder
https://buymeacoffee.com an derselben Stelle.

---

## 🚀 Mehr Besucher = mehr Einnahmen

Ohne Besucher kein Umsatz. Die Seite bringt dafür schon einiges mit:
Meta-Tags, Open Graph, strukturierte Daten (`WebApplication` und `FAQPage` für
Rich Snippets in der Google-Suche), einen ausführlichen Ratgeber-Text und einen
FAQ-Bereich. Zusätzlich lohnt sich:

1. **Eigene Domain (dringend empfohlen, ~10 €/Jahr):** z. B. `rechnungfix.de`.
   Wirkt seriöser, ist praktisch Voraussetzung für die AdSense-Freigabe und für
   gute Google-Rankings. Einrichtung: Repo → Settings → Pages → Custom domain,
   dann beim Domain-Anbieter einen CNAME auf `philglibota7-bit.github.io` setzen.
   Danach bitte auch das `<link rel="canonical">` im `<head>` anpassen.
2. **Google Search Console:** Seite kostenlos anmelden, damit Google sie
   indexiert: https://search.google.com/search-console
3. **Verbreitung:** Freelancer- und Gründerforen, Facebook-Gruppen für
   Selbstständige, Reddit (r/selbststaendig), Kleinunternehmer-Communities.
   Kurze Erklärvideos (TikTok/YouTube Shorts: „Rechnung schreiben in 2 Minuten –
   kostenlos“) bringen erfahrungsgemäß viel Traffic.
4. **Auf die Keywords setzen, die die Seite schon abdeckt:** Neben „Rechnung
   schreiben“ ranken auch „Angebot erstellen“, „Lieferschein Vorlage“,
   „Mahnung schreiben“ und „E-Rechnung“ – jeder Dokumenttyp ist ein eigener
   Suchbegriff mit eigener Zielgruppe.

---

## Was die Website kann (alles bereits fertig eingebaut)

**Fünf Dokumenttypen** mit je eigener Nummernfolge und passenden Standardtexten:
Rechnung, Angebot, Lieferschein, Stornorechnung und Zahlungserinnerung.

**Rechnen und Recht**
- Alle Pflichtangaben nach § 14 UStG
- MwSt.-Berechnung mit frei wählbarem Satz (19 %, 7 %, 0 %, auch 20 %/10 % für
  Österreich und 8,1 % für die Schweiz), getrennt nach Steuersatz ausgewiesen
- Kleinunternehmerregelung § 19 UStG per Klick inkl. Pflichthinweis
- Rabatt (prozentual oder als fester Betrag), Anzahlungen und Skonto mit
  automatisch berechneter Frist
- Mahngebühr bei Zahlungserinnerungen, negative Beträge bei Stornorechnungen
- Vier Währungen: Euro, Franken, Dollar, Pfund

**Zahlung und Export**
- **GiroCode**: QR-Code nach EPC-Standard, den Kunden mit der Banking-App
  scannen – IBAN, Betrag und Verwendungszweck sind sofort ausgefüllt
- IBAN-Prüfziffernkontrolle nach Modulo 97 direkt bei der Eingabe
- PDF-Export im DIN-A4-Format über den Druckdialog, auch mehrseitig mit
  wiederholtem Tabellenkopf und korrekten Seitenrändern
- **E-Rechnung als XML** im Standard XRechnung 3.0, geprüft mit dem offiziellen
  KoSIT-Validator
- Warnung, wenn eine Rechnungsnummer im Archiv bereits vergeben ist
- Beträge lassen sich mit Komma eingeben („85,50“) und werden cent-genau
  gerundet, sodass Einzelposten und Summen immer exakt zusammenpassen

**Komfort**
- Archiv: Dokumente speichern, wieder laden, duplizieren, löschen
- Kundenverwaltung mit Autovervollständigung der Adresse
- Backup: alle Daten als JSON-Datei sichern und auf einem anderen Gerät einlesen
- Logo-Upload, sechs Akzentfarben, Positionen frei sortierbar
- Live-Vorschau im A4-Format, automatisches Speichern im Browser

**Technik**
- 100 % clientseitig → keine Serverkosten, DSGVO-freundlich, skaliert gratis
- Keine externen Abhängigkeiten: keine CDN, keine Tracker, funktioniert offline
- Impressum und Datenschutzerklärung eingebaut

**Laufende Kosten: 0 €** (GitHub Pages ist kostenlos) – jede Einnahme ist Gewinn.

---

## Hinweis zur E-Rechnung (XML-Export)

Der XML-Export erzeugt eine strukturierte Rechnung im Standard **XRechnung 3.0**
(UBL 2.1 nach EN 16931). Für Stornorechnungen wird automatisch eine Gutschrift
(`CreditNote`, Typcode 381) erzeugt.

Die Ausgabe wurde mit dem **offiziellen Validator der KoSIT**
(Koordinierungsstelle für IT-Standards, Konfiguration XRechnung 3.0.2) geprüft –
in acht Varianten: Standardrechnung, Kleinunternehmer, zwei Steuersätze,
krummer Prozentrabatt, Anzahlung, Storno, Rechnung mit 23 Positionen und ein
Kunde in Österreich. Alle acht werden mit dem Ergebnis *ACCEPTABLE* akzeptiert
(Schema und Schematron bestanden).

Damit das gelingt, verlangt der Standard ein paar Angaben mehr als eine
Papierrechnung: E-Mail-Adressen beider Seiten, einen Ansprechpartner mit
Telefonnummer und eine Kundenreferenz (bei Behörden die Leitweg-ID). Fehlt
etwas, nennt das Tool beim Export genau das fehlende Feld und markiert es.

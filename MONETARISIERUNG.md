# 💰 RechnungFix – So verdienst du Geld mit der Rechnungs-Website

Die Website `rechnung.html` ist komplett betriebsfähig und wird nach dem Merge
automatisch über GitHub Pages veröffentlicht:

**Live-URL:** `https://philglibota7-bit.github.io/1/rechnung.html`

Alle Werbe- und Einnahme-Flächen sind bereits eingebaut, aber **unsichtbar,
solange du keine IDs einträgst**. So wirkt die Seite für Besucher immer
professionell. Zum Aktivieren öffnest du `rechnung.html` und füllst oben den
Block `MONETIZATION` aus:

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

Eine geschäftlich betriebene Website (und das ist sie, sobald Werbung läuft)
braucht in Deutschland ein Impressum mit Name und ladungsfähiger Anschrift
(§ 5 DDG). Trage `imprintName` und `imprintAddress` ein, **bevor** du Werbung
aktivierst. Die Impressum- und Datenschutz-Seiten sind bereits eingebaut und
zeigen deine Angaben automatisch an.

---

## Einnahmequelle 1: Google AdSense (Werbung) – der Hauptweg

1. Konto erstellen auf https://adsense.google.com (kostenlos).
2. Deine Website-URL angeben: `https://philglibota7-bit.github.io/1/rechnung.html`
   *(Tipp: Mit eigener Domain, siehe unten, wird die Freigabe deutlich leichter –
   AdSense akzeptiert Subdomain-Seiten wie github.io oft nicht.)*
3. Nach der Freigabe bekommst du eine Publisher-ID im Format `ca-pub-1234567890123456`.
4. Diese ID in `rechnung.html` bei `adsenseClient` eintragen, committen, fertig.
   Die zwei vorbereiteten Anzeigenflächen (oben + unter dem Generator) werden
   automatisch aktiv.

**Verdienst:** typischerweise 1–5 € pro 1.000 Besucher, bei Finanz-Themen oft mehr.

## Einnahmequelle 2: Affiliate-Links (höchstes Potenzial)

Buchhaltungssoftware-Anbieter zahlen hohe Provisionen pro vermitteltem Kunden
(oft 20–50 € oder mehr). Die Seite hat dafür bereits eine Empfehlungs-Box
("Sie schreiben regelmäßig Rechnungen?") eingebaut.

1. Bei einem Partnerprogramm anmelden, z. B.:
   - **sevDesk** Partnerprogramm
   - **Lexware Office** (früher Lexoffice) über Netzwerke wie AWIN
   - **Billomat**, **FastBill** u. a.
2. Deinen persönlichen Affiliate-Link bei `affiliateUrl` eintragen.
3. Optional den Button-Text über `affiliateLabel` anpassen.

## Einnahmequelle 3: Freiwillige Unterstützung (PayPal)

1. Kostenlosen Link erstellen auf https://paypal.me
2. Link (z. B. `https://paypal.me/deinname`) bei `paypalLink` eintragen.
3. Unter der Rechnungs-Vorschau erscheint dann automatisch eine dezente
   "Unterstützen"-Box.

Alternativ funktioniert auch ein Link von https://ko-fi.com oder
https://buymeacoffee.com – einfach dieselbe Stelle verwenden.

---

## 🚀 Mehr Besucher = mehr Einnahmen

Ohne Besucher kein Umsatz. Die Seite ist bereits SEO-optimiert (Meta-Tags,
strukturierte Daten, deutsche Keywords wie „Rechnung schreiben kostenlos“).
Zusätzlich lohnt sich:

1. **Eigene Domain (dringend empfohlen, ~10 €/Jahr):**
   z. B. `rechnungfix.de` – wirkt seriöser, ist Voraussetzung für gute
   AdSense-Freigabe und Google-Rankings.
   Einrichtung: Repo → Settings → Pages → Custom domain, dann beim
   Domain-Anbieter einen CNAME auf `philglibota7-bit.github.io` setzen.
2. **Google Search Console:** Seite anmelden (kostenlos), damit Google sie
   indexiert: https://search.google.com/search-console
3. **Verbreitung:** In Freelancer-/Gründer-Foren, Facebook-Gruppen für
   Selbstständige, Reddit (r/selbststaendig), Kleinunternehmer-Communities
   teilen. Kurze Erklärvideos (TikTok/YouTube Shorts: „Rechnung schreiben in
   2 Minuten – kostenlos“) bringen erfahrungsgemäß viel Traffic.

---

## Was die Website kann (alles bereits fertig eingebaut)

- Professionelle Rechnungen mit allen Pflichtangaben nach § 14 UStG
- Automatische MwSt.-Berechnung (19 % / 7 % / 0 %, getrennt ausgewiesen)
- Kleinunternehmerregelung § 19 UStG per Klick inkl. Pflichthinweis
- Logo-Upload und 6 Farbdesigns
- Live-Vorschau im DIN-A4-Format + PDF-Export (über den Browser-Druckdialog)
- Automatisches Speichern im Browser, fortlaufende Rechnungsnummern
- 100 % clientseitig → keine Serverkosten, DSGVO-freundlich, skaliert gratis
- Impressum & Datenschutzerklärung eingebaut
- SEO: Meta-Tags, Open Graph, Schema.org, FAQ-Bereich

**Laufende Kosten: 0 €** (GitHub Pages ist kostenlos) – jede Einnahme ist Gewinn.

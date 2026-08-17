---
category: Folien
---

# ClosingSlide — Abschlussfolie

Dank, optionaler Schlusssatz, Kontaktkarte. Diese Folie bleibt während der
Diskussion stehen — deshalb gehören die Kontaktdaten hierher.

## Verwendung

```jsx
<ClosingSlide
  title="Vielen Dank für Ihre Aufmerksamkeit"
  message="Für Rückfragen zu den Kennzahlen stehe ich gern zur Verfügung."
  contact={{
    name: "Dr. med. Andrea Vogt",
    role: "Leitung Qualitätsmanagement",
    department: "Die Kliniken Landkreis Schwäbisch Hall",
    email: "andrea.vogt@kliniken-sha.de",
    phone: "0791 753-1420",
  }}
/>
```

## Hinweise

- `title` hat einen Standardtext („Vielen Dank für Ihre Aufmerksamkeit“) und kann
  überschrieben werden — etwa mit der Kernbotschaft oder der offenen Frage an das
  Gremium.
- `message` eignet sich für die Einladung zur Diskussion oder den nächsten
  Schritt („Beschlussvorschlag siehe Anlage 3“).
- Die Kontaktkarte nur mit Daten füllen, die tatsächlich genutzt werden sollen;
  eine kurze Karte wirkt aufgeräumter als eine vollständige.
- `tone="blue"` passt, wenn auch die Titelfolie blau ist — Anfang und Ende
  rahmen den Vortrag dann sichtbar ein.

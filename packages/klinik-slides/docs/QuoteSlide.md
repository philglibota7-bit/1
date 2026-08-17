---
category: Folien
---

# QuoteSlide — Zitatfolie

Eine Stimme, eine Aussage, sonst nichts. Wirkt als Ruhepunkt zwischen
datenlastigen Folien am stärksten.

## Verwendung

```jsx
<QuoteSlide
  quote="Die neue Ersteinschätzung hat unsere Wartezeiten in der Notaufnahme sichtbar verkürzt — das merken die Patienten sofort."
  author="Sabine Wolf"
  role="Pflegedirektion, Klinikum Crailsheim"
  footerLabel="Qualitätsbericht 2025"
  pageNumber={12}
/>
```

## Hinweise

- `quote` ohne Anführungszeichen übergeben — das große Anführungszeichen setzt
  die Folie selbst.
- Zwei bis drei Zeilen sind das Maximum. Längere Zitate kürzen und die Auslassung
  mit „…“ kennzeichnen, statt die Schrift zu verkleinern.
- `role` beantwortet, warum diese Stimme zählt: Funktion oder Erhebung
  („Patientenbefragung 2025, n = 412“).
- `tone="blue"` für den stärkeren Auftritt, etwa als Übergang in ein neues
  Kapitel.

---
category: Folien
---

# TitleSlide — Titelfolie

Erste Folie jeder Präsentation: Anlass, Thema, Untertitel, dann die Angaben zu
Person, Datum und Ort. Das Logo sitzt oben rechts, die rote Akzentlinie über dem
Titel ist das Markenzeichen des Foliensatzes.

## Verwendung

```jsx
<TitleSlide
  kicker="Chefarztkonferenz"
  title="Qualitätsbericht 2025"
  subtitle="Kennzahlen, Entwicklungen und Schwerpunkte für das kommende Jahr"
  speaker="Dr. med. Andrea Vogt"
  role="Leitung Qualitätsmanagement"
  date="12. März 2026"
  place="Klinikum Crailsheim"
/>
```

## Hinweise

- `title` ist die größte Zeile der ganzen Präsentation — ein Thema, keine
  Satzkonstruktion. Untertitel trägt die Erläuterung.
- `kicker` benennt den Anlass („Chefarztkonferenz“, „Aufsichtsratssitzung“),
  nicht das Thema.
- `variant="blue"` ergibt eine tiefblaue Titelfolie. Wirkt in abgedunkelten
  Räumen stärker; im Rest des Foliensatzes dann sparsam bleiben, sonst verliert
  der Wechsel seine Wirkung.
- `logoSrc` mit der offiziellen Logodatei belegen. Ohne `logoSrc` erscheint die
  Textmarke als Platzhalter.
- Kontaktdaten gehören nicht hierher, sondern auf `ClosingSlide` — die Folie,
  die während der Diskussion stehen bleibt.

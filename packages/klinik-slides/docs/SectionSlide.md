---
category: Folien
---

# SectionSlide — Kapiteltrenner

Markiert den Themenwechsel und zeigt dem Publikum, wo im Vortrag es sich
befindet. Nur Kapitelnummer, Kapitelname und ein Satz Erläuterung.

## Verwendung

```jsx
<SectionSlide
  index={2}
  total={5}
  title="Leistungsentwicklung"
  subtitle="Fallzahlen, Verweildauer und Auslastung im Fünfjahresvergleich"
  tone="light"
/>
```

## Hinweise

- `index` und `total` ergeben zusammen „02 / 05“ — einstellige Zahlen werden
  automatisch mit führender Null gesetzt.
- Farbtöne: `light` (zartblau, Standard) für den Regelfall, `blue` (tiefblau)
  für den Auftakt eines gewichtigen Blocks, `band` (weiß mit rotem Seitenband)
  als ruhigste Variante.
- Ein Kapiteltrenner pro Kapitel. Bei einem Vortrag unter zehn Minuten meist
  ganz verzichtbar.
- Keine Inhalte auf dieser Folie — sie ist eine Atempause, keine Agenda. Für
  eine Gliederung eine `ContentSlide` mit `BulletList marker="number"` nehmen.

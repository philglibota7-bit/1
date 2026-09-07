---
category: Folien
---

# ContentSlide — Inhaltsfolie

Der Arbeitsfolientyp: Überschrift, optionaler Einleitungssatz, Inhaltsbereich mit
ein bis drei Spalten, Fußnote und Fußzeile. Praktisch jede Folie zwischen Titel
und Abschluss ist eine `ContentSlide`.

## Verwendung

```jsx
<ContentSlide
  kicker="Kapitel 2 — Leistungsentwicklung"
  title="Die Fallzahlen wachsen, die Verweildauer sinkt weiter"
  lead="Beide Entwicklungen zusammen erklären die höhere Auslastung bei gleicher Bettenzahl."
  columns={3}
  footnote="Datenstand 31.12.2025, ohne ambulante Fälle."
  footerLabel="Qualitätsbericht 2025"
  pageNumber={7}
>
  <KpiTile label="Stationäre Fälle" value="12.480" delta="+4,2 %" trend="up" tone="blue" />
  <KpiTile label="Verweildauer" value="4,3" unit="Tage" delta="−0,3 Tage" trend="down" tone="positive" />
  <KpiTile label="Bettenauslastung" value="87,6" unit="%" delta="+2,1 pp" trend="up" />
</ContentSlide>
```

## Hinweise

- Die Überschrift trägt die Aussage: „Die Fallzahlen wachsen, die Verweildauer
  sinkt weiter“ statt „Leistungsentwicklung“. Das Publikum liest die Überschrift
  zuerst — sie soll den Punkt schon machen.
- `columns={2}` und `{3}` legen ein Raster; jedes direkte Kind füllt eine Spalte.
  Für ungleiche Aufteilungen `columns={1}` verwenden und im Inhalt ein eigenes
  Grid mit `gap: var(--k-sp-6)` aufbauen.
- `lead` ist ein Satz, keine zweite Überschrift. Bei Kennzahlenfolien meist der
  Satz, der die Zahlen einordnet.
- `footnote` für Datenstand, Definition oder Abgrenzung — Rückfragen aus dem
  Publikum entstehen fast immer genau hier.
- `variant="muted"` (zartblau) trennt Abschnitte optisch, ohne die Farbwelt zu
  verlassen; `variant="blue"` für einzelne Betonungsfolien.

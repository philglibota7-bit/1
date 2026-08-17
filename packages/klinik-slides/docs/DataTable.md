---
category: Inhalte
---

# DataTable — Tabelle

Kennzahlen je Fachabteilung, Standort oder Zeitraum. Mit Spaltenausrichtung,
Hervorhebung einzelner Zeilen und Summenzeile.

## Verwendung

```jsx
<DataTable
  caption="Fallzahlen je Fachabteilung"
  columns={[
    { key: "abt", label: "Fachabteilung", width: "34%" },
    { key: "fa2024", label: "2024", align: "right" },
    { key: "fa2025", label: "2025", align: "right" },
    { key: "delta", label: "Veränderung", align: "right" },
  ]}
  rows={[
    { abt: "Innere Medizin", fa2024: "3.812", fa2025: "4.015", delta: "+5,3 %" },
    { abt: "Chirurgie", fa2024: "2.964", fa2025: "3.102", delta: "+4,7 %" },
    { abt: "Geriatrie", fa2024: "1.240", fa2025: "1.198", delta: "−3,4 %" },
  ]}
  highlightRows={[0]}
  totalRow={{ abt: "Gesamt", fa2024: "11.976", fa2025: "12.480", delta: "+4,2 %" }}
  source="Quelle: Medizincontrolling, Stand 31.12.2025"
  zebra
/>
```

## Hinweise

- **Höhenbudget:** mit Überschrift und Fußzeile passen etwa **sechs Datenzeilen
  plus Summenzeile** auf eine Folie, mit `dense` etwa acht. Jede zusätzliche
  Angabe kostet eine Zeile: Einleitungssatz, Fußnote, Quellenzeile,
  Hinweisbox darunter. Mehr Zeilen werden am Folienrand abgeschnitten —
  lieber aufteilen oder auf `BarChart` wechseln.
- Sechs Spalten sind die Obergrenze, danach wird die Schrift für den Saal zu klein.
- Zahlenspalten immer `align: "right"` — dann fluchten die Ziffern, die Schrift
  läuft ohnehin mit gleichbreiten Ziffern.
- `highlightRows` (Index ab 0) für die Zeile, um die es im Vortrag geht;
  `totalRow` für Summen, damit die Summe nicht als normale Datenzeile gelesen wird.
- `dense` ab etwa acht Zeilen, `zebra` bei vielen Spalten — beides zusammen wirkt
  schnell unruhig.
- `source` ausfüllen: bei Klinikkennzahlen ist die Quelle die erste Rückfrage
  aus dem Publikum.

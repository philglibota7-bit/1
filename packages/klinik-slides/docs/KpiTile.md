---
category: Inhalte
---

# KpiTile — Kennzahlen-Kachel

Eine Kennzahl mit Beschriftung, Einheit, Veränderung und Bezugsgröße. Drei
Kacheln in einer `ContentSlide columns={3}` ergeben eine vollständige
Kennzahlenfolie.

## Verwendung

```jsx
<ContentSlide title="Leistungszahlen 2025 im Überblick" columns={3}>
  <KpiTile label="Stationäre Fälle" value="12.480" delta="+4,2 %" trend="up" tone="blue"
           footnote="Vorjahr: 11.976" />
  <KpiTile label="Verweildauer" value="4,3" unit="Tage" delta="−0,3 Tage" trend="down" tone="positive"
           footnote="Zielwert: 4,5 Tage" />
  <KpiTile label="Offene Pflegestellen" value="34" delta="+6" trend="up" tone="warning"
           footnote="Stand 31.12.2025" />
</ContentSlide>
```

## Hinweise

- Richtung und Bewertung sind getrennt: `trend` zeigt nur, wohin sich der Wert
  bewegt, `tone` bewertet. Eine sinkende Verweildauer ist ein Erfolg
  (`trend="down"`, `tone="positive"`), eine sinkende Fallzahl nicht.
- Farben: `blue` für die Leitkennzahl der Folie, `positive` für Zielerreichung,
  `warning` für Handlungsbedarf, `accent` (Rot) nur für die eine Zahl, die im
  Vortrag hängen bleiben soll, `neutral` für alles Übrige.
- Werte deutsch formatiert übergeben: Tausenderpunkt, Dezimalkomma
  („12.480“, „4,3“).
- `footnote` trägt die Bezugsgröße (Vorjahr, Zielwert, Datenstand) — ohne sie ist
  eine Veränderung nicht interpretierbar.
- Drei bis vier Kacheln pro Folie. Mehr Kennzahlen gehören in eine `DataTable`.

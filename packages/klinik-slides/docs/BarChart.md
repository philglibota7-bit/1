---
category: Inhalte
---

# BarChart — Balken- und Säulendiagramm

Diagramm ohne Diagrammbibliothek, rein aus CSS. Sieht dadurch in Vorschau,
Vollbild und Ausdruck identisch aus. Gehört in einen `ChartFrame`.

## Verwendung

Säulen für Verläufe über die Zeit, mit Ziellinie:

```jsx
<BarChart
  data={[
    { label: "2021", value: 78.2 },
    { label: "2022", value: 81.4 },
    { label: "2023", value: 83.9 },
    { label: "2024", value: 85.5 },
    { label: "2025", value: 87.6, tone: "accent" },
  ]}
  unit=" %"
  target={85}
  targetLabel="Ziel 85 %"
/>
```

Balken für Vergleiche zwischen Abteilungen:

```jsx
<BarChart
  orientation="horizontal"
  data={[
    { label: "Innere Medizin", value: 4015 },
    { label: "Chirurgie", value: 3102 },
    { label: "Geriatrie", value: 1198, tone: "muted" },
  ]}
/>
```

## Hinweise

- `vertical` (Standard) für Zeitreihen, `horizontal` für Rangfolgen — dort sind
  die Beschriftungen lesbar, auch wenn sie lang sind.
- `tone: "accent"` auf genau einem Balken: der, über den gesprochen wird.
  `muted` für Vergleichs- oder Vorjahreswerte.
- Werte werden deutsch formatiert (Dezimalkomma). Eigene Formatierung über
  `display` je Datenpunkt.
- `target` mit `targetLabel` zeigt Ziel- oder Referenzwerte — bei
  Qualitätsindikatoren fast immer die eigentliche Botschaft.
- Höchstens etwa acht Säulen; darüber werden die Beschriftungen zu eng.
- Ohne `max` skaliert die Achse auf den größten Wert plus Luft. `max` setzen,
  wenn zwei Diagramme auf einer Folie vergleichbar sein sollen.

---
category: Inhalte
---

# ChartFrame — Diagramm-Rahmen

Rahmen für Diagramme: Titel, Legende, Zeichenfläche, Erläuterung, Quelle.
Nimmt `BarChart` oder eigenes SVG auf.

## Verwendung

```jsx
<ChartFrame
  title="Stationäre Fälle je Quartal"
  legend={[{ label: "2025" }, { label: "2024", color: "var(--k-blue-200)" }]}
  caption="Das vierte Quartal trägt den Zuwachs — Grippewelle und zwei zusätzliche Belegbetten."
  source="Quelle: Medizincontrolling, Stand 31.12.2025"
  height="20cqw"
>
  <BarChart
    data={[
      { label: "Q1", value: 2980 },
      { label: "Q2", value: 3040 },
      { label: "Q3", value: 3080 },
      { label: "Q4", value: 3380, tone: "accent" },
    ]}
  />
</ChartFrame>
```

## Hinweise

- `caption` trägt die **Aussage** des Diagramms, nicht die Beschreibung der
  Achsen: „Das vierte Quartal trägt den Zuwachs“ statt „Fälle je Quartal“.
- `height` in `cqw` angeben (z. B. `"20cqw"`), damit die Zeichenfläche mit der
  Folie skaliert. Feste Pixelhöhen brechen die Skalierung in der Vorschau.
- Legendenfarben aus den Tokens setzen (`var(--k-blue)`, `var(--k-blue-200)`,
  `var(--k-red)`) — nur so bleiben Diagramm und Foliensatz farblich eine Einheit.
- Zwei Diagramme nebeneinander funktionieren in `ContentSlide columns={2}`, dann
  `height` reduzieren (etwa `"16cqw"`).
- `source` ausfüllen — sie beantwortet die erste Rückfrage, bevor sie gestellt wird.

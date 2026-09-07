---
category: Inhalte
---

# BulletList — Aufzählung

Aufzählung mit Klinik-Aufzählungszeichen und optionaler grauer Zweitzeile je
Punkt. Der häufigste Inhaltsbaustein.

## Verwendung

```jsx
<BulletList
  marker="check"
  items={[
    { text: "Zentrale Ersteinschätzung nach Manchester-Triage", detail: "Eingeführt in allen drei Häusern seit Mai 2025" },
    { text: "Verkürzte Wartezeit bis zum Arztkontakt", detail: "Median 18 Minuten, vorher 34 Minuten" },
    { text: "Gemeinsame Rufbereitschaft der Fachabteilungen" },
  ]}
/>
```

Kurze, tragende Aussagen ohne Details:

```jsx
<BulletList size="lg" marker="arrow" items={["Qualität sichern", "Wege verkürzen", "Personal binden"]} />
```

## Hinweise

- Höchstens sechs Punkte pro Folie, pro Punkt eine Aussage. Was Erklärung
  braucht, gehört in `detail`, nicht in einen längeren Hauptsatz.
- **Höhenbudget:** sechs Punkte gelten *ohne* Zweitzeilen. Mit `detail` an jedem
  Punkt passen **vier bis fünf**, und ein `lead` an der Folie kostet einen
  weiteren Punkt. Überzähliges wird am Folienrand abgeschnitten.
- Aufzählungszeichen: `check` für Erreichtes und Maßnahmen, `number` für Abläufe
  und Reihenfolgen, `arrow` für Schlussfolgerungen, `dot` für neutrale Listen.
- `columns={2}` erst ab etwa sechs Punkten — vorher entsteht nur eine Lücke.
- `size="lg"` für drei bis vier tragende Aussagen; mit vielen Punkten wird die
  Folie damit zu voll.
- `tone: "muted"` nimmt einzelne Punkte optisch zurück (z. B. „noch offen“),
  `tone: "accent"` hebt einen Punkt in Klinik-Blau hervor.

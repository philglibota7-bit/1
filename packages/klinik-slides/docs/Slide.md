---
category: Folien
---

# Slide — freier Folienrahmen

Der 16:9-Rahmen mit Kopf- und Fußbereich, auf dem alle anderen Folientypen
aufbauen. Richtige Wahl, wenn kein spezialisierter Folientyp passt: Bildfolien,
Vollflächen-Layouts, Schaubilder, Vergleiche mit eigenem Raster.

## Verwendung

```jsx
<Slide
  kicker="Ausgangslage"
  title="Drei Häuser, eine gemeinsame Notaufnahme-Struktur"
  footerLabel="Strukturkonzept 2026"
  pageNumber={4}
  showLogo
>
  <div style={{ display: "grid", gridTemplateColumns: "1.4fr 1fr", gap: "var(--k-sp-6)" }}>
    <BulletList items={["Zentrale Ersteinschätzung", "Gemeinsame Rufbereitschaft"]} />
    <Callout title="Beschluss" tone="info">Umsetzung ab Q3 2026.</Callout>
  </div>
</Slide>
```

## Hinweise

- Der Folienrahmen ist der Skalierungs-Container: alles darin ist in `cqw`
  bemessen und wächst proportional mit der Folienbreite. Inhaltsbausteine daher
  immer **innerhalb** einer Folie verwenden, nie freistehend.
- `flush` entfernt den Innenabstand — für randlose Bild- oder Farbflächen.
- `align="center"` zentriert den Inhalt vertikal, sinnvoll bei einer einzelnen
  Aussage oder einem Schaubild.
- `decor` legt eine dezente Schmuckfläche unten rechts an; auf datenreichen
  Folien besser weglassen. Auf `variant="blue"` ist sie bewusst unterdrückt.
- **Höhenbudget:** unter dem Kopfbereich bleiben etwa 40–43 cqw Höhe. Ein
  zweizeiliger Titel kostet rund 4,5 cqw. Wird es mehr, schneidet die Folie den
  Überlauf **lautlos ab** (`overflow: hidden`) — Summenzeilen und Quellenangaben
  verschwinden dann zuerst. Faustregel: KPI-Reihe **oder** Tabelle mit
  Summenzeile, nicht beides auf einer Folie.
- Eigene Layout-Glue-Elemente mit den Abstands-Tokens (`var(--k-sp-6)`) bauen,
  nicht mit festen Pixelwerten — sonst bricht die proportionale Skalierung.

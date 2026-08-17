# Klinik-Präsentation — so wird mit diesem Design-System gebaut

Ein Präsentations-Baukasten im Corporate Design der Kliniken Landkreis
Schwäbisch Hall. Alles, was gebaut wird, ist eine **Folie im Format 16:9** —
keine Web-Seite, kein Dashboard. Sprache der Inhalte: **Deutsch**.

## Aufbau und Einbindung

Kein Provider, kein Theme-Wrapper, kein Kontext. Nur das Stylesheet einbinden,
dann die Komponenten verwenden:

```jsx
import "@klinik-sh/slides/styles.css";
import { TitleSlide, ContentSlide, KpiTile, Callout } from "@klinik-sh/slides";
```

Das Stylesheet bringt Tokens, Komponenten-Regeln und die mitgelieferte Schrift
**Inter** (selbst gehostet, keine externe Verbindung nötig).

**Die eine Regel, die man kennen muss: der Folienrahmen ist der
Skalierungs-Container.** Jede Folie (`Slide`, `TitleSlide`, `SectionSlide`,
`ContentSlide`, `QuoteSlide`, `ClosingSlide`) setzt `container-type: inline-size`,
und alle Größen im System sind in `cqw` notiert. Dadurch skaliert eine Folie
proportional: als Vollbild, als kleine Vorschaukarte, im Ausdruck.

Daraus folgt: **Inhaltsbausteine niemals freistehend rendern.** `KpiTile`,
`BulletList`, `DataTable`, `Callout`, `ChartFrame`, `BarChart` und `KlinikLogo`
gehören immer in eine Folie. Freistehend beziehen sich ihre `cqw`-Größen auf den
Viewport und sie werden winzig oder riesig.

## Der Gestaltungs-Idiom: Tokens, keine eigenen Klassen

Die Komponenten bringen ihre Klassen selbst mit (alle mit `ksl-` präfixiert).
**Diese Klassen nicht selbst schreiben und nicht überschreiben** — sie sind
Implementierungsdetail. Für eigene Layout-Elemente (Spalten, Stapel, Raster)
`style={{ … }}` mit **Tokens** verwenden. Es gibt keine Utility-Klassen in
diesem System.

| Familie | Tokens (vollständig) |
|---|---|
| Marke Blau | `--k-blue` (Primär), `--k-blue-900` `--k-blue-800` `--k-blue-600` `--k-blue-400` `--k-blue-200` `--k-blue-100` `--k-blue-50` |
| Marke Rot (Akzent) | `--k-red`, `--k-red-700`, `--k-red-100`, `--k-red-50` |
| Text und Linien | `--k-ink` `--k-ink-700` `--k-ink-500` `--k-ink-300`, `--k-line`, `--k-line-strong`, `--k-surface`, `--k-surface-muted` |
| Status | `--k-ok` `--k-ok-50`, `--k-warn` `--k-warn-50`, `--k-crit` `--k-crit-50` |
| Schrift | `--k-font`, `--k-fs-display` `--k-fs-h1` `--k-fs-h2` `--k-fs-h3` `--k-fs-body` `--k-fs-small` `--k-fs-caption` `--k-fs-eyebrow` `--k-fs-kpi`, `--k-lh-tight` `--k-lh-heading` `--k-lh-body`, `--k-tracking-eyebrow`, `--k-weight-regular` `--k-weight-medium` `--k-weight-semibold` `--k-weight-bold` |
| Abstände | `--k-sp-1` … `--k-sp-8` (4 px … 64 px bei Folienbreite 1280) |
| Formen | `--k-radius-sm` `--k-radius` `--k-radius-lg`, `--k-border`, `--k-rule`, `--k-shadow-soft`, `--k-shadow` |
| Folienmaß | `--k-slide-ratio`, `--k-slide-max`, `--k-slide-px`, `--k-slide-py` |

Eigene Maße immer relativ (`cqw`) oder über Tokens — **keine festen
Pixelwerte**, die brechen die proportionale Skalierung der Folie.

## Gestaltungsregeln des Hauses

- **Blau trägt, Rot ist Akzent.** Rot markiert genau eine Sache pro Folie: die
  Zahl, den Balken, die Warnung. Flächiges Rot gibt es nicht.
- **Eine Aussage pro Folie, und sie steht in der Überschrift** — als Satz
  („Mehr Fälle bei kürzerer Verweildauer“), nicht als Stichwort
  („Leistungsentwicklung“).
- **Tiefblaue Folien sparsam** (`variant="blue"` / `tone="blue"`): Titel,
  Kapitelauftakt, eine Betonungsfolie. Jede zweite Folie in Blau wirkt als
  Hintergrundfarbe statt als Betonung.
- **Quelle und Datenstand** auf jede Datenfolie (`source` an `DataTable` /
  `ChartFrame`, `footnote` an `ContentSlide`).
- **Zahlen deutsch formatieren**: Tausenderpunkt, Dezimalkomma, Einheit über
  `unit` statt im Wert („12.480“, „4,3“ + `unit="Tage"`).
- Fußzeile (`footerLabel`) und Seitenzahl (`pageNumber`) auf allen
  Inhaltsfolien gleich durchziehen; Titel-, Kapitel- und Abschlussfolie ohne.

## Wo die verbindliche Wahrheit steht

- `_ds/<folder>/styles.css` und die daraus importierten Dateien — die echten
  Tokens und Komponenten-Regeln. Vor eigenem Styling dort nachsehen.
- `_ds/<folder>/components/<gruppe>/<Name>/<Name>.prompt.md` — pro Komponente
  Zweck, Beispiel und die Regeln für ihren Einsatz.
- `_ds/<folder>/components/<gruppe>/<Name>/<Name>.d.ts` — die verbindliche API.
- `_ds/<folder>/guidelines/docs/guides/foliensatz-aufbauen.md` (verlinkt aus
  `guidelines/index.md`) — Aufbau eines vollständigen Foliensatzes und bewährte
  Kombinationen. Bei „baue eine Präsentation“ ist das der richtige Einstieg.

## Beispiel: eine fertige Folie

```jsx
<ContentSlide
  kicker="Kapitel 2 — Leistungsentwicklung"
  title="Mehr Fälle bei kürzerer Verweildauer"
  lead="Die höhere Auslastung entsteht ohne zusätzliche Betten."
  columns={2}
  footnote="Datenstand 31.12.2025, ohne ambulante Fälle."
  footerLabel="Qualitätsbericht 2025"
  pageNumber={7}
  showLogo
>
  <ChartFrame
    title="Bettenauslastung"
    caption="Der Zielwert von 85 % wird seit 2024 übertroffen."
    source="Quelle: Controlling, Stand 31.12.2025"
    height="17cqw"
  >
    <BarChart
      data={[
        { label: "2022", value: 81.4 },
        { label: "2023", value: 83.9 },
        { label: "2024", value: 85.5 },
        { label: "2025", value: 87.6, tone: "accent" },
      ]}
      unit=" %"
      target={85}
      targetLabel="Ziel 85 %"
    />
  </ChartFrame>

  {/* eigenes Layout-Glue: nur Tokens, keine ksl-Klassen */}
  <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-5)" }}>
    <BulletList
      items={[
        { text: "Zwei zusätzliche Belegbetten in der Inneren Medizin", detail: "Seit April 2025 in Betrieb" },
        { text: "Kürzere Verweildauer schafft zusätzliche Kapazität" },
      ]}
    />
    <Callout title="Zu beachten" tone="warning" compact>
      Oberhalb von 90 % Auslastung steigt die Verlegungsquote messbar an.
    </Callout>
  </div>
</ContentSlide>
```

## Das echte Logo

`KlinikLogo` zeichnet ohne `src` eine **Textmarke als Platzhalter**. Sobald die
offizielle Logodatei vorliegt, `logoSrc="/pfad/zum/logo.svg"` an den
Folientypen setzen (`TitleSlide`, `ContentSlide`, `Slide`, `ClosingSlide`) —
damit ist die Marke überall gleichzeitig ausgetauscht. Wort- und Bildmarke nie
nachbauen oder verändern.

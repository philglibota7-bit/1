# Einen Foliensatz aufbauen

Diese Anleitung beschreibt, wie die Bausteine zu einer vollständigen Präsentation
kombiniert werden. Sie ergänzt die Einzeldokumentation der Komponenten.

## Der Grundaufbau

Ein tragfähiger Klinik-Vortrag folgt fast immer derselben Abfolge:

| Position | Folientyp | Zweck |
|---|---|---|
| 1 | `TitleSlide` | Thema, Anlass, Person, Datum |
| 2 | `ContentSlide` + `BulletList marker="number"` | Gliederung (bei Vorträgen ab ~10 Minuten) |
| 3 | `SectionSlide` | Kapitelauftakt |
| 4 … | `ContentSlide` | Inhalt: Kennzahlen, Tabellen, Diagramme, Aufzählungen |
| … | `QuoteSlide` | Ruhepunkt zwischen datenlastigen Folien |
| vorletzte | `ContentSlide` + `Callout` | Fazit, Beschlussvorschlag, nächste Schritte |
| letzte | `ClosingSlide` | Dank und Kontakt |

Seitenzahlen (`pageNumber`) und Fußzeile (`footerLabel`) auf allen Inhaltsfolien
gleich durchziehen; Titel-, Kapitel- und Abschlussfolien bleiben ohne.

## Bewährte Kombinationen

**Kennzahlen-Überblick** — drei Kacheln, eine Leitkennzahl in Blau:

```jsx
<ContentSlide
  kicker="Kapitel 2 — Leistungsentwicklung"
  title="Mehr Fälle bei kürzerer Verweildauer"
  lead="Die höhere Auslastung entsteht ohne zusätzliche Betten."
  columns={3}
  footnote="Datenstand 31.12.2025, ohne ambulante Fälle."
  footerLabel="Qualitätsbericht 2025"
  pageNumber={7}
>
  <KpiTile label="Stationäre Fälle" value="12.480" delta="+4,2 %" trend="up" tone="blue" footnote="Vorjahr: 11.976" />
  <KpiTile label="Verweildauer" value="4,3" unit="Tage" delta="−0,3 Tage" trend="down" tone="positive" footnote="Zielwert: 4,5 Tage" />
  <KpiTile label="Bettenauslastung" value="87,6" unit="%" delta="+2,1 pp" trend="up" footnote="Ziel: 85 %" />
</ContentSlide>
```

**Diagramm mit Einordnung** — Diagramm links, Erläuterung und Hinweis rechts:

```jsx
<ContentSlide title="Die Auslastung liegt seit 2024 über dem Zielwert" columns={2} pageNumber={8}>
  <ChartFrame
    title="Bettenauslastung"
    caption="Der Zielwert von 85 % wird seit 2024 übertroffen."
    source="Quelle: Controlling, Stand 31.12.2025"
    height="18cqw"
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
  <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-5)" }}>
    <BulletList
      items={[
        { text: "Zwei zusätzliche Belegbetten in der Inneren Medizin", detail: "Seit April 2025 in Betrieb" },
        { text: "Kürzere Verweildauer schafft Kapazität" },
      ]}
    />
    <Callout title="Zu beachten" tone="warning" compact>
      Über 90 % Auslastung steigt die Verlegungsquote messbar an.
    </Callout>
  </div>
</ContentSlide>
```

**Tabelle mit Fazit** — Tabelle oben, Hinweisbox darunter:

```jsx
<ContentSlide title="Drei Fachabteilungen tragen den Zuwachs" pageNumber={9}>
  <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-5)" }}>
    <DataTable
      columns={[
        { key: "abt", label: "Fachabteilung", width: "40%" },
        { key: "a", label: "2024", align: "right" },
        { key: "b", label: "2025", align: "right" },
        { key: "d", label: "Veränderung", align: "right" },
      ]}
      rows={[
        { abt: "Innere Medizin", a: "3.812", b: "4.015", d: "+5,3 %" },
        { abt: "Chirurgie", a: "2.964", b: "3.102", d: "+4,7 %" },
        { abt: "Geriatrie", a: "1.240", b: "1.198", d: "−3,4 %" },
      ]}
      totalRow={{ abt: "Gesamt", a: "11.976", b: "12.480", d: "+4,2 %" }}
      source="Quelle: Medizincontrolling"
      dense
    />
    <Callout title="Schlussfolgerung" tone="info" compact>
      Der Rückgang in der Geriatrie ist auf die Umwidmung von acht Betten zurückzuführen.
    </Callout>
  </div>
</ContentSlide>
```

## Regeln, die den Foliensatz zusammenhalten

- **Eine Aussage pro Folie**, und sie steht in der Überschrift. Die Überschrift
  ist ein Satz, kein Stichwort.
- **Rot ist Akzent, nicht Fläche.** Rot markiert genau die Zahl, den Balken oder
  die Warnung, um die es geht. Alles Tragende ist blau, alles Ruhige weiß.
- **Blaue Folien sparsam.** Eine tiefblaue Folie (`variant="blue"`) wirkt als
  Betonung; jede zweite Folie in Blau wirkt als Hintergrundfarbe.
- **Abstände über Tokens.** Eigene Layout-Elemente mit `var(--k-sp-5)` /
  `var(--k-sp-6)` setzen, nie mit festen Pixelwerten — sonst bricht die
  proportionale Skalierung der Folie.
- **Zahlen deutsch formatieren**: Tausenderpunkt, Dezimalkomma, Einheit über
  `unit` statt im Wert.
- **Quelle und Datenstand** gehören auf jede Datenfolie (`source`, `footnote`).

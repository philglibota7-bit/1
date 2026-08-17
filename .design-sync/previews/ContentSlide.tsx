import {
  BarChart,
  BulletList,
  Callout,
  ChartFrame,
  ContentSlide,
  DataTable,
  KpiTile,
} from "@klinik-sh/slides";

/** Kennzahlenfolie: drei Kacheln, Fußnote, Fußzeile, Logo. */
export function KennzahlenDreiSpalten() {
  return (
    <ContentSlide
      kicker="Kapitel 2 — Leistungsentwicklung"
      title="Mehr Fälle bei kürzerer Verweildauer"
      lead="Die höhere Auslastung entsteht ohne zusätzliche Betten."
      columns={3}
      footnote="Datenstand 31.12.2025, ohne ambulante Fälle."
      footerLabel="Qualitätsbericht 2025"
      pageNumber={7}
      showLogo
    >
      <KpiTile label="Stationäre Fälle" value="12.480" delta="+4,2 %" trend="up" tone="blue" footnote="Vorjahr: 11.976" />
      <KpiTile label="Verweildauer" value="4,3" unit="Tage" delta="−0,3 Tage" trend="down" tone="positive" footnote="Zielwert: 4,5 Tage" />
      <KpiTile label="Bettenauslastung" value="87,6" unit="%" delta="+2,1 pp" trend="up" footnote="Ziel: 85 %" />
    </ContentSlide>
  );
}

/** Zweispaltige Kombination: Diagramm links, Einordnung und Hinweis rechts. */
export function DiagrammMitEinordnung() {
  return (
    <ContentSlide
      kicker="Kapitel 2 — Leistungsentwicklung"
      title="Die Auslastung liegt seit 2024 über dem Zielwert"
      columns={2}
      footerLabel="Qualitätsbericht 2025"
      pageNumber={8}
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
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-5)" }}>
        <BulletList
          items={[
            { text: "Zwei zusätzliche Belegbetten in der Inneren Medizin", detail: "Seit April 2025 in Betrieb" },
            { text: "Kürzere Verweildauer schafft zusätzliche Kapazität" },
            { text: "Elektive Eingriffe besser über die Woche verteilt" },
          ]}
        />
        <Callout title="Zu beachten" tone="warning" compact>
          Oberhalb von 90 % Auslastung steigt die Verlegungsquote messbar an.
        </Callout>
      </div>
    </ContentSlide>
  );
}

/** Einspaltige Aufzählungsfolie mit Einleitungssatz. */
export function AufzaehlungMitEinleitung() {
  return (
    <ContentSlide
      kicker="Kapitel 3 — Maßnahmen"
      title="Vier Maßnahmen haben die Notaufnahme entlastet"
      lead="Alle vier sind seit dem zweiten Quartal 2025 in allen drei Häusern umgesetzt."
      footerLabel="Qualitätsbericht 2025"
      pageNumber={11}
    >
      <BulletList
        items={[
          { text: "Zentrale Ersteinschätzung nach Manchester-Triage", detail: "Einheitliche Dringlichkeitsstufen an allen Standorten" },
          { text: "Wartezeit bis zum Arztkontakt verkürzt", detail: "Median 18 Minuten, vorher 34 Minuten" },
          { text: "Gemeinsame Rufbereitschaft der Fachabteilungen", detail: "Ein Dienstplan für Innere Medizin, Chirurgie und Anästhesie" },
          { text: "Direkte Übergabe an die Kurzliegerstation", detail: "Entlastet die Notaufnahme in den Abendstunden" },
        ]}
      />
    </ContentSlide>
  );
}

/** Zartblaue Variante: Tabelle mit Schlussfolgerung darunter. */
export function TabelleMitFazit() {
  return (
    <ContentSlide
      variant="muted"
      title="Drei Fachabteilungen tragen den Zuwachs"
      footerLabel="Qualitätsbericht 2025"
      pageNumber={9}
    >
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
            { abt: "Unfallchirurgie", a: "1.884", b: "1.965", d: "+4,3 %" },
            { abt: "Geriatrie", a: "1.240", b: "1.198", d: "−3,4 %" },
          ]}
          highlightRows={[0]}
          totalRow={{ abt: "Gesamt", a: "11.976", b: "12.480", d: "+4,2 %" }}
          source="Quelle: Medizincontrolling, Stand 31.12.2025"
          dense
        />
        <Callout title="Schlussfolgerung" tone="info" compact>
          Der Rückgang in der Geriatrie ist auf die Umwidmung von acht Betten zurückzuführen.
        </Callout>
      </div>
    </ContentSlide>
  );
}

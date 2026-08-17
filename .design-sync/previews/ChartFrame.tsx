import { BarChart, BulletList, Callout, ChartFrame, ContentSlide, Slide } from "@klinik-sh/slides";

/** Vollbreiter Rahmen mit Legende, Erläuterung und Quelle. */
export function DiagrammMitLegende() {
  return (
    <ContentSlide
      kicker="Kapitel 3 — Zentrale Notaufnahme"
      title="Die Ersteinschätzung erreicht 2025 erstmals den Zielwert"
      lead="Anteil der Patienten, die innerhalb von zehn Minuten ersteingeschätzt werden."
      footnote="Alle drei Standorte zusammengefasst, alle Dringlichkeitsstufen."
      footerLabel="Qualitätsbericht 2025"
      pageNumber={12}
      showLogo
    >
      <ChartFrame
        title="Ersteinschätzung innerhalb von 10 Minuten"
        legend={[{ label: "Ist-Wert" }, { label: "Zielwert 90 %", color: "var(--k-red)" }]}
        caption="Den Sprung trägt die zentrale Anmeldung, die seit Mai 2025 in allen drei Häusern gilt."
        source="Quelle: Notaufnahmeregister, Stand 31.12.2025"
        height="17cqw"
      >
        <BarChart
          data={[
            { label: "2021", value: 71.4 },
            { label: "2022", value: 76.8 },
            { label: "2023", value: 81.2 },
            { label: "2024", value: 85.9 },
            { label: "2025", value: 92.3, tone: "accent" },
          ]}
          unit=" %"
          target={90}
          targetLabel="Ziel 90 %"
        />
      </ChartFrame>
    </ContentSlide>
  );
}

/** Zwei Rahmen nebeneinander: geringere Höhe, gleiche Skala über `max`. */
export function ZweiDiagrammeNebeneinander() {
  return (
    <ContentSlide
      kicker="Kapitel 3 — Zentrale Notaufnahme"
      title="Haus Mitte wächst im Winter, Haus Süd bleibt über das Jahr gleichmäßig"
      columns={2}
      footnote="Beide Diagramme auf derselben Skala (max. 3.600 Zugänge) — nur so ist der Vergleich zulässig."
      footerLabel="Qualitätsbericht 2025"
      pageNumber={13}
    >
      <ChartFrame
        title="Haus Mitte — Zugänge je Quartal"
        caption="Das vierte Quartal trägt den Zuwachs: Grippewelle und zwei zusätzliche Belegbetten."
        source="Quelle: Notaufnahmeregister"
        height="13cqw"
      >
        <BarChart
          max={3600}
          data={[
            { label: "Q1", value: 2980 },
            { label: "Q2", value: 3040 },
            { label: "Q3", value: 3080 },
            { label: "Q4", value: 3380, tone: "accent" },
          ]}
        />
      </ChartFrame>
      <ChartFrame
        title="Haus Süd — Zugänge je Quartal"
        caption="Gleichmäßige Auslastung ohne Winterspitze — die Grundlast bleibt bei etwa 1.900 Zugängen."
        source="Quelle: Notaufnahmeregister"
        height="13cqw"
      >
        <BarChart
          max={3600}
          data={[
            { label: "Q1", value: 1920 },
            { label: "Q2", value: 1880 },
            { label: "Q3", value: 1940 },
            { label: "Q4", value: 1960 },
          ]}
        />
      </ChartFrame>
    </ContentSlide>
  );
}

/** Rangfolge im Rahmen, daneben Einordnung und Hinweisbox. */
export function RahmenNebenAufzaehlung() {
  return (
    <ContentSlide
      kicker="Kapitel 4 — Pflegepersonal"
      title="Intensivstation und Geriatrie tragen die Hälfte der offenen Stellen"
      columns={2}
      footerLabel="Personalbericht 2025"
      pageNumber={17}
    >
      <ChartFrame
        title="Offene Pflegestellen je Station"
        legend={[{ label: "Offene Vollkräfte" }, { label: "Nachbesetzung läuft", color: "var(--k-blue-200)" }]}
        caption="Die beiden Spitzen sind fachlich schwer zu besetzen — Intensivpflege und Geriatrie."
        source="Quelle: Pflegedirektion, Stichtag 31.12.2025"
        height="16cqw"
      >
        <BarChart
          orientation="horizontal"
          unit=" VK"
          data={[
            { label: "Intensivstation", value: 6.5, tone: "accent" },
            { label: "Geriatrie", value: 6.0 },
            { label: "Innere 1", value: 3.5 },
            { label: "Innere 2", value: 2.0, tone: "muted" },
            { label: "Chirurgie 1", value: 1.5, tone: "muted" },
          ]}
        />
      </ChartFrame>
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-5)" }}>
        <BulletList
          marker="check"
          items={[
            {
              text: "Fachweiterbildung Intensivpflege wird vollständig finanziert",
              detail: "Sechs Plätze im Jahr 2026, Freistellung inklusive",
            },
            {
              text: "Kooperation mit der Pflegeschule Schwäbisch Hall verlängert",
              detail: "24 Ausbildungsplätze je Jahrgang",
            },
            { text: "Springerpool mit 8,0 Vollkräften aufgebaut" },
          ]}
        />
        <Callout title="Zu beachten" tone="warning" compact>
          Ohne Nachbesetzung auf der Intensivstation bleibt ein Beatmungsplatz ab dem
          zweiten Quartal 2026 gesperrt.
        </Callout>
      </div>
    </ContentSlide>
  );
}

/** Eigenes SVG in der Zeichenfläche — Rahmen, Legende und Quelle bleiben gleich. */
export function EigenesSvgImRahmen() {
  return (
    <Slide
      kicker="Kapitel 3 — Zentrale Notaufnahme"
      title="Die Zugänge steigen ab Oktober deutlich über das Monatsmittel"
      footerLabel="Qualitätsbericht 2025"
      pageNumber={14}
      align="center"
      decor
    >
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-5)" }}>
        <ChartFrame
          title="Zugänge Notaufnahme je Monat, 2025"
          legend={[
            { label: "Zugänge je Monat" },
            { label: "Monatsmittel 3.100", color: "var(--k-red)" },
          ]}
          caption="Von Januar bis September liegen die Zugänge im Mittel; der Anstieg beginnt im Oktober und hält bis zum Jahresende an."
          source="Quelle: Notaufnahmeregister, Stand 31.12.2025"
          height="15cqw"
        >
          <svg
            viewBox="0 0 600 100"
            preserveAspectRatio="none"
            style={{ display: "block", width: "100%", height: "100%" }}
            role="img"
            aria-label="Zugänge der Notaufnahme je Monat im Jahr 2025"
          >
            <line x1="0" y1="10" x2="600" y2="10" stroke="var(--k-line)" strokeWidth="1" vectorEffect="non-scaling-stroke" />
            <line x1="0" y1="52.5" x2="600" y2="52.5" stroke="var(--k-line)" strokeWidth="1" vectorEffect="non-scaling-stroke" />
            <line x1="0" y1="95" x2="600" y2="95" stroke="var(--k-line-strong)" strokeWidth="1" vectorEffect="non-scaling-stroke" />
            <polygon
              points="10,54.6 62.7,80.1 115.5,71.6 168.2,86.5 220.9,78 273.6,69.5 326.4,61 379.1,72.7 431.8,67.4 484.5,48.2 537.3,33.4 590,18.5 590,95 10,95"
              fill="var(--k-blue-50)"
            />
            <polyline
              points="10,54.6 62.7,80.1 115.5,71.6 168.2,86.5 220.9,78 273.6,69.5 326.4,61 379.1,72.7 431.8,67.4 484.5,48.2 537.3,33.4 590,18.5"
              fill="none"
              stroke="var(--k-blue)"
              strokeWidth="2.5"
              strokeLinejoin="round"
              vectorEffect="non-scaling-stroke"
            />
            <line
              x1="0"
              y1="63.1"
              x2="600"
              y2="63.1"
              stroke="var(--k-red)"
              strokeWidth="1.5"
              strokeDasharray="6 5"
              vectorEffect="non-scaling-stroke"
            />
          </svg>
        </ChartFrame>
        <Callout title="Konsequenz für die Dienstplanung" tone="info" compact>
          Für das vierte Quartal 2026 wird die ärztliche Abendbesetzung im Haus Mitte um
          eine Schicht je Woche verstärkt.
        </Callout>
      </div>
    </Slide>
  );
}

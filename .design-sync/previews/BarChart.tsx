import { BarChart, Callout, ChartFrame, ContentSlide, KpiTile } from "@klinik-sh/slides";

/** Säulen für die Zeitreihe, mit Ziellinie und Akzent auf dem aktuellen Jahr. */
export function SaeulenMitZiellinie() {
  return (
    <ContentSlide
      kicker="Kapitel 5 — Patientenzufriedenheit"
      title="Die Weiterempfehlungsquote liegt seit 2024 über dem Zielwert"
      lead="Anteil der Befragten, die das Klinikum weiterempfehlen würden."
      footnote="Patientenbefragung, 2.140 verwertbare Fragebögen, Rücklaufquote 38,4 %."
      footerLabel="Qualitätsbericht 2025"
      pageNumber={19}
      showLogo
    >
      <ChartFrame
        title="Weiterempfehlungsquote"
        legend={[{ label: "Ist-Wert" }, { label: "Zielwert 85 %", color: "var(--k-red)" }]}
        caption="Den Zuwachs tragen die kürzeren Wartezeiten in der Notaufnahme und das neue Entlassgespräch."
        source="Quelle: Qualitätsmanagement, Befragung 2025"
        height="17cqw"
      >
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
      </ChartFrame>
    </ContentSlide>
  );
}

/** Balken für Rangfolgen: lange Beschriftungen bleiben lesbar, `muted` als Vergleich. */
export function BalkenRangfolge() {
  return (
    <ContentSlide
      kicker="Kapitel 2 — Leistungsentwicklung"
      title="Zwei Fachabteilungen stellen mehr als die Hälfte aller Fälle"
      lead="Stationäre Fälle des Jahres 2025 je Fachabteilung."
      footnote="Ohne ambulante Fälle. Fachabteilungen unter 500 Fällen sind zusammengefasst."
      footerLabel="Qualitätsbericht 2025"
      pageNumber={10}
    >
      <ChartFrame
        title="Stationäre Fälle je Fachabteilung, 2025"
        caption="Die Innere Medizin bleibt die tragende Abteilung — jeder dritte Fall wird dort behandelt."
        source="Quelle: Medizincontrolling, Stand 31.12.2025"
        height="17cqw"
      >
        <BarChart
          orientation="horizontal"
          data={[
            { label: "Innere Medizin", value: 4015, display: "4.015", tone: "accent" },
            { label: "Allgemeinchirurgie", value: 3102, display: "3.102" },
            { label: "Unfallchirurgie", value: 1965, display: "1.965" },
            { label: "Gynäkologie", value: 1472, display: "1.472" },
            { label: "Geriatrie", value: 1198, display: "1.198", tone: "muted" },
            { label: "Neurologie", value: 728, display: "728", tone: "muted" },
          ]}
        />
      </ChartFrame>
    </ContentSlide>
  );
}

/** Vollständige Folie: Diagramm links, Kennzahl und Hinweis rechts. */
export function DiagrammMitKennzahlUndFazit() {
  return (
    <ContentSlide
      kicker="Kapitel 4 — Pflegepersonal"
      title="Die Fluktuation in der Pflege sinkt, bleibt aber über dem Zielwert"
      columns={2}
      footnote="Fluktuation = Abgänge im Jahr geteilt durch durchschnittliche Beschäftigtenzahl."
      footerLabel="Personalbericht 2025"
      pageNumber={18}
    >
      <ChartFrame
        title="Fluktuationsquote Pflege"
        legend={[{ label: "Ist-Wert" }, { label: "Zielwert 8 %", color: "var(--k-red)" }]}
        caption="Der Rückgang setzt mit der verbindlichen Dienstplanung ab Januar 2024 ein."
        source="Quelle: Personalabteilung, Stand 31.12.2025"
        height="16cqw"
      >
        <BarChart
          data={[
            { label: "2022", value: 13.4 },
            { label: "2023", value: 12.1 },
            { label: "2024", value: 10.6 },
            { label: "2025", value: 9.8, tone: "accent" },
          ]}
          unit=" %"
          target={8}
          targetLabel="Ziel 8 %"
        />
      </ChartFrame>
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-5)" }}>
        <KpiTile
          label="Fluktuation Pflege"
          value="9,8"
          unit="%"
          delta="−0,8 pp"
          trend="down"
          tone="warning"
          footnote="Zielwert: 8,0 % — Vorjahr: 10,6 %"
        />
        <KpiTile
          label="Durchschnittliche Betriebstreue"
          value="8,4"
          unit="Jahre"
          delta="+0,3 Jahre"
          trend="up"
          tone="blue"
          footnote="Pflegedienst, alle drei Standorte"
        />
        <Callout title="Zu beachten" tone="warning" compact>
          Zwei Drittel der Abgänge erfolgen in den ersten 18 Monaten — das Einarbeitungskonzept
          wird 2026 überarbeitet.
        </Callout>
      </div>
    </ContentSlide>
  );
}

/** `display` für eigene Zahlenformate, `max` für eine feste Skala. */
export function EigeneWerteformatierung() {
  return (
    <ContentSlide
      kicker="Kapitel 5 — Strukturvorhaben"
      title="Das Investitionsvolumen verdoppelt sich mit dem Neubau Haus Nord"
      lead="Gesamtinvestitionen je Jahr, ab 2026 als Planwert."
      footnote="Enthält Eigenmittel und Landesförderung; ohne Instandhaltungsbudget."
      footerLabel="Aufsichtsratssitzung"
      pageNumber={20}
    >
      <ChartFrame
        title="Investitionsvolumen je Jahr"
        legend={[{ label: "Ist-Werte" }, { label: "Planwert 2026", color: "var(--k-red)" }]}
        caption="Der Sprung 2026 entsteht vollständig aus dem ersten Bauabschnitt des Hauses Nord."
        source="Quelle: Kaufmännische Leitung, Wirtschaftsplan 2026"
        height="17cqw"
      >
        <BarChart
          max={16}
          data={[
            { label: "2022", value: 4.2, display: "4,2 Mio. €" },
            { label: "2023", value: 5.8, display: "5,8 Mio. €" },
            { label: "2024", value: 6.1, display: "6,1 Mio. €" },
            { label: "2025", value: 7.4, display: "7,4 Mio. €" },
            { label: "2026", value: 14.6, display: "14,6 Mio. €", tone: "accent" },
          ]}
        />
      </ChartFrame>
    </ContentSlide>
  );
}

import { BarChart, BulletList, Callout, ChartFrame, ContentSlide } from "@klinik-sh/slides";

/** Alle fünf Tonwerte im Vergleich, jeweils in der kompakten Variante. */
export function Tonwerte() {
  return (
    <ContentSlide
      align="top"
      title="Fünf Tonwerte für fünf Anlässe"
      lead="Die Farbe richtet sich nach dem Charakter der Aussage, nicht nach dem Wunsch nach Aufmerksamkeit."
      footnote="Auf einer Vortragsfolie steht höchstens eine Hinweisbox."
      footerLabel="Bausteine"
    >
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-4)" }}>
        <Callout title="Beschlussvorschlag" tone="info" compact>
          Der Aufsichtsrat stimmt der gemeinsamen Notaufnahme-Struktur ab dem dritten
          Quartal 2026 zu.
        </Callout>
        <Callout title="Zielwert erreicht" tone="success" compact>
          Die Verweildauer liegt mit 4,3 Tagen unter dem Zielwert von 4,5 Tagen.
        </Callout>
        <Callout title="Frist" tone="warning" compact>
          Die Meldung der Qualitätsindikatoren an das Landesamt muss bis zum 31. März 2026
          erfolgen.
        </Callout>
        <Callout title="Personalengpass" tone="critical" compact>
          Auf der Intensivstation fehlen 6,5 Vollkräfte in der Pflege — die
          Pflegepersonaluntergrenze ist nur mit Leihkräften einzuhalten.
        </Callout>
        <Callout title="Begriffsabgrenzung" tone="neutral" compact>
          Fallzahl meint stationäre Fälle nach § 21 KHEntgG, ohne ambulante Behandlungen.
        </Callout>
      </div>
    </ContentSlide>
  );
}

/** Fazitfolie: Schlussfolgerungen als Aufzählung, Beschluss als blaue Hinweisbox. */
export function BeschlussvorschlagFazit() {
  return (
    <ContentSlide
      kicker="Kapitel 6 — Beschluss"
      title="Die gemeinsame Notaufnahme-Struktur startet im dritten Quartal 2026"
      lead="Die Vorbereitungen sind abgeschlossen, offen ist allein die Freigabe der Stellen."
      footnote="Beschlussvorlage AR-2026-04, Anlage 2."
      footerLabel="Aufsichtsratssitzung"
      pageNumber={21}
      showLogo
    >
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-6)" }}>
        <BulletList
          marker="arrow"
          items={[
            {
              text: "Ersteinschätzung und Rufbereitschaft sind bereits vereinheitlicht",
              detail: "Seit Mai 2025 an allen drei Standorten im Regelbetrieb",
            },
            {
              text: "Haus Süd benötigt eine zweite ärztliche Besetzung am Abend",
              detail: "1,0 Vollkraft, im Wirtschaftsplan 2026 hinterlegt",
            },
            {
              text: "Die Kurzliegerbereiche werden zusammengelegt",
              detail: "16 Betten im Haus Mitte, Umzug im vierten Quartal 2026",
            },
          ]}
        />
        <Callout title="Beschlussvorschlag" tone="info">
          Der Aufsichtsrat beschließt die gemeinsame Notaufnahme-Struktur der drei Häuser
          zum 1. Juli 2026 und gibt die dafür erforderliche ärztliche Stelle im Haus Süd frei.
        </Callout>
      </div>
    </ContentSlide>
  );
}

/** `tone="success"` als Fazit unter einem Diagramm mit Ziellinie. */
export function ZielwertErreicht() {
  return (
    <ContentSlide
      kicker="Kapitel 2 — Leistungsentwicklung"
      title="Die Verweildauer liegt erstmals unter dem Zielwert"
      columns={2}
      footerLabel="Qualitätsbericht 2025"
      pageNumber={10}
    >
      <ChartFrame
        title="Durchschnittliche Verweildauer"
        caption="Der Rückgang kommt aus der Inneren Medizin und dem neuen Kurzliegerbereich."
        source="Quelle: Medizincontrolling, Stand 31.12.2025"
        height="16cqw"
      >
        <BarChart
          data={[
            { label: "2022", value: 5.1 },
            { label: "2023", value: 4.8 },
            { label: "2024", value: 4.6 },
            { label: "2025", value: 4.3, tone: "accent" },
          ]}
          unit=" Tage"
          target={4.5}
          targetLabel="Ziel 4,5 Tage"
        />
      </ChartFrame>
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-5)" }}>
        <BulletList
          marker="check"
          items={[
            {
              text: "Kurzliegerbereich mit 16 Betten eröffnet",
              detail: "Seit Februar 2025 im Haus Mitte",
            },
            { text: "Entlassmanagement täglich statt zweimal wöchentlich" },
            { text: "Sozialdienst früher eingebunden", detail: "Ab dem zweiten Behandlungstag" },
          ]}
        />
        <Callout title="Zielwert erreicht" tone="success" compact>
          4,3 Tage bei gleichzeitig 4,2 % mehr Fällen — die Kapazität entstand ohne
          zusätzliche Betten.
        </Callout>
      </div>
    </ContentSlide>
  );
}

/** `tone="neutral"` ohne Symbol für Definitionen und Abgrenzungen. */
export function DefinitionOhneSymbol() {
  return (
    <ContentSlide
      variant="muted"
      align="top"
      kicker="Anhang — Begriffe"
      title="Drei Begriffe werden im Bericht durchgängig gleich verwendet"
      lead="Abweichende Definitionen sind die häufigste Ursache für Rückfragen aus den Fachabteilungen."
      footerLabel="Qualitätsbericht 2025"
      pageNumber={26}
    >
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-5)" }}>
        <BulletList
          marker="dot"
          items={[
            {
              text: "Fallzahl — stationäre Fälle nach § 21 KHEntgG",
              detail: "Ohne ambulante Behandlungen, ohne Begleitpersonen",
            },
            {
              text: "Verweildauer — Belegungstage geteilt durch Fälle",
              detail: "Aufnahme- und Entlassungstag zählen gemeinsam als ein Tag",
            },
            {
              text: "Besetzungsquote Pflege — Ist-Vollkräfte zu Soll-Vollkräften",
              detail: "Stichtagsbetrachtung zum Monatsende, ohne Leihpersonal",
            },
          ]}
        />
        <Callout title="Abgrenzung zur Vorjahresberichterstattung" tone="neutral" icon={false}>
          Bis 2023 wurden teilstationäre Fälle der Geriatrie mitgezählt. Die Werte für 2024
          und 2025 sind deshalb nur untereinander, nicht mit dem Bericht 2023 vergleichbar.
        </Callout>
      </div>
    </ContentSlide>
  );
}

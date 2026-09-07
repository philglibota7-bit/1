import { Callout, ContentSlide, DataTable, KpiTile } from "@klinik-sh/slides";

/** `zebra`, `highlightRows` und `totalRow` mit Titel und Quelle. */
export function FallzahlenJeFachabteilung() {
  return (
    <ContentSlide
      align="top"
      kicker="Kapitel 2 — Leistungsentwicklung"
      title="Die Innere Medizin trägt den größten Teil des Zuwachses"
      footerLabel="Qualitätsbericht 2025"
      pageNumber={9}
      showLogo
    >
      <DataTable
        caption="Stationäre Fälle je Fachabteilung"
        columns={[
          { key: "abt", label: "Fachabteilung", width: "34%" },
          { key: "y24", label: "2024", align: "right" },
          { key: "y25", label: "2025", align: "right" },
          { key: "delta", label: "Veränderung", align: "right" },
          { key: "vwd", label: "Verweildauer", align: "right" },
        ]}
        rows={[
          { abt: "Innere Medizin", y24: "3.812", y25: "4.015", delta: "+5,3 %", vwd: "4,6 Tage" },
          { abt: "Allgemein- und Visceralchirurgie", y24: "2.964", y25: "3.102", delta: "+4,7 %", vwd: "5,1 Tage" },
          { abt: "Unfallchirurgie", y24: "1.884", y25: "1.965", delta: "+4,3 %", vwd: "4,8 Tage" },
          { abt: "Gynäkologie und Geburtshilfe", y24: "1.406", y25: "1.472", delta: "+4,7 %", vwd: "3,2 Tage" },
          { abt: "Geriatrie", y24: "1.240", y25: "1.198", delta: "−3,4 %", vwd: "12,4 Tage" },
          { abt: "Neurologie", y24: "670", y25: "728", delta: "+8,7 %", vwd: "6,0 Tage" },
        ]}
        highlightRows={[0]}
        totalRow={{ abt: "Gesamt", y24: "11.976", y25: "12.480", delta: "+4,2 %", vwd: "4,3 Tage" }}
        dense
        source="Quelle: Medizincontrolling, Stand 31.12.2025"
        zebra
      />
    </ContentSlide>
  );
}

/** `dense` ohne `zebra` für neun Zeilen — mit rotem Hinweis auf das echte Risiko. */
export function PflegestellenJeStation() {
  return (
    <ContentSlide
      align="top"
      kicker="Kapitel 4 — Pflegepersonal"
      title="Zwei Stationen tragen fast die Hälfte der offenen Pflegestellen"
      footerLabel="Personalbericht 2025"
      pageNumber={16}
    >
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-5)" }}>
        <DataTable
          columns={[
            { key: "st", label: "Station", width: "30%" },
            { key: "betten", label: "Betten", align: "right" },
            { key: "soll", label: "Soll-VK", align: "right" },
            { key: "ist", label: "Ist-VK", align: "right" },
            { key: "offen", label: "Offen", align: "right" },
            { key: "quote", label: "Besetzung", align: "right" },
          ]}
          rows={[
            { st: "Innere 1 — Kardiologie", betten: "32", soll: "24,0", ist: "20,5", offen: "3,5", quote: "85,4 %" },
            { st: "Innere 2 — Gastroenterologie", betten: "28", soll: "21,0", ist: "19,0", offen: "2,0", quote: "90,5 %" },
            { st: "Intensivstation Haus Mitte", betten: "14", soll: "28,0", ist: "21,5", offen: "6,5", quote: "76,8 %" },
            { st: "Geriatrie", betten: "36", soll: "29,0", ist: "23,0", offen: "6,0", quote: "79,3 %" },
          ]}
          highlightRows={[2, 3]}
          totalRow={{ st: "Gesamt", betten: "110", soll: "102,0", ist: "84,0", offen: "18,0", quote: "82,4 %" }}
          source="Quelle: Pflegedirektion, Stichtag 31.12.2025"
          dense
        />
        <Callout title="Personalengpass" tone="critical" compact>
          Auf der Intensivstation und in der Geriatrie fehlen zusammen 12,5 Vollkräfte — bei
          weiterem Rückgang ist die Pflegepersonaluntergrenze nicht mehr einzuhalten.
        </Callout>
      </div>
    </ContentSlide>
  );
}

/** Schlichte Tabelle ohne `zebra` und ohne `dense`, neben Kennzahl und Fazit. */
export function WartezeitenJeStandort() {
  return (
    <ContentSlide
      kicker="Kapitel 3 — Zentrale Notaufnahme"
      title="Haus Süd erreicht die Zielwartezeit noch nicht"
      columns={2}
      footnote="Median über alle Dringlichkeitsstufen, Erhebungszeitraum Januar bis Dezember 2025."
      footerLabel="Qualitätsbericht 2025"
      pageNumber={13}
    >
      <DataTable
        caption="Wartezeit bis zum Arztkontakt"
        columns={[
          { key: "haus", label: "Standort", width: "40%" },
          { key: "y24", label: "2024", align: "right" },
          { key: "y25", label: "2025", align: "right" },
        ]}
        rows={[
          { haus: "Haus Mitte", y24: "31 Min.", y25: "16 Min." },
          { haus: "Haus Nord", y24: "29 Min.", y25: "17 Min." },
          { haus: "Haus Süd", y24: "42 Min.", y25: "27 Min." },
        ]}
        highlightRows={[2]}
        source="Quelle: Notaufnahmeregister, Stand 31.12.2025"
      />
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-5)" }}>
        <KpiTile
          label="Wartezeit bis Arztkontakt"
          value="18"
          unit="Min."
          delta="−16 Min."
          trend="down"
          tone="blue"
          footnote="Median aller drei Häuser, Ziel: 20 Minuten"
        />
        <Callout title="Schlussfolgerung" tone="info">
          In Haus Süd fehlt die zweite ärztliche Besetzung zwischen 16 und 22 Uhr. Die
          Stelle ist ab dem zweiten Quartal 2026 im Wirtschaftsplan vorgesehen.
        </Callout>
      </div>
    </ContentSlide>
  );
}

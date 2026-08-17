import {
  BulletList,
  Callout,
  DataTable,
  KpiTile,
  Slide,
} from "@klinik-sh/slides";

/** Vollständige Folie: eigenes Zweispalten-Layout aus Aufzählung und Hinweisbox. */
export function StrukturkonzeptZweispaltig() {
  return (
    <Slide
      kicker="Ausgangslage"
      title="Drei Häuser arbeiten künftig zusammen"
      footerLabel="Strukturkonzept 2026"
      pageNumber={4}
      showLogo
    >
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1.4fr 1fr",
          gap: "var(--k-sp-6)",
          alignItems: "start",
        }}
      >
        <BulletList
          items={[
            {
              text: "Zentrale Ersteinschätzung nach Manchester-Triage",
              detail: "Einheitliche Dringlichkeitsstufen in Schwäbisch Hall, Crailsheim und Öhringen",
            },
            {
              text: "Gemeinsame Rufbereitschaft der Fachabteilungen",
              detail: "Ein Dienstplan für Innere Medizin, Chirurgie und Anästhesie",
            },
            {
              text: "Kurzliegerstation übernimmt direkt aus der Notaufnahme",
              detail: "Entlastet die Aufnahme zwischen 17 und 23 Uhr",
            },
            {
              text: "Schwerpunktversorgung bleibt am Standort Schwäbisch Hall",
              tone: "accent",
            },
          ]}
        />
        <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-5)" }}>
          <Callout title="Beschluss der Geschäftsführung" tone="info">
            Umsetzung ab dem dritten Quartal 2026, Übergangsphase von sechs Monaten.
          </Callout>
          <Callout title="Offen" tone="warning" compact>
            Der Stellenplan für die zentrale Ersteinschätzung ist noch nicht hinterlegt.
          </Callout>
        </div>
      </div>
    </Slide>
  );
}

/** Vollständige Folie: Kennzahlenreihe über einer Tabelle je Standort. */
export function PersonalkennzahlenMitTabelle() {
  return (
    <Slide
      kicker="Kapitel 4 — Personal und Nachwuchs"
      title="Die Pflege wächst, 34 Stellen fehlen"
      footerLabel="Qualitätsbericht 2025"
      pageNumber={18}
      showLogo
    >
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-6)" }}>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
            gap: "var(--k-sp-5)",
          }}
        >
          <KpiTile
            label="Vollzeitstellen Pflege"
            value="412,5"
            delta="+18,0 VK"
            trend="up"
            tone="blue"
            footnote="Vorjahr: 394,5 VK"
          />
          <KpiTile
            label="Fluktuationsquote"
            value="9,8"
            unit="%"
            delta="−1,4 pp"
            trend="down"
            tone="positive"
            footnote="Zielwert: unter 10 %"
          />
          <KpiTile
            label="Offene Pflegestellen"
            value="34"
            delta="+6"
            trend="up"
            tone="accent"
            footnote="Stand 31.12.2025"
          />
        </div>
        <DataTable
          columns={[
            { key: "ort", label: "Standort", width: "40%" },
            { key: "vk", label: "Vollzeitstellen", align: "right" },
            { key: "offen", label: "Offene Stellen", align: "right" },
            { key: "flukt", label: "Fluktuation", align: "right" },
          ]}
          rows={[
            { ort: "Schwäbisch Hall", vk: "236,0", offen: "19", flukt: "9,2 %" },
            { ort: "Crailsheim", vk: "118,5", offen: "11", flukt: "10,4 %" },
            { ort: "Öhringen", vk: "58,0", offen: "4", flukt: "10,1 %" },
          ]}
          source="Quelle: Personalcontrolling, Stand 31.12.2025"
          dense
        />
      </div>
    </Slide>
  );
}

/** Tiefblaue Betonungsfolie: eine Kernaussage, drei tragende Punkte, mittig gesetzt. */
export function TiefblaueKernaussage() {
  return (
    <Slide
      variant="blue"
      kicker="Strukturvorhaben 2026"
      title="Die Notaufnahme wird an einem Standort gebündelt"
      align="center"
      footerLabel="Strukturkonzept 2026"
      pageNumber={21}
      showLogo
    >
      <BulletList
        size="lg"
        marker="arrow"
        items={[
          {
            text: "Schwäbisch Hall übernimmt die Schwerpunktversorgung rund um die Uhr",
            detail: "Crailsheim und Öhringen bleiben als Basisnotfallversorgung erhalten",
          },
          {
            text: "Ein gemeinsamer Dienstplan statt drei getrennter Rufbereitschaften",
            detail: "Rechnerisch 4,5 Vollzeitstellen weniger im Nachtdienst",
          },
          {
            text: "Die Entscheidung fällt im Aufsichtsrat am 12. März 2026",
          },
        ]}
      />
    </Slide>
  );
}

/** Zartblaue Variante: vier Etappen als Hinweisboxen, mittig gesetzt. */
export function FahrplanZartblau() {
  return (
    <Slide
      variant="muted"
      kicker="Projektvorhaben"
      title="Der Umbau der Notaufnahme läuft in vier Etappen"
      align="center"
      footerLabel="Baubegleitung Notaufnahme"
      pageNumber={9}
    >
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-5)" }}>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(4, minmax(0, 1fr))",
            gap: "var(--k-sp-5)",
            alignItems: "stretch",
          }}
        >
          <Callout title="Q1 2026 — Planung" tone="success">
            Baugenehmigung liegt vor, Vergabe der Rohbauarbeiten abgeschlossen.
          </Callout>
          <Callout title="Q2 2026 — Interimsbetrieb" tone="info">
            Ersteinschätzung zieht in den Anbau West, 14 Behandlungsplätze.
          </Callout>
          <Callout title="Q3 2026 — Rohbau" tone="info">
            Sechs Wochen Vollsperrung der Zufahrt Ost, Rettungsdienst über Süd.
          </Callout>
          <Callout title="Q4 2026 — Inbetriebnahme" tone="warning">
            Termin hängt an der Medizintechnik, Vorlauf 22 Wochen.
          </Callout>
        </div>
        <BulletList
          items={[
            {
              text: "Der Betrieb der Notaufnahme läuft in allen vier Etappen ohne Schließtag weiter",
              detail: "Abstimmung mit dem Rettungsdienstbereich Schwäbisch Hall vom 04.02.2026",
            },
          ]}
        />
      </div>
    </Slide>
  );
}

import { BulletList, Callout, ContentSlide } from "@klinik-sh/slides";

/** `marker="check"` für Erreichtes — fünf Punkte mit grauer Zweitzeile. */
export function MassnahmenHaekchen() {
  return (
    <ContentSlide
      kicker="Kapitel 4 — Krankenhaushygiene"
      title="Fünf Maßnahmen des Hygieneplans sind vollständig umgesetzt"
      lead="Die Umsetzung wurde im Dezember 2025 in allen drei Häusern auditiert."
      footnote="Auditbericht Krankenhaushygiene, Stand 11.12.2025."
      footerLabel="Qualitätsbericht 2025"
      pageNumber={14}
      showLogo
    >
      <BulletList
        marker="check"
        items={[
          {
            text: "Händedesinfektionsmittelverbrauch flächendeckend erfasst",
            detail: "28,4 ml je Patiententag, im Vorjahr 23,1 ml",
          },
          {
            text: "Aufnahmescreening auf multiresistente Erreger",
            detail: "Alle Intensiv- und Beatmungsplätze seit 1. März 2025",
          },
          {
            text: "Hygienefachkraft an jedem Standort besetzt",
            detail: "Drei Vollzeitstellen, zuletzt Haus Süd im Oktober 2025",
          },
          {
            text: "Antibiotic-Stewardship-Visite eingeführt",
            detail: "Wöchentlich auf beiden Intensivstationen",
          },
          {
            text: "Schulungsquote der Pflege bei 96,2 %",
            detail: "Zielwert 95 %, Nachschulungen im Januar 2026",
          },
        ]}
      />
    </ContentSlide>
  );
}

/** `number` für den Ablauf, `dot` für die neutrale Liste — mit Hinweisbox. */
export function AblaufUndBeteiligte() {
  return (
    <ContentSlide
      kicker="Kapitel 3 — Zentrale Notaufnahme"
      title="Die Ersteinschätzung folgt seit Mai 2025 fünf festen Schritten"
      lead="Der Ablauf gilt einheitlich in allen drei Häusern."
      columns={2}
      footnote="Verfahrensanweisung ZNA-04, Version 3.0."
      footerLabel="Qualitätsbericht 2025"
      pageNumber={12}
    >
      <BulletList
        marker="number"
        items={[
          { text: "Anmeldung am Empfang, Versichertenkarte einlesen" },
          {
            text: "Ersteinschätzung nach Manchester-Triage-System",
            detail: "Innerhalb von 10 Minuten nach Ankunft",
          },
          { text: "Zuordnung zu Behandlungsbereich und Dringlichkeitsstufe" },
          {
            text: "Arztkontakt nach Dringlichkeit",
            detail: "Median 18 Minuten, Stufe Rot unverzüglich",
          },
          { text: "Übergabe an Station, Kurzliegerbereich oder Entlassung" },
        ]}
      />
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-5)" }}>
        <BulletList
          marker="dot"
          items={[
            { text: "Zentrale Notaufnahme, rund um die Uhr besetzt" },
            {
              text: "Innere Medizin und Chirurgie in gemeinsamer Rufbereitschaft",
              tone: "accent",
            },
            { text: "Radiologie mit CT-Bereitschaft rund um die Uhr" },
            { text: "Kinder- und Jugendmedizin nur im Haus Mitte", tone: "muted" },
          ]}
        />
        <Callout title="Zu beachten" tone="info" compact>
          Die Dringlichkeitsstufe wird nach 60 Minuten Wartezeit erneut überprüft.
        </Callout>
      </div>
    </ContentSlide>
  );
}

/** `size="lg"` mit `marker="arrow"` für wenige tragende Aussagen. */
export function KernaussagenGross() {
  return (
    <ContentSlide
      variant="muted"
      kicker="Kapitel 6 — Ausblick"
      title="Vier Schlussfolgerungen für das Jahr 2026"
      lead="Sie bilden die Grundlage der Zielvereinbarungen mit den Fachabteilungen."
      footerLabel="Qualitätsbericht 2025"
      pageNumber={22}
    >
      <BulletList
        size="lg"
        marker="arrow"
        items={[
          "Verweildauer auf 4,3 Tagen halten",
          "Offene Pflegestellen bis Jahresende auf unter 20 senken",
          "Notaufnahmen der drei Häuser organisatorisch zusammenführen",
          "Hygieneschulung verbindlich für alle Berufsgruppen",
        ]}
      />
    </ContentSlide>
  );
}

/** `columns={2}` ab sechs Punkten, darunter eine Frist als Hinweisbox. */
export function TeilprojekteZweispaltig() {
  return (
    <ContentSlide
      align="top"
      kicker="Kapitel 5 — Strukturvorhaben"
      title="Sechs Teilprojekte bündeln das Strukturvorhaben Neubau Haus Nord"
      lead="Die Teilprojekte laufen parallel und berichten monatlich an die Projektleitung."
      footnote="Projektstatusbericht Neubau Haus Nord, Stand 31.01.2026."
      footerLabel="Aufsichtsratssitzung"
      pageNumber={17}
    >
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-5)" }}>
        <BulletList
          marker="dot"
          columns={2}
          items={[
            { text: "Bauantrag und Genehmigung", detail: "Einreichung erfolgt am 14.01.2026" },
            { text: "Medizintechnik und Ausstattung", detail: "Bedarfsliste je Fachabteilung abgestimmt" },
            { text: "OP-Bereich mit vier Sälen", detail: "Zwei Hybridsäle vorgesehen" },
            { text: "Umzugsplanung der Stationen", detail: "Vier Etappen im Jahr 2027" },
            { text: "IT- und Netzinfrastruktur", detail: "Anbindung an das Krankenhausinformationssystem" },
            { text: "Personalgewinnung Pflege", detail: "Noch nicht begonnen", tone: "muted" },
          ]}
        />
        <Callout title="Frist" tone="warning" compact>
          Der Förderantrag beim Land muss bis zum 31. März 2026 vollständig vorliegen.
        </Callout>
      </div>
    </ContentSlide>
  );
}

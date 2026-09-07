import { Callout, ContentSlide, KpiTile } from "@klinik-sh/slides";

/** Kanonische Kennzahlenfolie: drei Kacheln, Leitkennzahl in Blau. */
export function Kennzahlenfolie() {
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
      <KpiTile
        label="Stationäre Fälle"
        value="12.480"
        delta="+4,2 %"
        trend="up"
        tone="blue"
        footnote="Vorjahr: 11.976"
      />
      <KpiTile
        label="Verweildauer"
        value="4,3"
        unit="Tage"
        delta="−0,3 Tage"
        trend="down"
        tone="positive"
        footnote="Zielwert: 4,5 Tage"
      />
      <KpiTile
        label="Bettenauslastung"
        value="87,6"
        unit="%"
        delta="+2,1 pp"
        trend="up"
        footnote="Ziel: 85 %"
      />
    </ContentSlide>
  );
}

/** Alle Farbgebungen im Vergleich — von neutral bis Handlungsbedarf. */
export function Farbgebung() {
  return (
    <ContentSlide
      title="Farbgebung der Kennzahlen-Kacheln"
      lead="Blau trägt, Grün bestätigt, Amber warnt, Rot bleibt der einen Zahl vorbehalten."
      columns={3}
      footerLabel="Bausteine"
    >
      <KpiTile label="Neutral — Kontext" value="1.842" footnote="Ambulante Notfälle" />
      <KpiTile label="Blau — Leitkennzahl" value="12.480" tone="blue" footnote="Stationäre Fälle" />
      <KpiTile label="Rot — Kernbotschaft" value="34" tone="accent" footnote="Offene Pflegestellen" />
      <KpiTile label="Grün — Ziel erreicht" value="4,3" unit="Tage" tone="positive" footnote="Ziel: 4,5 Tage" />
      <KpiTile label="Amber — Handlungsbedarf" value="9,8" unit="%" tone="warning" footnote="Fluktuation Pflege" />
      <Callout title="Regel" tone="neutral" compact>
        Höchstens eine rote Kachel pro Folie — sonst verliert der Akzent seine Wirkung.
      </Callout>
    </ContentSlide>
  );
}

/** Richtung und Bewertung sind getrennt: sinkende Verweildauer ist ein Erfolg. */
export function VeraenderungUndTrend() {
  return (
    <ContentSlide
      title="Richtung und Bewertung sind zwei verschiedene Dinge"
      lead="Der Pfeil zeigt die Bewegung, die Farbe die Bewertung."
      columns={3}
      footnote="Eine sinkende Verweildauer ist ein Erfolg, eine sinkende Fallzahl nicht."
      footerLabel="Bausteine"
    >
      <KpiTile
        label="Fallzahl steigt — gut"
        value="12.480"
        delta="+4,2 %"
        trend="up"
        tone="positive"
        footnote="Vorjahr: 11.976"
      />
      <KpiTile
        label="Verweildauer sinkt — gut"
        value="4,3"
        unit="Tage"
        delta="−0,3 Tage"
        trend="down"
        tone="positive"
        footnote="Zielwert: 4,5 Tage"
      />
      <KpiTile
        label="Wartezeit unverändert"
        value="18"
        unit="Min."
        delta="±0"
        trend="flat"
        footnote="Median bis Arztkontakt"
      />
    </ContentSlide>
  );
}

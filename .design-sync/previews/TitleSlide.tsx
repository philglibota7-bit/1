import { TitleSlide } from "@klinik-sh/slides";

/** Titelfolie im Regelfall: heller Grund, vollständige Angaben. */
export function Standard() {
  return (
    <TitleSlide
      kicker="Chefarztkonferenz"
      title="Qualitätsbericht 2025"
      subtitle="Kennzahlen, Entwicklungen und Schwerpunkte für das kommende Jahr"
      speaker="Dr. med. Andrea Vogt"
      role="Leitung Qualitätsmanagement"
      date="12. März 2026"
      place="Klinikum Crailsheim"
    />
  );
}

/** Tiefblaue Titelfolie — stärkerer Auftritt für abgedunkelte Räume. */
export function Tiefblau() {
  return (
    <TitleSlide
      variant="blue"
      kicker="Aufsichtsratssitzung"
      title="Gemeinsame Notaufnahme-Struktur für drei Häuser"
      subtitle="Strukturkonzept, Zeitplan und Personalbedarf"
      speaker="Michael Hartmann"
      role="Geschäftsführung"
      date="24. April 2026"
    />
  );
}

/** Nur Thema und Untertitel — für interne Kurzvorträge. */
export function Kurzfassung() {
  return (
    <TitleSlide
      title="Hygienevisite: Ergebnisse des zweiten Halbjahres"
      subtitle="Ergebnisse aller drei Standorte im Überblick"
      date="9. Februar 2026"
    />
  );
}

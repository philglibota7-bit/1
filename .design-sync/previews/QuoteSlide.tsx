import { QuoteSlide } from "@klinik-sh/slides";

/** Vollständige, vorführbare Zitatfolie: Stimme, Funktion, Fußzeile, Seitenzahl. */
export function StimmeAusDerPflege() {
  return (
    <QuoteSlide
      quote="Die neue Ersteinschätzung hat unsere Wartezeiten in der Notaufnahme sichtbar verkürzt — das merken die Patienten sofort."
      author="Sabine Wolf"
      role="Pflegedirektion, Klinikum Crailsheim"
      footerLabel="Qualitätsbericht 2025"
      pageNumber={12}
    />
  );
}

/** Tiefblau als Übergang in ein neues Kapitel — der stärkere Auftritt. */
export function UebergangTiefblau() {
  return (
    <QuoteSlide
      quote="Wir gewinnen keine Pflegekräfte über Prämien, sondern über verlässliche Dienstpläne. Daran müssen wir 2026 zuerst arbeiten."
      author="Dr. med. Andrea Vogt"
      role="Ärztliche Direktion, Die Kliniken Landkreis Schwäbisch Hall"
      tone="blue"
      footerLabel="Qualitätsbericht 2025"
      pageNumber={17}
    />
  );
}

/** `role` als Erhebung statt als Funktion — Rückmeldung aus einer Befragung. */
export function RueckmeldungAusBefragung() {
  return (
    <QuoteSlide
      quote="Die Übergabe zwischen Notaufnahme und Station läuft heute deutlich ruhiger als vor zwei Jahren."
      author="Freitextantwort einer Stationsleitung"
      role="Mitarbeiterbefragung 2025, n = 1.184"
      footerLabel="Qualitätsbericht 2025"
      pageNumber={19}
    />
  );
}

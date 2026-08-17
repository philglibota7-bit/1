import { ClosingSlide } from "@klinik-sh/slides";

/** Vollständige Abschlussfolie: Dank, Schlusssatz und komplette Kontaktkarte. */
export function AbschlussMitKontaktkarte() {
  return (
    <ClosingSlide
      title="Vielen Dank für Ihre Aufmerksamkeit"
      message="Für Rückfragen zu den Kennzahlen des Qualitätsberichts stehe ich gern zur Verfügung."
      contact={{
        name: "Dr. med. Andrea Vogt",
        role: "Leitung Qualitätsmanagement",
        department: "Die Kliniken Landkreis Schwäbisch Hall",
        email: "andrea.vogt@kliniken-sha.de",
        phone: "0791 753-1420",
      }}
    />
  );
}

/** Tiefblau — rahmt den Vortrag ein, wenn auch die Titelfolie blau ist. */
export function AbschlussTiefblau() {
  return (
    <ClosingSlide
      title="Vielen Dank — ich freue mich auf Ihre Fragen"
      message="Der Beschlussvorschlag zur Notaufnahme-Struktur liegt Ihnen als Anlage 3 vor."
      contact={{
        name: "Michael Brenner",
        role: "Kaufmännischer Direktor",
        department: "Die Kliniken Landkreis Schwäbisch Hall",
        email: "michael.brenner@kliniken-sha.de",
        phone: "0791 753-1105",
      }}
      tone="blue"
    />
  );
}

/** Kernbotschaft statt Dank, kurze Kontaktkarte — wirkt aufgeräumter. */
export function AbschlussMitKernbotschaft() {
  return (
    <ClosingSlide
      title="34 offene Pflegestellen sind die Aufgabe für 2026"
      message="Die drei Maßnahmen zur Dienstplanung starten im zweiten Quartal."
      contact={{
        name: "Sabine Wolf",
        role: "Pflegedirektion",
        email: "sabine.wolf@kliniken-sha.de",
      }}
    />
  );
}

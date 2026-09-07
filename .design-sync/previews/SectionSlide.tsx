import { SectionSlide } from "@klinik-sh/slides";

/** Regelfall: zartblauer Kapiteltrenner mit Nummer, Kapitelname und einem Satz. */
export function KapitelZartblau() {
  return (
    <SectionSlide
      index={2}
      total={5}
      title="Leistungsentwicklung"
      subtitle="Fallzahlen, Verweildauer und Auslastung im Fünfjahresvergleich"
      tone="light"
    />
  );
}

/** Tiefblau für den Auftakt eines gewichtigen Blocks. */
export function KapitelTiefblau() {
  return (
    <SectionSlide
      index={4}
      total={5}
      title="Personal und Nachwuchs"
      subtitle="34 offene Pflegestellen, 9,8 % Fluktuation und was wir dagegen unternehmen"
      tone="blue"
    />
  );
}

/** Ruhigste Variante: weiß mit rotem Seitenband. */
export function KapitelMitSeitenband() {
  return (
    <SectionSlide
      index={5}
      total={5}
      title="Beschlussvorschläge"
      subtitle="Drei Vorlagen für die Sitzung des Aufsichtsrats am 12. März 2026"
      tone="band"
    />
  );
}

/** Ohne Kapitelzählung — für Vorträge, die nur einen Themenwechsel markieren. */
export function KapitelOhneZaehlung() {
  return (
    <SectionSlide
      title="Hygiene und Infektionsschutz"
      subtitle="Ergebnisse der Händehygiene-Beobachtungen aus dem vierten Quartal 2025"
      tone="light"
    />
  );
}

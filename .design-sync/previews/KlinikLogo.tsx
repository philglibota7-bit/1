import { BulletList, Callout, KlinikLogo, Slide } from "@klinik-sh/slides";

/**
 * Der Regelfall: die Marke sitzt einmal pro Folie oben rechts im Folienkopf.
 * Hier auf einer vollständigen Inhaltsfolie, damit Größe und Abstand im
 * Verhältnis zur Folie erkennbar sind.
 */
export function MarkeImFolienkopf() {
  return (
    <Slide
      kicker="Hygiene und Infektionsschutz"
      title="Die Händehygiene-Quote liegt erstmals über dem Zielwert"
      footerLabel="Qualitätsbericht 2025"
      pageNumber={14}
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
              text: "Beobachtete Händedesinfektionen: 87,6 % der Indikationen",
              detail: "Zielwert 85 %, Vorjahr 81,4 %",
            },
            {
              text: "Verbrauch Händedesinfektionsmittel: 24,8 ml je Patiententag",
              detail: "Erhebung nach HAND-KISS, 1.240 beobachtete Situationen",
            },
            {
              text: "Vier Stationen liegen weiterhin unter 80 %",
              tone: "accent",
            },
          ]}
        />
        <Callout title="Nächster Schritt" tone="info">
          Schulung der vier Stationen im zweiten Quartal 2026, Nacherhebung im Juli.
        </Callout>
      </div>
    </Slide>
  );
}

/** Die farbige Wortmarke: gestapelt, kompakt und in größerer Auszeichnung. */
export function MarkenvariantenHell() {
  const caption = {
    fontSize: "var(--k-fs-caption)",
    fontWeight: "var(--k-weight-semibold)" as const,
    letterSpacing: "var(--k-tracking-eyebrow)",
    textTransform: "uppercase" as const,
    color: "var(--k-ink-500)",
  };

  return (
    <Slide
      kicker="Marke"
      title="Die Wortmarke in drei Ausführungen"
      footerLabel="Corporate Design — Bausteine"
    >
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-6)" }}>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
            gap: "var(--k-sp-6)",
            alignItems: "start",
          }}
        >
          <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-4)" }}>
            <span style={caption}>Standard, gestapelt</span>
            <KlinikLogo />
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-4)" }}>
            <span style={caption}>Kompakt, einzeilig</span>
            <KlinikLogo layout="compact" />
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-4)" }}>
            <span style={caption}>Größer, Abschlussfolie</span>
            <KlinikLogo size={4.2} />
          </div>
        </div>
        <Callout title="Regel" tone="neutral" compact>
          Die Marke gehört einmal pro Folie oben rechts — nicht zusätzlich in die Fußzeile.
          Sobald die offizielle Logodatei vorliegt, ersetzt die Angabe der Logodatei am
          Folientyp die Textmarke überall gleichzeitig.
        </Callout>
      </div>
    </Slide>
  );
}

/** Auf tiefblauem Grund trägt nur die weiße Marke — die farbige verliert den Kontrast. */
export function MarkeAufTiefblauerFolie() {
  const caption = {
    fontSize: "var(--k-fs-caption)",
    fontWeight: "var(--k-weight-semibold)" as const,
    letterSpacing: "var(--k-tracking-eyebrow)",
    textTransform: "uppercase" as const,
    color: "var(--k-blue-200)",
  };

  return (
    <Slide
      variant="blue"
      kicker="Marke"
      title="Weiße Wortmarke auf tiefblauen Folien"
      footerLabel="Corporate Design — Bausteine"
      showLogo
    >
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-6)" }}>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(2, minmax(0, 1fr))",
            gap: "var(--k-sp-6)",
            alignItems: "start",
          }}
        >
          <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-4)" }}>
            <span style={caption}>Weiß, gestapelt</span>
            <KlinikLogo variant="white" size={3.4} />
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: "var(--k-sp-4)" }}>
            <span style={caption}>Weiß, kompakt</span>
            <KlinikLogo variant="white" layout="compact" size={3.4} />
          </div>
        </div>
        <BulletList
          items={[
            {
              text: "Titel- und Abschlussfolie setzen die Marke selbst — dort kein zweites Logo",
            },
            {
              text: "Auf Kapiteltrennern bleibt die Folie frei von der Marke",
              detail: "Der Kapiteltrenner ist eine Atempause, keine Markenfläche",
            },
          ]}
        />
      </div>
    </Slide>
  );
}

import type { ReactNode } from "react";
import { cx } from "../internal/util.js";
import { KlinikLogo } from "./KlinikLogo.js";

export interface SlideProps {
  /** Überschrift. Ohne Titel entfällt der Kopfbereich vollständig. */
  title?: string;
  /** Kleine Auszeichnung über dem Titel, z. B. Kapitel oder Bereich. */
  kicker?: string;
  /** `light` = weiß, `muted` = zartblau, `blue` = tiefblau mit weißem Text. */
  variant?: "light" | "muted" | "blue";
  /** Beschriftung links im Fuß, z. B. Anlass oder Abteilung. */
  footerLabel?: string;
  /** Seitenzahl rechts im Fuß. Ohne Angabe bleibt der Platz leer. */
  pageNumber?: number | string;
  /** Logo oben rechts einblenden. */
  showLogo?: boolean;
  /** Logodatei für das eingeblendete Logo. */
  logoSrc?: string;
  /** Inhalt vertikal mittig statt oben ausrichten. */
  align?: "top" | "center";
  /** Innenabstand entfernen — für randlose Bild- oder Vollflächenfolien. */
  flush?: boolean;
  /** Dezente blaue Schmuckfläche unten rechts. */
  decor?: boolean;
  children?: ReactNode;
  className?: string;
}

/**
 * Freier 16:9-Folienrahmen mit Kopf- und Fußbereich — die Grundlage aller
 * anderen Folientypen und die richtige Wahl für Layouts, die kein
 * spezialisierter Folientyp abdeckt.
 *
 * Die Folie ist der Skalierungs-Container: alle Inhalte darin wachsen und
 * schrumpfen proportional mit der Folienbreite.
 */
export function Slide({
  title,
  kicker,
  variant = "light",
  footerLabel,
  pageNumber,
  showLogo = false,
  logoSrc,
  align = "top",
  flush = false,
  decor = false,
  children,
  className,
}: SlideProps) {
  const hasFooter = Boolean(footerLabel) || pageNumber !== undefined;

  return (
    <section
      className={cx(
        "ksl-slide",
        `ksl-slide--${variant}`,
        decor && variant !== "blue" && "ksl-slide--decor",
        className,
      )}
    >
      {showLogo && (
        <div className="ksl-slide__logo">
          <KlinikLogo src={logoSrc} variant={variant === "blue" ? "white" : "color"} />
        </div>
      )}

      <div
        className={cx(
          "ksl-slide__body",
          align === "center" && "ksl-slide__body--center",
          flush && "ksl-slide__body--flush",
          showLogo && "ksl-slide__body--haslogo",
        )}
      >
        {(kicker || title) && (
          <header className="ksl-slide__header">
            {kicker && <span className="ksl-kicker">{kicker}</span>}
            {title && (
              <>
                <h2 className="ksl-slide__title">{title}</h2>
                <span className="ksl-rule" style={{ marginTop: "var(--k-sp-4)" }} />
              </>
            )}
          </header>
        )}
        {children}
      </div>

      {hasFooter && (
        <footer className="ksl-slide__footer">
          <span className="ksl-slide__footer-label">{footerLabel}</span>
          <span className="ksl-slide__footer-right">
            {pageNumber !== undefined && <span className="ksl-pagenumber">{pageNumber}</span>}
          </span>
        </footer>
      )}
    </section>
  );
}

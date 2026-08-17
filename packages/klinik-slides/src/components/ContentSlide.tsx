import type { ReactNode } from "react";
import { cx } from "../internal/util.js";
import { KlinikLogo } from "./KlinikLogo.js";

export interface ContentSlideProps {
  /** Aussagesatz als Überschrift — nicht nur ein Stichwort. */
  title: string;
  /** Kleine Auszeichnung über dem Titel, z. B. Kapitel oder Bereich. */
  kicker?: string;
  /** Einleitungssatz unter der Überschrift, ordnet den Inhalt ein. */
  lead?: string;
  /** Spaltenraster für den Inhaltsbereich. */
  columns?: 1 | 2 | 3;
  /** Fußnote über der Fußzeile, z. B. Datenstand oder Definition. */
  footnote?: string;
  /** Beschriftung links im Fuß, z. B. Anlass oder Abteilung. */
  footerLabel?: string;
  /** Seitenzahl rechts im Fuß. */
  pageNumber?: number | string;
  /** Logo oben rechts einblenden. */
  showLogo?: boolean;
  /** Logodatei für das eingeblendete Logo. */
  logoSrc?: string;
  /** `light` = weiß, `muted` = zartblau, `blue` = tiefblau mit weißem Text. */
  variant?: "light" | "muted" | "blue";
  /**
   * Ausrichtung des Inhaltsbereichs im Raum unter der Überschrift.
   * Standard `center` — auf 16:9 sitzt der Inhalt sonst als Block oben und
   * lässt unten eine leere Bahn. `top` für lange Tabellen und Textfolien.
   */
  align?: "top" | "center";
  children?: ReactNode;
  className?: string;
}

/**
 * Standard-Inhaltsfolie: Überschrift, optionaler Einleitungssatz und ein
 * Inhaltsbereich mit ein bis drei Spalten. Der Arbeitsfolientyp für praktisch
 * alles — Aufzählungen, Kennzahlen, Tabellen, Diagramme, Hinweisboxen.
 *
 * Inhaltsbausteine (`BulletList`, `KpiTile`, `DataTable`, `Callout`,
 * `ChartFrame`) werden als `children` hineingegeben; bei `columns={2}` oder
 * `{3}` füllt jedes Kind eine Rasterspalte.
 */
export function ContentSlide({
  title,
  kicker,
  lead,
  columns = 1,
  footnote,
  footerLabel,
  pageNumber,
  showLogo = false,
  logoSrc,
  variant = "light",
  align = "center",
  children,
  className,
}: ContentSlideProps) {
  const hasFooter = Boolean(footerLabel) || pageNumber !== undefined;

  return (
    <section className={cx("ksl-slide", `ksl-slide--${variant}`, className)}>
      {showLogo && (
        <div className="ksl-slide__logo">
          <KlinikLogo src={logoSrc} variant={variant === "blue" ? "white" : "color"} />
        </div>
      )}

      <div className="ksl-slide__body">
        <header className="ksl-slide__header">
          {kicker && <span className="ksl-kicker">{kicker}</span>}
          <h2 className="ksl-slide__title">{title}</h2>
          <span className="ksl-rule" style={{ marginTop: "var(--k-sp-4)", marginBottom: 0 }} />
          {lead && <p className="ksl-slide__lead">{lead}</p>}
        </header>

        <div
          className={cx(
            "ksl-slide__content",
            columns === 2 && "ksl-slide__content--cols-2",
            columns === 3 && "ksl-slide__content--cols-3",
            align === "center" && "ksl-slide__content--middle",
          )}
        >
          {children}
        </div>

        {footnote && <p className="ksl-footnote">{footnote}</p>}
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

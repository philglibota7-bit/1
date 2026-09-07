import { cx } from "../internal/util.js";

export interface QuoteSlideProps {
  /** Zitattext ohne Anführungszeichen — die setzt die Folie selbst. */
  quote: string;
  /** Wer es gesagt hat. */
  author?: string;
  /** Funktion oder Quelle, z. B. „Pflegedirektion“ oder „Patientenbefragung 2025“. */
  role?: string;
  /** `light` = weiß, `blue` = tiefblau. */
  tone?: "light" | "blue";
  /** Beschriftung links im Fuß. */
  footerLabel?: string;
  /** Seitenzahl rechts im Fuß. */
  pageNumber?: number | string;
  className?: string;
}

/**
 * Zitatfolie — eine Stimme, eine Aussage, sonst nichts.
 *
 * Wirkt am stärksten als Ruhepunkt zwischen datenlastigen Folien, etwa mit
 * einer Rückmeldung aus einer Patienten- oder Mitarbeiterbefragung.
 */
export function QuoteSlide({
  quote,
  author,
  role,
  tone = "light",
  footerLabel,
  pageNumber,
  className,
}: QuoteSlideProps) {
  const hasFooter = Boolean(footerLabel) || pageNumber !== undefined;

  return (
    <section
      className={cx("ksl-slide", tone === "blue" ? "ksl-slide--blue" : "ksl-slide--light", className)}
    >
      <div className="ksl-slide__body ksl-quote">
        <span className="ksl-quote__mark" aria-hidden="true">
          „
        </span>
        <blockquote className="ksl-quote__text">{quote}</blockquote>
        {(author || role) && (
          <div className="ksl-quote__footer">
            {author && <span className="ksl-quote__author">{author}</span>}
            {role && <span className="ksl-quote__role">{role}</span>}
          </div>
        )}
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

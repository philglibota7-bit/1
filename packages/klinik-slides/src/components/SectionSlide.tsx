import { cx } from "../internal/util.js";

export interface SectionSlideProps {
  /** Kapitelname. */
  title: string;
  /** Ein Satz dazu, was das Kapitel behandelt. */
  subtitle?: string;
  /** Kapitelnummer, z. B. `2`. */
  index?: number | string;
  /** Gesamtzahl der Kapitel — ergibt zusammen mit `index` „02 / 05“. */
  total?: number | string;
  /** `light` = zartblau, `blue` = tiefblau, `band` = weiß mit rotem Seitenband. */
  tone?: "light" | "blue" | "band";
  className?: string;
}

const pad = (value: number | string) =>
  typeof value === "number" && value < 10 ? `0${value}` : String(value);

/**
 * Kapiteltrenner — markiert den Themenwechsel und gibt dem Publikum
 * eine Orientierung, wo im Vortrag es sich befindet.
 */
export function SectionSlide({
  title,
  subtitle,
  index,
  total,
  tone = "light",
  className,
}: SectionSlideProps) {
  const variant = tone === "blue" ? "blue" : tone === "light" ? "muted" : "light";

  return (
    <section
      className={cx(
        "ksl-slide",
        `ksl-slide--${variant}`,
        tone === "band" && "ksl-section--band",
        className,
      )}
    >
      <div className="ksl-slide__body ksl-section">
        {index !== undefined && (
          <span className="ksl-section__index">
            {pad(index)}
            {total !== undefined && <span className="ksl-section__index-total"> / {pad(total)}</span>}
          </span>
        )}
        <h2 className="ksl-section__title">{title}</h2>
        {subtitle && <p className="ksl-section__subtitle">{subtitle}</p>}
      </div>
    </section>
  );
}

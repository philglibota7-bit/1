import type { CSSProperties } from "react";
import { cx } from "../internal/util.js";

export interface KlinikLogoProps {
  /**
   * Pfad zur offiziellen Logodatei (SVG oder PNG). Ohne `src` wird die
   * Wortmarke aus Text gesetzt — layoutgleich, aber als Platzhalter gedacht.
   */
  src?: string;
  /** Höhe der Marke, in Folienbreiten-Prozent (`cqw`). Standard: 2.6 ≈ 33px. */
  size?: number;
  /** `color` für helle Folien, `white` für blaue Folien. */
  variant?: "color" | "white";
  /** `compact` setzt Träger und Region in eine Zeile. */
  layout?: "stacked" | "compact";
  /** Erste Zeile der Wortmarke. */
  organisation?: string;
  /** Zweite Zeile der Wortmarke, in Akzentrot. */
  region?: string;
  /** Alternativtext für die Logodatei. */
  alt?: string;
  className?: string;
}

/**
 * Wort-/Bildmarke im Folienkopf und auf der Abschlussfolie.
 *
 * Mit `src` wird die echte Logodatei ausgegeben, ohne `src` eine Textmarke in
 * Klinik-Blau und Akzentrot. Für den Produktiveinsatz die offizielle Logodatei
 * hinterlegen — die Textmarke ist bewusst nur ein sauberer Ersatz.
 */
export function KlinikLogo({
  src,
  size = 2.6,
  variant = "color",
  layout = "stacked",
  organisation = "DIE KLINIKEN",
  region = "Landkreis Schwäbisch Hall",
  alt,
  className,
}: KlinikLogoProps) {
  const height = `${size}cqw`;

  if (src) {
    return (
      <img
        src={src}
        alt={alt ?? `${organisation} ${region}`}
        className={cx("ksl-logo__img", className)}
        style={{ height }}
      />
    );
  }

  const style: CSSProperties = {
    fontSize: `${size * 0.42}cqw`,
  };

  return (
    <span
      className={cx(
        "ksl-logo",
        variant === "white" && "ksl-logo--white",
        layout === "compact" && "ksl-logo--compact",
        className,
      )}
      style={style}
      aria-label={`${organisation} ${region}`}
    >
      <span className="ksl-logo__org">{organisation}</span>
      <span className="ksl-logo__region">{region}</span>
    </span>
  );
}

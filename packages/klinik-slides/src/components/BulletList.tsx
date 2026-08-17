import { cx } from "../internal/util.js";
import { IconArrowRight, IconCheck } from "../internal/icons.js";

export interface BulletItem {
  /** Kernaussage — kurz, ein Gedanke. */
  text: string;
  /** Erläuterung in kleinerer, grauer Zweitzeile. */
  detail?: string;
  /** `accent` hebt in Klinik-Blau hervor, `muted` nimmt Gewicht zurück. */
  tone?: "default" | "accent" | "muted";
}

export interface BulletListProps {
  /** Punkte als Text oder als Objekt mit Zweitzeile. */
  items: Array<string | BulletItem>;
  /** Aufzählungszeichen: Häkchen, Punkt, Nummer oder Pfeil. */
  marker?: "check" | "dot" | "number" | "arrow";
  /** Zweispaltig setzen — sinnvoll ab etwa sechs Punkten. */
  columns?: 1 | 2;
  /** `lg` für wenige, tragende Aussagen. */
  size?: "md" | "lg";
  className?: string;
}

const normalize = (item: string | BulletItem): BulletItem =>
  typeof item === "string" ? { text: item } : item;

/**
 * Aufzählung mit Klinik-Aufzählungszeichen und optionaler Zweitzeile je Punkt.
 *
 * Faustregel für Vorträge: höchstens sechs Punkte pro Folie, pro Punkt eine
 * Aussage. Was Erklärung braucht, gehört in `detail` — nicht in einen
 * längeren Hauptsatz.
 */
export function BulletList({
  items,
  marker = "check",
  columns = 1,
  size = "md",
  className,
}: BulletListProps) {
  return (
    <ul
      className={cx(
        "ksl-bullets",
        columns === 2 && "ksl-bullets--cols-2",
        size === "lg" && "ksl-bullets--lg",
        className,
      )}
    >
      {items.map(normalize).map((item, i) => (
        <li
          key={`${item.text}-${i}`}
          className={cx(
            "ksl-bullets__item",
            item.tone === "accent" && "ksl-bullets__item--accent",
            item.tone === "muted" && "ksl-bullets__item--muted",
          )}
        >
          <span className={cx("ksl-bullets__marker", `ksl-bullets__marker--${marker}`)} aria-hidden="true">
            {marker === "check" && <IconCheck />}
            {marker === "arrow" && <IconArrowRight />}
            {marker === "number" && i + 1}
          </span>
          <span className="ksl-bullets__text">
            {item.text}
            {item.detail && <span className="ksl-bullets__detail">{item.detail}</span>}
          </span>
        </li>
      ))}
    </ul>
  );
}

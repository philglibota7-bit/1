import type { ReactNode } from "react";
import { cx } from "../internal/util.js";

export interface ChartLegendItem {
  /** Beschriftung der Reihe. */
  label: string;
  /** Farbe der Reihe; Standard ist Klinik-Blau. Am besten ein Token, z. B. `"var(--k-red)"`. */
  color?: string;
}

export interface ChartFrameProps {
  /** Titel des Diagramms. */
  title?: string;
  /** Legende der Datenreihen. */
  legend?: ChartLegendItem[];
  /** Erläuterung unter dem Diagramm — die Aussage, nicht die Achsen. */
  caption?: string;
  /** Quellenangabe, z. B. „Quelle: Controlling, Stand 31.12.2025“. */
  source?: string;
  /** Höhe der Zeichenfläche, z. B. `"22cqw"` oder `280`. */
  height?: number | string;
  children?: ReactNode;
  className?: string;
}

/**
 * Rahmen für Diagramme: Titel, Legende, Zeichenfläche, Erläuterung, Quelle.
 *
 * Enthält `BarChart` oder eigenes SVG als `children`. Die Quellenangabe ist bei
 * Klinikkennzahlen kein Beiwerk — sie beantwortet die erste Rückfrage aus dem
 * Publikum, bevor sie gestellt wird.
 */
export function ChartFrame({
  title,
  legend,
  caption,
  source,
  height = "20cqw",
  children,
  className,
}: ChartFrameProps) {
  return (
    <figure className={cx("ksl-chart", className)} style={{ margin: 0 }}>
      {(title || legend) && (
        <div className="ksl-chart__head">
          {title && <h3 className="ksl-chart__title">{title}</h3>}
          {legend && legend.length > 0 && (
            <ul className="ksl-chart__legend">
              {legend.map((item) => (
                <li key={item.label} className="ksl-chart__legend-item">
                  <span
                    className="ksl-chart__swatch"
                    style={item.color ? { background: item.color } : undefined}
                    aria-hidden="true"
                  />
                  {item.label}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      <div className="ksl-chart__plot" style={{ height: typeof height === "number" ? `${height}px` : height }}>
        {children}
      </div>

      {caption && <figcaption className="ksl-chart__caption">{caption}</figcaption>}
      {source && <span className="ksl-chart__source">{source}</span>}
    </figure>
  );
}

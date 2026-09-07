import { cx } from "../internal/util.js";

export interface BarChartDatum {
  /** Achsenbeschriftung, z. B. „Chirurgie“ oder „2025“. */
  label: string;
  /** Zahlenwert. */
  value: number;
  /** `blue` (Standard), `accent` für den hervorgehobenen Balken, `muted` für Vergleichswerte. */
  tone?: "blue" | "accent" | "muted";
  /** Angezeigter Wert, falls er anders formatiert werden soll als `value`. */
  display?: string;
}

export interface BarChartProps {
  /** Datenpunkte in Anzeigereihenfolge. */
  data: BarChartDatum[];
  /** Obergrenze der Skala; Standard ist der größte Wert plus Luft nach oben. */
  max?: number;
  /** Einheit hinter den Werten, z. B. `" %"` oder `" Tage"`. */
  unit?: string;
  /** `vertical` = Säulen (Zeitreihen), `horizontal` = Balken (Rangfolgen). */
  orientation?: "vertical" | "horizontal";
  /** Werte an den Balken anzeigen. */
  showValues?: boolean;
  /** Ziel- oder Referenzwert als gestrichelte rote Linie (nur bei Säulen). */
  target?: number;
  /** Beschriftung der Ziellinie, z. B. „Ziel 85 %“. */
  targetLabel?: string;
  className?: string;
}

const fmt = (value: number) =>
  new Intl.NumberFormat("de-DE", { maximumFractionDigits: 1 }).format(value);

/**
 * Balken- und Säulendiagramm ohne Diagrammbibliothek — reines CSS, damit es in
 * jeder Umgebung (Vorschau, Vollbild, Ausdruck) identisch aussieht.
 *
 * `vertical` für Verläufe über die Zeit, `horizontal` für Vergleiche zwischen
 * Abteilungen oder Standorten. Wird in `ChartFrame` gesetzt, der Titel,
 * Legende und Quelle beisteuert.
 */
export function BarChart({
  data,
  max,
  unit = "",
  orientation = "vertical",
  showValues = true,
  target,
  targetLabel,
  className,
}: BarChartProps) {
  const peak = Math.max(...data.map((d) => d.value), target ?? 0);
  const scale = max ?? peak * 1.12;
  const pct = (value: number) => `${Math.max(0, Math.min(100, (value / scale) * 100))}%`;

  if (orientation === "horizontal") {
    return (
      <div className={cx("ksl-bars", "ksl-bars--horizontal", className)}>
        {data.map((d) => (
          <div key={d.label} className="ksl-bars__col">
            <span className="ksl-bars__label">{d.label}</span>
            <span className="ksl-bars__track">
              <span
                className={cx("ksl-bars__bar", d.tone && d.tone !== "blue" && `ksl-bars__bar--${d.tone}`)}
                style={{ width: pct(d.value), display: "block" }}
              />
            </span>
            <span className="ksl-bars__value">{showValues ? `${d.display ?? fmt(d.value)}${unit}` : ""}</span>
          </div>
        ))}
      </div>
    );
  }

  // Balken sind absolut im Zeichenbereich positioniert und die Wertebeschriftung
  // sitzt an der Balkenspitze: nur so ist die Balkenhöhe exakt der Anteil an der
  // Skala — im Fluss würden Wert- und Achsenbeschriftung den Balken stauchen und
  // die Ziellinie läge nicht mehr auf derselben Skala.
  return (
    <div className={cx("ksl-bars", className)}>
      <div className="ksl-bars__plot">
        {data.map((d) => {
          const height = pct(d.value);
          return (
            <div key={d.label} className="ksl-bars__col">
              <span
                className={cx("ksl-bars__bar", d.tone && d.tone !== "blue" && `ksl-bars__bar--${d.tone}`)}
                style={{ height }}
              />
              {showValues && (
                <span className="ksl-bars__value" style={{ bottom: `calc(${height} + 0.5cqw)` }}>
                  {`${d.display ?? fmt(d.value)}${unit}`}
                </span>
              )}
            </div>
          );
        })}
        {target !== undefined && (
          <div className="ksl-bars__target" style={{ bottom: pct(target) }}>
            {targetLabel && <span className="ksl-bars__target-label">{targetLabel}</span>}
          </div>
        )}
      </div>
      <div className="ksl-bars__labels">
        {data.map((d) => (
          <span key={d.label} className="ksl-bars__label">
            {d.label}
          </span>
        ))}
      </div>
    </div>
  );
}

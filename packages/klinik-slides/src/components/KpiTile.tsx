import { cx } from "../internal/util.js";
import { IconTrend } from "../internal/icons.js";

export interface KpiTileProps {
  /** Der Wert selbst, bereits deutsch formatiert (z. B. `"12.480"`, `"4,3"`). */
  value: string | number;
  /** Was gemessen wurde, z. B. „Stationäre Fälle“. */
  label: string;
  /** Einheit hinter dem Wert, z. B. „Tage“, „%“. */
  unit?: string;
  /** Veränderung als Text, z. B. `"+4,2 %"` oder `"−0,3 Tage"`. */
  delta?: string;
  /** Richtung der Veränderung — nur Symbol, bewertet nichts. */
  trend?: "up" | "down" | "flat";
  /** Farbgebung. `positive`/`warning` bewerten, `blue`/`accent` heben hervor. */
  tone?: "neutral" | "blue" | "accent" | "positive" | "warning";
  /** Bezugsgröße oder Datenstand, z. B. „Vorjahr: 11.960“. */
  footnote?: string;
  className?: string;
}

/**
 * Kennzahlen-Kachel für Fallzahlen, Belegung, Verweildauer, Quoten.
 *
 * In `ContentSlide` mit `columns={3}` legen drei Kacheln eine vollständige
 * Kennzahlenfolie. Die Richtung (`trend`) ist absichtlich von der Bewertung
 * (`tone`) getrennt: eine sinkende Verweildauer ist ein Erfolg, eine sinkende
 * Fallzahl nicht.
 */
export function KpiTile({
  value,
  label,
  unit,
  delta,
  trend,
  tone = "neutral",
  footnote,
  className,
}: KpiTileProps) {
  return (
    <div className={cx("ksl-kpi", tone !== "neutral" && `ksl-kpi--${tone}`, className)}>
      <span className="ksl-kpi__label">{label}</span>
      <span className="ksl-kpi__value">
        {value}
        {unit && <span className="ksl-kpi__unit">{unit}</span>}
      </span>
      {delta && (
        <span className="ksl-kpi__delta">
          {trend && (
            <span className="ksl-kpi__trend">
              <IconTrend direction={trend} />
            </span>
          )}
          {delta}
        </span>
      )}
      {footnote && <span className="ksl-kpi__footnote">{footnote}</span>}
    </div>
  );
}

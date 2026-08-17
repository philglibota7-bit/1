import type { ReactNode } from "react";
import { cx } from "../internal/util.js";
import { IconCheck } from "../internal/icons.js";

export interface CalloutProps {
  /** Fette Kopfzeile der Box. */
  title?: string;
  /** `info` blau, `success` grün, `warning` amber, `critical` rot, `neutral` grau. */
  tone?: "info" | "success" | "warning" | "critical" | "neutral";
  /** Eigenes Symbol; `false` blendet das Symbol aus. */
  icon?: ReactNode | false;
  /** Kompakte Variante für Randbemerkungen. */
  compact?: boolean;
  children?: ReactNode;
  className?: string;
}

const defaultIcon: Record<string, ReactNode> = {
  info: "i",
  warning: "!",
  critical: "!",
  neutral: "i",
};

/**
 * Hinweisbox für Merksätze, Fristen, Risiken und Beschlüsse.
 *
 * `critical` ist für echte Risiken reserviert (Fristablauf, Personalengpass) —
 * inflationär eingesetzt verliert die Farbe auf Klinikfolien ihre Wirkung.
 */
export function Callout({
  title,
  tone = "info",
  icon,
  compact = false,
  children,
  className,
}: CalloutProps) {
  const symbol = icon === false ? null : (icon ?? (tone === "success" ? <IconCheck /> : defaultIcon[tone]));

  return (
    <aside
      className={cx("ksl-callout", tone !== "info" && `ksl-callout--${tone}`, compact && "ksl-callout--compact", className)}
    >
      {symbol !== null && (
        <span className="ksl-callout__icon" aria-hidden="true">
          {symbol}
        </span>
      )}
      <div className="ksl-callout__body">
        {title && <p className="ksl-callout__title">{title}</p>}
        {children}
      </div>
    </aside>
  );
}

import { cx } from "../internal/util.js";
import { KlinikLogo } from "./KlinikLogo.js";

export interface TitleSlideProps {
  /** Thema des Vortrags — die größte Zeile der Präsentation. */
  title: string;
  /** Erläuternder Untertitel, ein Satz. */
  subtitle?: string;
  /** Anlass über dem Titel, z. B. „Chefarztkonferenz“. */
  kicker?: string;
  /** Name des Vortragenden. */
  speaker?: string;
  /** Funktion des Vortragenden, z. B. „Leitung Qualitätsmanagement“. */
  role?: string;
  /** Datum, frei formatiert, z. B. „12. März 2026“. */
  date?: string;
  /** Ort oder Haus, z. B. „Diakonie-Klinikum Schwäbisch Hall“. */
  place?: string;
  /** Logodatei; ohne Angabe erscheint die Textmarke. */
  logoSrc?: string;
  /** `light` = weiß (Standard), `blue` = tiefblaue Titelfolie. */
  variant?: "light" | "blue";
  className?: string;
}

/**
 * Titelfolie — Einstieg der Präsentation.
 *
 * Aufbau: Anlass, Akzentlinie, Thema, Untertitel, darunter die Angaben zu
 * Person, Datum und Ort. Das Logo sitzt oben rechts.
 */
export function TitleSlide({
  title,
  subtitle,
  kicker,
  speaker,
  role,
  date,
  place,
  logoSrc,
  variant = "light",
  className,
}: TitleSlideProps) {
  const meta = [speaker, role, date, place].some(Boolean);

  return (
    <section
      className={cx("ksl-slide", `ksl-slide--${variant}`, variant === "light" && "ksl-slide--decor", className)}
    >
      <div className="ksl-slide__logo">
        <KlinikLogo src={logoSrc} size={3} variant={variant === "blue" ? "white" : "color"} />
      </div>

      <div className="ksl-slide__body ksl-title-slide__body">
        {kicker && <span className="ksl-kicker">{kicker}</span>}
        <span className="ksl-rule ksl-rule--wide" />
        <h1 className="ksl-title">{title}</h1>
        {subtitle && <p className="ksl-title-slide__subtitle">{subtitle}</p>}

        {meta && (
          <div className="ksl-slide__meta">
            {speaker && (
              <span className="ksl-slide__meta-item">
                <span className="ksl-slide__meta-strong">{speaker}</span>
                {role && <span>{role}</span>}
              </span>
            )}
            {date && <span className="ksl-slide__meta-item">{date}</span>}
            {place && <span className="ksl-slide__meta-item">{place}</span>}
          </div>
        )}
      </div>
    </section>
  );
}

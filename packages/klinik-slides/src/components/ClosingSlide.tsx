import { cx } from "../internal/util.js";
import { KlinikLogo } from "./KlinikLogo.js";

export interface ClosingContact {
  /** Name der Ansprechperson. */
  name: string;
  /** Funktion, z. B. „Leitung Qualitätsmanagement“. */
  role?: string;
  /** Abteilung oder Haus. */
  department?: string;
  /** E-Mail-Adresse. */
  email?: string;
  /** Telefonnummer. */
  phone?: string;
}

export interface ClosingSlideProps {
  /** Schlusszeile. Standard: „Vielen Dank für Ihre Aufmerksamkeit“. */
  title?: string;
  /** Ein Satz darunter, z. B. eine Einladung zur Diskussion. */
  message?: string;
  /** Kontaktkarte mit Ansprechperson. */
  contact?: ClosingContact;
  /** Logodatei; ohne Angabe erscheint die Textmarke. */
  logoSrc?: string;
  /** `light` = weiß, `blue` = tiefblau. */
  tone?: "light" | "blue";
  className?: string;
}

/**
 * Abschlussfolie mit Dank, optionalem Schlusssatz und Kontaktkarte —
 * die Folie, die während der Diskussion stehen bleibt. Deshalb gehören
 * hier die Kontaktdaten hin, nicht auf die Titelfolie.
 */
export function ClosingSlide({
  title = "Vielen Dank für Ihre Aufmerksamkeit",
  message,
  contact,
  logoSrc,
  tone = "light",
  className,
}: ClosingSlideProps) {
  return (
    <section
      className={cx(
        "ksl-slide",
        tone === "blue" ? "ksl-slide--blue" : "ksl-slide--light",
        tone === "light" && "ksl-slide--decor",
        className,
      )}
    >
      <div className="ksl-slide__logo">
        <KlinikLogo src={logoSrc} size={3} variant={tone === "blue" ? "white" : "color"} />
      </div>

      <div className="ksl-slide__body ksl-slide__body--center">
        <span className="ksl-rule ksl-rule--wide" />
        <h2 className="ksl-title">{title}</h2>
        {message && <p className="ksl-closing__message">{message}</p>}

        {contact && (
          <div className="ksl-contact">
            <span className="ksl-contact__name">{contact.name}</span>
            {contact.role && <span className="ksl-contact__role">{contact.role}</span>}
            {contact.department && <span className="ksl-contact__role">{contact.department}</span>}
            {contact.email && <span className="ksl-contact__line">{contact.email}</span>}
            {contact.phone && <span className="ksl-contact__line">{contact.phone}</span>}
          </div>
        )}
      </div>
    </section>
  );
}

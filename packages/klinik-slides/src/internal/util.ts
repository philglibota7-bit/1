/** Klassennamen zusammensetzen und leere Werte verwerfen. */
export function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

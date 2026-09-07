/**
 * Symbole als Inline-SVG statt als Schriftzeichen: Häkchen und Pfeile liegen
 * außerhalb des ausgelieferten Inter-Subsets und würden sonst aus einer
 * Systemschrift ersetzt werden — auf Folien sofort sichtbar.
 */

const box = {
  viewBox: "0 0 16 16",
  width: "1em",
  height: "1em",
  fill: "none",
  focusable: "false" as const,
  "aria-hidden": true,
};

export function IconCheck() {
  return (
    <svg {...box} stroke="currentColor" strokeWidth={2.4} strokeLinecap="round" strokeLinejoin="round">
      <polyline points="3.5,8.6 6.4,11.5 12.5,4.9" />
    </svg>
  );
}

export function IconArrowRight() {
  return (
    <svg {...box} stroke="currentColor" strokeWidth={2.2} strokeLinecap="round" strokeLinejoin="round">
      <line x1="2.5" y1="8" x2="12.5" y2="8" />
      <polyline points="8.4,3.9 12.6,8 8.4,12.1" />
    </svg>
  );
}

export function IconTrend({ direction }: { direction: "up" | "down" | "flat" }) {
  if (direction === "flat") {
    return (
      <svg {...box} stroke="currentColor" strokeWidth={2.2} strokeLinecap="round">
        <line x1="3" y1="8" x2="13" y2="8" />
      </svg>
    );
  }
  return (
    <svg {...box} fill="currentColor">
      {direction === "up" ? (
        <polygon points="8,3.4 13.2,11.6 2.8,11.6" />
      ) : (
        <polygon points="8,12.6 2.8,4.4 13.2,4.4" />
      )}
    </svg>
  );
}

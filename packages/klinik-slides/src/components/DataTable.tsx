import type { ReactNode } from "react";
import { cx } from "../internal/util.js";

export interface DataTableColumn {
  /** Schlüssel, unter dem der Wert in jeder Zeile liegt. */
  key: string;
  /** Spaltenkopf. */
  label: string;
  /** Zahlen rechts, Text links ausrichten. */
  align?: "left" | "right" | "center";
  /** Feste Spaltenbreite, z. B. `"18%"`. */
  width?: string;
}

export interface DataTableProps {
  /** Spaltendefinition in Anzeigereihenfolge. */
  columns: DataTableColumn[];
  /** Datenzeilen; je Spaltenschlüssel ein Wert. */
  rows: Array<Record<string, ReactNode>>;
  /** Tabellentitel über der Tabelle. */
  caption?: string;
  /** Quellenangabe unter der Tabelle, z. B. „Quelle: Medizincontrolling“. */
  source?: string;
  /** Zeilenindizes (ab 0), die blau hervorgehoben werden. */
  highlightRows?: number[];
  /** Summenzeile am Fuß, fett und abgesetzt. */
  totalRow?: Record<string, ReactNode>;
  /** Abwechselnde Zeilenhintergründe. */
  zebra?: boolean;
  /** Geringere Zeilenhöhe — für mehr als acht Zeilen. */
  dense?: boolean;
  className?: string;
}

/**
 * Tabelle für Kennzahlen je Fachabteilung, Standort oder Zeitraum.
 *
 * Auf Folien lesbar bleiben bis etwa zehn Zeilen und sechs Spalten; darüber
 * lieber aufteilen oder auf ein Diagramm wechseln. Zahlen laufen mit
 * gleichbreiten Ziffern, damit Spalten optisch fluchten.
 */
export function DataTable({
  columns,
  rows,
  caption,
  source,
  highlightRows = [],
  totalRow,
  zebra = false,
  dense = false,
  className,
}: DataTableProps) {
  const alignClass = (col: DataTableColumn) =>
    col.align === "right"
      ? "ksl-table__cell--right"
      : col.align === "center"
        ? "ksl-table__cell--center"
        : undefined;

  return (
    <div className={cx("ksl-table-wrap", className)}>
      {caption && <span className="ksl-table__caption">{caption}</span>}
      <table className={cx("ksl-table", zebra && "ksl-table--zebra", dense && "ksl-table--dense")}>
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col.key} scope="col" className={alignClass(col)} style={col.width ? { width: col.width } : undefined}>
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, rowIndex) => (
            <tr
              key={rowIndex}
              className={cx(highlightRows.includes(rowIndex) && "ksl-table__row--highlight")}
            >
              {columns.map((col) => (
                <td key={col.key} className={alignClass(col)}>
                  {row[col.key]}
                </td>
              ))}
            </tr>
          ))}
          {totalRow && (
            <tr className="ksl-table__row--total">
              {columns.map((col) => (
                <td key={col.key} className={alignClass(col)}>
                  {totalRow[col.key]}
                </td>
              ))}
            </tr>
          )}
        </tbody>
      </table>
      {source && <span className="ksl-table__source">{source}</span>}
    </div>
  );
}

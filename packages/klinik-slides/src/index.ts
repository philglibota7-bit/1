/**
 * Klinik-Präsentation — Design-System für Vorträge im Klinik-CI.
 *
 * Folientypen (16:9): Slide, TitleSlide, SectionSlide, ContentSlide,
 * QuoteSlide, ClosingSlide.
 * Inhaltsbausteine: BulletList, KpiTile, DataTable, Callout, ChartFrame,
 * BarChart. Marke: KlinikLogo.
 */

export { Slide } from "./components/Slide.js";
export type { SlideProps } from "./components/Slide.js";

export { TitleSlide } from "./components/TitleSlide.js";
export type { TitleSlideProps } from "./components/TitleSlide.js";

export { SectionSlide } from "./components/SectionSlide.js";
export type { SectionSlideProps } from "./components/SectionSlide.js";

export { ContentSlide } from "./components/ContentSlide.js";
export type { ContentSlideProps } from "./components/ContentSlide.js";

export { QuoteSlide } from "./components/QuoteSlide.js";
export type { QuoteSlideProps } from "./components/QuoteSlide.js";

export { ClosingSlide } from "./components/ClosingSlide.js";
export type { ClosingSlideProps, ClosingContact } from "./components/ClosingSlide.js";

export { BulletList } from "./components/BulletList.js";
export type { BulletListProps, BulletItem } from "./components/BulletList.js";

export { KpiTile } from "./components/KpiTile.js";
export type { KpiTileProps } from "./components/KpiTile.js";

export { DataTable } from "./components/DataTable.js";
export type { DataTableProps, DataTableColumn } from "./components/DataTable.js";

export { Callout } from "./components/Callout.js";
export type { CalloutProps } from "./components/Callout.js";

export { ChartFrame } from "./components/ChartFrame.js";
export type { ChartFrameProps, ChartLegendItem } from "./components/ChartFrame.js";

export { BarChart } from "./components/BarChart.js";
export type { BarChartProps, BarChartDatum } from "./components/BarChart.js";

export { KlinikLogo } from "./components/KlinikLogo.js";
export type { KlinikLogoProps } from "./components/KlinikLogo.js";

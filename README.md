# 1

Statische Seiten (GitHub Pages) und ein Präsentations-Design-System.

## Seiten

| Datei | Inhalt |
|---|---|
| `index.html` | „For Marwa“ — interaktive Seite |
| `bodyscan.html` | FitScan — Körperscan und Kleidungsgrößen |
| `fussball.html` | Fußball-Arena |
| `ip-rechner.html` | IP-Rechner: Subnetting, IPv6, Taschenrechner |
| `jarvis.html` | J.A.R.V.I.S. — Assistent mit Routenplaner |

## Präsentations-Design-System (`packages/klinik-slides`)

Baukasten für Vorträge im Corporate Design der Kliniken Landkreis Schwäbisch
Hall: 13 React-Komponenten (Folientypen 16:9, Inhaltsbausteine, Wortmarke),
Design-Tokens in Klinik-Blau `#00417B` und Akzentrot `#E2001A`, Inter als
selbst gehostete Schrift.

```sh
npm --prefix packages/klinik-slides install
npm --prefix packages/klinik-slides run build     # Bundle, Typen, CSS, Schriften
```

Verwendung:

```jsx
import "@klinik-sh/slides/styles.css";
import { ContentSlide, KpiTile } from "@klinik-sh/slides";
```

Für den Einsatz in **claude.ai/design** erzeugt

```sh
./scripts/design-system-bauen.sh
```

das vollständige Upload-Paket (`ds-bundle/` und
`ds-bundle-klinik-praesentation.zip`): kompiliertes Bundle, Stylesheet,
Schriften, pro Komponente Typen, Anleitung und geprüfte Vorschaukarte.

Konfiguration und Notizen dazu liegen in `.design-sync/`:
`config.json` (Konverter-Einstellungen), `conventions.md` (Anleitung für den
Design-Agenten), `previews/` (handgeschriebene Vorschaukarten), `NOTES.md`
(Stolperstellen und Re-Sync-Hinweise).

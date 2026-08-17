# design-sync — Notizen zu diesem Repo

Das Design-System ist in diesem Repo **neu entstanden** (kein Import einer
bestehenden Bibliothek): `packages/klinik-slides` (`@klinik-sh/slides`) ist ein
Präsentations-Baukasten im CI der Kliniken Landkreis Schwäbisch Hall, gebaut für
die Verwendung in claude.ai/design. Das übrige Repo (`index.html`, `jarvis.html`
usw.) hat damit nichts zu tun und wird vom Konverter nicht angefasst.

## Einmal-Einrichtung nach einem frischen Clone

- `npm --prefix packages/klinik-slides install` — Paket-Abhängigkeiten
  (`packages/*/dist/` und `node_modules/` sind bewusst nicht eingecheckt).
- `.ds-sync/` (gestagte Konverter-Skripte) ist gitignored und muss vom
  design-sync-Skill neu abgelegt werden; danach läuft
  `./scripts/design-system-bauen.sh` alles in einem Durchlauf durch
  (Paket-Build → Konverter → Validierung → ZIP).
- Konverter-Deps in `.ds-sync/`: `npm i esbuild ts-morph @types/react playwright@1.56.1`.

## Gotchas, die Zeit gekostet haben

- **`cfg.tokensGlob` greift nur für ein separates Token-Paket in
  `node_modules`.** Die Tokens dieses Pakets liegen in seinem eigenen `dist/`,
  wurden dadurch nirgends kopiert und `package-validate` meldete
  `[TOKENS_MISSING]` (59 Variablen). Lösung: der Paket-Build erzeugt zusätzlich
  `dist/klinik-slides.css` mit **Tokens + Komponenten-Regeln in einer Datei**,
  und `cfg.cssEntry` zeigt darauf. `tokens/` im Upload-Paket bleibt deshalb leer
  — das ist beabsichtigt, die Tokens reisen im Komponenten-CSS und sind damit
  über die `styles.css`-Importkette für gerenderte Designs erreichbar.
- **`lib/preview-rebuild.mjs` erneuert nur die Vorschau-`.tsx`-Kompilate**, nicht
  `_ds_bundle.js` und nicht `_ds_bundle.css`. Nach jeder Änderung an
  Komponentenquellen oder CSS muss `package-build.mjs` laufen, sonst zeigt das
  Sheet den alten Stand (dieser Fehler kostete einen kompletten Review-Zyklus).
- **Playwright-Version an den vorinstallierten Chromium binden**: in dieser
  Umgebung liegt `chromium-1194` unter `/opt/pw-browsers` → `playwright@1.56.1`
  (1.55.1 pinnt 1193, 1.57.0 pinnt 1200). Falsche Version ⇒
  `browserType.launch: Executable doesn't exist`.
- **Google-Fonts-CSS liefert pro Schriftschnitt dieselbe Datei** (Inter ist ein
  Variable Font). Acht heruntergeladene Dateien waren vier Duplikat-Paare;
  ausgeliefert werden zwei Dateien (`latin`, `latin-ext`) mit
  `font-weight: 100 900`. Beide liegen als Quelle unter
  `packages/klinik-slides/src/fonts/` im Repo — kein Netzzugriff beim Bauen.
- **Häkchen, Pfeile und Trend-Dreiecke sind Inline-SVG, keine Schriftzeichen.**
  `✓` (U+2713), `→` (U+2192) und `▲` (U+25B2) liegen außerhalb der
  ausgelieferten Inter-Subsets und würden aus einer Systemschrift ersetzt — auf
  Folien sofort sichtbar. Wer neue Symbole braucht: `src/internal/icons.tsx`.

## Architektur-Entscheidung, die man kennen muss

Alle Größen sind in `cqw` notiert, der Folienrahmen setzt
`container-type: inline-size`. Dadurch skaliert eine Folie proportional
(Vollbild, Vorschaukarte, Ausdruck) — aber **Inhaltsbausteine freistehend
gerendert beziehen ihre `cqw`-Größen auf den Viewport** und sehen dann falsch
aus. Deshalb rendert jede Vorschaudatei ihren Baustein innerhalb einer Folie.
Wer künftig eine Vorschau ohne Folienrahmen schreibt, produziert eine
scheinbar kaputte Karte.

## Bekannte Warnungen im Render-Check

- `[RENDER_THIN] … mounted text is just "<Name>"` erscheint für jede Komponente
  **ohne** eigene Vorschaudatei (Platzhalter-Kachel). Nach dem Authoring aller
  13 Komponenten darf diese Warnung nicht mehr auftreten — wenn doch, ist eine
  `.tsx` nicht kompiliert (Build-Log: `! preview build failed: <Name>`).
- `tokens: 65 defined, 59 referenced` ist der gesunde Zustand.

## Upload

`DesignSync` ließ sich in dieser Umgebung nicht autorisieren
(`/design-login` braucht ein interaktives Terminal). Der Upload lief daher
**manuell**: `./scripts/design-system-bauen.sh` erzeugt
`ds-bundle-klinik-praesentation.zip` mit genau dem Dateisatz, den ein
Design-System-Projekt erwartet; Punkt-Dateien und `_screenshots/` bleiben
draußen. In einer Sitzung mit autorisiertem `DesignSync` stattdessen den
normalen Weg gehen (`finalize_plan` → `write_files` → `_ds_sync.json` zuletzt)
und die `projectId` hier in `config.json` eintragen — dann werden künftige
Syncs inkrementell.

## Re-sync: worauf zu achten ist

- **Kein `projectId` in `config.json`** (Upload war manuell). Solange das so
  bleibt, hat jeder Sync keinen Anker und prüft alle Komponenten neu — korrekt,
  aber langsamer. Nach dem ersten echten Upload nachtragen.
- **Das Logo ist eine Textmarke als Platzhalter.** Sobald die offizielle
  Logodatei vorliegt: Datei ins Projekt legen und `logoSrc` an den Folientypen
  setzen. Nicht die Wortmarke „schöner“ nachbauen.
- **Die Markenfarben (`#00417B` Blau, `#E2001A` Rot) sind aus dem Logobild
  abgeleitet**, nicht aus einem offiziellen CI-Handbuch. Liegen exakte Werte
  vor, nur `src/styles/tokens.css` anpassen — alles andere zieht nach.
- Vorschaudateien unter `.design-sync/previews/` sind eingecheckt und
  handgeschrieben; der Konverter fasst sie nie an. Sie sind die Quelle der
  Kartenqualität, nicht `ds-bundle/`.
- `dist/klinik-slides.css` ist generiert. Wer Komponenten-CSS ändert, ändert
  `src/styles/components.css` bzw. `src/styles/tokens.css`.

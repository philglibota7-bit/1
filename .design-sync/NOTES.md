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

## Höhenbudget der Folie — die häufigste Fehlerquelle

16:9 ist knapp. Unter dem Kopfbereich bleiben etwa **40–43 cqw**; ein zweizeiliger
Titel kostet rund 4,5 cqw, jede Zusatzangabe (Einleitungssatz, Fußnote,
Quellenzeile, Hinweisbox) etwa eine Zeile. Im Review lief das bei sechs von
achtzehn Kombinationsfolien über — Tabellenzeilen und Hinweisboxen schoben sich
über Fußnote und Fußzeile.

Zwei Konsequenzen, beide eingebaut:

- `.ksl-slide__body` hat jetzt `overflow: hidden`. Zu hoher Inhalt wird
  abgeschnitten statt über die Fußzeile gezeichnet — abgeschnitten ist schlecht,
  übereinanderliegender Text ist unlesbar.
- Die Grenzwerte stehen in `docs/DataTable.md`, `docs/BulletList.md`,
  `docs/Slide.md` und im Leitfaden: **sechs Datenzeilen plus Summe** (mit `dense`
  acht), **vier bis fünf Aufzählungspunkte mit Zweitzeilen**, KPI-Reihe **oder**
  Tabelle mit Summenzeile — nicht beides.

Wer eine Folie überfüllt, sieht keinen Fehler im Build und keine Warnung im
Capture. Nur der Screenshot zeigt es. Deshalb: nach jeder inhaltlichen Änderung
an einer Vorschau das Sheet ansehen.

## Behobene Designfehler (nicht wieder einbauen)

- **Titel lief in die Wortmarke.** `.ksl-slide__logo` ist absolut positioniert;
  der Kopfbereich reservierte keinen Platz. Ab etwa 40 Zeichen — also bei jedem
  Aussagesatz — überlappten Titel und Marke. Behoben über
  `.ksl-slide__body--haslogo .ksl-slide__header { padding-right: 17cqw }`, gesetzt
  von `Slide` und `ContentSlide`, wenn `showLogo` aktiv ist.
- **Zentrierter Inhalt lief nach oben über.** `justify-content: center` überläuft
  bei zu hohem Inhalt nach **beiden** Seiten und schob den Inhaltsbereich über
  Einleitungssatz und Überschrift. Behoben mit `justify-content: safe center`
  (`safe` ist hier zwingend, nicht kosmetisch).
- **Balkendiagramm skalierte falsch.** Werte- und Achsenbeschriftung lagen im
  Balkenfluss und stauchten ihn; die Ziellinie lag dadurch auf einer anderen
  Skala als die Balken. Behoben: Balken absolut im Zeichenbereich, Wert an der
  Balkenspitze, Achsenbeschriftungen in eigener Zeile darunter.
- **`decor` war auf `variant="muted"` unsichtbar** (Schmuckfläche und
  Folienhintergrund beide `--k-blue-50`). Behoben mit `--k-blue-100` auf muted.
- **Ziellinien-Beschriftung war unlesbar**, wenn die Ziellinie tief liegt und ein
  Balken dahinter steht. Behoben mit hellem Träger hinter der Beschriftung.
- **Weiße Folien hatten keine erkennbare Kante** — auf hellem Grund (Vorschau,
  Übersicht, Handout) schwebte der Inhalt. Behoben mit einem sehr feinen
  Schatten auf `.ksl-slide`.

## Offene Punkte (bewusst nicht umgesetzt)

- **Kopf oben, Inhalt mittig ist auf `Slide` nicht ausdrückbar.** `align="center"`
  zentriert den ganzen Textkörper einschließlich Kicker, Titel und Akzentlinie.
  `ContentSlide` trennt das (fester Kopf, `align` nur für den Inhalt); für `Slide`
  wäre eine zusätzliche Prop `contentAlign` die saubere Lösung.
- **Die Größenachse der Text-Wortmarke ist kaum wahrnehmbar**, weil ohne `src`
  nur die Schriftgröße skaliert. Statt die Platzhaltermarke aufwendiger zu bauen,
  nennt `docs/KlinikLogo.md` jetzt brauchbare Stufen (2,6 / 3 / ab 4,2). Mit der
  echten Logodatei greift `size` unmittelbar als Bildhöhe — das Thema löst sich
  damit von selbst.

## Bekannte Warnungen im Render-Check

Der aktuelle Stand ist **warnungsfrei** — alle 13 Komponenten haben eine eigene
Vorschaudatei, `package-validate.mjs` läuft ohne eine einzige `!`-Zeile durch.
Jede neue Warnung ist damit wirklich neu. Zwei Zeilen zur Einordnung:

- `[RENDER_THIN] … mounted text is just "<Name>"` erscheint nur für Komponenten
  **ohne** eigene Vorschaudatei (Platzhalter-Kachel). Tritt sie auf, ist eine
  `.tsx` nicht kompiliert (Build-Log: `! preview build failed: <Name>`).
- `tokens: 65 defined, 59 referenced` ist der gesunde Zustand.
- `tokens/` im Upload-Paket ist leer — beabsichtigt, siehe Gotcha oben.

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

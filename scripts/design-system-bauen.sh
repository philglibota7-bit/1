#!/usr/bin/env bash
#
# Baut das Klinik-Präsentations-Design-System in einem Durchlauf und packt das
# Upload-Paket für claude.ai/design.
#
#   ./scripts/design-system-bauen.sh
#
# Ergebnis:
#   ds-bundle/                              — Upload-Paket (Ordnerform)
#   ds-bundle-klinik-praesentation.zip      — dasselbe als ZIP zum Hochladen
#
# Schritte: Paket-Build (Bundle, Typen, CSS, Schriften) → Konverter → Validierung
# (Render-Check im Browser) → ZIP. Bricht bei jedem Fehler ab.
set -euo pipefail

cd "$(dirname "$0")/.."
ROOT="$PWD"
PKG="packages/klinik-slides"
OUT="ds-bundle"
ZIP="ds-bundle-klinik-praesentation.zip"

if [ ! -d ".ds-sync" ]; then
  cat >&2 <<'EOF'
✗ .ds-sync/ fehlt — darin liegen die Konverter-Skripte des design-sync-Skills.
  Sie sind absichtlich nicht eingecheckt (sie gehören zum Skill, nicht zum Repo).
  In einer Claude-Code-Sitzung mit /design-sync werden sie neu abgelegt; danach
  läuft dieses Skript wieder durch.
EOF
  exit 1
fi

echo "▸ 1/4  Abhängigkeiten des Pakets"
if [ ! -d "$PKG/node_modules" ]; then
  npm --prefix "$PKG" install --no-audit --no-fund
else
  echo "  (node_modules vorhanden — übersprungen)"
fi

echo "▸ 2/4  Paket bauen (Bundle, Typen, CSS, Schriften)"
npm --prefix "$PKG" run build

echo "▸ 3/4  Konverter + Validierung"
node .ds-sync/package-build.mjs \
  --config .design-sync/config.json \
  --node-modules "$PKG/node_modules" \
  --entry "./$PKG/dist/index.mjs" \
  --out "./$OUT"
node .ds-sync/package-validate.mjs "./$OUT"

echo "▸ 4/4  Upload-Paket packen"
rm -f "$ROOT/$ZIP"
cd "$ROOT/$OUT"
# Genau die Dateien, die das Design-System-Projekt erwartet — ohne lokale
# Artefakte (_screenshots/, .review.html, .render-check.json und andere
# Punkt-Dateien bleiben absichtlich draußen).
ENTRIES=()
for entry in components tokens fonts _vendor _preview guidelines \
             _ds_bundle.js _ds_bundle.css styles.css README.md \
             _ds_sync.json _ds_needs_recompile; do
  if [ -e "$entry" ]; then
    # leere Ordner überspringen (z. B. tokens/, wenn Tokens im Komponenten-CSS liegen)
    if [ -d "$entry" ] && [ -z "$(ls -A "$entry")" ]; then continue; fi
    ENTRIES+=("$entry")
  fi
done
zip -r -q "$ROOT/$ZIP" "${ENTRIES[@]}"
cd "$ROOT"

echo
echo "✓ fertig"
echo "  Ordner: $OUT/"
echo "  ZIP:    $ZIP  ($(du -h "$ZIP" | cut -f1))"

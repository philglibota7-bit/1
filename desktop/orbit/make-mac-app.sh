#!/usr/bin/env bash
# Setzt aus dem Neutralino-Build ein fertiges macOS-Programm zusammen: ORBIT.app
# Ein .app-Bundle ist nur ein Ordner mit fester Struktur — das geht auch auf Linux.
set -euo pipefail
cd "$(dirname "$0")"

APP_NAME="ORBIT"
BUNDLE="dist/${APP_NAME}.app"
BIN="dist/orbit/orbit-mac_universal"      # laeuft auf Apple Silicon und Intel
RES="dist/orbit/resources.neu"
VERSION="$(python3 -c "import json;print(json.load(open('neutralino.config.json'))['version'])")"

[ -f "$BIN" ] || { echo "Fehlt: $BIN — bitte zuerst 'neu build --release' ausfuehren."; exit 1; }
[ -f "$RES" ] || { echo "Fehlt: $RES — bitte zuerst 'neu build --release' ausfuehren."; exit 1; }

rm -rf "$BUNDLE"
mkdir -p "$BUNDLE/Contents/MacOS" "$BUNDLE/Contents/Resources"

cp "$BIN" "$BUNDLE/Contents/MacOS/${APP_NAME}"
chmod +x "$BUNDLE/Contents/MacOS/${APP_NAME}"
# Neutralino sucht resources.neu neben dem Programm. In Contents/MacOS darf fuer eine
# gueltige Signatur aber nur Programmcode liegen — die Daten liegen deshalb unter
# Resources, neben dem Programm steht nur ein Verweis darauf.
cp "$RES" "$BUNDLE/Contents/Resources/resources.neu"
ln -s ../Resources/resources.neu "$BUNDLE/Contents/MacOS/resources.neu"
[ -f build/icon.icns ] && cp build/icon.icns "$BUNDLE/Contents/Resources/icon.icns"

cat > "$BUNDLE/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleName</key><string>${APP_NAME}</string>
  <key>CFBundleDisplayName</key><string>${APP_NAME}</string>
  <key>CFBundleExecutable</key><string>${APP_NAME}</string>
  <key>CFBundleIdentifier</key><string>app.orbit.leitstand</string>
  <key>CFBundleVersion</key><string>${VERSION}</string>
  <key>CFBundleShortVersionString</key><string>${VERSION}</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>CFBundleIconFile</key><string>icon</string>
  <key>CFBundleInfoDictionaryVersion</key><string>6.0</string>
  <key>LSMinimumSystemVersion</key><string>10.15</string>
  <key>NSHighResolutionCapable</key><true/>
  <key>NSSupportsAutomaticGraphicsSwitching</key><true/>
</dict>
</plist>
PLIST

# Download-Markierung entfernen, falls vorhanden
xattr -cr "$BUNDLE" 2>/dev/null || true

# Ad-hoc signieren: ohne Apple-Konto, aber das ganze Paket versiegelt (Programm,
# Info.plist, Daten). Ohne diese Siegel meldet macOS auf Apple Silicon gern
# „beschädigt" statt nur „nicht überprüft". Auf dem Mac mit codesign, sonst mit
# rcodesign (cargo install apple-codesign), falls vorhanden.
RCODESIGN="${RCODESIGN:-$(command -v rcodesign || true)}"
if command -v codesign >/dev/null 2>&1; then
  codesign --force --deep --sign - --identifier app.orbit.leitstand "$BUNDLE"
  echo "Signiert (ad-hoc, codesign)"
elif [ -n "$RCODESIGN" ]; then
  "$RCODESIGN" sign "$BUNDLE" >/dev/null 2>&1
  echo "Signiert (ad-hoc, rcodesign)"
else
  echo "Nicht signiert: weder codesign noch rcodesign gefunden"
fi

( cd dist && rm -f "${APP_NAME}-mac.zip" && zip -qry "${APP_NAME}-mac.zip" "${APP_NAME}.app" )
echo "Fertig: $BUNDLE"
echo "ZIP:    dist/${APP_NAME}-mac.zip"

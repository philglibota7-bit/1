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
cp "$RES" "$BUNDLE/Contents/MacOS/resources.neu"
chmod +x "$BUNDLE/Contents/MacOS/${APP_NAME}"
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

( cd dist && rm -f "${APP_NAME}-mac.zip" && zip -qry "${APP_NAME}-mac.zip" "${APP_NAME}.app" )
echo "Fertig: $BUNDLE"
echo "ZIP:    dist/${APP_NAME}-mac.zip"

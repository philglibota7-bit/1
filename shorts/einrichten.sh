#!/usr/bin/env bash
# Richtet die Shorts-Kette auf einem Mac ein.
#
#   bash shorts/einrichten.sh
#
# Sucht heruntergeladene ffmpeg- und Whisper-Dateien, macht sie lauffaehig,
# richtet eine Python-Umgebung ein und prueft am Ende alles durch.
# Aendert nichts am System und braucht kein sudo.

set -u
HIER="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN="$HIER/bin"
mkdir -p "$BIN"

blau()  { printf '\033[1;34m%s\033[0m\n' "$1"; }
gut()   { printf '  \033[32m✓\033[0m %s\n' "$1"; }
warn()  { printf '  \033[33m!\033[0m %s\n' "$1"; }
fehl()  { printf '  \033[31m✗\033[0m %s\n' "$1"; }

blau "1. Suche nach heruntergeladenen Dateien"

SUCHORTE=("$HOME/Downloads" "$HOME/Desktop" "$HOME/Documents" "$HIER")
gefunden=0

entpacken() {
  # $1 = Archiv, $2 = Zielordner
  case "$1" in
    *.zip)          unzip -oq "$1" -d "$2" 2>/dev/null ;;
    *.tar.xz|*.txz) tar -xf "$1" -C "$2" 2>/dev/null ;;
    *.tar.gz|*.tgz) tar -xzf "$1" -C "$2" 2>/dev/null ;;
    *.7z)           command -v 7z >/dev/null && 7z x -y -o"$2" "$1" >/dev/null 2>&1 ;;
    *)              return 1 ;;
  esac
}

einsetzen() {
  # $1 = gefundene Programmdatei, $2 = Zielname (ffmpeg / ffprobe)
  cp "$1" "$BIN/$2" 2>/dev/null || return 1
  chmod +x "$BIN/$2"
  # Ohne das blockiert macOS jede heruntergeladene Datei beim Start.
  # Das ist der Grund, warum "ffmpeg kann nicht geoeffnet werden" erscheint.
  xattr -d com.apple.quarantine "$BIN/$2" 2>/dev/null || true
  if "$BIN/$2" -version >/dev/null 2>&1; then
    gut "$2 eingerichtet: $BIN/$2"
    return 0
  fi
  fehl "$2 laesst sich nicht starten (evtl. falsche Architektur: Intel statt Apple Silicon?)"
  rm -f "$BIN/$2"
  return 1
}

for name in ffmpeg ffprobe; do
  command -v "$name" >/dev/null 2>&1 && { gut "$name ist bereits im System vorhanden"; gefunden=1; continue; }
  [ -x "$BIN/$name" ] && { gut "$name liegt schon in bin/"; gefunden=1; continue; }

  treffer=""
  for ort in "${SUCHORTE[@]}"; do
    [ -d "$ort" ] || continue
    # entpackte Programmdatei
    t=$(find "$ort" -maxdepth 3 -type f -name "$name" -perm -u+r 2>/dev/null | head -1)
    [ -n "$t" ] && { treffer="$t"; break; }
    # noch gepacktes Archiv
    a=$(find "$ort" -maxdepth 2 -type f \( -iname "$name*.zip" -o -iname "$name*.tar.*" -o -iname "$name*.7z" \) 2>/dev/null | head -1)
    if [ -n "$a" ]; then
      tmp=$(mktemp -d)
      if entpacken "$a" "$tmp"; then
        t=$(find "$tmp" -type f -name "$name" 2>/dev/null | head -1)
        [ -n "$t" ] && { treffer="$t"; break; }
      fi
    fi
  done

  if [ -n "$treffer" ]; then
    einsetzen "$treffer" "$name" && gefunden=1
  else
    warn "$name nicht gefunden"
  fi
done

if [ ! -x "$BIN/ffprobe" ] && ! command -v ffprobe >/dev/null 2>&1; then
  warn "ffprobe fehlt. Achtung: Auf evermeet.cx wird ffprobe SEPARAT"
  warn "heruntergeladen – die ffmpeg-Datei allein reicht nicht."
  warn "Einfacher: brew install ffmpeg  (bringt beides mit)"
fi

blau "2. Python-Umgebung"
PY=$(command -v python3 || true)
if [ -z "$PY" ]; then
  fehl "python3 fehlt. Installieren mit: brew install python"
else
  gut "python3: $($PY --version 2>&1)"
  if [ ! -d "$HIER/.venv" ]; then
    "$PY" -m venv "$HIER/.venv" && gut "Umgebung angelegt: shorts/.venv"
  else
    gut "Umgebung vorhanden"
  fi
  # shellcheck disable=SC1091
  source "$HIER/.venv/bin/activate"
  if python -c "import faster_whisper" 2>/dev/null; then
    gut "faster-whisper ist installiert"
  else
    printf '  … faster-whisper wird installiert (einige hundert MB)\n'
    pip install --quiet --upgrade pip
    if pip install --quiet faster-whisper; then
      gut "faster-whisper installiert"
    else
      fehl "Installation fehlgeschlagen. Von Hand: pip install faster-whisper"
    fi
  fi
fi

blau "3. Schrift fuer die Untertitel"
SCHRIFT=$(python3 -c "import json,sys;print(json.load(open('$HIER/konfig.json'))['untertitel']['schrift'])" 2>/dev/null)
if [ -n "$SCHRIFT" ]; then
  if ls "/System/Library/Fonts" "/Library/Fonts" "$HOME/Library/Fonts" 2>/dev/null \
     | grep -qi "${SCHRIFT%% *}"; then
    gut "$SCHRIFT ist vorhanden"
  else
    warn "$SCHRIFT nicht sicher gefunden. Wenn die Untertitel anders aussehen"
    warn "als erwartet, trag in shorts/konfig.json eine andere Schrift ein"
    warn "(auf jedem Mac vorhanden: Helvetica, Arial, Impact)."
  fi
fi

blau "4. Abschlusspruefung"
if [ -d "$HIER/.venv" ]; then
  "$HIER/.venv/bin/python" "$HIER/shorts.py" pruefen
else
  python3 "$HIER/shorts.py" pruefen
fi

printf '\nSo geht es weiter:\n'
printf '  1. Video nach shorts/eingang/ legen\n'
printf '  2. source shorts/.venv/bin/activate\n'
printf '  3. python3 shorts/shorts.py machen shorts/eingang/deinvideo.mp4\n\n'

# PULSE als Mac-Programm

`PULSE.app` ist ein echtes macOS-Programm: doppelklicken, fertig. Kein Browser,
kein Terminal, keine Installation von Node oder sonstigem.

## Herunterladen und starten

1. **[download/PULSE-mac.zip](../download/PULSE-mac.zip)** herunterladen und entpacken
2. `PULSE.app` in den Ordner **Programme** ziehen
3. Beim **allerersten Start**: Rechtsklick auf `PULSE.app` → **Öffnen** → im Dialog
   nochmal **Öffnen** klicken

Der dritte Schritt ist einmalig nötig, weil die App nicht bei Apple registriert ist
(das kostet 99 $ im Jahr). Danach startet sie ganz normal per Doppelklick.

Falls macOS trotzdem blockt, hilft ein Befehl im Terminal:

```bash
xattr -cr /Applications/PULSE.app
```

Das entfernt nur die Download-Markierung, sonst nichts.

## Technisch

- **Universal Binary** — läuft auf Apple Silicon (M1–M4) *und* Intel-Macs
- **6 MB** groß, weil die App die in macOS eingebaute Web-Ansicht nutzt
  statt einen kompletten Browser mitzuliefern
- Braucht Internet für Live-Daten (Fußball, Wetter, Kurse, Nachrichten)
- Einstellungen und Favoriten bleiben lokal auf dem Mac

## Selbst neu bauen

Wenn `info-hub.html` geändert wurde, erzeugt ein Befehl die App neu:

```bash
npm i -g @neutralinojs/neu    # einmalig
./desktop/build-app.sh
```

Gebraucht werden außerdem `python3` und `zip` — auf macOS beides ab Werk dabei.

Ergebnis liegt danach in `desktop/dist/PULSE.app` und als ZIP daneben.

Dateien:

| Datei | Zweck |
|---|---|
| `neutralino.config.json` | Fenstergröße, Titel, Berechtigungen |
| `build-app.sh` | Alles-in-einem: Dateien sammeln, bauen, App erzeugen |
| `make-mac-app.sh` | Setzt das `.app`-Bundle aus Programm, Daten und Icon zusammen |
| `build/icon.icns` | App-Icon für Dock und Finder |

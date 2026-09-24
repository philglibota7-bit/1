# PULSE als Mac-Programm

`PULSE.app` ist ein echtes macOS-Programm. Kein Browser, keine Installation von
Node oder sonstigem. Einmal freigeben, danach startet sie per Doppelklick.

## Herunterladen und starten

1. **[download/PULSE-mac.zip](../download/PULSE-mac.zip)** herunterladen und entpacken
2. `PULSE.app` in den Ordner **Programme** ziehen
3. Einmalig freigeben — siehe unten

### Warum der dritte Schritt nötig ist

Die App ist nicht bei Apple notariell beglaubigt; das setzt ein kostenpflichtiges
Entwicklerkonto voraus. macOS zeigt deshalb beim ersten Start:

> „PULSE" nicht geöffnet — Apple konnte nicht überprüfen, ob „PULSE" frei von
> Schadsoftware ist.

Dieser Dialog bietet **nur „In den Papierkorb legen" und „Fertig"** an. Seit
macOS 15 (Sequoia) gibt es den früheren Weg über Rechtsklick → Öffnen nicht
mehr. **„Fertig" drücken**, dann einen der beiden Wege gehen:

**Über das Terminal (ein Befehl):**

```bash
xattr -cr /Applications/PULSE.app
```

Danach startet die App per Doppelklick. Der Befehl entfernt nur die
Download-Markierung, sonst nichts.

**Oder über die Oberfläche:**

Systemeinstellungen → **Datenschutz & Sicherheit** → ganz nach unten scrollen.
Dort steht nach dem Startversuch „PULSE wurde blockiert…" mit dem Knopf
**„Trotzdem öffnen"**. Mit TouchID bestätigen; der folgende Dialog hat dann
einen **„Öffnen"**-Knopf.

Bei älteren macOS-Versionen (14 und davor) genügt Rechtsklick auf `PULSE.app`
→ **Öffnen** → im Dialog nochmal **Öffnen**.

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

Ergebnis liegt danach in `desktop/dist/PULSE.app` und als ZIP daneben.

Dateien:

| Datei | Zweck |
|---|---|
| `neutralino.config.json` | Fenstergröße, Titel, Berechtigungen |
| `build-app.sh` | Alles-in-einem: Dateien sammeln, bauen, App erzeugen |
| `make-mac-app.sh` | Setzt das `.app`-Bundle aus Programm, Daten und Icon zusammen |
| `build/icon.icns` | App-Icon für Dock und Finder |

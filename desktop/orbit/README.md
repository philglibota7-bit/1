# ORBIT als Mac-Programm

`ORBIT.app` zeigt deine echten Arbeitsabläufe als Astronauten um eine Raumstation.
Doppelklicken, fertig. Kein Terminal, kein Node, keine Installation.

## Drei Wege, ORBIT zu benutzen

| Weg | Was funktioniert | Wofür |
|---|---|---|
| **ORBIT.app** (diese Seite) | alles — Sessions, Ordner, Prozesse, GitHub, eigene Agenten | am Schreibtisch |
| **Auf dem Handy installieren** | eigene Claude-Agenten und GitHub | unterwegs nachsehen und beauftragen |
| **Im Browser öffnen** | dasselbe wie auf dem Handy | schnell mal reinschauen |

Fürs Handy: [orbit.html](../../orbit.html) auf dem iPhone in Safari öffnen →
Teilen-Symbol → „Zum Home-Bildschirm". Auf Android und im Desktop-Chrome bietet
ORBIT die Installation von selbst an. Danach ist es eine eigene App mit eigenem
Icon, ohne Browserleiste, und startet auch ohne Internet.

## Warum überhaupt ein Programm?

Im Browser geht das nicht. Eine Webseite darf grundsätzlich nicht sehen, welche
Programme auf deinem Rechner laufen oder welche Dateien du gerade bearbeitest —
das ist die Sicherheitsgrenze des Browsers und lässt sich nicht umgehen.

`orbit.html` auf GitHub Pages kann deshalb nur zwei Dinge: deine selbst angelegten
Claude-Agenten und GitHub (das geht übers Netz). Alles andere — Claude-Code-Sessions,
VS Code, laufende Befehle — braucht dieses Programm.

## Herunterladen und starten

1. **[download/ORBIT-mac.zip](../../download/ORBIT-mac.zip)** herunterladen und entpacken
2. `ORBIT.app` in den Ordner **Programme** ziehen
3. Beim **allerersten Start**: Rechtsklick auf `ORBIT.app` → **Öffnen** → im Dialog
   nochmal **Öffnen** klicken

Schritt 3 ist einmalig nötig, weil die App nicht bei Apple registriert ist
(das kostet 99 $ im Jahr). Danach startet sie per Doppelklick.

Falls macOS trotzdem blockt:

```bash
xattr -cr /Applications/ORBIT.app
```

Das entfernt nur die Download-Markierung, sonst nichts.

## Was du siehst

Jeder Astronaut ist eine echte Sache, die gerade läuft. Antippen zeigt Ort und Tätigkeit.

| Zeichen | Astronaut | Woher die Daten kommen | Was im Detail steht |
|---|---|---|---|
| ⌘ | **Claude-Code-Session** | `~/.claude/projects/*/*.jsonl` | Ordner, Branch, aktuelles Werkzeug, Datei oder Befehl, Modell, Aufwand, letzte 8 Schritte mit Uhrzeit |
| ▣ | **Projektordner / VS Code** | `git` im Ordner, Datei-Zeitstempel, Prozessliste | Pfad, Branch, zuletzt gespeicherte Dateien, Anzahl geänderter Dateien, letzter Commit, ob VS Code läuft |
| ▶ | **Laufender Befehl** | `ps` | PID, Laufzeit, CPU-Auslastung, vollständiger Befehl |
| ⑂ | **GitHub-Repo** | GitHub-API (Token nötig) | Offene Pull Requests und letzte Actions-Läufe, jeweils anklickbar |
| ◆ | **Eigener Claude-Agent** | dein Anthropic-Schlüssel | Rolle, Modell, Missionen, verbrauchte Tokens |

Einrichten über den Brücken-Knopf oben rechts: dort Projektordner hinzufügen,
GitHub-Token hinterlegen und einzelne Astronauten-Arten ab- oder anschalten.

## Die eine ehrliche Einschränkung

**VS Code meldet nicht selbst, welche Datei gerade offen ist.** Dafür gibt es keine
Schnittstelle. ORBIT leitet das aus Datei-Zeitstempeln ab: „Datei X wurde vor
4 Sekunden gespeichert". Das trifft in der Praxis fast immer zu — aber wenn du
nur liest oder ungespeichert tippst, sieht der Astronaut nichts. Für hundertprozentige
Genauigkeit bräuchte es eine eigene VS-Code-Erweiterung.

## Was die App darf

Absichtlich wenig. Die Berechtigungen stehen in `neutralino.config.json`:

| Recht | Wofür |
|---|---|
| `filesystem.readDirectory`, `readFile`, `getStats` | Session-Protokolle lesen — **nur lesen, nie schreiben** |
| `os.execCommand` | `git`, `ps` und `ls` in deinen Projektordnern |
| `os.getPath` | dein Heimverzeichnis finden |
| `os.open`, `os.showFolderDialog` | Links im Browser öffnen, Ordner auswählen |

Keine Schreibrechte, kein Löschen, kein Netzwerkzugriff außer zu `api.anthropic.com`
und `api.github.com`. Nichts verlässt den Rechner, außer was du selbst an Claude
oder GitHub schickst.

## Technisch

- **Universal Binary** — Apple Silicon (M1–M4) *und* Intel
- **7 MB**, weil die App die in macOS eingebaute Web-Ansicht nutzt statt einen
  ganzen Browser mitzuliefern
- Einstellungen, Agenten und Schlüssel bleiben lokal (`localStorage`)

## Selbst neu bauen

Wenn `orbit.html` geändert wurde:

```bash
npm i -g @neutralinojs/neu    # einmalig
./desktop/orbit/build-app.sh
```

Ergebnis: `desktop/orbit/dist/ORBIT.app` und `ORBIT-mac.zip` daneben.

| Datei | Zweck |
|---|---|
| `neutralino.config.json` | Fenstergröße, Titel, Berechtigungen |
| `build-app.sh` | Alles-in-einem: Datei kopieren, Start einbauen, bauen |
| `make-mac-app.sh` | Setzt das `.app`-Bundle zusammen |
| `build/icon.icns` | App-Icon in acht Auflösungen |

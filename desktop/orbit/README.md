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

**Am einfachsten, ganz ohne Meldung von macOS:** das Terminal öffnen
(Programme → Dienstprogramme → Terminal), diese eine Zeile hineinkopieren und
Enter drücken:

```bash
rm -rf /Applications/ORBIT.app && curl -fL https://github.com/philglibota7-bit/1/raw/claude/festive-bardeen-wkf62y/download/ORBIT-mac.zip -o /tmp/ORBIT-mac.zip && ditto -xk /tmp/ORBIT-mac.zip /Applications && open /Applications/ORBIT.app
```

Sie lädt das Programm, legt es in den Ordner Programme (ein älteres ORBIT dort
wird ersetzt) und startet es. Was `curl` lädt, bekommt von macOS keine
Download-Markierung, anders als im Browser. Deshalb prüft Gatekeeper das
Programm gar nicht erst, und der Dialog mit dem Papierkorb kommt nicht.
Danach startet ORBIT ganz normal per Doppelklick.

**Oder über den Browser:**

1. **[download/ORBIT-mac.zip](../../download/ORBIT-mac.zip)** herunterladen und entpacken
2. `ORBIT.app` in den Ordner **Programme** ziehen
3. Beim **allerersten Start**:
   - `ORBIT.app` doppelklicken. macOS meldet „ORBIT“ wurde nicht geöffnet.
     Auf **Fertig** klicken, **nicht** auf „In den Papierkorb legen“.
   - **Systemeinstellungen → Datenschutz & Sicherheit** öffnen und ganz nach unten
     scrollen. Dort steht „ORBIT“ wurde blockiert … mit dem Knopf **Dennoch öffnen**.
     Klicken, mit Passwort oder Touch ID bestätigen, im nächsten Dialog nochmal
     **Dennoch öffnen**.

Danach startet ORBIT ganz normal per Doppelklick. Der Knopf in den Einstellungen
erscheint nur etwa eine Stunde lang nach dem ersten Versuch — sonst einfach nochmal
doppelklicken.

Nötig ist das, weil die App nicht bei Apple registriert ist (das kostet 99 $ im Jahr).
Den früheren Weg „Rechtsklick → Öffnen“ gibt es seit macOS 15 nicht mehr.

**Schneller, mit einem Befehl im Terminal** (Programme → Dienstprogramme → Terminal):

```bash
xattr -cr /Applications/ORBIT.app
```

Das entfernt nur die Download-Markierung, sonst nichts. Danach startet ORBIT per
Doppelklick ohne jede Meldung. Das hilft auch, wenn macOS „beschädigt“ sagt.

Das Paket ist ad-hoc signiert: ohne Apple-Konto, aber Programm, `Info.plist` und
Daten sind versiegelt. Eine veränderte Datei fällt damit auf.

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

Gebraucht werden außerdem `python3` und `zip` — auf macOS beides ab Werk dabei.

Ergebnis: `desktop/orbit/dist/ORBIT.app` und `ORBIT-mac.zip` daneben.

| Datei | Zweck |
|---|---|
| `neutralino.config.json` | Fenstergröße, Titel, Berechtigungen |
| `build-app.sh` | Alles-in-einem: Datei kopieren, Start einbauen, bauen |
| `make-mac-app.sh` | Setzt das `.app`-Bundle zusammen |
| `build/icon.icns` | App-Icon in acht Auflösungen |

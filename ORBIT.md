# ORBIT · Agenten-Leitstand

ORBIT zeigt Agenten und laufende Arbeit als Astronauten an Halteleinen um eine Raumstation. Antippen zeigt, wo einer ist und was er dort tut.

Alles steckt in einer Datei ohne Abhängigkeiten: `orbit.html`, ein Canvas, alles prozedural gezeichnet.

## Drei Wege, es zu benutzen

| Weg | Was funktioniert | Wofür |
|---|---|---|
| **ORBIT.app** (macOS) | alles | am Schreibtisch |
| **Auf dem Handy installiert** | eigene Claude-Agenten, GitHub | unterwegs |
| **Im Browser** | dasselbe wie Handy | schnell reinschauen |

### Die Vorführung

Im Browser und auf dem Handy darf keine Seite Dateien oder Prozesse lesen — die halbe App blieb dort leer, und man sah nie, wofür sie da ist. Die leere Crew-Liste bietet deshalb eine Vorführung an: zweieinhalb Minuten mit Beispieldaten, dann von vorn. Eine Sitzung liest sich ein, schickt zwei Unteragenten los, wartet auf eine Freigabe, macht weiter und ist fertig; die Unteragenten berichten, ein dritter prüft nach; die Tests eines Pull Requests laufen und werden grün; ein Entwicklungsserver läuft, und im Projektordner sammeln sich die Änderungen.

Sie liefert dieselben Felder wie die echte Brücke, deshalb laufen Szene, Liste, Detail, Takt, Winken und Fenstertitel genau wie mit echter Arbeit. Und sie sagt, was sie ist: oben steht „Vorführung", auf dem Handy als Band unter dem Kopf, und im Detail jeder Figur „Beispieldaten der Vorführung — nichts davon ist echt". Nichts darin führt irgendwohin: die Beispiel-PRs und -Läufe sind keine Links, und der Knopf „Öffnen" fehlt, statt auf ein erfundenes Repo zu zeigen. Nach dem Beenden fragt die echte Brücke sofort wieder, auch GitHub.

## Die Astronauten

| | Astronaut | Quelle | Was im Detail steht |
|---|---|---|---|
| ⌘ | Claude-Code-Session | `~/.claude/projects/*/*.jsonl`, `~/.claude/tasks/<sitzung>/` | Ordner, Branch, Auftrag, aktuelles Werkzeug, Zustand samt Dauer, Modell, Aufwand, zuletzt Gesagtes, Aufgabenliste mit Fortschritt, Anzuguhr, belegter Kontext, Unteragenten, Takt der letzten Stunde, letzte 8 Schritte als Zeitstrahl, geänderte Dateien |
| ↳ | Unteragent | `<sitzung>/subagents/agent-*.jsonl`, auch `subagents/workflows/<lauf>/` | Aufgabe, von welcher Sitzung geschickt, Agententyp und Phase, Bericht oder Abbruch, eigener Zeitstrahl |
| ▣ | Projektordner / VS Code | `git`, Datei-Zeitstempel, Prozessliste | Pfad, Branch, zuletzt gespeicherte Dateien, geänderte Dateien, letzter Commit, ob VS Code läuft |
| ▶ | Laufender Befehl | `ps` | PID, Auslastung, Anzuguhr, vollständiger Befehl |
| ⑂ | GitHub-Repo | GitHub-API | offene Pull Requests als Karten mit dem Stand ihrer Prüfungen, Läufe als Zeitstrahl mit Dauer, anklickbar |
| ◆ | Eigener Claude-Agent | Anthropic-API | Rolle, Modell, Missionen, Tokens |

Unter **Crew** stehen die selbst angelegten Agenten und darunter alles, was wirklich läuft — je Zeile Name, aktuelle Tätigkeit, Branch und die Dauer; Unteragenten eingerückt unter ihrer Sitzung, Berichte grün, Abbrüche rot. Antippen fährt zur Figur.

Vor der Dauer steht bei Sitzungen und Unteragenten ein kleiner Takt: die letzten zwanzig Minuten, eine Säule je Minute. Er beantwortet in der Liste nur eine Frage — wer arbeitet gerade wirklich, und wer steht schon eine Weile? Der Maßstab hat einen Boden, damit ein einzelner Aufruf eine kleine Säule ist und keine volle. Minuten, für die das gelesene Protokoll nicht reicht, stehen gepunktet da: „nichts getan" zeigt der Takt nur für eine Minute, die er ganz kennt. Minuten vor dem Start bleiben leer — ein Unteragent, der seit einer halben Minute läuft, hatte vorher keine neunzehn stillen Minuten.

Die Chips der Leiste unten tragen denselben Plan als feinen Strich an der Unterkante — wie weit jede Sitzung ist, sieht man, ohne eine einzige zu öffnen.

Die Liste wird bei jedem Durchlauf der Brücke neu gebaut, in der Vorführung jede Sekunde. Ersetzt wird jetzt nur, was sich geändert hat, Karte für Karte; nie, während ein Finger auf der Liste liegt; und der Tastaturfokus bleibt an seiner Karte. Vorher ging ein Tipp verloren, wenn zwischen Drücken und Loslassen neu gebaut wurde.

### Heute: der Tag in Sitzungen

Die Szene zeigt, was gerade läuft; was heute schon vorbei ist, stand nirgends. In der Brücke steht deshalb ein Tagesbogen: je Projekt, wann heute Sitzungen offen waren — von der ersten bis zur letzten Zeile ihrer Datei —, die laufenden hell umrandet, oben die Zahl der Sitzungen und wie lange insgesamt etwas offen war, ohne dass zwei gleichzeitige doppelt zählen. Darunter steht, dass das „offen" heißt und nicht „gearbeitet". Gebaut wird er aus dem, was die Brücke ohnehin weiß; nur der Projektname einer schon beendeten Sitzung wird einmal aus ihren ersten Zeilen gelesen und gemerkt. Die Vorführung bringt einen Beispieltag mit.

Eine Sitzung, die vor Mitternacht angelegt wurde, über Nacht offen oder mit `--resume` fortgesetzt, begann im Bogen um null Uhr. Eine Sitzung von Montag, heute um 14 Uhr fortgesetzt, stand dann mit „14 Std. 59 Min. offen“ da, obwohl sie 59 Minuten lief. Das Protokoll wird nur angehängt, die Zeitstempel steigen also mit der Stelle in der Datei. Eine Halbierungssuche findet deshalb die erste Zeile ab Mitternacht mit wenigen Lesezugriffen: 10 bei einer Datei von einem Megabyte mit einer Riesenzeile darin. Gelesen wird je ganze Zeile nur ihr oberster Zeitstempel, damit fremde Zeitstempel im Ergebnis eines Werkzeugs nicht zählen. Das Ergebnis wird je Datei und Tag gemerkt.

Jede Zeile nimmt einen Tipp an und wählt die Sitzung, die der Stelle am nächsten liegt — die Balken sind sieben Punkte hoch, zu klein für einen Finger. Darunter steht, von wann bis wann und wie lange, und bei einer beendeten, womit sie begann: die erste Eingabe eines Menschen, nach denselben Regeln wie beim Auftrag (keine Meta-Einträge, keine Befehle in spitzen Klammern, keine Bilder). Sie steht in denselben ersten Zeilen wie der Ordner und kostet keinen weiteren Lesezugriff. Bei einer laufenden stehen der Auftrag und „Zur Figur". Mit der Tastatur wählt Eingabe, links und rechts blättern, und der Fokus bleibt, wenn die Brücke den Bogen neu baut.

Darunter gibt „Tag kopieren“ den ganzen Tag als Text her, für die Notiz am Abend, das Standup am nächsten Morgen oder die Stundenliste. „Als Datei sichern“ legt ihn als Markdown ab. Es sind dieselben Zahlen wie im Bogen, und auch dort steht, dass „offen“ nicht „gearbeitet“ heißt. Je Projekt stehen die Sitzungen der Zeit nach mit Zeitspanne, Dauer und womit sie begannen, bei einer laufenden ihr Auftrag. In der Vorführung steht obenan, dass nichts davon echt ist. Kann der Betrachter keine Dateien hergeben, fällt der Dateiknopf weg wie beim Log.

### Die Woche

Unter dem Tagesbogen steht die Woche: je Tag eine Säule mit der offenen Zeit, nach Projekt gestapelt, in denselben Farben wie im Bogen, heute ganz rechts. Antippen zeigt den Tag: je Projekt die Zeit und darunter seine Sitzungen, von wann bis wann und womit sie begannen. So beantwortet sich auch „Was war eigentlich am Dienstag?“. „Woche kopieren“ gibt sie als Text her, je Tag die Projekte und am Ende die Summen, etwa für die Stundenliste oder den Rückblick am Freitag. „Als Datei sichern“ legt sie als Markdown ab.

Eine Sitzungsdatei kennt nur ihren Beginn und ihre letzte Änderung. Läuft eine Sitzung über Tage, wird deshalb an jeder Mitternacht dazwischen gesucht, mit derselben Halbierungssuche wie beim Tagesbeginn: die letzte Zeile davor und die erste danach. Ein Tag ohne Zeile ist ein Tag ohne Sitzung. Ohne das stünde eine am Montag begonnene und am Donnerstag fortgesetzte Sitzung an jedem Tag dazwischen mit 24 Stunden da. Je Durchlauf werden höchstens zwölf Dateiköpfe und drei Grenzen gelesen; bis alles da ist, steht das unter der Woche. Heute kommt aus dem Bogen, damit beide dieselbe Zahl zeigen. Die Vorführung hat eine Beispielwoche.

### Fortsetzen

Eine Sitzung von vorhin nimmt man in Claude Code mit `claude --resume <Sitzung>` wieder auf, und zwar in dem Ordner, in dem sie lief. Im Mac-Programm steht dieser Befehl fertig im Detail einer Sitzung und im Tagesbogen bei einer beendeten, mit einem Knopf „Kopieren":

```
cd '/Users/phil/Phil'\''s Kasse' && claude --resume 0b7c2e9a-1f4d-4c6b-9a3e-5d8f7e6a1b2c
```

Der Pfad ist für die Shell gequotet, auch mit Leerzeichen und Apostroph. ORBIT führt nichts aus, es legt den Befehl nur in die Zwischenablage. Dafür ist `clipboard.writeText` die einzige neue Berechtigung. Klappt das Kopieren nicht, bleibt der Befehl markiert stehen, und der Knopf sagt „Mit ⌘C kopieren".

Hat ein lebender Prozess die Sitzung laut Sitzungsregister noch offen, steht statt des Befehls „Die Sitzung ist noch offen (Prozess 4711) — dort geht es weiter.". Ein zweites `--resume` daneben öffnete denselben Verlauf ein zweites Mal. Das gilt auch im Tagesbogen, etwa für eine Sitzung, die seit dem Morgen still in einem Terminal steht und deshalb keine Figur mehr ist.

Detail und Tagesbogen werden alle paar Sekunden neu gebaut. Die Zeile bleibt dabei dasselbe Element, Fokus und Markierung kommen zurück. Sonst sprang „Kopiert ✓" sofort wieder auf „Kopieren", und ein von Hand markierter Befehl verlor mitten im Kopieren die Markierung.

### Der Puls der Crew

Ein Leitstand braucht einen Monitor, an dem man ohne hinzusehen erkennt, ob etwas lebt. Oben neben dem Namen läuft eine Linie wie auf einem EKG: jeder Zacken ist ein echter Werkzeugaufruf einer Sitzung oder eines Unteragenten, in dessen Farbe, zu der Zeit, zu der er im Protokoll steht — die letzten anderthalb Minuten. Daneben „8 Aufrufe/min". Ruht alles, ist die Linie flach; arbeiten drei Sitzungen gleichzeitig, sieht man es an den Farben. Sie wird in die Szene gezeichnet und nicht als animiertes Element — eine CSS-Animation in der Kopfzeile hat hier schon einmal die Bildrate von 60 auf 14 gedrückt. Ohne Sitzungen, ohne Platz (Handy, schmale Fenster mit Vorführungsknopf) und im Kinomodus gibt es sie nicht.

Weil sie in die Szene gezeichnet ist, konnte man weder auf sie zeigen noch sie antippen. Darüber liegt jetzt ein unsichtbarer Knopf: Beim Zeigen steht da, was ein Zacken bedeutet, und ein Tipp öffnet die Crew-Liste. Er wird nur angefasst, wenn sich die Lage der Linie ändert, nicht in jedem Bild.

### Der Zeitstrahl der Arbeitsschritte

Jeder Schritt hängt als Punkt an einer durchgehenden Schiene: das Verb in der Farbe seiner Art (lesen blau, schreiben bernstein, Befehl violett, suchen türkis, delegieren rosa, Netz cyan, planen grau), das Ziel in Schreibmaschine darunter, rechts die Uhrzeit. Der oberste Schritt pulst, solange er läuft, und zeigt „seit 4 Sek." statt einer Uhrzeit — bei dem, was gerade passiert, ist die Dauer die Frage, nicht der Zeitpunkt.

Zwischen zwei Schritten steht die Pause, aber erst ab zehn Sekunden. Darunter ist es keine Pause, sondern die Laufzeit des Werkzeugs, und eine Reihe gleicher „3 Sek."-Marken sagt nichts außer dass sie da ist.

### Die Aufgabenliste: wie weit eine Sitzung ist

Claude Code führt für jede Sitzung eine Aufgabenliste, und sie ist ihr eigentlicher Fortschritt. Die Werkzeugaufrufe sagen, *was* eine Sitzung tut; die Liste sagt, *wofür* und wie weit. Im Detail steht „Aufgaben · 3 von 8 erledigt", darüber ein Balken aus so vielen Stücken, wie es Aufgaben gibt (erledigt grün, laufend blau, offen leer), darunter die Liste: bei einer laufenden Aufgabe, was sie gerade *tut* („Stellt die Preisberechnung um"), bei einer wartenden, worauf („nach #5"), die Beschreibung als Hinweis. In der Crew-Liste steht dieselbe Liste als eine Zeile — kleiner Balken, „2/8 · Installiert decimal.js" —, und im Namensschild in der Szene der Stand neben dem Branch.

- Gelesen aus `~/.claude/tasks/<sitzung>/<nummer>.json`, an echten Dateien nachgesehen: `id`, `subject`, `description`, `activeForm`, `status`, `blocks`, `blockedBy`. Ältere Fassungen führen die Liste über das Werkzeug `TodoWrite`; dann gilt dessen jüngster Aufruf im Protokoll.
- Neu gelesen wird nur, wenn das Protokoll der Sitzung gewachsen ist — jede Änderung an der Liste ist ein Werkzeugaufruf und steht dort —, und je Datei nur, wenn sie sich geändert hat. Eine ruhende Sitzung kostet nichts.
- Laufen zwei Aufgaben zugleich, etwa eine delegierte neben der eigenen, steht in der Liste die zuletzt begonnene.

Dabei aufgefallen: jedes Werkzeug ohne eigenen Text stand als rohes JSON da — `TaskUpdate {"taskId":"3","status":"completed"}` in Leiste, Blase und Detail, ebenso jedes Werkzeug eines MCP-Servers. Aufgabenwerkzeuge, Rückfragen, Pläne und das Nachladen von Werkzeugen haben jetzt Sätze („hakt Aufgabe #3 ab", „fragt dich: …"), alle anderen ihren Namen und den ersten kurzen Text ihrer Eingabe.

### Der Takt der letzten Stunde

Über den Arbeitsschritten steht, wie die letzte Stunde verlief: dreißig Säulen zu je zwei Minuten, die Höhe ist die Zahl der Werkzeugaufrufe. Eine Pause sieht man sofort, ebenso ob eine Sitzung im Sekundentakt arbeitet oder alle paar Minuten einmal liest. Gelesen wird vom Ende des Protokolls her; reicht das nicht eine Stunde zurück — bei einer Sitzung, die viel schreibt —, beginnt der Takt später und sagt das darunter, statt die fehlende Zeit als Stille zu zeigen.

### Geänderte Dateien

Darunter steht, welche Dateien die Sitzung geändert hat: der Name vorn, der Ordner klein daneben und von vorn gekürzt, wie oft und wann zuletzt, die jüngste oben. Gezählt wird ein Edit oder Write erst, wenn sein Ergebnis im Protokoll steht und kein Fehler war. Ein abgelehnter Edit steht dort als `"is_error": true` mit „The user doesn't want to proceed with this tool use" (an einem echten Protokoll nachgesehen), und die Datei ist dann unverändert. Ein gescheiterter („String to replace not found") oder noch offener zählt ebenso wenig. Was ein Befehl in der Shell ändert, ist aus dem Protokoll nicht sicher abzulesen; das steht unter der Liste, ebenso ab wann gezählt wird, wenn der gelesene Teil nicht bis zum Anfang reicht.

### Zwei an derselben Datei

Arbeiten zwei Sitzungen im selben Ordner, oder läuft ein Unteragent im Hintergrund neben seiner Sitzung, ändern beide manchmal dieselbe Datei, ohne voneinander zu wissen. Gemerkt wird das meist erst beim Mergen. ORBIT zeigt es, sobald es passiert:

- **In der Szene** sehen die beiden einander an, gleich wie weit sie auseinander sind, und zwischen ihnen zieht sich eine rote Zackenlinie, in der Mitte ein Schild mit dem Namen der Datei („⚠ preis.ts“). Sind es mehrere Dateien, steht die Zahl daneben („+1“). Rot und gezackt, damit sie nicht mit dem Funk zwischen Sitzung und Unteragent verwechselt wird, der blau und gewölbt ist.
- **Unter Stationswerte** steht KONFLIKT mit der jüngsten Datei und den beiden Namen, rot.
- **Im Detailfenster** hat die Datei einen roten Punkt, darunter „⚠ auch pruefung:rundung (vor 11 Sek.)“.
- **Eine Mitteilung** und ein Eintrag im Bordbuch, je Paar und Datei einmal: „Konflikt: preis.ts“ mit beiden Namen und dem vollen Pfad. Antippen öffnet die Figur, die zuletzt geändert hat.
- **In der Leiste unten und in der Crew-Liste** steht bei beiden statt der letzten Tätigkeit „⚠ preis.ts · auch webshop-kasse“, rot. Die sind immer zu sehen, auch wenn die Figuren gerade nicht im Bild sind.
- **In der Befehlspalette** (⌘K) steht je Konflikt „⚠ Konflikt: preis.ts“; Enter öffnet die Figur, die zuletzt geändert hat, und fährt hin. Ebenso „⟲ Im Kreis: …“ je Kreis. Höchstens drei von jeder Sorte.

Als Konflikt gilt: Zwei Figuren haben dieselbe Datei geändert, beide in der letzten halben Stunde, und **jede Änderung fiel in eine Zeit, in der die andere Figur da war**. Das trennt zwei Fälle, die im Protokoll gleich aussehen:
- Eine Übergabe ist keiner: Die Sitzung ändert `preis.ts`, danach schickt sie einen Unteragenten los, der die Datei weiter ändert. Bei der ersten Änderung war er noch nicht da.
- Parallel ist einer: Der Unteragent läuft im Hintergrund, und die Sitzung ändert dieselbe Datei, bevor er berichtet hat.

Ein Unteragent ist da von seinem Start bis zu seinem Bericht. Eine Sitzung ist da, solange ein Prozess sie offen hat: Führt das Sitzungsregister von Claude Code andere Sitzungen, aber diese nicht mehr, ist ihr Terminal zu, und sie war da bis zu ihrer letzten Tätigkeit. Ist das Register leer, lässt sich das nicht unterscheiden (ältere Fassung, oder gerade keine Sitzung offen), dann gilt sie, solange sie in der Liste steht. Verglichen werden die zwölf jüngsten geänderten Dateien jeder Figur, jeweils mit vollem Pfad. Zwei Arbeitskopien desselben Projekts (`git worktree`) sind also verschiedene Dateien, und das stimmt auch. Gezählt werden nur Edit und Write, die gelungen sind, wie bei den geänderten Dateien; was ein Befehl in der Shell ändert, sieht ORBIT nicht.

Gemeldet wird nur, was zwischen zwei Durchläufen der Brücke entstanden ist: Beide Figuren waren schon beim letzten Durchlauf da. Was beim Start oder mit einer neu gelesenen Sitzung schon bestand, steht in Szene und Stationswerten, klingelt aber nicht. Nur „die erste Rechnung meldet nichts“ reichte dafür nicht, denn die erste läuft, bevor die Brücke überhaupt Sitzungen gelesen hat.

In der Vorführung soll der Unteragent „pruefung:rundung“ die Rundung nur prüfen, ändert `preis.ts` bei Sekunde 86 aber gleich selbst, und die Sitzung ändert dieselbe Datei bei Sekunde 95.

### Wer sich im Kreis dreht

Ein Agent, der denselben Befehl immer wieder startet und jedes Mal an demselben Fehler scheitert, kommt nicht weiter und verbraucht dabei Kontext. Das kann eine Viertelstunde gehen, bevor man es merkt. ORBIT zeigt es:

- **In der Szene** dreht sich um seine Figur ein gestrichelter orangefarbener Ring, daran ein Schild mit der Zahl („⟲ 4×“). Orange und nicht bernstein, denn bernstein ist der Ring dessen, der auf dich wartet.
- **Unter Stationswerte** steht SCHLEIFE mit Namen, Befehl und Zahl.
- **Im Detailfenster** steht „Im Kreis · 4-mal derselbe Fehler · seit 14:02 · 251 Tsd. Tokens“, darunter der Befehl und die Zeile, die den Fehler sagt. Die Tokens sind alle Antworten dieser Figur seit dem ersten Fehlschlag der Reihe, gezählt wie in der Energie, aus derselben Liste: frisch, geschrieben, gelesen und erzeugt, jede Antwort einmal, ohne die ihrer Unteragenten. Weiß die Energie nichts von ihr, fehlt die Zahl.
- **Eine Mitteilung** und ein Eintrag im Bordbuch, je Reihe einmal. Wird eine Reihe nur länger, klingelt es nicht noch einmal.
- **In der Leiste unten und in der Crew-Liste** steht statt der letzten Tätigkeit „⟲ 4× derselbe Fehler“, orange. Hat eine Figur beides, steht der Kreis vorn, denn er kostet, solange er läuft. Wer auf dich wartet, behält seine Zeile.

Als Schleife gilt: derselbe Befehl mindestens dreimal hintereinander gescheitert, jedes Mal mit **demselben** Fehler, und der letzte Lauf ist der gescheiterte. Andere Befehle und Änderungen an Dateien dazwischen unterbrechen die Reihe nicht, ein gelungener Lauf desselben Befehls schon. Verglichen wird die ganze Ausgabe, bis auf Farbcodes, Uhrzeiten und Dauern („Time: 2.31 s“). Dreimal ein roter Test ist also noch keine Schleife, wenn sich der Fehler ändert: Aus „5 failed“ über „3 failed“ zu „1 failed“ kommt der Agent voran.

Aus dem Protokoll, an einem echten nachgesehen: Ein gescheiterter Befehl steht als `tool_result` mit `"is_error": true`, und sein Inhalt beginnt mit „Exit code 1“. Nur das zählt als Fehlschlag. Eine Ablehnung durch dich ist auch `is_error`, aber kein Fehlschlag des Befehls; sie unterbricht die Reihe. Der Inhalt kann Text sein oder eine Liste von Textblöcken, beides wird gelesen.

Die Schleife gilt, solange die Figur arbeitet und der letzte Fehlschlag keine Viertelstunde her ist. Hat ein Unteragent berichtet oder ist die Sitzung mit ihrem Zug fertig, ist sie vorbei, wie auch immer sie ausging. Gemeldet wird wie beim Konflikt nur für Figuren, die schon beim letzten Durchlauf da waren.

In der Vorführung lässt der Unteragent „Aufrufe berechnePreis“ den Linter viermal auf `summe.ts` los, und jedes Mal kommt derselbe Fehler in Zeile 41, genau die doppelte Rundung, die er am Ende berichtet.

### Wie voll, wofür, und wer noch mitläuft

- **Kontext.** Jeder Assistenteneintrag im Protokoll führt mit, wie groß der Prompt beim letzten Aufruf war. Frisch gesendet plus neu zwischengespeichert plus aus dem Zwischenspeicher gelesen ist der belegte Kontext — abgerechnet, nicht geschätzt. Daneben steht der Anteil aus dem Zwischenspeicher und, wenn es welche gab, die Denk-Tokens des letzten Aufrufs. Gezählt wird nur der neueste Eintrag: die Frage ist, wie voll die Sitzung gerade ist, nicht was sie insgesamt verbraucht hat.
- **Auftrag und zuletzt Gesagtes.** Der Auftrag kommt aus der Zeile `last-prompt`, sonst aus dem jüngsten Benutzereintrag — eingefügte Bilder, Programmmeldungen und `isMeta`-Einträge zählen nicht. Er steht vor der Tätigkeit: erst wo, dann wofür, dann was. Darunter als Zitat, was die Sitzung zuletzt gesagt hat; bei einer wartenden oft genau die Erklärung, worauf.
- **Unteragenten.** Schickt eine Sitzung einen Agenten los, schreibt der ein eigenes Protokoll unter `<sitzung>/subagents/`, die Agenten eines Arbeitsablaufs eine Ebene tiefer unter `subagents/workflows/<lauf>/`. Jeder wird ein eigener Astronaut mit dem Zeichen ↳. Sein Name kommt aus der `description` in der `.meta.json` daneben, sonst aus den ersten Wörtern seiner Aufgabe ohne Füllwörter („Tests Warenkorb", nicht „Die Tests für"). Höchstens sechs je Sitzung, nur frische. Die Kennung kommt aus `agentId` — die `sessionId` eines Unteragenten ist die seiner Mutter-Sitzung. Er trägt den Namen, unter dem man seine Sitzung in der Szene sieht, auch wenn das Register sie umbenannt hat; das Detail der Sitzung nennt ihre Unteragenten, ein Tipp fährt hin.
- **Fertig, berichtet, abgebrochen.** Sicher fertig ist ein Unteragent, sobald die Sitzung sein Ergebnis hat — sie schreibt es mit seiner `agentId` im `toolUseResult` mit. Sonst gilt er als fertig, wenn sein Protokoll mit dem Bericht endet (Text ohne Werkzeugaufruf danach, oder `StructuredOutput` bei Arbeitsabläufen) und seit einer Viertelminute nichts dazukam. Der Bericht steht grün gerandet im Detail. Ein Eintrag mit `model: "<synthetic>"` und `isApiErrorMessage` ist kein Bericht, sondern ein Abbruch durch Claude Code selbst, etwa ein Nutzungslimit — er steht wörtlich da, rot. Die Anzuguhr eines fertigen oder abgebrochenen Unteragenten bleibt beim letzten Lebenszeichen stehen.
- **Störung des Dienstes.** Lehnt der Dienst eine Anfrage ab, schreibt Claude Code einen Eintrag `api_error` ins Protokoll und wiederholt — an einem echten nachgesehen: `"formatted": "529 Overloaded"`, `retryAttempt`, `maxRetries`. Eine solche Sitzung wartet auf den Dienst und arbeitet nicht, sah aber aus wie mitten in der Arbeit. Steht die Störung nach dem letzten Eintrag des Assistenten und ist sie frisch, heißt die Tätigkeit jetzt „Dienst überlastet — Versuch 2 von 10", im Detail steht der Wortlaut, und die Figur hält die Hand an den Helm, während an der Sprechkappe eine Leuchte bernstein blinkt. Überlastet, Anfragegrenze, gestört und keine Verbindung werden unterschieden.
- **Verdichtet.** Ebenso `compact_boundary`: unter dem Kontext steht „Verdichtet vor 50 Min. · automatisch · 787.738 → 17.212 Tokens" — danach kennt die Sitzung ihren Verlauf nur noch als Zusammenfassung. Die Zeile steht nur eine Weile im gelesenen Ende, also wird sie gemerkt; eine neue Verdichtung kommt einmal ins Bordbuch.
- **Funkstrecke.** Zwischen Sitzung und Unteragent liegt ein dünner gestrichelter Bogen. Die Punkte darauf laufen zum Unteragenten, solange er arbeitet, und zurück zur Sitzung, wenn er berichtet hat. Er liegt in Bildpunkten über der Szene wie die Namen, beginnt am Rand der Figuren, hat einen dunklen Saum und wird hell, wenn eine der beiden gewählt ist.

Alle Feldnamen sind an echten Protokollen geprüft und nicht aus der Doku übernommen.

### Energie: der Verbrauch im Fenster von fünf Stunden

Ganz oben unter Stationswerte steht, was Claude Code gerade verbraucht. Ein Abo rechnet in Fenstern von fünf Stunden: die erste Antwort nach einer Pause öffnet eines, und was darin anfällt, zählt gegen eine Grenze. Wie groß die ist, sagt Anthropic nicht, und ORBIT rät sie nicht. Wann das Fenster aufging und wie viel schon hineinging, steht aber in den eigenen Protokollen.

- **Die Zeilen:**
  - FENSTER, zum Beispiel 12:00–17:00. Der Balken ist die verstrichene Zeit, nicht der Verbrauch.
  - NEUES FENSTER in 2 Std. 26 Min.
  - VERBRAUCH in Tokens.
  - ZWISCHENSPEICHER: welcher Anteil davon aus dem Zwischenspeicher kam, meist über neunzig Prozent.
  - TEMPO der letzten zehn Minuten und HOCHGERECHNET bis zum Ende des Fensters.
  - GRÖSSTER: die Sitzung mit dem größten Anteil, ihre Unteragenten eingeschlossen.
- **Im Detailfenster** jeder Sitzung und jedes Unteragenten steht „Im Fenster: 1,2 Mio. Tokens · 38 % des Fensters“, bei einer Sitzung dazu, wie viel davon auf ihre Unteragenten entfiel.
- **Gezählt wird wie bei ccusage**, damit die Zahlen vergleichbar sind:
  - Alle Protokolle der letzten zehn Stunden, auch die der Unteragenten und der Agenten eines Arbeitsablaufs.
  - Jede Antwort einmal. Claude Code schreibt jeden Block einer Antwort als eigene Zeile und wiederholt darin dieselbe Nutzung; an einem echten Protokoll nachgesehen. Gezählt wird deshalb nach `message.id` und `requestId`.
  - Die Summe ist alles, was abgerechnet wurde: frisch gesendet, neu zwischengespeichert, aus dem Zwischenspeicher gelesen und erzeugt. Fehlermeldungen von Claude Code selbst (`<synthetic>`) zählen nicht.
  - Ein Fenster beginnt zur vollen Stunde (UTC) vor seiner ersten Antwort. Die erste Antwort nach seinem Ende öffnet das nächste.
- **Gelesen wird nur das Neue**, je Datei bis wohin. Beim ersten Mal sucht eine Halbierung die Stelle, an der die zehn Stunden beginnen. Das Protokoll dieser Sitzung hatte beim Testen 480 MB, davon betrafen die zehn Stunden 136 MB. Je Durchlauf werden höchstens 8 MB gelesen, bis dahin steht „LIEST NOCH 40 %“ da.
- **Der Rückblick.** Wer den ganzen Tag arbeitet, reiht Fenster an Fenster; wo das laufende begann, hängt dann an der letzten Pause von fünf Stunden. Bei dieser Sitzung lag sie 18 Stunden zurück, und nur mit zehn Stunden kam der Beginn eine Stunde zu spät heraus (10:00 statt 09:00 UTC). ORBIT sucht deshalb, statt alles zu lesen: rückwärts in Schritten von vier Stunden, bis vor einer Antwort fünf Stunden lang keine war, dann vorwärts Fenster für Fenster. Unteragenten zählen dabei mit. Das läuft nebenher und höchstens 48 Stunden zurück. Findet sich keine Pause, steht „etwa“ vor der Zeit.
- **Anker.** Ist ein Fenster einmal sicher, merkt ORBIT es sich und rechnet von dort weiter; danach wird nicht mehr zurückgesucht.

### Wer auf dich wartet, winkt

Meldet das Sitzungsregister `waiting` — eine Rückfrage oder eine Freigabe —, hebt der Astronaut einen Arm, lehnt sich ein Stück von der Struktur weg, und sein Ring pulst bernsteinfarben. Der Fehler blinkt schnell, das Winken langsam: zwei Dringlichkeiten, zwei Takte. Wie lange schon, steht dabei: „wartet auf deine Freigabe — seit 4 Min.", aus `statusUpdatedAt` im Register.

Oben neben dem Namen der App steht dann ein Knopf „2 warten": ein Tipp fährt zum Nächsten, der an dir hängt, der nächste Tipp zum übernächsten. Dasselbe mit der Taste **W**.

**Und ORBIT meldet sich.** Wartet eine Sitzung auf dich oder ist sie mit ihrem Zug fertig, schlägt ein GitHub-Lauf fehl oder wartet er auf Freigabe, ist einer der eigenen Agenten fertig — dann kommt eine Mitteilung, aber nur, wenn ORBIT gerade nicht vorn ist. Im Mac-Programm als Mitteilung des Systems, im Browser über dessen Mitteilungen, wenn erlaubt. Der Fenstertitel nennt immer, wer gerade wartet: „(1) webshop-kasse wartet · ORBIT". Bei Sitzungen zählt nur das Register, die erste Sichtung meldet nichts, höchstens eine Meldung je Figur, Art und Minute. Im Hintergrund liest die Brücke dafür nur das Register — ein paar hundert Byte je Datei, alle zehn Sekunden; git, ps und die Protokolle bleiben aus. Schalter unter Brücke, im Programm voreingestellt an.

### GitHub: Pull Requests mit ihrem Stand

Jeder offene PR ist eine Karte: links ein Streifen in der Farbe seines Stands, Nummer und Alter, der ganze Titel, der Zweig und je Arbeitsablauf eine Marke — ✓ erfolgreich, ✗ fehlgeschlagen, ● läuft (mit Dauer), ✋ wartet auf Freigabe, ⊘ abgebrochen. Gibt es zu einem Stand keine Prüfungen, steht das da, statt dass die Zeile fehlt. Die Läufe des Repos stehen auf demselben Strahl wie die Schritte einer Sitzung, mit Dauer, Anlass und Versuch; ein Lauf von gestern zeigt „gestern 11:24" und nicht nur eine Uhrzeit.

- Abgefragt über `actions/runs?head_sha=…` je PR, an der echten API geprüft. Ein Zwischenspeicher je Stand hält die Zahl der Abfragen klein: solange etwas läuft, wird jeden Takt nachgesehen; ist alles fertig, gilt das Ergebnis zehn Minuten — nicht für immer, weil ein neu gestarteter Job das Ergebnis ändert, ohne dass ein neuer Stand entsteht.
- **Nicht nur Actions.** Vercel, Netlify, CircleCI und andere melden sich über die Checks-Schnittstelle oder mit einem Commit-Status. Beides wird zum selben Stand mit abgefragt und steht als Marke neben den Actions, mit Dienst und Beschreibung im Tooltip.
  - Die Checks von GitHub Actions selbst fallen weg, denn die Läufe sind schon da.
  - Ein feinkörniger Schlüssel braucht dafür die Leserechte „Checks“ und „Commit statuses“. Fehlen sie, bleibt es still bei den Actions.
  - Ein Vorschau-Deploy, das scheitert, macht den PR rot, wie ein roter Job.
- Die Summe folgt derselben Rangfolge wie der kombinierte Status bei GitHub: ein roter Ablauf macht den PR rot, auch wenn andere noch laufen.
- Ein Lauf, der vor einer geschützten Umgebung auf Freigabe wartet, lässt den Astronauten winken wie eine wartende Sitzung.
- „Läuft" hat eine feste blaue Farbe. Der Akzent wechselt mit dem Himmel, und bei fünf Himmeln ist er orange oder rot — dann sahen ein laufender und ein fehlgeschlagener Lauf gleich aus.
- **Durchsicht.** Neben der Nummer steht, wie weit der PR durchgesehen ist: „✓ freigegeben“ (oder „2 Freigaben“), „✎ Änderungen gewünscht“ oder „◌ Durchsicht angefragt“. Je Prüfer zählt seine letzte entscheidende Bewertung: Ein Kommentar entscheidet nichts, eine verworfene nimmt die vorige zurück. Angefragte Prüfer stehen schon in der PR-Liste und kosten keine Abfrage. Die Bewertungen kosten eine Abfrage je PR und gelten, bis sich der PR ändert, höchstens zehn Minuten. Wünscht jemand Änderungen, sagt das auch die Figur. Wird ein PR freigegeben oder wünscht jemand Änderungen, meldet ORBIT sich, wenn es nicht vorn ist; die erste Sichtung meldet nichts. Bei einer Freigabe steigt über der Figur des Repos dasselbe grüne Häkchen auf wie für eine erledigte Aufgabe, und beides kommt ins Bordbuch.

### Die Anzuguhr

Die Station hat einen Stoffwechsel; ein Mensch draußen auch, und der hängt nur an einer Zahl: wie lange er schon draußen ist. Im Detailfenster steht deshalb ein Balken von null bis sieben Stunden, und bei 6,5 beginnt eine schraffierte Sperrzone — die halbe Stunde Reserve, die der Grund für die 6,5 ist und nicht die Arbeit.

Darunter die vier Vorräte, der knappste zuerst: Strom und CO₂-Filter reichen sieben Stunden, Sauerstoff und Kühlwasser acht. Dass zwei Paare denselben Wert zeigen, ist keine Doppelung, sondern die Aussage — Batterie und Filter beenden einen Einsatz, nicht die Luft. Die Zahlen sind die des amerikanischen Anzugs in der ISS-Fassung; der längste Einsatz der Geschichte dauerte 8 Std. 56 Min. (Voss und Helms, 11. März 2001).

Auf die Uhr gelegt wird die Laufzeit der Sitzung oder des Prozesses. Das ist eine Entsprechung und keine Messung, und genau das steht unter dem Balken. Die Startzeit kommt, in dieser Reihenfolge, aus `startedAt` im Sitzungsregister, sonst aus dem Erstelldatum der jsonl-Datei, bei Prozessen aus der Laufzeit von `ps`. Ohne echte Startzeit fällt die ganze Uhr weg, statt eine zu erfinden.

In der Szene taucht sie zweimal auf: als Punkt vor dem Namensschild (bernstein in der Reserve, rot darüber hinaus) und aus der Nähe als Ampel auf der Bedieneinheit an der Brust.

### Aussteigen und Einsteigen

Ein neuer Astronaut erschien früher einfach mitten auf dem Träger und ein beendeter verschwand ebenso. Das ist der einzige Weg von draußen nach drinnen, den es an einer echten Station nicht gibt.

Wer während des Laufens dazukommt, steht jetzt an der Luftschleuse und hangelt sich zu seinem Platz. Wer schon da war, als die App aufging, ist einfach draußen — die App hat die Sitzungen nicht gestartet, und ein Ausstieg bei jedem Neuladen wäre eine Lüge. Wer aus den Quellen fällt, hangelt zurück und ist erst an der Luke wirklich weg; unterwegs kehrt er um, wenn er noch nicht über der Hälfte ist, und dreht wieder um, falls die Quelle zurückkommt. Im Bordbuch steht der ganze Bogen.

Wer einsteigt, hinterlässt im Bordbuch einen kurzen Einsatzbericht — „webshop-kasse ist eingestiegen · 1 Std. 24 Min. im Einsatz · 6 von 8 Aufgaben erledigt": von der ersten bis zur letzten Zeile der Sitzung, und wie weit ihre Aufgabenliste gekommen ist. Fehlt eine Angabe, fehlt sie auch im Bericht.

### Wie sich die Crew draußen verhält

- **Das Goldvisier fährt mit dem Licht.** Bei Tag ist es unten, im Erdschatten schiebt die Crew es hoch — sonst sähe sie im Licht der Helmlampen nichts. Dann sieht man hinter dem klaren Visier schwach ein Gesicht unter der Sprechkappe. Jeder tut das zu seiner eigenen Zeit, nicht alle auf einen Schlag; während der Bewegung sieht man die Goldkante wandern. Nachts verschwindet auch die Spiegelung der Erde im Visier, denn darunter ist es dunkel.
- **Während ein Triebwerk läuft, hält sich jeder fest.** An einer Station, die beschleunigt, ist ein treibender Anzug nicht mehr in Ruhe mit ihr; die Crew zieht sich sichtbar an die Struktur heran.
- **Kommt ein Schiff an oder fährt es ab, sieht die ganze Crew hin** — ein Anflug wird von außen beobachtet, weil im Zweifel jemand den Abbruch rufen muss. Sonst dreht sich jeder zu seinem nächsten Nachbarn.
- **Helmlampen und Kennleuchten.** Die Lampen sind harte Punkte, und ihr Lichthof hat eine feste Größe in Bildpunkten: er entsteht in Auge und Linse, nicht draußen, und darf beim Heranfahren nicht mitwachsen. Vorher waren es flache Scheiben mit dem Helm als Maßstab, und aus der Nähe standen zwei graue Ohren am Helm. Die Kennleuchten der Station sitzen jetzt auf Mast und Beschlag auf dem Obergurt, statt als Kreise im Leeren zu schweben.
- **Sprechblasen** brechen auch lange Pfade um, am liebsten hinter einem Schrägstrich, und zeigen bei einer Tätigkeit den Anfang — ein Befehl beginnt mit dem, was er tut. Bei einem Gedanken, der gerade einläuft, bleibt es das Ende.
- **Die Hand zeigt das echte Werkzeug.** Wer liest, hält die Kamera in ihrer weißen Thermohülle — draußen wird fotografiert, was man sich ansieht —, wer sucht, schwenkt sie langsam. Wer schreibt, hat den Schrauber. Wer einen Befehl ausführt, hat die Hand an der Bedieneinheit vor der Brust, wer im Netz ist, an der Seite des Helms, wo innen die Sprechkappe sitzt. Wer delegiert, zeigt mit gestrecktem Arm hinaus und dreht sich dabei zu dem Unteragenten, den er zuletzt losgeschickt hat. Wer plant, hält die Prüfliste. Und jeder echte Werkzeugaufruf wird ein kurzer Puls in der Hand: der Schrauber zieht an und sprüht Funken, die Aufnahmeleuchte der Kamera geht an, an der Konsole leuchtet eine Taste. Vorher zog der Schrauber nach einer festen Uhr — jetzt sind die Funken die Arbeit selbst. Weil die Brücke nur alle paar Sekunden liest, kommen Aufrufe in Bündeln; sie werden über zweieinhalb Sekunden verteilt, höchstens sechs, und die erste Sichtung holt nichts nach.
- **Die Leine ist eine Nervenbahn.** Bei einer Sitzung lief auf der Leine ein gleichmäßiger Strom alle 150 Millisekunden, fünfundzwanzig Sekunden lang nach dem letzten Eintrag — eine Sitzung, die einmal eine Datei las, sah genauso beschäftigt aus wie eine, die zwanzig Befehle hintereinander absetzte. Jetzt ist jeder Impuls ein echter Werkzeugaufruf: ein Lichtpunkt mit hellem Kern läuft zur Station, und wo er ankommt, leuchtet der Haltepunkt kurz in der Farbe des Absenders auf. Eigene Agenten, deren Antwort wirklich hereinströmt, behalten den Strom.
- **Die Prüfliste am Unterarm.** Jeder Anzug trägt links am Unterarm eine „cuff checklist", ein kleines Heft mit Ringbindung, in dem die Schritte des Einsatzes stehen. Aus der Nähe steht darauf der Stand der Aufgabenliste, wenn die Sitzung eine hat: so viele Zeilen grün abgehakt, wie erledigt sind.
- **Abgehakt.** Hakt eine Sitzung eine Aufgabe ab, steigt über ihrer Figur für drei Sekunden ein kleines grünes Häkchen mit dem Namen der Aufgabe auf. Ins Bordbuch kommt „webshop-kasse hat „decimal.js installieren" erledigt". Werden mehrere auf einmal fertig, kommen sie nacheinander und stapeln sich. Ist die Liste durch, sagt das letzte „Alle 8 Aufgaben erledigt". Die erste Sichtung feiert nichts nach, und eine wieder geöffnete Aufgabe darf beim nächsten Abhaken wieder feiern.
- **Ein Bericht kommt an.** Gibt ein Unteragent seinen Bericht ab, steigt über der Sitzung, die ihn bekommt, „Bericht von Tests Warenkorb" auf, mit einem ankommenden Pfeil in der Farbe des Unteragenten. Vorher stand das nur im Bordbuch. Die erste Sichtung eines schon fertigen Unteragenten gilt dabei nicht als Wechsel.
- **Bänder und Blasen weichen einander aus.** Das aufsteigende Band lag am Handy drei Sekunden lang quer über den Namensschildern der Nachbarn. Jetzt sucht es sich wie die Blasen die nächste freie Höhe über oder unter Namen, Figuren und Blasen, prüft dabei den ganzen Weg nach oben und behält seine Höhe. Liegt die Lücke weit weg, führen drei Punkte zur Figur. Umgekehrt landet eine neue Blase nicht auf einem Band, das schon steht. Dabei aufgefallen: Die Figuren standen in der Liste der Hindernisse in Szenenkoordinaten, Schilder und Blasen in Bildschirmkoordinaten. Herangefahren wichen die Blasen deshalb einem Kasten aus, der woanders lag.
- **Farben, die sich unterscheiden.** Die Farbe einer Figur kommt aus ihrem Namen, und die alte Streuung (h · 31 + Zeichen, dann modulo 8) hing nur an den unteren drei Bits jedes Zeichens — „orbit", „webshop" und „blog" bekamen dasselbe Grün. Jetzt FNV-1a mit Nachmischen; 4000 zufällige Sitzungskennungen verteilen sich mit 469 bis 545 je Farbe.
- **Details nach der Größe auf dem Schirm.** Die Detailstufen der Figuren hingen an ihrer Größe in der Welt, und die hängt an der Fensterbreite — gemessen 15 auf dem Handy, 17,6 bei 1000 Punkten, 30,6 bei 1920. Auf dem Handy waren Lagerringe, Funkantenne und das Anzeigefeld der Bedieneinheit deshalb auch ganz nah nie zu sehen, auf einem großen Schirm dagegen immer, auch ganz herausgezoomt. Jetzt zählt die Größe auf dem Schirm.
- **Namen und Blasen am Bildrand.** Wer ganz außerhalb des Bildes treibt, bekommt weder Namensschild noch Blase — beide wurden an den Rand geklemmt und standen dort ohne ihre Figur, halb abgeschnitten, über den Knöpfen. Schilder werden nach ihrer echten Breite eingepasst und weichen einander nach ihrer echten Breite aus; vorher galt für alle eine halbe Breite von 54 Punkten, und zwei lange Namen achtzig Punkte auseinander galten als frei. Unter Kopf- und Fußleiste steht keins. Blasen suchen die nächste freie Höhe über oder unter Figuren, Namen und anderen Blasen und bleiben unter dem Kopf; findet sich keine, entfällt die Blase, statt auf einer anderen zu liegen. Steht sie unter ihrer Figur, führen die Punkte hinauf zu den Füßen.

## Gegen echte Daten geprüft

Die Brücke lief lange nur gegen nachgebaute Protokolle und Befehlsausgaben. Dann einmal gegen eine echte Arbeitsumgebung — Neutralinos Datei- und Befehlszugriffe auf das echte System umgeleitet, nur lesend. Gefunden und behoben:

1. **Das Lesefenster war zu klein.** Bei einem Agenten war die letzte Zeile ein Schreibbefehl von 90 kB; die 120 kB am Dateiende schnitten ihn an, und es blieb kein einziger Eintrag des Assistenten übrig — kein Modell, kein Schritt, obwohl er über fünfzig Werkzeugaufrufe hinter sich hatte. In der Sitzungsdatei (221 MB) sind einzelne Zeilen über 1,3 MB groß: eingebettete Bilder. Jetzt wächst das Fenster: 120 kB, 600 kB, 3 MB.
2. **Abbrüche sahen aus wie Berichte** — drei Agenten im Nutzungslimit standen als „Bericht abgegeben" da.
3. **Die Agenten von Arbeitsabläufen fehlten ganz**, eine Ebene tiefer; und ihr Ergebnis über `StructuredOutput` zählte nicht als Bericht, weil danach noch die Quittung des Ablaufs im Protokoll steht.
4. **Namen**: „Die Tests für" statt der Beschreibung aus der `.meta.json`.
5. **Laufende Befehle**: „claude" im Suchmuster passte auf jeden Prozess mit `.claude/` im Aufruf, darunter die Hüllen, in denen Claude Code jeden Befehl ausführt — jeder Entwicklungsserver stand doppelt da. Und `python -m` passte nicht auf `python3 -m`.
6. **Projektordner**: `stat -f %m` ist die Schreibweise von macOS; unter Linux gab sie die Daten des Dateisystems aus. Jetzt erst `stat -c %Y`, das auf dem Mac still scheitert.
7. **Sprechblasen** sprengte ein Pfad ohne Leerzeichen.
8. **Die Anzuguhr** fertiger Unteragenten lief bis in die Reserve weiter.
9. **Kleinigkeiten**: Marke und Zustand widersprachen sich, „vor 1 Tagen", abgeschnittene Aufträge ohne „…".

Und weil es mit echten Datenmengen erst sichtbar wurde: ein Protokoll, das nicht gewachsen ist, wird nicht neu gelesen; Aufgabe und `.meta.json` eines Unteragenten einmal; und je Projektordner nur neu gelistet, wenn sich sein Datum geändert hat, mit einem vollen Blick je Minute. Bei 50 Projekten mit je 20 alten Sitzungen sind das 52 Dateiabfragen je Durchlauf statt 1053.

## Eigene Claude-Agenten

Anlegen mit Name, Rolle als System-Prompt, Modell, Aufwandsstufe und Anzugfarbe. Aufträge gehen an einen Agenten oder parallel an die ganze Crew. Vier fertige Rollen stehen bereit: Prüfer, Lehrer, Gegenrede, Kurzfassung.

Die Aufrufe laufen direkt aus dem Browser gegen `api.anthropic.com`, freigeschaltet über `anthropic-dangerous-direct-browser-access`. Der Schlüssel bleibt im `localStorage`. Adaptives Denken mit `display: "summarized"`, Denktiefe über `output_config.effort`. Bei den großen Modellen ist der serverseitige Fallback aktiv; kennt das Konto die Beta nicht, wiederholt die App die Anfrage ohne sie. Das kleinste Modell bekommt korrekterweise weder `thinking` noch `effort`.

Antworten laufen als Strom ein: das Denkprotokoll in die Gedankenblase, der Text ins Missions-Log. Je Mission werden Tokens und geschätzte Kosten angezeigt.

## Die Station

Nach echten Maßen gebaut, und die Maße sind der Grund, warum sie aussieht, wie sie aussieht.

| Bauteil | Maß | In Modulradien |
|---|---|---|
| Gitterträger | 108,5 m | 50,7 |
| Solarflügel | 34 × 11,6 m | 15,8 × 5,4 |
| Radiator | 23 × 3,4 m | 10,7 × 1,6 |
| Druckmodul | 4,3 m dick | 2 |
| Mensch im Anzug | 1,9 m | 0,88 |

Daraus folgt: die Druckmodule sind ein kleiner Klumpen in der Mitte eines langen Balkens, und die Figuren sind winzig. Frühere Fassungen hatten den Träger halb so lang und die Flügel ein Viertel so groß — genau das ließ die Station wie ein Modell aussehen.

**Die Flügel stehen quer zum Träger, nicht längs.** Anders könnte das Alpha-Drehgelenk sie nicht zur Sonne drehen, denn es dreht um die Trägerachse. Daraus entsteht die bekannte Silhouette.

**Und sie drehen sich.** Einmal je Umlauf, mit gleichbleibender Rate — im Vakuum bremst nichts, also gibt es kein Anlaufen und kein Auslaufen an den Umkehrpunkten. Die Wärmetauscher drehen gegenläufig: ihr Gelenk hält sie schmal zur Sonne, damit sie sich nicht aufheizen.

**Die Rückseite der Flügel leuchtet.** Weil das Gelenk den Flügel immer zur Sonne dreht, steht die Sonne dahinter, wenn man von hinten daraufsieht — sie scheint durch die Kaptonfolie, und die Zellen zeichnen sich als dunkles Gitter davor ab wie ein Blatt gegen den Himmel.

**Der Frachter bringt, was wirklich geliefert wurde.** Ist GitHub angeschlossen, fliegt er nicht mehr nach Plan. Er kommt, wenn ein Pull Request gemergt oder auf den Hauptzweig gepusht wurde, bleibt drei Minuten am Stutzen und legt wieder ab. Ein Schild sagt, was er gebracht hat („FRACHTER · PR #12 · webshop“), und unter Stationswerte steht es ebenso. Im Bordbuch steht jede Lieferung mit Titel, und liegt ORBIT nicht vorn, kommt eine Mitteilung.
- **Erkannt wird ohne weitere Abfragen.** Ein neuer Lauf mit dem Anlass `push` auf dem Hauptzweig ist eine Lieferung; mehrere Abläufe auf denselben Commit (`head_sha`) sind eine.
  - Heißt er „Merge pull request #12 …“ oder endet er auf „(#12)“ wie ein Squash-Merge, ist es dieser PR, mit dem Titel, den er als offener hatte.
  - Verschwindet ein PR aus den offenen, ohne dass ein solcher Lauf kam, fragt ORBIT einmal nach. Nur gemergt zählt, geschlossen nicht.
- **Nichts wird nachgeholt:** nicht bei der ersten Sichtung und nichts, was länger als eine Stunde her ist.
- **Was dazukommt,** während er anfliegt oder angedockt ist, geht mit an Bord; angedockt bleibt er dann eine Minute länger. Was beim Ablegen kommt, nimmt der nächste Flug mit.
- **Ohne GitHub** fliegt er wie bisher nach Plan, damit an der Station trotzdem etwas ankommt.
- **In der Vorführung** wird PR #12 nach hundert Sekunden gemergt, und der Frachter bringt ihn.

**Der Träger trägt Leitungen.** Ein Baugerüst hat Streben, eine Station hat Leitungen: zwei dick isolierte Ammoniakleitungen über die ganze Länge, eine warme hin und eine kalte zurück, daneben der Kabelstrang der Flügel — mit Schellen an jedem zweiten Feldknoten, denn eine Leitung, die nirgends befestigt ist, sieht aufgemalt aus.

**Die Fenster sind Glas.** Vier Dinge machen aus einem farbigen Kreis ein Fenster: die tiefe Fassung als schmaler dunkler Ring, der vom Rahmen verdeckte Rand, die Erde als heller Bogen auf der erdzugewandten Seite und der harte kleine Sonnenpunkt (die Sonne misst ein halbes Grad, also ist ihr Spiegelbild scharf). Das Innenlicht wird bei Tag halbiert — gegen Erde und Sonne draußen ist eine Deckenleuchte nichts.

Dazu: Handläufe höchstens 61 cm auseinander, Steppmuster der Schutzdecken in Metermaß als Größenhinweis, harte Schlagschatten ohne Halbschatten, Einschlagspuren, Alterungsflecken, eine Antennenschüssel, die der Bodenstation folgt.

**Aus der Nähe bleiben die Linien.** Ab Zoom 3 wird die Station als scharfer Ausschnitt in voller Auflösung gebacken, mit 400 bis über 2000 Punkten Radius. Einige Striche hatten aber feste Breiten von 0,35 bis 0,5 Punkten. Das ist richtig für die Stufen der Leiter, im Nahausschnitt waren sie mit einem Viertel Deckkraft weg. Genau beim Heranfahren verschwanden so die Nähte der Modulhüllen, die Rippen der Wärmetauscher, die Kanten der Trägerkästen, Drehgelenke und Knoten und das Zellraster der Kapselpaneele. Jetzt bleibt auf der Leiter jeder Strich, wie er war, und im Nahausschnitt ist er mindestens einen Punkt breit, mit der Auflösung wachsend bis zwei. Die angedockte Kapsel hatte dadurch aus der Nähe zwei flache dunkelblaue Flächen. Ihre Paneele haben jetzt Zellreihen und den Glanz auf dem Glas, der Stutzen ist Metall mit Kopplungsringen, und die Stirnseite liest sich als Ring statt als Loch.

**Gas hat keine Kante.** Die Wolken beim Abblasen des CO₂-Filters und bei der Bahnanhebung waren gefüllte Kreise, bis zu 46 Prozent deckend. Aus der Nähe standen dort graue Scheiben wie Seifenblasen. Jetzt ist jeder Wolkenteil ein weicher Hauch, einmal gebacken und skaliert kopiert. Die Eiskörner im Ventilstrahl wuchsen mit der Kamera. Jetzt bleiben sie bei jedem Zoom Lichtpunkte von ein, zwei Bildpunkten, denn ein Korn misst Millimeter.

**Keine Namensschilder an den Bauteilen.** Sie standen früher ab Zoom 1,5 über der halben Station und haben genau das verdeckt, was man sich ansehen wollte. Die Namen gibt es weiter — beim Antippen, und zwar bei jedem Zoom. Es gewinnt das nächstgelegene Bauteil, nicht das erste in der Liste.

## Die Erde

Unter der Station liegt die echte Erde. Bis hierher war sie gerechnet: Land, Meer und Wolken aus Rauschen, zu einer endlosen Bahn gebacken, die unter einer runden Maske durchzog. Das sah nach einem Planeten aus, aber nach keinem bestimmten.

- **Die Karten.** Drei Bilder der NASA, gemeinfrei, zusammen 1,4 MB, als Dateien neben der Seite.
  - Blue Marble: Land und Meeresboden ohne Wolken, 4096 × 2048.
  - Die Wolkendecke aus demselben Satz, 2048 × 1024. Sie ist leicht weichgezeichnet, damit das feine Korn der Passatwolken nicht wie Rauschen aussieht.
  - Black Marble: die Stadtlichter, 4096 × 2048. ORBIT nimmt davon nur die Lichter, nicht das mondbeschienene Gelände.
- **Die Abbildung.** Ein WebGL-Schattierer rechnet für jeden Bildpunkt der Scheibe aus, welcher Punkt der Kugel dort liegt, und schlägt Länge und Breite in den Karten nach. Die Erde ist dabei eine Kugel, von weit weg und senkrecht auf die Bahnebene gesehen. Der Punkt unter der Station liegt oben auf der Kante, darunter der Streifen seitlich der Bahn, zur Kante hin immer flacher. Mit dem Umlauf dreht sich die ganze Scheibe um ihren Mittelpunkt.
- **Bahn und Sonne.**
  - Die Bahn ist wie die der ISS 51,6 Grad geneigt.
  - Die Sonne steht, wo sie wirklich steht, aus Datum und Uhrzeit auf ein Hundertstel Grad gerechnet.
  - Die Bahnebene wird so gelegt, dass die Sonne in ihr liegt, wie es der Tag-und-Nacht-Takt der Szene annimmt.
  - Am Mittag der Station liegt unter ihr das Land, auf dem gerade Mittag ist. Ist es in Europa Nacht, zieht Europa mit seinen Lichtern auf der Nachtseite vorbei.
- **Der Tagesrand.** Mit der echten Erde ist der Rand nicht mehr getaktet, sondern gerechnet. Die Sonne liegt in der Bahnebene, deshalb ist der Rand in dieser Ansicht eine Gerade durch den Mittelpunkt der Scheibe, senkrecht zur Sonne. So liegt er dort, wo auf der Karte wirklich Tag und Nacht aneinanderstoßen, und passt zur Bodenspur.
  - Dabei ist ein alter Rechenfehler aufgefallen. Der Punkt unter der Station kreuzt den Rand nicht zwei, sondern gut fünf Minuten vor ihrem eigenen Sonnenuntergang.
  - Der Grund: Die Station tritt erst 69,8 Grad vor dem Gegenpunkt der Sonne in den Schatten (asin 6371/6790), also 20 Grad später als der Boden unter ihr.
  - Auch die gerechnete Erde nimmt jetzt die fünf Minuten.
- **Polarlicht am magnetischen Pol.**
  - Das Polarlicht kommt nicht mehr zweimal je Umlauf nach Formel, sondern aus dem Ort. Gerechnet wird die magnetische Breite des Punkts unter der Station, als Dipol mit dem Pol über Nordkanada.
  - Deshalb leuchtet es dort, wo die Crew es wirklich filmt: über Kanada und über dem Südpolarmeer südlich von Australien. Dort kommt die Station auf gut 60 Grad magnetische Breite, über Europa nur auf knapp 52.
- **Das echte Weltraumwetter, auf Wunsch.** Wie weit das Polarlicht zum Äquator reicht und wie hell es ist, hängt an der Sonne. Das Maß dafür ist der Kp-Index, von 0 (ganz ruhig) bis 9 (schwerster Sturm), in Dritteln: 5− ist 4,67, 5+ ist 5,33. Ohne echte Werte rechnet ORBIT mit Kp 2, einem gewöhnlichen Tag; so sah es immer aus. Unter Stationswerte lässt sich das echte Weltraumwetter einschalten.
  - Dann fragt ORBIT alle fünf Minuten beim Space Weather Prediction Center der NOAA nach dem Kp, geschätzt aus der letzten Minute. Solange die ganze Erde offen ist, holt es alle zehn Minuten auch die Vorhersage OVATION: eine Karte mit einem Wert je Grad Breite und Länge, wie wahrscheinlich dort in der nächsten Stunde Polarlicht zu sehen ist. Sie ist gut 900 Kilobyte groß, gepackt 140. Beide Dienste sind öffentlich, brauchen keinen Schlüssel und erlauben Browsern die Antwort.
  - Ausgeschaltet geht keine Anfrage hinaus, im Hintergrund auch nicht. Nach einem Fehler kommt der nächste Versuch nach einer Minute. Ein Kp, der älter ist als drei Stunden, und eine Karte, die älter ist als eine Stunde, gelten nicht mehr; dann steht „nicht erreichbar“ da, und es gilt wieder der gewöhnliche Tag.
  - **In der Szene** rückt die Grenze des Polarlichts je Kp-Stufe um zwei Grad magnetischer Breite zum Äquator, und es wird heller. Bei Kp 7 leuchtet es auch über Europa, bei Kp 0 über Kanada nur schwach. Bei einem Sturm stehen die Vorhänge höher und bekommen oben das Rot des Sauerstoffs, wie bei den Stürmen im Mai 2024. Die Helligkeit ist über dem gewöhnlichen Tag gestaucht, sonst stünde im Sturm jeder Vorhang am Anschlag, und aus Knoten und Lücken würde eine gleichmäßige Wand. Liegt die Karte der NOAA vor, zählt sie: das Hellste im Umkreis von 24 Grad, so weit sieht die Crew Polarlicht über den Horizont hinaus, das Nahe mehr als das Ferne.
  - **Auf der Kugel** liegt die Karte der NOAA statt des gerechneten Ovals. Zehn Prozent, so viel hat das Oval in einer ruhigen Nacht, werden so hell wie das gerechnete bei Kp 0, dreißig Prozent so hell wie bei Kp 2, darüber geht es in die Sättigung. Ein Prozent ist Grundrauschen und bleibt dunkel. Die Vorhänge bleiben, denn die Karte ist nur ein Grad fein. Ohne Karte rückt das gerechnete Oval mit Kp: um Mitternacht gut zwei Grad je Stufe, mittags knapp eins, und es wird breiter.
  - Die Stationswerte nennen den Kp in der üblichen Schreibweise und die Sturmstufe der NOAA, etwa „Kp 7+ · Sturm G3 · stark“. Beginnt ein Sturm oder wird er stärker, steht es im Bordbuch. Ein Tipp auf die Nachtseite der Kugel nennt die Wahrscheinlichkeit dort, etwa „Polarlicht 45 %“.
  - **Der Sonnenwind.** Im selben Takt holt ORBIT zwei kleine Zusammenfassungen von je sechzig Bytes: wie schnell der Sonnenwind an der Messsonde vor der Erde vorbeizieht und wohin sein Magnetfeld zeigt. Zeigt es nach Süden, koppelt es an das Erdfeld, und das Polarlicht wird unruhig. Die Vorhänge laufen schneller, bei 400 km/s und 6 nT nach Süden doppelt so schnell, höchstens zweieinviertelmal, und es leuchtet in Schüben auf wie bei einem Teilsturm. Nach Norden bleibt es ruhig, egal wie schnell der Wind ist. Der Kp folgt dem erst Stunden später; der Wind ist das, was gerade ankommt. In den Stationswerten steht er als „620 km/s · Feld 12 nT nach Süden“, und dreht das Feld kräftig nach Süden, steht es einmal im Bordbuch.
  - Um wie viel Kp das Oval verschiebt, ist die übliche Faustregel, keine Modellrechnung. Bei Kp 9 liegt die Mitte des Ovals um Mitternacht damit bei 53 Grad magnetischer Breite; das passt zum Mai 2024, als es bis Mitteleuropa zu sehen war.
- **Wolken.**
  - Ihre Schatten fallen auf die sonnenabgewandte Seite, und die sonnenzugewandte Flanke ist heller.
  - An den Rändern liegt feines Rauschen, denn die Karte hat dort acht Kilometer je Bildpunkt, der Schirm zwei.
  - Dicke Wolken verschlucken Stadtlichter, dünne machen sie weich.
- **Gewitter, Mond und Blitze** hängen an der echten Wolkendecke.
  - Die Zellen sitzen erdfest in ihren dicksten Stellen zwischen 50 Grad Nord und Süd, auf einem Raster von einem Grad. Über die ganze Erde sind es 651.
  - Der Mond beleuchtet nur, wo wirklich Wolken sind. Über klarem Himmel bleibt die Nacht schwarz, mit den Städten darin.
- **Worüber die Station fliegt.**
  - Unter Stationswerte steht zum Beispiel „Unter uns: Italien · 44° N · 12° O“.
  - Wer auf die Erde tippt, erfährt, welches Land oder Meer an der Stelle liegt, dazu die Sonnenzeit und ob dort Tag, Dämmerung oder Nacht ist: „Mittelmeer · 35° N · 18° O · 15:50 Sonnenzeit · Tag“. Die Sonnenzeit zeigt, was eine Sonnenuhr dort zeigen würde, nicht die Uhrzeit der Zeitzone. Ist gerade etwas offen, schließt der Tipp es wie bisher.
  - Die Grenzen kommen von Natural Earth und sind gemeinfrei: Länder im Maßstab 1:50 Millionen, dazu Ozeane, Meere, Golfe und Meeresstraßen, zusammen 355 deutsche Namen.
  - Gebacken sind sie zu einer Karte von 1440 × 720 Punkten (47 KB), mit der Nummer des Namens in jedem Punkt. Enklaven wie Lesotho bleiben erhalten, Zwergstaaten wie der Vatikan fallen durchs Raster.
- **Die Bodenspur.** Unter der Umlaufuhr zeigt eine kleine Weltkarte die Spur der Bahn: den letzten halben Umlauf blass, den nächsten hell. Dazu zeigt sie die Nacht aus dem echten Sonnenstand und einen Punkt, wo die Station gerade steht. So fangen die ISS-Verfolger im Netz an. Die Spur schlängelt sich zwischen 51,6 Grad Nord und Süd.
- **Im Rundgang und im Bordbuch.**
  - Mit der echten Erde kommt zum Schluss der Blick nach unten. Die ganze Station rückt ein Stück nach oben, und auf der Tafel steht, was gerade unter uns liegt.
  - Der letzte Halt ist die ganze Erde. Die Kamera fährt zurück, bis die Kugel im Bild ist, und mit dem Ende des Rundgangs wieder zur Station. Wer vorher tippt, Esc oder E drückt, beendet beides. R mitten in diesem Halt beendet den Rundgang, statt ihn gleich neu zu beginnen.
  - Im Bordbuch steht bei Sonnenaufgang und Erdschatten der Ort: „Sonnenaufgang · Indischer Ozean“.
  - In der Hilfe standen „acht Halte“, es waren aber neun. Jetzt wird gezählt.
- **Die ganze Erde.** Wer weiter herauszoomt, als der Zoom reicht, oder E drückt, fährt zurück, bis die ganze Kugel im Bild ist. Es sind dieselbe Karte, dieselbe Sonne und dieselbe Bahn, nur von weiter weg und schräg von oben: Die Kamera steht fünfzig Grad vom Punkt unter der Station entfernt.
  - Tag und Nacht rechnet hier jeder Bildpunkt selbst aus der echten Sonne. In der Dämmerung liegt ein schmaler roter Saum, vor allem auf den Wolken, denn der Boden darunter ist dort schon dunkel. Auf der Nachtseite leuchten nur die Städte.
  - **Sonnenglanz.** Wo das Meer die Sonne zum Betrachter spiegelt, liegt ein heller, silbriger Fleck, wie auf jedem Foto der ganzen Erde. Er sitzt dort, wo die Oberfläche genau zwischen Sonne und Auge steht. Die Wellen verschmieren ihn: Nach Cox und Munk ist die Neigung der kleinen Wasserflächen etwa normalverteilt, bei fünf Metern Wind mit einem mittleren Quadrat um 0,03. Wasser erkennt der Schattierer an der Karte, denn Blue Marble malt nur Wasser blau. Gemessen ist Blau dort mindestens 2,3-mal so stark wie Rot, an Land höchstens gleich stark. Inseln und Wolken bleiben ohne Glanz.
  - **Polarlicht.** Auf der Nachtseite liegt das Oval um den magnetischen Pol, derselbe Dipol wie in der Szene. Es sitzt um Mitternacht bei gut 67 Grad magnetischer Breite, zur Mittagsseite hin näher am Pol, bei 75 Grad, und ist um Mitternacht am hellsten. Von oben gesehen liegt es in Bögen längs des Ovals, zwei oder drei nebeneinander, mit Falten und hellen Knoten, wie auf den Nachtbildern der Wettersatelliten. Es leuchtet in hundert Kilometern Höhe, über den Wolken.
  - **Blitze.** In den Gewitterzellen der Szene, den dicksten Wolken der Karte, leuchtet es auf der Nachtseite kurz auf. Ein Blitz dauert ein bis drei Schläge, manchmal springt er auf die Nachbarzelle über. Über Land blitzt es öfter als über dem Meer. Bei Tag und bei angehaltener Zeit blitzt es nie. Auf der Nachtseite der echten Erde sind es rund vierzig Blitze je Sekunde, hier nur die hellen, im Mittel vier.
  - **Der Himmel dahinter ist der echte.** 117 helle Sterne stehen an ihren Himmelskoordinaten: Orion, der Große Wagen mit dem Polarstern, Kassiopeia, das Kreuz des Südens mit den beiden Zeigern, Skorpion, Schütze, das Sommerdreieck, Pegasus, die Plejaden und die Hyaden, die auffallenden in ihrer Farbe. Dazu kommen gut 3700 schwache, dichter entlang der Milchstraße. Die Sternzeit dreht sie ins erdfeste System, und sie werden durch dieselbe Kamera gesehen wie die Kugel, nur mit Brennweite. Dreht man die Kugel, dreht sich der Himmel mit. Schaut die Kamera gegen das Licht, steht hinter der Erde die Sonne mit ihrem Schein. Die Sterne sind gedämpft, denn neben der hellen Erde ist die Belichtung kurz; auf echten Fotos der ganzen Erde sieht man meist gar keine.
  - **Der echte Mond.** Er steht hinter der Erde, wo er wirklich steht, in seiner echten Phase, die helle Seite zur Sonne. Gerechnet wird er aus den Hauptgliedern der Mondbahn nach Meeus: Mittelpunktsgleichung, Evektion, Variation und jährliche Gleichung. Auf der Nachtseite liegen die Wolken grau-blau in seinem Licht, dort, wo er über dem Horizont steht. Bei Vollmond ist das deutlich, bei Halbmond kaum zu sehen, bei Neumond gar nicht. Als Helligkeit gilt der beleuchtete Anteil hoch 3,3.
  - **Der Rand im Gegenlicht.** Wo der Luftsaum über den Tagesrand läuft, geht dort gerade die Sonne auf oder unter. Das Licht kommt flach durch viel Luft, das Blau ist herausgestreut, und der Saum wird orange, am Boden roter.
  - **Der Rand bei Nacht.** Über der Nachtkante steht eine dünne grüne Linie, das Nachthimmelsleuchten in 95 Kilometern Höhe, rund um die ganze Nachtseite, wie in der Szene. Wo das Polarlicht-Oval hinter der Kante liegt, steht dort das Polarlicht von der Seite: grün um 110 Kilometer, darüber rot bis gut 250, im Sturm röter. Streifend gesehen leuchtet eine dünne Schicht viel heller als von oben; so hebt sich der Bogen von der dunklen Kugel ab. Beides ist Licht, es deckt die Sterne dahinter nicht zu. Die Rechnung des Polarlichts ist dieselbe wie auf der Oberfläche, mit der Karte der NOAA, wenn sie da ist.
  - Die Bahn läuft als Ellipse um die Kugel, in echter Höhe: 420 über 6371 Kilometern. Hinter der Kugel ist sie verdeckt, vor der Station heller als hinter ihr.
  - Oben auf der Bahn steht die Station als heller Punkt. Maßstäblich wäre sie von hier aus nicht einmal ein Bildpunkt. Darüber steht, wer an Bord ist und was unter ihr liegt, etwa „Unter uns: Atlantischer Ozean“. Die Namen kommen aus einer Liste ohne Artikel; „über Atlantischer Ozean“ wäre falsch gebeugt, deshalb der Doppelpunkt.
  - **Ziehen dreht die Kugel.** Was man greift, geht mit dem Finger: seitwärts um die Station herum, hoch und runter gekippt, von fast senkrecht über ihr bis flach von der Seite. Die Station bleibt dabei oben in der Mitte. Beim nächsten Hineinzoomen steht die Kamera wieder fünfzig Grad schräg.
  - **Zoomen zoomt die Kugel.** Mausrad, zwei Finger und Plus machen sie bis zu zweieinhalbmal so groß oder halb so klein, mit Satellitenbildern bis 6000-fach (siehe unten). Wer darüber hinaus weiter hineinzoomt, kommt zur Station zurück. Hineingezoomt rechnet der Schattierer nur den Ausschnitt, der auf dem Schirm liegt, höchstens 2048 Punkte je Seite; den Rest zieht der Browser hoch.
  - Ein Tipp auf die Kugel nennt Land oder Meer mit Sonnenzeit. Ein Tipp auf die Station, Esc, Doppelklick und die Leertaste führen zurück, ebenso der Sprung zu einem Astronauten. Esc schließt zuerst die Karte zum angetippten Ort.
  - Die Überblendung läuft nach der Uhr und nicht nach Bildern. Eine Blende mit festem Schritt je Bild stand ohne Grafikchip nach Sekunden noch auf halbem Weg, und die Station schimmerte durch die Erde.
  - **Behoben:** Bis Version 18 pendelte die Blende, sobald sie angekommen war: Bei 1 zog sie das nächste Bild wieder ein Stück zurück und das übernächste wieder hoch. Die Station schimmerte in jedem zweiten Bild durch, und das Einsparen der Szene griff nur jedes zweite Mal.
  - Liegt die Kugel ganz über allem, wird die Station nicht gezeichnet. Was an Bord läuft, läuft weiter. Die Kugel selbst wird nur neu gerechnet, wenn sie sich um einen halben Bildpunkt gedreht hat, und alle zwei Sekunden für die Sonne.
  - Auf dem Handy bestimmt die Breite die Größe: Die Bahn reicht links und rechts ein Fünfzehntel über die Kugel hinaus und passt noch ins Bild.
- **Die echte ISS, auf Wunsch.** Die Station hier fliegt eine Bahn wie die ISS, aber nicht die echte an ihrer echten Stelle. Wer sehen will, wo die gerade ist, schaltet es unter Stationswerte ein.
  - Dann fragt ORBIT alle zwanzig Sekunden bei wheretheiss.at nach, einem öffentlichen Dienst ohne Schlüssel, der Browsern die Antwort erlaubt. Mitgeschickt wird nichts als die Anfrage selbst.
  - Ausgeschaltet geht keine einzige Anfrage hinaus. Gefragt wird nur, solange die Stationswerte oder die ganze Erde offen sind.
  - In den Stationswerten steht, worüber sie fliegt, mit Breite, Länge und ob dort Tag ist. In der ganzen Erde erscheint sie als zweiter, türkiser Punkt in ihrer echten Höhe, dazu ihre Bahn gestrichelt: der Großkreis durch die letzten beiden Antworten. Daneben sieht man, wie weit unsere Bahn von der echten abliegt.
  - Zwischen zwei Antworten läuft sie auf dem Großkreis durch die letzten beiden Punkte weiter. Als Zeit gilt die eigene Uhr beim Empfang, nicht der Zeitstempel des Dienstes: Geht die Uhr des Rechners ein paar Minuten falsch, wäre die Antwort sonst sofort zu alt. Nach zwei Minuten ohne Antwort steht „nicht erreichbar“ da.
- **Die Wolken von heute, auf Wunsch.** Die Wolken der Karte sind eine Aufnahme der NASA, schön, aber nicht das Wetter von heute. Unter Stationswerte lässt sich einschalten, dass ORBIT alle drei Stunden eine Wolkenkarte der ganzen Erde lädt. Sie kommt von Live Cloud Maps (clouds.matteason.co.uk), gerechnet aus Satellitendaten von EUMETSAT, 2048 × 1024 Punkte, gut 400 Kilobyte. Der Dienst erlaubt Browsern die Antwort.
  - Sie ist ein Infrarotbild: Hell ist, was kalt ist. Das sind die hohen Wolken, aber auch klare Luft über kühlem Meer, und in hohen Breiten ist fast alles hell. Heute früh war zwischen 50 und 60 Grad die Hälfte der Punkte heller als 0,84, in der Aufnahme der NASA als 0,33. So eingesetzt läge über Europa und dem Südpolarmeer eine geschlossene weiße Decke.
  - Deshalb gleicht ORBIT die Helligkeit je Breitenband an die Verteilung der Aufnahme an: in 64 Bändern je dieselbe Rangfolge, weich dazwischen. Bewölkt ist dann, was dort heute am kältesten ist, und zwar so viel, wie dort üblich ist. Jenseits von 62 Grad geht es bis 72 Grad in die Aufnahme über, denn dort sehen die Satelliten schräg und lückenhaft, und die Karte hat Randfehler.
  - Aus demselben Bild kommen die Gewitterzellen, im Infrarot die kältesten Türme. Die Scheibe unter der Station und die ganze Erde werden sofort neu gerechnet.
  - Ausgeschaltet geht keine Anfrage hinaus, im Hintergrund auch nicht. Nach einem Fehler kommt der nächste Versuch nach zehn Minuten, und bis dahin bleiben die zuletzt geladenen Wolken. Wieder aus kehrt die Aufnahme bildpunktgenau zurück.
  - In den Stationswerten steht, seit wann sie gelten, etwa „von heute · 06:24“, und die Karte der Erde sagt, woher sie kommen.
- **Die Erde von gestern, auf Wunsch.** Blue Marble ist ein Bild ohne Wolken aus vielen Monaten, die Wolken darauf eine andere Aufnahme. Unter Stationswerte lässt sich einschalten, dass ORBIT stattdessen die Erde zeigt, wie sie gestern wirklich aussah: das Echtfarbenbild des Satelliten Suomi NPP (VIIRS), ein Mosaik aus vierzehn Überflügen, jeder um halb zwei Ortszeit. Es kommt vom Kartendienst der NASA (GIBS, als WMS), 4096 × 2048 Punkte, gut zwei Megabyte, einmal am Tag. Die NASA erlaubt Browsern die Antwort.
  - Gestern, weil das Bild von heute erst im Lauf des Tages voll wird: Genommen wird der Tag, der vor dreißig Stunden war. Am 23. September um 08:30 UTC ist das der 22.
  - Wolken und Land sind darin, wie sie waren. Auf der Tagseite liegen dort keine zweiten Wolken darauf und keine Wolkenschatten; nachts gelten weiter die Wolkenkarte für Mondlicht und Gewitter, auf Wunsch die von heute. Die Scheibe unter der Station zeigt dasselbe Bild.
  - Wo der Satellit nichts sah, in der Polarnacht und in Lücken zwischen den Bahnen, ist das Bild schwarz. Dort bleibt Blue Marble mit den Wolken der Aufnahme. Echtes Meer ist nie so dunkel: Im hellsten Kanal hat es mindestens 26, gemessen am Bild vom 22. September. Die Grenze liegt weich zwischen 14 und 26. Am 22. September galt das Bild für 85 % der Erde; der Rest lag fast ganz jenseits von 70 Grad.
  - Die Tönung für den Blick aus dem Orbit, gedacht für die kräftige Blue Marble, bleibt auf dem Echtfarbenbild zu einem Drittel.
  - Ein leeres Bild wird verworfen, das letzte gute bleibt. Nach einem Fehler oder einem leeren Bild kommt der nächste Versuch nach zehn Minuten. Ausgeschaltet geht keine Anfrage hinaus, und Blue Marble kehrt bildpunktgenau zurück.
  - In den Stationswerten steht der Tag, etwa „von gestern · 22.09. · Suomi NPP“, und der Text zur Erde sagt, woher die Tageskarte kommt.
- **Satellitenbilder, auf Wunsch: die Kugel als Karte.** Mit dem Knopf unten in der Zoomleiste der ganzen Erde, oder unter Stationswerte, wird die Kugel zur Karte wie bei Google Earth. Die Bilder kommen von Esri World Imagery, derselben Quelle, die God's Eye View ohne Schlüssel nimmt: Kacheln von 256 × 256 Punkten im Netz von Web-Mercator, bis Stufe 16. Dort ist ein Punkt am Äquator 2,4 Meter breit, in München 1,6.
  - Solange die ganze Kugel zu sehen ist, geht keine Anfrage hinaus. Welche Stufe gilt, folgt aus den Metern je Bildpunkt in der Blickmitte. Ab Stufe 5 blenden die Kacheln über die Karte der NASA, die dort ähnlich fein ist. Ab Stufe 7 gehen die Wolken, bei Stufe 10 sind sie weg, samt ihren Schatten.
  - Die Kacheln liegen in einem Mosaik im Grafikspeicher: quer 16 × 10 Plätze, 4096 × 2560 Punkte, hochkant wie auf dem Handy 8 × 16. Jede Kachel hat ihren festen Platz aus Spalte und Zeile. Beim Verschieben bleiben die liegen, die weiter gebraucht werden, auch über die Datumsgrenze. Dafür muss die Zahl der Spalten eine Zweierpotenz sein. Der Schattierer rechnet jeden Punkt der Kugel nach Web-Mercator um und schlägt ihn im Mosaik nach; zum Rand des Fensters hin wird es weich.
  - Welche Plätze ihre Kachel schon haben, hält eine winzige zweite Textur fest. Ein leerer Platz zeigt die Karte der NASA, nicht die Kachel, die vorher dort lag.
  - Angefragt wird nur, was auf dem Schirm liegt: Ein Raster von Punkten über den ganzen Schirm sagt, welche Kacheln das sind. Dazu kommt ein Rand als Vorrat fürs Verschieben, der erst nach allem Sichtbaren kommt. Das Fenster selbst ist viel größer als der Schirm; beim Hineinzoomen bis Stufe 12 wären es sonst rund 700 Kacheln statt gut 400. Wer schnell durch die Stufen zoomt, lässt die übersprungenen fallen, bevor sie angefragt werden.
  - Höchstens acht Anfragen zugleich, die nächsten zur Blickmitte zuerst. 400 Kacheln bleiben im Speicher, das am längsten Ungebrauchte geht zuerst. Wer zurückkehrt, lädt nichts neu; aus dem Speicher kommen je Bild höchstens zwölf auf den Grafikchip, damit nichts ruckelt.
  - Zoomen geht bis 6000-fach, immer auf den Punkt unter dem Zeiger. Ziehen verschiebt: Was man greift, bleibt unter dem Finger. Beides ist geschlossen gerechnet statt genähert, in Breite und Länge um das Oben des Bildes als Pol. Der Ort unter dem Zeiger bleibt so auf Tausendstel Bildpunkte stehen, auch an der ganzen Kugel. Nahe am Rand, wo ein Ort nicht hinkommt, ohne dass sich das Bild verdreht, wird es weich, statt dass die Kugel um den Pol wirbelt.
  - In der Zoomleiste steht, wie breit der Ausschnitt ist, etwa „39 km“. Der Knopf mit dem Pfeil im Kreis bringt erst zur ganzen Kugel zurück, dann zur Station. Der Text zur ganzen Erde nennt Stufe und Auflösung.
  - **Der Kompass.** Die freie Kugel übernimmt die Drehung, mit der sie gerade gezeigt wurde, und Norden steht dann nicht unbedingt oben. Oben in der Zoomleiste zeigt eine Nadel, wo Norden liegt: die Richtung zum Pol in der Ebene, die die Kugel in der Blickmitte berührt. Antippen dreht das Bild um die Blickmitte, bis Norden oben ist, schnell am Anfang und sanft am Ende. Der Ort in der Mitte bleibt dabei, wo er war. Direkt über einem Pol gibt es kein Norden, dann tut der Knopf nichts und sagt das.
  - Esri verlangt eine Quellenangabe. „Powered by Esri · Bilder: Esri, Maxar, Earthstar Geographics, GIS User Community“ steht unten links, sobald Kacheln zu sehen sind, auf dem Handy in zwei Zeilen.
  - **Die Beschriftung.** Wie bei Google Earth stehen über den Bildern die Namen der Länder, Städte, Orte, Seen und Parks, dazu die Grenzen bis zu den Landkreisen. Sie kommen als durchsichtige Kacheln im selben Netz von Esri („World Boundaries and Places“, aus Daten von HERE, Garmin und OpenStreetMap), ohne Schlüssel und mit offener Antwort für Browser. Voreingestellt ist sie an; unter Stationswerte lässt sie sich ausblenden, und das wird gemerkt.
    - Jede Schrift wird vor dem Hochladen über ihr Bild gemalt. Wie viel Schrift einen Punkt deckt, steht im Alphakanal. So kann der Schattierer sie aus sich selbst leuchten lassen, wie bei Google Earth: bei Nacht und in der Dämmerung so lesbar wie am Mittag, über Wolken und Luft. Nur wo die Schrift einen Punkt fast ganz deckt; an ihren weichen Kanten bleibt das beleuchtete Bild, sonst schiene dort nachts der Tag durch. Über den scharfen Nachtlichtern steht dann „München“ auf dem hellen Fleck.
    - Die Schrift in den Kacheln ist für Schirme gemacht, auf denen ein Kachelpunkt ein Bildpunkt ist. Auf einem Retina-Schirm wären die Namen halb so groß und kaum zu lesen. Dort kommt die Schrift deshalb eine Stufe gröber, doppelt so groß, und auf dem Handy zwei Stufen. Eine gröbere Kachel deckt vier oder sechzehn Bildkacheln, und jede wird nur einmal geholt. Ändert sich die Schärfe des Schirms, etwa auf einem zweiten Bildschirm, kommen die Schriften neu.
    - Fehlt eine Schrift, bleibt das Bild, ohne Fehler. Bis zum nächsten Einschalten wird sie nicht noch einmal angefragt.
    - Unten links steht dann zusätzlich „Beschriftung: Esri, HERE, Garmin, © OpenStreetMap contributors, GIS User Community“. Auf dem Handy wird jede Angabe am letzten Komma umbrochen, das noch passt.
  - **Das Relief nach der echten Sonne.** Das Satellitenbild trägt das Licht seiner Aufnahme. Die Satelliten dafür überfliegen jeden Ort gegen halb elf Ortszeit, meist im Sommer. Die Sonne steht dann gut 50 Grad hoch, auf der Nordhalbkugel im Südosten. Morgens und abends sieht die echte Landschaft ganz anders aus: Die der Sonne zugewandten Hänge leuchten, die abgewandten liegen im Schatten. Genau das rechnet ORBIT dazu.
    - Die Höhen sind die Terrain Tiles von Mapzen bei AWS (Open Data), ohne Schlüssel und mit offener Antwort für Browser. Sie liegen im selben Netz wie die Bilder, eine Stufe gröber, also mit etwa der Auflösung eines halb so feinen Bilds. Eine Höhenkachel deckt vier Bildkacheln und wird nur einmal geholt. Die Höhe steckt in den Farben: Rot × 256 + Grün + Blau / 256 − 32768 Meter. Entpackt wird ohne Farbanpassung, denn jede Umrechnung zerstörte die Höhen.
    - Daraus wird je Punkt die Steigung nach Osten und nach Norden, gestaucht in zwei Bytes: flache Hügel bleiben fein aufgelöst, und doch passt eine Wand hinein. Unter dem Meer zählt der Meeresspiegel, sonst bekäme das Wasser die Form des Meeresbodens und jede Küste eine Klippe. Das Relief liegt in einem zweiten Mosaik mit denselben Plätzen, halb so fein.
    - Der Schattierer rechnet, wie viel Licht ein Hang jetzt bekommt und wie viel damals, beides im Verhältnis zu flachem Boden: ein Drittel Himmelslicht von überall, der Rest direkt von der Sonne. Mit diesem Verhältnis, etwas verstärkt (hoch 1,3), wird das Bild heller oder dunkler. Flacher Boden bleibt genau wie ohne Relief. Mittags ändert sich wenig, morgens und abends viel.
    - **Schlagschatten.** Bei tiefer Sonne, unter gut 27 Grad, werfen die Berge Schatten ins Tal dahinter; dort bleibt nur das Himmelslicht. Der Schattierer schickt von jedem Punkt einen Strahl zur Sonne, in 24 immer längeren Schritten von einem Punkt des Reliefs bis gut drei Kacheln weit, und fragt, ob irgendwo ein Berg höher ist als der Strahl dort. Der Rand ist weich wie der Halbschatten der Sonne. Dafür steht neben der Neigung auch die Höhe im Relief-Mosaik, in zwei Bytes: ganze 35 Meter und der Rest in 255steln davon, bis 8925 Meter. Beide Teile lassen sich getrennt weich dazwischen rechnen, die Summe bleibt richtig. Höher am Himmel sind die Schatten kurz und stecken schon im Bild.
    - Dafür braucht der Schattierer eine neunte Textur. WebGL verspricht nur acht, fast jeder Grafikchip kann sechzehn; mit acht bleibt das Relief aus.
    - Voreingestellt an, unter Stationswerte abschaltbar, gemerkt. Unten links steht dann „Relief: Mapzen Terrain Tiles (AWS) · USGS, Copernicus EU-DEM, NOAA u. a.“, die ganze Liste der Quellen steht in der Hilfe.
    - Ein Umschalter versucht nur seine eigenen Daten neu: Wer das Relief ausschaltet, holt keine fehlenden Schriften nach, und umgekehrt.
  - Ausgeschaltet geht keine Anfrage mehr hinaus. Der Zoom geht auf 2,4 zurück, man bleibt über demselben Ort, und Ziehen verschiebt weiter.
  - **Scharfe Nachtlichter.** Die Karte der Stadtlichter hat knapp zehn Kilometer je Punkt. Hineingezoomt wird eine Stadt darauf zu einem weichen orangen Fleck, bei tiefem Zoom über den ganzen Schirm. Mit Satellitenbildern holt ORBIT deshalb für den Ausschnitt ein Bild aus Black Marble 2016 vom Kartendienst der NASA (GIBS, als WMS): gut einen halben Kilometer fein, ohne Schlüssel, gemeinfrei, mit offener Antwort für Browser.
    - Gefragt wird erst ab einem Ausschnitt unter 3000 Kilometern Breite, nur wenn ein Teil davon auf der Nachtseite liegt, und erst, wenn der Blick eine halbe Sekunde stillsteht. Unter 1500 Kilometern gilt die feine Karte ganz.
    - Das Bild ist so fein wie der Schirm, höchstens so fein wie die Daten und höchstens 2048 Punkte je Seite, mit einem Rand von 15 % für kleines Verschieben. Es liegt in Länge und Breite; ein älteres bleibt dort richtig, wo es den Ausschnitt noch deckt. Über die Datumsgrenze reicht es nicht, dort endet es.
    - Genommen werden nur die Lichter: warm und hell. Das Gelände ist bei Black Marble mondbeschienen blaugrau und der Schnee bläulich, beides bleibt dunkel. Dann wird leicht geglättet, sonst werden einzelne Punkte beim Vergrößern zu Kreuzen und Treppen, und weich gesättigt. Linear verstärkt, wie zuerst, brannten Poebene und Ruhrgebiet weiß aus.
    - Unten links steht dann „Nachtlichter: NASA Black Marble (GIBS)“.
  - Die Kacheln tragen schon das Licht ihres Aufnahmetags, meist vormittags bei hoher Sonne. Noch einmal beleuchtet, wären sie doppelt dunkel. Deshalb zählt für sie das Licht im Verhältnis zu dem bei der Aufnahme: bei hoher Sonne so hell wie aufgenommen, bei tiefer dunkler, hinter dem Tagesrand dunkel wie der Rest der Karte. Von der Tönung für den Blick aus dem Orbit bleibt beim tiefen Zoom ein Zehntel. Vorher kam München um ein Sechstel dunkler und grauer heraus als die Kacheln selbst.
- **Das Regenradar, auf Wunsch.** Unter Stationswerte → LIVE lässt sich einschalten, dass auf der ganzen Erde steht, wo es gerade regnet oder schneit. Die Daten kommen von RainViewer, zusammengesetzt aus den Wetterradaren vieler Länder, alle zehn Minuten neu, ohne Schlüssel und mit offener Antwort für Browser.
  - Geholt werden nicht die bunten Bilder, sondern die Messwerte (Farbtafel 255). Im Rot steht die Reflektivität des Radars in dBZ plus 32, im Blau, ob es Schnee ist, und im Alpha, ob dort überhaupt ein Radar hinsieht (255) oder nicht (63). So malt ORBIT die Farben selbst und unterscheidet „trocken“ von „kein Radar“. Nachgeprüft an allen 16 Kacheln der ganzen Erde, in beiden Farbtafeln: Jeder dBZ-Wert hat im bunten Bild des Dienstes genau eine Farbe, 108 Paare. Kommt einmal nur noch das bunte Bild, liest ORBIT die Werte über diese Tafel aus den Farben zurück; dann heißt es „kein Regen gemessen“ statt „trocken“. Die übrigen Farbtafeln liefert der Dienst inzwischen alle als dasselbe Blau.
  - Die Farben sind die üblichen Stufen: hellblau Niesel, blau leichter Regen, grün mäßiger (ab gut 20 dBZ, ein bis vier Millimeter je Stunde), gelb ab 35 starker, orange, rot ab 48 Starkregen, violett ab 55, wo Hagel sein kann. Schnee weiß bis lila. Sichtbar wird es ab 12 dBZ, darunter ist es Dunst oder Störung.
  - Nachts leuchtet der Regen gedämpft aus sich selbst, wie die Beschriftung, die über ihm bleibt.
  - Im Grafikspeicher liegt ein Fenster aus 4 × 4 Kacheln zu 512 Punkten. Aus der Ferne ist das Stufe 2, die ganze Erde in 16 Kacheln, knapp 20 Kilometer je Punkt am Äquator. Hineingezoomt, also mit Satellitenbildern, wird es feiner, bis Stufe 6: gut 800 Meter je Punkt in Mitteleuropa. Feiner rechnet der Dienst nur hoch; das kann der Grafikchip selbst. Das Fenster wandert erst, wenn die Blickmitte in seine äußere Reihe kommt.
  - Kommt ein neues Bild, bleiben die Kacheln des alten stehen, bis ihre Nachfolger da sind; es gibt kein Loch. 40 Kacheln bleiben im Speicher, je Kachel ein Byte je Punkt.
  - Tippst du auf einen Ort oder fliegst hin, steht in der Karte, wie stark es dort regnet: „starker Regen, etwa 13 mm pro Stunde“. Die Menge nach Marshall und Palmer (Z = 200 R^1,6), eine Faustformel für Regen; bei Schnee und ab 55 dBZ steht deshalb keine Zahl. Kommen feinere Kacheln, solange die Karte offen ist, zieht die Zeile nach. Über dem Meer und in weiten Teilen Afrikas und Asiens steht „kein Radar hier“.
  - **Regen als Türme.** Jede Regenzelle steht als Säule auf der Erde, so hoch, wie sie stark ist: Niesel bleibt flach, ab 55 dBZ die ganze Höhe. Echt reichen Gewitter gut 12 Kilometer hoch; aus der Ferne wäre das ein halber Bildpunkt. Deshalb sind die Türme überhöht: höchstens 26 Bildpunkte, höchstens 0,03 Erdradien (rund 190 km), nah heran nie weniger als echt.
    - Gerechnet wird je Bildpunkt entlang des Blicks: von oben durch die Schale in der größten Höhe bis zum Boden, in dreizehn Schritten; an der ersten Säule wird dreimal halbiert, damit die Kanten glatt werden statt in Stufen. Kostet ein Bild der Kugel mehr als 120 Millisekunden, rechnet offenbar kein Grafikchip, und es sind halb so viele Schritte. Der erste Punkt, der in einer Säule liegt, ist das, was man sieht: ihr Dach, wenn der Schritt davor darüber lag, sonst ihre Wand. Alle Schritte laufen immer, ohne Abbruch; nur so bleiben die Verkleinerungsstufen der Textur überall richtig.
    - Das Dach ist nach seiner Steigung beleuchtet, die Wand nach ihrer Richtung zur echten Sonne und unten dunkler. Wände sind dicht, Dächer so durchscheinend wie der Regen.
    - Der Schatten fällt entlang der Sonne: Von jedem Punkt am Boden prüfen bis zu sechs Schritte zur Sonne, ob eine Säule den Strahl schneidet. Bei tiefer Sonne werden die Schatten lang.
    - Von oben gesehen, in der Mitte der Kugel, sieht man nur die Dächer. Zum Rand hin und bei geneigtem Blick stehen die Türme sichtbar auf.
    - Kosten in reiner Software-Rasterung: ein Bild der ganzen Erde mit echtem Radar 541 statt 328 Millisekunden, mit zwölf Schritten waren es 668. Mit Grafikchip sind es ein paar Millisekunden.
  - **Der Regenfilm.** Unten auf der Erde steht ein Knopf ▶ mit der Uhrzeit des Bilds und dreizehn Strichen: Er spielt die letzten zwei Stunden im Zeitraffer ab, alle zehn Minuten ein Bild, knapp drei je Sekunde, das neueste etwas länger. So sieht man, wohin der Regen zieht. Geholt werden nur die Kacheln des Fensters, das gerade im Grafikspeicher liegt, für die zwölf älteren Bilder; die des neuesten liegen schon da. Im Speicher liegen sie gepackt, je Lauf gleicher Werte zwei Bytes: Mit echten Daten über Europa waren es 208 Kacheln in 1,9 MB statt 52 MB. Während des Films steht unter Stationswerte „Film · 14:10 · 1 von 13“. Fehlt eine Kachel, bleibt die des Bilds davor stehen. Der Knopf hält an und bringt das neueste Bild zurück; der Film endet auch, wenn die Erde zugeht, das Radar aus geht oder das Fenster wandert. Eine neueste Kachel, die während des Films kommt, wartet bis zu seinem Ende. In der Palette heißt er „Regenfilm“.
  - **Zuhause.** In der Karte eines Orts steht „⌂ Als Zuhause merken“. Dann behält die Station diesen Ort im Blick, auch bei geschlossener Erde und im Hintergrund:
    - Unter Stationswerte steht eine Zeile wie „München · trocken · Regen in etwa 30 min · zieht aus Westen, 59 km/h“ oder „mäßiger Regen · hört in etwa 40 min auf“. Auf der Erde steht ein kleines Haus mit dem Namen, bei Regen mit einem Tropfen.
    - Einmal je Ereignis eine Mitteilung und ein Eintrag im Bordbuch: „Regen in München in etwa 30 Minuten“, wenn er in einer halben Stunde da sein dürfte, und „Es regnet in München“, wenn er angefangen hat. Die erste Rechnung nach dem Start meldet nichts.
    - Die Vorhersage ist eine Verschiebung, kein Wettermodell. Um das Zuhause liegt ein Ausschnitt von 192 × 192 Punkten der Stufe 4, gut drei Kilometer je Punkt in Mitteleuropa, also rund 600 × 600 km. Aus dem Bild von vor zwanzig Minuten und dem neuesten wird die Verschiebung bestimmt, bei der beide am besten übereinstimmen (normierte Kreuzkorrelation, bis 16 Punkte in jede Richtung, gut 150 km/h). Dieselbe Bewegung wird eine Stunde weitergedacht, in Schritten von zehn Minuten, mit einem Rand von einem Viertel des Wegs.
    - Bei Gleichstand gewinnt die kleinste Verschiebung; ein Maximum am Rand der Suche zählt nicht, und kaum besser als gar keine Bewegung heißt: es steht. Ohne diese Regeln meldete ein Feld ohne Struktur 224 km/h.
    - Zellen, die wachsen, zerfallen oder neu entstehen, sieht die Rechnung nicht. Für eine halbe Stunde passt das bei Fronten meist, bei Gewittern oft nicht; deshalb steht immer „etwa“ davor.
    - Dafür fragt ORBIT alle fünf Minuten den Index und holt je Bild höchstens vier Kacheln der Stufe 4, von den letzten drei Bildern. RainViewer erfährt dabei, in welchem Gebiet von gut 1500 km das Zuhause liegt. Im Hintergrund, wo das Bild stillsteht, übernimmt ein Zeitgeber; der Browser drosselt ihn auf einmal je Minute.
    - „⌂ Zuhause · nicht mehr merken“ vergisst den Ort; dann geht bei geschlossener Erde nichts mehr hinaus. Gemerkt wird er mit den übrigen Einstellungen.
  - Mit dem Radar blitzt es nachts in den echten Gewittern: Aus den 16 Kacheln der Stufe 2 werden die Kerne ab 45 dBZ, einer je halbes Grad. Wo kein Radar hinsieht, bleiben die Gewitter aus der Wolkenkarte.
  - In den Stationswerten steht „Radar von 15:40 · nass auf 8 % der Radarfläche“, hineingezoomt „im Ausschnitt“. Unten links steht „Regenradar: RainViewer“, solange es zu sehen ist.
  - Gefragt wird nur, solange die ganze Erde offen ist: alle fünf Minuten der Index (zwei Kilobyte), Kacheln nur, wenn das Bild neu ist oder der Blick ein neues Fenster braucht, höchstens sechs zugleich. Adresse und Pfad der Kacheln kommen aus der Antwort und werden streng geprüft: nur https und nur Rechner unter rainviewer.com. Ausgeschaltet geht keine Anfrage hinaus, und der Speicher wird frei.
  - Dafür braucht der Schattierer eine zehnte Textur. WebGL verspricht acht, fast jeder Grafikchip kann sechzehn; mit weniger als zehn steht in den Stationswerten, dass es nicht geht.
  - Die Scheibe unter der Station bekommt kein Radar. Sie ist der Blick aus dem Fenster, und bunte Flecken gehören nicht hinein.
  - Kosten: In reiner Software-Rasterung braucht ein Bild der ganzen Erde mit Radar 315 statt 269 Millisekunden. Eine Kachel zu lesen und hochzuladen kostet je gut zwei Millisekunden, die Gewitterkerne der ganzen Erde 17.
- **Rückfall.** Fehlt eines der Bilder, kann der Browser kein WebGL oder geht der Grafikkontext verloren, zeichnet ORBIT die gerechnete Erde wie bisher. Solange die Karten laden, wartet die Seite bis zu zwei Sekunden mit der Erde. So zeigt sie nicht erst die gerechnete und springt dann um.
- **Kosten.**
  - Neu gemalt wird nur, wenn sich die Scheibe weit genug gedreht hat. Das regelt dieselbe Schwelle wie vorher beim Durchziehen.
  - In reiner Software-Rasterung kostet ein Stand 25–47 Millisekunden. Die Bildrate bleibt bei 58–62 Bildern je Sekunde, vorher 49–62. Mit Grafikchip kostet es so gut wie nichts.
  - Die Wolkendecke als Licht wird nur gemalt, wenn Mond oder Nacht sie brauchen.

## Die Nacht unter der Station

- **Gewitter.** Auf jedem Nachtflug zucken unten die Wolken auf. Die Zellen sitzen in den dicksten Wolken der Erdscheibe, bei der echten Erde in denen der Karte, und ziehen mit dem Boden vorbei. Ein Blitz leuchtet die echte Wolkendecke von innen aus — beim Backen entsteht dafür ein eigenes Bild der Wolken —, mit ein bis vier Folgeschlägen, weicher in der Wolke, härter zum Boden, und zündet manchmal die Nachbarzelle, sodass das Leuchten über das Wolkenfeld läuft. Über Land und kurz nach Sonnenuntergang blitzt es am meisten; bei Tag, angehalten und neben der Scheibe nie.
- **Rote Kobolde.** Selten steht über einem starken Schlag zum Boden am Horizont für einen Augenblick ein roter Kobold (Sprite) — eine Entladung nach oben bis fast in neunzig Kilometer Höhe, in echter Größe, mit roter Krone und violetten Ranken. Einmal in zehn Minuten ein Eintrag im Bordbuch.
- **Wolken im Mondlicht.** Die Nachtseite war bis auf die Städte schwarz — so sieht sie nur bei Neumond aus. Steht der Mond, liegen die Wolken grau-blau im Licht, und bei Vollmond erkennt man jede Front. Die Helligkeit folgt der Mondphase der Szene mit einer hohen Potenz: Der Halbmond ist nur rund ein Zehntel so hell wie der Vollmond. Die Städte liegen weiterhin obenauf. Die Phase beginnt beim Start mit der echten von heute und läuft dann mit der gerafften Zeit weiter. Vorher stand sie fest auf 118 Grad.
- **Sternschnuppen unter der Station.** Ein Meteor verglüht in achtzig bis hundert Kilometern Höhe, weit unter der Station. Er zog bisher durch das obere Bilddrittel, mitten durch die Sterne, und auch bei Tag — obwohl der Kommentar im Code das Richtige sagte. Jetzt nur nachts, über der dunklen Erde oder in der Leuchtschicht am Horizont, grün vom Sauerstoff wie auf dem bekannten Bild einer Perseide von der Station.
- **Die Meteorströme des Jahres.** In den Tagen um die großen Ströme gibt es mehr Sternschnuppen. Das sind die Quadrantiden, Lyriden, Eta-Aquariiden, Perseiden, Orioniden, Leoniden und Geminiden. Gerechnet wird mit ihrer Rate und einer Glocke um den Tag des Höhepunkts. Um die Geminiden sind es sechzehnmal so viele wie ohne Strom, um die Perseiden elfmal. Läuft einer, steht es im Bordbuch und in den Stationswerten.
- **Das Nachthimmelsleuchten ohne Nähte.** Das grüne Band über der Kante wird in 26 Streifen gezeichnet, die sich um einen Bildpunkt überlappten; weil das Leuchten addiert wird, stand an jeder Naht ein doppelt heller Strich — eine Linealskala entlang des Horizonts. Gemessen lagen die Nähte 36 (Desktop) und 53 (Handy) Helligkeitsstufen über ihrer Umgebung, jetzt 0,7.
- **Der Boden zieht flüssig vorbei.** Die Erdscheibe wurde erst neu zusammengesetzt, wenn der Boden 22 Bildpunkte weiter war; gemessen sprang er damit um 45 Bildpunkte gut einmal je Sekunde. Jetzt hängt die Schwelle an dem, was das Zusammensetzen auf dem Gerät wirklich kostet — gemessen als Unterschied der Bilddauer mit und ohne, denn die Aufrufzeit sagt nichts, der Browser zeichnet später. Höchstens ein Zwölftel der Zeit darf es fressen.

| Software-Zeichnen, ohne Grafikchip | Sprung vorher | nachher | Bilder/s vorher | nachher |
|---|---|---|---|---|
| Handy 390 × 844, dreifach | 22 px | 1,1 px | 60 | 59 |
| Desktop 1440 × 900, einfach | 45 px | 3,8 px | 59 | 55 |
| Desktop 1440 × 900, doppelt | 23 px | 15 px | 23 | 21 |

## Der Lebenserhalt

Die Station hat einen Stoffwechsel, und er hängt an derselben Zahl wie das Licht — an der Stelle im Umlauf.

- **Strom**: acht Flügel, 84 bis 120 kW im Sonnenlicht; 24 Batterieeinheiten mit 96 kWh nutzbar; Grundlast 74 kW plus das, was die Crew gerade anstellt. Sinkt der Ladestand, gehen in den Modulen die Lichter aus — das sieht man von außen.
- **Luft**: ein Mensch atmet 1 kg CO₂ am Tag aus. Steigt der Wert über 3,4 mmHg, läuft der Filter an und bläst ab — das Ventil geht auf, *weil* der Wert gestiegen ist.
- **Wärme**: im Vakuum kann Wärme nur abgestrahlt werden. Der Vorlauf schwingt im Takt des Umlaufs, und je wärmer der Kreis läuft, desto weiter werden die Paneele aufgedreht.
- **Bahn**: sinkt, wird angehoben. Kommt Schrott zu nah, gibt es eine Warnung, dann eine Bahnrechnung, dann einen Vorbeiflug oder einen Ausweichschub.
- **Funk**: Kontakt über wechselnde Bodenstationen, mit Lücken. Die Schüssel fährt mit fester Rate nach — ein Schrittmotor beschleunigt nicht.

Die Anzeige zeigt das mit einer Pulskurve der Strombilanz, dem längsten laufenden Einsatz und einer **Umlaufuhr**: Erde, Bahn und Schattenkegel maßstabsgetreu. Die Bahn liegt nur sieben Prozent über der Kugel, und der Schatten deckt 139,6 von 360 Grad ab.

Das **Bordbuch** — Frachter, Erdschatten, Einschläge, Ausweichschübe, Aus- und Einstieg, Berichte der Unteragenten — steht in den Stationswerten mit den fünf jüngsten Einträgen und hat einen eigenen Reiter im Log mit allen vierzig. Das Log sagt, was ein Agent geantwortet hat; das Bordbuch, was an der Station geschehen ist. Zwei Erzählungen, ein Fenster.

## Umlauf und Zeit

92 Minuten, davon 59 Prozent Sonne. Der Übergang dauert echte 43 Sekunden. Gerafft läuft ein Umlauf in 7:40; die Uhr lässt sich anhalten oder bis auf das Zwölffache beschleunigen. Angehalten steht wirklich alles still — auch der Stoffwechsel.

## Bedienung

Ziehen und Zoomen mit Maus, Rad und Fingern; weiter heraus, als der Zoom reicht, kommt die ganze Erde. Auf der Tastatur: L Log, C Crew, H Hintergrund, B Brücke, T Stationswerte, K Kinomodus, R Rundgang, E ganze Erde. **Pfeiltasten schieben** (ein Achtel der Bildbreite, mit Umschalt ein Viertel), Plus und Minus zoomen, **N und P springen von Astronaut zu Astronaut**, **W zum Nächsten, der auf dich wartet**, Leertaste stellt die Kamera zurück, Escape schließt. Tab springt ebenfalls durch die Crew, aber nur solange nichts anderes den Fokus hat — Tab ist die Taste, mit der man überhaupt erst zu den Knöpfen kommt.

**Die Befehlspalette.** ⌘K (Strg+K) öffnet sie, auch aus einem Textfeld heraus; außerhalb von Textfeldern auch der Schrägstrich. Sie ist eine Suche über alles, was sonst hinter Knöpfen liegt:
- die Crew; Enter fährt zur Figur und öffnet sie,
- Aktionen: zum Nächsten, der wartet, Rundgang, ganze Erde, Kamera zurück, Vorführung,
- die Blenden oben, mit ihrer Taste daneben,
- die Schalter unter Stationswerte, mit ihrem Zustand,
- Orte: 1822 Städte und 242 Länder, deutsch und englisch („Munich“ findet München), die größere zuerst, höchstens zwölf,
- die 42 Hintergründe, aber erst, wenn man nach ihnen sucht.

**Ortssuche und Flug.** Enter auf einen Ort fliegt die ganze Erde dorthin, wie bei Google Earth:
- über den Großkreis, weich an- und auslaufend, 1,2 bis 3 Sekunden je nach Weite;
- bei weiten Flügen ein Stück hinaus, höchstens so weit, dass Start und Ziel zugleich zu sehen wären (München nach Tokio: von 220-fach auf 1,6-fach und wieder hinein);
- unterwegs dreht sich Norden nach oben: Das Oben vom Start wird auf dem Großkreis mitgeführt und dabei gleichmäßig um die Blickachse zum Norden am Ziel gedreht. Früher wurden die beiden linear gemischt. Zeigten sie fast gegeneinander, ging die Mischung durch null, und das Bild kippte mitten im Flug ruckartig, mit gut dem Dreifachen der Geschwindigkeit des Flugs. Die Mitte dreht jetzt um eine Achse statt als Kugel-Interpolation, die beim Flug zum genauen Gegenpunkt durch null geteilt hätte.

**Die Station hinter der Erde.** In der frei gedrehten Kugel kann die Station hinter der Erde liegen, etwa nach einem Flug nach Europa, während sie über dem Indischen Ozean ist. Früher schien ihr Punkt dann durch die Erde hindurch. Er stand samt „Unter uns: Indischer Ozean“ mitten auf dem Mittelmeer. Jetzt:
- Liegt sie hinter der Kugel, steht knapp außerhalb von deren Rand ein kleiner Zeiger, dort, wo sie wieder hervorkäme: „Station hinter der Erde · antippen: zurück“.
- Liegt sie vorn, aber außerhalb des Schirms (tief hineingezoomt), steht der Zeiger am Rand des Schirms und heißt nur „Station“.
- Antippen fliegt zurück, und zwar nicht zu einem festen Punkt: Ziel ist der Blick, der der Station folgt, in jedem Bild neu, denn sie fliegt weiter. Am Ende geht der Flug ohne Sprung in die folgende Kamera über.

Am Ziel steht ein pulsierender Ring mit dem Namen, und die Karte zum Ort geht auf: Land, Koordinaten, Sonnenzeit. Wie nah es geht:
- ohne Satellitenbilder bis 2,4-fach,
- mit ihnen eine Stadt auf gut siebzig Kilometer Bildhöhe,
- ein Land so, dass es drei Viertel der Höhe füllt (Italien 11,8-fach).

Wer zoomt oder greift, hält den Flug an, ohne dass das Bild ans Ziel springt. Die Orte stammen aus Natural Earth (gemeinfrei): alle Städte ab 250.000 Einwohnern, alle Hauptstädte und alle Orte in Deutschland, Österreich und der Schweiz, zusammen 67 kB in der Datei.

Gesucht wird ohne Groß- und Kleinschreibung und ohne Akzente: „bru“ findet die Brücke und hebt „Brü“ hervor. Jedes Wort muss vorkommen; Treffer im Titel stehen vor denen im Untertitel. Pfeile wählen und laufen oben und unten herum, Enter führt aus, Escape schließt nur die Palette, und der Fokus kehrt dorthin zurück, wo er war. Ein Tipp neben die Karte schließt ebenfalls. Buchstaben in der Suche lösen keine Tastenkürzel aus.

Behoben:
- **R in einem Textfeld.** Der Rundgang wurde vor der Prüfung auf Textfelder abgefragt. Jedes r beim Tippen eines Ordnerpfads fing ihn deshalb an oder beendete ihn und schloss dabei die Brücke, in die man gerade schrieb. Auch Strg/⌘+R war ein Rundgang.
- **Leertaste auf einem Knopf.** Die Leertaste drückt jetzt einen Knopf, zu dem man mit Tab gegangen ist, statt die Kamera zurückzustellen. Nach einem Mausklick, wenn der Knopf den Fokus nur unsichtbar hat, bleibt sie bei der Kamera.
- **Tasten, die schon jemand behandelt hat.** Leertaste und Pfeile auf einer Zeile des Tagesbogens bewegten zusätzlich die Kamera.

**Die Kopfzeile läuft nie über.** Wie breit sie ist, hängt daran, ob jemand wartet, ob die Vorführung läuft, an der Beschriftung des Logs und an der Schrift. Feste Grenzen in Bildpunkten reichten dafür nicht: Zwischen 470 und 770 Punkten Breite lief sie über, sobald jemand wartete, um bis zu 215 Punkte, und der letzte Knopf war nicht mehr zu erreichen. Jetzt misst sie nach und spart Stufe um Stufe:

1. die Beschriftung der Knöpfe (das Symbol bleibt, der Titel beim Draufzeigen sagt dasselbe),
2. die Unterzeile,
3. den Namen,
4. das Logo,
5. zuletzt das Wort neben der Zahl der Wartenden.

Die Zahl und alle sieben Knöpfe bleiben immer. Die Knöpfe animieren auch keine Größen mehr. Nach dem Drehen des Telefons wuchsen sie sonst eine Viertelsekunde lang in ihrer alten Breite nach.

**Das Menü unter Stationswerte** ist nach Gruppen geordnet: KARTE (Satellitenbilder, Beschriftung, Relief), ERDE (Erde von gestern, Wolken von heute) und LIVE (echte ISS, Weltraumwetter). Jeder Schalter hat ein Symbol, seinen Namen, darunter in einer Zeile, was er tut oder gerade tut, und rechts einen Schieber. Vorher standen sieben gleiche Kästen untereinander, und die Aufschrift wechselte zwischen „Beschriftung“ und „Beschriftung aus“: Man musste lesen, um zu wissen, ob etwas an ist. Jetzt ist ein eingeschalteter Schalter getönt, sein Symbol leuchtet, und der Schieber steht rechts. Der Zustand steht zusätzlich in `aria-pressed`, für Vorleseprogramme. Beschriftung und Relief wirken nur mit Satellitenbildern; ohne sie werden Name und Symbol leiser, und darunter steht „wirkt mit Satellitenbildern“. Auf dem Handy ist das Menü etwas breiter, und zu lange Zeilen enden mit Auslassungspunkten statt umzubrechen.

**Die Blenden sind aus Glas.** Oben links fällt Licht ein, unten rechts liegt ein Hauch der Themenfarbe, der Rand schimmert von Weiß über die Themenfarbe nach Violett, und hinter der offenen Blende wird das Bild stärker weichgezeichnet und gesättigt. Sie gleiten beim Öffnen aus der Tiefe und blenden dabei weich ein. Das Kreuz dreht sich beim Draufzeigen. Die Karten zu einem Astronauten und zu einem Bauteil liegen über der laufenden Szene. Durchsichtiges Glas kostete dort die Hälfte der Bildrate, deshalb sind sie undurchsichtig, aber mit denselben Lichtern gemalt.

**Die Schrift ist Inter.** Vorher war es die Systemschrift: auf dem Mac SF Pro, auf anderen Rechnern jedes Mal eine andere, mit anderen Breiten. Jetzt ist Inter eingebettet (Rasmus Andersson, SIL Open Font License 1.1), als variable Schrift von 300 bis 700, nur der lateinische Zeichensatz, 48 KB. Sie gilt für die ganze Oberfläche und alles, was auf der Leinwand geschrieben wird: Namensschilder, Blasen, Quellenangaben, Maßstab. Zeichen außerhalb des Satzes (Pfeile, ⌘, ◆, ₂) kommen aus der Systemschrift. Das einstöckige a und die geschlossene Vier lesen sich in kleinen Größen ruhiger. Die Namen in der Szene stehen halbfett und leicht gesperrt, wie auf einem Anzeigefeld. Gezeichnet wird mit genauen Zeichenbreiten; unter Linux standen sonst Lücken im Wort („Wol ken“). Wie sie auf einem echten Mac aussieht, ist nicht geprüft, nur unter Linux.

**Klicks im Detailfenster gehen nicht mehr verloren.** Die Brücke meldet sich laufend neu, in der Vorführung jede Sekunde, im Mac-Programm alle zweieinhalb. Jedes Mal baute das Detailfenster eines Astronauten seinen ganzen Inhalt neu, auch wenn sich nichts geändert hatte. Fiel ein Neubau zwischen Drücken und Loslassen, ging der Klick verloren, etwa auf einen Unteragenten; gemessen mit 400 ms langem Drücken ging er jedes Mal verloren. Die Hervorhebung unter dem Zeiger flackerte im selben Takt. Jetzt wird der neue Inhalt in den alten eingearbeitet: Wo Art und Klasse eines Elements gleich bleiben, bleibt das Element und bekommt nur neue Texte, Attribute und Handgriffe. Ersetzt wird nur, was wirklich anders gebaut ist. Aufgefallen ist es, weil ein Test unter Last hängen blieb, der Klick fand nie ein ruhiges Element. Dasselbe galt für die Crew-Leiste unten: auch sie wurde jede Sekunde ganz neu gebaut, und ein Test, der auf „Kepler“ tippte, blieb unter Last hängen. Sie wird jetzt ebenso eingearbeitet. Vermutet hatte ich dort auch ein abreißendes Doppeltippen und eine Leiste, die auf dem Handy an den Anfang zurückspringt; beides ließ sich im alten Stand nicht nachweisen, es war nicht so.

**Die Hintergrund-Blende** zieht mit: Schalter, Knöpfe und die 42 Themenkarten sind aus demselben Glas, das gewählte Thema leuchtet in seiner Farbe. Dabei fielen zwei alte Fehler auf. Die beiden Erklärungen unter Tag/Nacht und dem Zeitraffer standen frei in der Blende und fielen auf die Grundschrift zurück, groß und weiß; jetzt sind sie klein und leise wie in den Schaltern. Und der gewählte Zeitraffer (etwa „1×“) sah aus wie die anderen; jetzt ist er in der Themenfarbe getönt.

**Die Kurzanleitung klappt auf.** Jeder Abschnitt ist eine nummerierte Karte. Zu zeigt sie den Titel und den ersten Satz, auf den ganzen Text; sie gleitet dabei auf die echte Höhe des Texts. Der erste Abschnitt ist offen. Beim erklärten Bauteil steht der eine Satz groß, darunter der Absatz und die Zahlen in einer eigenen Karte „IN ZAHLEN“. Alle Tönungen folgen dem gewählten Farbthema.

Bei vielen Astronauten greifen zwei Grenzen: höchstens elf Namensschilder (auf schmalen Schirmen fünf), sortiert nach Zustand, die verfolgte Figur fällt nie heraus; und wo sich mehrere einen Arbeitsplatz teilen müssen, rücken sie quer zur Fläche auseinander statt übereinander zu stehen.

## Tempo

Alles Unbewegliche wird einmal in ein Bild gebacken und danach nur noch kopiert, gestuft nach einer festen Auflösungsleiter mit Hysterese. Kopiert wird streifenweise und nur das, was auf dem Schirm landet.

Die beweglichen Teile werden **gedreht gebacken**. Das ist der Trick hinter der Geschwindigkeit: ein Bild, das beim Kopieren nur noch gestaucht und verschoben wird, läuft über den schnellen Weg der Leinwand; kommt eine Drehung dazu, muss für jeden Zielbildpunkt die Umkehrabbildung gerechnet werden — gemessen kostete das die halbe Bildrate.

Beim starken Heranfahren werden Kanten und Nähte live nachgezogen: Verläufe verlieren beim Vergrößern nichts, Linien alles. Aus der Stelle im Umlauf werden höchstens **zwei** Bilder überblendet statt dreien.

Figuren ganz außerhalb des Bildes werden nicht gemalt, nur gerechnet. Mit den Detailstufen nach Schirmgröße zusammen, vorher gegen nachher abwechselnd gemessen bei 24 Figuren: herausgezoomt auf dem Desktop 33 → 38 Bilder je Sekunde, bei Zoom 1 und 3 unverändert, am Handy bei Zoom 1 unverändert und bei Zoom 3 39 → 37 — dort erscheinen jetzt die feinen Details.

## Mac-Programm

`desktop/orbit/` baut `ORBIT.app`, fertig in `download/ORBIT-mac.zip`. Universal Binary für Apple Silicon und Intel, eigenes Icon in acht Auflösungen.

Es liest alles über Neutralinos Datei- und Befehls-API — **kein Node nötig**. Die Berechtigungen sind bewusst eng: nur lesende Dateizugriffe, `execCommand`, `getPath`, `open`, der Ordnerdialog, `showNotification` für die Meldungen und `clipboard.writeText` für den Befehl zum Fortsetzen. Keine Schreibrechte auf Dateien.

**Starten ohne Papierkorb.** Beim ersten Start meldet macOS 15 „ORBIT“ wurde nicht geöffnet, mit den Knöpfen „Fertig“ und „In den Papierkorb legen“. Den alten Weg „Rechtsklick → Öffnen“ gibt es dort nicht mehr. Stattdessen: „Fertig“, dann Systemeinstellungen → Datenschutz & Sicherheit → „Dennoch öffnen“. Oder ein Befehl im Terminal: `xattr -cr /Applications/ORBIT.app`. Die Anleitung in `desktop/orbit/README.md` beschrieb noch den alten Weg; sie ist korrigiert.

**Am einfachsten: gar nicht erst markieren lassen.** Den Dialog gibt es nur für Dateien mit der Download-Markierung (`com.apple.quarantine`), und die setzt der Browser, nicht `curl`. Deshalb steht in `desktop/orbit/README.md` jetzt als erster Weg eine Zeile fürs Terminal: laden mit `curl`, entpacken mit `ditto` nach `/Applications`, starten mit `open`. Ein älteres, markiertes ORBIT dort wird vorher gelöscht, sonst bliebe die Markierung am Ordner des Pakets hängen. Geprüft: Der Link liefert per `curl` byte-genau die Zip von Version 24 (das Repo ist öffentlich). Auf einem Mac ausprobiert ist die Zeile nicht; dass `curl` keine Markierung setzt, ist aber das bekannte Verhalten, Homebrew setzt sie deshalb für seine Downloads eigens selbst.

Das Paket ist jetzt ad-hoc signiert, beide Architekturen, samt `Info.plist` und Daten. Vorher war nur der Apple-Silicon-Teil des Programms vom Linker signiert, und `Contents/_CodeSignature` fehlte ganz. Ein solches Paket nennt macOS auf Apple Silicon oft „beschädigt“ — dann gibt es keinen Knopf „Dennoch öffnen“, nur den Papierkorb. Dafür musste `resources.neu` umziehen. Neutralino sucht die Datei neben dem Programm in `Contents/MacOS`, dort darf für eine gültige Signatur aber nur Programmcode liegen; rcodesign ließ sie beim ersten Versuch einfach unversiegelt, und macOS hätte das als verändertes Paket gewertet. Jetzt liegt sie in `Contents/Resources`, neben dem Programm steht nur ein Verweis. Geprüft: mit dem Linux-Programm von Neutralino, gestartet aus einem fremden Ordner — es liest `resources.neu` über den Verweis und liefert die volle Seite aus; ohne Verweis bricht es mit „resources.neu is missing“ ab. Die Signatur prüft ein eigenes Skript unabhängig von rcodesign: jeder Seitenhash beider Architekturen, die Hashes von `Info.plist` und `CodeResources`, jede versiegelte Datei, und dass nichts unversiegelt daneben liegt. Ein verändertes Byte in `resources.neu` fällt dabei auf. Auf dem Mac signiert `make-mac-app.sh` mit `codesign`, auf Linux mit `rcodesign`, wenn vorhanden.

Vom Detail einer Sitzung oder eines Projektordners geht es direkt zur Arbeit: „In VS Code öffnen" und „Im Finder zeigen". VS Code wird über seine eigene Adresse `vscode://file/…` geöffnet und nicht über einen Befehl in der Shell — ein Pfad mit einem Anführungszeichen darin kann so nie zu einem Befehl werden.

## Log und Szene sichern

Das Missions-Log lässt sich als Markdown sichern, die Szene als Bild in voller Auflösung. Im Browser und im Mac-Programm ist das ein gewöhnlicher Download. Im Artefakt-Betrachter von claude.ai darf eine Seite nicht selbst herunterladen — dort taten beide Knöpfe still nichts, und der Bildknopf meldete trotzdem „Gesichert". Jetzt bietet dort der Betrachter die Datei an und fragt nach; „Gesichert" steht nur, wenn gesichert wurde, nach einer Ablehnung „Nicht gesichert", und kann der Betrachter keine Dateien hergeben, fallen die Knöpfe weg.

## Als App auf dem Handy

Eigenes Manifest, eigener Service Worker, eigene Icons. Die Installationseinladung erscheint nur, wenn es etwas zu installieren gibt. Die Seite kommt bevorzugt frisch aus dem Netz; fremde Hosts laufen immer live und landen nie im Cache.

Auf schmalen Schirmen lagen die Stationswerte über dem Band der Vorführung. Ausgerechnet der Hinweis, dass nichts davon echt ist, war halb verdeckt. Jetzt sitzen sie darunter und rechnen, wie der Kopf, die Kamerakerbe des iPhones mit ein.

## Zwei gleichnamige Funktionen

In JavaScript gilt von zwei gleichnamigen Funktionen die spätere, ohne Warnung. Das ist bei ORBIT zweimal passiert:
- `zeitText(ms)` schreibt die Uhrzeit eines Eintrags ins Missions-Log, `zeitText()` die Anzeige des Zeitraffers. Seit es die zweite gab, stand im Log bei keinem Eintrag eine Uhrzeit. Die zweite heißt jetzt `zeitrafferText()`.
- `ersterAuftrag()` holt die Aufgabe eines Unteragenten und kennt den Vorspann der Arbeitsabläufe. Die neue Funktion für den Tagesbogen hieß zuerst genauso. Dadurch verloren die Agenten eines Arbeitsablaufs ihre Aufgabe, und die Brücke las ihre Protokolle bei jedem Durchlauf neu. Aufgefallen ist das im Test gegen echte Daten: sieben Dateien im zweiten Durchlauf statt einer. Sie heißt jetzt `sitzungsBeginn()`.

Meine Syntaxprüfung vor jedem Commit verweigert jetzt doppelte Funktionsnamen. Sie liegt nicht im Repository.

## Geprüft

105 Tests mit Playwright, ohne echte API-Kosten. Die ganze Reihe läuft gegen einen eingefrorenen Stand. Wo „gegengeprüft“ steht, schlägt der Test gegen die alte oder eine absichtlich kaputte Fassung an.

**Daten und Brücke**
- **Regenradar** (regen.mjs, ein nachgebautes RainViewer mit bekannten Werten):
  - Das Wetter: eine Zelle über München, 42 dBZ und nach außen schwächer, mit einem Kern von 52 dBZ und drei Kilometern, den nur feine Kacheln sehen. Ein Gewitter über Wien mit 56 dBZ, Schnee über Oslo, trocken in Paris, kein Radar auf dem Atlantik. Die Kacheln schreibt der Test selbst als PNG, roh und bunt.
  - Aus fragt nichts, auch mit offener Erde. Ein, aber die Erde zu: keine Anfrage, die Zeile sagt, wo es zu sehen ist. Erde offen: genau ein Index und 16 verschiedene Kacheln der Stufe 2, Fenster 0/0, Quellenangabe, Zeile „Radar von … · nass auf … % der Radarfläche“.
  - Die Worte an allen fünf Orten, aus Stufe 2. Blitze: ein Radarkern bei Wien, keiner woanders, und keine Wolkenzelle, wo ein Radar hinsieht.
  - Flug nach München: dort orange (Rot über 170, Blau weit darunter), neun Punkte nördlich, südlich, westlich und östlich fast gleich. Die Zelle sitzt also auf dem Ort. Paris sieht mit und ohne Radar gleich aus, München deutlich anders. Die Karte sagt „starker Regen, etwa 13 mm pro Stunde“.
  - Mit Satellitenbildern hinein: Stufe 6, das Fenster enthält Münchens Kachel, höchstens 16 Kacheln. Die offene Karte zieht auf den Kern nach, „Starkregen, wohl Gewitter“. Ganz nah bleibt es bei Stufe 6.
  - Ein neues Bild: Dazwischen zeigt München das alte, danach das neue. Die Palette kennt den Schalter, nach dem Neuladen ist er noch an. Aus: Speicher leer, keine Anfrage, München wie ohne. Eine fremde Adresse im Index wird abgelehnt, keine Anfrage dorthin.
  - Das bunte Bild als Rückfall: dieselben Worte für München und Oslo, „kein Regen gemessen“ für Paris und den Atlantik. Eine Kachel ganz im Regen wird trotzdem richtig erkannt: bunt ganz blau ergibt 24 dBZ, roh ganz 40 dBZ bleibt roh. Die erste Erkennung stützte sich nur auf durchsichtige Punkte und hätte die blaue Kachel für Messwerte gehalten; jetzt zählt auch der Blaukanal, der in den Messwerten nur 0, 191 oder 255 ist. An 54 echten rohen und 16 echten bunten Kacheln nachgeprüft: keine falsch.
  - Gegengeprüft mit 17 kaputten Fassungen: Erkennung nur am Alpha, Breite ohne Mercator, ohne Schnee, ohne Radarfläche, fremde Adresse erlaubt, nur grob, ohne Nachziehen, ohne Quelle, Aus räumt nicht auf, Tafel falsch, ohne Zeile, neues Bild übersehen, fragt auch bei geschlossener Erde, Loch beim neuen Bild, Blitze nur aus Wolken, um 3,6 Grad nach Osten verschoben, malt ausgeschaltet weiter. Alle 17 schlagen an.
- **Version 23 gegen den eingefrorenen Stand b58b8d0: 95 von 98 grün.** Die drei roten:
  - echt.mjs braucht ein echtes Unteragenten-Protokoll der letzten 48 Stunden; das einzige in dieser Umgebung war vom 21. September. Mit einem frischen wieder grün. Die Testdaten waren gealtert, nicht der Code.
  - menue.mjs kannte die neue Schalterliste mit „Regenradar“ noch nicht. Erwartung ergänzt, grün.
  - regen.mjs maß Farben bei echter Uhrzeit, abends ist alles dunkler: Orange kam mit Rot 170 statt über 170. Jetzt steht die Uhr im Test auf Vormittag. Dazu wartet jede Farbmessung, bis die Kugel nachweislich neu gerechnet wurde; unter Last dauerte das länger als drei Bilder.
  - Danach gegen den Endstand 0841bd2 grün: echt, menue, regen, regenfilm, palette, hilfe, erdansicht, erdkarte, orte, wolkenheute, weltraumwetter, satellit, tasten, handy, schalter.
- **Regentürme** (regenturm.mjs): Ein großes Gewitter über Wien, 49 Grad von der Blickmitte, also schräg gesehen. Flach liegt es genau auf Wien. Als Turm liegt sein Schwerpunkt 4,8 Bildpunkte weiter außen, zum Rand der Kugel hin, und es reicht 2,3 Bildpunkte weiter, weil die Wand zur Blickmitte dazukommt. Von oben, Wien in der Mitte, bleibt es an seinem Platz. Dazu die Höhe je Radius: 0,03 Erdradien bei 300 Punkten, 26 Punkte bei 900, echt 0,0019 ganz nah. Gegengeprüft mit drei kaputten Fassungen: flach, Blick in die falsche Richtung, Höhe nicht gedeckelt.
- **Zuhause** (regenheim.mjs, eine Front zieht mit 60 km/h von Westen auf München zu, alle zehn Minuten ein Bild):
  - Der Knopf „⌂ Als Zuhause merken“ steht in der Karte von München, nicht beim offenen Meer und nicht bei Bauteilen. Danach „⌂ Zuhause · nicht mehr merken“, und auf der Erde steht das Haus.
  - Front 50 km westlich: „München · trocken · Regen in etwa 40 min · zieht aus Westen, 59 km/h“, ohne Meldung, denn es ist die erste Rechnung. Zwei Bilder später „Regen in etwa 30 min“ und genau eine Meldung, ein Bild später keine zweite. Über München: „starker Regen · hört in etwa 40 min auf“ und „Es regnet in München“.
  - Für das Zuhause nur Kacheln der Stufe 4, bei geschlossener Erde keine anderen. Vergessen: keine Zeile, keine Anfrage mehr. Nach dem Neuladen noch gemerkt.
  - Die Rechnung selbst: Eine Front aus Südwesten ergibt genau 0,35 Punkte je Minute nach Nordosten, „aus Südwesten“. Ein Feld ohne Struktur ergibt keine Bewegung; zuerst kamen dort 224 km/h heraus.
  - Die erste Rechnung meldet nichts, auch wenn Regen kommt. Dabei gefunden, dass der Test das zuerst nicht bemerkte: Das Bordbuch nimmt dieselbe Meldung nicht zweimal hintereinander, und genau diese kam im Test schon vorher vor.
  - Gegengeprüft mit zwölf kaputten Fassungen: erste meldet, doppelt, Richtung verkehrt, nicht im Hintergrund, Vergessen bleibt, nicht gespeichert, kein Haus, Stufe 5, ohne Gleichstandsregel, ohne Bewegung, ohne Zeile, Knopf beim Meer. Alle zwölf schlagen an.
- **„Unter uns“ auf der ganzen Erde** (erdunteruns.mjs): Solange sie offen ist, wird die Szene darunter nicht gezeichnet, und die Beschriftung am Stationspunkt kam aus deren letztem Blick. Nach 15 Sekunden lag sie 10,7 Grad neben dem Punkt, nach Minuten stand ein Meer dort, das die Station längst hinter sich hatte. Aufgefallen auf den Fotos vom Regenradar. Jetzt kommt sie aus der Bahn von jetzt, wie der Punkt: 0 Grad. Gegen den alten Stand schlägt der Test an.
- **Regenfilm** (regenfilm.mjs, dreizehn nachgebaute Bilder, die Zelle von München zieht in zwei Stunden sechs Grad von Westen heran):
  - Ohne Radar kein Knopf. Mit Radar und Erde: Knopf, „Regen 16:02“, dreizehn Striche; die Palette findet „Regenfilm“.
  - Abspielen holt genau 192 Kacheln: zwölf ältere Bilder zu je 16, keine des neuesten, keine doppelt.
  - Auf Bild 0 angehalten: orange sechs Grad westlich, nicht über München; die Uhrzeit am Knopf und „Film · … · 1 von 13“ unter Stationswerte. Eine spät kommende neueste Kachel ändert daran nichts. Bild 12: wieder über München. Weiterlaufen: mindestens drei Bilder in zweieinhalb Sekunden.
  - Der Knopf hält an, das neueste Bild ist zurück. Erde zu: Film weg, Knopf weg. Mit Satellitenbildern nach München, Stufe 6: der Film endet.
  - Kommt keine ältere Kachel, aber drei fehlende des neuesten, gibt es keinen Film, und der Knopf sagt „Film nicht geladen“. Dabei gefunden: Zuerst zählte ORBIT nur, ob alle Anfragen scheiterten. Holte der Film fehlende Kacheln des neuesten Bilds mit, kamen die an, und es liefen zwölf leere Bilder. Jetzt braucht es mindestens zwei Bilder mit Kacheln.
  - Zweimal hintereinander grün, und einmal neben drei kaputten Fassungen unter voller Last.
  - Gegengeprüft mit zwölf kaputten Fassungen: Knopf immer, alles neu laden, neueste Kachel überschreibt den Film, kein Zurück, bleibt beim Wandern, bleibt bei geschlossener Erde, steht still, ohne Zeile, falsche Zeit, Packen kaputt, Fehlschlag still, Fehlschlag nach der alten Regel. Alle zwölf schlagen an.
  - Mit echten Kacheln angesehen: Europa, Russland und Indien am 23. September gegen 15:30 UTC, Konstanza mit Satellitenbildern bei Stufe 6.
- **Ortssuche und Flug** (orte.mjs):
  - Gefunden werden München auch als „Munich“, Italien als Land, Frankfurt am Main vor Frankfurt (Oder). Ein Buchstabe liefert keine Orte, „san“ höchstens zwölf.
  - Der Flug wird bei angehaltener Szene in vierzig Schritten nachgerechnet. Er liegt auf dem Großkreis (Abweichung 10⁻¹⁶) und springt nie weiter als erlaubt. Bei München nach Tokio geht der Zoom genau bis 1,57-fach hinaus.
  - Am Ziel: München genau in der Mitte, Norden oben, der Ring auf den Bildpunkt über München, auch 5 Grad verschoben. Die Karte ist offen, Esc schließt erst sie, dann die Erde.
  - Zoom 2,4 ohne, 220 mit Satellitenbildern, Italien 11,8. Das Mausrad bei 30 % des Wegs hält den Flug an, ohne Sprung. Ohne Erde gibt es keine Orte.
  - Die ganze Reihe fand danach einen echten Fehler: „kasse“ fand zuerst die Stadt Kassel und nicht die Sitzung webshop-kasse, denn nach einem Bindestrich galt kein Wortanfang. Jetzt beginnen Wörter auch nach Bindestrich, Unterstrich, Schrägstrich und Punkt, und Orte stehen bei gleich gutem Treffer hinter der Crew. „kassel“ findet weiter Kassel.
  - Dabei gefunden: Das Ende des Flugs verglich einen Bruch mit 1, und (t0 + d − t0) / d liegt in 42 % der Fälle knapp darunter. Jetzt wird die Uhr verglichen, mit einem Test genau dafür.
- **Station hinter der Erde** (stationhinten.mjs):
  - Gefunden auf einem Foto mit echten Radardaten: Die Station stand über dem Indischen Ozean, der Blick auf Europa, und ihr Punkt schien durch die Kugel hindurch.
  - Nach dem Flug zum Gegenpunkt: kein Stationspunkt, kein „Unter uns“, dort, wo er durchschiene, kein weißer Bildpunkt (vorher 255). Der Zeiger steht am Rand und sagt „Station hinter der Erde“.
  - Antippen startet den Flug zurück. Jeder Schritt wird mit der Uhr aufgezeichnet, nach der der Flug rechnet, samt Blickrichtung und Oben. Am schnellsten dreht das Bild 0,12 Grad je Millisekunde; die Formel erwartet für diesen Weg knapp 0,1. Beim Übergang in die folgende Kamera sind es 0,0005, also kein Sprung. Danach: Station zu sehen, „Unter uns“ wieder da, Zoom 1.
  - Vorher drehte das Oben mitten im Flug mit 0,37 Grad je Millisekunde, während die Blickrichtung 0,096 hatte. Deshalb rechnet jetzt jeder Flug das Oben als Drehung (siehe Ortssuche und Flug). orte.mjs, palette.mjs, kompass.mjs, erdansicht.mjs, erdunteruns.mjs, satellit.mjs und die drei Regen-Tests sind danach grün.
  - Vorn, aber 40-fach hineingezoomt: Zeiger am Schirmrand, „Station“, frei von Kopfzeile und Bedienung.
  - Gegengeprüft mit sechs kaputten Fassungen: Punkt scheint durch, Punkt außerhalb des Schirms, kein Zeiger, Ziel nicht nachgeführt (Sprung am Ende), Oben linear gemischt, Antippen ohne Wirkung. Alle sechs schlagen an.
- **Zwei an derselben Datei** (konflikt.mjs):
  - Die Regel an zehn nachgebauten Fällen: zwei Sitzungen an `preis.ts` (Konflikt), andere Datei, eine Änderung 31 Minuten alt, Übergabe an einen Unteragenten, Sitzung ändert, während der Unteragent läuft (Konflikt), Sitzung ändert nach seinem Bericht, zwei Geschwister gleichzeitig (Konflikt), zwei Arbeitskopien, drei Sitzungen an einer Datei (drei Paare, die jüngste zuerst), ein Projektordner zählt nicht.
  - Durch die Brücke: Beim ersten Lesen besteht der Konflikt schon, also keine Meldung und kein Eintrag. Derselbe Stand noch einmal: nichts. Eine dritte, neu gelesene Sitzung an derselben Datei: drei Paare, keine Meldung. Dann ändert die erste Sitzung eine Datei der zweiten: genau eine Meldung „Konflikt: gutschein.ts“ an die, die zuletzt geändert hat, und „⚠ gutschein und kasse ändern beide gutschein.ts“ im Bordbuch.
  - Stationswerte „gutschein.ts · gutschein und kasse · 1 weitere“ in Rot. Im Detailfenster beide Dateien mit rotem Punkt und „⚠ auch kasse (vor 9 Min.)“. In der Szene die Strecke mit „⚠ gutschein.ts +1“, gemessen an roten Bildpunkten am Rand des Schilds und an zwei Stellen der Zacken.
  - Die Vorführung: bei Sekunde 70 und 94 nichts, bei 96 und 140 `preis.ts` von pruefung:rundung zu webshop-kasse.
  - Gegengeprüft mit zwölf kaputten Fassungen: ohne Zeitregel, ohne Frist, meldet beim Start, meldet immer wieder, vergleicht nur den Dateinamen, zählt Projektordner, kein Bild, keine Zeile, kein Hinweis im Detail, Vorführung ohne Konflikt, Richtung verkehrt, die alten zuerst. Alle zwölf schlagen an. Ohne die Zeitregel meldete die Vorführung schon bei Sekunde 94 einen Konflikt, obwohl die Sitzung `preis.ts` geändert hatte, bevor die Prüfung überhaupt losging.
  - Dazu grün: dateien, vorf, detailtausch, familie, funk, aufgaben, test-bruecke, palette, werkzeug, minitakt, github, lieferung, hilfe und menue.
  - Befehlspalette: „konflikt“ findet „⚠ Konflikt: gutschein.ts“ und „⚠ Konflikt: preis.ts“, Enter öffnet kasse, die gutschein.ts zuletzt geändert hat. „im kreis“ findet alle drei Kreise, Enter öffnet den obersten. palette.mjs bleibt grün; ohne die Einträge schlägt der Test an.
  - Der Blick: Beide Figuren sehen einander an, aus dem Grund „konflikt“ und nicht, weil sie zufällig Nachbarn sind. Ohne die Regel sah kasse im Test weg; gegengeprüft.
  - Geschlossene Sitzungen: Führt das Register nur b, war a vor 20 Minuten an `preis.ts` und vor 15 zuletzt tätig, und b ändert vor 3 Minuten, ist das keiner. Führt das Register beide, ist es einer, und bei leerem Register ebenso. Gegengeprüft: Eine Fassung, die das Register übergeht, meldet den geschlossenen Fall.
  - Leiste und Crew-Liste (in konflikt.mjs und schleife.mjs): „⚠ gutschein.ts · auch kasse“ in Rot, gekürzt auf 26 Zeichen wie jede Zeile der Leiste, der volle Pfad als Hinweis beim Zeigen; „⟲ 5× derselbe Fehler“ in Orange, mit Befehl und Fehlerzeile als Hinweis; eine Sitzung ohne Kreis behält ihre Tätigkeit. Gegengeprüft: ohne die Zeile in der Leiste und ohne die in der Crew-Liste schlagen beide Tests an. crewliste, familie, winken, minitakt, vorf, unteragent, stoerung und palette bleiben grün.
- **Wer sich im Kreis dreht** (schleife.mjs, sechs nachgebaute Sitzungen im echten Protokollformat, gelesen über die Brücke):
  - kreis: `npm test -- kasse` viermal mit demselben Fehler, nur die Dauern verschieden („1.24 s“, „Time: 2.31 s“), dazwischen Änderungen und ein anderer Befehl, einmal mit doppelten Leerzeichen geschrieben. Erkannt: vier, die Fehlerzeile „FAIL tests/kasse.test.ts“.
  - fortschritt: viermal rot, aber 5, 3, 2, 1 failed: kein Kreis. geloest: dreimal derselbe Fehler, dann grün: keiner. abgelehnt: zweimal, eine Ablehnung, einmal, dazu dreimal ein anderer Befehl abgelehnt: keiner. zwei: `tsc` dreimal mit dem Inhalt als Liste und Exit code 2, danach `pytest` nur zweimal: der Kreis ist `tsc`. alt: dreimal vor 16 bis 20 Minuten: erkannt, gilt aber nicht mehr.
  - Beim ersten Lesen keine Meldung. Danach wird kreis nur länger (fünf): keine neue Meldung. geloest fällt in eine neue Reihe: genau eine, „geloest dreht sich im Kreis“ mit „cargo build: 3-mal derselbe Fehler. error[E0425]…“, und im Bordbuch.
  - Stationswerte „geloest · cargo build · 3× derselbe Fehler · 2 weitere“. Im Detail „Im Kreis · 5-mal derselbe Fehler · seit …“, Befehl und Fehlerzeile. In der Szene der Ring mit „⟲ 5×“, gemessen an orangefarbenen Bildpunkten links und unten auf dem Ring und am Schild.
  - Vorführung: bei Sekunde 50 nichts, bei 56 dreimal, bei 62 viermal, nach dem Bericht bei 71 nichts.
  - Gegengeprüft mit 13 kaputten Fassungen: ohne Fehlervergleich, Dauern zählen mit, Ablehnung zählt als Fehlschlag, Schwelle 2, Inhalt als Liste nicht gelesen, ohne Frist, gilt nach dem Ende weiter, meldet immer wieder, meldet beim Start, kein Ring, keine Zeile, kein Hinweis im Detail, Vorführung ohne. Alle 13 schlagen an. „Meldet beim Start“ kam zuerst durch, weil der Test zu spät hinsah: Die Brücke läuft beim Laden schon von selbst, und ihr erster Durchlauf war vorbei, bevor der Test mitschrieb. Jetzt stellt er den Stand des Starts her.
  - An echten Daten: Das ganze Protokoll dieser Sitzung (516 MB) mit derselben Regel in Python durchgerechnet: 4668 Befehle, 57 gescheitert, keine einzige Reihe von drei gleichen Fehlschlägen, auch ohne den Fehlervergleich nicht. Fehlalarme gab es dort also keine. Einen echten Kreis aber auch nicht: Dass die Regel einen findet, ist nur an den nachgebauten Protokollen geprüft.
  - Die Kosten: Von fünf Antworten in der Liste der Energie zählen genau die zwei dieser Sitzung nach dem ersten Fehlschlag (120.000 und 64.000, zusammen „184 Tsd. Tokens“); eine davor, eine einer anderen Sitzung und eine ihres Unteragenten nicht. Gegengeprüft: ohne die Auswahl nach Figur kamen 1,5 Mio. heraus, ohne die Zeitgrenze 9,4 Tsd.
  - Weil der Leser geändert ist, dazu grün: echt, echt2, dateien, aufgaben, stoerung, unteragent, familie, test-bruecke, werkzeug, vorf, funk, melden, wartet, energie-echt und konflikt.
  - Zehn kaputte Fassungen schlagen an.
- **Lieferungen** (lieferung.mjs, Flugzeiten für den Test verkürzt):
  - Erste Sichtung: ein alter Merge und drei offene PRs, nichts wird geliefert.
  - Dann PR #12 gemergt, zwei Abläufe auf denselben Commit: genau eine Lieferung mit dem Titel des offenen PR, Anflug, Schild am Stutzen, Stationswerte.
  - Angedockt kommen dazu: ein Squash-Merge „(#15)“, ein gewöhnlicher Push mit zwei Abläufen, PR #13 (GitHub meldet gemergt) und PR #14 (nur geschlossen). Genau vier Lieferungen an Bord, #14 nicht, das Andocken verlängert.
  - Nach dem Ablegen liefert derselbe Stand nichts noch einmal. Ohne GitHub wieder der Plan. In der Vorführung bringt er PR #12 nach hundert Sekunden.
  - Gegengeprüft mit sieben kaputten Fassungen: alles nachholen, je Ablauf zählen, ohne Titel, geschlossen zählt, kein Nachschub, immer nach Plan, Squash nicht erkannt. Alle sieben schlagen an.
- **Befehlspalette** (palette.mjs): Strg+K und / öffnen; ohne Suchwort die Gruppen Crew, Aktionen, Öffnen und Schalter, samt „Zum Nächsten, der wartet“. Die Pfeile laufen oben und unten herum. „bru“ findet „Brücke“ mit „Brü“ hervorgehoben, und dabei startet kein Rundgang. Enter schaltet das Relief um, fährt zu webshop-kasse und öffnet sie, und wählt den Hintergrund Trifid. Esc lässt die Hilfe darunter offen. Aus dem Auftragsfeld öffnet Strg+K, ein / dort bleibt ein Zeichen, und nach Esc ist der Fokus wieder im Feld. Am Handy passt die Karte mit 16 Punkten Rand. Gegengeprüft mit sechs kaputten Fassungen: mit Akzenten, Esc ungefangen, ohne Fokus zurück, ohne Umlauf, nicht im Textfeld, Hintergründe immer. Alle sechs schlagen an.
- **Energie, nachgebaut** (energie.mjs):
  - Zwei Fenster mit über fünf Stunden Pause dazwischen, jede Antwort in zwei Zeilen, eine synthetische Antwort und ein Werkzeugergebnis mit `"usage"` als Text.
  - Dazu ein Unteragent, ein Ablauf-Agent und dieselbe Antwort auch im Protokoll der Mutter.
  - Eine 14-MB-Datei, deren Anfang vor den zehn Stunden liegt: gelesen wird ab 4 kB vor der ersten zählenden Zeile, kein Happen über 4 MB.
  - Eine Zeile, die in zwei Stücken geschrieben wird, zählt genau einmal, und erst, wenn sie ganz ist.
  - Die Uhr steht in Indien (UTC+5:30), damit ein Beginn zur vollen Ortsstunde auffiele. Summen, Tempo, Aufteilung, alle Zeilen und das Detailfenster sind auf die Zahl geprüft, dazu die Vorführung und dass ohne Brücke nichts dasteht.
  - Gegengeprüft mit zehn kaputten Fassungen, darunter doppelt gezählt, Ortsstunde, ohne Rest, von vorn gelesen, ohne Unteragenten, immer sicher. Alle zehn schlagen an.
- **Energie, echt** (energie-echt.mjs): Das Protokoll dieser Sitzung (480 MB, mit Umlauten) wird byte-genau wie von Neutralino gelesen und mit einer eigenen Rechnung in Python über alle Antworten verglichen. Beginn 09:00 UTC, 393 Antworten, 172.064.380 Tokens, in allen vier Feldern gleich. Das Lesen der zehn Stunden dauerte hier 91 Sekunden. Der Rückblick las 78 bis 116 MB in 8 bis 13 Sekunden, weil 78 % der Datei in Zeilen über 256 kB stecken.
- **Die Kette der Fenster** (energie-kette.mjs):
  - Nach einer alten Sitzung folgen sechseinhalb Stunden Pause, dann 22 Stunden durchgehende Arbeit in zwei Dateien. An einer Fenstergrenze arbeitet nur ein Unteragent weiter.
  - Erwartet wird 10:00 UTC; ohne den Unteragenten käme 11:00 heraus. Nach dem Rückblick wandert der Anker mit.
  - 60 Stunden ohne Pause ergeben „etwa“.
  - Fünf kaputte Fassungen schlagen an: ohne Rückblick, ohne Unteragenten, ohne den Weg vorwärts, Zwischenspeicher ohne Zeitpunkt und eine verschobene Stunde.
- **Drei Tests maßen unter Last falsch, nicht die App.** In der ganzen Reihe liefen neben ihr noch Gegenproben. Einzeln waren alle drei grün; die Ursache ließ sich jeweils mit zwölffach bis sechsfach gedrosseltem Prozessor nachstellen.
  - **erdansicht.mjs** zählte eigene Bilder und verglich sie mit den eingesparten der App: 33 von 60. Mit der nachgebauten Uhr von Playwright lief die billige Schleife des Tests unter Last bis doppelt so oft wie die teure der App (60 gegen 35); ohne die Uhr beide gleich. Jetzt zählt der Test über die Bilder der App.
  - **erdkarte.mjs** setzte die Phase und wartete 450 ms nach der nachgebauten Uhr. Unter Last kam in der Zeit kaum ein Bild, und der Tagesrand war noch der vorige (23 von 156 Punkten falsch). Jetzt wartet er auf fünf Bilder der App. Dabei fiel ein Fehler in der eigenen Testhilfe auf: Die App plant ihr nächstes Bild über den Namen `rahmen`, eine Hülle darum wird einmal mehr gerufen, als sie zählt, und darf dann nur sich selbst zurücknehmen.
  - **funk.mjs** maß nach drei Sekunden. Steht ein Unteragent noch dicht neben seiner Sitzung, zeichnet die App bewusst keine Strecke, und unter Last ist er noch nicht auf seinem Platz, weil ein Bild höchstens 64 ms rechnet. Jetzt wartet der Test, bis beide Strecken stehen, höchstens 30 Sekunden.
  - Alle drei sind gegengeprüft: Tagesrand verkehrt, Szene nicht eingespart und eine laufende Strecke als still fallen weiter auf.
- **Pulse der Hand** (werkzeug.mjs): Der Test zählte die Pulse erst zwei Bilder nach dem Planen. Jeder Puls verlischt aber 750 ms nach seinem Zeitpunkt, und unter der Last der ganzen Reihe dauerte ein Bild über 1,6 Sekunden. So meldete er „Bündel nicht begrenzt: 3“, obwohl sechs geplant waren. Mit zwölffach gedrosseltem Prozessor ließ sich das nachstellen. Jetzt hält er fest, was die App im selben Bild plant, und ist auch gedrosselt grün. Gegengeprüft: ohne Obergrenze meldet er 20, ohne Verteilung drei gleichzeitige.
- **Echte Arbeitsumgebung**:
  - eine Sitzung von 221 MB,
  - sechs Ablauf-Agenten, drei im Limit abgebrochen, drei mit Ergebnis,
  - echte Ausgaben von `ps` und `git`.
  Im zweiten Durchlauf wird nur noch das Register gelesen.
- **Nachgebaute Neutralino-API mit echten Formaten**: Sessions, Unteragenten samt `.meta.json`, Ordner und Prozesse.
  - Kontext 2 + 31.579 + 38.673 = 70.254 Tokens, davon 55 % aus dem Zwischenspeicher.
  - 50 Projekte mit je 20 alten Sitzungen brauchen 52 statt 1053 Dateiabfragen.
  - Jede benutzte Funktion ist gegen die mitgelieferte Client-Bibliothek geprüft.
- **Protokolle**:
  - Unteragenten, fertig nach Vermutung oder nach dem Ergebnis in der Sitzung; der Registername ist gegengeprüft.
  - Die Aufgabenliste gegen echte Aufgabendateien.
  - Störung und Verdichten im echten Wortlaut.
  - Geänderte Dateien: aus einem Protokoll voller Fallen zählen genau die vier echten Änderungen.
- **Durchsicht**: Zwei Freigaben, mit einem Kommentar und einer verworfenen Bewertung dazwischen; angefragt; Änderungen gewünscht. Ein PR ohne Zugriff auf die Bewertungen zeigt keine Marke. Der zweite Durchlauf fragt nicht neu, ein geänderter PR schon, und genau diese Änderung ergibt eine Mitteilung.
- **GitHub**:
  - Ein roter Ablauf macht den PR rot, ein älterer Versuch wird verdrängt, und ein wartender Lauf winkt. Die Abfragen sind über vier Takte gezählt.
  - Ein gescheiterter Vercel-Check und ein laufender CircleCI-Status stehen neben den Actions.
  - Derselbe Job als Actions-Check erscheint nicht doppelt.
  - Ohne Leserecht für Checks (403) bleiben die zwei Actions, ohne Fehler.
- **Meldungen**: Die erste Sichtung bleibt still, Titel und Mitteilung stimmen, im Hintergrund wird nur das Register gelesen.

**Tagesbogen, Fortsetzen, Tag als Text**
- **Tagesbogen**: beendete, über Mitternacht laufende, gestrige und laufende Sitzungen. Im zweiten Durchlauf wird kein Dateikopf neu gelesen. Die Uhr der Seite steht fest auf 15 Uhr, denn kurz nach Mitternacht gäbe es keine „heute beendete“ Sitzung.
- **Fortgesetzte Sitzung**: Eine Sitzung von vor drei Tagen, heute um 14 Uhr fortgesetzt, beginnt um 14 Uhr, nicht um 0 Uhr. Die Datei hat 1 MB, eine Riesenzeile und einen fremden Zeitstempel in einem Werkzeugergebnis. Die Suche braucht 10 Lesezugriffe, im zweiten Durchlauf keinen. Gegengeprüft: Vorher stand dort „14 Std. 59 Min. offen“.
- **Antippen**: „Begann mit …“ ohne Meta-Eintrag und ohne `/clear`; eine laufende Sitzung mit Auftrag und „Zur Figur“; Tastatur; der Fokus übersteht den Neuaufbau.
- **Woche**:
  - Eine Sitzung am Tag −5 fortgesetzt am Tag −2 ergibt zwei Säulen und nichts dazwischen.
  - Eine gestern um 20 Uhr fortgesetzte Sitzung läuft bis 23:59 und heute ab 0:00; heute ist gleich dem Bogen.
  - Der zweite Durchlauf liest nichts neu.
  - Text, Säulen und Antippen stimmen; die Vorführung ist gekennzeichnet, am Handy gibt es keinen Überlauf.
  - Gegengeprüft: Ohne die Suche an den Grenzen stehen Tage ohne Zeile mit 23 Std. 59 Min. da.
- **Fortsetzen**:
  - Der Befehl `cd '/Users/phil/Phil'\''s Kasse' && claude --resume b2` ist in bash, dash und sh ausgeführt; zsh war nicht vorhanden.
  - „Kopiert ✓“ und die Markierung überstehen den Neuaufbau.
  - Ohne Zwischenablage steht „Mit ⌘C kopieren“ da.
  - Eine noch offene Sitzung zeigt den Hinweis statt des Befehls.
  - In Browser und Vorführung gibt es die Zeile nicht.
- **Tag als Text**: Kopf, Summe und die Sitzungen der Zeit nach. Der Download heißt `orbit-heute-2026-09-23.md`, die Vorführung ist gekennzeichnet, und im Betrachter ohne Dateien fehlt der Dateiknopf.

**Szene**
- **Echte Erde**:
  - Die Sonne steht am 23. September um 12 Uhr UTC über dem Äquator bei −1,9 Grad, das ist die Zeitgleichung. Im Juni steht sie bei 23,44 Grad Nord.
  - Die Bahn ist 51,64 Grad geneigt, mit der Sonne in ihrer Ebene. Am Mittag der Station liegt sie genau unter der Sonne, und der Boden zieht nach links.
  - An 120 klaren Stellen weicht die gemalte Farbe im Mittel um 2 Stufen von der Karte am selben Ort ab. Gegengeprüft: Um 3,6 Grad verschoben sind es 18.
  - Ohne Karten fällt die Seite auf die gerechnete Erde zurück, mit Gewittern.
  - An acht Ständen um Auf- und Untergang liegen je rund vierzig Stellen links und rechts vom Tagesrand. An jeder steht die Sonne auf der Karte über oder unter dem Horizont, genau wie die Szene es zeigt.
  - Mondlicht auf den Wolken ist mit beiden Erden geprüft.
  - Magnetische Breite: Churchill in Kanada liegt bei 67,2 Grad, Berlin bei 52,1, und südlich von Australien kommt die Station auf −60.
- **Die ganze Erde**:
  - Am Mausrad über den kleinsten Zoom hinaus kommt die Kugel, die Überblendung läuft durch, und die Zoomanzeige sagt „Erde“.
  - Die Station steht auf weniger als einen Bildpunkt genau dort, wo die Bahn in 420 Kilometern Höhe sie hinstellt.
  - An 120 klaren Stellen der Tagseite weicht die gemalte Farbe im Mittel um 1,9 Stufen von der Karte am selben Ort ab, samt Sonnenlicht und Luftsaum. Gegengeprüft: Um zehn Grad verdreht sind es 44,5.
  - An 80 dunklen Stellen der Nachtseite ohne Städte ist keine heller als 10 von 255.
  - Mond: An vier bekannten Neu- und Vollmonden 2026 (18. Januar, 3. März mit der totalen Mondfinsternis, 11. und 26. September) liegt die gerechnete Elongation höchstens 0,09 Grad neben 0 oder 180. Wolken der Nachtseite, über denen der Mond steht, sind mit seinem Licht im Mittel 13 Stufen heller als ohne.
  - Himmel: 3817 Sterne. Schaut die Kamera gegen das Licht, ist die Stelle, an der die Sonne stehen muss, weiß (255, 253, 246), und 150 Punkte daneben ist es dunkel.
  - Polarlicht: Auf dem Oval ist die Nachtseite im Mittel um 40 Stufen grüner als zehn Grad daneben, dort sind es −0,2. Gegengeprüft: ohne Oval −0,4.
  - Blitze: 26 in sechs Sekunden, alle in dunklen Zellen auf der sichtbaren Seite. Bei angehaltener Zeit kommt keiner dazu. Gegengeprüft: ohne Blitze null.
  - Sonnenglanz: An klarem Wasser rund um die Stelle zwischen Sonne und Auge ist es im Mittel 92 Stufen heller als ohne Glanz. Weit davon entfernt sind es 0,6. Gegengeprüft: Ohne Glanz sind es auch in der Mitte −0,2, und der Farbvergleich weicht dann um 12 statt 2 Stufen ab.
  - Auf dem Schirm ist die Tagseite im Mittel 59 hell, die Nachtseite 4.
  - Ein Tipp nennt das Land samt Sonnenzeit, hier Namibia. Esc schließt zuerst die Karte, dann die Ansicht. E, Plus und ein Tipp auf die Station führen hinein und zurück.
  - Angekommen bleibt die Blende 60 Bilder lang bei genau 1, und die Szene darunter wird in jedem dieser Bilder eingespart. Gegengeprüft: In Version 18 lagen 32 von 60 Bildern darunter, bis hinab auf 0,93.
  - Plus macht die Kugel 1,45-mal so groß und bleibt in der Erdansicht. Erst weitere Klicks über zweieinhalbfach hinaus führen zurück.
  - Ziehen um 150 Punkte zur Seite und 60 nach unten dreht die Kugel um genau 150 und 60 durch den Radius, im Bogenmaß. Die Station bleibt auf einen Punkt genau oben in der Mitte, in der Höhe, die zur neuen Neigung gehört. Die Kugel wird dafür neu gerechnet, und es öffnet sich nichts.
  - Die Beschriftung beugt nicht falsch. Auf dem Handy passt die Kugel zwischen Kopf und Leiste.
- **Überflug**:
  - Über Norditalien steht in den Stationswerten „Italien · 44° N · 12° O“.
  - Acht bekannte Orte werden richtig benannt: Berlin, Kairo, Mittelmeer, Atlantik, Lesotho, Nordsee, Tokio und Sydney.
  - Ein Tipp südlich davon nennt das Mittelmeer mit „15:50 Sonnenzeit · Tag“, ein zweiter Tipp schließt, und über der Kante gibt es keine Erde.
  - Um 14:30 UTC zeigt die Sonnenuhr in Greenwich 14:37, das ist die Zeitgleichung. Auf der Gegenseite bei 140 Grad Ost ist es 23:57 und Nacht.
- **Bodenspur**:
  - Die Karte ist 2 : 1, und der Punkt der Station liegt genau über dem Ort unter ihr.
  - Die Spur reicht bis ±51,6 Grad.
  - Um 14:30 UTC liegt Asien in der Nacht und der Atlantik unter der Sonne.
  - Ohne echte Erde gibt es weder Karte noch „Unter uns“.
- **Tempo**: 60 Bilder/s bei 0,8- bis 11-fachem Zoom und bei Nacht. Backzeit und Speicher sind unverändert.
- **Nacht**:
  - Gewitter: 19 Blitze in 12 s am Abend, keiner bei Tag, gegengeprüft.
  - Kobolde.
  - Sternschnuppen: je 200, keine im Sternhimmel.
  - Echte ISS: Die Antworten des Dienstes sind nachgebaut, mit den Feldern der echten API. Ausgeschaltet geht keine Anfrage hinaus. Eingeschaltet kommt die erste sofort, die nächste nach zwanzig Sekunden, nicht früher. Über Bayern steht „Deutschland · 48° N · 12° O · Tag“. Auf der Kugel liegt der Punkt auf 0,003 Bildpunkte genau an ihrer Stelle, zwischen den Antworten weitergerechnet. Fällt der Dienst aus, steht „nicht erreichbar“ da. Wieder ausgeschaltet kommt keine Anfrage mehr.
  - Meteorströme: Am 12. August um 20 Uhr UTC laufen die Perseiden mit elffacher Rate und stehen im Bordbuch, am 14. Dezember die Geminiden mit sechzehnfacher. Am 23. September läuft keiner.
  - Wolken von heute:
    - Das Bild des Dienstes ist nachgebaut: ein Infrarotbild wie das echte, mit Dunst, der zu den Polen hin heller wird, einem Wirbelsturm bei 20 Grad Nord und 60 West und einer Front bei 40 Grad Süd. Das echte Bild von heute früh ist nur für die Bilder benutzt.
    - Aus geht keine Anfrage hinaus. Ein kommt eine, die nächste nach drei Stunden, nicht früher, nach einem Fehler nach zehn Minuten, im Hintergrund nie. Ein einfarbiges Bild wird verworfen, die Wolken davor bleiben.
    - Angeglichen: Im Wirbelsturm stehen die Wolken bei 215 von 255, im Dunst daneben bei 33, die Aufnahme hat dort 58. Zwischen 52 und 58 Grad Nord liegt das Mittel bei 79, in der Aufnahme bei 76. Bei 75 und 80 Grad Nord und Süd ist jede Zeile genau die Aufnahme.
    - Die Wolkendecke deckt über dem Wirbelsturm zu drei Vierteln, das ist die volle Deckung dieser Schicht. Im Wirbelsturm liegen 49 Gewitterzellen, mit der Aufnahme 3.
    - Wieder aus ist die Kugel innen bildpunktgleich mit vorher, die Gewitterzellen und die Karte der Erde auch.
    - Gegengeprüft mit fünf absichtlich kaputten Fassungen: ohne Angleichen, ohne Übergang an den Polen, ohne Hochladen auf den Grafikchip, mit Gewitterzellen aus der Aufnahme und ohne Zurückschalten beim Ausschalten. Alle fünf schlagen an.
  - Weltraumwetter:
    - Die Antworten der NOAA sind nachgebaut, mit den Feldern der echten Dienste. Das Format ist an ihren echten Antworten von heute früh geprüft: Kp 0, Karte bis 12 %.
    - Aus geht keine Anfrage hinaus, auch nicht mit offener Kugel. Ein kommt sofort der Kp, die Karte nur mit offener Kugel. Danach alle fünf und zehn Minuten, nicht früher, nach einem Fehler nach einer Minute, im Hintergrund nie. Wieder aus kommt keine Anfrage mehr.
    - Kp 7,33 steht als „Kp 7+ · Sturm G3 · stark“ in den Stationswerten und im Bordbuch. Die Schreibweise stimmt an den Grenzen: 5− ist G1, 9− ist G4, 9 ist G5. Auch die ältere Tabellenform der Antwort wird gelesen.
    - Szene: Über Europa ist das Polarlicht am gewöhnlichen Tag 0,04 stark, bei Kp 7+ 1,69; über Kanada 0,67 und 2,4; am Äquator nie.
    - Kugel: Ein Fleck der Karte über Kansas liegt genau dort, 19,6 Stufen grüner. Zwanzig Grad östlich, westlich und südlich davon und auf dem gerechneten Oval ist nichts, höchstens 0,4. Über den Nullmeridian läuft ein Band ohne Naht, mit dem 1,07- und 1,16-fachen des Umfelds. Ohne Karte rückt das gerechnete Oval bei Kp 7+ entlang 100 Grad West von 59 auf 48 Grad Nord.
    - Ein Tipp auf die Nachtseite nennt „Polarlicht 45 %“, wo die Karte 45 hat.
    - Sonnenwind: Mit 283 km/s und dem Feld nach Norden steht „283 km/s · Feld nach Norden“ da, und die Vorhänge laufen mit der Bilduhr, ohne Zuschlag. Mit 620 km/s und 12 nT nach Süden laufen sie in einer Sekunde 2,27 Sekunden weit, erwartet 2,25, und das Bordbuch meldet es. Bei angehaltener Zeit verschiebt ein um fünf Sekunden verstellter Zuschlag die Vorhänge im nächsten Bild um 5,3 Stufen, ein Bild ohne Verstellen um 0,2. Gegengeprüft: Zählt das Feld auch nach Norden, oder zeichnet die Szene mit der Bilduhr statt mit der des Winds, schlägt der Test an.
    - Ausgeschaltet ist die Kugel innen bildpunktgleich mit Version 19, das Polarlicht der Szene auch. Im äußersten Bildpunkt der Kugel ist sie halb durchsichtig; dort schwankt schon Version 19 zwischen zwei gleichen Aufrufen um ein paar Stufen.
    - Gegengeprüft mit sechs weiteren absichtlich kaputten Fassungen: ohne Ausrichtung der Zeilen beim Hochladen, mit gespiegelter Breite, ohne angehängte Spalte, ohne Kp in der Szene, mit der Karte zusätzlich statt anstelle des Ovals und mit um 180 Grad verschobener Länge. Alle sechs schlagen an. Die fehlende Spalte fällt auf der Kugel mit dem 0,63-fachen des Umfelds auf.
  - Satellitenbilder:
    - Die Kacheln von Esri sind nachgebaut: einfarbig, rot bei ungerader Spalte, blau bei ungerader Zeile. So lässt sich an jedem Punkt der Kugel prüfen, ob dort die richtige Kachel liegt. Andere Adressen sind gesperrt.
    - Aus geht keine Anfrage hinaus. Der Zoom endet bei 2,4, und die Kugel bleibt dabei offen. Ein, bei der ganzen Kugel, geht auch keine hinaus, und es steht keine Quellenangabe da.
    - Zwanzig Schritte mit dem Mausrad auf einen Punkt neben der Mitte, bis 837-fach: Der Ort unter dem Zeiger bleibt in jedem Schritt auf 0,001 Bildpunkte stehen. Angefragt werden die Stufen 5 bis 12, höchstens acht zugleich. Die Wolken sind weg, die Zoomleiste zeigt „39 km“, und die Quellenangabe steht wirklich im Bild, gezählt an ihren hellen Punkten.
    - An 120 Stellen liegt die richtige Kachel, auch über die Datumsgrenze hinweg, dort bei Tag. Angefragt werden nur gültige Kacheln.
    - Ziehen verschiebt genau, null Bildpunkte daneben. Zurückgezogen geht keine neue Anfrage hinaus, und an 120 Stellen liegt wieder die richtige Kachel.
    - Alle Plätze für ungültig erklärt, ist das Bild dasselbe wie ganz ohne Kacheln (Abweichung 0); mit ihnen weicht es im Mittel um 105 Stufen ab.
    - Weit weg und zurück: Die sichtbaren Kacheln werden dabei aus dem Fenster verdrängt und kommen zurück aus dem Speicher, ohne eine einzige neue Anfrage, und liegen an 120 Stellen richtig.
    - Über der dicksten Gewitterzelle auf der Tagseite, im Kongo, ist die Stelle ohne Kacheln fast weiß (234 von 255). Hineingezoomt liegen dort an 120 Stellen die richtigen Kacheln frei.
    - Beim Hineinzoomen bis Stufe 12 gehen gut 410 Anfragen hinaus, nicht mehr als 520.
    - Hochkant wie auf dem Handy (390 × 844) ist das Fenster 8 × 16 Kacheln. Auch in den obersten und untersten Bildzeilen liegen 174 von 174 Stichproben richtig, und die Zoomleiste zeigt „25 km“.
    - Der Pfeil im Kreis bringt die ganze Kugel zurück. Aus in 427-facher Vergrößerung über Manhattan: Der Zoom geht auf 2,4, es geht keine Anfrage mehr hinaus, die Mitte bleibt über Manhattan, und Ziehen verschiebt weiter genau.
    - Die Rechnung für Ziehen und Zoomen ist zusätzlich außerhalb des Browsers geprüft, an 480.000 zufälligen Zügen: Wo es eine Lösung ohne Verdrehen gibt, liegt der gegriffene Ort auf 10⁻¹⁴ Radien genau. Nirgends springt das Bild; vorher tat es das an der Nahtstelle des Winkels.
    - Gegengeprüft mit elf absichtlich kaputten Fassungen: Zeilen gespiegelt, Spalten an der Datumsgrenze nicht umgebrochen, ohne Zoomanker, ohne Grenze für gleichzeitige Anfragen, Ziehen nach dem Ausschalten wie vorher, genähertes Verschieben, Wolken ohne Ausblenden, Quellenangabe nicht gezeichnet, ohne Speicher, leere Plätze zeigen die alte Kachel, und wieder das ganze Fenster statt des Sichtbaren (650 statt gut 410 Anfragen). Alle elf schlagen an, jede an der Stelle, die sie treffen soll; die gute Fassung bleibt grün.
  - Erde von gestern:
    - Das Bild der NASA ist nachgebaut: westlich von Greenwich magenta, östlich schwarz, also ohne Daten.
    - Aus geht keine Anfrage hinaus, auch nicht mit der ganzen Erde. Ein geht genau eine hinaus: Echtfarben von Suomi NPP, der 22. September am 23. um 16 Uhr UTC, die ganze Erde, 4096 × 2048, JPEG.
    - Im Westen gilt das Bild: magenta (190, 40, 190). Im Osten bleibt Blue Marble genau wie vorher. Über der dicksten Wolke der Aufnahme im Westen, vorher weiß (220, 225, 232), ist es jetzt magenta: keine zweiten Wolken. Es gilt für die Hälfte der Erde, und die Einstellung wird gemerkt.
    - Die Stationswerte zeigen „von gestern · 22.09. · Suomi NPP“. Am nächsten Tag geht genau eine neue Anfrage mit dem neuen Datum hinaus.
    - Ein leeres Bild wird verworfen, das letzte bleibt. Nach einem Fehler geht nach fünf Minuten nichts hinaus, nach elf genau eine Anfrage.
    - Aus kehrt Blue Marble bildpunktgenau zurück, und es geht keine Anfrage mehr hinaus.
    - Gegengeprüft mit sechs absichtlich kaputten Fassungen: Lücken schwarz statt Blue Marble, Wolken doppelt, das Bild von heute statt von gestern, leeres Bild übernommen, ohne Pause nach einem Fehler, Aus ohne Zurückschalten. Alle sechs schlagen an, jede an der Stelle, die sie treffen soll.
  - Der Rand bei Nacht: Gemalt wird nur der obere Rand einer Kugel mit 2000 Punkten Radius, damit die Schichten mehrere Punkte dick sind; oben auf der Kante liegt ein gewählter Ort, um 04:51 UTC zur magnetischen Mitternacht.
    - Über dem Oval (58 Nord, 72,7 West, 67 Grad magnetischer Breite): in 95 und 110 Kilometern grün (Grünwert 132 und 162), in 210 Kilometern rot, in 500 Kilometern schwarz.
    - Weit südlich davon (30 Nord): nur die schwache grüne Linie (47), darüber nichts. Bei Tag steht dort der blaue Luftsaum, in 95 Kilometern nicht grüner als in 110.
    - Gegengeprüft mit vier absichtlich kaputten Fassungen: ohne Nachthimmelsleuchten, ohne Polarlicht am Rand, grüne Linie auch bei Tag, ohne Rot. Alle vier schlagen an.
  - Scharfe Nachtlichter:
    - Das Bild der NASA ist nachgebaut: dunkler, bläulicher Grund und ein heller warmer Fleck mitten im Mittelmeer, wo die grobe Karte kein Licht hat. Andere Adressen sind gesperrt.
    - Ohne Satellitenbilder geht keine Anfrage hinaus, auch nicht bei 30-fachem Zoom. Mit ihnen bei der ganzen Kugel auch nicht.
    - Die Uhr der Seite steht, während neunmal gezoomt wird, und läuft nach jedem Schritt 150 ms weiter: dabei keine Anfrage. Steht der Blick, geht genau eine hinaus, mit Black Marble 2016 in Länge und Breite, und das Bild deckt den Fleck.
    - Der Fleck liegt genau dort: in seiner Mitte 240 von 255, einen halben Grad daneben in jede Richtung 4. Ohne die feine Karte ist es dort 4,7. Die Quellenangabe der NASA steht da.
    - Kleines Verschieben braucht kein neues Bild. Bei Tag geht keine Anfrage hinaus, und die Quellenangabe verschwindet.
    - Über der Datumsgrenze endet das Bild bei 180 Grad. Wieder aus: keine Anfrage, keine Quellenangabe.
    - Gegengeprüft mit acht absichtlich kaputten Fassungen: Breite gespiegelt, Länge verschoben, ohne Entprellen, auch bei Tag, ohne Quellenangabe, auch ohne Satellitenbilder, über die Datumsgrenze hinaus, altes Bild genügt immer. Alle acht schlagen an, jede an der Stelle, die sie treffen soll.
  - Kompass:
    - In der Szene und bei der ganzen Kugel ohne freien Blick ist er nicht zu sehen, zurück zur ganzen Kugel auch nicht mehr.
    - Steht Norden 60 Grad rechts von oben, zeigt die Nadel 60 Grad, und der Ort über der Mitte liegt nordwestlich.
    - Antippen dreht in mehreren Bildern, nicht in einem. Danach steht Norden genau oben, der Ort über der Mitte liegt genau nördlich, und die Mitte hat sich nicht bewegt.
    - Über dem Nordpol gibt es kein Norden: Der Knopf sagt das und dreht nicht.
    - Gegengeprüft mit drei absichtlich kaputten Fassungen: Nadel verkehrt herum, Drehung verschiebt die Mitte, Knopf bleibt nach dem Zurück stehen. Alle drei schlagen an.
  - Beschriftung über den Satellitenbildern:
    - Bilder und Schrift sind nachgebaut: jedes Bild einheitlich grau, jede Schrift ein weißes Quadrat mitten in ihrer Kachel, sonst durchsichtig. Andere Adressen sind gesperrt.
    - Voreingestellt an: Zu jeder der 42 Bildkacheln über München geht genau eine Schriftkachel derselben Stelle hinaus. In der Kachelmitte ist das Bild an 60 von 60 Stellen weiß, am Rand an keiner, und dort ist es an allen 1149 das graue Bild, nicht die Karte der NASA. Die Quellenangabe steht da.
    - Aus: keine neue Anfrage, überall grau, keine Quellenangabe, und das wird gemerkt. Wieder an: die Schrift aus dem Speicher, ohne neue Anfrage.
    - Nachts über Colorado, um vier Uhr früh: Der Rand ist an allen 1902 Stellen dunkel, die Schrift an 60 von 60 hell.
    - Fehlt die Schrift (404), liegt das Bild trotzdem an allen Stellen, ohne Fehler.
    - Auf dem Handy (390 Punkte breit) stehen die Angaben in vier Zeilen, jede höchstens 330 von 366 Punkten breit, ohne dass etwas fehlt.
    - Auf einem Retina-Schirm (doppelt scharf): 88 Bildkacheln der Stufe 11, dazu 24 Schriftkacheln der Stufe 10, keine doppelt. Das weiße Quadrat liegt an 60 von 60 Stellen in der Mitte der gröberen Kachel, also richtig ausgeschnitten.
    - Gegengeprüft mit zwölf absichtlich kaputten Fassungen: Schrift nicht gemalt, nachts dunkel, ohne Alphakanal, Bild verworfen, wenn die Schrift fehlt, Umschalten ohne neues Füllen, nicht gemerkt, ohne Quellenangabe, kein Umbruch am Komma, ganze Schriftkachel statt Ausschnitt, Ausschnitt vertauscht, gleiche Stufe auf Retina, jede Schrift einzeln geholt. Alle zwölf schlagen an, jede nur an der Stelle, die sie treffen soll.
    - Mit den echten Kacheln (mit curl geholt, siehe unten) über München, Rom, Manhattan und bei Nacht über Bayern angesehen.
  - Relief:
    - Bilder und Höhen sind nachgebaut: jedes Bild einheitlich grau, jede Höhenkachel ein Kamm von Nord nach Süd, links ein Westhang, rechts ein Osthang, gut 16 Grad steil. Beschriftung und Nachtlichter fehlen, andere Adressen sind gesperrt.
    - Über den Alpen (46,5 Nord, 10 Ost), 35 Bildkacheln der Stufe 10: dazu genau 12 Höhenkacheln der Stufe 9, keine doppelt, keine fehlt.
    - Morgens um 7:20 Uhr Sonnenzeit ist der Osthang 93,8 hell, der Westhang 21,7. Abends um 16:40 der Westhang 110,9, der Osthang 16,2. Mittags 145 zu 112: Der Westhang war bei der Aufnahme am Vormittag im Schatten und wird dafür aufgehellt; auf echten Bildern gleicht das den Unterschied aus, auf dem grauen hier sieht man ihn.
    - Aus: beide Hänge 57,5, keine Anfrage, gemerkt, keine Quellenangabe. Wieder an: aus dem Speicher, keine Anfrage, genau wie vorher.
    - Flaches Land, ein Meer mit Gefälle am Grund und fehlende Höhen (404) sehen an 900 Stellen aus wie ohne Relief, höchstens eine Stufe daneben. Fehlende Höhen zählen als Fehler des Reliefs, nicht des Bilds; das Bild liegt trotzdem.
    - Nachts ist alles dunkel.
    - Die Knöpfe „Erde von gestern“, „Beschriftung“ und „Relief“ unter Stationswerte sind gleich beim Start beschriftet. In Version 21 waren die ersten beiden leer, bis man den Knopf für die Wolken von heute drückte: Ihr Aufruf war beim Einbauen in dessen Handler gerutscht statt an den Start. Gegengeprüft mit genau dieser Fassung.
    - Gegengeprüft mit zwölf absichtlich kaputten Fassungen: ohne Schattierung, Osten verkehrt, Achsen vertauscht, Meeresboden statt Meeresspiegel, ohne das Licht der Aufnahme, Aus ohne Wirkung, jede Höhe einzeln geholt, Viertel vertauscht, Höhen in der Stufe der Bilder, Bild verworfen, wenn die Höhe fehlt, ohne Quellenangabe, flacher Boden verschoben. Alle zwölf schlagen an. „Aus ohne Wirkung“ blieb zuerst grün: Der Aus-Knopf holte alle Kacheln neu, weil im Test die Beschriftung fehlte und jeder Umschalter auch fehlende Schriften nachholte. Das ist behoben, und jetzt schlägt sie an.
    - Mit den echten Höhen und Bildern über den Alpen und den Dolomiten angesehen, morgens, mittags und abends, mit und ohne Relief.
    - Schlagschatten: Höhen nachgebaut als Ebene auf 500 Metern mit einer Mauer von 3000 Metern, nord-südlich. Bei 13,6 Grad Sonne ist ihr Schatten gut 10 Kilometer lang. Morgens liegt die Ebene westlich der Mauer bei 20 statt 57, abends östlich bei 17 statt 49; knapp hinter dem Ende des Schattens ist sie wieder so hell wie frei. Mittags und ohne Relief kein Schatten (höchstens ein halbes Prozent Unterschied). Gegengeprüft mit vier absichtlich kaputten Fassungen: ohne Schatten, zur falschen Seite, ohne den Anstieg des Strahls, Höhe falsch zusammengesetzt. Die letzte blieb zuerst grün, denn auch mit falschen Höhen war die Mauer höher als die Ebene; erst der Streifen hinter dem Ende des Schattens fängt sie.
  - Nähte im Nachthimmelsleuchten: 36 → 0,7.
  - Mondlicht: Neumond 11, Halbmond 16, Vollmond 35; die Tagseite bleibt gleich.
- **Nahansicht**:
  - Gaswolken: steilster Sprung 9 % statt 100 %, Bahnanhebung 4–9 statt 49 Stufen, Eiskörner bleiben Punkte (vorher 11 → 51 Punkte), gegengeprüft.
  - Haarlinien: bei 1152 Punkten Radius kein Strich unter einem Punkt, vorher 28.
- **Crew**: Diese Teile sind getestet und dort, wo es angegeben ist, gegengeprüft:
  - Leine: ein Aufruf ergibt einen Impuls, gegengeprüft.
  - Werkzeug in der Hand.
  - Schleuse: voller Bogen, Umkehr ohne Sprung.
  - Einsatzbericht, gegengeprüft.
  - Abgehakt und Bericht.
  - Puls der Crew, gegengeprüft.
- **Beschriftung**:
  - In drei Fenstergrößen liegt kein Schild außerhalb oder unter der Bedienung, und nichts überlappt.
  - Über einen Durchgang liegt kein Band auf einem fremden Namen oder einer Blase; ohne Ausweichen waren es 58 von 129 Proben, gegengeprüft.
  - Antippen trifft 9 von 9 Bauteilen.
  - Gedränge: Paare unter 30 Punkten Abstand fallen von 14 auf 6.
  - Lichthöfe bleiben fest bei 12–20 statt 21–92 Punkten.

**Bedienung**
- **Detailfenster**: Die Brücke meldet zehn Sekunden lang jede Sekunde dieselbe Familie aus zwei Sitzungen und zwei Unteragenten. Bei allen drei geöffneten Astronauten ändert sich der Text („vor 14 s“), aber kein Knoten wird ersetzt, und der erste Knopf ist hinterher noch derselbe. Ein Klick mit 400 ms langem Drücken auf einen Unteragenten, während die Brücke sich meldet, öffnet ihn. Gegengeprüft mit dem Stand davor: Dort blieb kein Knopf derselbe, und der lange Klick ging verloren. In der Crew-Leiste bleiben über sechs Meldungen alle neun Chips dieselben, vorher keiner. Doppeltippen auf Kepler mit einer Meldung zwischen den Tipps öffnet ihn, und auf dem Handy bleibt die gewischte Leiste stehen; beides war auch vorher so. familie.mjs lief vorher unter der Last von vier gleichzeitigen Erd-Tests dreimal von drei rot, jetzt dreimal grün.
- **Menü und Blenden**: Auf dem Rechner und dem Handy stehen die Schalter in der Reihenfolge KARTE, ERDE, LIVE. Jeder hat Titel, Symbol und Beschreibung, der Zustand in `aria-pressed` stimmt, und kein Titel bricht um. Ohne Satellitenbilder ruhen Beschriftung und Relief; eingeschaltet ruhen sie nicht mehr, und der Schieber steht 12 Punkte weiter rechts. Die Kurzanleitung hat 14 Karten, die erste offen; eine andere klappt auf (323 Punkte hoch) und wieder zu (0). Die offene Blende zeichnet mit 26 Punkten weich und hat den schimmernden Rand. Die Tests für echte ISS, Weltraumwetter, Wolken von heute und Relief lesen den Zustand jetzt aus `aria-pressed` statt aus der Aufschrift. Gegengeprüft mit acht absichtlich kaputten Fassungen: ohne `aria-pressed`, ohne Ruhen, alte Reihenfolge, alle Karten zu, Aufklappen ohne Wirkung, altes Glas, Titel brechen auf dem Handy um, Beschriftung und Relief folgen den Satellitenbildern nicht. Alle acht schlagen an.
- **Tastatur**:
  - Pfeile, N/P, W und Tab funktionieren.
  - Ein Ordnerpfad mit vier r lässt die Brücke offen.
  - Strg+R startet keinen Rundgang.
  - Die Leertaste drückt einen per Tab erreichten Knopf.
  Gegengeprüft.
- **Crew-Liste**: Nur geänderte Karten werden neu gebaut, und ein langer Tipp über einen Neuaufbau kommt an, gegengeprüft. Das Missions-Log trägt die Uhrzeit, gegengeprüft. Die Stationswerte decken am Handy das Vorführungsband nicht.
- **Öffnen und Sichern**: Öffnen über `vscode://file/…` ohne einen einzigen Befehl. Sichern geprüft mit Download, mit Ablehnung und ohne die Fähigkeit.
- **Kopfzeile**: Geprüft bei 16 Breiten von 340 bis 1280 Punkten, jeweils ohne Wartende, mit 2 und mit 12 Wartenden und in der Vorführung. Sie läuft nie über, kein Knopf wird zusammengedrückt, und wer wartet, bleibt als Zahl sichtbar. Gegengeprüft: Vorher lief sie in 81 dieser Fälle über, um bis zu 215 Punkte.
- **Ohne Karten ohne Service Worker**: Drei Tests sperren die Kartenbilder, um die gerechnete Erde zu prüfen. Der Service Worker der App lädt dieselben Bilder aber für den Betrieb ohne Netz vorab, und diese Anfragen gehen an der Sperre des Tests vorbei. Je nachdem, wer schneller war, kam die echte Erde dann doch. Die Seite handelt dabei richtig, deshalb laufen diese Tests jetzt ohne Service Worker.
- **Rundgang**: Elf Halte, der zehnte die Erde mit dem Ort darunter, der elfte die ganze Kugel; vorher ist sie nie an, danach wieder aus. Der Test wartet auf den Zähler „RUNDGANG n VON 11“ und nicht mehr auf die Uhr. Er fragte alle 9,2 Sekunden nach, ein Halt dauert aber 9,5. Bei langsamen Bildern kam er so beim zehnten Halt zu früh, mit 96 % auf dem neunten.
- Kein waagerechtes Scrollen bei 320 bis 760 px, keine Konsolen- oder Seitenfehler.

## Offene Punkte

- **Die Grenze des Abos kennt ORBIT nicht.** Anthropic veröffentlicht sie nicht, und wie die Teile (frisch, Zwischenspeicher, erzeugt) gegen sie zählen, ist ebenfalls nicht bekannt. Deshalb gibt es keinen Prozentwert, nur Zeit, Summe und Tempo. Dass ein Fenster zur vollen Stunde UTC beginnt, ist die Regel von ccusage, nicht eine von Anthropic.
- **Die Vorhersage für das Zuhause ist eine Verschiebung.** Wachsende, zerfallende und neue Zellen sieht sie nicht, und an Echtdaten ist sie nicht gegen das Wetter danach geprüft, nur an nachgebauten Fronten. Liegt das Fenster im Hintergrund, drosselt der Browser den Zeitgeber; ob das Mac-Programm dann noch meldet, ist auf einem Mac nicht ausprobiert.
- **Das Regenradar zeigt nur, wo Radare stehen**, also vor allem Europa, Nordamerika, Teile Asiens und Australien. Über dem Meer und in weiten Teilen Afrikas und Südamerikas gibt es nichts, auch wenn es dort regnet. Die Vorhersage (Nowcast) liefert RainViewer frei nicht mehr, es gibt nur die letzten zwei Stunden. Die Messwerte in Farbtafel 255 sind nicht beschrieben, sondern gemessen; fällt diese Tafel weg, bleibt der Rückfall über die Farben. Ob der Betrachter von claude.ai die Anfragen durchlässt, ist ungeprüft.
- **Die Ortsliste ist grob:** Städte ab 250.000 Einwohnern und Hauptstädte, nur im deutschsprachigen Raum auch kleinere. Adressen, Berge oder Sehenswürdigkeiten findet sie nicht. Einen Dienst im Netz zu fragen hätte mehr gefunden, aber ohne Netz nichts, und jede Suche wäre nach draußen gegangen.
- **Der Rückblick sucht höchstens 48 Stunden zurück** und erkennt eine Pause nur, wenn in ihr fünf Stunden lang keine Zeile mit Nutzung steht. Nur im Mac-Programm; nicht auf einem Mac gemessen, wie schnell Neutralino die Megabytes liefert.

- **VS Code meldet nicht selbst, welche Datei offen ist.** Dafür gibt es keine Schnittstelle. ORBIT leitet es aus Datei-Zeitstempeln ab, was in der Praxis fast immer zutrifft — aber reines Lesen oder ungespeichertes Tippen ist unsichtbar. Im Detailfenster steht ein Hinweis darauf.
- **Die Signatur ist nicht auf einem Mac geprüft.** Ob macOS 15 nach „Fertig“ tatsächlich „Dennoch öffnen“ anbietet statt „beschädigt“ zu melden, habe ich nicht gesehen, nur die Signatur selbst nachgerechnet. Der Weg über `xattr -cr` funktioniert in beiden Fällen.
- **Die Mitteilungen des Mac-Programms sind nicht auf einem Mac ausprobiert.** Neutralino benutzt dafür `NSUserNotificationCenter` bzw. `osascript`; ob ein unsigniertes Programm damit etwas anzeigt, weiß ich nicht. Der Fenstertitel funktioniert unabhängig davon. Ob ein verdecktes Fenster in WebKit seine Zeitgeber so weit drosselt, dass der Hintergrund-Durchlauf seltener läuft, ist ebenfalls ungeprüft.
- **Die echten Daten kamen aus einer Linux-Umgebung**, nicht von einem Mac: Protokollformat, Register und Verzeichnisaufbau sind dieselben, die Befehle `ps` und `stat` verhalten sich aber verschieden — deshalb stehen beide Schreibweisen im Code. In dieser Umgebung stand in `last-prompt` nur die allererste Eingabe; ob eine lokale Sitzung die Zeile bei jeder Eingabe fortschreibt, ist nicht geprüft.
- Dass das Agent-Werkzeug sein Ergebnis mit `agentId` im `toolUseResult` mitschreibt, ist angenommen — gesehen habe ich das Feld bei einem abgezweigten Skill. Fehlt es, greift die Vermutung aus dem Protokoll des Unteragenten.
- Die echten Claude-Aufrufe sind gegen einen nachgebauten Strom geprüft, nicht gegen den Dienst.
- **Die Aufgabenliste aus `TodoWrite` ist nicht an echten Daten geprüft**: in dieser Umgebung schreibt Claude Code die neuere Form, die Dateien unter `~/.claude/tasks/`. Das Format von `TodoWrite` (`todos` mit `content`, `status`, `activeForm`) ist aus der Beschreibung des Werkzeugs übernommen. Geteilte Listen eines Agententeams liegen unter dem Namen des Teams statt der Sitzung und erscheinen nicht.
- **Das Sichern im echten Betrachter ist nicht ausprobiert**, nur gegen einen nachgebauten; die Rückfrage des Betrachters ließ sich hier nicht auslösen.
- `ORBIT.app` ist gebaut und im Bundle verifiziert, aber nicht auf macOS gestartet — das war hier nicht möglich.
- Im Browser bleiben Sessions, Ordner und Prozesse leer. Die Brücken-Ansicht sagt das deutlich, statt still nichts anzuzeigen.
- **Die Figuren sind bewusst zu groß: 2,05-fach statt maßstäblich.** Ein Mensch im Anzug erscheint damit so groß wie 1,8 Modulradien statt 0,88. Maßstäblich wäre ein Astronaut neben einem 4,3-m-Modul ein Strich, und es geht in dieser App um die Leute, nicht um das Metall. Das ist die eine Lüge in der Szene, und sie steht im Code ausgeschrieben statt sich zu verstecken.
- Die Anzuguhr ist eine Entsprechung, keine Messung: sie legt die Laufzeit einer Sitzung auf die Vorräte eines echten Anzugs. Das steht unter dem Balken, damit niemand die Reserve für eine Warnung seines Rechners hält.
- Einschlagspuren bleiben stehen und sammeln sich an, sind aber echten Kratern entsprechend klein.
- Die Lichtrichtung der Szene ist eine Stilisierung. Deshalb sitzt an den Berührungsstellen Umgebungsverschattung statt geworfener Schatten: die hat keine Richtung und kann darum auch keine falsche haben.
- Die Bildraten sind in reiner Software-Rasterung gemessen (SwiftShader, ohne Grafikkarte) und damit der schlechteste Fall. Bei 24 Figuren liegt sie dort bei 37 statt 60, bei Nacht und 1400 × 900 Punkten bei 23.
- **Der flüssige Boden ist auf einem Mac nicht gemessen.** Die Regelung misst dort selbst, was das Zusammensetzen kostet; hier ließ sich nur die Software-Rasterung messen, und dort kostet er bei doppelter Auflösung zwei Bilder je Sekunde.
- **Die Erde ist echt, die Bahn nicht.**
  - Die Station fliegt eine Bahn mit der Neigung der ISS, aber nicht die echte ISS an ihrer echten Stelle. Wo die echte ist, zeigt ORBIT auf Wunsch zusätzlich an; die Szene selbst folgt ihr nicht.
  - Ob wheretheiss.at aus dem Betrachter von claude.ai heraus erreichbar ist, habe ich nicht geprüft. Dort könnte die Seite fremde Adressen sperren; dann steht „nicht erreichbar“ da.
  - Dasselbe gilt für die Dienste der NOAA. Ich habe sie hier nur mit curl erreicht, nicht aus dem Browser, denn dem Testbrowser fehlt hier der Weg nach draußen. Geprüft ist das Format an ihren echten Antworten.
  - OVATION sagt, wie wahrscheinlich Polarlicht vom Boden aus zu sehen ist, nicht wie hell es von oben aussieht. Die Umrechnung in Helligkeit habe ich gewählt, sie ist nicht gemessen.
  - Der Umlauf ist zwölffach gerafft, die Sonne läuft in Echtzeit. Deshalb verschiebt sich die Bahn von Runde zu Runde nur um knapp zwei Grad statt um 23.
  - Die Wolken sind eine Aufnahme, kein Wetter von heute; die von heute gibt es auf Wunsch. Sie hängen an einem privat betriebenen Dienst (Live Cloud Maps), nicht an EUMETSAT selbst. Fällt er weg, bleiben die zuletzt geladenen Wolken bis zum Neuladen der Seite, danach die Aufnahme. Angeglichen ist die Menge je Breite, nicht die wirkliche Dicke: Eine dünne, kalte Schleierwolke kann heller herauskommen als eine dicke, warme.
  - Auf einem Mac mit Grafikchip ist die Erde nicht gemessen, nur in Software-Rasterung.
  - **Die Schlagschatten sind so fein wie die Höhen und reichen nur so weit wie das geladene Fenster.** Ein Grat, der außerhalb der geladenen Kacheln liegt, wirft keinen Schatten herein, und über gut drei Kacheln hinaus sucht der Strahl nicht. Wolken werfen ihre Schatten weiter nur über der Karte der NASA. Wann ein Bild aufgenommen wurde, weiß ORBIT nicht, es nimmt halb elf im Sommer an. Wo das nicht stimmt, bleibt mittags ein Rest der alten Schatten oder kommt ein wenig zu viel dazu. Der Strahl kostet je Bildpunkt 48 Texturzugriffe, aber nur bei tiefer Sonne und nur wo Satellitenbilder liegen.
  - **Die Beschriftung dreht sich mit der Karte.** Sie ist in die Kacheln gemalt, nicht wie bei Google Earth eigene Schrift auf dem Schirm. Steht Norden nicht oben, steht sie schief; der Kompass dreht Norden mit einem Tipp wieder nach oben. Auf dem Retina-Schirm ist sie hochgerechnet und darum etwas weicher als das Bild. Die Namen sind die von Esri, oft zweisprachig („München Munich“, „Roma Rome“), und die Grenzen der Landkreise sind dicht.
  - **Die Satellitenbilder hängen an Esri.** Der Dienst ist ohne Schlüssel erreichbar, aber Esri regelt den Zugang und kann ihn ändern. Getestet ist mit nachgebauten Kacheln. Die echten habe ich hier mit curl geholt und dem Testbrowser untergeschoben, denn dem fehlt der Weg nach draußen. Ob der Betrachter von claude.ai fremde Bilder lädt, ist nicht geprüft.
  - Die Bilder sind ein Mosaik vieler Aufnahmen aus verschiedenen Jahren. Helligkeitssprünge an ihren Nähten und unscharfe Flecken stammen von Esri, das habe ich an den rohen Kacheln nachgesehen.
  - **Die Erde von gestern ist ein Mosaik aus vierzehn Überflügen.** An den Nähten stoßen Aufnahmen verschiedener Stunden aneinander, dort springen Wolken und Helligkeit, etwa als gerade Kante über Arabien. Über den tropischen Meeren liegt in jedem Überflug ein heller Streifen der Sonnenspiegelung, schwach auch auf der Kugel. Beides stammt aus dem Bild selbst; herausrechnen ließ es sich nicht sauber. Die Wolken sind die von gestern Mittag Ortszeit, nicht die von jetzt.
  - Die scharfen Nachtlichter sind die von 2016, nicht die von heute; neue Siedlungen fehlen. Wie hell sie herauskommen, habe ich an München geeicht, nicht gemessen. Ob GIBS aus dem Betrachter von claude.ai heraus erreichbar ist, ist so ungeprüft wie bei Esri; hier habe ich die echten Bilder mit curl geholt. Auch mit einem halben Kilometer je Punkt ist eine Stadt bei tiefem Zoom ein weicher Fleck, keine Straßen.
  - Die Scheibe unter der Station bleibt bei der Karte der NASA. Sie wird flach von der Seite gesehen und nur alle zwei Sekunden gerechnet, dort brächten die Kacheln wenig.
- **Fortsetzen ist nicht auf einem Mac ausprobiert.** Die Zwischenablage über Neutralino ist gegen die mitgelieferte Client-Bibliothek geprüft, nicht im laufenden Programm. Das Quoten ist in bash, dash und sh ausgeführt. zsh, die Standard-Shell des Mac, war hier nicht installiert: Sie behandelt einfache Anführungszeichen gleich, ausprobiert ist es aber nicht. Wie `claude --resume` mit einer Sitzung umgeht, die noch in einem anderen Terminal offen ist, habe ich nicht geprüft. ORBIT bietet den Befehl in diesem Fall deshalb gar nicht an.

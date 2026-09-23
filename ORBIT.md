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

### Wie voll, wofür, und wer noch mitläuft

- **Kontext.** Jeder Assistenteneintrag im Protokoll führt mit, wie groß der Prompt beim letzten Aufruf war. Frisch gesendet plus neu zwischengespeichert plus aus dem Zwischenspeicher gelesen ist der belegte Kontext — abgerechnet, nicht geschätzt. Daneben steht der Anteil aus dem Zwischenspeicher und, wenn es welche gab, die Denk-Tokens des letzten Aufrufs. Gezählt wird nur der neueste Eintrag: die Frage ist, wie voll die Sitzung gerade ist, nicht was sie insgesamt verbraucht hat.
- **Auftrag und zuletzt Gesagtes.** Der Auftrag kommt aus der Zeile `last-prompt`, sonst aus dem jüngsten Benutzereintrag — eingefügte Bilder, Programmmeldungen und `isMeta`-Einträge zählen nicht. Er steht vor der Tätigkeit: erst wo, dann wofür, dann was. Darunter als Zitat, was die Sitzung zuletzt gesagt hat; bei einer wartenden oft genau die Erklärung, worauf.
- **Unteragenten.** Schickt eine Sitzung einen Agenten los, schreibt der ein eigenes Protokoll unter `<sitzung>/subagents/`, die Agenten eines Arbeitsablaufs eine Ebene tiefer unter `subagents/workflows/<lauf>/`. Jeder wird ein eigener Astronaut mit dem Zeichen ↳. Sein Name kommt aus der `description` in der `.meta.json` daneben, sonst aus den ersten Wörtern seiner Aufgabe ohne Füllwörter („Tests Warenkorb", nicht „Die Tests für"). Höchstens sechs je Sitzung, nur frische. Die Kennung kommt aus `agentId` — die `sessionId` eines Unteragenten ist die seiner Mutter-Sitzung. Er trägt den Namen, unter dem man seine Sitzung in der Szene sieht, auch wenn das Register sie umbenannt hat; das Detail der Sitzung nennt ihre Unteragenten, ein Tipp fährt hin.
- **Fertig, berichtet, abgebrochen.** Sicher fertig ist ein Unteragent, sobald die Sitzung sein Ergebnis hat — sie schreibt es mit seiner `agentId` im `toolUseResult` mit. Sonst gilt er als fertig, wenn sein Protokoll mit dem Bericht endet (Text ohne Werkzeugaufruf danach, oder `StructuredOutput` bei Arbeitsabläufen) und seit einer Viertelminute nichts dazukam. Der Bericht steht grün gerandet im Detail. Ein Eintrag mit `model: "<synthetic>"` und `isApiErrorMessage` ist kein Bericht, sondern ein Abbruch durch Claude Code selbst, etwa ein Nutzungslimit — er steht wörtlich da, rot. Die Anzuguhr eines fertigen oder abgebrochenen Unteragenten bleibt beim letzten Lebenszeichen stehen.
- **Störung des Dienstes.** Lehnt der Dienst eine Anfrage ab, schreibt Claude Code einen Eintrag `api_error` ins Protokoll und wiederholt — an einem echten nachgesehen: `"formatted": "529 Overloaded"`, `retryAttempt`, `maxRetries`. Eine solche Sitzung wartet auf den Dienst und arbeitet nicht, sah aber aus wie mitten in der Arbeit. Steht die Störung nach dem letzten Eintrag des Assistenten und ist sie frisch, heißt die Tätigkeit jetzt „Dienst überlastet — Versuch 2 von 10", im Detail steht der Wortlaut, und die Figur hält die Hand an den Helm, während an der Sprechkappe eine Leuchte bernstein blinkt. Überlastet, Anfragegrenze, gestört und keine Verbindung werden unterschieden.
- **Verdichtet.** Ebenso `compact_boundary`: unter dem Kontext steht „Verdichtet vor 50 Min. · automatisch · 787.738 → 17.212 Tokens" — danach kennt die Sitzung ihren Verlauf nur noch als Zusammenfassung. Die Zeile steht nur eine Weile im gelesenen Ende, also wird sie gemerkt; eine neue Verdichtung kommt einmal ins Bordbuch.
- **Funkstrecke.** Zwischen Sitzung und Unteragent liegt ein dünner gestrichelter Bogen. Die Punkte darauf laufen zum Unteragenten, solange er arbeitet, und zurück zur Sitzung, wenn er berichtet hat. Er liegt in Bildpunkten über der Szene wie die Namen, beginnt am Rand der Figuren, hat einen dunklen Saum und wird hell, wenn eine der beiden gewählt ist.

Alle Feldnamen sind an echten Protokollen geprüft und nicht aus der Doku übernommen.

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
  - Die Bahn läuft als Ellipse um die Kugel, in echter Höhe: 420 über 6371 Kilometern. Hinter der Kugel ist sie verdeckt, vor der Station heller als hinter ihr.
  - Oben auf der Bahn steht die Station als heller Punkt. Maßstäblich wäre sie von hier aus nicht einmal ein Bildpunkt. Darüber steht, wer an Bord ist und was unter ihr liegt, etwa „Unter uns: Atlantischer Ozean“. Die Namen kommen aus einer Liste ohne Artikel; „über Atlantischer Ozean“ wäre falsch gebeugt, deshalb der Doppelpunkt.
  - **Ziehen dreht die Kugel.** Was man greift, geht mit dem Finger: seitwärts um die Station herum, hoch und runter gekippt, von fast senkrecht über ihr bis flach von der Seite. Die Station bleibt dabei oben in der Mitte. Beim nächsten Hineinzoomen steht die Kamera wieder fünfzig Grad schräg.
  - **Zoomen zoomt die Kugel.** Mausrad, zwei Finger und Plus machen sie bis zu zweieinhalbmal so groß oder halb so klein. Wer darüber hinaus weiter hineinzoomt, kommt zur Station zurück. Hineingezoomt rechnet der Schattierer höchstens 2048 Punkte je Seite, den Rest zieht der Browser hoch.
  - Ein Tipp auf die Kugel nennt Land oder Meer mit Sonnenzeit. Ein Tipp auf die Station, Esc, Doppelklick und die Leertaste führen zurück, ebenso der Sprung zu einem Astronauten. Esc schließt zuerst die Karte zum angetippten Ort.
  - Die Überblendung läuft nach der Uhr und nicht nach Bildern. Eine Blende mit festem Schritt je Bild stand ohne Grafikchip nach Sekunden noch auf halbem Weg, und die Station schimmerte durch die Erde.
  - Liegt die Kugel ganz über allem, wird die Station nicht gezeichnet. Was an Bord läuft, läuft weiter. Die Kugel selbst wird nur neu gerechnet, wenn sie sich um einen halben Bildpunkt gedreht hat, und alle zwei Sekunden für die Sonne.
  - Auf dem Handy bestimmt die Breite die Größe: Die Bahn reicht links und rechts ein Fünfzehntel über die Kugel hinaus und passt noch ins Bild.
- **Die echte ISS, auf Wunsch.** Die Station hier fliegt eine Bahn wie die ISS, aber nicht die echte an ihrer echten Stelle. Wer sehen will, wo die gerade ist, schaltet es unter Stationswerte ein.
  - Dann fragt ORBIT alle zwanzig Sekunden bei wheretheiss.at nach, einem öffentlichen Dienst ohne Schlüssel, der Browsern die Antwort erlaubt. Mitgeschickt wird nichts als die Anfrage selbst.
  - Ausgeschaltet geht keine einzige Anfrage hinaus. Gefragt wird nur, solange die Stationswerte oder die ganze Erde offen sind.
  - In den Stationswerten steht, worüber sie fliegt, mit Breite, Länge und ob dort Tag ist. In der ganzen Erde erscheint sie als zweiter, türkiser Punkt in ihrer echten Höhe.
  - Zwischen zwei Antworten läuft sie auf dem Großkreis durch die letzten beiden Punkte weiter. Als Zeit gilt die eigene Uhr beim Empfang, nicht der Zeitstempel des Dienstes: Geht die Uhr des Rechners ein paar Minuten falsch, wäre die Antwort sonst sofort zu alt. Nach zwei Minuten ohne Antwort steht „nicht erreichbar“ da.
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

Bei vielen Astronauten greifen zwei Grenzen: höchstens elf Namensschilder (auf schmalen Schirmen fünf), sortiert nach Zustand, die verfolgte Figur fällt nie heraus; und wo sich mehrere einen Arbeitsplatz teilen müssen, rücken sie quer zur Fläche auseinander statt übereinander zu stehen.

## Tempo

Alles Unbewegliche wird einmal in ein Bild gebacken und danach nur noch kopiert, gestuft nach einer festen Auflösungsleiter mit Hysterese. Kopiert wird streifenweise und nur das, was auf dem Schirm landet.

Die beweglichen Teile werden **gedreht gebacken**. Das ist der Trick hinter der Geschwindigkeit: ein Bild, das beim Kopieren nur noch gestaucht und verschoben wird, läuft über den schnellen Weg der Leinwand; kommt eine Drehung dazu, muss für jeden Zielbildpunkt die Umkehrabbildung gerechnet werden — gemessen kostete das die halbe Bildrate.

Beim starken Heranfahren werden Kanten und Nähte live nachgezogen: Verläufe verlieren beim Vergrößern nichts, Linien alles. Aus der Stelle im Umlauf werden höchstens **zwei** Bilder überblendet statt dreien.

Figuren ganz außerhalb des Bildes werden nicht gemalt, nur gerechnet. Mit den Detailstufen nach Schirmgröße zusammen, vorher gegen nachher abwechselnd gemessen bei 24 Figuren: herausgezoomt auf dem Desktop 33 → 38 Bilder je Sekunde, bei Zoom 1 und 3 unverändert, am Handy bei Zoom 1 unverändert und bei Zoom 3 39 → 37 — dort erscheinen jetzt die feinen Details.

## Mac-Programm

`desktop/orbit/` baut `ORBIT.app`, fertig in `download/ORBIT-mac.zip`. Universal Binary für Apple Silicon und Intel, eigenes Icon in acht Auflösungen.

Es liest alles über Neutralinos Datei- und Befehls-API — **kein Node nötig**. Die Berechtigungen sind bewusst eng: nur lesende Dateizugriffe, `execCommand`, `getPath`, `open`, der Ordnerdialog, `showNotification` für die Meldungen und `clipboard.writeText` für den Befehl zum Fortsetzen. Keine Schreibrechte auf Dateien.

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

79 Tests mit Playwright, ohne echte API-Kosten. Die ganze Reihe läuft gegen einen eingefrorenen Stand. Wo „gegengeprüft“ steht, schlägt der Test gegen die alte oder eine absichtlich kaputte Fassung an.

**Daten und Brücke**
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
- **Tastatur**:
  - Pfeile, N/P, W und Tab funktionieren.
  - Ein Ordnerpfad mit vier r lässt die Brücke offen.
  - Strg+R startet keinen Rundgang.
  - Die Leertaste drückt einen per Tab erreichten Knopf.
  Gegengeprüft.
- **Crew-Liste**: Nur geänderte Karten werden neu gebaut, und ein langer Tipp über einen Neuaufbau kommt an, gegengeprüft. Das Missions-Log trägt die Uhrzeit, gegengeprüft. Die Stationswerte decken am Handy das Vorführungsband nicht.
- **Öffnen und Sichern**: Öffnen über `vscode://file/…` ohne einen einzigen Befehl. Sichern geprüft mit Download, mit Ablehnung und ohne die Fähigkeit.
- **Kopfzeile**: Geprüft bei 16 Breiten von 340 bis 1280 Punkten, jeweils ohne Wartende, mit 2 und mit 12 Wartenden und in der Vorführung. Sie läuft nie über, kein Knopf wird zusammengedrückt, und wer wartet, bleibt als Zahl sichtbar. Gegengeprüft: Vorher lief sie in 81 dieser Fälle über, um bis zu 215 Punkte.
- **Rundgang**: Elf Halte, der zehnte die Erde mit dem Ort darunter, der elfte die ganze Kugel; vorher ist sie nie an, danach wieder aus. Der Test wartet auf den Zähler „RUNDGANG n VON 11“ und nicht mehr auf die Uhr. Er fragte alle 9,2 Sekunden nach, ein Halt dauert aber 9,5. Bei langsamen Bildern kam er so beim zehnten Halt zu früh, mit 96 % auf dem neunten.
- Kein waagerechtes Scrollen bei 320 bis 760 px, keine Konsolen- oder Seitenfehler.

## Offene Punkte

- **VS Code meldet nicht selbst, welche Datei offen ist.** Dafür gibt es keine Schnittstelle. ORBIT leitet es aus Datei-Zeitstempeln ab, was in der Praxis fast immer zutrifft — aber reines Lesen oder ungespeichertes Tippen ist unsichtbar. Im Detailfenster steht ein Hinweis darauf.
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
  - Der Umlauf ist zwölffach gerafft, die Sonne läuft in Echtzeit. Deshalb verschiebt sich die Bahn von Runde zu Runde nur um knapp zwei Grad statt um 23.
  - Die Wolken sind eine Aufnahme, kein Wetter von heute.
  - Auf einem Mac mit Grafikchip ist die Erde nicht gemessen, nur in Software-Rasterung.
- **Fortsetzen ist nicht auf einem Mac ausprobiert.** Die Zwischenablage über Neutralino ist gegen die mitgelieferte Client-Bibliothek geprüft, nicht im laufenden Programm. Das Quoten ist in bash, dash und sh ausgeführt. zsh, die Standard-Shell des Mac, war hier nicht installiert: Sie behandelt einfache Anführungszeichen gleich, ausprobiert ist es aber nicht. Wie `claude --resume` mit einer Sitzung umgeht, die noch in einem anderen Terminal offen ist, habe ich nicht geprüft. ORBIT bietet den Befehl in diesem Fall deshalb gar nicht an.

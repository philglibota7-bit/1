# Motive automatisch ausspielen

Posten über die offiziellen Schnittstellen ist erlaubt und ausdrücklich
vorgesehen. **Konten anlegen** ist es nicht — das verbieten Meta und Pinterest
in ihren Bedingungen, und dieses Werkzeug tut es auch nicht.

```bash
node werkzeuge/posten/posten.mjs                    # Probelauf über alles
node werkzeuge/posten/posten.mjs --kanal pinterest  # nur ein Kanal
node werkzeuge/posten/posten.mjs --nur pumpe-pin-8-szene
node werkzeuge/posten/posten.mjs --kanal pinterest --los   # wirklich senden
```

Ohne `--los` wird nichts gesendet. Der Probelauf zeigt Bild, Titel und Ziel
jedes Beitrags, so wie er abginge.

## Was vorher stehen muss

**1. Die Bilder müssen öffentlich liegen.** Instagram und Pinterest laden die
Datei selbst herunter — Metas Doku sagt es wörtlich: „the media must be hosted
on a publicly accessible server at the time of the attempt." Ein Pfad auf
deiner Festplatte nützt ihnen nichts. Sobald PR #27 in `main` gemerged ist,
liefert GitHub Pages sie unter `philglibota7-bit.github.io/1/…`; genau diese
Adressen stehen im Plan. Vorher schlägt jeder echte Lauf fehl.

**2. Konten und Rechte.**

| Kanal | Konto | Rechte |
|---|---|---|
| Instagram | Professional (Business oder Creator), mit einer Facebook-Seite verbunden | `instagram_basic`, `instagram_content_publish`, `pages_read_engagement` |
| Facebook | Seite, keine Privatchronik | `pages_manage_posts` |
| Pinterest | Unternehmenskonto | `pins:write`, `boards:read` |

Bei Meta reicht für die eigenen Konten der Entwicklungsmodus der App, solange
du selbst als Administrator eingetragen bist. Erst wenn du für fremde Konten
posten willst, kommt die App-Prüfung dazu.

**3. Schlüssel in der Umgebung**, nie in einer Datei im Ordner:

```bash
export PINTEREST_TOKEN=…      export PINTEREST_BOARD_ID=…
export META_TOKEN=…           export IG_USER_ID=…    export FB_PAGE_ID=…
```

`gesendet.json` und alles, was nach Zugangsdaten aussieht, gehören in
`.gitignore` — nichts davon darf je eingecheckt werden.

## Grenzen, die im Werkzeug schon berücksichtigt sind

- **Instagram: 100 Beiträge in 24 Stunden.** `--hoechstens` begrenzt zusätzlich
  pro Lauf, Voreinstellung 5 — lieber langsam anfangen.
- **Instagram macht Links im Text nicht anklickbar.** Die Adresse gehört ins
  Profil. Im Beitragstext steht sie deshalb nicht mit drin, auf Facebook schon.
- **Zweimal dasselbe** wird nicht gesendet: was durchging, steht in
  `gesendet.json`, ein zweiter Lauf überspringt es.
- **Zwei Sekunden Pause** zwischen den Aufrufen.

## Was noch fehlt

`plan.json` führt 29 Motive, aber nur die neun Pumpen-Pins haben Titel, Text
und Alternativtext. Die anderen 20 stehen als `"fertig": false` drin und werden
übersprungen, statt leer hochgeladen zu werden. Texte dazuschreiben heißt:
`plan-bauen.py` ergänzen und neu laufen lassen.

## Ungeprüft

Metas Endpunkte habe ich gegen die aktuelle Doku abgeglichen. **Pinterests
Referenz liegt hinter einer Anmeldung** — der Aufruf in `posten.mjs` folgt der
v5-Doku aus zweiter Hand. Vor dem ersten echten Pinterest-Lauf gegen die
Referenz prüfen; der Probelauf zeigt genau, was gesendet würde.

# Hygge & Co. — Editorial Cozy Shop 🕯️

Eine interaktive Verkaufs-Website im Premium-Editorial-Stil: XXL-Typografie,
Vollbild-Hero, Chevron-Bildmasken, riesige klickbare Kategorie-Wörter und ein
dunkler Footer mit gigantischer Wortmarke — gepaart mit warmem, „cozy" Look.
Komplett mit Platzhalter-Inhalten: Texte, Preise, Emojis und Farben einfach
austauschen.

## Öffnen

Einfach `index.html` im Browser öffnen — funktioniert auch direkt am Handy.
Keine externen Bibliotheken, kein Build-Schritt.

## Features

- 🖤 **Editorial-Design**: XXL-Headlines, Serifen-Akzente, helle & dunkle Sektionen im Wechsel
- 🎬 **Cineastische Motion**: Wort-für-Wort-Hero-Reveal, Parallax, gestaffelte Chevrons, Scroll-Reveals
- 🔤 **Wortmarke mit Farbverlaufs-Durchblick** (`background-clip: text`)
- 🛍️ **Voll funktionsfähiger Warenkorb** — Hinzufügen, Menge ändern, Summe
- 🔎 **Kategorie-Filter** — auch über die XXL-Kategorie-Wörter klickbar
- ❤️ **Merken/Favoriten** pro Produkt
- 📈 **Animierte Statistik-Zähler** & Lauftext-Ticker
- 🌗 **Hell-/Dunkelmodus** mit Umschalter (merkt sich die Auswahl)
- 💌 **Newsletter-Formular** mit Validierung
- 📱 **Voll responsiv** — mobile-first
- ♿ Berücksichtigt `prefers-reduced-motion`

## Dateien

| Datei         | Zweck                          |
|---------------|--------------------------------|
| `index.html`  | Struktur & Inhalt              |
| `styles.css`  | Design, Farben, Animationen    |
| `app.js`      | Warenkorb, Filter, Interaktion |

## Anpassen

- **Produkte:** Array `PRODUCTS` in `app.js`
- **Bewertungen:** Array `TESTIMONIALS` in `app.js`
- **Farben:** CSS-Variablen unter `:root` und `[data-theme="dark"]` in `styles.css`
- **Sektionen:** klar kommentierte Blöcke in `index.html`

Alles Platzhalter — viel Spaß beim Umbauen! 💛

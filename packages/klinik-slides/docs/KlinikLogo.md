---
category: Marke
---

# KlinikLogo — Wort-/Bildmarke

Die Marke im Folienkopf und auf der Abschlussfolie. Mit `src` wird die offizielle
Logodatei ausgegeben, ohne `src` eine Textmarke in Klinik-Blau und Akzentrot.

## Verwendung

```jsx
{/* Regelfall: offizielle Logodatei */}
<KlinikLogo src="/assets/kliniken-sha-logo.svg" size={3} />

{/* Ersatz ohne Datei: Textmarke */}
<KlinikLogo />

{/* Auf tiefblauer Folie */}
<KlinikLogo variant="white" />
```

Innerhalb der Folientypen ist das Logo eingebaut — dort genügt `showLogo` und
optional `logoSrc`:

```jsx
<ContentSlide title="…" showLogo logoSrc="/assets/kliniken-sha-logo.svg">…</ContentSlide>
```

## Hinweise

- Die Textmarke ist ein Platzhalter, kein Ersatz für das echte Logo. Sobald die
  offizielle Datei vorliegt, `logoSrc` an den Folientypen setzen — dann ist sie
  überall gleichzeitig ausgetauscht.
- `variant="white"` auf tiefblauen Folien; die farbige Marke verliert dort den
  Kontrast.
- `size` ist in Folienbreiten-Prozent (`cqw`) angegeben, damit die Marke mit der
  Folie skaliert. Standard 2,6 ≈ 33 px bei Folienbreite 1280 px.
- Das Logo gehört einmal pro Folie oben rechts — nicht zusätzlich in die Fußzeile.
  Auf Titel- und Abschlussfolie ist es bereits gesetzt.
- Wort- und Bildmarke nicht nachbauen oder verändern: Farbe, Schnitt und
  Abstände sind Bestandteil des Corporate Designs.

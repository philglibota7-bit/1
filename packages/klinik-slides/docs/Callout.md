---
category: Inhalte
---

# Callout — Hinweisbox

Abgesetzter Kasten für Merksätze, Fristen, Risiken und Beschlüsse. Farbe und
Symbol richten sich nach dem Charakter der Aussage.

## Verwendung

```jsx
<Callout title="Beschlussvorschlag" tone="info">
  Der Aufsichtsrat stimmt der gemeinsamen Notaufnahme-Struktur ab dem
  dritten Quartal 2026 zu.
</Callout>

<Callout title="Frist" tone="warning">
  Die Meldung an das Landesamt muss bis zum 31. März erfolgen.
</Callout>

<Callout title="Zielwert erreicht" tone="success">
  Die Verweildauer liegt mit 4,3 Tagen unter dem Zielwert von 4,5 Tagen.
</Callout>
```

## Hinweise

- `critical` (Rot) ist echten Risiken vorbehalten — Fristablauf mit Folgen,
  Personalengpass, Meldepflicht. Inflationär eingesetzt verliert Rot auf
  Klinikfolien seine Wirkung.
- `tone="neutral"` für Definitionen und Abgrenzungen ohne Wertung.
- Eine Hinweisbox pro Folie. Zwei Kästen nebeneinander konkurrieren um genau die
  Aufmerksamkeit, die der Kasten erzeugen soll.
- `compact` für Randbemerkungen unter einer Tabelle oder einem Diagramm.
- Der Kasten ersetzt keine Fußnote: Datenstand und Definitionen gehören in
  `footnote` der `ContentSlide`.

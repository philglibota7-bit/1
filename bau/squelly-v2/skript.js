document.documentElement.classList.add("js");

/* ══════════════════════════════════════════════════════════════════════
   HIER ANPASSEN — Partner-Kürzel und die Produkte
   ══════════════════════════════════════════════════════════════════════ */
const PARTNER_TAG = "squelly-21";
const AMAZON_DOM  = "amazon.de";
/* Solange DEMO_PREISE auf true steht, sind alle Preise Beispielwerte und
   die Karten sagen das auch. Echte Preise dürfen als Partner nur aus der
   Produkt-Schnittstelle kommen und müssen regelmäßig erneuert werden. */
const DEMO_PREISE = true;

const PRODUKTE = /*DATEN*/;

/* ══════════════════════════════════════════════════════════════════════
   Herkunft: kommt jemand über eine Anzeige, steckt das in der Adresse.
   Es wandert in die SubID des Amazon-Links und taucht im Provisions-
   bericht wieder auf — nur so ist zu sehen, welches Motiv verkauft hat.
   ══════════════════════════════════════════════════════════════════════ */
const kurz = function(v, n){
  return String(v || "").toLowerCase().replace(/[^a-z0-9]+/g, "").slice(0, n || 12);
};
const HERKUNFT = (function(){
  let h = null;
  try{
    const q = new URLSearchParams(location.search);
    if(q.get("utm_source")){
      h = { quelle: kurz(q.get("utm_source")), kampagne: kurz(q.get("utm_campaign"), 16),
            motiv: kurz(q.get("utm_content"), 22) };
      sessionStorage.setItem("squelly_herkunft", JSON.stringify(h));
    } else {
      h = JSON.parse(sessionStorage.getItem("squelly_herkunft") || "null");
    }
  }catch(e){}
  return h || { quelle: "direkt", kampagne: "", motiv: "" };
})();

function subId(p){
  return ["sq", HERKUNFT.quelle, HERKUNFT.kampagne || "ohne",
          HERKUNFT.motiv || "seite", p.kuerzel].join("-").slice(0, 100);
}
function amazonLink(p){
  const b = p.asin
    ? "https://www." + AMAZON_DOM + "/dp/" + encodeURIComponent(p.asin) + "/"
    : "https://www." + AMAZON_DOM + "/s?k=" + encodeURIComponent(p.suche);
  return b + (b.indexOf("?") === -1 ? "?" : "&") +
    "tag=" + encodeURIComponent(PARTNER_TAG) +
    "&ascsubtag=" + encodeURIComponent(subId(p));
}

/* ---------- kleine Helfer ---------- */
const esc = function(s){
  return String(s).replace(/[&<>"]/g, function(c){
    return { "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;" }[c];
  });
};
const eur = function(n){
  return n.toLocaleString("de-DE", { style:"currency", currency:"EUR" });
};
const datum = function(s){
  const d = new Date(s + "T12:00:00");
  return d.toLocaleDateString("de-DE", { day:"numeric", month:"long", year:"numeric" });
};
const jetzt = function(p){ return p.verlauf[p.verlauf.length - 1]; };
const vorher = function(p){ return p.verlauf[p.verlauf.length - 2] || jetzt(p); };
const tief = function(p){ return Math.min.apply(null, p.verlauf.map(function(x){ return x.p; })); };
const hoch = function(p){ return Math.max.apply(null, p.verlauf.map(function(x){ return x.p; })); };
const amTief = function(p){ return Math.abs(jetzt(p).p - tief(p)) < 0.005; };
const SANFT = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

const HAKEN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" ' +
  'stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>';
const PFEIL_AB = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" ' +
  'stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M6 13l6 6 6-6"/></svg>';
const PFEIL_AUF = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" ' +
  'stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M6 11l6-6 6 6"/></svg>';

/* ══════════════════════════════════════════════════════════════════════
   Wirkzeichen — jedes Produkt zeigt, was es tut, bevor ein Wort gelesen
   ist. Sog zieht ein, Impuls schlägt aus, Licht wandert durch seine
   Farben, Druck steigt bis zum eingestellten Wert und beginnt von vorn.
   Die Bewegung steckt im SVG selbst, damit sie mit der Karte kommt.
   ══════════════════════════════════════════════════════════════════════ */
function wirkzeichen(art, farben){
  const halt = SANFT ? "animation:none" : "";
  if(art === "sog" || art === "impuls"){
    const ein = (art === "sog");
    const ringe = [0, 1, 2, 3].map(function(i){
      return '<circle class="r" cx="200" cy="200" r="' + (78 + i * 42) + '" ' +
             'style="animation-delay:' + (i * .55).toFixed(2) + 's"/>';
    }).join("");
    let spitzen = "";
    for(let i = 0; i < 8; i++){
      const w = 22.5 + i * 45, rad = w * Math.PI / 180;
      spitzen += '<path class="s" d="M0,0 L14,-8 L14,8 Z" transform="translate(' +
        (200 + Math.cos(rad) * 168).toFixed(1) + ' ' + (200 + Math.sin(rad) * 168).toFixed(1) +
        ') rotate(' + (w + (ein ? 180 : 0)) + ')" ' +
        'style="animation-delay:' + (i * .09).toFixed(2) + 's"/>';
    }
    return '<svg viewBox="0 0 400 400" aria-hidden="true"><style>' +
      '.r{fill:none;stroke:var(--akzent);stroke-width:2.2;transform-origin:200px 200px;' +
      'animation:' + (ein ? 'zieh' : 'stoss') + ' 4.4s ease-in-out infinite;' + halt + '}' +
      '.s{fill:var(--akzent);opacity:.34;transform-box:fill-box;' +
      'animation:' + (ein ? 'zieh2' : 'stoss2') + ' 4.4s ease-in-out infinite;' + halt + '}' +
      '@keyframes zieh{0%{transform:scale(1);opacity:.34}70%{transform:scale(.42);opacity:0}' +
      '100%{transform:scale(.42);opacity:0}}' +
      '@keyframes stoss{0%{transform:scale(.42);opacity:.36}70%{transform:scale(1.06);opacity:0}' +
      '100%{transform:scale(1.06);opacity:0}}' +
      '@keyframes zieh2{0%,100%{opacity:.12}45%{opacity:.42}}' +
      '@keyframes stoss2{0%,100%{opacity:.12}45%{opacity:.42}}' +
      '</style>' + ringe + spitzen + '</svg>';
  }

  if(art === "licht"){
    /* Die sechzehn Farben lassen sich nicht alle zeigen, sechs schon —
       sie kreisen langsam, wie der Projektor selbst. */
    const f = farben || ["#ff7a3d","#ff4d6d","#c94bd0","#7a5cf0","#3aa0ff","#2fd0c4"];
    const seg = f.map(function(c, i){
      const a1 = (i / f.length) * 2 * Math.PI - Math.PI / 2;
      const a2 = ((i + 1) / f.length) * 2 * Math.PI - Math.PI / 2;
      const r = 150;
      const x1 = 200 + Math.cos(a1) * r, y1 = 200 + Math.sin(a1) * r;
      const x2 = 200 + Math.cos(a2) * r, y2 = 200 + Math.sin(a2) * r;
      return '<path d="M' + x1.toFixed(1) + ',' + y1.toFixed(1) + ' A' + r + ',' + r +
        ' 0 0 1 ' + x2.toFixed(1) + ',' + y2.toFixed(1) + '" stroke="' + c +
        '" stroke-width="26" fill="none" stroke-linecap="butt" opacity=".5"/>';
    }).join("");
    return '<svg viewBox="0 0 400 400" aria-hidden="true"><style>' +
      '.kreisel{transform-origin:200px 200px;animation:dreh 26s linear infinite;' + halt + '}' +
      '.schein{transform-origin:200px 200px;animation:atmen 6s ease-in-out infinite;' + halt + '}' +
      '@keyframes dreh{to{transform:rotate(360deg)}}' +
      '@keyframes atmen{0%,100%{opacity:.28;transform:scale(.96)}50%{opacity:.5;transform:scale(1.04)}}' +
      '</style><defs><radialGradient id="gl"><stop offset="0" stop-color="#ffd79a"/>' +
      '<stop offset="1" stop-color="#ffd79a" stop-opacity="0"/></radialGradient></defs>' +
      '<circle class="schein" cx="200" cy="200" r="150" fill="url(#gl)"/>' +
      '<g class="kreisel">' + seg + '</g></svg>';
  }

  /* druck — Manometer, der Zeiger läuft hoch und fällt zurück */
  const cx = 200, cy = 200, start = 140, ende = 400, anteil = .72;
  const punkt = function(r, g){
    const a = g * Math.PI / 180;
    return [cx + Math.cos(a) * r, cy + Math.sin(a) * r];
  };
  const bogen = function(r, g1, g2){
    const a = punkt(r, g1), b = punkt(r, g2);
    return "M" + a[0].toFixed(1) + "," + a[1].toFixed(1) + " A" + r + "," + r + " 0 " +
           ((g2 - g1) % 360 > 180 ? 1 : 0) + " 1 " + b[0].toFixed(1) + "," + b[1].toFixed(1);
  };
  let striche = "";
  for(let i = 0; i < 13; i++){
    const g = start + (ende - start) * i / 12, lang = (i % 3 === 0);
    const a = punkt(lang ? 152 : 160, g), b = punkt(lang ? 138 : 145, g);
    striche += '<line x1="' + a[0].toFixed(1) + '" y1="' + a[1].toFixed(1) + '" x2="' +
      b[0].toFixed(1) + '" y2="' + b[1].toFixed(1) + '" stroke="var(--akzent)" stroke-opacity="' +
      (lang ? ".5" : ".28") + '" stroke-width="' + (lang ? "3.4" : "2") + '" stroke-linecap="round"/>';
  }
  const voll = bogen(174, start, start + (ende - start) * anteil);
  return '<svg viewBox="0 0 400 400" aria-hidden="true"><style>' +
    '.fuell{stroke-dasharray:1000;stroke-dashoffset:1000;animation:steig 4.6s ease-in-out infinite;' +
    halt + '}' +
    '.zeiger{transform-origin:200px 200px;animation:schwenk 4.6s ease-in-out infinite;' + halt + '}' +
    '@keyframes steig{0%{stroke-dashoffset:1000}55%,80%{stroke-dashoffset:670}100%{stroke-dashoffset:1000}}' +
    '@keyframes schwenk{0%{transform:rotate(0deg)}55%,80%{transform:rotate(187deg)}' +
    '100%{transform:rotate(0deg)}}' +
    '</style>' +
    '<path d="' + bogen(174, start, ende) + '" fill="none" stroke="var(--akzent)" ' +
    'stroke-opacity=".18" stroke-width="3" stroke-linecap="round"/>' +
    '<path class="fuell" d="' + voll + '" fill="none" stroke="var(--akzent)" ' +
    'stroke-opacity=".62" stroke-width="8" stroke-linecap="round"/>' + striche +
    '<g class="zeiger"><line x1="200" y1="200" x2="' + punkt(126, start)[0].toFixed(1) +
    '" y2="' + punkt(126, start)[1].toFixed(1) + '" stroke="var(--akzent)" stroke-opacity=".7" ' +
    'stroke-width="4.5" stroke-linecap="round"/></g>' +
    '<circle cx="200" cy="200" r="8" fill="var(--akzent)" fill-opacity=".55"/></svg>';
}

/* ---------- Preisverlauf als Linie ---------- */
function kurve(p){
  const w = 300, h = 52, pad = 3;
  const werte = p.verlauf.map(function(x){ return x.p; });
  const lo = Math.min.apply(null, werte), hi = Math.max.apply(null, werte);
  const y = function(v){
    return hi === lo ? h / 2 : pad + (hi - v) / (hi - lo) * (h - pad * 2);
  };
  const x = function(i){ return i / (werte.length - 1) * w; };
  const pfad = werte.map(function(v, i){
    return (i ? "L" : "M") + x(i).toFixed(1) + "," + y(v).toFixed(1);
  }).join(" ");
  const flaeche = pfad + " L" + w + "," + h + " L0," + h + " Z";
  const letzt = werte.length - 1;
  return '<svg class="kurve" viewBox="0 0 ' + w + ' ' + h + '" preserveAspectRatio="none" ' +
    'aria-hidden="true">' +
    '<path class="flaeche" d="' + flaeche + '"/>' +
    '<line class="tiefmarke" x1="0" y1="' + y(lo).toFixed(1) + '" x2="' + w + '" y2="' +
      y(lo).toFixed(1) + '"/>' +
    '<path class="linie" d="' + pfad + '"/>' +
    '<circle class="punkt" cx="' + x(letzt).toFixed(1) + '" cy="' + y(werte[letzt]).toFixed(1) +
      '" r="3.4"/></svg>';
}

/* ---------- Wunschpreis-Alarm ---------- */
const SPEICHER = "squelly_alarme_v2";
let ALARME = {};
try{ ALARME = JSON.parse(localStorage.getItem(SPEICHER) || "{}"); }catch(e){ ALARME = {}; }
function alarmeSichern(){
  try{ localStorage.setItem(SPEICHER, JSON.stringify(ALARME)); }catch(e){}
}

function meldung(art, titel, text){
  const d = document.createElement("div");
  d.className = "meldung " + art;
  d.innerHTML = "<b>" + esc(titel) + "</b><span>" + esc(text) + "</span>";
  document.getElementById("meldungen").appendChild(d);
  setTimeout(function(){ d.remove(); }, 6000);
}
function browserMeldung(titel, text){
  try{
    if("Notification" in window && Notification.permission === "granted")
      new Notification(titel, { body: text });
  }catch(e){}
}

function alarmUmschalten(k){
  const el = document.getElementById("kasten-" + k);
  el.classList.toggle("auf");
  if(el.classList.contains("auf")) el.querySelector("input").focus();
}
function zielSetzen(k, faktor){
  const p = finde(k);
  document.getElementById("ziel-" + k).value = (jetzt(p).p * faktor).toFixed(2);
}
function alarmSpeichern(k){
  const p = finde(k), preis = jetzt(p).p;
  const ziel = parseFloat(String(document.getElementById("ziel-" + k).value).replace(",", "."));
  if(!(ziel > 0)){
    meldung("acht", "Kein gültiger Wunschpreis", "Trag einen Betrag über null ein.");
    return;
  }
  if(ziel >= preis){
    meldung("acht", "Ziel liegt zu hoch",
      "Der Preis steht schon bei " + eur(preis) + ". Setz das Ziel darunter.");
    return;
  }
  ALARME[k] = { ziel: ziel, seit: Date.now(), start: preis, gemeldet: null };
  alarmeSichern();
  if("Notification" in window && Notification.permission === "default"){
    /* Eingebettete Ansichten weisen die Frage rundheraus ab. Der Alarm
       steht trotzdem — dann eben nur auf der Seite. */
    Notification.requestPermission().then(function(r){
      meldung(r === "granted" ? "gut" : "info",
        r === "granted" ? "Benachrichtigungen aktiv" : "Nur auf der Seite",
        r === "granted"
          ? "Du bekommst eine Meldung, sobald der Preis fällt — solange diese Seite offen ist."
          : "Ohne Erlaubnis siehst du den Treffer nur hier auf der Seite.");
    }).catch(function(){
      meldung("info", "Nur auf der Seite",
        "Dein Browser lässt hier keine Benachrichtigungen zu. Der Alarm greift, solange " +
        "diese Seite offen ist.");
    });
  } else {
    meldung("gut", "Wunschpreis gemerkt",
      p.name.split(" ").slice(0, 3).join(" ") + " ab " + eur(ziel));
  }
  zeichnen();
}
function alarmLoeschen(k){ delete ALARME[k]; alarmeSichern(); zeichnen(); }

function alarmePruefen(){
  Object.keys(ALARME).forEach(function(k){
    const p = finde(k);
    if(!p) return;
    const a = ALARME[k], preis = jetzt(p).p;
    if(preis <= a.ziel && a.gemeldet !== preis){
      a.gemeldet = preis; alarmeSichern();
      const text = p.name.split("—")[0].trim() + " kostet jetzt " + eur(preis) +
                   " — dein Ziel war " + eur(a.ziel) + ".";
      meldung("gut", "Wunschpreis erreicht", text);
      browserMeldung("SQUELLY — Wunschpreis erreicht", text);
    }
  });
}

/* ---------- eine Karte ---------- */
function finde(k){
  return PRODUKTE.filter(function(x){ return x.kuerzel === k; })[0];
}

function karte(p){
  const preis = jetzt(p).p, alt = vorher(p).p, diff = preis - alt;
  const richtung = diff < -0.004 ? "ab" : (diff > 0.004 ? "auf" : "gleich");
  const trendText = richtung === "gleich"
    ? "unverändert"
    : eur(Math.abs(diff)) + " · " + Math.abs(diff / alt * 100).toFixed(1).replace(".", ",") + " %";
  const trendPfeil = richtung === "ab" ? PFEIL_AB : (richtung === "auf" ? PFEIL_AUF : "");
  const sparen = hoch(p) - preis;
  const anteil = hoch(p) === tief(p) ? 0 : (hoch(p) - preis) / (hoch(p) - tief(p)) * 100;
  const a = ALARME[p.kuerzel];
  const fortschritt = a ? Math.max(0, Math.min(100,
    (a.start - preis) / Math.max(0.01, a.start - a.ziel) * 100)) : 0;

  return '' +
  '<article class="karte" data-kat="' + esc(p.kat) + '" data-kuerzel="' + esc(p.kuerzel) + '" ' +
    'data-suche="' + esc((p.name + " " + p.marke + " " + p.kat + " " +
      p.fakten.join(" ")).toLowerCase()) + '" style="--akzent:' + p.akzent + '">' +
    '<div class="bild">' +
      '<span class="kat">' + esc(p.kat) + '</span>' +
      (amTief(p) ? '<span class="marker">Tiefpreis</span>' : '') +
      '<span class="fx">' + wirkzeichen(p.wirkung, p.farben) + '</span>' +
      '<img src="' + p.bild + '" alt="' + esc(p.alt) + '" decoding="async" loading="lazy">' +
    '</div>' +
    '<h2 class="name">' + esc(p.name) + '</h2>' +
    '<p class="hersteller">' + esc(p.marke) + '</p>' +

    '<div class="preisreihe">' +
      '<span class="preis" data-wert="' + preis + '">' + eur(preis) + '</span>' +
      '<span class="trend ' + richtung + '">' + trendPfeil + trendText + '</span>' +
      (DEMO_PREISE ? '<span class="beispiel">Beispielpreis</span>' : '') +
    '</div>' +

    '<div class="abstand">' +
      '<div class="spanne"><i data-breite="' + anteil.toFixed(0) + '"></i></div>' +
      '<div class="spannefuss">' +
        '<span>Tief <b>' + eur(tief(p)) + '</b></span>' +
        '<span>' + (sparen > 0.004 ? eur(sparen) + ' unter dem Höchstwert' : 'auf Höchstwert') +
        '</span>' +
      '</div>' +
    '</div>' +

    kurve(p) +
    '<div class="kurvefuss"><span>' + datum(p.verlauf[0].d).replace(/ \d{4}$/, "") +
      '</span><span>Stand ' + datum(jetzt(p).d).replace(/ \d{4}$/, "") + '</span></div>' +

    /* Alle Merkmale stehen da. Ein Aufklapper hatte hier nichts zu
       verbergen — vier Zeilen passen, und wer vergleicht, will sie sehen. */
    '<ul class="punkte">' +
      p.fakten.map(function(f){
        return '<li>' + HAKEN + '<span>' + esc(f) + '</span></li>';
      }).join("") +
    '</ul>' +

    '<a class="cta" href="' + esc(amazonLink(p)) + '" target="_blank" ' +
      'rel="noopener sponsored nofollow">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
        'stroke-linecap="round" stroke-linejoin="round">' +
        '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>' +
        '<path d="M15 3h6v6"/><path d="M10 14 21 3"/></svg>Preis auf Amazon prüfen</a>' +

    '<button class="wecker' + (a ? ' aktiv' : '') + '" ' +
      'onclick="alarmUmschalten(\'' + p.kuerzel + '\')">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
        'stroke-linecap="round"><path d="M18 8a6 6 0 1 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/>' +
        '<path d="M13.7 21a2 2 0 0 1-3.4 0"/></svg>' +
      (a ? "Wunschpreis " + eur(a.ziel) + " gemerkt" : "Wunschpreis merken") + '</button>' +

    '<div class="kasten" id="kasten-' + p.kuerzel + '">' +
      '<label for="ziel-' + p.kuerzel + '">Sag Bescheid, sobald der Preis fällt auf</label>' +
      '<div class="zeile">' +
        '<input type="number" id="ziel-' + p.kuerzel + '" step="0.01" min="0.01" ' +
          'inputmode="decimal" value="' + (a ? a.ziel.toFixed(2) : (preis * 0.9).toFixed(2)) + '">' +
        '<button onclick="alarmSpeichern(\'' + p.kuerzel + '\')">' +
          (a ? "Ändern" : "Merken") + '</button>' +
      '</div>' +
      '<div class="schnell">' +
        '<button onclick="zielSetzen(\'' + p.kuerzel + '\',0.95)">−5 %</button>' +
        '<button onclick="zielSetzen(\'' + p.kuerzel + '\',0.9)">−10 %</button>' +
        '<button onclick="zielSetzen(\'' + p.kuerzel + '\',0.85)">−15 %</button>' +
        '<button onclick="zielSetzen(\'' + p.kuerzel + '\',' +
          (tief(p) / preis).toFixed(4) + ')">auf das Tief</button>' +
        (a ? '<button onclick="alarmLoeschen(\'' + p.kuerzel + '\')">entfernen</button>' : '') +
      '</div>' +
      (a ? '<div class="balken"><i style="width:' + fortschritt.toFixed(0) + '%"></i></div>' : '') +
      '<p class="notiz">Der Wunschpreis bleibt <b>in deinem Browser</b>. Geprüft wird, solange ' +
        'diese Seite offen ist — ohne Server kann eine Seite nicht im Hintergrund nachsehen.</p>' +
    '</div>' +

    '<p class="warum">' + esc(p.warum) + '</p>' +
  '</article>';
}

/* ---------- Zeichnen, Filtern, Suchen ---------- */
let KAT = "Alle", WORT = "";

function zeichnen(){
  document.getElementById("gitter").innerHTML = PRODUKTE.map(karte).join("");
  beobachten();
  zeiger();
  filtern();
}

function filtern(){
  let n = 0;
  document.querySelectorAll(".karte").forEach(function(k){
    const passt = (KAT === "Alle" || k.dataset.kat === KAT) &&
                  (!WORT || k.dataset.suche.indexOf(WORT) !== -1);
    k.classList.toggle("weg", !passt);
    if(passt) n++;
  });
  document.getElementById("treffer").textContent =
    n + (n === 1 ? " Produkt" : " Produkte");
  document.getElementById("leer").classList.toggle("an", n === 0);
}

function faecher(){
  const kats = ["Alle"].concat(PRODUKTE.map(function(p){ return p.kat; })
    .filter(function(v, i, a){ return a.indexOf(v) === i; }));
  document.getElementById("fach").innerHTML = kats.map(function(k){
    return '<button type="button" aria-pressed="' + (k === KAT) + '" data-kat="' + esc(k) +
      '">' + esc(k) + '</button>';
  }).join("");
  document.querySelectorAll("#fach button").forEach(function(b){
    b.onclick = function(){
      KAT = b.dataset.kat;
      document.querySelectorAll("#fach button").forEach(function(x){
        x.setAttribute("aria-pressed", String(x.dataset.kat === KAT));
      });
      filtern();
    };
  });
}

/* Karten kommen beim Hereinrollen, die Linie zeichnet sich dabei, die
   Spanne läuft auf und der Preis zählt hoch. Einmal je Karte. */
function beobachten(){
  const karten = document.querySelectorAll(".karte");
  if(SANFT || !("IntersectionObserver" in window)){
    karten.forEach(function(k){ k.classList.add("da"); fertig(k); });
    return;
  }
  const beo = new IntersectionObserver(function(eintraege){
    eintraege.forEach(function(e){
      if(!e.isIntersecting) return;
      const k = e.target;
      beo.unobserve(k);
      setTimeout(function(){ k.classList.add("da"); fertig(k); },
        Math.min(260, [].indexOf.call(karten, k) % 2 * 110));
    });
  }, { rootMargin: "0px 0px -60px 0px", threshold: .12 });
  karten.forEach(function(k){ beo.observe(k); });
}

function fertig(k){
  const b = k.querySelector(".spanne i");
  if(b) requestAnimationFrame(function(){ b.style.width = b.dataset.breite + "%"; });
  const linie = k.querySelector(".kurve .linie");
  if(linie && !SANFT){
    const l = linie.getTotalLength();
    linie.style.strokeDasharray = l;
    linie.style.strokeDashoffset = l;
    linie.getBoundingClientRect();
    linie.style.transition = "stroke-dashoffset 1.2s cubic-bezier(.2,.8,.3,1)";
    linie.style.strokeDashoffset = "0";
  }
  const pr = k.querySelector(".preis");
  if(pr && !SANFT) hochzaehlen(pr, parseFloat(pr.dataset.wert));
}

function hochzaehlen(el, ziel){
  const dauer = 900, t0 = performance.now();
  const lauf = function(t){
    const f = Math.min(1, (t - t0) / dauer);
    const e = 1 - Math.pow(1 - f, 3);
    el.textContent = eur(ziel * e);
    if(f < 1) requestAnimationFrame(lauf);
    else el.textContent = eur(ziel);
  };
  requestAnimationFrame(lauf);
}

/* Der Schimmer folgt dem Zeiger — nur dort, wo es einen echten gibt. */
function zeiger(){
  if(SANFT || !window.matchMedia("(pointer: fine)").matches) return;
  document.querySelectorAll(".karte").forEach(function(k){
    k.addEventListener("pointermove", function(e){
      const r = k.getBoundingClientRect();
      k.style.setProperty("--mx", ((e.clientX - r.left) / r.width * 100).toFixed(1) + "%");
      k.style.setProperty("--my", ((e.clientY - r.top) / r.height * 100).toFixed(1) + "%");
    });
  });
}

/* ---------- Nordlicht ---------- */
(function himmel(){
  const c = document.getElementById("himmel");
  if(SANFT){ c.remove(); return; }
  const x = c.getContext("2d");
  let b = 0, h = 0, t = 0, laeuft = true;
  const flecken = [
    { f:"#1e5ea8", r:.62, sx:.00021, sy:.00013, ax:.30, ay:.22 },
    { f:"#6c4bb8", r:.52, sx:.00016, sy:.00019, ax:.72, ay:.30 },
    { f:"#1d7f88", r:.46, sx:.00024, sy:.00011, ax:.48, ay:.72 }
  ];
  function messen(){
    b = c.width = Math.floor(innerWidth * .5);
    h = c.height = Math.floor(Math.min(innerHeight * 1.4, 1400) * .5);
  }
  function malen(zeit){
    if(!laeuft) return;
    t = zeit || 0;
    x.clearRect(0, 0, b, h);
    x.globalCompositeOperation = "lighter";
    flecken.forEach(function(f, i){
      const cxp = (f.ax + Math.sin(t * f.sx + i) * .16) * b;
      const cyp = (f.ay + Math.cos(t * f.sy + i) * .14) * h;
      const r = f.r * Math.min(b, h);
      const g = x.createRadialGradient(cxp, cyp, 0, cxp, cyp, r);
      g.addColorStop(0, f.f + "66");
      g.addColorStop(1, f.f + "00");
      x.fillStyle = g;
      x.beginPath(); x.arc(cxp, cyp, r, 0, 6.2832); x.fill();
    });
    requestAnimationFrame(malen);
  }
  addEventListener("resize", messen, { passive:true });
  document.addEventListener("visibilitychange", function(){
    laeuft = !document.hidden;
    if(laeuft) requestAnimationFrame(malen);
  });
  messen(); requestAnimationFrame(malen);
})();

/* ---------- Leiste, die sich meldet, sobald sie klebt ---------- */
(function(){
  const l = document.getElementById("leiste");
  const wache = document.createElement("div");
  l.parentNode.insertBefore(wache, l);
  new IntersectionObserver(function(e){
    l.classList.toggle("haftet", !e[0].isIntersecting);
  }, { threshold: 1 }).observe(wache);
})();

/* ---------- Rechtstexte ---------- */
const TEXTE = /*TEXTE*/;
function blatt(k){
  const t = TEXTE[k];
  document.getElementById("dlgTitel").textContent = t[0];
  document.getElementById("dlgText").innerHTML = t[1];
  document.getElementById("dlg").showModal();
}

/* ---------- los ---------- */
document.getElementById("suchfeld").addEventListener("input", function(e){
  WORT = e.target.value.trim().toLowerCase();
  filtern();
});
faecher();
zeichnen();
alarmePruefen();
setInterval(alarmePruefen, 60000);
document.getElementById("jahr").textContent = new Date().getFullYear();

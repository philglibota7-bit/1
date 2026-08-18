/* Werkbank – Kern der Plattform.
 *
 * Jedes Tool bindet nur diese eine Datei ein und ruft Werkbank.start() auf.
 * Kopf, Fuss, Querverlinkung, Messung und die Pro-Schranke kommen von hier.
 * Ein neues Tool muss sich um nichts davon kuemmern.
 */
(function () {
  "use strict";

  // Wurzelpfad aus dem eigenen <script src> ableiten. Damit funktionieren
  // Tools in jeder Verzeichnistiefe und auch unter /reponame/ bei GitHub Pages.
  var eigenes = document.currentScript;
  var WURZEL = eigenes
    ? eigenes.src.replace(/platform\/werkbank\.js.*$/, "")
    : "/";

  var LIZENZ_SCHLUESSEL = "werkbank.lizenz";
  var MESS_SCHLUESSEL = "werkbank.messung";

  /* ------------------------------------------------------------------ *
   * Messung – standardmaessig verlaesst nichts den Rechner.
   * Wer spaeter Plausible/Umami einsetzt, setzt window.WERKBANK_ANALYTIK
   * auf eine Funktion (ereignis, daten) und muss hier nichts aendern.
   * ------------------------------------------------------------------ */
  function messen(ereignis, daten) {
    try {
      var roh = localStorage.getItem(MESS_SCHLUESSEL);
      var zaehler = roh ? JSON.parse(roh) : {};
      zaehler[ereignis] = (zaehler[ereignis] || 0) + 1;
      localStorage.setItem(MESS_SCHLUESSEL, JSON.stringify(zaehler));
    } catch (e) { /* privater Modus: egal, Messung ist kein Kernzweck */ }

    if (typeof window.WERKBANK_ANALYTIK === "function") {
      try { window.WERKBANK_ANALYTIK(ereignis, daten || {}); } catch (e) {}
    }
    window.dispatchEvent(new CustomEvent("werkbank:ereignis", {
      detail: { ereignis: ereignis, daten: daten || {} }
    }));
  }

  function messwerte() {
    try { return JSON.parse(localStorage.getItem(MESS_SCHLUESSEL) || "{}"); }
    catch (e) { return {}; }
  }

  /* ------------------------------------------------------------------ *
   * Lizenz
   *
   * WICHTIG UND BEWUSST SO: Diese Pruefung laeuft im Browser und ist damit
   * umgehbar. Das ist in Stufe 1 in Ordnung – sie haelt ehrliche Kunden
   * ehrlich und kostet null Infrastruktur. Sobald Umsatz da ist, wird
   * WERKBANK_LIZENZ_ENDPUNKT gesetzt; dann prueft ein Server den Schluessel
   * und nur diese eine Funktion aendert sich. Siehe docs/BEZAHLUNG.md.
   * ------------------------------------------------------------------ */
  var lizenz = {
    // Format: WB-XXXX-XXXX-P  (P = Pruefzeichen aus der Quersumme)
    gueltigesFormat: function (schluessel) {
      var s = String(schluessel || "").toUpperCase().replace(/\s/g, "");
      var m = /^WB-([A-Z0-9]{4})-([A-Z0-9]{4})-([A-Z0-9])$/.exec(s);
      if (!m) return false;
      var kern = m[1] + m[2], summe = 0;
      for (var i = 0; i < kern.length; i++) summe += kern.charCodeAt(i);
      var alphabet = "0123456789ABCDEFGHJKLMNPQRSTUVWXYZ";
      return alphabet[summe % alphabet.length] === m[3];
    },

    setzen: function (schluessel) {
      var s = String(schluessel || "").toUpperCase().replace(/\s/g, "");
      if (!this.gueltigesFormat(s)) return false;
      try { localStorage.setItem(LIZENZ_SCHLUESSEL, s); } catch (e) { return false; }
      messen("lizenz.aktiviert");
      return true;
    },

    entfernen: function () {
      try { localStorage.removeItem(LIZENZ_SCHLUESSEL); } catch (e) {}
    },

    schluessel: function () {
      try { return localStorage.getItem(LIZENZ_SCHLUESSEL) || ""; } catch (e) { return ""; }
    },

    istPro: function () {
      return this.gueltigesFormat(this.schluessel());
    },

    // Stufe 2: echte Pruefung gegen einen kleinen Endpunkt.
    pruefeServer: function () {
      var endpunkt = window.WERKBANK_LIZENZ_ENDPUNKT;
      if (!endpunkt) return Promise.resolve(this.istPro());
      var s = this.schluessel();
      if (!s) return Promise.resolve(false);
      return fetch(endpunkt + "?schluessel=" + encodeURIComponent(s))
        .then(function (a) { return a.json(); })
        .then(function (d) { return !!d.gueltig; })
        .catch(function () { return false; }); // offline: nicht aussperren? bewusst nein
    }
  };

  /* Schranke fuer eine Pro-Funktion. Gibt true zurueck, wenn benutzt werden
     darf, sonst false und zeigt das Kauf-Fenster. */
  function pro(funktion, text) {
    if (lizenz.istPro()) return true;
    messen("pro.blockiert", { funktion: funktion });
    fensterZeigen(funktion, text);
    return false;
  }

  function fensterZeigen(funktion, text) {
    var alt = document.getElementById("wb-pro-fenster");
    if (alt) alt.remove();
    var d = document.createElement("dialog");
    d.id = "wb-pro-fenster";
    d.style.cssText =
      "border:1px solid var(--rand);border-radius:12px;padding:0;max-width:26rem;" +
      "background:var(--grund);color:var(--text)";
    d.innerHTML =
      '<div style="padding:1.5rem">' +
      '<h2 style="margin:0 0 .5rem;font-size:1.2rem">Diese Funktion gehoert zu Pro</h2>' +
      '<p style="color:var(--text-leise);margin:0 0 1rem">' +
        (text || "Alle Pro-Funktionen aller Werkbank-Tools, einmal zahlen, dauerhaft nutzen.") +
      "</p>" +
      '<a class="knopf" style="width:100%" href="' + WURZEL + 'pro.html">Pro ansehen</a>' +
      '<div style="margin-top:1rem">' +
        '<label for="wb-schluessel">Schluessel bereits gekauft?</label>' +
        '<div style="display:flex;gap:.5rem">' +
          '<input id="wb-schluessel" type="text" placeholder="WB-XXXX-XXXX-X" ' +
            'autocomplete="off" spellcheck="false">' +
          '<button class="knopf leise" id="wb-einloesen">Aktivieren</button>' +
        "</div>" +
        '<p id="wb-lizenz-hinweis" class="leise" style="margin:.5rem 0 0"></p>' +
      "</div>" +
      '<button class="knopf leise" id="wb-schliessen" style="width:100%;margin-top:1rem">' +
        "Schliessen</button>" +
      "</div>";
    document.body.appendChild(d);

    d.querySelector("#wb-schliessen").onclick = function () { d.close(); d.remove(); };
    d.querySelector("#wb-einloesen").onclick = function () {
      var eingabe = d.querySelector("#wb-schluessel").value;
      var hinweis = d.querySelector("#wb-lizenz-hinweis");
      if (lizenz.setzen(eingabe)) {
        hinweis.textContent = "Aktiviert. Seite wird neu geladen.";
        hinweis.style.color = "var(--gut)";
        setTimeout(function () { location.reload(); }, 700);
      } else {
        hinweis.textContent = "Dieser Schluessel ist nicht gueltig.";
        hinweis.style.color = "var(--fehler)";
      }
    };
    if (typeof d.showModal === "function") d.showModal(); else d.setAttribute("open", "");
  }

  /* ------------------------------------------------------------------ *
   * Kopf und Fuss
   * ------------------------------------------------------------------ */
  function kopfBauen(aktuell) {
    var k = document.createElement("header");
    k.className = "wb-kopf";
    k.innerHTML =
      '<div class="huelle">' +
        '<a class="wb-marke" href="' + WURZEL + 'werkbank.html">WERK<span>BANK</span></a>' +
        "<nav>" +
          '<a href="' + WURZEL + 'werkbank.html">Alle Tools</a>' +
          '<a href="' + WURZEL + 'pro.html">Pro</a>' +
          '<button class="knopf leise" id="wb-thema" title="Hell/Dunkel umschalten" ' +
            'style="padding:.35rem .6rem">◐</button>' +
        "</nav>" +
      "</div>";
    document.body.insertBefore(k, document.body.firstChild);
    k.querySelector("#wb-thema").onclick = themaUmschalten;
    if (aktuell) {
      var a = k.querySelector('a[href$="werkbank.html"]');
      if (a) a.style.color = "var(--text)";
    }
  }

  function fussBauen(verwandte) {
    var f = document.createElement("footer");
    f.className = "wb-fuss";
    var links = (verwandte || []).map(function (t) {
      return '<a href="' + WURZEL + t.pfad + '">' + t.titel + "</a>";
    }).join(" &middot; ");
    f.innerHTML =
      '<div class="huelle">' +
        "<div style='flex:2;min-width:14rem'><strong>Werkbank</strong><br>" +
          "Kleine Werkzeuge, die eine Sache richtig machen. " +
          "Alles laeuft im Browser – deine Daten bleiben auf deinem Rechner.</div>" +
        "<div style='flex:2;min-width:14rem'>" +
          (links ? "<strong>Weitere Tools</strong><br>" + links : "") + "</div>" +
        "<div style='flex:1;min-width:9rem'>" +
          '<a href="' + WURZEL + 'impressum.html">Impressum</a><br>' +
          '<a href="' + WURZEL + 'datenschutz.html">Datenschutz</a><br>' +
          '<a href="' + WURZEL + 'pro.html">Pro</a></div>' +
      "</div>";
    document.body.appendChild(f);
  }

  function themaUmschalten() {
    var jetzt = document.documentElement.getAttribute("data-thema");
    var dunkelSystem = matchMedia("(prefers-color-scheme: dark)").matches;
    var neu = jetzt ? (jetzt === "dunkel" ? "hell" : "dunkel")
                    : (dunkelSystem ? "hell" : "dunkel");
    document.documentElement.setAttribute("data-thema", neu);
    try { localStorage.setItem("werkbank.thema", neu); } catch (e) {}
  }

  (function themaLaden() {
    try {
      var t = localStorage.getItem("werkbank.thema");
      if (t) document.documentElement.setAttribute("data-thema", t);
    } catch (e) {}
  })();

  /* ------------------------------------------------------------------ *
   * Start
   * ------------------------------------------------------------------ */
  function start(einstellungen) {
    var e = einstellungen || {};
    function los() {
      kopfBauen(e.slug);
      fussBauen(e.verwandte);
      messen("seite.aufruf", { slug: e.slug || "unbekannt" });
      if (lizenz.istPro()) document.documentElement.setAttribute("data-pro", "1");
    }
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", los);
    } else { los(); }
  }

  window.Werkbank = {
    version: "1.0.0",
    wurzel: WURZEL,
    start: start,
    messen: messen,
    messwerte: messwerte,
    lizenz: lizenz,
    pro: pro
  };
})();

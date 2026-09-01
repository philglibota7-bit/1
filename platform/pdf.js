/* Werkbank – PDF-Erzeuger.
 *
 * Bewusst selbst geschrieben statt eine fremde Bibliothek einzubinden:
 * die ueblichen PDF-Bibliotheken wiegen mehrere hundert Kilobyte, muessten
 * von einem fremden Server geladen werden und koennen weit mehr, als hier
 * je gebraucht wird. Dieser Erzeuger deckt genau ab, was die Werkzeuge
 * brauchen: JPEG-Bilder, Text in Helvetica, Linien und Flaechen.
 *
 * Er liegt in platform/, weil ihn inzwischen mehr als ein Werkzeug benutzt –
 * genau das ist der Punkt der gemeinsamen Basis: das naechste Werkzeug, das
 * ein PDF ausgibt, kostet keine Zeile PDF-Code mehr.
 *
 * Koordinaten: PDF rechnet von unten links. Weil sich Dokumente von oben
 * nach unten denken lassen, nehmen text() und flaeche() ihr y von OBEN und
 * rechnen intern um. bild() ebenfalls.
 */
(function () {
  "use strict";

  var MM = 2.8346457;   // Millimeter -> Punkte
  var A4 = [595.28, 841.89];
  var LETTER = [612, 792];

  /* ---- Bytepuffer -------------------------------------------------- */
  function Puffer() { this.teile = []; this.laenge = 0; }
  Puffer.prototype.schreib = function (x) {
    var b = typeof x === "string"
      ? Uint8Array.from(x, function (z) { return z.charCodeAt(0) & 0xff; })
      : x;
    this.teile.push(b);
    this.laenge += b.length;
    return this;
  };

  /* ---- WinAnsi ------------------------------------------------------
   * Die eingebauten PDF-Schriften sprechen WinAnsi. Fuer Latin-1 stimmt
   * das mit dem Zeichenwert ueberein; nur der Bereich 0x80-0x9F weicht ab.
   * Ohne diese Tabelle wuerde ein Euro-Zeichen im PDF verschwinden.        */
  var SONDER = {
    "€": 0x80, "‚": 0x82, "ƒ": 0x83, "„": 0x84,
    "…": 0x85, "†": 0x86, "‡": 0x87, "ˆ": 0x88,
    "‰": 0x89, "Š": 0x8A, "‹": 0x8B, "Œ": 0x8C,
    "Ž": 0x8E, "‘": 0x91, "’": 0x92, "“": 0x93,
    "”": 0x94, "•": 0x95, "–": 0x96, "—": 0x97,
    "˜": 0x98, "™": 0x99, "š": 0x9A, "›": 0x9B,
    "œ": 0x9C, "ž": 0x9E, "Ÿ": 0x9F
  };

  function winansi(text) {
    var aus = "";
    for (var i = 0; i < text.length; i++) {
      var z = text[i], c = text.charCodeAt(i);
      if (SONDER[z] !== undefined) { aus += String.fromCharCode(SONDER[z]); }
      else if (c < 256) { aus += z; }
      else { aus += "?"; }          // nicht darstellbar, aber nie stillschweigend weg
    }
    return aus.replace(/([\\()])/g, "\\$1");
  }

  /* ---- Textbreite ---------------------------------------------------
   * Arial und Helvetica sind absichtlich massgleich gebaut, ebenso die
   * freien Ersatzschriften (Liberation Sans, Arimo). Deshalb liefert die
   * Messung im Browser dieselben Vorschubbreiten wie die PDF-Schrift.     */
  var messFlaeche = null;
  function breiteVon(text, groesse, fett) {
    if (!messFlaeche) messFlaeche = document.createElement("canvas").getContext("2d");
    messFlaeche.font = (fett ? "bold " : "") + groesse + "px Arial, Helvetica, sans-serif";
    return messFlaeche.measureText(text).width;
  }

  /* ---- Seite --------------------------------------------------------- */
  function Seite(dok, breite, hoehe) {
    this.dok = dok;
    this.breite = breite;
    this.hoehe = hoehe;
    this.inhalt = "";
    this.bilder = [];      // { nr, jpeg, breite, hoehe }
    this.schriftBenutzt = false;
  }

  Seite.prototype.zahl = function (n) {
    return (Math.round(n * 100) / 100).toString();
  };

  /** Gefuellte Flaeche. y von oben. graustufe 0 = schwarz, 1 = weiss. */
  Seite.prototype.flaeche = function (x, y, breite, hoehe, farbe) {
    var f = farbe === undefined ? 0 : farbe;
    var rgb = typeof f === "number" ? [f, f, f] : f;
    this.inhalt += rgb.map(this.zahl, this).join(" ") + " rg " +
      [x, this.hoehe - y - hoehe, breite, hoehe].map(this.zahl, this).join(" ") + " re f\n";
    return this;
  };

  /** Waagerechte Linie. y von oben. */
  Seite.prototype.linie = function (x, y, breite, staerke, farbe) {
    return this.flaeche(x, y, breite, staerke === undefined ? 0.5 : staerke,
                        farbe === undefined ? 0.8 : farbe);
  };

  /**
   * Text setzen. y ist die Grundlinie, von oben gemessen.
   * einst: { groesse, fett, farbe, ausrichtung: "links"|"rechts"|"mitte" }
   * Bei "rechts" ist x die rechte Kante, bei "mitte" die Mitte.
   */
  Seite.prototype.text = function (inhalt, x, y, einst) {
    var e = einst || {};
    var groesse = e.groesse || 10;
    var fett = !!e.fett;
    var f = e.farbe === undefined ? 0 : e.farbe;
    var rgb = typeof f === "number" ? [f, f, f] : f;
    var s = String(inhalt === undefined || inhalt === null ? "" : inhalt);
    if (!s) return this;

    if (e.ausrichtung === "rechts") x -= breiteVon(s, groesse, fett);
    else if (e.ausrichtung === "mitte") x -= breiteVon(s, groesse, fett) / 2;

    this.schriftBenutzt = true;
    this.inhalt += "BT /" + (fett ? "F2" : "F1") + " " + groesse + " Tf " +
      rgb.map(this.zahl, this).join(" ") + " rg 1 0 0 1 " +
      this.zahl(x) + " " + this.zahl(this.hoehe - y) + " Tm (" +
      winansi(s) + ") Tj ET\n";
    return this;
  };

  /** Text im Kasten umbrechen. Gibt die benutzte Hoehe zurueck. */
  Seite.prototype.absatz = function (inhalt, x, y, maxBreite, einst) {
    var e = einst || {};
    var groesse = e.groesse || 10;
    var zeilenhoehe = e.zeilenhoehe || groesse * 1.4;
    var woerter = String(inhalt || "").split(/\s+/).filter(Boolean);
    var zeile = "", zeilen = [];
    woerter.forEach(function (w) {
      var versuch = zeile ? zeile + " " + w : w;
      if (breiteVon(versuch, groesse, !!e.fett) > maxBreite && zeile) {
        zeilen.push(zeile); zeile = w;
      } else { zeile = versuch; }
    });
    if (zeile) zeilen.push(zeile);
    zeilen.forEach(function (z, i) {
      this.text(z, x, y + i * zeilenhoehe, e);
    }, this);
    return zeilen.length * zeilenhoehe;
  };

  /** JPEG-Bild platzieren. y von oben, Groesse in Punkten. */
  Seite.prototype.bild = function (jpeg, pxBreite, pxHoehe, x, y, breite, hoehe) {
    var nr = this.bilder.length;
    this.bilder.push({ nr: nr, jpeg: jpeg, breite: pxBreite, hoehe: pxHoehe });
    this.inhalt += "q " + [breite, 0, 0, hoehe, x, this.hoehe - y - hoehe]
      .map(this.zahl, this).join(" ") + " cm /Im" + nr + " Do Q\n";
    return this;
  };

  /* ---- Dokument ------------------------------------------------------ */
  function Dokument() { this.seiten = []; }

  Dokument.prototype.seite = function (breite, hoehe) {
    var s = new Seite(this, breite || A4[0], hoehe || A4[1]);
    this.seiten.push(s);
    return s;
  };

  Dokument.prototype.fertig = function () {
    var p = new Puffer();
    var versatz = [];
    var naechste = 1;
    function nr() { return naechste++; }

    // Objektnummern vorab vergeben, damit Verweise stimmen
    var nrKatalog = nr(), nrBaum = nr();
    var brauchtSchrift = this.seiten.some(function (s) { return s.schriftBenutzt; });
    var nrF1 = brauchtSchrift ? nr() : 0;
    var nrF2 = brauchtSchrift ? nr() : 0;
    var seiten = this.seiten.map(function (s) {
      return {
        s: s, nrSeite: nr(), nrInhalt: nr(),
        nrBilder: s.bilder.map(function () { return nr(); })
      };
    });
    var gesamt = naechste - 1;

    function objekt(n, kopf, daten) {
      versatz[n] = p.laenge;
      p.schreib(n + " 0 obj\n" + kopf);
      if (daten !== undefined) p.schreib("stream\n").schreib(daten).schreib("\nendstream\n");
      p.schreib("endobj\n");
    }

    p.schreib("%PDF-1.4\n%\xE2\xE3\xCF\xD3\n");   // Binaerkennung ist Pflicht

    objekt(nrKatalog, "<< /Type /Catalog /Pages " + nrBaum + " 0 R >>\n");
    objekt(nrBaum, "<< /Type /Pages /Kids [" +
      seiten.map(function (e) { return e.nrSeite + " 0 R"; }).join(" ") +
      "] /Count " + seiten.length + " >>\n");

    if (brauchtSchrift) {
      objekt(nrF1, "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica" +
                   " /Encoding /WinAnsiEncoding >>\n");
      objekt(nrF2, "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold" +
                   " /Encoding /WinAnsiEncoding >>\n");
    }

    seiten.forEach(function (e) {
      var mittel = [];
      if (brauchtSchrift) {
        mittel.push("/Font << /F1 " + nrF1 + " 0 R /F2 " + nrF2 + " 0 R >>");
      }
      if (e.nrBilder.length) {
        mittel.push("/XObject << " + e.nrBilder.map(function (b, i) {
          return "/Im" + i + " " + b + " 0 R";
        }).join(" ") + " >>");
      }
      objekt(e.nrSeite,
        "<< /Type /Page /Parent " + nrBaum + " 0 R /MediaBox [0 0 " +
        e.s.zahl(e.s.breite) + " " + e.s.zahl(e.s.hoehe) + "]" +
        " /Resources << " + mittel.join(" ") + " >>" +
        " /Contents " + e.nrInhalt + " 0 R >>\n");

      objekt(e.nrInhalt, "<< /Length " + e.s.inhalt.length + " >>\n", e.s.inhalt);

      e.s.bilder.forEach(function (b, i) {
        objekt(e.nrBilder[i],
          "<< /Type /XObject /Subtype /Image /Width " + b.breite +
          " /Height " + b.hoehe + " /ColorSpace /DeviceRGB /BitsPerComponent 8" +
          " /Filter /DCTDecode /Length " + b.jpeg.length + " >>\n", b.jpeg);
      });
    });

    // Querverweistabelle: jeder Eintrag muss exakt 20 Byte lang sein
    var xref = p.laenge;
    p.schreib("xref\n0 " + (gesamt + 1) + "\n0000000000 65535 f\r\n");
    for (var n = 1; n <= gesamt; n++) {
      var v = String(versatz[n] || 0);
      while (v.length < 10) v = "0" + v;
      p.schreib(v + " 00000 n\r\n");
    }
    p.schreib("trailer\n<< /Size " + (gesamt + 1) + " /Root " + nrKatalog +
              " 0 R >>\nstartxref\n" + xref + "\n%%EOF\n");

    return new Blob(p.teile, { type: "application/pdf" });
  };

  /* ---- Bild -> JPEG --------------------------------------------------- */
  function bildLaden(datei) {
    if (window.createImageBitmap) return createImageBitmap(datei);
    return new Promise(function (ok, fehler) {
      var i = new Image();
      i.onload = function () { ok(i); };
      i.onerror = fehler;
      i.src = URL.createObjectURL(datei);
    });
  }

  function alsJpeg(datei, guete, maxKante) {
    var grenze = maxKante || 2200;
    return bildLaden(datei).then(function (bild) {
      var b = bild.width, h = bild.height;
      var faktor = Math.min(1, grenze / Math.max(b, h));
      b = Math.max(1, Math.round(b * faktor));
      h = Math.max(1, Math.round(h * faktor));

      var c = document.createElement("canvas");
      c.width = b; c.height = h;
      var ctx = c.getContext("2d");
      ctx.fillStyle = "#ffffff";        // sonst wird Transparenz im JPEG schwarz
      ctx.fillRect(0, 0, b, h);
      ctx.imageSmoothingEnabled = true;
      ctx.imageSmoothingQuality = "high";
      ctx.drawImage(bild, 0, 0, b, h);
      if (bild.close) bild.close();

      return new Promise(function (ok) {
        c.toBlob(function (blob) {
          blob.arrayBuffer().then(function (puffer) {
            ok({ jpeg: new Uint8Array(puffer), breite: b, hoehe: h });
          });
        }, "image/jpeg", guete === undefined ? 0.85 : guete);
      });
    });
  }

  window.WerkbankPDF = {
    MM: MM, A4: A4, LETTER: LETTER,
    neu: function () { return new Dokument(); },
    alsJpeg: alsJpeg,
    breiteVon: breiteVon
  };
})();

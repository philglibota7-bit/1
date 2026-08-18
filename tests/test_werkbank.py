"""Tests: python3 -m unittest discover -s tests -v"""

import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WURZEL))

from cockpit import bericht, bewertung, cli, store  # noqa: E402
from cockpit.geld import eur, fmt, zu_cent  # noqa: E402


class Geld(unittest.TestCase):
    def test_deutsche_und_englische_schreibweise(self):
        self.assertEqual(zu_cent("800"), 80000)
        self.assertEqual(zu_cent("1.250,50"), 125050)
        self.assertEqual(zu_cent("99.90"), 9990)
        self.assertEqual(zu_cent("0,99"), 99)
        self.assertEqual(zu_cent(12), 1200)

    def test_rundung_verliert_nichts(self):
        # Drei mal 33,33 EUR muessen exakt 99,99 ergeben, nicht 99,98999...
        self.assertEqual(zu_cent("33,33") * 3, 9999)

    def test_formatierung(self):
        self.assertEqual(fmt(1234567), "12.345,67")
        self.assertEqual(fmt(-500), "-5,00")
        self.assertEqual(eur(80000), "800,00 EUR")

    def test_muell_wird_abgelehnt(self):
        for schrott in ["", "abc", "12,34,56"]:
            with self.assertRaises(ValueError):
                zu_cent(schrott)


class Bewertung(unittest.TestCase):
    def test_leere_bewertung_ist_null(self):
        self.assertEqual(bewertung.punkte({}), 0)

    def test_hoechstwertung(self):
        beste = {"nachfrage": 5, "absicht": 5, "pro_hebel": 5,
                 "wettbewerb": 0, "wiederkehr": 5, "aufwand": 0}
        self.assertEqual(bewertung.punkte(beste), 100)

    def test_inverse_kriterien_drehen_richtig(self):
        """Viel Wettbewerb muss die Punktzahl senken, nicht heben."""
        wenig = {"nachfrage": 3, "wettbewerb": 0}
        viel = {"nachfrage": 3, "wettbewerb": 5}
        self.assertGreater(bewertung.punkte(wenig), bewertung.punkte(viel))

    def test_werte_ausserhalb_der_skala_werden_gekappt(self):
        self.assertEqual(bewertung.punkte({"nachfrage": 99}),
                         bewertung.punkte({"nachfrage": 5}))

    def test_urteil_grenzen(self):
        self.assertEqual(bewertung.urteil(90), "bauen")
        self.assertEqual(bewertung.urteil(bewertung.GRENZE_BAUEN), "bauen")
        self.assertEqual(bewertung.urteil(bewertung.GRENZE_BAUEN - 1), "vielleicht")
        self.assertEqual(bewertung.urteil(10), "liegen lassen")


class Speicher(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["WERKBANK_HOME"] = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()
        os.environ.pop("WERKBANK_HOME", None)

    def test_runde_um_die_platte(self):
        db = store.leer()
        db["ideen"].append({"id": 1, "titel": "Prüfung mit Umlaut", "punkte": 70})
        store.speichern(db)
        self.assertEqual(store.laden()["ideen"][0]["titel"], "Prüfung mit Umlaut")

    def test_migration_ergaenzt_fehlende_felder(self):
        store.db_pfad().parent.mkdir(parents=True, exist_ok=True)
        store.db_pfad().write_text('{"version": 1, "ideen": []}', encoding="utf-8")
        db = store.laden()
        self.assertIn("einstellungen", db)
        self.assertIn("ziel_monat_cent", db["einstellungen"])
        self.assertEqual(db["version"], store.VERSION)

    def test_monatseintrag_wird_nicht_doppelt_angelegt(self):
        db = store.leer()
        store.monat_eintrag(db, "2026-08", "x")["besucher"] = 5
        store.monat_eintrag(db, "2026-08", "x")["besucher"] += 5
        self.assertEqual(len(db["monate"]), 1)
        self.assertEqual(db["monate"][0]["besucher"], 10)


class Auswertung(unittest.TestCase):
    def bau(self, monate):
        db = store.leer()
        db["monate"] = monate
        return db

    def test_umsatz_und_reichweite_heisst_ausbauen(self):
        db = self.bau([{"monat": "2026-08", "slug": "a", "besucher": 5000,
                        "kaeufe": 4, "umsatz_cent": 7600}])
        self.assertEqual(bericht.empfehlung(bericht.je_tool(db)["a"]), "ausbauen")

    def test_reichweite_ohne_umsatz_heisst_monetarisieren(self):
        db = self.bau([{"monat": "2026-08", "slug": "a", "besucher": 5000,
                        "kaeufe": 0, "umsatz_cent": 0}])
        self.assertEqual(bericht.empfehlung(bericht.je_tool(db)["a"]), "monetarisieren")

    def test_nach_gnadenfrist_ohne_reichweite_heisst_einstellen(self):
        monate = [{"monat": f"2026-{m:02d}", "slug": "a", "besucher": 3,
                   "kaeufe": 0, "umsatz_cent": 0} for m in range(1, 8)]
        self.assertEqual(bericht.empfehlung(bericht.je_tool(self.bau(monate))["a"]),
                         "einstellen")

    def test_junges_tool_bekommt_zeit(self):
        db = self.bau([{"monat": "2026-08", "slug": "a", "besucher": 3,
                        "kaeufe": 0, "umsatz_cent": 0}])
        self.assertEqual(bericht.empfehlung(bericht.je_tool(db)["a"]), "abwarten")


class Registry(unittest.TestCase):
    def test_tools_json_ist_gueltig_und_vollstaendig(self):
        reg = json.loads((WURZEL / "tools.json").read_text(encoding="utf-8"))
        self.assertTrue(reg["tools"], "keine Tools registriert")
        for t in reg["tools"]:
            for feld in ("slug", "titel", "kurz", "pfad", "status", "stichworte"):
                self.assertIn(feld, t, f"{t.get('slug')} fehlt '{feld}'")
            self.assertIn(t["status"], ("idee", "gebaut", "live", "eingestellt"))

    def test_jeder_live_pfad_existiert(self):
        reg = json.loads((WURZEL / "tools.json").read_text(encoding="utf-8"))
        for t in reg["tools"]:
            if t["status"] == "live":
                self.assertTrue((WURZEL / t["pfad"]).exists(),
                                f"{t['slug']}: Datei {t['pfad']} fehlt")

    def test_slugs_sind_eindeutig(self):
        reg = json.loads((WURZEL / "tools.json").read_text(encoding="utf-8"))
        slugs = [t["slug"] for t in reg["tools"]]
        self.assertEqual(len(slugs), len(set(slugs)))


class ToolSeiten(unittest.TestCase):
    """Diese Pruefungen gelten automatisch fuer jedes neue Werkzeug.

    Genau das ist der Punkt des Portfolio-Modells: die Qualitaetsschwelle darf
    nicht davon abhaengen, dass beim zwanzigsten Werkzeug noch jemand an die
    Checkliste denkt.
    """

    def tools(self):
        reg = json.loads((WURZEL / "tools.json").read_text(encoding="utf-8"))
        return [t for t in reg["tools"] if t["status"] == "live"
                and t["pfad"].startswith("tools/")]

    def test_kopfdaten_vollstaendig(self):
        for t in self.tools():
            html = (WURZEL / t["pfad"]).read_text(encoding="utf-8")
            with self.subTest(tool=t["slug"]):
                self.assertRegex(html, r"<title>[^<]{20,}</title>")
                self.assertRegex(html, r'name="description" content="[^"]{80,}"')
                self.assertIn('rel="canonical"', html)
                self.assertIn(t["slug"], html, "canonical/slug passt nicht zum Eintrag")

    def test_inhaltsteil_ist_lang_genug(self):
        """Der Textteil unter dem Werkzeug ist der Grund, warum es gefunden wird."""
        for t in self.tools():
            html = (WURZEL / t["pfad"]).read_text(encoding="utf-8")
            with self.subTest(tool=t["slug"]):
                m = re.search(r'<div class="inhalt">(.*?)</div>\s*</main>', html, re.S)
                self.assertIsNotNone(m, "kein Inhaltsteil vorhanden")
                text = re.sub(r"<[^>]+>", " ", m.group(1))
                woerter = len(text.split())
                self.assertGreater(woerter, 550,
                                   f"Inhaltsteil zu kurz ({woerter} Woerter)")

    def test_keine_fremden_ressourcen(self):
        """Kein externes Skript, keine fremde Schriftart - Tempo und Datenschutz."""
        for t in self.tools():
            html = (WURZEL / t["pfad"]).read_text(encoding="utf-8")
            with self.subTest(tool=t["slug"]):
                extern = re.findall(r'(?:src|href)="(https?://[^"]+)"', html)
                erlaubt = [u for u in extern if "philglibota7-bit.github.io" in u
                           or "schema.org" in u]
                self.assertEqual([u for u in extern if u not in erlaubt], [],
                                 "laedt von fremden Servern")

    def test_bindet_die_plattform_ein(self):
        for t in self.tools():
            html = (WURZEL / t["pfad"]).read_text(encoding="utf-8")
            with self.subTest(tool=t["slug"]):
                self.assertIn("platform/werkbank.css", html)
                self.assertIn("platform/werkbank.js", html)
                self.assertRegex(html, r"Werkbank\.start\(")

    def test_pro_funktionen_sind_auch_verbaut(self):
        """Was auf der Pro-Seite versprochen wird, muss im Werkzeug eine
        Schranke haben - sonst verkauft man Luft."""
        for t in self.tools():
            if not t.get("pro"):
                continue
            html = (WURZEL / t["pfad"]).read_text(encoding="utf-8")
            with self.subTest(tool=t["slug"]):
                self.assertIn("Werkbank.pro(", html,
                              "Pro-Funktionen angekuendigt, aber keine Schranke im Code")


class Lizenz(unittest.TestCase):
    """Der Schluesselgenerator im CLI und die Pruefung im Browser muessen
    dasselbe Alphabet benutzen. Driftet eins davon, verkauft man Schluessel,
    die niemand einloesen kann - deshalb dieser Test."""

    def test_alphabet_stimmt_mit_werkbank_js_ueberein(self):
        js = (WURZEL / "platform" / "werkbank.js").read_text(encoding="utf-8")
        treffer = re.search(r'var alphabet = "([^"]+)"', js)
        self.assertIsNotNone(treffer, "Alphabet in werkbank.js nicht gefunden")
        self.assertEqual(treffer.group(1), cli.ALPHABET)

    def test_erzeugte_schluessel_bestehen_die_pruefziffer(self):
        import random
        random.seed(1)
        for _ in range(200):
            kern = "".join(random.choice(cli.ALPHABET) for _ in range(8))
            pruef = cli.ALPHABET[sum(ord(c) for c in kern) % len(cli.ALPHABET)]
            schluessel = f"WB-{kern[:4]}-{kern[4:]}-{pruef}"
            self.assertRegex(schluessel, r"^WB-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]$")
            # Pruefziffer unabhaengig nachrechnen
            k = schluessel[3:7] + schluessel[8:12]
            self.assertEqual(schluessel[-1],
                             cli.ALPHABET[sum(ord(c) for c in k) % len(cli.ALPHABET)])


class Generator(unittest.TestCase):
    def test_build_erzeugt_alle_seiten(self):
        import build
        d = build.laden()
        for name, funktion in [("katalog", build.katalog), ("pro", build.pro_seite),
                               ("impressum", build.impressum),
                               ("datenschutz", build.datenschutz)]:
            html = funktion(d)
            self.assertIn("<!doctype html>", html, name)
            self.assertIn("werkbank.css", html, name)
            self.assertNotIn("{e(", html, f"{name}: nicht ersetzter Platzhalter")

    def test_basispfad_aus_domain(self):
        import build
        faelle = {
            "https://name.github.io/1": "/1/",
            "https://name.github.io/1/": "/1/",
            "https://eigene-domain.de": "/",
            "https://eigene-domain.de/": "/",
            "https://x.github.io/a/b": "/a/b/",
        }
        for domain, erwartet in faelle.items():
            with self.subTest(domain=domain):
                self.assertEqual(build.basispfad({"domain": domain}), erwartet)

    def test_404_zeigt_auf_den_richtigen_basispfad(self):
        """Die 404-Seite wird in beliebiger Tiefe ausgeliefert - relative
        Pfade greifen dort nicht."""
        import build
        d = build.laden()
        html = build.nicht_gefunden(d)
        b = build.basispfad(d["marke"])
        self.assertIn(f'href="{b}platform/werkbank.css"', html)
        self.assertIn(f'src="{b}platform/werkbank.js"', html)
        self.assertIn('name="robots" content="noindex"', html)

    def test_sitemap_ist_deterministisch(self):
        """Ohne das schlaegt die Pruefung in der CI jeden Tag neu fehl."""
        import build
        d = build.laden()
        self.assertNotIn("lastmod", build.sitemap(d))
        self.assertEqual(build.sitemap(d), build.sitemap(d))

    def test_sitemap_enthaelt_jedes_live_tool(self):
        import build
        d = build.laden()
        xml = build.sitemap(d)
        for t in build.live(d["tools"]):
            self.assertIn(t["pfad"], xml)


if __name__ == "__main__":
    unittest.main()

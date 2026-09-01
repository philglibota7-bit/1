"""Tests der Shorts-Kette: python3 -m unittest discover -s tests"""

import json
import sys
import unittest
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WURZEL / "shorts"))

import schnitt        # noqa: E402
import untertitel     # noqa: E402
from untertitel import Wort  # noqa: E402

KONFIG = json.loads((WURZEL / "shorts" / "konfig.json").read_text(encoding="utf-8"))


class AssFormat(unittest.TestCase):
    def test_farbe_wird_nach_bgr_gedreht(self):
        """ASS speichert BGR. Ohne die Drehung kommt die Farbe falsch heraus -
        das ist der haeufigste Fehler bei selbst erzeugten ASS-Dateien."""
        self.assertEqual(untertitel.farbe("00E5FF"), "&H00FFE500")
        self.assertEqual(untertitel.farbe("#FFFFFF"), "&H00FFFFFF")
        self.assertEqual(untertitel.farbe("FF0000"), "&H000000FF")

    def test_ungueltige_farbe_fliegt_auf(self):
        for schrott in ["", "12345", "GGGGGG12"]:
            with self.assertRaises(ValueError):
                untertitel.farbe(schrott)

    def test_zeitformat(self):
        self.assertEqual(untertitel.zeit(0), "0:00:00.00")
        self.assertEqual(untertitel.zeit(3725.5), "1:02:05.50")
        self.assertEqual(untertitel.zeit(-5), "0:00:00.00")

    def test_geschweifte_klammern_werden_entschaerft(self):
        """In ASS leiten sie Steuerbefehle ein - im Text zerstoeren sie die Zeile."""
        self.assertNotIn("{", untertitel.schuetzen("a {b} c"))
        self.assertNotIn("}", untertitel.schuetzen("a {b} c"))


class Gruppierung(unittest.TestCase):
    def test_wird_nach_wortzahl_umgebrochen(self):
        w = [Wort(str(i), i * 0.3, i * 0.3 + 0.25) for i in range(7)]
        self.assertEqual([len(g) for g in untertitel.gruppieren(w, 3)], [3, 3, 1])

    def test_lange_pause_beendet_die_gruppe(self):
        w = [Wort("a", 0, 0.3), Wort("b", 0.3, 0.6), Wort("c", 5.0, 5.3)]
        gruppen = untertitel.gruppieren(w, 5)
        self.assertEqual(len(gruppen), 2, "Pause muss trennen, auch wenn Platz waere")

    def test_leere_eingabe(self):
        self.assertEqual(untertitel.gruppieren([], 3), [])


class Ausschnitt(unittest.TestCase):
    def test_woerter_werden_an_den_raendern_beschnitten(self):
        w = [Wort("vorher", 0, 5), Wort("mitte", 8, 9), Wort("nachher", 20, 25)]
        drin = untertitel.ausschnitt(w, 4, 21)
        self.assertEqual([x.text for x in drin], ["vorher", "mitte", "nachher"])
        self.assertEqual(drin[0].start, 4, "Anfang muss auf den Clipstart gezogen werden")
        self.assertEqual(drin[-1].ende, 21, "Ende muss auf das Clipende gezogen werden")

    def test_woerter_ausserhalb_fallen_weg(self):
        w = [Wort("weg", 0, 1), Wort("drin", 10, 11), Wort("auch weg", 30, 31)]
        self.assertEqual([x.text for x in untertitel.ausschnitt(w, 5, 20)], ["drin"])


class AssErzeugen(unittest.TestCase):
    def bau(self, versatz=0.0):
        w = [Wort("eins", 10, 10.4), Wort("zwei", 10.4, 10.8), Wort("drei", 10.8, 11.2)]
        return untertitel.ass_erzeugen(w, KONFIG["untertitel"], 1080, 1920, versatz)

    def test_grundgeruest(self):
        ass = self.bau()
        for pflicht in ("[Script Info]", "[V4+ Styles]", "[Events]",
                        "PlayResX: 1080", "PlayResY: 1920", "Style: Haupt"):
            self.assertIn(pflicht, ass)

    def test_je_wort_ein_eintrag(self):
        """Die Hervorhebung wandert - dafuer braucht jedes Wort eine Zeile."""
        self.assertEqual(self.bau().count("Dialogue:"), 3)

    def test_versatz_verschiebt_die_zeiten(self):
        """Ohne Versatz stuenden die Untertitel im Clip an der falschen Stelle."""
        self.assertIn("0:00:10.00", self.bau(versatz=0))
        self.assertIn("0:00:00.00", self.bau(versatz=10))

    def test_umlaute_bleiben_erhalten(self):
        w = [Wort("Straße", 0, 1), Wort("größer", 1, 2)]
        ass = untertitel.ass_erzeugen(w, KONFIG["untertitel"], 1080, 1920)
        self.assertIn("Straße", ass)
        self.assertIn("größer", ass)


class Filterkette(unittest.TestCase):
    def test_zielformat_ist_hochkant(self):
        for modus in ("zuschnitt", "unschaerfe"):
            with self.subTest(modus=modus):
                k = schnitt.filterkette(modus, KONFIG, None)
                self.assertIn("1080:1920", k)
                self.assertTrue(k.rstrip().endswith("[v]"))

    def test_unschaerfe_legt_das_bild_auf_den_hintergrund(self):
        k = schnitt.filterkette("unschaerfe", KONFIG, None)
        self.assertIn("gblur", k)
        self.assertIn("overlay", k)
        self.assertIn("force_original_aspect_ratio=decrease", k,
                      "Vordergrund darf nicht beschnitten werden")

    def test_sonderzeichen_im_pfad_werden_entwertet(self):
        """Ein Doppelpunkt im Pfad wuerde die Filterkette sonst zerreissen."""
        k = schnitt.filterkette("zuschnitt", KONFIG, Path("/a b/c:d.ass"))
        self.assertIn("\\:", k)
        self.assertIn("subtitles=", k)


class Kandidaten(unittest.TestCase):
    def abschrift(self, saetze):
        segs, t = [], 20.0
        for text in saetze:
            woerter = text.split()
            ws = []
            for w in woerter:
                ws.append({"wort": w, "start": round(t, 2), "ende": round(t + 0.3, 2)})
                t += 0.35
            segs.append({"start": ws[0]["start"], "ende": ws[-1]["ende"],
                         "text": text, "woerter": ws})
            t += 0.4
        return {"segmente": segs}

    def test_ohne_abschrift_keine_kandidaten(self):
        self.assertEqual(schnitt.kandidaten({"segmente": []}, KONFIG), [])

    def test_clips_halten_die_laengengrenzen_ein(self):
        satz = "Warum die meisten hier genau diesen einen Fehler machen."
        d = self.abschrift([satz] * 12)
        for k in schnitt.kandidaten(d, KONFIG):
            with self.subTest(von=k["von"]):
                self.assertGreaterEqual(k["dauer"], KONFIG["clips"]["min_sekunden"])
                self.assertLessEqual(k["dauer"], KONFIG["clips"]["max_sekunden"])

    def test_clips_ueberschneiden_sich_nicht(self):
        d = self.abschrift(["Warum das hier wichtig ist und niemand darueber redet."] * 30)
        liste = schnitt.kandidaten(d, KONFIG)
        for a, b in zip(liste, liste[1:]):
            self.assertLessEqual(a["bis"], b["von"], "Clips duerfen sich nicht ueberlappen")

    def test_aufhaenger_wird_hoeher_bewertet(self):
        mit = schnitt.bewerten("Warum die meisten hier einen Fehler machen und wie du "
                               "ihn in zwei Minuten behebst ohne etwas zu bezahlen", 30, 60)
        ohne = schnitt.bewerten("Also dann machen wir jetzt einfach mal weiter mit dem "
                                "naechsten Teil von dem was wir vorhin hatten", 30, 60)
        self.assertGreater(mit, ohne)

    def test_intro_wird_abgewertet(self):
        text = "Warum die meisten hier einen Fehler machen und wie du das loest"
        self.assertGreater(schnitt.bewerten(text, 30, 300),
                           schnitt.bewerten(text, 30, 5))


class Konfiguration(unittest.TestCase):
    def test_konfig_ist_vollstaendig(self):
        for block, felder in {
            "video": ["breite", "hoehe", "bildrate", "crf"],
            "audio": ["lautheit_lufs", "bitrate"],
            "abschrift": ["modell", "sprache"],
            "clips": ["min_sekunden", "max_sekunden", "anzahl"],
            "untertitel": ["schrift", "groesse", "farbe", "farbe_aktiv"],
        }.items():
            for feld in felder:
                with self.subTest(block=block, feld=feld):
                    self.assertIn(feld, KONFIG[block])

    def test_zielformat_ist_neun_zu_sechzehn(self):
        v = KONFIG["video"]
        self.assertAlmostEqual(v["breite"] / v["hoehe"], 9 / 16, places=4)

    def test_maximallaenge_passt_zu_shorts(self):
        self.assertLessEqual(KONFIG["clips"]["max_sekunden"], 60)

    def test_standardschrift_gibt_es_auf_dem_mac(self):
        """DejaVu Sans gibt es auf keinem Mac - eine still ersetzte Schrift
        faellt erst am fertigen Video auf."""
        self.assertIn(KONFIG["untertitel"]["schrift"],
                      ("Helvetica", "Arial", "Impact", "Arial Black"))


if __name__ == "__main__":
    unittest.main()

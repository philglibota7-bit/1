#!/usr/bin/env python3
"""NASA-Mosaike fuer ORBIT.

Im Betrachter von claude.ai laedt eine Seite nichts von fremden Servern; die
Satellitenbilder von Esri kommen dort nie an. Was neben der Seite liegt, kommt
an. Dieses Werkzeug holt deshalb Blue Marble (mit Relief und Meeresboden) von
NASA GIBS, gemeinfrei, in Web-Mercator bei Stufe 6: 64 x 64 Kacheln zu 256
Punkten, gut 2,4 Kilometer je Punkt am Aequator, 1,6 in Mitteleuropa. Je 8 x 8
Kacheln werden zu einem Bild von 2048 x 2048 Punkten, zusammen 64 Bilder.
ORBIT schneidet sich die Kacheln daraus selbst heraus.

Dazu die Lichter der Nacht aus Black Marble 2016, im selben Netz, als
Graustufen: nur die Lichter, warm und hell, weich gesaettigt, genau wie ORBIT
die scharfen Nachtlichter von GIBS aufbereitet. Das mondbeschienene Gelaende
und der blaeuliche Schnee bleiben dunkel. Name: 6-x-y-n.jpg.

Aufruf: python3 werkzeug/orbit-nasa-mosaike.py [Zielordner] [Rohordner]
Vorgabe: orbit-nasa neben orbit.html; die einzelnen Kacheln landen im
Rohordner (Vorgabe: Zielordner/_roh) und werden beim zweiten Lauf nicht neu
geholt.
"""
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from PIL import Image

GIBS = "https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/"
EBENEN = {
    # Der Tag: Land mit Relief, Meeresboden
    "tag": GIBS + "BlueMarble_ShadedRelief_Bathymetry/default/GoogleMapsCompatible_Level8/{z}/{y}/{x}.jpeg",
    # Die Nacht: Black Marble 2016, daraus nur die Lichter
    "nacht": GIBS + "VIIRS_Black_Marble/default/2016-01-01/GoogleMapsCompatible_Level8/{z}/{y}/{x}.png",
}
STUFE = 6
N = 1 << STUFE          # Kacheln je Seite der Welt
JE = 8                  # Kacheln je Seite eines Mosaiks
GUETE = 82

hier = os.path.dirname(os.path.abspath(__file__))
ziel = sys.argv[1] if len(sys.argv) > 1 else os.path.join(hier, "..", "orbit-nasa")
roh = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ziel, "_roh")
os.makedirs(ziel, exist_ok=True)
os.makedirs(roh, exist_ok=True)


def rohpfad(ebene, x, y):
    return os.path.join(roh, f"{STUFE}-{x}-{y}.jpg" if ebene == "tag" else f"{STUFE}-{x}-{y}-{ebene}.png")


def hole(auftrag):
    ebene, x, y = auftrag
    pfad = rohpfad(ebene, x, y)
    if os.path.exists(pfad) and os.path.getsize(pfad) > 0:
        return pfad
    fehler = None
    for versuch in range(6):
        try:
            with urllib.request.urlopen(EBENEN[ebene].format(z=STUFE, x=x, y=y), timeout=60) as antwort:
                daten = antwort.read()
            if not (daten.startswith(b"\xff\xd8") or daten.startswith(b"\x89PNG")):
                raise ValueError("kein Bild")
            with open(pfad + ".neu", "wb") as f:
                f.write(daten)
            os.replace(pfad + ".neu", pfad)
            return pfad
        except Exception as e:  # noqa: BLE001 - jeder Fehler: nochmal, dann aufgeben
            fehler = e
            time.sleep(2 ** versuch)
    raise RuntimeError(f"Kachel {STUFE}/{x}/{y}: {fehler}")


def nur_lichter(bild):
    """Wie lichterAufbereiten in orbit.html, ohne das Glaetten: bei
    Stufe 6 ist Black Marble schon aus dem Feineren heruntergerechnet."""
    r, g, b = [k.astype("float32") for k in np.asarray(bild.convert("RGB")).transpose(2, 0, 1)]
    roh_ = np.maximum(0, 0.3 * r + 0.55 * g + 0.15 * b - 1.2 * np.maximum(0, b - r) - 20) / 235
    return Image.fromarray(np.round(255 * (1 - np.exp(-2.5 * roh_))).astype("uint8"), "L")


alle = [(e, x, y) for e in EBENEN for y in range(N) for x in range(N)]
start = time.time()
with ThreadPoolExecutor(8) as pool:
    for i, _ in enumerate(pool.map(hole, alle), 1):
        if i % 512 == 0:
            print(f"{i}/{len(alle)} Kacheln, {time.time() - start:.0f} s", flush=True)

summe = {"tag": 0, "nacht": 0}
for my in range(N // JE):
    for mx in range(N // JE):
        for ebene in EBENEN:
            bild = Image.new("RGB" if ebene == "tag" else "L", (JE * 256, JE * 256))
            for j in range(JE):
                for i in range(JE):
                    with Image.open(rohpfad(ebene, mx * JE + i, my * JE + j)) as k:
                        bild.paste(k.convert("RGB") if ebene == "tag" else nur_lichter(k), (i * 256, j * 256))
            pfad = os.path.join(ziel, f"{STUFE}-{mx}-{my}.jpg" if ebene == "tag" else f"{STUFE}-{mx}-{my}-n.jpg")
            bild.save(pfad, quality=GUETE, optimize=True, subsampling=2)
            summe[ebene] += os.path.getsize(pfad)
print(f"{(N // JE) ** 2} Mosaike je Ebene, Tag {summe['tag'] / 1e6:.1f} MB, Nacht {summe['nacht'] / 1e6:.1f} MB, in {ziel}")

"""
Aufnahme-Helfer: Templates ausschneiden und Koordinaten ablesen.

Damit legst du fest, WAS der Bot anklicken soll (Templates) und WO Joystick /
Schuss liegen (Koordinaten). Das Tool holt einen echten Screenshot aus einer
LDPlayer-Instanz und laesst dich direkt darauf arbeiten.

Start (mit dem Port der gewuenschten Instanz):
    python capture.py --port 5555
    python capture.py --port 5555 --adb "C:\\LDPlayer\\LDPlayer9\\adb.exe"

Bedienung im Bildfenster:
    * Linksklick     -> zeigt die Koordinate (x, y) an. Genau dieselben Zahlen
                        gehoerst du in die Config unter "joystick" (Mittelpunkt
                        des Bewegungssticks) bzw. "attack" (Schuss-Punkt).
    * Taste  c       -> Ausschnitt-Modus: Rechteck mit der Maus aufziehen,
                        dann ENTER. Anschliessend im Konsolenfenster einen
                        Namen eintippen (z. B. play_button) -> wird als
                        templates/play_button.png gespeichert.
    * Taste  r       -> neuen Screenshot holen (z. B. nach Menuewechsel).
    * Taste  q       -> beenden.

Wichtig: Aufloesung. Die Klick-Koordinaten passen 1:1 als Tap-Koordinaten,
solange der LDPlayer eine normale Aufloesung hat, die auf deinen Monitor passt
(z. B. 960x540 oder 1280x720). Sehr grosse Aufloesungen bitte im LDPlayer
kleiner stellen, sonst skaliert das Fenster und die Koordinaten stimmen nicht.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2

from ldplayer import LDPlayer

TEMPLATE_DIR = Path(__file__).parent / "templates"
WINDOW = "Capture - Linksklick=Koordinate  c=Ausschnitt  r=neu  q=Ende"


def save_template(crop) -> None:
    TEMPLATE_DIR.mkdir(exist_ok=True)
    name = input("Dateiname fuer den Ausschnitt (ohne .png): ").strip()
    if not name:
        print("  -> abgebrochen (kein Name).")
        return
    if not name.endswith(".png"):
        name += ".png"
    path = TEMPLATE_DIR / name
    cv2.imwrite(str(path), crop)
    print(f"  -> gespeichert: {path}")


def main() -> None:
    p = argparse.ArgumentParser(description="Template-/Koordinaten-Helfer")
    p.add_argument("--port", type=int, default=5555, help="ADB-Port der Instanz")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--adb", default="adb", help="Pfad zu adb.exe")
    args = p.parse_args()

    ld = LDPlayer(host=args.host, port=args.port, adb_path=args.adb)
    print(f"Verbinde mit {ld.serial} ...")
    ld.connect()
    print("Verbunden. Hole Screenshot ...")

    screen = ld.screenshot()
    print(f"Aufloesung: {screen.shape[1]} x {screen.shape[0]} px\n")
    print("Fenster ist offen. Tasten: Linksklick=Koordinate  c=Ausschnitt  "
          "r=neu  q=Ende")

    def on_mouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(f"  Koordinate: x={x}  y={y}")

    cv2.namedWindow(WINDOW, cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback(WINDOW, on_mouse)

    while True:
        cv2.imshow(WINDOW, screen)
        key = cv2.waitKey(30) & 0xFF
        if key == ord("q"):
            break
        if key == ord("r"):
            screen = ld.screenshot()
            print("  -> neuer Screenshot geholt.")
        if key == ord("c"):
            print("  Ziehe ein Rechteck auf und druecke ENTER (oder c zum "
                  "Abbrechen) ...")
            roi = cv2.selectROI(WINDOW, screen, showCrosshair=True)
            x, y, w, h = roi
            if w > 0 and h > 0:
                crop = screen[y:y + h, x:x + w]
                save_template(crop)
            else:
                print("  -> kein Bereich gewaehlt.")

    cv2.destroyAllWindows()
    print("Beendet.")


if __name__ == "__main__":
    main()

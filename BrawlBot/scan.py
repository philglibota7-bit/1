"""
LDPlayer-Instanzen finden und ihre ADB-Ports anzeigen.

Startet man mehrere LDPlayer-Fenster, lauscht jede Instanz auf einem eigenen
ADB-Port (typisch 5555, 5557, 5559 ... je +2). Dieses Tool probiert einen
Portbereich durch, verbindet sich und zeigt zu jeder erreichbaren Instanz
Modell/Android-Version an -- so weisst du, welcher Port zu welchem Fenster
gehoert und was du in config.brawlstars.json eintragen musst.

Start:
    python scan.py                       # prueft 5555..5585
    python scan.py --start 5555 --count 16
    python scan.py --adb "C:\\LDPlayer\\LDPlayer9\\adb.exe"

Tipp: Am eindeutigsten benennst du jede Instanz IM Spiel/Emulator klar
(z. B. Geraetename), dann kannst du sie hier zuordnen. Alternativ die Fenster
einzeln starten und jeweils scannen.
"""

from __future__ import annotations

import argparse
import subprocess


def adb(adb_path: str, *args: str, timeout: float = 8.0) -> str:
    try:
        out = subprocess.run([adb_path, *args], capture_output=True,
                             text=True, timeout=timeout)
        return (out.stdout or "").strip()
    except Exception:  # noqa: BLE001
        return ""


def prop(adb_path: str, serial: str, name: str) -> str:
    return adb(adb_path, "-s", serial, "shell", "getprop", name)


def main() -> None:
    p = argparse.ArgumentParser(description="LDPlayer ADB-Ports scannen")
    p.add_argument("--adb", default="adb", help="Pfad zu adb.exe")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--start", type=int, default=5555)
    p.add_argument("--count", type=int, default=16,
                   help="Wie viele Ports (Schrittweite 2) geprueft werden")
    args = p.parse_args()

    print(f"Scanne {args.host}:{args.start} bis "
          f"{args.start + (args.count - 1) * 2} ...\n")

    found = []
    for i in range(args.count):
        port = args.start + i * 2
        serial = f"{args.host}:{port}"
        adb(args.adb, "connect", serial)               # Verbindung versuchen
        state = adb(args.adb, "-s", serial, "get-state")
        if state != "device":
            continue
        model = prop(args.adb, serial, "ro.product.model") or "?"
        release = prop(args.adb, serial, "ro.build.version.release") or "?"
        found.append((port, model, release))
        print(f"  ✓ Port {port:>5}  Modell: {model:<20}  Android {release}")

    print()
    if not found:
        print("Keine Instanz gefunden. Pruefe:")
        print("  - Laeuft mindestens ein LDPlayer-Fenster?")
        print("  - Ist ADB-Debugging in der Instanz aktiviert?")
        print("  - Stimmt der adb-Pfad? (--adb \"...\\adb.exe\")")
        return

    print("Fuer config.brawlstars.json  ->  \"instances\":")
    print("  [")
    for n, (port, _model, _rel) in enumerate(found):
        komma = "," if n < len(found) - 1 else ""
        print(f'    {{ "name": "Account-{n+1}", "port": {port}, '
              f'"ld_index": {n} }}{komma}')
    print("  ]")


if __name__ == "__main__":
    main()

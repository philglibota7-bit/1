"""
Mehrere LDPlayer-Fenster gleichzeitig steuern.

Jede LDPlayer-Instanz hat eine eigene ADB-Adresse:
    Instanz 0 -> 127.0.0.1:5555
    Instanz 1 -> 127.0.0.1:5557
    Instanz 2 -> 127.0.0.1:5559   (immer +2)

Dieses Skript startet fuer jede in der Config gelistete Instanz einen
eigenen Thread mit einem eigenen BrawlBot. So laufen z. B. vier Accounts
parallel in vier Fenstern.

Optional koennen die Fenster vorab automatisch gestartet werden, wenn in der
Config der Pfad zu 'ldconsole.exe' (LDPlayer-Installationsordner) steht.

Start:
    python multi.py                # nutzt config.brawlstars.json
    python multi.py --config x.json

WICHTIG: Automatisierung von Brawl Stars verstoesst gegen Supercells
Nutzungsbedingungen und fuehrt zu Sperren. Nur mit Wegwerf-Accounts nutzen.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import threading
import time
from pathlib import Path

from brawl import BrawlBot
from ldplayer import LDPlayer

HERE = Path(__file__).parent


def launch_instance(ldconsole: str, index: int) -> None:
    """Startet eine LDPlayer-Instanz ueber ldconsole.exe (optional)."""
    try:
        subprocess.run([ldconsole, "launch", "--index", str(index)], check=False)
    except FileNotFoundError:
        print(f"ldconsole nicht gefunden: {ldconsole} (Instanz {index} bitte "
              f"manuell starten).")


def run_instance(inst: dict, cfg: dict) -> None:
    tag = f"[{inst.get('name', inst['port'])}]"
    ld = LDPlayer(
        host=cfg.get("host", "127.0.0.1"),
        port=inst["port"],
        adb_path=cfg.get("adb_path", "adb"),
    )
    try:
        ld.connect()
    except Exception as exc:  # noqa: BLE001 - pro Instanz robust bleiben
        print(f"{tag} Verbindung fehlgeschlagen: {exc}")
        return
    bot = BrawlBot(ld, cfg, tag=tag)
    try:
        bot.run()
    except KeyboardInterrupt:
        pass
    except Exception as exc:  # noqa: BLE001
        print(f"{tag} Fehler: {exc}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Brawl Stars Multi-Instanz-Bot")
    parser.add_argument("--config", default="config.brawlstars.json")
    args = parser.parse_args()

    cfg_path = HERE / args.config
    if not cfg_path.exists():
        raise SystemExit(
            f"{cfg_path.name} fehlt. Kopiere config.brawlstars.example.json "
            f"nach {cfg_path.name} und passe sie an."
        )
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

    instances = cfg.get("instances", [])
    if not instances:
        raise SystemExit("Keine 'instances' in der Config definiert.")

    # optional: Fenster automatisch starten
    ldconsole = cfg.get("ldconsole")
    if ldconsole:
        for inst in instances:
            if "ld_index" in inst:
                launch_instance(ldconsole, inst["ld_index"])
        print("Warte, bis die Instanzen hochgefahren sind ...")
        time.sleep(cfg.get("boot_wait", 25))

    threads = []
    for inst in instances:
        th = threading.Thread(target=run_instance, args=(inst, cfg), daemon=True)
        th.start()
        threads.append(th)
        time.sleep(1.0)  # gestaffelt starten, ADB nicht ueberrennen

    print(f"{len(threads)} Instanz(en) gestartet. Zum Beenden: Strg+C")
    try:
        while any(t.is_alive() for t in threads):
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\nBeende alle Instanzen ...")


if __name__ == "__main__":
    main()

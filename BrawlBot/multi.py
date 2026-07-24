"""
Mehrere LDPlayer-Fenster gleichzeitig steuern -- Konsolen-Variante.

Fuer eine grafische Bedienung stattdessen 'python gui.py' starten.

Jede LDPlayer-Instanz hat eine eigene ADB-Adresse:
    Instanz 0 -> 127.0.0.1:5555
    Instanz 1 -> 127.0.0.1:5557   (immer +2)

Dieses Skript startet fuer jede in der Config gelistete Instanz einen Bot
und laesst sie parallel laufen, bis du mit Strg+C abbrichst.

Start:
    python multi.py                       # nutzt config.brawlstars.json
    python multi.py --config x.json
    python multi.py --dry-run             # nur erkennen, keine Eingaben

WICHTIG: Automatisierung von Brawl Stars verstoesst gegen Supercells
Nutzungsbedingungen und fuehrt zu Sperren. Nur mit Wegwerf-Accounts nutzen.
"""

from __future__ import annotations

import argparse
import subprocess
import time

from controller import BotController, load_config


def launch_windows(cfg: dict) -> None:
    """Startet LDPlayer-Instanzen optional ueber ldconsole.exe."""
    ldconsole = cfg.get("ldconsole")
    if not ldconsole:
        return
    for inst in cfg.get("instances", []):
        if "ld_index" in inst:
            try:
                subprocess.run([ldconsole, "launch", "--index",
                                str(inst["ld_index"])], check=False)
            except FileNotFoundError:
                print(f"ldconsole nicht gefunden: {ldconsole} "
                      f"(Instanz {inst['ld_index']} bitte manuell starten).")
    print("Warte, bis die Instanzen hochgefahren sind ...")
    time.sleep(cfg.get("boot_wait", 25))


def main() -> None:
    parser = argparse.ArgumentParser(description="Brawl Stars Multi-Instanz-Bot")
    parser.add_argument("--config", default="config.brawlstars.json")
    parser.add_argument("--dry-run", action="store_true",
                        help="Nur erkennen, keine Eingaben senden.")
    args = parser.parse_args()

    cfg = load_config(args.config)
    if not cfg.get("instances"):
        raise SystemExit("Keine 'instances' in der Config definiert.")

    launch_windows(cfg)

    controller = BotController(cfg)
    controller.start_all(dry_run=args.dry_run)
    print(f"{len(controller.instances())} Instanz(en) gestartet. "
          f"Zum Beenden: Strg+C")

    try:
        while controller.any_running():
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\nBeende alle Instanzen ...")
        controller.stop_all()
        controller.join_all(timeout=8)


if __name__ == "__main__":
    main()

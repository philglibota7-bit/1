"""
Game-Bot fuer LDPlayer -- Grundgeruest.

Ablauf (Loop):
  1. Screenshot vom Emulator holen
  2. Nach bekannten Bild-Elementen suchen (templates/)
  3. Passende Aktion ausfuehren (tippen / wischen / warten)
  4. Wiederholen

Die Aktionsregeln stehen in config.json und lassen sich ohne Code-Aenderung
anpassen. So passt du den Bot an ein neues Spiel an, indem du Screenshots als
Templates ablegst und Regeln in die Config schreibst.

Start:
    python bot.py               # nutzt config.json
    python bot.py --dry-run     # erkennt nur, tippt aber NICHT (zum Testen)

Hinweis: Automatisierung kann gegen die Nutzungsbedingungen eines Spiels
verstossen. Nur fuer eigene Projekte / erlaubte Faelle verwenden.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import vision
from ldplayer import LDPlayer

CONFIG_PATH = Path(__file__).parent / "config.json"


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        example = CONFIG_PATH.with_name("config.example.json")
        raise SystemExit(
            f"{CONFIG_PATH.name} fehlt. Kopiere {example.name} nach "
            f"{CONFIG_PATH.name} und passe sie an."
        )
    with open(CONFIG_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def run_rule(ld: LDPlayer, screen, rule: dict, dry_run: bool) -> bool:
    """Prueft eine Regel gegen den Screenshot. True = Regel hat gegriffen."""
    threshold = rule.get("threshold", 0.85)
    match = vision.find(screen, rule["template"], threshold)
    if not match.found:
        return False

    action = rule.get("action", "tap")
    print(f"  [{match.score:.2f}] '{rule['name']}' erkannt -> {action}")

    if dry_run:
        return True

    if action == "tap":
        ld.tap(match.x, match.y)
    elif action == "swipe":
        s = rule["swipe"]  # [x1, y1, x2, y2, ms]
        ld.swipe(*s)
    elif action == "key":
        ld.key(rule["keycode"])
    elif action == "wait":
        pass  # nur erkennen, dann warten
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="LDPlayer Game-Bot")
    parser.add_argument("--dry-run", action="store_true",
                        help="Nur erkennen, keine Eingaben senden.")
    args = parser.parse_args()

    cfg = load_config()
    ld = LDPlayer(
        host=cfg.get("host", "127.0.0.1"),
        port=cfg.get("port", 5555),
        adb_path=cfg.get("adb_path", "adb"),
    )

    print(f"Verbinde mit LDPlayer ({ld.serial}) ...")
    ld.connect()
    print("Verbunden. Bot laeuft. Zum Beenden: Strg+C\n")

    loop_delay = cfg.get("loop_delay", 1.0)
    rules = cfg.get("rules", [])

    try:
        while True:
            screen = ld.screenshot()
            for rule in rules:
                if run_rule(ld, screen, rule, args.dry_run):
                    # nach einem Treffer optional extra warten
                    time.sleep(rule.get("cooldown", 0))
                    break
            time.sleep(loop_delay)
    except KeyboardInterrupt:
        print("\nBot gestoppt.")


if __name__ == "__main__":
    main()

"""
Brawl-Stars-Ablauflogik fuer eine einzelne LDPlayer-Instanz.

Zustandsautomat (State Machine):

    MENU   -> "Play"-Button erkannt        -> tippen, in die Warteschlange
    QUEUE  -> warten, bis Match startet
    MATCH  -> einfache Spiel-Routine (laufen + schiessen) fuer eine Weile
    END    -> Ende-/Weiter-/OK-Bildschirme wegtippen
    -> zurueck zu MENU (automatisch "wieder bereit machen")

Nach 'matches_per_account' Matches wird optional der Account gewechselt.

Der Bot ist so gebaut, dass er von der grafischen Oberflaeche (gui.py) sauber
gesteuert werden kann:
  * stop_event   -> Bot bricht die Schleifen kontrolliert ab
  * on_status(s) -> meldet den aktuellen Zustand (MENU/QUEUE/MATCH/...)
  * on_log(msg)  -> leitet Log-Zeilen an die Oberflaeche weiter
  * dry_run      -> erkennt nur, sendet aber KEINE Eingaben (zum Testen)

WICHTIG / rechtlich:
  Brawl Stars gehoert Supercell. Automatisierung verstoesst gegen deren
  Nutzungsbedingungen und fuehrt regelmaessig zu (dauerhaften) Sperren.
  Nur mit Wegwerf-Accounts und auf eigene Verantwortung verwenden.

Da sich die Brawl-Stars-Oberflaeche je nach Version, Sprache und Aufloesung
unterscheidet, musst du eigene Screenshots als Templates in 'templates/'
ablegen -- fertige Templates gibt es nicht.
"""

from __future__ import annotations

import math
import random
import threading
import time
from typing import Callable, Optional

import vision
from ldplayer import LDPlayer


class BrawlBot:
    def __init__(
        self,
        ld: LDPlayer,
        cfg: dict,
        tag: str = "",
        stop_event: Optional[threading.Event] = None,
        on_status: Optional[Callable[[str], None]] = None,
        on_log: Optional[Callable[[str], None]] = None,
        dry_run: bool = False,
    ):
        self.ld = ld
        self.cfg = cfg
        self.tag = tag
        self.stop_event = stop_event or threading.Event()
        self.on_status = on_status
        self.on_log = on_log
        self.dry_run = dry_run
        self.matches_done = 0
        self.account_index = 0
        self.state = "INIT"

    # ---- Steuerung / Rueckmeldung --------------------------------------
    def stopping(self) -> bool:
        return self.stop_event.is_set()

    def sleep(self, seconds: float) -> None:
        """Wartet, reagiert dabei aber sofort auf Stop."""
        self.stop_event.wait(seconds)

    def log(self, msg: str) -> None:
        line = f"{self.tag} {msg}".strip()
        if self.on_log:
            self.on_log(line)
        else:
            print(line)

    def set_state(self, state: str) -> None:
        self.state = state
        if self.on_status:
            self.on_status(state)

    # ---- Eingaben (respektieren dry_run) -------------------------------
    def _tap(self, x: int, y: int) -> None:
        if self.dry_run:
            return
        self.ld.tap(x, y)

    def _swipe(self, *a: int) -> None:
        if self.dry_run:
            return
        self.ld.swipe(*a)

    def _key(self, code: str) -> None:
        if self.dry_run:
            return
        self.ld.key(code)

    # ---- Wahrnehmung ----------------------------------------------------
    def _see(self, template: str, thr: float = 0.85):
        return vision.find(self.ld.screenshot(), template, thr)

    def _tap_if(self, template: str, thr: float = 0.85) -> bool:
        m = self._see(template, thr)
        if m.found:
            if self.dry_run:
                self.log(f"(dry-run) wuerde '{template}' antippen [{m.score:.2f}]")
            else:
                self.ld.tap(m.x, m.y)
            return True
        return False

    def _wait_for(self, template: str, timeout: float, thr: float = 0.85) -> bool:
        end = time.time() + timeout
        while time.time() < end and not self.stopping():
            if self._see(template, thr).found:
                return True
            self.sleep(1.0)
        return False

    # ---- einzelne Phasen ------------------------------------------------
    def ready_and_play(self) -> bool:
        self.set_state("MENU")
        if self._tap_if(self.cfg["templates"]["play_button"]):
            self.log("Play gedrueckt -> in der Warteschlange.")
            return True
        self.dismiss_popups()
        return False

    def wait_match_start(self) -> bool:
        self.set_state("QUEUE")
        ok = self._wait_for(self.cfg["templates"]["in_match"],
                            self.cfg.get("queue_timeout", 90))
        if ok:
            self.log("Match gestartet.")
        return ok

    def play_match(self) -> None:
        """Einfache Spiel-Routine: zufaellig laufen (Joystick-Swipes) + schiessen."""
        self.set_state("MATCH")
        t = self.cfg["templates"]
        joy = self.cfg["joystick"]      # {"cx","cy","radius"}
        atk = self.cfg["attack"]        # {"x","y"}
        end = time.time() + self.cfg.get("match_max_seconds", 180)

        while time.time() < end and not self.stopping():
            if (self._see(t.get("victory", "victory.png")).found or
                    self._see(t.get("defeat", "defeat.png")).found or
                    self._see(t.get("proceed", "proceed.png")).found):
                self.log("Match-Ende erkannt.")
                return
            ang = random.uniform(0, 2 * math.pi)
            reach = joy["radius"] * random.uniform(0.6, 1.0)
            dx, dy = int(reach * math.cos(ang)), int(reach * math.sin(ang))
            self._swipe(joy["cx"], joy["cy"], joy["cx"] + dx, joy["cy"] + dy, 400)
            self._tap(atk["x"], atk["y"])
            self.sleep(0.4)
        if not self.stopping():
            self.log("Match-Zeit abgelaufen.")

    def dismiss_popups(self) -> None:
        self.set_state("END")
        t = self.cfg["templates"]
        for _ in range(15):
            if self.stopping():
                return
            tapped = False
            for key in ("proceed", "ok", "continue", "reward", "close"):
                name = t.get(key)
                if name and self._tap_if(name):
                    tapped = True
                    self.sleep(1.2)
                    break
            if not tapped:
                if self._see(t["play_button"]).found:
                    return
                self._key("KEYCODE_BACK")
                self.sleep(1.0)

    # ---- Account-Wechsel (fest definierter Ablauf) ----------------------
    def _run_step(self, step: dict) -> bool:
        """
        Fuehrt EINEN Schritt eines festgelegten Ablaufs aus.
        Unterstuetzte 'type'-Werte:
          tap_template : Button per Bild erkennen und antippen (braucht Template)
          tap          : feste Koordinate antippen        -> "x","y"
          swipe        : wischen                           -> "from":[x,y],"to":[x,y],"ms"
          key          : Hardware-Taste                    -> "code" (z. B. KEYCODE_BACK)
          wait         : nur warten
          select_account: naechsten Account aus "accounts" waehlen
        Jeder Schritt kann "wait"/"delay" (Sekunden Pause danach) setzen.
        """
        typ = step.get("type", "tap_template")
        wait = step.get("wait", step.get("delay", 1.5))

        if typ == "tap_template":
            tmpl = step["template"]
            if not self._wait_for(tmpl, step.get("timeout", 15)):
                self.log(f"Schritt-Bild '{tmpl}' nicht gefunden.")
                return False
            self._tap_if(tmpl)
        elif typ == "tap":
            self.log(f"tap ({step['x']}, {step['y']})")
            self._tap(int(step["x"]), int(step["y"]))
        elif typ == "swipe":
            f, t = step["from"], step["to"]
            self._swipe(int(f[0]), int(f[1]), int(t[0]), int(t[1]),
                        int(step.get("ms", 300)))
        elif typ == "key":
            self._key(step["code"])
        elif typ == "wait":
            pass
        elif typ == "select_account":
            if not self._select_account():
                return False
        else:
            self.log(f"Unbekannter Schritt-Typ: {typ}")
            return False

        self.sleep(wait)
        return True

    def _select_account(self) -> bool:
        """Waehlt reihum den naechsten Account aus cfg['accounts']."""
        accounts = self.cfg.get("accounts", [])
        if not accounts:
            return True
        self.account_index = (self.account_index + 1) % len(accounts)
        acc = accounts[self.account_index]
        self.log(f"Waehle Account: {acc.get('name', self.account_index)}")
        if "template" in acc:
            if not self._wait_for(acc["template"], 15):
                self.log("Account-Bild nicht gefunden.")
                return False
            self._tap_if(acc["template"])
        elif "slot" in acc:
            self._tap(int(acc["slot"][0]), int(acc["slot"][1]))
        self.sleep(acc.get("wait", 2.0))
        return True

    def switch_account(self) -> None:
        steps = self.cfg.get("account_switch", {}).get("steps", [])
        if not steps:
            self.log("Kein Account-Wechsel-Ablauf konfiguriert -> uebersprungen.")
            return
        self.set_state("SWITCH")
        self.log("Starte festgelegten Account-Wechsel-Ablauf ...")
        for i, step in enumerate(steps, 1):
            if self.stopping():
                return
            self.log(f"  Schritt {i}/{len(steps)}: {step.get('type', 'tap_template')}")
            if not self._run_step(step):
                self.log("Account-Wechsel abgebrochen (Schritt fehlgeschlagen).")
                return
        self.log("Account-Wechsel abgeschlossen.")

    # ---- Hauptschleife --------------------------------------------------
    def run(self) -> None:
        per_acc = self.cfg.get("matches_per_account", 0)   # 0 = nie wechseln
        self.log("Brawl-Bot laeuft." + (" (DRY-RUN)" if self.dry_run else ""))
        while not self.stopping():
            try:
                if not self.ready_and_play():
                    self.sleep(1.5)
                    continue
                if not self.wait_match_start():
                    self.log("Match nicht gestartet (Timeout) -> zurueck ins Menue.")
                    self.dismiss_popups()
                    continue
                self.play_match()
                self.dismiss_popups()
                self.matches_done += 1
                self.log(f"Matches gesamt: {self.matches_done}")
                if per_acc and self.matches_done % per_acc == 0:
                    self.switch_account()
                self.sleep(self.cfg.get("between_matches", 2.0))
            except Exception as exc:  # noqa: BLE001 - Instanz nicht abstuerzen lassen
                self.log(f"Fehler: {exc} -> versuche in 5 s weiter.")
                self.sleep(5.0)
        self.set_state("STOPPED")
        self.log("Bot gestoppt.")

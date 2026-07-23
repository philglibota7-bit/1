"""
Brawl-Stars-Ablauflogik fuer eine einzelne LDPlayer-Instanz.

Zustandsautomat (State Machine):

    MENU   -> "Play"-Button erkannt        -> tippen, in die Warteschlange
    QUEUE  -> warten, bis Match startet
    MATCH  -> einfache Spiel-Routine (laufen + schiessen) fuer eine Weile
    END    -> Ende-/Weiter-/OK-Bildschirme wegtippen
    -> zurueck zu MENU (automatisch "wieder bereit machen")

Nach 'matches_per_account' Matches wird optional der Account gewechselt.

WICHTIG / rechtlich:
  Brawl Stars gehoert Supercell. Automatisierung verstoesst gegen deren
  Nutzungsbedingungen und fuehrt regelmaessig zu (dauerhaften) Sperren.
  Nur mit Wegwerf-Accounts und auf eigene Verantwortung verwenden.

Alle erkannten Elemente kommen aus 'templates/' und werden in der Config
den Zustaenden zugeordnet. Da sich die Brawl-Stars-Oberflaeche je nach
Version, Sprache und Aufloesung unterscheidet, MUSST du eigene Screenshots
als Templates ablegen -- fertige Templates kann und darf ich nicht liefern.
"""

from __future__ import annotations

import random
import time

import vision
from ldplayer import LDPlayer


class BrawlBot:
    def __init__(self, ld: LDPlayer, cfg: dict, tag: str = ""):
        self.ld = ld
        self.cfg = cfg
        self.tag = tag                      # z. B. "[Instanz 1]" fuer Logs
        self.matches_done = 0
        self.account_index = 0

    # ---- kleine Helfer --------------------------------------------------
    def log(self, msg: str) -> None:
        print(f"{self.tag} {msg}".strip())

    def _see(self, template: str, thr: float = 0.85):
        """Ist 'template' aktuell sichtbar? Gibt den Treffer zurueck."""
        return vision.find(self.ld.screenshot(), template, thr)

    def _tap_if(self, template: str, thr: float = 0.85) -> bool:
        m = self._see(template, thr)
        if m.found:
            self.ld.tap(m.x, m.y)
            return True
        return False

    def _wait_for(self, template: str, timeout: float, thr: float = 0.85) -> bool:
        end = time.time() + timeout
        while time.time() < end:
            if self._see(template, thr).found:
                return True
            time.sleep(1.0)
        return False

    # ---- einzelne Phasen ------------------------------------------------
    def ready_and_play(self) -> bool:
        """Im Menue den Play-Button druecken ('wieder bereit machen')."""
        t = self.cfg["templates"]
        if self._tap_if(t["play_button"]):
            self.log("Play gedrueckt -> in der Warteschlange.")
            return True
        # evtl. haengt noch ein Ende-Dialog -> wegtippen
        self.dismiss_popups()
        return False

    def wait_match_start(self) -> bool:
        """Warten, bis das Match laedt (Joystick / In-Match-Marker sichtbar)."""
        t = self.cfg["templates"]
        started = self._wait_for(t["in_match"], self.cfg.get("queue_timeout", 90))
        if started:
            self.log("Match gestartet.")
        return started

    def play_match(self) -> None:
        """
        Sehr einfache Spiel-Routine: in zufaellige Richtungen 'laufen'
        (kurze Swipes am linken Joystick) und rechts 'schiessen' (Taps).
        Das ist bewusst simpel -- ein Screenshot-Bot spielt nicht clever.
        Endet, sobald ein Ende-Bildschirm erkannt wird oder die Zeit ablaeuft.
        """
        t = self.cfg["templates"]
        joy = self.cfg["joystick"]          # {"cx","cy","radius"}
        atk = self.cfg["attack"]            # {"x","y"}
        end = time.time() + self.cfg.get("match_max_seconds", 180)

        while time.time() < end:
            # Ende erkannt? -> raus
            if (self._see(t.get("victory", "victory.png"), 0.85).found or
                    self._see(t.get("defeat", "defeat.png"), 0.85).found or
                    self._see(t.get("proceed", "proceed.png"), 0.85).found):
                self.log("Match-Ende erkannt.")
                return
            # bewegen: Joystick in zufaellige Richtung ziehen
            ang = random.uniform(0, 6.283)
            dx = int(joy["radius"] * random.uniform(0.6, 1.0) * __import__("math").cos(ang))
            dy = int(joy["radius"] * random.uniform(0.6, 1.0) * __import__("math").sin(ang))
            self.ld.swipe(joy["cx"], joy["cy"], joy["cx"] + dx, joy["cy"] + dy, 400)
            # schiessen: nach vorn tippen
            self.ld.tap(atk["x"], atk["y"])
            time.sleep(0.4)
        self.log("Match-Zeit abgelaufen.")

    def dismiss_popups(self) -> None:
        """Ende-/Belohnungs-/Weiter-Dialoge wegtippen, bis wieder im Menue."""
        t = self.cfg["templates"]
        for _ in range(15):
            tapped = False
            for key in ("proceed", "ok", "continue", "reward", "close"):
                name = t.get(key)
                if name and self._tap_if(name):
                    tapped = True
                    time.sleep(1.2)
                    break
            if not tapped:
                # nichts mehr wegzutippen -> wahrscheinlich im Menue
                if self._see(t["play_button"]).found:
                    return
                # zur Sicherheit Zurueck-Taste
                self.ld.key("KEYCODE_BACK")
                time.sleep(1.0)

    # ---- Account-Wechsel ------------------------------------------------
    def switch_account(self) -> None:
        """
        Fuehrt die in der Config hinterlegte Tap-Sequenz aus, um den Account
        zu wechseln (Einstellungen -> Supercell ID -> anderes Konto laden).
        Da die Menue-Fuehrung versionsabhaengig ist, wird die Sequenz aus
        Templates in cfg['account_switch'] Schritt fuer Schritt abgearbeitet.
        """
        acc = self.cfg.get("accounts", [])
        seq = self.cfg.get("account_switch", {}).get("steps", [])
        if not seq:
            self.log("Kein Account-Wechsel konfiguriert -> uebersprungen.")
            return
        self.account_index = (self.account_index + 1) % max(len(acc), 1)
        self.log(f"Wechsle Account -> Index {self.account_index}.")
        for step in seq:
            tmpl = step["template"]
            if not self._wait_for(tmpl, step.get("timeout", 15)):
                self.log(f"Schritt '{tmpl}' nicht gefunden -> Wechsel abgebrochen.")
                return
            self._tap_if(tmpl)
            time.sleep(step.get("delay", 1.5))
        self.log("Account gewechselt.")

    # ---- Hauptschleife --------------------------------------------------
    def run(self) -> None:
        matches_per_account = self.cfg.get("matches_per_account", 0)  # 0 = nie wechseln
        self.log("Brawl-Bot laeuft. Zum Beenden: Strg+C")
        while True:
            if not self.ready_and_play():
                time.sleep(1.5)
                continue
            if not self.wait_match_start():
                self.log("Match nicht gestartet (Timeout) -> zurueck ins Menue.")
                self.dismiss_popups()
                continue
            self.play_match()
            self.dismiss_popups()
            self.matches_done += 1
            self.log(f"Matches gesamt: {self.matches_done}")
            if matches_per_account and self.matches_done % matches_per_account == 0:
                self.switch_account()
            time.sleep(self.cfg.get("between_matches", 2.0))

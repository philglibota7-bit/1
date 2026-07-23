"""
Aufgaben-Motor: zeitgesteuertes Klicken und synchrone Bewegung pro Instanz.

Eine "Aufgabe" (Task) ist eine wiederkehrende Aktion mit einem Zeitabstand
(interval). Damit deckst du beides ab:
  * Button per Bild automatisch klicken  (type "tap_template")
  * feste Bewegung / fester Klick        (type "swipe" / "tap")

Alle Instanzen einer Gruppe bekommen DIESELBE Aufgabenliste -> sie machen das
Gleiche (gleiche Bewegung, gleiche Klicks). Jede Instanz fuehrt einen eigenen
TaskRunner in einem eigenen Thread aus.

Task-Felder (in der Config bzw. ueber die Oberflaeche):
    { "type": "tap_template", "name": "Play", "template": "play.png",
      "interval": 5, "threshold": 0.85 }
    { "type": "swipe", "name": "vor", "from": [220,780], "to": [220,650],
      "ms": 400, "interval": 1 }
    { "type": "tap", "name": "schuss", "x": 1000, "y": 720, "interval": 1 }
"""

from __future__ import annotations

import threading
import time
from typing import Callable, List, Optional

import vision
from ldplayer import LDPlayer


class Task:
    def __init__(self, d: dict):
        self.type: str = d.get("type", "tap_template")
        self.name: str = d.get("name", self.type)
        self.template: Optional[str] = d.get("template")
        self.threshold: float = float(d.get("threshold", 0.85))
        self.interval: float = float(d.get("interval", 5.0))
        self.x = d.get("x")
        self.y = d.get("y")
        self.frm = d.get("from")
        self.to = d.get("to")
        self.ms = int(d.get("ms", 300))
        self.last = 0.0            # wird pro Instanz gefuehrt

    def to_dict(self) -> dict:
        d = {"type": self.type, "name": self.name, "interval": self.interval}
        if self.type == "tap_template":
            d["template"] = self.template
            d["threshold"] = self.threshold
        elif self.type == "swipe":
            d["from"] = self.frm
            d["to"] = self.to
            d["ms"] = self.ms
        elif self.type == "tap":
            d["x"] = self.x
            d["y"] = self.y
        return d


class TaskRunner:
    def __init__(
        self,
        ld: LDPlayer,
        tasks: List[dict],
        stop_event: threading.Event,
        on_log: Optional[Callable[[str], None]] = None,
        on_status: Optional[Callable[[str], None]] = None,
        dry_run: bool = False,
        loop_delay: float = 1.0,
        tag: str = "",
    ):
        # frische Task-Objekte -> jede Instanz hat eigene Timer
        self.tasks: List[Task] = [Task(t) for t in tasks]
        self.ld = ld
        self.stop_event = stop_event
        self.on_log = on_log
        self.on_status = on_status
        self.dry_run = dry_run
        self.loop_delay = loop_delay
        self.tag = tag
        self.clicks = 0

    def log(self, msg: str) -> None:
        line = f"{self.tag} {msg}".strip()
        (self.on_log or print)(line)

    def status(self, s: str) -> None:
        if self.on_status:
            self.on_status(s)

    def sleep(self, sec: float) -> None:
        self.stop_event.wait(sec)

    def _do(self, t: Task, screen) -> bool:
        """Fuehrt eine Aufgabe aus. True = Aktion wurde ausgefuehrt."""
        if t.type == "tap_template":
            if not t.template:
                return False
            m = vision.find(screen, t.template, t.threshold)
            if not m.found:
                return False
            if not self.dry_run:
                self.ld.tap(m.x, m.y)
            self.log(f"{t.name}: getippt [{m.score:.2f}]"
                     + (" (dry-run)" if self.dry_run else ""))
            self.clicks += 1
            return True
        if t.type == "swipe":
            if not self.dry_run:
                self.ld.swipe(int(t.frm[0]), int(t.frm[1]),
                              int(t.to[0]), int(t.to[1]), t.ms)
            return True
        if t.type == "tap":
            if not self.dry_run:
                self.ld.tap(int(t.x), int(t.y))
            return True
        return False

    def run(self) -> None:
        self.status("RUN")
        self.log("Aufgaben-Motor laeuft" + (" (DRY-RUN)" if self.dry_run else ""))
        while not self.stop_event.is_set():
            try:
                now = time.time()
                # Screenshot nur holen, wenn eine Bild-Aufgabe faellig ist
                need_shot = any(
                    t.type == "tap_template" and now - t.last >= t.interval
                    for t in self.tasks
                )
                screen = self.ld.screenshot() if need_shot else None
                for t in self.tasks:
                    if self.stop_event.is_set():
                        break
                    if now - t.last < t.interval:
                        continue
                    did = self._do(t, screen)
                    # Bild-Aufgabe: Timer nur bei Treffer setzen, sonst weiter
                    # suchen; Bewegung/Tap: Timer immer setzen.
                    if did or t.type != "tap_template":
                        t.last = now
                self.sleep(self.loop_delay)
            except Exception as exc:  # noqa: BLE001
                self.log(f"Fehler: {exc} -> weiter in 3 s.")
                self.sleep(3.0)
        self.status("STOPPED")
        self.log("Aufgaben-Motor gestoppt.")

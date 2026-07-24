"""
Aufgaben-Motor pro Instanz: zeitgesteuertes Klicken + synchrone Bewegung,
mit menschlicherem Verhalten, Auto-Reconnect (Watchdog) und koordiniertem
Account-Wechsel (pausierbar).

Eine "Aufgabe" (Task) ist eine wiederkehrende Aktion mit Zeitabstand (interval):
  * type "tap_template" : Button-Bild alle N s klicken
  * type "swipe"        : Bewegung
  * type "tap"          : feste Position klicken

Menschlicheres Verhalten (cfg["humanize"]):
  * pos_jitter      : zufaellige Pixel-Abweichung beim Klick
  * interval_jitter : zufaellige +/-% Abweichung beim Intervall

Multi-Scale-Erkennung (cfg["detection"]["multi_scale"]): Buttons werden auch
erkannt, wenn die Aufloesung leicht abweicht.

Account-Wechsel: Der Controller ruft request_switch(account, flow) auf. Der
Runner pausiert die normalen Aufgaben, fuehrt den Wechsel-Ablauf aus (jede
Instanz einen ANDEREN Account) und meldet ueber ready_event, sobald er in der
Lobby ist. Der Controller wartet, bis ALLE bereit sind, und ruft dann resume().
"""

from __future__ import annotations

import random
import threading
import time
from typing import Callable, Dict, List, Optional

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
        self.next_due = 0.0


class TaskRunner:
    def __init__(
        self,
        ld: LDPlayer,
        tasks: List[dict],
        cfg: dict,
        stop_event: threading.Event,
        on_log: Optional[Callable[[str], None]] = None,
        on_status: Optional[Callable[[str], None]] = None,
        dry_run: bool = False,
        loop_delay: float = 1.0,
        tag: str = "",
    ):
        self.tasks: List[Task] = [Task(t) for t in tasks]
        self.ld = ld
        self.cfg = cfg
        self.stop_event = stop_event
        self.on_log = on_log
        self.on_status = on_status
        self.dry_run = dry_run
        self.loop_delay = loop_delay
        self.tag = tag
        self.clicks = 0

        self.hum = cfg.get("humanize", {}) or {}
        det = cfg.get("detection", {}) or {}
        self.scales = det.get("scales", [0.9, 0.95, 1.0, 1.05, 1.1]) \
            if det.get("multi_scale") else [1.0]

        # Koordinierte Ablaeufe (Account-Wechsel, Team-Lobby)
        self.pause_event = threading.Event()
        self.ready_event = threading.Event()
        self.job: Optional[dict] = None      # {"kind": "switch"/"create"/"join", ...}
        self.result_code: str = ""           # vom Host gelesener Team-Code

    # ---- Rueckmeldung ---------------------------------------------------
    def log(self, msg: str) -> None:
        (self.on_log or print)(f"{self.tag} {msg}".strip())

    def status(self, s: str) -> None:
        if self.on_status:
            self.on_status(s)

    def sleep(self, sec: float) -> None:
        self.stop_event.wait(sec)

    # ---- menschlicheres Verhalten --------------------------------------
    def _jpos(self, x: int, y: int):
        j = int(self.hum.get("pos_jitter", 0) or 0)
        if j > 0:
            x += random.randint(-j, j)
            y += random.randint(-j, j)
        return int(x), int(y)

    def _jinterval(self, base: float) -> float:
        p = float(self.hum.get("interval_jitter", 0.0) or 0.0)
        return base * (1 + random.uniform(-p, p)) if p > 0 else base

    # ---- Steuerung von aussen (Controller) -----------------------------
    def _request(self, job: dict) -> None:
        self.job = job
        self.ready_event.clear()
        self.pause_event.set()

    def request_switch(self, account: dict, flow: dict) -> None:
        self._request({"kind": "switch", "account": account, "flow": flow or {}})

    def request_create(self, flow: dict) -> None:
        self.result_code = ""
        self._request({"kind": "create", "flow": flow or {}})

    def request_join(self, flow: dict, code: str) -> None:
        self._request({"kind": "join", "flow": flow or {}, "code": code})

    def request_steps(self, steps: list, ready_template: str = "") -> None:
        """Fuehrt eine beliebige Schrittfolge aus (fuer die Zyklus-Automatik)."""
        self._request({"kind": "steps", "steps": steps or [],
                       "ready_template": ready_template})

    def resume(self) -> None:
        self.pause_event.clear()

    def pause(self) -> None:
        self.pause_event.set()

    # ---- Wahrnehmung / Watchdog ----------------------------------------
    def _grab(self):
        try:
            return self.ld.screenshot()
        except Exception:  # noqa: BLE001
            self.log("Verbindung weg – versuche Reconnect ...")
            if self.ld.reconnect():
                self.log("Reconnect ok.")
                return self.ld.screenshot()
            raise

    def _wait_for(self, template: str, timeout: float) -> bool:
        end = time.time() + timeout
        while time.time() < end and not self.stop_event.is_set():
            try:
                if vision.find(self._grab(), template, 0.85, self.scales).found:
                    return True
            except Exception:  # noqa: BLE001
                pass
            self.sleep(0.8)
        return False

    # ---- normale Aufgaben ----------------------------------------------
    def _do(self, t: Task, screen, now: float) -> None:
        if t.type == "tap_template":
            if screen is None:
                screen = self._grab()
            m = vision.find(screen, t.template, t.threshold, self.scales)
            if m.found:
                x, y = self._jpos(m.x, m.y)
                if not self.dry_run:
                    self.ld.tap(x, y)
                self.clicks += 1
                self.log(f"{t.name}: getippt [{m.score:.2f}]"
                         + (" (dry-run)" if self.dry_run else ""))
                t.next_due = now + self._jinterval(t.interval)
            # nicht gefunden -> naechste Runde erneut suchen
        elif t.type == "swipe":
            if not self.dry_run:
                self.ld.swipe(int(t.frm[0]), int(t.frm[1]),
                              int(t.to[0]), int(t.to[1]), t.ms)
            t.next_due = now + self._jinterval(t.interval)
        elif t.type == "tap":
            x, y = self._jpos(int(t.x), int(t.y))
            if not self.dry_run:
                self.ld.tap(x, y)
            t.next_due = now + self._jinterval(t.interval)

    # ---- Account-Wechsel-Ablauf ----------------------------------------
    def _do_step(self, step: dict) -> None:
        typ = step.get("type", "tap_template")
        if typ == "tap_template":
            if self._wait_for(step["template"], step.get("timeout", 15)):
                m = vision.find(self._grab(), step["template"],
                                step.get("threshold", 0.85), self.scales)
                if m.found and not self.dry_run:
                    self.ld.tap(*self._jpos(m.x, m.y))
        elif typ == "tap" and not self.dry_run:
            self.ld.tap(*self._jpos(int(step["x"]), int(step["y"])))
        elif typ == "swipe" and not self.dry_run:
            f, t = step["from"], step["to"]
            self.ld.swipe(int(f[0]), int(f[1]), int(t[0]), int(t[1]),
                          int(step.get("ms", 300)))
        elif typ == "key" and not self.dry_run:
            self.ld.key(step["code"])
        self.sleep(step.get("wait", step.get("delay", 1.2)))

    def _run_switch(self, job: dict) -> None:
        acc = job.get("account") or {}
        flow = job.get("flow") or {}
        self.log(f"Account-Wechsel -> {acc.get('name', '?')}")
        for step in flow.get("open_steps", []):
            if self.stop_event.is_set():
                return
            self._do_step(step)
        # gewuenschten Account auswaehlen (Bild oder feste Position)
        if acc.get("template"):
            if self._wait_for(acc["template"], 15):
                m = vision.find(self._grab(), acc["template"], 0.8, self.scales)
                if m.found and not self.dry_run:
                    self.ld.tap(*self._jpos(m.x, m.y))
        elif acc.get("slot") and not self.dry_run:
            self.ld.tap(int(acc["slot"][0]), int(acc["slot"][1]))
        self.sleep(acc.get("wait", 2.0))
        for step in flow.get("confirm_steps", []):
            if self.stop_event.is_set():
                return
            self._do_step(step)
        lobby = flow.get("lobby_template")
        if lobby:
            ok = self._wait_for(lobby, flow.get("lobby_timeout", 60))
            self.log("In Lobby." if ok else "Lobby-Timeout.")

    # ---- Team-Lobby: Host erstellt + liest Code -------------------------
    def _run_create(self, job: dict) -> None:
        flow = job.get("flow") or {}
        self.log("Erstelle Team-Lobby (Host) ...")
        for step in flow.get("create_steps", []):
            if self.stop_event.is_set():
                return
            self._do_step(step)
        # Team-Code per OCR lesen
        region = flow.get("code_region")
        code = ""
        if region:
            tcmd = self.cfg.get("tesseract_cmd", "")
            for _ in range(6):                       # ein paar Versuche
                if self.stop_event.is_set():
                    break
                code = vision.read_text(self._grab(), region, tcmd)
                code = "".join(ch for ch in code if ch.isalnum()).upper()
                if len(code) >= 3:
                    break
                self.sleep(1.0)
        self.result_code = code
        self.log(f"Team-Code gelesen: '{code or '(leer)'}'")
        rt = flow.get("ready_template")
        if rt:
            self._wait_for(rt, flow.get("ready_timeout", 60))

    # ---- Team-Lobby: Gast tritt per Code bei ---------------------------
    def _run_join(self, job: dict) -> None:
        flow = job.get("flow") or {}
        code = job.get("code", "")
        self.log(f"Trete Lobby bei mit Code '{code}' ...")
        for step in flow.get("join_steps_before", []):
            if self.stop_event.is_set():
                return
            self._do_step(step)
        field = flow.get("code_field")
        if field and not self.dry_run:
            self.ld.tap(int(field[0]), int(field[1]))
            self.sleep(0.6)
        if code and not self.dry_run:
            self.ld.text(code)
            self.sleep(0.6)
        for step in flow.get("join_steps_after", []):
            if self.stop_event.is_set():
                return
            self._do_step(step)
        rt = flow.get("ready_template")
        if rt:
            ok = self._wait_for(rt, flow.get("ready_timeout", 60))
            self.log("In der Lobby." if ok else "Beitritt-Timeout.")

    def _run_steps(self, job: dict) -> None:
        for step in job.get("steps", []):
            if self.stop_event.is_set():
                return
            self._do_step(step)
        rt = job.get("ready_template")
        if rt:
            self._wait_for(rt, 30)

    # ---- Hauptschleife --------------------------------------------------
    def run(self) -> None:
        self.status("RUN")
        self.log("Aufgaben-Motor laeuft" + (" (DRY-RUN)" if self.dry_run else ""))
        while not self.stop_event.is_set():
            try:
                # 1) Koordinierter Job angefordert (switch/create/join)?
                if self.job is not None:
                    job = self.job
                    kind = job.get("kind")
                    self.status(kind.upper() if kind else "JOB")
                    if kind == "switch":
                        self._run_switch(job)
                    elif kind == "create":
                        self._run_create(job)
                    elif kind == "join":
                        self._run_join(job)
                    elif kind == "steps":
                        self._run_steps(job)
                    self.job = None
                    self.ready_event.set()      # dem Controller melden
                    continue
                # 2) pausiert (wartet auf resume des Controllers)?
                if self.pause_event.is_set():
                    self.status("PAUSE")
                    self.sleep(0.4)
                    continue
                # 3) normale Aufgaben
                self.status("RUN")
                now = time.time()
                need_shot = any(t.type == "tap_template" and now >= t.next_due
                                for t in self.tasks)
                screen = self._grab() if need_shot else None
                for t in self.tasks:
                    if self.stop_event.is_set() or self.pause_event.is_set():
                        break
                    if now < t.next_due:
                        continue
                    self._do(t, screen, now)
                self.sleep(self.loop_delay)
            except Exception as exc:  # noqa: BLE001
                self.log(f"Fehler: {exc} -> Watchdog, weiter in 3 s.")
                self.ld.reconnect()
                self.sleep(3.0)
        self.status("STOPPED")
        self.log("Aufgaben-Motor gestoppt.")

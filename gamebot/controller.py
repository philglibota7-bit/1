"""
Steuer-Kern: verwaltet mehrere Bot-Instanzen (Threads) und deren Status.

Wird sowohl von der grafischen Oberflaeche (gui.py) als auch von der Konsole
(multi.py) benutzt, damit die Logik nur an einer Stelle liegt.
"""

from __future__ import annotations

import json
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional

from brawl import BrawlBot
from ldplayer import LDPlayer

HERE = Path(__file__).parent


def load_config(name: str = "config.brawlstars.json") -> dict:
    path = HERE / name
    if not path.exists():
        raise FileNotFoundError(
            f"{path.name} fehlt. Kopiere config.brawlstars.example.json "
            f"nach {path.name} und passe sie an."
        )
    return json.loads(path.read_text(encoding="utf-8"))


@dataclass
class InstanceStatus:
    name: str
    port: int
    running: bool = False
    connected: bool = False
    state: str = "-"
    matches: int = 0
    last_msg: str = ""


class BotController:
    """Startet/stoppt Bot-Threads und haelt deren Live-Status."""

    def __init__(self, cfg: dict, on_log: Optional[Callable[[str], None]] = None):
        self.cfg = cfg
        self.on_log = on_log or (lambda s: print(s))
        self._threads: Dict[int, threading.Thread] = {}
        self._stops: Dict[int, threading.Event] = {}
        self._bots: Dict[int, BrawlBot] = {}
        self.status: Dict[int, InstanceStatus] = {}
        self._lock = threading.Lock()
        for inst in cfg.get("instances", []):
            self.status[inst["port"]] = InstanceStatus(
                name=inst.get("name", str(inst["port"])), port=inst["port"]
            )

    # ---- oeffentliche API ----------------------------------------------
    def instances(self) -> List[dict]:
        return self.cfg.get("instances", [])

    def is_running(self, port: int) -> bool:
        th = self._threads.get(port)
        return bool(th and th.is_alive())

    def any_running(self) -> bool:
        return any(t.is_alive() for t in self._threads.values())

    def start(self, port: int, dry_run: bool = False) -> None:
        if self.is_running(port):
            return
        inst = next((i for i in self.instances() if i["port"] == port), None)
        if inst is None:
            self.on_log(f"Unbekannter Port {port}.")
            return
        stop = threading.Event()
        self._stops[port] = stop
        th = threading.Thread(
            target=self._run_instance, args=(inst, stop, dry_run), daemon=True
        )
        self._threads[port] = th
        th.start()

    def start_all(self, dry_run: bool = False, stagger: float = 1.0) -> None:
        for inst in self.instances():
            self.start(inst["port"], dry_run)
            time.sleep(stagger)   # ADB nicht ueberrennen

    def stop(self, port: int) -> None:
        ev = self._stops.get(port)
        if ev:
            ev.set()

    def stop_all(self) -> None:
        for ev in self._stops.values():
            ev.set()

    def join_all(self, timeout: float = 10.0) -> None:
        end = time.time() + timeout
        for th in self._threads.values():
            th.join(max(0.0, end - time.time()))

    # ---- intern ---------------------------------------------------------
    def _set(self, port: int, **kw) -> None:
        with self._lock:
            st = self.status[port]
            for k, v in kw.items():
                setattr(st, k, v)

    def _run_instance(self, inst: dict, stop: threading.Event, dry_run: bool) -> None:
        port = inst["port"]
        name = inst.get("name", str(port))
        tag = f"[{name}]"
        self._set(port, running=True, connected=False, state="CONNECT")

        ld = LDPlayer(
            host=self.cfg.get("host", "127.0.0.1"),
            port=port,
            adb_path=self.cfg.get("adb_path", "adb"),
        )
        try:
            ld.connect()
            self._set(port, connected=True)
        except Exception as exc:  # noqa: BLE001
            self.on_log(f"{tag} Verbindung fehlgeschlagen: {exc}")
            self._set(port, running=False, state="ERR", last_msg=str(exc))
            return

        def log(msg: str) -> None:
            self._set(port, last_msg=msg.replace(tag, "").strip())
            self.on_log(msg)

        def status(state: str) -> None:
            self._set(port, state=state, matches=bot.matches_done)

        bot = BrawlBot(ld, self.cfg, tag=tag, stop_event=stop,
                       on_status=status, on_log=log, dry_run=dry_run)
        self._bots[port] = bot
        try:
            bot.run()
        finally:
            self._set(port, running=False, state="STOPPED",
                      matches=bot.matches_done)

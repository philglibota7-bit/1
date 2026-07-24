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


def save_config(cfg: dict, name: str = "config.brawlstars.json") -> None:
    path = HERE / name
    path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False),
                    encoding="utf-8")


# ---- Mehrere Config-Profile (configs/<name>.json) ----------------------
CONFIGS_DIR = HERE / "configs"


def configs_dir() -> Path:
    CONFIGS_DIR.mkdir(exist_ok=True)
    return CONFIGS_DIR


def list_configs() -> list:
    return sorted(p.stem for p in configs_dir().glob("*.json"))


def load_named_config(name: str) -> dict:
    return json.loads((configs_dir() / f"{name}.json").read_text(encoding="utf-8"))


def save_named_config(cfg: dict, name: str) -> None:
    (configs_dir() / f"{name}.json").write_text(
        json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")


def ensure_configs() -> list:
    """Sorgt dafuer, dass mindestens ein Profil existiert (Migration)."""
    if not list_configs():
        legacy = HERE / "config.brawlstars.json"
        example = HERE / "config.brawlstars.example.json"
        src = legacy if legacy.exists() else example
        if src.exists():
            save_named_config(json.loads(src.read_text(encoding="utf-8")),
                              "standard")
    return list_configs()


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
        # Status auch fuer Ports anlegen, die nur in Gruppen vorkommen
        for gname, grp in cfg.get("groups", {}).items():
            for port in grp.get("ports", []):
                if port not in self.status:
                    self.status[port] = InstanceStatus(name=f"{gname}:{port}",
                                                       port=port)

    # ---- oeffentliche API ----------------------------------------------
    def instances(self) -> List[dict]:
        return self.cfg.get("instances", [])

    def groups(self) -> dict:
        return self.cfg.get("groups", {})

    def ensure_port(self, port: int, name: Optional[str] = None) -> None:
        """Legt einen Status-Eintrag fuer einen (neu gesetzten) Port an."""
        if port not in self.status:
            self.status[port] = InstanceStatus(name=name or str(port), port=port)

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

    # ---- Gruppen (LOOSE / WIN): synchron dieselben Aufgaben -------------
    def group_ports(self, group_name: str) -> List[int]:
        return self.groups().get(group_name, {}).get("ports", [])

    def group_tasks(self, group_name: str) -> List[dict]:
        return self.groups().get(group_name, {}).setdefault("tasks", [])

    def start_group(self, group_name: str, dry_run: bool = False,
                    stagger: float = 0.5) -> None:
        grp = self.groups().get(group_name)
        if not grp:
            self.on_log(f"Unbekannte Gruppe: {group_name}")
            return
        tasks = grp.get("tasks", [])
        for port in grp.get("ports", []):
            if self.is_running(port):
                continue
            stop = threading.Event()
            self._stops[port] = stop
            th = threading.Thread(
                target=self._run_task_instance,
                args=(port, tasks, stop, dry_run, group_name), daemon=True,
            )
            self._threads[port] = th
            th.start()
            time.sleep(stagger)

    def stop_group(self, group_name: str) -> None:
        for port in self.group_ports(group_name):
            self.stop(port)

    def group_running(self, group_name: str) -> bool:
        return any(self.is_running(p) for p in self.group_ports(group_name))

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

    def _run_task_instance(self, port: int, tasks: List[dict],
                           stop: threading.Event, dry_run: bool,
                           group: str) -> None:
        """Fuehrt fuer eine Instanz die (Gruppen-)Aufgabenliste aus."""
        from tasks import TaskRunner  # lokaler Import: nur wenn Gruppen genutzt

        tag = f"[{group}:{port}]"
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
            self._set(port, state=state, matches=runner.clicks)

        runner = TaskRunner(
            ld, tasks, stop_event=stop, on_log=log, on_status=status,
            dry_run=dry_run, loop_delay=self.cfg.get("loop_delay", 1.0), tag=tag,
        )
        try:
            runner.run()
        finally:
            self._set(port, running=False, state="STOPPED", matches=runner.clicks)

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
from stats import Stats

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
        self._runners: Dict[int, object] = {}   # port -> TaskRunner
        self._cycle_stop = threading.Event()
        self._cycle_thread: Optional[threading.Thread] = None
        self._current_account: Dict[int, str] = {}   # port -> Account-Name
        self.stats = Stats()
        self.cycle_info = {"round": 0, "phase": "-"}
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

    # ---- koordinierter Account-Wechsel ----------------------------------
    def _pick_accounts(self, group_name: str, n: int) -> list:
        """Waehlt n unterschiedliche, noch nicht benutzte Accounts.
        Merkt sich benutzte (used) und setzt zurueck, wenn zu wenige uebrig."""
        grp = self.groups().get(group_name, {})
        accs = grp.get("accounts", [])
        if not accs:
            return []
        unused = [a for a in accs if not a.get("used")]
        if len(unused) < n:
            for a in accs:
                a["used"] = False
            unused = list(accs)
        chosen = unused[:n]
        for a in chosen:
            a["used"] = True
        return chosen

    def reset_accounts(self, group_name: str) -> None:
        for a in self.groups().get(group_name, {}).get("accounts", []):
            a["used"] = False
        self.on_log(f"[{group_name}] Benutzt-Markierungen zurueckgesetzt.")

    def switch_group_accounts(self, group_name: str) -> None:
        """Pausiert die Gruppe, jede Instanz waehlt EINEN anderen Account,
        wartet bis ALLE in der Lobby sind, dann laeuft die Steuerung weiter.
        Blockiert -> aus der Oberflaeche in einem Thread aufrufen."""
        grp = self.groups().get(group_name, {})
        pairs = [(p, self._runners[p]) for p in grp.get("ports", [])
                 if self.is_running(p) and p in self._runners]
        if not pairs:
            self.on_log(f"[{group_name}] Keine laufende Instanz -> Wechsel "
                        f"nicht moeglich (Gruppe zuerst starten).")
            return
        accounts = self._pick_accounts(group_name, len(pairs))
        if not accounts:
            self.on_log(f"[{group_name}] Keine Accounts hinterlegt "
                        f"(im Accounts-Fenster anlegen).")
            return
        runners = [r for _, r in pairs]
        flow = grp.get("switch_flow", {})
        self.on_log(f"[{group_name}] Account-Wechsel gestartet: "
                    f"{[a.get('name') for a in accounts]}")
        for (port, r), acc in zip(pairs, accounts):
            self._current_account[port] = acc.get("name", str(port))
            r.request_switch(acc, flow)
        # warten bis alle in der Lobby sind (oder Timeout)
        timeout = flow.get("all_ready_timeout", 150)
        end = time.time() + timeout
        for r in runners:
            r.ready_event.wait(max(0.0, end - time.time()))
        for r in runners:
            r.resume()
        ready = sum(1 for r in runners if r.ready_event.is_set())
        self.on_log(f"[{group_name}] Wechsel fertig ({ready}/{len(runners)} "
                    f"in Lobby). Steuerung laeuft synchron weiter.")

    # ---- Team-Lobby: Host erstellt, Gaeste treten per Code bei ---------
    def form_team(self, group_name: str) -> bool:
        """Eine Instanz (Host) erstellt eine Lobby, liest den Team-Code (OCR),
        die anderen tippen ihn ein und treten bei. Gibt True bei Erfolg zurueck.
        Blockiert -> aus der Oberflaeche in einem Thread aufrufen."""
        grp = self.groups().get(group_name, {})
        flow = grp.get("team", {})
        if not flow:
            self.on_log(f"[{group_name}] Kein 'team'-Ablauf konfiguriert "
                        f"(in Config bearbeiten anlegen).")
            return False
        ports = [p for p in grp.get("ports", []) if self.is_running(p)]
        ordered = [self._runners.get(p) for p in ports]
        ordered = [r for r in ordered if r]
        if len(ordered) < 2:
            self.on_log(f"[{group_name}] Mindestens 2 laufende Instanzen noetig "
                        f"(1 Host + Gaeste).")
            return False
        host_index = min(int(flow.get("host_index", 0)), len(ordered) - 1)
        host = ordered[host_index]
        guests = [r for i, r in enumerate(ordered) if i != host_index]

        for r in ordered:            # alle pausieren
            r.pause()
        timeout = flow.get("timeout", 120)

        self.on_log(f"[{group_name}] Host erstellt Lobby ...")
        host.request_create(flow)
        host.ready_event.wait(timeout)
        code = host.result_code
        if not code:
            self.on_log(f"[{group_name}] Kein Team-Code gelesen "
                        f"(Tesseract/'code_region' pruefen).")
            for r in ordered:
                r.resume()
            return False
        self.on_log(f"[{group_name}] Team-Code '{code}' -> Gaeste treten bei ...")
        for g in guests:
            g.request_join(flow, code)
        end = time.time() + timeout
        for g in guests:
            g.ready_event.wait(max(0.0, end - time.time()))
        ok = all(g.ready_event.is_set() for g in guests)
        for r in ordered:
            r.resume()
        self.on_log(f"[{group_name}] Team gebildet "
                    f"({'ok' if ok else 'unvollstaendig'}).")
        return ok

    # ---- Vollautomatik: kompletter Zyklus ------------------------------
    def _group_runners(self, group_name: str) -> list:
        ports = [p for p in self.group_ports(group_name) if self.is_running(p)]
        return [self._runners[p] for p in ports if p in self._runners]

    def _host_steps(self, group_name: str, steps: list) -> None:
        runners = self._group_runners(group_name)
        if not runners or not steps:
            return
        hi = min(int(self.groups().get(group_name, {}).get("team", {})
                     .get("host_index", 0)), len(runners) - 1)
        host = runners[hi]
        host.request_steps(steps)
        host.ready_event.wait(60)
        host.resume()

    def _all_steps(self, group_name: str, steps: list) -> None:
        runners = self._group_runners(group_name)
        if not runners or not steps:
            return
        for r in runners:
            r.request_steps(steps)
        for r in runners:
            r.ready_event.wait(60)
        for r in runners:
            r.resume()

    def _wait_match_end(self, group_name: str, template: str,
                        timeout: float, stop) -> None:
        """Wartet, bis der Endscreen erkannt wird (oder Timeout).
        Nutzt den Host, der waehrend des Spielens nebenbei darauf achtet."""
        runners = self._group_runners(group_name)
        if not runners:
            stop.wait(timeout)
            return
        hi = min(int(self.groups().get(group_name, {}).get("team", {})
                     .get("host_index", 0)), len(runners) - 1)
        host = runners[hi]
        host.watch_for(template)
        end = time.time() + timeout
        while not stop.is_set() and time.time() < end:
            if host.watch_event.is_set():
                self.on_log(f"[{group_name}] Endscreen erkannt – Runde vorbei.")
                break
            stop.wait(1.0)
        else:
            if not stop.is_set():
                self.on_log(f"[{group_name}] Kein Endscreen erkannt (Timeout).")
        host.stop_watch()

    def _collect_results(self, group_name: str, cyc: dict, expect_win: bool) -> None:
        """Liest nach dem Match Trophaeen/Sieg pro Instanz und schreibt Stats."""
        region = cyc.get("trophy_region")
        win_tmpl = cyc.get("victory_template", "")
        if not region and not win_tmpl:
            return
        pairs = [(p, self._runners[p]) for p in self.group_ports(group_name)
                 if self.is_running(p) and p in self._runners]
        for _, r in pairs:
            r.request_read(region, win_tmpl)
        for _, r in pairs:
            r.ready_event.wait(30)
        for port, r in pairs:
            name = self._current_account.get(port, f"{group_name}:{port}")
            win = r.result_win if win_tmpl else expect_win
            self.stats.record_game(name, win=win, trophies=r.result_trophies)
            self.on_log(f"[{group_name}] {name}: "
                        f"{'Sieg' if win else 'kein Sieg'}, "
                        f"Trophaeen {r.result_trophies}")
        for _, r in pairs:
            r.resume()

    def _recover(self, group_name: str, cyc: dict) -> None:
        steps = cyc.get("recover_steps") or [
            {"type": "key", "code": "KEYCODE_BACK", "wait": 1.0},
            {"type": "key", "code": "KEYCODE_BACK", "wait": 1.0},
            {"type": "key", "code": "KEYCODE_BACK", "wait": 1.0},
        ]
        self.on_log(f"[{group_name}] Recovery (zurueck ins Menue) ...")
        self._all_steps(group_name, steps)

    def check_setup(self) -> list:
        """Prueft vor dem Start, was noch fehlt (Templates, Ports, Accounts)."""
        problems = []
        tdir = HERE / "templates"

        def need(tmpl):
            if tmpl and not (tdir / tmpl).exists():
                problems.append(f"Template fehlt: templates/{tmpl}")

        for gname, grp in self.groups().items():
            if not grp.get("ports"):
                problems.append(f"Gruppe {gname}: keine Ports gesetzt")
            for t in grp.get("tasks", []):
                if t.get("type") == "tap_template":
                    need(t.get("template"))
            for key in ("switch_flow", "team"):
                flow = grp.get(key, {})
                for lst in ("open_steps", "confirm_steps", "create_steps",
                            "join_steps_before", "join_steps_after"):
                    for st in flow.get(lst, []):
                        if st.get("type") == "tap_template":
                            need(st.get("template"))
        cyc = self.cfg.get("cycle", {})
        for lst in ("start_match_steps", "leave_steps", "recover_steps"):
            for st in cyc.get(lst, []):
                if st.get("type") == "tap_template":
                    need(st.get("template"))
        need(cyc.get("match_end_template"))
        need(cyc.get("victory_template"))
        if cyc.get("match_end_template") and not self.cfg.get("tesseract_cmd"):
            pass  # OCR-Pfad optional (falls im PATH)
        # doppelte entfernen, Reihenfolge egal
        return sorted(set(problems))

    def _set_phase(self, rnd: int, phase: str) -> None:
        self.cycle_info = {"round": rnd, "phase": phase}

    def start_cycle(self) -> None:
        if self._cycle_thread and self._cycle_thread.is_alive():
            return
        self._cycle_stop = threading.Event()
        self._cycle_thread = threading.Thread(target=self._run_cycle, daemon=True)
        self._cycle_thread.start()

    def stop_cycle(self) -> None:
        self._cycle_stop.set()

    def cycle_running(self) -> bool:
        return bool(self._cycle_thread and self._cycle_thread.is_alive())

    def _run_cycle(self) -> None:
        cyc = self.cfg.get("cycle", {})
        win = cyc.get("win_group", "WIN")
        loose = cyc.get("loose_group", "LOOSE")
        loose_delay = float(cyc.get("loose_delay", 35))
        match_dur = float(cyc.get("match_duration", 150))
        rounds = int(cyc.get("rounds", 0))
        do_switch = cyc.get("switch_accounts", True)
        start_steps = cyc.get("start_match_steps", [])
        leave_steps = cyc.get("leave_steps", [])
        retries = int(cyc.get("retries", 2))
        stop = self._cycle_stop
        n = 0
        self.on_log("▶ Vollautomatik gestartet.")
        while not stop.is_set():
            n += 1
            self.on_log(f"═══ Runde {n} ═══")
            # 1) Accounts wechseln (jede Instanz ein anderer, nach Name)
            self._set_phase(n, "Accounts wechseln")
            if do_switch:
                self.switch_group_accounts(win)
                self.switch_group_accounts(loose)
                if stop.is_set():
                    break
            # 2) Beide Teams bilden – mit Pruefung + Wiederholung
            self._set_phase(n, "Teams bilden")
            if not self._form_team_retry(win, retries, stop) or \
               not self._form_team_retry(loose, retries, stop):
                self.on_log("Teambildung fehlgeschlagen -> Recovery, neue Runde.")
                self._recover(win, cyc)
                self._recover(loose, cyc)
                continue
            if stop.is_set():
                break
            # 3) WIN geht in die Runde
            self._set_phase(n, f"{win} startet")
            self.on_log(f"[{win}] startet die Runde.")
            self._host_steps(win, start_steps)
            # 4) LOOSE wartet und geht dann rein
            self._set_phase(n, f"{loose} wartet {loose_delay:.0f}s")
            self.on_log(f"[{loose}] wartet {loose_delay:.0f}s ...")
            stop.wait(loose_delay)
            if stop.is_set():
                break
            self._set_phase(n, f"{loose} startet")
            self.on_log(f"[{loose}] startet die Runde.")
            self._host_steps(loose, start_steps)
            # 5) Spielphase – Ende am Endscreen erkennen
            self._set_phase(n, "Spielphase")
            end_tmpl = cyc.get("match_end_template", "")
            if end_tmpl:
                mt = float(cyc.get("match_timeout", max(match_dur * 2, 300)))
                self.on_log(f"Spielphase – warte auf Endscreen "
                            f"'{end_tmpl}' (max {mt:.0f}s) ...")
                self._wait_match_end(win, end_tmpl, mt, stop)
            else:
                self.on_log(f"Spielphase ~{match_dur:.0f}s ...")
                stop.wait(match_dur)
            if stop.is_set():
                break
            # 6) Ergebnis erfassen (Trophaeen/Sieg) + Team verlassen
            self._set_phase(n, "Ergebnis + verlassen")
            self._collect_results(win, cyc, expect_win=True)
            self._collect_results(loose, cyc, expect_win=False)
            self._all_steps(win, leave_steps)
            self._all_steps(loose, leave_steps)
            self.stats.round_done()
            if rounds and n >= rounds:
                self.on_log(f"Zyklus fertig nach {n} Runden.")
                break
        self._set_phase(0, "-")
        self.on_log("■ Vollautomatik beendet.")

    def _form_team_retry(self, group_name: str, retries: int, stop) -> bool:
        for attempt in range(1, retries + 1):
            if stop.is_set():
                return False
            if self.form_team(group_name):
                return True
            self.on_log(f"[{group_name}] Teambildung Versuch {attempt} "
                        f"fehlgeschlagen.")
            self._recover(group_name, self.cfg.get("cycle", {}))
        return False

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
            ld, tasks, self.cfg, stop_event=stop, on_log=log, on_status=status,
            dry_run=dry_run, loop_delay=self.cfg.get("loop_delay", 1.0), tag=tag,
        )
        self._runners[port] = runner
        try:
            runner.run()
        finally:
            self._runners.pop(port, None)
            self._set(port, running=False, state="STOPPED", matches=runner.clicks)

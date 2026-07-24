"""
Statistik-Speicher: Spiele, Siege und Trophaeen pro Account.

Wird nach jedem Match aktualisiert (Trophaeen/Sieg per Screen-Erkennung, siehe
controller._collect_results). Persistiert in stats.json.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path

HERE = Path(__file__).parent
STATS_FILE = HERE / "stats.json"


class Stats:
    def __init__(self):
        self.lock = threading.Lock()
        self.data = self._load()

    def _load(self) -> dict:
        if STATS_FILE.exists():
            try:
                return json.loads(STATS_FILE.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                pass
        return {"rounds": 0, "accounts": {}}

    def save(self) -> None:
        try:
            STATS_FILE.write_text(
                json.dumps(self.data, indent=2, ensure_ascii=False),
                encoding="utf-8")
        except Exception:  # noqa: BLE001
            pass

    def round_done(self) -> None:
        with self.lock:
            self.data["rounds"] = self.data.get("rounds", 0) + 1
            self.save()

    def _acc(self, name: str) -> dict:
        return self.data.setdefault("accounts", {}).setdefault(
            name, {"games": 0, "wins": 0, "trophies": None, "trophy_gain": 0})

    def record_game(self, name: str, win=None, trophies=None) -> None:
        with self.lock:
            a = self._acc(name)
            a["games"] += 1
            if win:
                a["wins"] += 1
            if trophies is not None:
                if a.get("trophies") is not None:
                    a["trophy_gain"] = a.get("trophy_gain", 0) + \
                        (trophies - a["trophies"])
                a["trophies"] = trophies
            self.save()

    def summary(self) -> str:
        lines = [f"Runden gesamt: {self.data.get('rounds', 0)}", ""]
        accs = self.data.get("accounts", {})
        if not accs:
            lines.append("(noch keine Spieldaten)")
        for name, a in sorted(accs.items()):
            wr = (a["wins"] / a["games"] * 100) if a["games"] else 0
            tro = a.get("trophies")
            lines.append(
                f"{name}:  {a['games']} Spiele · {a['wins']} Siege ({wr:.0f}%) · "
                f"Trophaeen {tro if tro is not None else '?'} "
                f"(Δ {a.get('trophy_gain', 0):+d})")
        return "\n".join(lines)

    def reset(self) -> None:
        with self.lock:
            self.data = {"rounds": 0, "accounts": {}}
            self.save()

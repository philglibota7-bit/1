"""
Chat-"Gehirn" pro Gruppe: versteht Anweisungen in normaler Sprache und lernt.

Funktionsweise (in dieser Reihenfolge):
  1. Gelernte Formulierungen: Wenn du dem Bot etwas beigebracht hast
     (lerne "meine worte" = BEFEHL), wird das zuerst benutzt.
  2. Eingebaute Regeln: viele deutsche Formulierungen werden direkt erkannt
     (starten, stoppen, klicke X alle 5 sekunden, status, ...).
  3. Optionale KI: ist in der Config unter "ai" ein API-Server + Key
     hinterlegt (OpenAI-kompatibel), wird alles Unverstandene an die KI
     geschickt, die es in einen Befehl uebersetzt. Erfolgreiche Uebersetzungen
     werden automatisch gelernt -> beim naechsten Mal ohne KI.

"Lernen" heisst: Zuordnungen von deinen Worten zu Befehlen werden in der
Config gespeichert (groups.<Gruppe>.learned). Mit "Config speichern" bleiben
sie dauerhaft erhalten.

Befehls-Sprache (das, was am Ende ausgefuehrt wird):
    START | STOP | STATUS | HELP
    INTERVAL <sek>                     alle Klick-Intervalle setzen
    CLICK <bild.png> <sek>             Button-Bild alle N s klicken
    TAP <x> <y> <sek>                  feste Position alle N s klicken
    MOVE <x1> <y1> <x2> <y2> <sek>     Bewegung (Swipe)
    REMOVE <name>                      Aufgabe entfernen
"""

from __future__ import annotations

import json
import re
import urllib.request
from typing import Callable, Dict, Optional

HELP_TEXT = (
    "Ich verstehe u. a.:\n"
    "  • 'starte' / 'stopp' – Gruppe starten/stoppen\n"
    "  • 'status' – was gerade eingestellt ist\n"
    "  • 'klicke play alle 5 sekunden' – Button-BILD automatisch klicken\n"
    "  • 'klicke bei 500,700 alle 3 sekunden' – feste POSITION klicken\n"
    "  • 'alle 3 sekunden' – alle Klick-Intervalle setzen\n"
    "  • 'bewege 220,780,220,650 alle 1 sekunde' – Bewegung (von→nach)\n"
    "  • 'entferne play' – Aufgabe loeschen\n"
    "Beibringen:  lerne \"deine worte\" = STARTE\n"
    "Vergessen:   vergiss deine worte"
)


class Brain:
    def __init__(self, cfg: dict, gname: str, actions: Dict[str, Callable]):
        self.cfg = cfg
        self.gname = gname
        self.a = actions
        grp = cfg.setdefault("groups", {}).setdefault(gname, {})
        self.learned: Dict[str, str] = grp.setdefault("learned", {})

    # ---- Haupteinstieg --------------------------------------------------
    def interpret(self, text: str) -> str:
        raw = text.strip()
        if not raw:
            return ""
        low = raw.lower()

        # 1) Lernen / Vergessen
        m = re.match(r"(lerne|merke)\s+(.+?)\s*(=>|=|->)\s*(.+)", raw, re.I)
        if m:
            phrase = m.group(2).strip().strip("\"'").lower()
            cmd = m.group(4).strip()
            self.learned[phrase] = cmd
            self._save()
            return f"Gelernt: '{phrase}' -> {cmd}"
        m = re.match(r"(vergiss|verlerne)\s+(.+)", raw, re.I)
        if m:
            phrase = m.group(2).strip().strip("\"'").lower()
            self.learned.pop(phrase, None)
            self._save()
            return f"Vergessen: '{phrase}'"

        # 2) Gelernte Formulierungen
        for phrase, cmd in self.learned.items():
            if phrase and phrase in low:
                return self._run_canon(cmd)

        # 3) Eingebaute Regeln
        cmd = self._rules_to_canon(low)
        if cmd:
            return self._run_canon(cmd)

        # 4) Optionale KI
        ai_cmd = self._ai_to_canon(raw)
        if ai_cmd:
            self.learned[low] = ai_cmd     # automatisch lernen
            self._save()
            return "🤖 " + self._run_canon(ai_cmd) + f"\n(gelernt: '{low}')"

        return ("Das habe ich nicht verstanden. Tippe 'hilfe' – oder bring es "
                "mir bei:\n  lerne \"deine worte\" = STARTE")

    # ---- Befehle ausfuehren --------------------------------------------
    def _run_canon(self, cmd: str) -> str:
        parts = cmd.strip().split()
        if not parts:
            return "Leerer Befehl."
        op = parts[0].upper()
        try:
            if op in ("START", "STARTE"):
                self.a["start"]()
                return "▶ Gruppe gestartet."
            if op in ("STOP", "STOPP"):
                self.a["stop"]()
                return "■ Gruppe gestoppt."
            if op == "STATUS":
                return self.a["status"]()
            if op in ("HELP", "HILFE"):
                return HELP_TEXT
            if op == "INTERVAL":
                sec = float(parts[1].replace(",", "."))
                self.a["set_interval"](sec)
                return f"Alle Klick-Intervalle auf {sec}s gesetzt."
            if op == "CLICK":
                tmpl = parts[1]
                sec = float(parts[2].replace(",", ".")) if len(parts) > 2 else 5.0
                return self.a["add_click"](tmpl, sec)
            if op == "TAP":
                x, y = int(parts[1]), int(parts[2])
                sec = float(parts[3].replace(",", ".")) if len(parts) > 3 else 2.0
                self.a["add_tap"](x, y, sec)
                return f"👆 Tippt Position {x},{y} alle {sec}s."
            if op == "MOVE":
                nums = [int(p) for p in parts[1:5]]
                sec = float(parts[5].replace(",", ".")) if len(parts) > 5 else 1.0
                self.a["add_move"](nums, sec)
                return "↔ Bewegung hinzugefuegt."
            if op == "REMOVE":
                return self.a["remove"](" ".join(parts[1:]))
        except Exception as exc:  # noqa: BLE001
            return f"Fehler beim Ausfuehren von '{cmd}': {exc}"
        return f"Unbekannter Befehl: {cmd}"

    # ---- Sprache -> Befehl (Regeln) ------------------------------------
    def _rules_to_canon(self, low: str) -> Optional[str]:
        if re.search(r"\b(start\w*|los|leg los|mach an|spiel\w*|beginn\w*)\b", low):
            return "START"
        if re.search(r"\b(stop\w*|halt\w*|anhalten|beende\w*|pause|aus)\b", low):
            return "STOP"
        if re.search(r"\b(status|aufgaben|was machst|was tust)\b", low):
            return "STATUS"
        if re.search(r"\b(hilfe|help|befehle|kommandos)\b", low):
            return "HELP"

        iv = re.search(r"alle\s+([0-9]+(?:[.,][0-9]+)?)\s*(sek\w*|s)\b", low)

        # Bewegung zuerst (4 Zahlen) – vor Positions-Tap (2 Zahlen)
        m = re.search(r"beweg\w*\s+([0-9]+)\s*,\s*([0-9]+)\s*,\s*([0-9]+)\s*,\s*([0-9]+)", low)
        if m:
            sec = iv.group(1) if iv else "1"
            return f"MOVE {m.group(1)} {m.group(2)} {m.group(3)} {m.group(4)} {sec}"

        # feste Position klicken: "klicke bei 500,700" / "tippe auf 500 700"
        m = re.search(r"(klick\w*|dr[uü]ck\w*|tipp\w*|tap\w*)\s+"
                      r"(?:bei|auf|an|pos\w*)?\s*\(?\s*([0-9]{1,4})\s*[,\s]\s*([0-9]{1,4})", low)
        if m:
            sec = iv.group(1) if iv else "2"
            return f"TAP {m.group(2)} {m.group(3)} {sec}"

        # Button-Bild klicken: "klicke play"
        m = re.search(r"(klick\w*|dr[uü]ck\w*|tipp\w*)\s+([a-z0-9_.]+)", low)
        if m:
            tmpl = m.group(2)
            if not tmpl.endswith(".png"):
                tmpl += ".png"
            sec = iv.group(1) if iv else "5"
            return f"CLICK {tmpl} {sec}"

        m = re.search(r"(entfern\w*|l[oö]sch\w*|weg mit)\s+([a-z0-9_.]+)", low)
        if m:
            return f"REMOVE {m.group(2)}"

        if iv:  # nur ein Intervall genannt
            return f"INTERVAL {iv.group(1)}"
        return None

    # ---- Optionale KI ---------------------------------------------------
    def _ai_to_canon(self, text: str) -> Optional[str]:
        ai = self.cfg.get("ai") or {}
        url = ai.get("server_url")
        key = ai.get("api_key")
        if not url or not key:
            return None
        model = ai.get("model", "gpt-4o-mini")
        system = (
            "Du wandelst eine Nutzer-Anweisung in GENAU EINEN Befehl aus dieser "
            "Liste um und antwortest NUR mit dem Befehl, ohne Erklaerung:\n"
            "START | STOP | STATUS | HELP | INTERVAL <sek> | "
            "CLICK <bild.png> <sek> | TAP <x> <y> <sek> | "
            "MOVE <x1> <y1> <x2> <y2> <sek> | REMOVE <name>\n"
            "Wenn nichts passt: NONE"
        )
        try:
            body = json.dumps({
                "model": model,
                "messages": [{"role": "system", "content": system},
                             {"role": "user", "content": text}],
                "max_tokens": 40, "temperature": 0,
            }).encode("utf-8")
            req = urllib.request.Request(
                url.rstrip("/") + "/v1/chat/completions", data=body,
                headers={"Content-Type": "application/json",
                         "Authorization": "Bearer " + key})
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read())
            out = data["choices"][0]["message"]["content"].strip()
            return None if out.upper().startswith("NONE") else out
        except Exception:  # noqa: BLE001
            return None

    def _save(self) -> None:
        try:
            self.a.get("save", lambda: None)()
        except Exception:  # noqa: BLE001
            pass

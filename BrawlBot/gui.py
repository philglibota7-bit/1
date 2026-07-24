"""
BrawlBot – Gruppen-Steuerpult.

Layout: links die Gruppe LOOSE, rechts die Gruppe WIN. Jede Gruppe hat 3 frei
festlegbare Instanzen (Port-Felder + Buttons). Alle Instanzen einer Gruppe
werden GLEICHZEITIG und IDENTISCH gesteuert (dieselben Tasten/Klicks, dieselbe
Bewegung).

Pro Gruppe gibt es:
  * 3 Instanz-Zeilen mit editierbarem Port, Live-Status und "Fenster"-Button
    (Live-Bild, per 2 Klicks Button ausschneiden -> Aufgabe).
  * "Ports uebernehmen" -> schreibt die Ports in die Config.
  * "Gruppe starten / stoppen".
  * "Erklaerung" -> eigenes Fenster: was das Programm macht + Bild-Legende der
    Buttons dieser Gruppe (+ eigene Erklaerbilder hinzufuegbar).
  * Aufgabenliste (zeitgesteuert): Bild einfuegen / Bewegung / entfernen.

Oben: Dry-Run, Config bearbeiten, Config speichern. Unten: Live-Log.

Start:  python gui.py

WICHTIG: Automatisierung von Brawl Stars verstoesst gegen Supercells
Nutzungsbedingungen und fuehrt zu Sperren. Nur mit Wegwerf-Accounts nutzen.
"""

from __future__ import annotations

import base64
import json
import queue
import shutil
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk

import cv2

from brain import Brain
from controller import (BotController, ensure_configs, list_configs,
                        load_config, load_named_config, save_config,
                        save_named_config)
from ldplayer import LDPlayer

HERE = Path(__file__).parent
TEMPLATE_DIR = HERE / "templates"
REFRESH_MS = 500
DISPLAY_W = 460
GROUP_ORDER = ["LOOSE", "WIN"]   # links -> rechts
SLOTS_PER_GROUP = 3


def png_photo(img, width: int) -> tk.PhotoImage:
    """OpenCV-Bild als tk-PhotoImage (ohne Temp-Datei, via base64-PNG)."""
    h, w = img.shape[:2]
    disp = cv2.resize(img, (width, max(1, int(h * width / w))))
    ok, buf = cv2.imencode(".png", disp)
    return tk.PhotoImage(data=base64.b64encode(buf.tobytes()).decode("ascii"))


class InstanceWindow:
    """Live-Bild einer Instanz; per 2 Klicks Button ausschneiden."""

    def __init__(self, app: "BotGUI", port: int, group: str):
        self.app = app
        self.port = port
        self.group = group
        self.screen = None
        self.scale = 1.0
        self.pt1 = None

        self.win = tk.Toplevel(app.root)
        self.win.title(f"Instanz {port}  (Gruppe {group})")
        top = ttk.Frame(self.win, padding=6)
        top.pack(fill="x")
        ttk.Button(top, text="🔄 Aktualisieren", command=self.refresh).pack(side="left")
        ttk.Button(top, text="💾 Screenshot", command=self.save_shot).pack(side="left", padx=4)
        ttk.Label(top, text="  2× klicken = Button ausschneiden").pack(side="left")

        self.canvas = tk.Canvas(self.win, width=DISPLAY_W, height=DISPLAY_W,
                                background="#000", cursor="crosshair")
        self.canvas.pack(padx=6, pady=6)
        self.canvas.bind("<Button-1>", self.on_click)
        self.info = ttk.Label(self.win, text="", padding=6)
        self.info.pack(fill="x")
        self.win.protocol("WM_DELETE_WINDOW", self.close)
        self.refresh()

    def refresh(self) -> None:
        try:
            ld = LDPlayer(host=self.app.cfg.get("host", "127.0.0.1"),
                          port=self.port,
                          adb_path=self.app.cfg.get("adb_path", "adb"))
            ld.connect()
            self.screen = ld.screenshot()
        except Exception as exc:  # noqa: BLE001
            self.info.config(text=f"Kein Bild: {exc}")
            return
        h, w = self.screen.shape[:2]
        self.scale = w / DISPLAY_W
        self.photo = png_photo(self.screen, DISPLAY_W)
        self.canvas.config(height=int(h / self.scale))
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        self.pt1 = None
        self.info.config(text=f"Aufloesung {w}x{h}. Klicke die zwei Ecken des Buttons.")

    def on_click(self, event) -> None:
        if self.screen is None:
            return
        ox, oy = int(event.x * self.scale), int(event.y * self.scale)
        if self.pt1 is None:
            self.pt1 = (ox, oy)
            self.info.config(text=f"Ecke 1 ({ox},{oy}). Jetzt die andere Ecke.")
            self.canvas.create_oval(event.x - 3, event.y - 3, event.x + 3,
                                    event.y + 3, outline="#0f0", width=2)
            return
        x1, y1 = self.pt1
        x2, y2 = ox, oy
        self.pt1 = None
        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))
        if x2 - x1 < 4 or y2 - y1 < 4:
            self.info.config(text="Bereich zu klein - nochmal.")
            return
        crop = self.screen[y1:y2, x1:x2]
        name = simpledialog.askstring("Button speichern",
                                      "Name des Buttons (z. B. play_button):",
                                      parent=self.win)
        if not name:
            return
        if not name.endswith(".png"):
            name += ".png"
        TEMPLATE_DIR.mkdir(exist_ok=True)
        cv2.imwrite(str(TEMPLATE_DIR / name), crop)
        self.info.config(text=f"Gespeichert: templates/{name}")
        if messagebox.askyesno("Als Aufgabe hinzufuegen?",
                               f"'{name}' als automatisch geklickten Button zur "
                               f"Gruppe '{self.group}' hinzufuegen?", parent=self.win):
            iv = simpledialog.askfloat("Intervall", "Alle wie viele Sekunden?",
                                       initialvalue=5.0, parent=self.win)
            self.app.add_task(self.group, {
                "type": "tap_template", "name": name.replace(".png", ""),
                "template": name, "interval": iv or 5.0, "threshold": 0.85})

    def save_shot(self) -> None:
        if self.screen is None:
            return
        path = filedialog.asksaveasfilename(defaultextension=".png",
                                            initialfile=f"shot_{self.port}.png",
                                            filetypes=[("PNG", "*.png")])
        if path:
            cv2.imwrite(path, self.screen)
            self.info.config(text=f"Screenshot gespeichert: {path}")

    def close(self) -> None:
        self.app.inst_windows.pop(self.port, None)
        self.win.destroy()


class GroupHelpWindow:
    """Erklaerung + Bild-Legende der Buttons einer Gruppe."""

    def __init__(self, app: "BotGUI", gname: str):
        self.app = app
        self.gname = gname
        self._imgs = []      # PhotoImage-Referenzen halten

        self.win = tk.Toplevel(app.root)
        self.win.title(f"Erklaerung – Gruppe {gname}")
        self.win.geometry("460x600")

        intro = (
            "Was macht das Programm?\n\n"
            "Es steuert mehrere LDPlayer-Fenster automatisch. Die Instanzen "
            f"der Gruppe '{gname}' werden GLEICHZEITIG und IDENTISCH bedient – "
            "dieselben Buttons werden zur selben Zeit gedrueckt, dieselbe "
            "Bewegung ausgefuehrt.\n\n"
            "Aufgaben sind zeitgesteuert: Ein Button-Bild wird alle X Sekunden "
            "gesucht und – wenn sichtbar – angeklickt.\n\n"
            "Unten die Buttons dieser Gruppe als Bild-Legende:"
        )
        ttk.Label(self.win, text=intro, wraplength=430, justify="left",
                  padding=8).pack(fill="x")

        canvas = tk.Canvas(self.win, borderwidth=0, highlightthickness=0)
        sb = ttk.Scrollbar(self.win, orient="vertical", command=canvas.yview)
        self.legend = ttk.Frame(canvas)
        self.legend.bind("<Configure>",
                         lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.legend, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        sb.pack(side="right", fill="y")

        btns = ttk.Frame(self.win, padding=6)
        btns.pack(fill="x")
        ttk.Button(btns, text="🖼 Erklaerbild hinzufuegen",
                   command=self.add_help_image).pack(side="left")
        ttk.Button(btns, text="Schliessen",
                   command=self.win.destroy).pack(side="right")

        self.render_legend()

    def render_legend(self) -> None:
        for w in self.legend.winfo_children():
            w.destroy()
        self._imgs.clear()
        grp = self.app.controller.groups().get(self.gname, {})

        for t in grp.get("tasks", []):
            row = ttk.Frame(self.legend, padding=4)
            row.pack(fill="x", anchor="w")
            tmpl = t.get("template")
            img = cv2.imread(str(TEMPLATE_DIR / tmpl)) if tmpl else None
            if img is not None:
                photo = png_photo(img, 120)
                self._imgs.append(photo)
                ttk.Label(row, image=photo).pack(side="left")
            txt = f"{t.get('name')}  –  {t.get('type')}, alle {t.get('interval')}s"
            ttk.Label(row, text=txt, wraplength=280, justify="left"
                      ).pack(side="left", padx=8)

        for h in grp.get("help_images", []):
            row = ttk.Frame(self.legend, padding=4)
            row.pack(fill="x", anchor="w")
            img = cv2.imread(str(TEMPLATE_DIR / h.get("image", "")))
            if img is not None:
                photo = png_photo(img, 120)
                self._imgs.append(photo)
                ttk.Label(row, image=photo).pack(side="left")
            ttk.Label(row, text=h.get("caption", ""), wraplength=280,
                      justify="left").pack(side="left", padx=8)

        if not grp.get("tasks") and not grp.get("help_images"):
            ttk.Label(self.legend, text="(noch keine Buttons/Bilder – ueber "
                      "'Bild einfuegen' oder das Instanz-Fenster hinzufuegen.)"
                      ).pack(anchor="w")

    def add_help_image(self) -> None:
        path = filedialog.askopenfilename(
            title="Erklaerbild waehlen",
            filetypes=[("Bilder", "*.png *.jpg *.jpeg *.bmp")])
        if not path:
            return
        TEMPLATE_DIR.mkdir(exist_ok=True)
        dest = TEMPLATE_DIR / Path(path).name
        if Path(path).resolve() != dest.resolve():
            shutil.copy(path, dest)
        cap = simpledialog.askstring("Beschreibung",
                                     "Was zeigt das Bild? (Erklaerung)",
                                     parent=self.win) or ""
        grp = self.app.controller.groups().setdefault(self.gname, {})
        grp.setdefault("help_images", []).append(
            {"image": dest.name, "caption": cap})
        self.render_legend()


class ChatWindow:
    """Chat pro Gruppe: in normaler Sprache steuern; der Bot lernt dazu."""

    def __init__(self, app: "BotGUI", gname: str):
        self.app = app
        self.gname = gname
        self.brain = Brain(app.cfg, gname, app.chat_actions(gname))

        self.win = tk.Toplevel(app.root)
        self.win.title(f"Chat – Gruppe {gname}")
        self.win.geometry("440x520")

        ttk.Label(self.win, padding=6, wraplength=420, justify="left",
                  text=(f"Sag mir, was Gruppe {gname} tun soll (z. B. "
                        "'starte', 'klicke play alle 5 sekunden', 'status'). "
                        "Ich lerne dazu: lerne \"deine worte\" = STARTE")
                  ).pack(fill="x")

        self.log = tk.Text(self.win, wrap="word", state="disabled",
                           background="#0d1117", foreground="#e6e6e6")
        self.log.pack(fill="both", expand=True, padx=6, pady=(0, 6))

        row = ttk.Frame(self.win, padding=6)
        row.pack(fill="x")
        self.entry = ttk.Entry(row)
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", lambda e: self.send())
        ttk.Button(row, text="Senden", command=self.send).pack(side="left", padx=4)

        self._say("Bot", "Bereit. Tippe 'hilfe' fuer Beispiele.")
        self.entry.focus_set()

    def _say(self, who: str, text: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", f"{who}: {text}\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def send(self) -> None:
        msg = self.entry.get().strip()
        if not msg:
            return
        self.entry.delete(0, "end")
        self._say("Du", msg)
        try:
            reply = self.brain.interpret(msg)
        except Exception as exc:  # noqa: BLE001
            reply = f"Fehler: {exc}"
        self._say("Bot", reply or "(nichts)")


class DashboardWindow:
    """Live-Miniaturbilder aller Instanzen auf einen Blick."""

    THUMB_W = 210

    def __init__(self, app: "BotGUI"):
        self.app = app
        self.win = tk.Toplevel(app.root)
        self.win.title("Dashboard – alle Instanzen")
        self.alive = True
        self._photos: dict = {}

        ports = []
        for grp in app.controller.groups().values():
            ports.extend(grp.get("ports", []))
        # doppelte raus, Reihenfolge behalten
        seen = set()
        self.ports = [p for p in ports if not (p in seen or seen.add(p))]

        grid = ttk.Frame(self.win, padding=6)
        grid.pack(fill="both", expand=True)
        self.labels = {}
        cols = 3
        for i, port in enumerate(self.ports):
            cell = ttk.LabelFrame(grid, text=f"Port {port}")
            cell.grid(row=i // cols, column=i % cols, padx=4, pady=4)
            lbl = ttk.Label(cell, text="…", width=28, anchor="center")
            lbl.pack()
            self.labels[port] = lbl

        self.win.protocol("WM_DELETE_WINDOW", self.close)
        threading.Thread(target=self._worker, daemon=True).start()

    def _worker(self) -> None:
        while self.alive:
            for port in self.ports:
                if not self.alive:
                    return
                try:
                    ld = LDPlayer(host=self.app.cfg.get("host", "127.0.0.1"),
                                  port=port,
                                  adb_path=self.app.cfg.get("adb_path", "adb"))
                    ld.connect()
                    img = ld.screenshot()
                    photo = png_photo(img, self.THUMB_W)
                    self.win.after(0, self._set, port, photo)
                except Exception:  # noqa: BLE001
                    self.win.after(0, self._set_text, port, "kein Bild")
            time.sleep(3.0)

    def _set(self, port, photo) -> None:
        if not self.alive:
            return
        self._photos[port] = photo
        lbl = self.labels.get(port)
        if lbl:
            lbl.configure(image=photo, text="")

    def _set_text(self, port, text) -> None:
        lbl = self.labels.get(port)
        if lbl:
            lbl.configure(text=text)

    def close(self) -> None:
        self.alive = False
        self.win.destroy()


class StatsWindow:
    """Statistik/Trophaeen pro Account anzeigen."""

    def __init__(self, app: "BotGUI"):
        self.app = app
        self.win = tk.Toplevel(app.root)
        self.win.title("Statistik – Siege & Trophaeen")
        self.win.geometry("520x420")
        self.text = tk.Text(self.win, wrap="word", state="disabled",
                            font=("Consolas", 11))
        self.text.pack(fill="both", expand=True, padx=6, pady=6)
        row = ttk.Frame(self.win, padding=6)
        row.pack(fill="x")
        ttk.Button(row, text="↻ Aktualisieren", command=self.refresh).pack(side="left")
        ttk.Button(row, text="🗑 Zuruecksetzen", command=self.reset).pack(side="left", padx=6)
        ttk.Button(row, text="Schliessen", command=self.win.destroy).pack(side="right")
        self.refresh()

    def refresh(self) -> None:
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", self.app.controller.stats.summary())
        self.text.configure(state="disabled")

    def reset(self) -> None:
        if messagebox.askyesno("Zuruecksetzen?", "Alle Statistiken loeschen?"):
            self.app.controller.stats.reset()
            self.refresh()


class AccountsWindow:
    """Verwaltung der Account-Liste einer Gruppe (Name + Position 'slot')."""

    def __init__(self, app: "BotGUI", gname: str):
        self.app = app
        self.gname = gname
        grp = app.controller.groups().setdefault(gname, {})
        self.accounts = grp.setdefault("accounts", [])

        self.win = tk.Toplevel(app.root)
        self.win.title(f"Accounts – Gruppe {gname}")
        self.win.geometry("420x460")

        ttk.Label(self.win, padding=6, wraplength=400, justify="left",
                  text=("Hinterlege die Accounts. Jede Instanz waehlt beim "
                        "Wechsel einen ANDEREN (der Bot merkt sich benutzte). "
                        "'Position' = wohin im Konto-Menue getippt wird "
                        "(Koordinate aus dem Instanz-Fenster ablesen).")
                  ).pack(fill="x")

        self.listbox = tk.Listbox(self.win)
        self.listbox.pack(fill="both", expand=True, padx=6, pady=6)

        row = ttk.Frame(self.win, padding=6)
        row.pack(fill="x")
        ttk.Button(row, text="＋ Account", command=self.add).pack(side="left")
        ttk.Button(row, text="🗑 Entfernen", command=self.remove).pack(side="left", padx=4)
        ttk.Button(row, text="↺ Benutzt zuruecksetzen",
                   command=self.reset).pack(side="left")
        ttk.Button(row, text="💾 Speichern",
                   command=self.app.save).pack(side="right")

        self.refresh()

    def refresh(self) -> None:
        self.listbox.delete(0, "end")
        for a in self.accounts:
            used = "  ✓benutzt" if a.get("used") else ""
            pos = a.get("slot") or a.get("template") or "-"
            self.listbox.insert("end", f"{a.get('name', '?')}  @ {pos}{used}")

    def add(self) -> None:
        name = simpledialog.askstring("Account", "Account-Name:", parent=self.win)
        if not name:
            return
        s = simpledialog.askstring(
            "Position", "Position im Konto-Menue x,y (z. B. 640,300):",
            parent=self.win)
        acc = {"name": name, "used": False}
        if s:
            try:
                x, y = [int(v.strip()) for v in s.split(",")]
                acc["slot"] = [x, y]
            except Exception:  # noqa: BLE001
                messagebox.showerror("Ungueltig", "Format: x,y")
                return
        self.accounts.append(acc)
        self.refresh()

    def remove(self) -> None:
        sel = self.listbox.curselection()
        if sel and 0 <= sel[0] < len(self.accounts):
            self.accounts.pop(sel[0])
            self.refresh()

    def reset(self) -> None:
        self.app.controller.reset_accounts(self.gname)
        self.refresh()


class ConfigEditor:
    """Fenster zum Bearbeiten und Speichern der kompletten Config (JSON)."""

    def __init__(self, app: "BotGUI"):
        self.app = app
        self.win = tk.Toplevel(app.root)
        self.win.title("Config bearbeiten – config.brawlstars.json")
        self.win.geometry("640x600")
        ttk.Label(self.win, text="Konfiguration (JSON). Aendern und speichern:",
                  padding=6).pack(fill="x")
        self.text = tk.Text(self.win, wrap="none", undo=True, font=("Consolas", 10))
        self.text.pack(fill="both", expand=True, padx=6, pady=6)
        self.status = ttk.Label(self.win, text="", padding=6, foreground="#080")
        self.status.pack(fill="x")
        btns = ttk.Frame(self.win, padding=6)
        btns.pack(fill="x")
        ttk.Button(btns, text="💾 Speichern", command=self.save).pack(side="left")
        ttk.Button(btns, text="↻ Neu laden", command=self.reload).pack(side="left", padx=6)
        ttk.Button(btns, text="Schliessen", command=self.win.destroy).pack(side="right")
        self.reload()

    def reload(self) -> None:
        self.text.delete("1.0", "end")
        self.text.insert("1.0", json.dumps(self.app.cfg, indent=2, ensure_ascii=False))
        self.status.config(text="Aktuelle Config geladen.", foreground="#080")

    def save(self) -> None:
        try:
            new_cfg = json.loads(self.text.get("1.0", "end"))
        except json.JSONDecodeError as exc:
            self.status.config(text=f"❌ JSON-Fehler (Zeile {exc.lineno}): {exc.msg}",
                               foreground="#b00")
            return
        self.app.cfg.clear()
        self.app.cfg.update(new_cfg)
        try:
            save_named_config(self.app.cfg, self.app.config_name)
        except Exception as exc:  # noqa: BLE001
            self.status.config(text=f"❌ Speichern fehlgeschlagen: {exc}",
                               foreground="#b00")
            return
        self.status.config(text=f"✅ Profil '{self.app.config_name}' gespeichert. "
                                "Ports/Gruppen wirken nach Neustart.",
                           foreground="#080")
        self.app.render_groups()


class BotGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("BrawlBot – Gruppen-Steuerpult")
        root.geometry("1040x680")
        self.log_queue: "queue.Queue[str]" = queue.Queue()
        self.inst_windows: dict[int, InstanceWindow] = {}

        names = ensure_configs()
        if not names:
            messagebox.showerror("Konfiguration fehlt",
                                 "Keine Config gefunden. Lege configs/standard.json "
                                 "an oder nutze config.brawlstars.example.json.")
            root.destroy()
            return
        self.config_name = names[0]
        try:
            self.cfg = load_named_config(self.config_name)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Konfiguration fehlt", str(exc))
            root.destroy()
            return

        self.controller = BotController(self.cfg, on_log=self.log_queue.put)
        self.dry_run = tk.BooleanVar(value=False)
        self.group_widgets: dict[str, dict] = {}

        self._build_header()
        self.groups_wrap = ttk.Frame(self.root, padding=8)
        self.groups_wrap.pack(fill="both", expand=False)
        self.render_groups()
        self._build_log()

        root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._refresh()

    # ---- Kopf -----------------------------------------------------------
    def _build_header(self) -> None:
        # Zeile 1: Profile
        bar = ttk.Frame(self.root, padding=(8, 8, 8, 2))
        bar.pack(fill="x")
        ttk.Label(bar, text="Profil:").pack(side="left")
        self.config_var = tk.StringVar(value=self.config_name)
        self.config_combo = ttk.Combobox(bar, textvariable=self.config_var,
                                         values=list_configs(), width=18,
                                         state="readonly")
        self.config_combo.pack(side="left", padx=4)
        self.config_combo.bind("<<ComboboxSelected>>",
                               lambda e: self.switch_config(self.config_var.get()))
        ttk.Button(bar, text="＋ Neu", command=self.new_config).pack(side="left")
        ttk.Button(bar, text="✎ Umbenennen",
                   command=self.rename_config).pack(side="left", padx=4)
        ttk.Button(bar, text="🗑 Loeschen",
                   command=self.delete_config).pack(side="left")
        ttk.Button(bar, text="💾 Profil speichern",
                   command=self.save).pack(side="right")
        ttk.Button(bar, text="⚙ Config bearbeiten",
                   command=lambda: ConfigEditor(self)).pack(side="right", padx=6)

        # Zeile 2: globale Steuerung
        bar2 = ttk.Frame(self.root, padding=(8, 2, 8, 6))
        bar2.pack(fill="x")
        ttk.Button(bar2, text="▶▶ Alle Gruppen starten",
                   command=self.start_all_groups).pack(side="left")
        ttk.Button(bar2, text="■ NOT-AUS (alles stoppen)",
                   command=self.stop_all).pack(side="left", padx=6)
        ttk.Button(bar2, text="🔍 Ports scannen",
                   command=self.scan_ports).pack(side="left")
        ttk.Checkbutton(bar2, text="Dry-Run (nur testen)",
                        variable=self.dry_run).pack(side="left", padx=(12, 0))
        ttk.Button(bar2, text="🖥 Dashboard",
                   command=self.open_dashboard).pack(side="left", padx=(12, 0))
        ttk.Button(bar2, text="📊 Statistik",
                   command=lambda: StatsWindow(self)).pack(side="left", padx=4)
        ttk.Button(bar2, text="■ Stop Automatik",
                   command=self.stop_cycle).pack(side="right")
        ttk.Button(bar2, text="🔁 Vollautomatik (Zyklus)",
                   command=self.start_cycle).pack(side="right", padx=6)

        # Zeile 3: Zyklus-Status
        bar3 = ttk.Frame(self.root, padding=(8, 0, 8, 4))
        bar3.pack(fill="x")
        self.cycle_status = tk.StringVar(value="Zyklus: gestoppt")
        ttk.Label(bar3, textvariable=self.cycle_status,
                  foreground="#06c").pack(side="left")
        ttk.Label(self.root, foreground="#b00", padding=(8, 0),
                  text="⚠ Brawl-Stars-Botting verstoesst gegen Supercells "
                       "Nutzungsbedingungen – nur Wegwerf-Accounts, Sperr-Risiko!"
                  ).pack(fill="x")

    # ---- Gruppen (LOOSE links, WIN rechts) ------------------------------
    def ordered_groups(self) -> list[str]:
        gs = list(self.controller.groups().keys())
        return [g for g in GROUP_ORDER if g in gs] + \
               [g for g in gs if g not in GROUP_ORDER]

    def render_groups(self) -> None:
        for w in self.groups_wrap.winfo_children():
            w.destroy()
        self.group_widgets.clear()
        if not self.controller.groups():
            ttk.Label(self.groups_wrap,
                      text="Keine 'groups' in der Config. Ueber 'Config "
                           "bearbeiten' anlegen.").pack()
            return
        for gname in self.ordered_groups():
            self._build_group_panel(gname)

    def _build_group_panel(self, gname: str) -> None:
        box = ttk.LabelFrame(self.groups_wrap, text=f"Gruppe {gname}", padding=8)
        box.pack(side="left", fill="both", expand=True, padx=6)

        grp = self.controller.groups().get(gname, {})
        ports = list(grp.get("ports", []))
        while len(ports) < SLOTS_PER_GROUP:
            ports.append("")

        rows = []
        for i in range(SLOTS_PER_GROUP):
            row = ttk.Frame(box)
            row.pack(fill="x", pady=1)
            ttk.Label(row, text=f"Instanz {i + 1}  Port:").pack(side="left")
            ent = ttk.Entry(row, width=7)
            if ports[i] != "":
                ent.insert(0, str(ports[i]))
            ent.pack(side="left", padx=4)
            status = ttk.Label(row, width=22, anchor="w", text="-")
            status.pack(side="left")
            ttk.Button(row, text="Fenster",
                       command=lambda idx=i, g=gname: self.open_instance_slot(g, idx)
                       ).pack(side="right")
            rows.append({"entry": ent, "status": status})

        top = ttk.Frame(box)
        top.pack(fill="x", pady=(6, 2))
        ttk.Button(top, text="✔ Ports uebernehmen",
                   command=lambda g=gname: self.apply_ports(g)).pack(side="left")
        ttk.Button(top, text="❔ Erklaerung",
                   command=lambda g=gname: GroupHelpWindow(self, g)).pack(side="left", padx=4)
        ttk.Button(top, text="💬 Chat",
                   command=lambda g=gname: ChatWindow(self, g)).pack(side="left")

        ctrl = ttk.Frame(box)
        ctrl.pack(fill="x", pady=(2, 2))
        ttk.Button(ctrl, text="▶ Gruppe starten",
                   command=lambda g=gname: self.start_group(g)).pack(side="left")
        ttk.Button(ctrl, text="■ Gruppe stoppen",
                   command=lambda g=gname: self.controller.stop_group(g)
                   ).pack(side="left", padx=6)

        accrow = ttk.Frame(box)
        accrow.pack(fill="x", pady=(0, 4))
        ttk.Button(accrow, text="👥 Accounts",
                   command=lambda g=gname: AccountsWindow(self, g)).pack(side="left")
        ttk.Button(accrow, text="🔀 Accounts wechseln",
                   command=lambda g=gname: self.switch_accounts(g)).pack(side="left", padx=4)
        ttk.Button(accrow, text="🏁 Team-Lobby",
                   command=lambda g=gname: self.form_team(g)).pack(side="left")

        ttk.Label(box, text="Aufgaben (zeitgesteuert · Doppelklick = bearbeiten):"
                  ).pack(anchor="w")
        listbox = tk.Listbox(box, height=7)
        listbox.pack(fill="both", expand=True)
        listbox.bind("<Double-Button-1>",
                     lambda e, g=gname: self.edit_task(g))
        tb = ttk.Frame(box)
        tb.pack(fill="x", pady=4)
        ttk.Button(tb, text="🖼 Bild einfuegen",
                   command=lambda g=gname: self.add_image_task(g)).pack(side="left")
        ttk.Button(tb, text="↔ Bewegung",
                   command=lambda g=gname: self.add_move_task(g)).pack(side="left", padx=4)
        ttk.Button(tb, text="🗑 Entfernen",
                   command=lambda g=gname: self.remove_task(g)).pack(side="left")
        kind = "loose" if "LOOSE" in gname.upper() else "win"
        ttk.Button(tb, text=f"🎮 Verhalten ({kind})",
                   command=lambda g=gname, k=kind: self.apply_preset(g, k)
                   ).pack(side="left", padx=4)

        self.group_widgets[gname] = {"rows": rows, "list": listbox}
        self._refresh_task_list(gname)

    # ---- Ports / Instanzen ---------------------------------------------
    def apply_ports(self, gname: str) -> None:
        rows = self.group_widgets[gname]["rows"]
        ports = []
        for r in rows:
            val = r["entry"].get().strip()
            if not val:
                continue
            try:
                p = int(val)
            except ValueError:
                messagebox.showerror("Ungueltig", f"'{val}' ist keine Portnummer.")
                return
            ports.append(p)
            self.controller.ensure_port(p, name=f"{gname}:{p}")
        self.controller.groups().setdefault(gname, {})["ports"] = ports
        self.log_queue.put(f"[{gname}] Ports gesetzt: {ports}")
        messagebox.showinfo("Uebernommen",
                            f"Gruppe {gname}: Ports {ports}.\nMit 'Config "
                            f"speichern' dauerhaft sichern.")

    def open_instance_slot(self, gname: str, idx: int) -> None:
        rows = self.group_widgets[gname]["rows"]
        val = rows[idx]["entry"].get().strip()
        if not val:
            messagebox.showinfo("Kein Port", "Bitte zuerst einen Port eintragen.")
            return
        try:
            port = int(val)
        except ValueError:
            messagebox.showerror("Ungueltig", f"'{val}' ist keine Portnummer.")
            return
        self.controller.ensure_port(port, name=f"{gname}:{port}")
        if port in self.inst_windows:
            self.inst_windows[port].win.lift()
            return
        self.inst_windows[port] = InstanceWindow(self, port, gname)

    # ---- Gruppe / Aufgaben ---------------------------------------------
    def start_group(self, gname: str) -> None:
        self.controller.start_group(gname, dry_run=self.dry_run.get())

    def switch_accounts(self, gname: str) -> None:
        if not self.controller.group_running(gname):
            messagebox.showinfo("Nicht gestartet",
                                f"Starte Gruppe {gname} zuerst – der Wechsel "
                                f"pausiert die laufende Steuerung.")
            return
        threading.Thread(target=self.controller.switch_group_accounts,
                         args=(gname,), daemon=True).start()

    def form_team(self, gname: str) -> None:
        if not self.controller.group_running(gname):
            messagebox.showinfo("Nicht gestartet",
                                f"Starte Gruppe {gname} zuerst (mind. 2 "
                                f"Instanzen: 1 Host + Gaeste).")
            return
        threading.Thread(target=self.controller.form_team,
                         args=(gname,), daemon=True).start()

    def add_task(self, gname: str, task: dict) -> None:
        self.controller.group_tasks(gname).append(task)
        self._refresh_task_list(gname)
        self.log_queue.put(f"[{gname}] Aufgabe hinzugefuegt: {task.get('name')}")

    def add_image_task(self, gname: str) -> None:
        path = filedialog.askopenfilename(
            title="Button-Bild waehlen",
            filetypes=[("Bilder", "*.png *.jpg *.jpeg *.bmp")])
        if not path:
            return
        TEMPLATE_DIR.mkdir(exist_ok=True)
        dest = TEMPLATE_DIR / Path(path).name
        if Path(path).resolve() != dest.resolve():
            shutil.copy(path, dest)
        iv = simpledialog.askfloat("Intervall", "Alle wie viele Sekunden klicken?",
                                   initialvalue=5.0, parent=self.root)
        self.add_task(gname, {"type": "tap_template", "name": dest.stem,
                              "template": dest.name, "interval": iv or 5.0,
                              "threshold": 0.85})

    def add_move_task(self, gname: str) -> None:
        s = simpledialog.askstring(
            "Bewegung", "von_x,von_y,nach_x,nach_y  (z. B. 220,780,220,650):",
            parent=self.root)
        if not s:
            return
        try:
            a, b, c, d = [int(v.strip()) for v in s.split(",")]
        except Exception:  # noqa: BLE001
            messagebox.showerror("Ungueltig", "Format: von_x,von_y,nach_x,nach_y")
            return
        iv = simpledialog.askfloat("Intervall", "Alle wie viele Sekunden?",
                                   initialvalue=1.0, parent=self.root)
        self.add_task(gname, {"type": "swipe", "name": "bewegung",
                              "from": [a, b], "to": [c, d], "ms": 400,
                              "interval": iv or 1.0})

    def remove_task(self, gname: str) -> None:
        lb = self.group_widgets[gname]["list"]
        sel = lb.curselection()
        if not sel:
            return
        tasks = self.controller.group_tasks(gname)
        idx = sel[0]
        if 0 <= idx < len(tasks):
            removed = tasks.pop(idx)
            self._refresh_task_list(gname)
            self.log_queue.put(f"[{gname}] Aufgabe entfernt: {removed.get('name')}")

    def edit_task(self, gname: str) -> None:
        lb = self.group_widgets[gname]["list"]
        sel = lb.curselection()
        if not sel:
            return
        tasks = self.controller.group_tasks(gname)
        idx = sel[0]
        if not (0 <= idx < len(tasks)):
            return
        t = tasks[idx]
        iv = simpledialog.askfloat("Intervall",
                                   f"Intervall (Sekunden) fuer '{t.get('name')}':",
                                   initialvalue=float(t.get("interval", 5.0)),
                                   parent=self.root)
        if iv is not None:
            t["interval"] = iv
        if t.get("type") == "tap_template":
            th = simpledialog.askfloat("Erkennung",
                                       "Erkennungs-Schwelle (0.5–1.0):",
                                       initialvalue=float(t.get("threshold", 0.85)),
                                       parent=self.root)
            if th is not None:
                t["threshold"] = th
        self._refresh_task_list(gname)

    def save(self) -> None:
        try:
            save_named_config(self.cfg, self.config_name)
            messagebox.showinfo("Gespeichert",
                                f"Profil '{self.config_name}' gespeichert.")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Fehler", str(exc))

    # ---- Profile (mehrere Configs) -------------------------------------
    def switch_config(self, name: str) -> None:
        if name == self.config_name:
            return
        if self.controller.any_running():
            if not messagebox.askyesno("Profil wechseln?",
                                       "Es laufen noch Instanzen. Stoppen und "
                                       "Profil wechseln?"):
                self.config_var.set(self.config_name)
                return
            self.controller.stop_all()
            self.controller.join_all(timeout=8)
        # offene Instanz-Fenster schliessen
        for w in list(self.inst_windows.values()):
            try:
                w.win.destroy()
            except Exception:  # noqa: BLE001
                pass
        self.inst_windows.clear()
        try:
            self.cfg = load_named_config(name)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Fehler", f"Profil '{name}' laedt nicht: {exc}")
            self.config_var.set(self.config_name)
            return
        self.config_name = name
        self.config_var.set(name)
        self.controller = BotController(self.cfg, on_log=self.log_queue.put)
        self.render_groups()
        self.log_queue.put(f"Profil gewechselt: {name}")

    def new_config(self) -> None:
        name = simpledialog.askstring("Neues Profil",
                                      "Name des neuen Profils (z. B. config2):",
                                      parent=self.root)
        if not name:
            return
        name = name.strip().replace(" ", "_")
        if name in list_configs():
            messagebox.showerror("Vorhanden", f"Profil '{name}' gibt es schon.")
            return
        base = "leeres Profil" if not messagebox.askyesno(
            "Kopieren?", "Aktuelles Profil als Vorlage kopieren?\n"
            "(Nein = leeres Profil mit denselben Gruppen)") else None
        if base is None:
            new_cfg = json.loads(json.dumps(self.cfg))   # tiefe Kopie
        else:
            new_cfg = json.loads(json.dumps(self.cfg))
            for g in new_cfg.get("groups", {}).values():
                g["tasks"] = []
                g["learned"] = {}
        save_named_config(new_cfg, name)
        self.config_combo["values"] = list_configs()
        self.switch_config(name)

    def delete_config(self) -> None:
        names = list_configs()
        if len(names) <= 1:
            messagebox.showinfo("Nicht moeglich",
                                "Es muss mindestens ein Profil geben.")
            return
        if not messagebox.askyesno("Loeschen?",
                                   f"Profil '{self.config_name}' wirklich loeschen?"):
            return
        if self.controller.any_running():
            self.controller.stop_all()
            self.controller.join_all(timeout=8)
        from controller import configs_dir
        (configs_dir() / f"{self.config_name}.json").unlink(missing_ok=True)
        remaining = list_configs()
        self.config_combo["values"] = remaining
        self.config_name = ""            # Wechsel erzwingen
        self.switch_config(remaining[0])

    # ---- globale Steuerung ---------------------------------------------
    def start_all_groups(self) -> None:
        for g in self.controller.groups():
            self.start_group(g)

    def stop_all(self) -> None:
        self.controller.stop_all()
        self.log_queue.put("NOT-AUS: alle Instanzen gestoppt.")

    def open_dashboard(self) -> None:
        DashboardWindow(self)

    def start_cycle(self) -> None:
        if self.controller.cycle_running():
            messagebox.showinfo("Laeuft", "Die Vollautomatik laeuft bereits.")
            return
        problems = self.controller.check_setup()
        if problems:
            msg = ("Setup-Check hat Probleme gefunden:\n\n"
                   + "\n".join("• " + p for p in problems[:15]))
            if len(problems) > 15:
                msg += f"\n… und {len(problems) - 15} weitere."
            msg += "\n\nTrotzdem starten?"
            if not messagebox.askyesno("Setup-Check", msg):
                return
        if not messagebox.askyesno(
            "Vollautomatik starten?",
            "Startet beide Gruppen und den kompletten Zyklus (Accounts wechseln "
            "→ Teams bilden → WIN spielt, LOOSE wirft → Team verlassen → wieder "
            "von vorn).\n\nNur mit Wegwerf-Accounts! Fortfahren?"):
            return
        for g in self.controller.groups():
            self.controller.start_group(g, dry_run=self.dry_run.get())
        self.controller.start_cycle()

    def stop_cycle(self) -> None:
        self.controller.stop_cycle()

    def scan_ports(self) -> None:
        self.log_queue.put("🔍 Suche laufende LDPlayer-Instanzen ...")
        threading.Thread(target=self._scan_worker, daemon=True).start()

    def _scan_worker(self) -> None:
        start = int(self.cfg.get("scan_start", 5555))
        found = []
        for i in range(16):
            port = start + i * 2
            try:
                ld = LDPlayer(host=self.cfg.get("host", "127.0.0.1"), port=port,
                              adb_path=self.cfg.get("adb_path", "adb"))
                ld.connect()
                found.append(port)
                self.log_queue.put(f"  ✓ Instanz auf Port {port}")
            except Exception:  # noqa: BLE001
                pass
        self.log_queue.put(f"🔍 Scan fertig. Gefunden: {found or 'keine'}")

    def rename_config(self) -> None:
        new = simpledialog.askstring("Profil umbenennen",
                                     f"Neuer Name fuer '{self.config_name}':",
                                     parent=self.root)
        if not new:
            return
        new = new.strip().replace(" ", "_")
        if new in list_configs():
            messagebox.showerror("Vorhanden", f"Profil '{new}' gibt es schon.")
            return
        from controller import configs_dir
        old_path = configs_dir() / f"{self.config_name}.json"
        save_named_config(self.cfg, new)
        try:
            old_path.unlink(missing_ok=True)
        except Exception:  # noqa: BLE001
            pass
        self.config_name = new
        self.config_combo["values"] = list_configs()
        self.config_var.set(new)
        self.log_queue.put(f"Profil umbenannt zu: {new}")

    # ---- Chat-Aktionen (vom Brain aufgerufen) --------------------------
    def chat_actions(self, gname: str) -> dict:
        return {
            "start": lambda: self.start_group(gname),
            "stop": lambda: self.controller.stop_group(gname),
            "status": lambda: self._chat_status(gname),
            "set_interval": lambda sec: self._chat_set_interval(gname, sec),
            "add_click": lambda tmpl, sec: self._chat_add_click(gname, tmpl, sec),
            "add_tap": lambda x, y, sec, w=0, h=0: self._chat_add_tap(
                gname, x, y, sec, w, h),
            "add_image": lambda: self.add_image_task(gname),
            "add_move": lambda nums, sec: self._chat_add_move(gname, nums, sec),
            "remove": lambda name: self._chat_remove(gname, name),
            "capture": lambda: self._chat_capture(gname),
            "switch": lambda: self.switch_accounts(gname),
            "team": lambda: self.form_team(gname),
            "preset": lambda kind: self.apply_preset(gname, kind),
            "save": lambda: save_config(self.cfg),
        }

    def _detect_resolution(self):
        """Aufloesung einer erreichbaren Instanz ermitteln (Fallback 1280x720)."""
        for grp in self.controller.groups().values():
            for p in grp.get("ports", []):
                try:
                    ld = LDPlayer(host=self.cfg.get("host", "127.0.0.1"), port=p,
                                  adb_path=self.cfg.get("adb_path", "adb"))
                    ld.connect()
                    img = ld.screenshot()
                    return img.shape[1], img.shape[0]
                except Exception:  # noqa: BLE001
                    continue
        return 1280, 720

    def _controls_px(self):
        """Liefert Joystick/Angriff in Pixeln – aus relativen 'controls'
        (auflösungs-unabhaengig) oder absoluten Werten als Fallback."""
        frac = self.cfg.get("controls")
        if frac:
            w, h = self._detect_resolution()
            j, a = frac.get("joystick", {}), frac.get("attack", {})
            joy = {"cx": int(j.get("cx", 0.16) * w),
                   "cy": int(j.get("cy", 0.78) * h),
                   "radius": int(j.get("radius", 0.13) * h)}
            atk = {"x": int(a.get("x", 0.88) * w), "y": int(a.get("y", 0.80) * h)}
            return joy, atk
        joy = self.cfg.get("joystick") or {"cx": 205, "cy": 560, "radius": 95}
        atk = self.cfg.get("attack") or {"x": 1120, "y": 575}
        return joy, atk

    def apply_preset(self, gname: str, kind: str) -> None:
        """Fuellt die Aufgaben der Gruppe mit fertigem Spiel-Verhalten.
        win = bewegen + schiessen, loose = nur bewegen. Koordinaten werden
        automatisch aus der Aufloesung berechnet."""
        joy, atk = self._controls_px()
        self.cfg["joystick"] = joy       # damit auch Chat-Bewegung/Schuss passt
        self.cfg["attack"] = atk
        cx, cy, r = joy["cx"], joy["cy"], joy["radius"]
        tasks = [
            {"type": "swipe", "name": "vor", "from": [cx, cy],
             "to": [cx, cy - r], "ms": 400, "interval": 1},
            {"type": "swipe", "name": "zurueck", "from": [cx, cy],
             "to": [cx, cy + r], "ms": 400, "interval": 2},
        ]
        if kind == "win":
            tasks.append({"type": "tap", "name": "schuss",
                          "x": atk["x"], "y": atk["y"], "interval": 1,
                          "w": 30, "h": 30})
        self.controller.group_tasks(gname)[:] = tasks
        self._refresh_task_list(gname)
        self.log_queue.put(f"[{gname}] Verhalten '{kind}' gesetzt "
                           f"({len(tasks)} Aufgaben).")

    def _chat_capture(self, gname: str) -> None:
        ports = self.controller.group_ports(gname)
        if ports:
            self.root.after(0, lambda: self.open_instance_slot(gname, 0))

    def _chat_status(self, gname: str) -> str:
        running = self.controller.group_running(gname)
        tasks = self.controller.group_tasks(gname)
        lines = [f"Gruppe {gname}: {'laeuft' if running else 'gestoppt'}, "
                 f"{len(tasks)} Aufgabe(n):"]
        for t in tasks:
            lines.append(f"  • {t.get('name')} ({t.get('type')}, "
                         f"alle {t.get('interval')}s)")
        return "\n".join(lines)

    def _chat_set_interval(self, gname: str, sec: float) -> None:
        for t in self.controller.group_tasks(gname):
            if t.get("type") == "tap_template":
                t["interval"] = sec
        self._refresh_task_list(gname)

    def _chat_add_click(self, gname: str, tmpl: str, sec: float) -> str:
        if not (TEMPLATE_DIR / tmpl).exists():
            return (f"Das Bild '{tmpl}' gibt es noch nicht in templates/. "
                    f"Nimm es zuerst im Instanz-Fenster auf oder fuege es per "
                    f"'Bild einfuegen' hinzu.")
        self.add_task(gname, {"type": "tap_template", "name": tmpl.replace(".png", ""),
                              "template": tmpl, "interval": sec, "threshold": 0.85})
        return f"🖼 '{tmpl}' wird jetzt alle {sec}s geklickt."

    def _chat_add_tap(self, gname: str, x: int, y: int, sec: float,
                      w: int = 0, h: int = 0) -> None:
        task = {"type": "tap", "name": f"tap_{x}_{y}", "x": x, "y": y,
                "interval": sec}
        if w and h:
            task["w"], task["h"] = int(w), int(h)
        self.add_task(gname, task)

    def _chat_add_move(self, gname: str, nums: list, sec: float) -> None:
        self.add_task(gname, {"type": "swipe", "name": "bewegung",
                              "from": [nums[0], nums[1]], "to": [nums[2], nums[3]],
                              "ms": 400, "interval": sec})

    def _chat_remove(self, gname: str, name: str) -> str:
        name = name.strip().replace(".png", "")
        tasks = self.controller.group_tasks(gname)
        for i, t in enumerate(tasks):
            if (t.get("name", "").lower() == name.lower() or
                    (t.get("template", "").replace(".png", "").lower() == name.lower())):
                tasks.pop(i)
                self._refresh_task_list(gname)
                return f"🗑 Aufgabe '{name}' entfernt."
        return f"Keine Aufgabe '{name}' gefunden."

    # ---- Anzeige --------------------------------------------------------
    def _refresh_task_list(self, gname: str) -> None:
        lb = self.group_widgets[gname]["list"]
        lb.delete(0, "end")
        for t in self.controller.group_tasks(gname):
            typ = t.get("type", "tap_template")
            iv = t.get("interval", "?")
            if typ == "tap_template":
                lb.insert("end", f"🖼 {t.get('name')}  ({t.get('template')}, alle {iv}s)")
            elif typ == "swipe":
                lb.insert("end", f"↔ {t.get('name')}  ({t.get('from')}→{t.get('to')}, alle {iv}s)")
            elif typ == "tap":
                area = (f" · Flaeche {t['w']}x{t['h']}"
                        if t.get("w") and t.get("h") else "")
                lb.insert("end", f"👆 {t.get('name')}  ({t.get('x')},{t.get('y')}"
                                 f"{area}, alle {iv}s)")
            else:
                lb.insert("end", f"• {t.get('name')}  ({typ}, alle {iv}s)")

    def _refresh(self) -> None:
        drained = 0
        while drained < 100:
            try:
                line = self.log_queue.get_nowait()
            except queue.Empty:
                break
            self._append_log(line)
            drained += 1

        info = self.controller.cycle_info
        if self.controller.cycle_running():
            self.cycle_status.set(f"Zyklus: Runde {info.get('round', 0)} · "
                                  f"{info.get('phase', '-')}")
        else:
            self.cycle_status.set("Zyklus: gestoppt")

        for gname, w in self.group_widgets.items():
            for r in w["rows"]:
                val = r["entry"].get().strip()
                if not val.isdigit():
                    r["status"].config(text="-")
                    continue
                st = self.controller.status.get(int(val))
                if st:
                    conn = "verbunden" if st.connected else (
                        "laeuft" if st.running else "-")
                    r["status"].config(text=f"{conn} · {st.state} · {st.matches}")
                else:
                    r["status"].config(text="(bereit)")
        self.root.after(REFRESH_MS, self._refresh)

    def _append_log(self, line: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", line + "\n")
        self.log.see("end")
        if int(self.log.index("end-1c").split(".")[0]) > 500:
            self.log.delete("1.0", "200.0")
        self.log.configure(state="disabled")

    def _build_log(self) -> None:
        frame = ttk.Frame(self.root, padding=8)
        frame.pack(fill="both", expand=True)
        head = ttk.Frame(frame)
        head.pack(fill="x")
        ttk.Label(head, text="Log:").pack(side="left")
        ttk.Button(head, text="Speichern", command=self.save_log).pack(side="right")
        ttk.Button(head, text="Leeren", command=self.clear_log).pack(side="right", padx=4)
        self.log = tk.Text(frame, height=8, wrap="word", state="disabled",
                           background="#111", foreground="#ddd")
        self.log.pack(fill="both", expand=True)

    def clear_log(self) -> None:
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    def save_log(self) -> None:
        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            initialfile="brawlbot_log.txt",
                                            filetypes=[("Text", "*.txt")])
        if path:
            Path(path).write_text(self.log.get("1.0", "end"), encoding="utf-8")

    def _on_close(self) -> None:
        if self.controller.any_running():
            if not messagebox.askyesno("Beenden?", "Es laufen noch Instanzen. "
                                       "Stoppen und beenden?"):
                return
            self.controller.stop_all()
            self.controller.join_all(timeout=8)
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    BotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

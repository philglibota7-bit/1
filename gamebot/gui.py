"""
Grafisches Gruppen-Steuerpult fuer den LDPlayer-Bot.

Funktionen:
  * Zwei Gruppen (Standard: WIN und LOSE) mit je mehreren Instanzen.
    Alle Instanzen einer Gruppe werden SYNCHRON mit derselben Aufgabenliste
    gesteuert (gleiche Bewegung, gleiche Klicks).
  * Pro Gruppe: Aufgabenliste. Aufgaben sind zeitgesteuert (Intervall in
    Sekunden). "Bild einfuegen" fuegt einen Button hinzu, der automatisch
    erkannt und geklickt wird.
  * Pro Instanz ein eigenes Fenster mit Live-Bild: dort kannst du direkt aus
    dem Screenshot einen Button ausschneiden (2x klicken) und als Bild-Aufgabe
    speichern.
  * Start/Stop pro Gruppe, Dry-Run (nur testen, keine Eingaben), Live-Log.

Start:
    python gui.py

Benoetigt nur die Standardbibliothek (tkinter) + opencv (fuer Bild/Crop).

WICHTIG: Automatisierung von Brawl Stars verstoesst gegen Supercells
Nutzungsbedingungen und fuehrt zu Sperren. Nur mit Wegwerf-Accounts nutzen.
"""

from __future__ import annotations

import json
import queue
import shutil
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk

import cv2

from controller import BotController, load_config, save_config
from ldplayer import LDPlayer

HERE = Path(__file__).parent
TEMPLATE_DIR = HERE / "templates"
REFRESH_MS = 500
DISPLAY_W = 460          # Anzeigebreite der Live-Instanzfenster


class InstanceWindow:
    """Eigenes Fenster einer Instanz: Live-Bild + Button ausschneiden."""

    def __init__(self, app: "BotGUI", port: int, group: str):
        self.app = app
        self.port = port
        self.group = group
        self.screen = None          # aktueller Screenshot (Original, BGR)
        self.scale = 1.0
        self.pt1 = None
        self.tmpfile = HERE / f".live_{port}.png"

        self.win = tk.Toplevel(app.root)
        self.win.title(f"Instanz {port}  (Gruppe {group or '-'})")
        top = ttk.Frame(self.win, padding=6)
        top.pack(fill="x")
        ttk.Button(top, text="🔄 Aktualisieren",
                   command=self.refresh).pack(side="left")
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
        disp_h = int(h / self.scale)
        disp = cv2.resize(self.screen, (DISPLAY_W, disp_h))
        cv2.imwrite(str(self.tmpfile), disp)
        self.photo = tk.PhotoImage(file=str(self.tmpfile))
        self.canvas.config(height=disp_h)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        self.pt1 = None
        self.info.config(text=f"Aufloesung {w}x{h}. Klicke die zwei Ecken des "
                              f"Buttons an.")

    def on_click(self, event) -> None:
        if self.screen is None:
            return
        ox, oy = int(event.x * self.scale), int(event.y * self.scale)
        if self.pt1 is None:
            self.pt1 = (ox, oy)
            self.info.config(text=f"Ecke 1 gesetzt ({ox},{oy}). Jetzt die "
                                  f"gegenueberliegende Ecke anklicken.")
            self.canvas.create_oval(event.x - 3, event.y - 3, event.x + 3,
                                    event.y + 3, outline="#0f0", width=2)
            return
        x1, y1 = self.pt1
        x2, y2 = ox, oy
        self.pt1 = None
        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))
        if x2 - x1 < 4 or y2 - y1 < 4:
            self.info.config(text="Bereich zu klein - nochmal versuchen.")
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
        if self.group and messagebox.askyesno(
            "Als Aufgabe hinzufuegen?",
            f"'{name}' als automatisch geklickten Button zur Gruppe "
            f"'{self.group}' hinzufuegen?", parent=self.win,
        ):
            iv = simpledialog.askfloat("Intervall",
                                       "Alle wie viele Sekunden klicken?",
                                       initialvalue=5.0, parent=self.win)
            self.app.add_task(self.group, {
                "type": "tap_template", "name": name.replace(".png", ""),
                "template": name, "interval": iv or 5.0, "threshold": 0.85,
            })

    def close(self) -> None:
        try:
            self.tmpfile.unlink(missing_ok=True)
        except Exception:  # noqa: BLE001
            pass
        self.app.inst_windows.pop(self.port, None)
        self.win.destroy()


class ConfigEditor:
    """Eigenes Fenster zum Bearbeiten und Speichern der kompletten Config."""

    def __init__(self, app: "BotGUI"):
        self.app = app
        self.win = tk.Toplevel(app.root)
        self.win.title("Config bearbeiten – config.brawlstars.json")
        self.win.geometry("640x600")

        top = ttk.Frame(self.win, padding=6)
        top.pack(fill="x")
        ttk.Label(top, text="Konfiguration (JSON). Aendern und speichern:"
                  ).pack(side="left")

        self.text = tk.Text(self.win, wrap="none", undo=True,
                            font=("Consolas", 10))
        self.text.pack(fill="both", expand=True, padx=6, pady=6)
        yscroll = ttk.Scrollbar(self.win, orient="vertical",
                                command=self.text.yview)
        self.text.configure(yscrollcommand=yscroll.set)

        self.status = ttk.Label(self.win, text="", padding=6, foreground="#080")
        self.status.pack(fill="x")

        btns = ttk.Frame(self.win, padding=6)
        btns.pack(fill="x")
        ttk.Button(btns, text="💾 Speichern",
                   command=self.save).pack(side="left")
        ttk.Button(btns, text="↻ Neu laden",
                   command=self.reload).pack(side="left", padx=6)
        ttk.Button(btns, text="Schliessen",
                   command=self.win.destroy).pack(side="right")

        self.reload()

    def reload(self) -> None:
        self.text.delete("1.0", "end")
        self.text.insert("1.0", json.dumps(self.app.cfg, indent=2,
                                           ensure_ascii=False))
        self.status.config(text="Aktuelle Config geladen.", foreground="#080")

    def save(self) -> None:
        raw = self.text.get("1.0", "end")
        try:
            new_cfg = json.loads(raw)
        except json.JSONDecodeError as exc:
            self.status.config(
                text=f"❌ JSON-Fehler (Zeile {exc.lineno}): {exc.msg}",
                foreground="#b00")
            return
        # Inhalt der bestehenden Config ersetzen (Referenz bleibt erhalten)
        self.app.cfg.clear()
        self.app.cfg.update(new_cfg)
        try:
            save_config(self.app.cfg)
        except Exception as exc:  # noqa: BLE001
            self.status.config(text=f"❌ Speichern fehlgeschlagen: {exc}",
                               foreground="#b00")
            return
        self.status.config(text="✅ Gespeichert. Hinweis: Aenderungen an Ports/"
                                "Gruppen wirken erst nach Neustart der Oberflaeche.",
                           foreground="#080")
        # Aufgabenlisten sofort aktualisieren
        for gname in self.app.group_widgets:
            try:
                self.app._refresh_task_list(gname)
            except Exception:  # noqa: BLE001
                pass


class BotGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("LDPlayer Bot – Gruppen-Steuerpult")
        root.geometry("980x640")
        self.log_queue: "queue.Queue[str]" = queue.Queue()
        self.inst_windows: dict[int, InstanceWindow] = {}

        try:
            self.cfg = load_config()
        except FileNotFoundError as exc:
            messagebox.showerror("Konfiguration fehlt", str(exc))
            root.destroy()
            return

        self.controller = BotController(self.cfg, on_log=self.log_queue.put)
        self.dry_run = tk.BooleanVar(value=False)
        self.group_widgets: dict[str, dict] = {}

        self._build_header()
        self._build_groups()
        self._build_log()

        root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._refresh()

    # ---- Aufbau ---------------------------------------------------------
    def _build_header(self) -> None:
        bar = ttk.Frame(self.root, padding=8)
        bar.pack(fill="x")
        ttk.Checkbutton(bar, text="Dry-Run (nur testen, keine Eingaben)",
                        variable=self.dry_run).pack(side="left")
        ttk.Button(bar, text="💾 Config speichern",
                   command=self.save).pack(side="right")
        ttk.Button(bar, text="⚙ Config bearbeiten",
                   command=self.open_config_editor).pack(side="right", padx=6)
        ttk.Label(self.root, foreground="#b00", padding=(8, 0),
                  text="⚠ Brawl-Stars-Botting verstoesst gegen Supercells "
                       "Nutzungsbedingungen – nur Wegwerf-Accounts, Sperr-Risiko!"
                  ).pack(fill="x")

    def _build_groups(self) -> None:
        wrap = ttk.Frame(self.root, padding=8)
        wrap.pack(fill="both", expand=False)
        groups = self.controller.groups()
        if not groups:
            ttk.Label(wrap, text="Keine 'groups' in der Config definiert."
                      ).pack()
            return
        for gname in groups:
            self._build_group_panel(wrap, gname)

    def _build_group_panel(self, parent, gname: str) -> None:
        box = ttk.LabelFrame(parent, text=f"Gruppe {gname}", padding=8)
        box.pack(side="left", fill="both", expand=True, padx=6)

        # Instanzliste
        ports = self.controller.group_ports(gname)
        inst_frame = ttk.Frame(box)
        inst_frame.pack(fill="x")
        port_labels = {}
        for port in ports:
            row = ttk.Frame(inst_frame)
            row.pack(fill="x", pady=1)
            lbl = ttk.Label(row, width=26, anchor="w",
                            text=f"Port {port}: -")
            lbl.pack(side="left")
            ttk.Button(row, text="Fenster",
                       command=lambda p=port, g=gname: self.open_instance(p, g)
                       ).pack(side="right")
            port_labels[port] = lbl

        # Start/Stop
        btns = ttk.Frame(box)
        btns.pack(fill="x", pady=(6, 4))
        ttk.Button(btns, text="▶ Gruppe starten",
                   command=lambda g=gname: self.start_group(g)).pack(side="left")
        ttk.Button(btns, text="■ Gruppe stoppen",
                   command=lambda g=gname: self.controller.stop_group(g)
                   ).pack(side="left", padx=6)

        # Aufgabenliste
        ttk.Label(box, text="Aufgaben (zeitgesteuert):").pack(anchor="w")
        listbox = tk.Listbox(box, height=8)
        listbox.pack(fill="both", expand=True)

        tb = ttk.Frame(box)
        tb.pack(fill="x", pady=4)
        ttk.Button(tb, text="🖼 Bild einfuegen",
                   command=lambda g=gname: self.add_image_task(g)).pack(side="left")
        ttk.Button(tb, text="↔ Bewegung",
                   command=lambda g=gname: self.add_move_task(g)).pack(side="left", padx=4)
        ttk.Button(tb, text="🗑 Entfernen",
                   command=lambda g=gname: self.remove_task(g)).pack(side="left")

        self.group_widgets[gname] = {"labels": port_labels, "list": listbox}
        self._refresh_task_list(gname)

    def _build_log(self) -> None:
        frame = ttk.Frame(self.root, padding=8)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Log:").pack(anchor="w")
        self.log = tk.Text(frame, height=8, wrap="word", state="disabled",
                           background="#111", foreground="#ddd")
        self.log.pack(fill="both", expand=True)

    # ---- Aktionen -------------------------------------------------------
    def open_config_editor(self) -> None:
        ConfigEditor(self)

    def open_instance(self, port: int, group: str) -> None:
        if port in self.inst_windows:
            self.inst_windows[port].win.lift()
            return
        self.inst_windows[port] = InstanceWindow(self, port, group)

    def start_group(self, gname: str) -> None:
        self.controller.start_group(gname, dry_run=self.dry_run.get())

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
        iv = simpledialog.askfloat("Intervall",
                                   "Alle wie viele Sekunden klicken?",
                                   initialvalue=5.0, parent=self.root)
        self.add_task(gname, {
            "type": "tap_template", "name": dest.stem, "template": dest.name,
            "interval": iv or 5.0, "threshold": 0.85,
        })

    def add_move_task(self, gname: str) -> None:
        s = simpledialog.askstring(
            "Bewegung", "von_x,von_y -> nach_x,nach_y  (z. B. 220,780,220,650):",
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
        self.add_task(gname, {
            "type": "swipe", "name": "bewegung", "from": [a, b], "to": [c, d],
            "ms": 400, "interval": iv or 1.0,
        })

    def remove_task(self, gname: str) -> None:
        lb = self.group_widgets[gname]["list"]
        sel = lb.curselection()
        if not sel:
            return
        idx = sel[0]
        tasks = self.controller.group_tasks(gname)
        if 0 <= idx < len(tasks):
            removed = tasks.pop(idx)
            self._refresh_task_list(gname)
            self.log_queue.put(f"[{gname}] Aufgabe entfernt: "
                               f"{removed.get('name')}")

    def save(self) -> None:
        try:
            save_config(self.cfg)
            messagebox.showinfo("Gespeichert", "config.brawlstars.json gespeichert.")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Fehler", str(exc))

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

        for gname, w in self.group_widgets.items():
            for port, lbl in w["labels"].items():
                st = self.controller.status.get(port)
                if st:
                    conn = "verbunden" if st.connected else (
                        "laeuft" if st.running else "-")
                    lbl.config(text=f"Port {port}: {conn} · {st.state} · "
                                    f"Klicks {st.matches}")
        self.root.after(REFRESH_MS, self._refresh)

    def _append_log(self, line: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", line + "\n")
        self.log.see("end")
        if int(self.log.index("end-1c").split(".")[0]) > 500:
            self.log.delete("1.0", "200.0")
        self.log.configure(state="disabled")

    def _on_close(self) -> None:
        if self.controller.any_running():
            if not messagebox.askyesno("Beenden?",
                                       "Es laufen noch Instanzen. Stoppen und "
                                       "beenden?"):
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

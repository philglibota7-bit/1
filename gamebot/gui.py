"""
Grafische Startflaeche fuer den LDPlayer / Brawl-Stars-Bot.

Nutzt nur die Python-Standardbibliothek (tkinter) -- keine Extra-Installation.

Funktionen:
  * Tabelle aller Instanzen aus config.brawlstars.json mit Live-Status
    (Verbindung, Zustand MENU/QUEUE/MATCH/..., Anzahl Matches).
  * Start / Stop einzeln pro Instanz und "Alle starten" / "Alle stoppen".
  * Dry-Run-Schalter: erkennt nur, sendet KEINE Eingaben (zum Testen).
  * Live-Log unten.

Start:
    python gui.py

WICHTIG: Automatisierung von Brawl Stars verstoesst gegen Supercells
Nutzungsbedingungen und fuehrt zu Sperren. Nur mit Wegwerf-Accounts nutzen.
"""

from __future__ import annotations

import queue
import tkinter as tk
from tkinter import messagebox, ttk

from controller import BotController, load_config

REFRESH_MS = 500


class BotGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("LDPlayer Bot – Steuerung")
        root.geometry("760x520")
        root.minsize(680, 440)

        self.log_queue: "queue.Queue[str]" = queue.Queue()

        try:
            self.cfg = load_config()
        except FileNotFoundError as exc:
            messagebox.showerror("Konfiguration fehlt", str(exc))
            root.destroy()
            return

        self.controller = BotController(self.cfg, on_log=self.log_queue.put)
        self.dry_run = tk.BooleanVar(value=False)

        self._build_header()
        self._build_table()
        self._build_log()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._refresh()

    # ---- Aufbau der Oberflaeche ----------------------------------------
    def _build_header(self) -> None:
        bar = ttk.Frame(self.root, padding=8)
        bar.pack(fill="x")

        ttk.Button(bar, text="▶ Alle starten",
                   command=self.start_all).pack(side="left")
        ttk.Button(bar, text="■ Alle stoppen",
                   command=self.stop_all).pack(side="left", padx=(6, 12))
        ttk.Checkbutton(bar, text="Dry-Run (nur testen, keine Eingaben)",
                        variable=self.dry_run).pack(side="left")

        warn = ttk.Label(
            self.root,
            text="⚠ Brawl-Stars-Botting verstoesst gegen Supercells "
                 "Nutzungsbedingungen – nur Wegwerf-Accounts, Sperr-Risiko!",
            foreground="#b00",
            padding=(8, 0),
        )
        warn.pack(fill="x")

    def _build_table(self) -> None:
        frame = ttk.Frame(self.root, padding=8)
        frame.pack(fill="both", expand=False)

        cols = ("name", "port", "conn", "state", "matches", "action")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings", height=8)
        for col, txt, w in (
            ("name", "Instanz", 140),
            ("port", "Port", 70),
            ("conn", "Verbindung", 100),
            ("state", "Zustand", 110),
            ("matches", "Matches", 80),
            ("action", "Laeuft", 80),
        ):
            self.tree.heading(col, text=txt)
            self.tree.column(col, width=w, anchor="center")
        self.tree.column("name", anchor="w")
        self.tree.pack(side="left", fill="x", expand=True)

        for inst in self.controller.instances():
            self.tree.insert("", "end", iid=str(inst["port"]),
                             values=(inst.get("name", inst["port"]), inst["port"],
                                     "-", "-", 0, "nein"))

        btns = ttk.Frame(frame, padding=(8, 0))
        btns.pack(side="left", fill="y")
        ttk.Button(btns, text="▶ Start (Auswahl)",
                   command=self.start_selected).pack(fill="x", pady=2)
        ttk.Button(btns, text="■ Stop (Auswahl)",
                   command=self.stop_selected).pack(fill="x", pady=2)

    def _build_log(self) -> None:
        frame = ttk.Frame(self.root, padding=8)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Log:").pack(anchor="w")
        self.log = tk.Text(frame, height=8, wrap="word", state="disabled",
                           background="#111", foreground="#ddd")
        self.log.pack(fill="both", expand=True)

    # ---- Aktionen -------------------------------------------------------
    def _selected_ports(self) -> list[int]:
        return [int(i) for i in self.tree.selection()]

    def start_selected(self) -> None:
        ports = self._selected_ports()
        if not ports:
            messagebox.showinfo("Hinweis", "Bitte oben eine Instanz auswaehlen.")
            return
        for p in ports:
            self.controller.start(p, dry_run=self.dry_run.get())

    def stop_selected(self) -> None:
        for p in self._selected_ports():
            self.controller.stop(p)

    def start_all(self) -> None:
        self.controller.start_all(dry_run=self.dry_run.get())

    def stop_all(self) -> None:
        self.controller.stop_all()

    # ---- periodische Aktualisierung ------------------------------------
    def _refresh(self) -> None:
        # Log-Zeilen abholen
        drained = 0
        while drained < 100:
            try:
                line = self.log_queue.get_nowait()
            except queue.Empty:
                break
            self._append_log(line)
            drained += 1

        # Statuszeilen aktualisieren
        for port, st in self.controller.status.items():
            iid = str(port)
            if self.tree.exists(iid):
                conn = "verbunden" if st.connected else ("laeuft" if st.running else "-")
                self.tree.item(iid, values=(
                    st.name, st.port, conn, st.state, st.matches,
                    "ja" if st.running else "nein",
                ))
        self.root.after(REFRESH_MS, self._refresh)

    def _append_log(self, line: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", line + "\n")
        self.log.see("end")
        # Log nicht unbegrenzt wachsen lassen
        if int(self.log.index("end-1c").split(".")[0]) > 500:
            self.log.delete("1.0", "200.0")
        self.log.configure(state="disabled")

    def _on_close(self) -> None:
        if self.controller.any_running():
            if not messagebox.askyesno(
                "Beenden?", "Es laufen noch Instanzen. Stoppen und beenden?"
            ):
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

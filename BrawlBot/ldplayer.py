"""
Steuerung eines LDPlayer-Emulators ueber ADB (Android Debug Bridge).

Der LDPlayer bringt eine eigene ADB-Bruecke mit. Ueber diese koennen wir
Screenshots holen und Taps / Swipes / Tasten senden -- der zuverlaessigste
Weg, ein Spiel im Emulator zu automatisieren (stabiler als Fenster-Klicks).

Voraussetzung:
  1. In den LDPlayer-Einstellungen  ->  "Andere Einstellungen"  ->
     "ADB-Debugging"  ->  "Lokale Verbindung aktivieren".
  2. ADB muss installiert / im PATH sein. LDPlayer liefert eine eigene
     adb.exe mit (im LDPlayer-Installationsordner). Alternativ die
     Android-Platform-Tools installieren.
"""

from __future__ import annotations

import subprocess
import time

import numpy as np

try:
    import cv2
except ImportError as exc:  # pragma: no cover - Hinweis fuer den Nutzer
    raise SystemExit(
        "OpenCV fehlt. Bitte 'pip install -r requirements.txt' ausfuehren."
    ) from exc


class LDPlayer:
    """Duenner ADB-Wrapper fuer genau eine LDPlayer-Instanz."""

    def __init__(self, host: str = "127.0.0.1", port: int = 5555,
                 adb_path: str = "adb"):
        # LDPlayer-Instanzen lauschen typischerweise auf 5555, 5557, 5559 ...
        # (eine Instanz = +2 Port). Bei nur einer Instanz passt 5555.
        self.serial = f"{host}:{port}"
        self.adb_path = adb_path

    # ---- interne Helfer -------------------------------------------------
    def _adb(self, *args: str, capture: bool = False) -> bytes:
        cmd = [self.adb_path, "-s", self.serial, *args]
        if capture:
            return subprocess.run(cmd, check=True, capture_output=True).stdout
        subprocess.run(cmd, check=True)
        return b""

    # ---- Verbindung -----------------------------------------------------
    def connect(self) -> None:
        """Stellt die ADB-Verbindung zur Instanz her."""
        subprocess.run([self.adb_path, "connect", self.serial], check=True)
        # kurz warten, bis das Geraet als 'device' gemeldet wird
        for _ in range(10):
            out = subprocess.run(
                [self.adb_path, "-s", self.serial, "get-state"],
                capture_output=True, text=True,
            )
            if out.stdout.strip() == "device":
                return
            time.sleep(0.5)
        raise RuntimeError(
            f"Keine ADB-Verbindung zu {self.serial}. Ist ADB-Debugging im "
            f"LDPlayer aktiviert und die Instanz gestartet?"
        )

    def reconnect(self) -> bool:
        """Versucht die Verbindung neu aufzubauen (fuer den Watchdog)."""
        try:
            subprocess.run([self.adb_path, "disconnect", self.serial],
                           capture_output=True)
        except Exception:  # noqa: BLE001
            pass
        try:
            self.connect()
            return True
        except Exception:  # noqa: BLE001
            return False

    # ---- Wahrnehmung ----------------------------------------------------
    def screenshot(self) -> np.ndarray:
        """Aktuelles Bild als BGR-Numpy-Array (fuer OpenCV)."""
        png = self._adb("exec-out", "screencap", "-p", capture=True)
        img = cv2.imdecode(np.frombuffer(png, np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            raise RuntimeError("Screenshot konnte nicht dekodiert werden.")
        return img

    # ---- Aktionen -------------------------------------------------------
    def tap(self, x: int, y: int) -> None:
        self._adb("shell", "input", "tap", str(x), str(y))

    def swipe(self, x1: int, y1: int, x2: int, y2: int, ms: int = 300) -> None:
        self._adb("shell", "input", "swipe",
                  str(x1), str(y1), str(x2), str(y2), str(ms))

    def key(self, keycode: str) -> None:
        # z. B. "KEYCODE_BACK", "KEYCODE_HOME", "KEYCODE_ENTER"
        self._adb("shell", "input", "keyevent", keycode)

    def text(self, value: str) -> None:
        # Leerzeichen fuer 'input text' maskieren
        self._adb("shell", "input", "text", value.replace(" ", "%s"))

    def start_app(self, package_activity: str) -> None:
        # z. B. "com.example.game/.MainActivity"
        self._adb("shell", "am", "start", "-n", package_activity)

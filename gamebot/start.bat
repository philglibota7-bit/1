@echo off
REM =====================================================================
REM  LDPlayer / Brawl Stars Bot - Ein-Klick-Start (Windows)
REM  Doppelklick auf diese Datei startet die komplette Einrichtung
REM  und oeffnet die Steuer-Oberflaeche.
REM =====================================================================
chcp 65001 >nul
cd /d "%~dp0"
title LDPlayer Bot - Start

echo ==========================================================
echo    LDPlayer / Brawl Stars Bot
echo ==========================================================
echo.
echo  Hinweis: Botting verstoesst gegen Supercells Nutzungs-
echo  bedingungen. Nur mit Wegwerf-Accounts nutzen (Sperr-Risiko).
echo.

REM ---- 1) Python vorhanden? -------------------------------------------
python --version >nul 2>&1
if errorlevel 1 (
  echo [FEHLER] Python wurde nicht gefunden.
  echo   Bitte Python von https://www.python.org/downloads installieren
  echo   und beim Setup "Add Python to PATH" anhaken. Danach neu starten.
  echo.
  pause
  exit /b 1
)

REM ---- 2) ADB von LDPlayer suchen und in PATH aufnehmen ---------------
set "ADBDIR="
for %%D in (
  "C:\LDPlayer\LDPlayer9"
  "C:\LDPlayer\LDPlayer64"
  "C:\Program Files\LDPlayer\LDPlayer9"
  "C:\Program Files (x86)\LDPlayer\LDPlayer9"
  "C:\ChangZhi\LDPlayer9"
  "D:\LDPlayer\LDPlayer9"
) do (
  if exist "%%~D\adb.exe" set "ADBDIR=%%~D"
)
if defined ADBDIR (
  echo [ADB] gefunden in "%ADBDIR%"
  set "PATH=%ADBDIR%;%PATH%"
) else (
  echo [ADB] LDPlayer-adb nicht automatisch gefunden.
  echo       Falls der Scan nichts findet, adb.exe in den PATH legen
  echo       oder scan.py mit --adb "Pfad\adb.exe" aufrufen.
)
echo.

REM ---- 3) Abhaengigkeiten installieren --------------------------------
echo [1/4] Installiere Abhaengigkeiten (opencv, numpy) ...
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo [FEHLER] Installation fehlgeschlagen. Internet/Proxy pruefen.
  pause
  exit /b 1
)
echo.

REM ---- 4) Config anlegen, falls nicht vorhanden -----------------------
if not exist "config.brawlstars.json" (
  echo [2/4] Lege config.brawlstars.json aus der Vorlage an ...
  copy /y "config.brawlstars.example.json" "config.brawlstars.json" >nul
) else (
  echo [2/4] config.brawlstars.json ist bereits vorhanden.
)
echo.

REM ---- 5) Instanzen / Ports scannen -----------------------------------
echo [3/4] Suche laufende LDPlayer-Instanzen ...
echo       (Stelle sicher, dass die Fenster laufen und ADB aktiviert ist.)
echo.
python scan.py
echo.
echo ----------------------------------------------------------
echo  Uebertrage die oben gezeigten Ports in config.brawlstars.json,
echo  falls sie abweichen. Die Datei liegt in DIESEM Ordner.
echo ----------------------------------------------------------
echo.
echo  Weiter mit einer beliebigen Taste, dann oeffnet sich die Oberflaeche.
pause >nul

REM ---- 6) Oberflaeche starten -----------------------------------------
echo [4/4] Starte die Steuer-Oberflaeche ...
python gui.py

echo.
echo Oberflaeche beendet.
pause

@echo off
REM =====================================================================
REM  BrawlBot als Windows-.exe bauen (ohne Python-Installation startbar)
REM  Ergebnis: dist\BrawlBot.exe
REM =====================================================================
chcp 65001 >nul
cd /d "%~dp0"
title BrawlBot - EXE bauen

echo [1/2] Installiere PyInstaller + Abhaengigkeiten ...
python -m pip install --upgrade pyinstaller >nul 2>&1
python -m pip install -r requirements.txt >nul 2>&1

echo [2/2] Baue BrawlBot.exe (das dauert 1-3 Minuten) ...
python -m PyInstaller --noconfirm --onefile --windowed ^
  --name BrawlBot ^
  --add-data "config.brawlstars.example.json;." ^
  gui.py

echo.
if exist "dist\BrawlBot.exe" (
  echo FERTIG: dist\BrawlBot.exe
  echo Lege die Datei zusammen mit dem Ordner 'templates' und deiner
  echo config.brawlstars.json / configs\ ins selbe Verzeichnis.
) else (
  echo FEHLER: Build nicht erfolgreich. Meldung oben pruefen.
)
echo.
pause

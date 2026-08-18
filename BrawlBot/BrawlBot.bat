@echo off
REM Startet BrawlBot (Doppelklick-App). Liegt im Projektordner.
cd /d "%~dp0"
python gui.py
if errorlevel 1 (
  echo.
  echo BrawlBot konnte nicht starten. Fehler oben pruefen.
  echo Tipp: einmal  pip install -r requirements.txt  ausfuehren.
  pause
)

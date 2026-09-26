@echo off
cd /d "%~dp0"
set "PYW="
where py >nul 2>&1
if %errorlevel%==0 (
  for /f "delims=" %%I in ('py -3 -c "import sys; from pathlib import Path; print(Path(sys.executable).with_name(''pythonw.exe''))"') do set "PYW=%%I"
)
if not exist "%PYW%" (
  echo Run setup.bat first.
  pause
  exit /b 1
)
start "" "%PYW%" "%~dp0ar_remote.py" --tray

@echo off
cd /d "%~dp0"
set "PYW="
where py >nul 2>&1
if %errorlevel%==0 (
  py -3 -c "import sys; from pathlib import Path; p=Path(sys.executable).with_name('pythonw.exe'); print(p if p.exists() else '')" > "%TEMP%\ar-pythonw.txt"
) else (
  python -c "import sys; from pathlib import Path; p=Path(sys.executable).with_name('pythonw.exe'); print(p if p.exists() else '')" > "%TEMP%\ar-pythonw.txt"
)
set /p PYW=<"%TEMP%\ar-pythonw.txt"
if not exist "%PYW%" (
  echo Run setup.bat first.
  pause
  exit /b 1
)
start "" "%PYW%" "%~dp0ar_remote.py" --tray

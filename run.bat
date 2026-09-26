@echo off
cd /d "%~dp0"
start "" "%LOCALAPPDATA%\Python\pythoncore-3.14-64\pythonw.exe" "%~dp0ar_remote.py" --tray

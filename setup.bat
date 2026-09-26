@echo off
cd /d "%~dp0"
echo.
echo DO NOT DO THIS ON PUBLIC WI-FI.
echo.
echo Use a private network you trust, such as your home Wi-Fi.
echo A cafe, hotel, airport, school, or guest network is not safe.
echo.
echo Wireless debugging lets this PC run commands on the phone.
echo Turn it off when you are done, and leave it off away from home.
echo.
pause
where py >nul 2>&1
if %errorlevel%==0 (
  set "RUN=py -3"
) else (
  set "RUN=python"
)
echo Installing the tray app...
%RUN% -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 goto fail
echo.
%RUN% "%~dp0ar_remote.py" --setup
if errorlevel 1 goto fail
echo.
%RUN% "%~dp0ar_remote.py" --pair
if errorlevel 1 goto fail
call "%~dp0run.bat"
echo.
echo Done. Click the round icon by the clock when you want the remote on this PC.
pause
exit /b 0

:fail
echo.
echo Setup stopped.
pause
exit /b 1

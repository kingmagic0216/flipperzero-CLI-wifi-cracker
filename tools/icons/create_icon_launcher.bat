@echo off
echo Creating WiFi Cracker shortcut with icon...
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0Create Launcher with Icon.ps1"

if errorlevel 1 (
    echo.
    echo Trying VBScript method...
    cscript //nologo "%~dp0Create Launcher with Icon.vbs"
)

echo.
echo Done! Check your desktop and app folder for "WiFi Cracker.lnk"
echo.
pause


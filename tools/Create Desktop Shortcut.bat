@echo off
echo Creating desktop shortcut for WiFi Cracker...
echo.

set SCRIPT_DIR=%~dp0
set DESKTOP=%USERPROFILE%\Desktop
set SHORTCUT_NAME=WiFi Cracker.lnk

powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\%SHORTCUT_NAME%'); $Shortcut.TargetPath = '%SCRIPT_DIR%start_wifi_cracker_gui.pyw'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.Description = 'Launch WiFi Cracker Web App'; $Shortcut.Save()"

echo.
echo ✓ Desktop shortcut created!
echo   Look for "WiFi Cracker" on your desktop
echo.
pause


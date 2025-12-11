@echo off
title Create WiFi Cracker Shortcuts
color 0B

echo.
echo ═══════════════════════════════════════════════════════
echo   Creating WiFi Cracker Shortcuts with Icons
echo ═══════════════════════════════════════════════════════
echo.

cd /d "%~dp0\.."

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell -ExecutionPolicy Bypass -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\WiFi Cracker.lnk'); $Shortcut.TargetPath = '%CD%\start_wifi_cracker_gui.pyw'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.Description = 'Launch WiFi Cracker Web App'; $Shortcut.IconLocation = 'shell32.dll,48'; $Shortcut.Save()"

REM Create app folder shortcut
echo Creating app folder shortcut...
powershell -ExecutionPolicy Bypass -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%CD%\WiFi Cracker.lnk'); $Shortcut.TargetPath = '%CD%\start_wifi_cracker_gui.pyw'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.Description = 'Launch WiFi Cracker Web App'; $Shortcut.IconLocation = 'shell32.dll,48'; $Shortcut.Save()"

echo.
echo ✓ Shortcuts created successfully!
echo.
echo   • Desktop: WiFi Cracker.lnk (with lock icon)
echo   • App folder: WiFi Cracker.lnk (with lock icon)
echo.
echo   You can now use these shortcuts instead of the .pyw file!
echo.
pause


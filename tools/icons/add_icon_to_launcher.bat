@echo off
title Add Icon to WiFi Cracker Launcher
color 0B

echo.
echo ═══════════════════════════════════════════════════════
echo   Creating WiFi Cracker Shortcut with Icon
echo ═══════════════════════════════════════════════════════
echo.

cd /d "%~dp0"

REM Delete old shortcut if exists
if exist "WiFi Cracker.lnk" del "WiFi Cracker.lnk"

REM Create shortcut in app folder with icon
echo Creating shortcut with lock icon...
powershell -ExecutionPolicy Bypass -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%CD%\WiFi Cracker.lnk'); $Shortcut.TargetPath = '%CD%\start_wifi_cracker_gui.pyw'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.Description = 'Launch WiFi Cracker Web App'; $Shortcut.IconLocation = 'C:\Windows\System32\shell32.dll,48'; $Shortcut.Save(); Write-Host '✓ Shortcut created!' -ForegroundColor Green"

REM Also create desktop shortcut
echo Creating desktop shortcut...
powershell -ExecutionPolicy Bypass -Command "$WshShell = New-Object -ComObject WScript.Shell; $Desktop = [Environment]::GetFolderPath('Desktop'); if (Test-Path ($Desktop + '\WiFi Cracker.lnk')) { Remove-Item ($Desktop + '\WiFi Cracker.lnk') -Force }; $Shortcut = $WshShell.CreateShortcut($Desktop + '\WiFi Cracker.lnk'); $Shortcut.TargetPath = '%CD%\start_wifi_cracker_gui.pyw'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.Description = 'Launch WiFi Cracker Web App'; $Shortcut.IconLocation = 'C:\Windows\System32\shell32.dll,48'; $Shortcut.Save(); Write-Host '✓ Desktop shortcut created!' -ForegroundColor Green"

echo.
echo ═══════════════════════════════════════════════════════
echo   ✓ Done!
echo ═══════════════════════════════════════════════════════
echo.
echo   Created shortcuts with lock icon:
echo   • WiFi Cracker.lnk (in this folder)
echo   • WiFi Cracker.lnk (on your Desktop)
echo.
echo   The icon should appear after refreshing (F5 in Explorer)
echo.
pause

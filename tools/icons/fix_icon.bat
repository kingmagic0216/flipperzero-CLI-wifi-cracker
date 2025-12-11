@echo off
title Fix WiFi Cracker Icon
color 0B

echo.
echo ═══════════════════════════════════════════════════════
echo   Fixing WiFi Cracker Shortcut Icon
echo ═══════════════════════════════════════════════════════
echo.

cd /d "%~dp0"

powershell -ExecutionPolicy Bypass -File "tools\icons\fix_icon.ps1"

echo.
echo ═══════════════════════════════════════════════════════
echo   Manual Icon Setup (if needed)
echo ═══════════════════════════════════════════════════════
echo.
echo If you still don't see the icon:
echo.
echo 1. Right-click "WiFi Cracker.lnk"
echo 2. Select "Properties"
echo 3. Click "Change Icon" button
echo 4. Click "Browse"
echo 5. Navigate to: C:\Windows\System32\shell32.dll
echo 6. Select icon #48 (lock) or any icon you like
echo 7. Click OK
echo.
echo Alternative icons to try:
echo   #48  - Lock icon
echo   #137 - Network/globe icon
echo   #138 - WiFi icon
echo   #19  - Key icon
echo   #24  - Lock with key
echo.
pause


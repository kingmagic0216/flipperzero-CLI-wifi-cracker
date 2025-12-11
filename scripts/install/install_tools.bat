@echo off
REM WiFi Cracker - Tools Installation Script (Batch version)
echo ========================================
echo WiFi Cracker - Tools Installation
echo ========================================
echo.

REM Check for hashcat
where hashcat >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo [OK] Hashcat is installed
    hashcat --version 2>nul | findstr /C:"v"
) else (
    echo [MISSING] Hashcat is not installed
    echo.
    echo To install Hashcat:
    echo 1. Download from: https://hashcat.net/hashcat/
    echo 2. Extract to a folder (e.g., C:\hashcat)
    echo 3. Add the folder to your PATH
    echo.
)

REM Check for hcxpcapngtool
where hcxpcapngtool >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo [OK] hcxpcapngtool is installed
    hcxpcapngtool -v 2>nul
) else (
    echo [MISSING] hcxpcapngtool is not installed
    echo.
    echo To install hcxtools:
    echo Option A - Use WSL (Recommended):
    echo   wsl --install
    echo   Then in WSL: sudo apt-get install hcxtools
    echo.
    echo Option B - Check: https://github.com/ZerBea/hcxtools/releases
    echo.
)

echo.
echo ========================================
echo For detailed instructions, see docs/INSTALL_TOOLS.md
echo ========================================
pause


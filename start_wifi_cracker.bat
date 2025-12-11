@echo off
title WiFi Cracker - Launcher
color 0A

echo.
echo ========================================
echo   WiFi Cracker - One-Click Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Please install Python from https://www.python.org/
    echo.
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Navigate to script directory
cd /d "%~dp0"

REM Check if Flask is installed, if not install requirements
echo Checking dependencies...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt --quiet
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies already installed
)

echo.
echo ========================================
echo   Starting WiFi Cracker Web Server...
echo ========================================
echo.
echo The server will start in a moment...
echo You can access it from:
echo   - Your computer: http://localhost:5000
echo   - Your phone: http://YOUR_IP:5000
echo.
echo Press CTRL+C to stop the server
echo.

REM Wait a moment then open browser
timeout /t 3 /nobreak >nul
start http://localhost:5000

REM Start the Flask app
python app.py

pause


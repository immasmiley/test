@echo off
title U3CP F-Droid Installation
color 0A
cls

echo.
echo ========================================
echo   U3CP F-DROID INSTALLATION
echo ========================================
echo.
echo This script will install U3CP as a proper
echo Android app using F-Droid
echo.
echo Prerequisites:
echo - Samsung Galaxy J3 connected via USB
echo - USB Debugging enabled
echo - F-Droid installed on device
echo.
echo Installation Steps:
echo 1. Check device connection
echo 2. Verify F-Droid installation
echo 3. Install Python via Pydroid 3
echo 4. Build U3CP Android app
echo 5. Install and launch U3CP app
echo.
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

echo ✅ Python found
echo.

echo Starting U3CP F-Droid installation...
echo.

python install_u3cp_via_fdroid.py

echo.
echo ========================================
echo Installation process completed
echo ========================================
echo.
echo Check the generated report for details:
echo - u3cp_fdroid_installation_report.json
echo.
pause 
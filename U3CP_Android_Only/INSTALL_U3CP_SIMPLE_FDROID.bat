@echo off
title Simple U3CP F-Droid Installation
color 0B
cls

echo.
echo ========================================
echo   SIMPLE U3CP F-DROID INSTALLATION
echo ========================================
echo.
echo This script will install Python via F-Droid
echo and deploy U3CP to run directly on your device
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
echo 4. Deploy U3CP files to device
echo 5. Create launcher interface
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

echo Starting Simple U3CP F-Droid installation...
echo.

python install_u3cp_simple_fdroid.py

echo.
echo ========================================
echo Installation process completed
echo ========================================
echo.
echo Check the generated report for details:
echo - u3cp_simple_fdroid_installation_report.json
echo.
echo If successful, open u3cp_pydroid3_launcher.html
echo to launch U3CP on your device.
echo.
pause 
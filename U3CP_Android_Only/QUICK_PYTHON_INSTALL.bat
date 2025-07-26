@echo off
title Quick Python Installer for U3CP
color 0C
cls

echo.
echo ========================================
echo   QUICK PYTHON INSTALLER FOR U3CP
echo ========================================
echo.
echo This installer will:
echo - Check what Python options are available
echo - Install the best Python environment
echo - Create appropriate launcher for U3CP
echo.
echo Available options:
echo - Pydroid 3 (Full Python IDE)
echo - QPython 3 (Lightweight interpreter)
echo - Termux (Linux terminal)
echo - Kivy Launcher (Python app launcher)
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

echo Starting Quick Python installation...
echo.

python quick_python_installer.py

echo.
echo ========================================
echo Installation process completed
echo ========================================
echo.
echo Check the generated report for details:
echo - quick_python_installation_report.json
echo.
echo If successful, open the generated launcher HTML
echo file to start U3CP on your device.
echo.
pause 
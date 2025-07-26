@echo off
echo ========================================
echo    SphereOS Enhanced Constituent App
echo ========================================
echo.
echo Starting SphereOS with enhanced constituent-wrapped dependencies...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.7+ and try again.
    pause
    exit /b 1
)

echo ✅ Python found
echo 🚀 Starting SphereOS Enhanced Constituent-Wrapped Application...
echo.

REM Run the enhanced constituent-wrapped application
python sphereos_enhanced_constituent.py

echo.
echo Application completed.
pause 
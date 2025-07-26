@echo off
echo ========================================
echo   SphereOS Independent Application
echo ========================================
echo.
echo Starting SphereOS Independent Copy...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

echo ✅ Python found
echo 🌌 Starting SphereOS Independent Application...
echo.

REM Run the enhanced constituent application
python sphereos_enhanced_constituent.py

echo.
echo ========================================
echo   SphereOS Independent - Complete
echo ========================================
pause 
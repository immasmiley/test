@echo off
REM SphereOS Android Unified Application Launcher
REM Windows batch file for launching the unified application

echo.
echo ========================================
echo   SphereOS Android Unified Application
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

echo Python found. Checking dependencies...

REM Check if Kivy is available
python -c "import kivy" >nul 2>&1
if errorlevel 1 (
    echo Kivy not found. Running in console mode...
    set GUI_MODE=false
) else (
    echo Kivy found. Running in GUI mode...
    set GUI_MODE=true
)

echo.
echo Starting SphereOS Android Unified Application...
echo.

if "%GUI_MODE%"=="true" (
    python SphereOS_Android_Unified.py --gui
) else (
    python SphereOS_Android_Unified.py
)

echo.
echo Application closed.
pause 
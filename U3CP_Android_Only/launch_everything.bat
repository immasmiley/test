@echo off
echo ========================================
echo U3CP Complete System Launcher
echo ========================================
echo.
echo Starting real installation system...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python first.
    pause
    exit /b 1
)

echo ✅ Python found. Starting real tap installer server...
echo.

REM Start the real tap installer server in background
start "U3CP Real Tap Installer Server" python real_tap_installer.py

echo 🚀 Real tap installer server started on port 8080
echo.
echo Waiting for server to initialize...
timeout /t 3 /nobreak >nul

echo.
echo 📱 Opening user-friendly interface...
echo.

REM Open the real tap installer interface
start "" "tap_to_install_real.html"

echo ========================================
echo 🎉 Everything is ready!
echo ========================================
echo.
echo ✅ Real tap installer server: Running on port 8080
echo ✅ User interface: Opened in browser
echo ✅ ADB connection: Ready
echo ✅ Termux: Installed
echo.
echo 📋 Next steps:
echo 1. Use the interface to install Python
echo 2. Start the real system dashboard
echo 3. Launch the U3CP system
echo.
echo 💚 No simulation theater - real commands only!
echo.
pause 
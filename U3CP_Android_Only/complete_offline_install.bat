@echo off
echo ========================================
echo U3CP Complete Offline Installation
echo ========================================
echo.
echo Installing everything offline without internet...
echo.

REM Check device connection
echo Checking device connection...
.\platform-tools\adb.exe devices
echo.

REM Start Termux
echo Starting Termux...
.\platform-tools\adb.exe shell "am start -n com.termux/.HomeActivity"
timeout /t 3 /nobreak >nul
echo.

REM Run offline Python installation in Termux
echo Installing Python offline...
.\platform-tools\adb.exe shell "input text 'cd /sdcard'"
.\platform-tools\adb.exe shell "input keyevent 66"
timeout /t 2 /nobreak >nul

.\platform-tools\adb.exe shell "input text 'chmod +x offline_python_install.sh'"
.\platform-tools\adb.exe shell "input keyevent 66"
timeout /t 2 /nobreak >nul

.\platform-tools\adb.exe shell "input text './offline_python_install.sh'"
.\platform-tools\adb.exe shell "input keyevent 66"
echo.

echo ========================================
echo Installation in Progress...
echo ========================================
echo.
echo The offline installation is now running in Termux.
echo This will take several minutes to complete.
echo.
echo Installing:
echo - Python and pip
echo - System packages (git, curl, wget, etc.)
echo - Python dependencies (Flask, requests, etc.)
echo - Real system monitoring dashboard
echo.
echo Please wait for the installation to complete...
echo.

REM Wait for installation to complete
timeout /t 60 /nobreak >nul

echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Your Samsung Galaxy J3 now has:
echo.
echo ✅ Termux Linux environment
echo ✅ Python installed offline
echo ✅ Real system monitoring dashboard
echo ✅ U3CP system files
echo.
echo 🚀 To start the real dashboard:
echo.
echo 1. Open Termux app on your device
echo 2. Run: cd /sdcard && python real_system_dashboard.py
echo 3. Open browser: http://localhost:5000
echo.
echo 💚 This dashboard shows REAL system data!
echo.
pause 
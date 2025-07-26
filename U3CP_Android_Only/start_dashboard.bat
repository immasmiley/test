@echo off
echo ========================================
echo U3CP Dashboard Launcher
echo ========================================
echo.
echo Starting U3CP Dashboard on Samsung Galaxy J3...
echo.

REM Check if device is connected
echo Checking device connection...
adb devices
echo.

REM Start the dashboard
echo Starting dashboard...
adb shell "cd /sdcard && python3 simple_dashboard.py" &
echo.

REM Wait a moment for the dashboard to start
echo Waiting for dashboard to start...
timeout /t 3 /nobreak > nul

REM Get device IP address
echo Getting device IP address...
for /f "tokens=*" %%i in ('adb shell "ip addr show wlan0 ^| findstr inet"') do (
    echo Found IP: %%i
)

echo.
echo ========================================
echo Dashboard Access Information
echo ========================================
echo.
echo The U3CP dashboard should now be running.
echo.
echo To access the dashboard:
echo 1. Open your web browser
echo 2. Go to: http://localhost:5000
echo 3. Or try: http://[device-ip]:5000
echo.
echo If the dashboard doesn't load:
echo 1. Make sure the device is connected via USB
echo 2. Check that USB Debugging is enabled
echo 3. Try refreshing the browser page
echo.
echo To stop the dashboard:
echo Press Ctrl+C in this window
echo.
echo ========================================
pause 
@echo off
echo ========================================
echo U3CP Native Dashboard Launcher
echo ========================================
echo.
echo Opening U3CP Dashboard on Samsung Galaxy J3...
echo.

REM Check if device is connected
echo Checking device connection...
.\platform-tools\adb.exe devices
echo.

REM Open the dashboard in browser
echo Opening dashboard in browser...
.\platform-tools\adb.exe shell "am start -a android.intent.action.VIEW -d file:///sdcard/native_dashboard.html -t text/html"
echo.

REM Alternative method - copy to browser cache
echo Copying dashboard to browser cache...
.\platform-tools\adb.exe shell "cp /sdcard/native_dashboard.html /sdcard/Download/"
echo.

echo ========================================
echo Dashboard Access Information
echo ========================================
echo.
echo The U3CP dashboard has been opened on your device!
echo.
echo If the browser didn't open automatically:
echo 1. Open your device's web browser
echo 2. Go to: file:///sdcard/native_dashboard.html
echo 3. Or check Downloads folder for native_dashboard.html
echo.
echo Dashboard Features:
echo ✅ Beautiful modern interface
echo ✅ Real-time system monitoring
echo ✅ Network device scanning
echo ✅ Messaging interface
echo ✅ Performance metrics
echo ✅ Responsive design
echo.
echo ========================================
pause 
@echo off
echo ========================================
echo U3CP Dashboard Direct Launcher
echo ========================================
echo.
echo Opening dashboard directly in browser...
echo.

REM Open the dashboard in the device's default browser
.\platform-tools\adb.exe shell "am start -a android.intent.action.VIEW -d file:///sdcard/native_dashboard.html -t text/html"

echo.
echo ========================================
echo Dashboard Access Information
echo ========================================
echo.
echo The U3CP dashboard should now be open in your device's browser!
echo.
echo If the browser didn't open automatically:
echo 1. Open your device's web browser (Chrome, Samsung Internet, etc.)
echo 2. Go to: file:///sdcard/native_dashboard.html
echo 3. Or navigate to: file:///sdcard/u3cp_system/native_dashboard.html
echo.
echo The dashboard features:
echo - Real-time system monitoring
echo - Interactive U3CP controls
echo - Network device discovery
echo - Beautiful modern interface
echo.
pause 
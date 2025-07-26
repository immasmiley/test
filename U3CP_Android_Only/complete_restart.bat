@echo off
echo ========================================
echo U3CP Complete System Restart
echo ========================================
echo.
echo Restarting and completing installation...
echo.

REM Check device connection
echo Checking device connection...
.\platform-tools\adb.exe devices
echo.

REM Restart ADB server
echo Restarting ADB server...
.\platform-tools\adb.exe kill-server
.\platform-tools\adb.exe start-server
timeout /t 3 /nobreak >nul
echo.

REM Check device again
echo Checking device after restart...
.\platform-tools\adb.exe devices
echo.

REM Start Termux
echo Starting Termux...
.\platform-tools\adb.exe shell "am start -n com.termux/.HomeActivity"
timeout /t 3 /nobreak >nul
echo.

REM Install Python properly
echo Installing Python in Termux...
.\platform-tools\adb.exe shell "input text 'pkg update -y'"
.\platform-tools\adb.exe shell "input keyevent 66"
timeout /t 10 /nobreak >nul

.\platform-tools\adb.exe shell "input text 'pkg install python -y'"
.\platform-tools\adb.exe shell "input keyevent 66"
timeout /t 15 /nobreak >nul

.\platform-tools\adb.exe shell "input text 'pkg install python-pip -y'"
.\platform-tools\adb.exe shell "input keyevent 66"
timeout /t 10 /nobreak >nul
echo.

REM Create proper directory structure
echo Creating directory structure...
.\platform-tools\adb.exe shell "mkdir -p /sdcard/u3cp_system"
.\platform-tools\adb.exe shell "chmod 755 /sdcard/u3cp_system"
echo.

REM Copy files to proper location
echo Copying files to proper location...
.\platform-tools\adb.exe shell "cp /sdcard/native_dashboard.html /sdcard/u3cp_system/"
.\platform-tools\adb.exe shell "cp /sdcard/U3CP_Android_Only_App.py /sdcard/u3cp_system/"
.\platform-tools\adb.exe shell "cp /sdcard/U3CP_Android_Only_System.py /sdcard/u3cp_system/"
echo.

REM Create proper launch script
echo Creating launch script...
.\platform-tools\adb.exe shell "echo '#!/data/data/com.termux/files/usr/bin/bash' > /sdcard/u3cp_system/start_u3cp.sh"
.\platform-tools\adb.exe shell "echo 'cd /sdcard/u3cp_system' >> /sdcard/u3cp_system/start_u3cp.sh"
.\platform-tools\adb.exe shell "echo 'python U3CP_Android_Only_App.py' >> /sdcard/u3cp_system/start_u3cp.sh"
.\platform-tools\adb.exe shell "chmod +x /sdcard/u3cp_system/start_u3cp.sh"
echo.

REM Open dashboard in browser
echo Opening dashboard in browser...
.\platform-tools\adb.exe shell "am start -a android.intent.action.VIEW -d file:///sdcard/native_dashboard.html -t text/html"
echo.

echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Your Samsung Galaxy J3 is now fully equipped with:
echo.
echo ✅ Termux Linux environment
echo ✅ Python installed and ready
echo ✅ U3CP system files in /sdcard/u3cp_system/
echo ✅ Beautiful HTML dashboard
echo ✅ Launch scripts created
echo.
echo 🚀 Access Methods:
echo.
echo 1. BROWSER DASHBOARD (RECOMMENDED):
echo    - Should be open now in your browser
echo    - Or go to: file:///sdcard/native_dashboard.html
echo.
echo 2. TERMUX U3CP SYSTEM:
echo    - Open Termux app
echo    - Run: cd /sdcard/u3cp_system && ./start_u3cp.sh
echo.
echo 3. ALTERNATIVE DASHBOARD:
echo    - Go to: file:///sdcard/u3cp_system/native_dashboard.html
echo.
echo The system is now ready for U3CP Android-Only operation!
echo.
pause 
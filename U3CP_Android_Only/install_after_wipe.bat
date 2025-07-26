@echo off
echo ========================================
echo U3CP Android-Only System Installation
echo ========================================
echo.
echo This script will install the U3CP system on your wiped Samsung Galaxy J3
echo.
echo Prerequisites:
echo 1. Phone has been wiped (factory reset completed)
echo 2. USB Debugging is enabled on phone
echo 3. Phone is connected via USB cable
echo 4. You've allowed USB Debugging on the phone
echo.
pause
echo.
echo Checking device connection...
adb devices
echo.
echo If you see your device listed above, press any key to continue...
pause
echo.
echo Installing U3CP system...
echo.
echo Step 1: Installing required packages...
adb shell "pm install -r -d ./android_resources/F-Droid.apk"
adb shell "pm install -r -d ./android_resources/Termux.apk"
echo.
echo Step 2: Pushing U3CP files to device...
adb push U3CP_Android_Only_App.py /sdcard/
adb push U3CP_Android_Only_System.py /sdcard/
adb push requirements_android_only.txt /sdcard/
echo.
echo Step 3: Setting up Termux environment...
adb shell "am start -n com.termux/.HomeActivity"
echo.
echo Step 4: Installing Python dependencies in Termux...
adb shell "su -c 'pkg install python'"
adb shell "su -c 'pip install -r /sdcard/requirements_android_only.txt'"
echo.
echo Step 5: Running U3CP system...
adb shell "su -c 'cd /sdcard && python U3CP_Android_Only_App.py'"
echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo The U3CP Android-Only system is now installed and running on your device.
echo.
echo Features available:
echo - Android-to-Android communication
echo - Nostr relay integration  
echo - SphereOS database
echo - U3CP algorithm processing
echo - Network discovery
echo - Real-time chat
echo - Value discovery
echo.
pause 
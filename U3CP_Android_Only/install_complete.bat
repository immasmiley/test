@echo off
echo U3CP Complete Installation
echo ==========================
echo.
echo This will:
echo 1. Download and install ADB automatically
echo 2. Detect your connected Android device
echo 3. Install F-Droid and Termux
echo 4. Set up the complete U3CP system
echo.
echo Requirements:
echo - Android device connected via USB
echo - USB debugging enabled on your device
echo - Internet connection for ADB download
echo.
echo Press any key to start the installation...
pause >nul
echo.
python setup_adb_and_install.py
echo.
echo Installation complete! Press any key to exit...
pause >nul 
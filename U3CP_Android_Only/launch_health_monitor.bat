@echo off
echo Starting App Health Monitor...
echo This will continuously monitor all apps on your Samsung Galaxy J3
echo.
echo The monitor will:
echo - Check device connection
echo - Monitor F-Droid app installations
echo - Test offline apps functionality
echo - Track system health
echo - Generate reports every 60 seconds
echo.
echo Press Ctrl+C to stop monitoring
echo.
python app_health_monitor.py
pause 
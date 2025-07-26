@echo off
title Automatic Health Monitor - Samsung Galaxy J3
color 0A
cls

echo.
echo ========================================
echo   AUTOMATIC HEALTH MONITOR SERVICE
echo ========================================
echo.
echo This service will run continuously in the background
echo Monitoring your Samsung Galaxy J3 apps automatically
echo.
echo Features:
echo - Continuous monitoring every 30 seconds
echo - Automatic report generation
echo - Device health tracking
echo - Installation progress monitoring
echo - Alert system for issues
echo.
echo Reports will be saved to:
echo - automatic_health_report.txt (human readable)
echo - automatic_health_report.json (detailed data)
echo - current_status.json (latest status)
echo - health_monitor.log (activity log)
echo.
echo Press Ctrl+C to stop the service
echo ========================================
echo.

python automatic_health_monitor.py

echo.
echo Health monitor stopped.
pause 
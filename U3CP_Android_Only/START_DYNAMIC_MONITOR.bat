@echo off
title Dynamic Health Monitor - Samsung Galaxy J3
color 0B
cls

echo.
echo ========================================
echo   DYNAMIC HEALTH MONITOR SERVICE
echo ========================================
echo.
echo This service automatically discovers and monitors
echo ALL apps on your Samsung Galaxy J3
echo.
echo Features:
echo - Automatic app discovery every 5 minutes
echo - Dynamic categorization of new apps
echo - Continuous health monitoring every 30 seconds
echo - Intelligent app functionality testing
echo - Persistent app database
echo - Real-time alerts for new apps
echo.
echo Reports will be saved to:
echo - dynamic_health_report.txt (human readable)
echo - dynamic_health_report.json (detailed data)
echo - dynamic_status.json (latest status)
echo - app_database.json (app catalog)
echo - dynamic_health_monitor.log (activity log)
echo.
echo Press Ctrl+C to stop the service
echo ========================================
echo.

python dynamic_health_monitor.py

echo.
echo Dynamic health monitor stopped.
pause 
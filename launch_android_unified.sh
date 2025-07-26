#!/bin/bash

# SphereOS Android Unified Application Launcher
# Linux/Mac shell script for launching the unified application

echo ""
echo "========================================"
echo "  SphereOS Android Unified Application"
echo "========================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7+ and try again"
    exit 1
fi

echo "Python found. Checking dependencies..."

# Check if Kivy is available
if python3 -c "import kivy" &> /dev/null; then
    echo "Kivy found. Running in GUI mode..."
    GUI_MODE=true
else
    echo "Kivy not found. Running in console mode..."
    GUI_MODE=false
fi

echo ""
echo "Starting SphereOS Android Unified Application..."
echo ""

if [ "$GUI_MODE" = true ]; then
    python3 SphereOS_Android_Unified.py --gui
else
    python3 SphereOS_Android_Unified.py
fi

echo ""
echo "Application closed." 
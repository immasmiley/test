#!/bin/bash
# U3CP Android-Only System Installation Script
# Open Source Only - No Google products required

echo "Installing U3CP Android-Only System..."
echo "Open Source Only - No Google products required"

# Check if Python is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Python not found. Please install Python in Termux:"
    echo "   pkg install python"
    exit 1
fi

echo "Python found: $($PYTHON_CMD --version)"

# Install dependencies
echo "Installing dependencies..."
$PYTHON_CMD -m pip install -r requirements_android_only.txt

# Test installation
echo "Testing installation..."
$PYTHON_CMD test_android_only.py

echo "Installation complete!"
echo "Run: $PYTHON_CMD U3CP_Android_Only_App.py"
echo "Open Source Only - No Google products required"

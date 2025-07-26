#!/system/bin/sh

# F-Droid Python Installation Automation Script
# Run this on your Samsung Galaxy J3

echo "F-Droid Python Installation Automation"
echo "======================================"

# Check if F-Droid is installed
if pm list packages | grep -q fdroid; then
    echo "SUCCESS: F-Droid is installed"
else
    echo "ERROR: F-Droid not found"
    exit 1
fi

# Launch F-Droid
echo "Launching F-Droid..."
am start -n org.fdroid.fdroid/.views.main.MainActivity

# Wait for F-Droid to load
echo "Waiting for F-Droid to load..."
sleep 5

# Try to install Pydroid 3
echo "Attempting to install Pydroid 3..."
am start -a android.intent.action.VIEW -d "fdroid://app/org.pydroid3"

echo "SUCCESS: Automation script completed"
echo "Check F-Droid on your device for installation progress"

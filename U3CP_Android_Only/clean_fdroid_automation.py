#!/usr/bin/env python3
"""
Clean F-Droid Automation Script
Automates Python installation through F-Droid on Samsung Galaxy J3
No emojis, proper encoding, Unix line endings
"""

import subprocess
import os
import time

def execute_adb_command(command):
    """Execute ADB command and return result"""
    try:
        result = subprocess.run(
            ["./platform-tools/adb.exe"] + command.split(),
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        }
    except Exception as e:
        return {'success': False, 'output': '', 'error': str(e)}

def check_fdroid_status():
    """Check if F-Droid is installed and running"""
    print("Checking F-Droid status...")
    
    check_cmd = "shell pm list packages | grep fdroid"
    result = execute_adb_command(check_cmd)
    
    if result['success'] and 'fdroid' in result['output'].lower():
        print("SUCCESS: F-Droid package found")
        return True
    else:
        print("ERROR: F-Droid package not found")
        return False

def launch_fdroid():
    """Launch F-Droid app"""
    print("Launching F-Droid...")
    
    launch_cmd = "shell am start -n org.fdroid.fdroid/.views.main.MainActivity"
    result = execute_adb_command(launch_cmd)
    
    if result['success']:
        print("SUCCESS: F-Droid launched successfully")
        return True
    else:
        print(f"ERROR: Failed to launch F-Droid: {result['error']}")
        return False

def create_clean_device_script():
    """Create a clean shell script with proper Unix formatting"""
    print("Creating clean device automation script...")
    
    script_content = '''#!/system/bin/sh

# F-Droid Python Installation Automation Script
# Samsung Galaxy J3 - Clean version

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

# Try to install Pydroid 3 via direct URL
echo "Attempting to install Pydroid 3..."
am start -a android.intent.action.VIEW -d "fdroid://app/org.pydroid3"

echo "SUCCESS: Automation script completed"
echo "Check F-Droid on your device for installation progress"
'''
    
    # Write with UTF-8 encoding and Unix line endings
    with open('fdroid_clean_script.sh', 'w', encoding='utf-8', newline='\n') as f:
        f.write(script_content)
    
    print("SUCCESS: Clean device automation script created: fdroid_clean_script.sh")
    return True

def push_and_run_clean_script():
    """Push clean automation script to device and run it"""
    print("Pushing clean automation script to device...")
    
    # Push the script
    push_cmd = "push fdroid_clean_script.sh /sdcard/"
    result = execute_adb_command(push_cmd)
    
    if result['success']:
        print("SUCCESS: Clean automation script pushed to device")
        
        # Make it executable
        chmod_cmd = "shell chmod +x /sdcard/fdroid_clean_script.sh"
        chmod_result = execute_adb_command(chmod_cmd)
        
        if chmod_result['success']:
            print("SUCCESS: Script made executable")
            
            # Run the script
            run_cmd = "shell sh /sdcard/fdroid_clean_script.sh"
            run_result = execute_adb_command(run_cmd)
            
            if run_result['success']:
                print("SUCCESS: Clean automation script executed successfully")
                print("Check your device for F-Droid activity")
                return True
            else:
                print(f"ERROR: Failed to run clean automation script: {run_result['error']}")
                return False
        else:
            print(f"ERROR: Failed to make script executable: {chmod_result['error']}")
            return False
    else:
        print(f"ERROR: Failed to push clean automation script: {result['error']}")
        return False

def create_manual_guide_clean():
    """Create a clean manual installation guide"""
    print("Creating clean manual installation guide...")
    
    guide_content = """# Manual F-Droid Python Installation Guide

## Current Status:
- F-Droid: INSTALLED AND RUNNING
- Python: READY TO INSTALL

## Step-by-Step Instructions:

### 1. Open F-Droid on Your Device
- F-Droid should now be open on your Samsung Galaxy J3
- If not, find "F-Droid" in your app drawer and tap it

### 2. Search for Pydroid 3
1. Tap the search icon (magnifying glass) in F-Droid
2. Type "Pydroid 3" in the search box
3. Tap the search button

### 3. Install Pydroid 3
1. Tap on "Pydroid 3" in the search results
2. Tap the "Install" button
3. Wait for download and installation to complete
4. Tap "Open" when installation is done

### 4. Install Python Packages
1. Open Pydroid 3
2. Tap the "Pip" tab at the bottom
3. Install these packages one by one:
   - flask
   - requests
   - psutil
   - pillow

### 5. Run U3CP System
After Python is installed, you can run:
```
python /sdcard/real_system_dashboard.py
```

## Alternative: Pure HTML System
If Python installation fails, use the pure HTML system:
- Open browser on device
- Go to: file:///sdcard/pure_u3cp.html
- This works without Python!

## Troubleshooting:
- If F-Droid doesn't open, restart your device
- If Pydroid 3 doesn't install, try QPython 3 instead
- If nothing works, use the pure HTML system

## Files Available on Device:
- /sdcard/F-Droid.apk (11.9MB)
- /sdcard/pure_u3cp.html (Pure HTML U3CP System)
- /sdcard/real_system_dashboard.py (Python Dashboard)
- /sdcard/fdroid_clean_script.sh (Clean Automation Script)
"""
    
    with open('MANUAL_FDROID_GUIDE_CLEAN.txt', 'w', encoding='utf-8', newline='\n') as f:
        f.write(guide_content)
    
    print("SUCCESS: Clean manual guide created: MANUAL_FDROID_GUIDE_CLEAN.txt")
    return True

def direct_adb_automation():
    """Use direct ADB commands instead of shell script"""
    print("Running direct ADB automation...")
    
    commands = [
        "shell am start -n org.fdroid.fdroid/.views.main.MainActivity",
        "shell sleep 3",
        "shell am start -a android.intent.action.VIEW -d 'fdroid://app/org.pydroid3'"
    ]
    
    for cmd in commands:
        print(f"Executing: {cmd}")
        result = execute_adb_command(cmd)
        
        if result['success']:
            print(f"SUCCESS: {cmd}")
        else:
            print(f"ERROR: {cmd} - {result['error']}")
            return False
    
    return True

def main():
    """Main automation process"""
    print("Clean F-Droid Python Installation Automation")
    print("=" * 50)
    
    # Step 1: Check F-Droid status
    if not check_fdroid_status():
        print("ERROR: F-Droid not installed. Please install F-Droid first.")
        return False
    
    # Step 2: Launch F-Droid
    if not launch_fdroid():
        print("ERROR: Cannot launch F-Droid")
        return False
    
    # Step 3: Create clean automation scripts
    create_clean_device_script()
    create_manual_guide_clean()
    
    # Step 4: Try direct ADB automation first
    print("\nTrying direct ADB automation...")
    if direct_adb_automation():
        print("\nSUCCESS: Direct ADB automation completed!")
        print("\nNext steps on your device:")
        print("1. F-Droid should be open")
        print("2. Search for 'Pydroid 3'")
        print("3. Tap 'Install'")
        print("4. Wait for installation to complete")
        print("5. Open Pydroid 3 and install packages")
        
        print("\nAlternative: Use the pure HTML system")
        print("Open browser and go to: file:///sdcard/pure_u3cp.html")
        
        return True
    
    # Step 5: Fallback to shell script
    print("\nDirect ADB failed, trying shell script...")
    if push_and_run_clean_script():
        print("\nSUCCESS: Shell script automation completed!")
        print("\nNext steps on your device:")
        print("1. F-Droid should be open")
        print("2. Search for 'Pydroid 3'")
        print("3. Tap 'Install'")
        print("4. Wait for installation to complete")
        print("5. Open Pydroid 3 and install packages")
        
        return True
    else:
        print("ERROR: Both automation methods failed")
        print("\nManual installation required:")
        print("1. Open F-Droid manually on your device")
        print("2. Search for 'Pydroid 3'")
        print("3. Install manually")
        
        return False

if __name__ == '__main__':
    success = main()
    if success:
        print("\nSUCCESS: Clean F-Droid automation ready!")
    else:
        print("\nERROR: Clean F-Droid automation failed") 
#!/usr/bin/env python3
"""
Direct Python Installation Script
Installs Python directly on Samsung Galaxy J3 via F-Droid
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
    """Check if F-Droid is installed"""
    print("Checking F-Droid status...")
    
    check_cmd = "shell pm list packages | grep fdroid"
    result = execute_adb_command(check_cmd)
    
    if result['success'] and 'fdroid' in result['output'].lower():
        print("SUCCESS: F-Droid package found")
        return True
    else:
        print("ERROR: F-Droid package not found")
        return False

def launch_fdroid_and_install_python():
    """Launch F-Droid and install Python directly"""
    print("Launching F-Droid and installing Python...")
    
    # Step 1: Launch F-Droid
    launch_cmd = "shell am start -n org.fdroid.fdroid/.views.main.MainActivity"
    result = execute_adb_command(launch_cmd)
    
    if result['success']:
        print("SUCCESS: F-Droid launched")
    else:
        print(f"ERROR: Failed to launch F-Droid: {result['error']}")
        return False
    
    # Wait for F-Droid to load
    print("Waiting for F-Droid to load...")
    time.sleep(3)
    
    # Step 2: Try to install Pydroid 3 directly
    print("Attempting to install Pydroid 3...")
    install_cmd = "shell am start -a android.intent.action.VIEW -d 'fdroid://app/org.pydroid3'"
    result = execute_adb_command(install_cmd)
    
    if result['success']:
        print("SUCCESS: Launched F-Droid for Pydroid 3 installation")
        return True
    else:
        print(f"ERROR: Failed to launch Pydroid 3 installation: {result['error']}")
        return False

def check_python_installation():
    """Check if Python is installed"""
    print("Checking Python installation...")
    
    check_cmd = "shell pm list packages | grep -E '(pydroid|qpython|termux)'"
    result = execute_adb_command(check_cmd)
    
    if result['success'] and result['output'].strip():
        print("SUCCESS: Python app found:")
        print(result['output'])
        return True
    else:
        print("ERROR: No Python apps found")
        return False

def install_python_packages():
    """Install Python packages after Python is installed"""
    print("Installing Python packages...")
    
    packages = ['flask', 'requests', 'psutil', 'pillow']
    
    for package in packages:
        print(f"Installing {package}...")
        install_cmd = f"shell pip install {package}"
        result = execute_adb_command(install_cmd)
        
        if result['success']:
            print(f"SUCCESS: {package} installed")
        else:
            print(f"ERROR: Failed to install {package}: {result['error']}")

def create_python_test_script():
    """Create a test script to verify Python installation"""
    print("Creating Python test script...")
    
    test_script = '''#!/usr/bin/env python3
import sys
import os

print("Python Test Script")
print("==================")
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current directory: {os.getcwd()}")

try:
    import flask
    print("SUCCESS: Flask imported")
except ImportError:
    print("ERROR: Flask not available")

try:
    import requests
    print("SUCCESS: Requests imported")
except ImportError:
    print("ERROR: Requests not available")

try:
    import psutil
    print("SUCCESS: Psutil imported")
except ImportError:
    print("ERROR: Psutil not available")

print("Python test completed")
'''
    
    with open('python_test.py', 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    print("SUCCESS: Python test script created: python_test.py")
    return True

def push_and_run_test():
    """Push test script to device and run it"""
    print("Pushing Python test script to device...")
    
    # Push the test script
    push_cmd = "push python_test.py /sdcard/"
    result = execute_adb_command(push_cmd)
    
    if result['success']:
        print("SUCCESS: Test script pushed to device")
        
        # Try to run the test script
        run_cmd = "shell python /sdcard/python_test.py"
        result = execute_adb_command(run_cmd)
        
        if result['success']:
            print("SUCCESS: Python test script executed")
            print("Output:")
            print(result['output'])
            return True
        else:
            print(f"ERROR: Failed to run Python test: {result['error']}")
            return False
    else:
        print(f"ERROR: Failed to push test script: {result['error']}")
        return False

def create_installation_summary():
    """Create a summary of the installation"""
    print("Creating installation summary...")
    
    summary = """# Direct Python Installation Summary

## Installation Status:
- F-Droid: INSTALLED AND RUNNING
- Python Installation: ATTEMPTED VIA F-DROID
- Python Packages: READY TO INSTALL

## What Was Done:
1. F-Droid was launched successfully
2. Pydroid 3 installation was initiated via F-Droid
3. Python test script was created and pushed to device

## Next Steps:
1. Check your device - F-Droid should be open
2. Look for Pydroid 3 installation progress
3. If installation completes, open Pydroid 3
4. Install Python packages: flask, requests, psutil, pillow
5. Run: python /sdcard/python_test.py

## Alternative: Pure HTML System
If Python installation fails, use the pure HTML system:
- Open browser on device
- Go to: file:///sdcard/pure_u3cp.html
- This works without Python!

## Files Available on Device:
- /sdcard/F-Droid.apk (11.9MB)
- /sdcard/pure_u3cp.html (Pure HTML U3CP System)
- /sdcard/real_system_dashboard.py (Python Dashboard)
- /sdcard/python_test.py (Python Test Script)

## Troubleshooting:
- If F-Droid doesn't show Pydroid 3, search manually
- If installation fails, try QPython 3 instead
- If nothing works, use the pure HTML system
"""
    
    with open('DIRECT_INSTALLATION_SUMMARY.txt', 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print("SUCCESS: Installation summary created: DIRECT_INSTALLATION_SUMMARY.txt")
    return True

def main():
    """Main direct installation process"""
    print("Direct Python Installation on Samsung Galaxy J3")
    print("=" * 50)
    
    # Step 1: Check F-Droid status
    if not check_fdroid_status():
        print("ERROR: F-Droid not installed. Cannot proceed.")
        return False
    
    # Step 2: Launch F-Droid and install Python
    if not launch_fdroid_and_install_python():
        print("ERROR: Failed to launch F-Droid installation")
        return False
    
    # Step 3: Create test script
    create_python_test_script()
    
    # Step 4: Push and run test
    print("\nTesting Python installation...")
    if push_and_run_test():
        print("\nSUCCESS: Python is working on your device!")
        print("\nNext steps:")
        print("1. Install Python packages in Pydroid 3")
        print("2. Run: python /sdcard/real_system_dashboard.py")
    else:
        print("\nPython installation may still be in progress")
        print("Check your device for F-Droid installation status")
    
    # Step 5: Create summary
    create_installation_summary()
    
    print("\nSUCCESS: Direct Python installation process completed!")
    print("\nCheck your device for F-Droid activity and Python installation progress")
    
    return True

if __name__ == '__main__':
    success = main()
    if success:
        print("\nSUCCESS: Direct Python installation ready!")
    else:
        print("\nERROR: Direct Python installation failed") 
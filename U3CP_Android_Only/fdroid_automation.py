#!/usr/bin/env python3
"""
F-Droid Automation Script
Automates Python installation through F-Droid on Samsung Galaxy J3
"""

import subprocess
import os
import time
import json

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
    print("🔍 Checking F-Droid status...")
    
    # Check if F-Droid package is installed
    check_cmd = "shell pm list packages | grep fdroid"
    result = execute_adb_command(check_cmd)
    
    if result['success'] and 'fdroid' in result['output'].lower():
        print("✅ F-Droid package found")
        return True
    else:
        print("❌ F-Droid package not found")
        return False

def launch_fdroid():
    """Launch F-Droid app"""
    print("🚀 Launching F-Droid...")
    
    launch_cmd = "shell am start -n org.fdroid.fdroid/.views.main.MainActivity"
    result = execute_adb_command(launch_cmd)
    
    if result['success']:
        print("✅ F-Droid launched successfully")
        return True
    else:
        print(f"❌ Failed to launch F-Droid: {result['error']}")
        return False

def search_python_apps():
    """Search for Python apps in F-Droid"""
    print("🔍 Searching for Python apps in F-Droid...")
    
    python_apps = [
        {
            'name': 'Pydroid 3',
            'package': 'org.pydroid3',
            'search_term': 'Pydroid 3',
            'description': 'Full Python IDE with package manager'
        },
        {
            'name': 'QPython 3',
            'package': 'org.qpython.qpy3',
            'search_term': 'QPython 3',
            'description': 'Lightweight Python interpreter'
        },
        {
            'name': 'Termux',
            'package': 'com.termux',
            'search_term': 'Termux',
            'description': 'Linux terminal with Python'
        }
    ]
    
    print("📱 Available Python apps to install:")
    for i, app in enumerate(python_apps, 1):
        print(f"{i}. {app['name']} ({app['package']})")
        print(f"   Description: {app['description']}")
    
    return python_apps

def install_python_app(app_package):
    """Install Python app via F-Droid"""
    print(f"📱 Installing {app_package}...")
    
    # Method 1: Try direct F-Droid URL
    fdroid_url = f"fdroid://app/{app_package}"
    install_cmd = f"shell am start -a android.intent.action.VIEW -d '{fdroid_url}'"
    result = execute_adb_command(install_cmd)
    
    if result['success']:
        print(f"✅ Launched F-Droid for {app_package}")
        return True
    else:
        print(f"❌ Failed to launch F-Droid for {app_package}")
        return False

def check_python_installation():
    """Check if Python is installed"""
    print("🔍 Checking Python installation...")
    
    # Check for various Python apps
    python_packages = [
        'org.pydroid3',
        'org.qpython.qpy3', 
        'com.termux',
        'com.hipipal.qpyplus'
    ]
    
    check_cmd = "shell pm list packages | grep -E '(pydroid|qpython|termux)'"
    result = execute_adb_command(check_cmd)
    
    if result['success'] and result['output'].strip():
        print("✅ Python app found:")
        print(result['output'])
        return True
    else:
        print("❌ No Python apps found")
        return False

def create_automation_script():
    """Create a script that can be run on the device"""
    print("📝 Creating device automation script...")
    
    script_content = '''#!/bin/bash
# F-Droid Python Installation Automation Script
# Run this on your Samsung Galaxy J3

echo "🚀 F-Droid Python Installation Automation"
echo "========================================"

# Check if F-Droid is installed
if pm list packages | grep -q fdroid; then
    echo "✅ F-Droid is installed"
else
    echo "❌ F-Droid not found"
    exit 1
fi

# Launch F-Droid
echo "🚀 Launching F-Droid..."
am start -n org.fdroid.fdroid/.views.main.MainActivity

# Wait for F-Droid to load
echo "⏳ Waiting for F-Droid to load..."
sleep 5

# Search for Python apps
echo "🔍 Searching for Python apps..."
echo "Available Python apps:"
echo "1. Pydroid 3 (org.pydroid3)"
echo "2. QPython 3 (org.qpython.qpy3)"
echo "3. Termux (com.termux)"

# Try to install Pydroid 3
echo "📱 Attempting to install Pydroid 3..."
am start -a android.intent.action.VIEW -d "fdroid://app/org.pydroid3"

echo "✅ Automation script completed"
echo "📱 Check F-Droid on your device for installation progress"
'''
    
    with open('fdroid_automation.sh', 'w') as f:
        f.write(script_content)
    
    print("✅ Device automation script created: fdroid_automation.sh")
    return True

def push_and_run_automation():
    """Push automation script to device and run it"""
    print("📤 Pushing automation script to device...")
    
    # Push the script
    push_cmd = "push fdroid_automation.sh /sdcard/"
    result = execute_adb_command(push_cmd)
    
    if result['success']:
        print("✅ Automation script pushed to device")
        
        # Make it executable
        chmod_cmd = "shell chmod +x /sdcard/fdroid_automation.sh"
        chmod_result = execute_adb_command(chmod_cmd)
        
        if chmod_result['success']:
            print("✅ Script made executable")
            
            # Run the script
            run_cmd = "shell sh /sdcard/fdroid_automation.sh"
            run_result = execute_adb_command(run_cmd)
            
            if run_result['success']:
                print("✅ Automation script executed successfully")
                print("📱 Check your device for F-Droid activity")
                return True
            else:
                print(f"❌ Failed to run automation script: {run_result['error']}")
                return False
        else:
            print(f"❌ Failed to make script executable: {chmod_result['error']}")
            return False
    else:
        print(f"❌ Failed to push automation script: {result['error']}")
        return False

def create_interactive_installer():
    """Create an interactive installer that guides the user"""
    print("📝 Creating interactive installer...")
    
    installer_content = '''#!/usr/bin/env python3
"""
Interactive F-Droid Python Installer
Run this on your desktop to guide F-Droid installation
"""

import subprocess
import time

def execute_adb(command):
    try:
        result = subprocess.run(
            ["./platform-tools/adb.exe"] + command.split(),
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🚀 Interactive F-Droid Python Installer")
    print("=" * 50)
    
    # Step 1: Check F-Droid
    print("\\nStep 1: Checking F-Droid installation...")
    success, output, error = execute_adb("shell pm list packages | grep fdroid")
    
    if success and "fdroid" in output.lower():
        print("✅ F-Droid is installed")
    else:
        print("❌ F-Droid not found. Please install F-Droid first.")
        return
    
    # Step 2: Launch F-Droid
    print("\\nStep 2: Launching F-Droid...")
    success, output, error = execute_adb("shell am start -n org.fdroid.fdroid/.views.main.MainActivity")
    
    if success:
        print("✅ F-Droid launched")
    else:
        print("❌ Failed to launch F-Droid")
        return
    
    # Step 3: Guide user through installation
    print("\\nStep 3: Installation Guide")
    print("📱 On your device:")
    print("1. F-Droid should now be open")
    print("2. Tap the search icon (magnifying glass)")
    print("3. Type 'Pydroid 3' and search")
    print("4. Tap on 'Pydroid 3' in results")
    print("5. Tap 'Install' button")
    print("6. Wait for download and installation")
    print("7. Tap 'Open' when done")
    
    input("\\nPress Enter when you've completed the installation...")
    
    # Step 4: Verify installation
    print("\\nStep 4: Verifying Python installation...")
    success, output, error = execute_adb("shell pm list packages | grep pydroid")
    
    if success and "pydroid" in output.lower():
        print("✅ Pydroid 3 installed successfully!")
        print("\\n🎉 Python is now ready on your device!")
        print("\\nNext steps:")
        print("1. Open Pydroid 3 on your device")
        print("2. Go to 'Pip' tab")
        print("3. Install: flask, requests, psutil, pillow")
        print("4. Run: python /sdcard/real_system_dashboard.py")
    else:
        print("❌ Pydroid 3 not found. Please try installing manually.")
        print("\\nAlternative: Use the pure HTML system:")
        print("Open browser and go to: file:///sdcard/pure_u3cp.html")

if __name__ == "__main__":
    main()
'''
    
    with open('interactive_fdroid_installer.py', 'w') as f:
        f.write(installer_content)
    
    print("✅ Interactive installer created: interactive_fdroid_installer.py")
    return True

def main():
    """Main automation process"""
    print("🚀 F-Droid Python Installation Automation")
    print("=" * 50)
    
    # Step 1: Check F-Droid status
    if not check_fdroid_status():
        print("❌ F-Droid not installed. Please install F-Droid first.")
        return False
    
    # Step 2: Launch F-Droid
    if not launch_fdroid():
        print("❌ Cannot launch F-Droid")
        return False
    
    # Step 3: Show available Python apps
    python_apps = search_python_apps()
    
    # Step 4: Create automation scripts
    create_automation_script()
    create_interactive_installer()
    
    # Step 5: Push and run automation
    print("\n📱 Running automation on device...")
    if push_and_run_automation():
        print("\n🎉 F-Droid automation completed!")
        print("\n📱 Next steps on your device:")
        print("1. F-Droid should be open")
        print("2. Search for 'Pydroid 3'")
        print("3. Tap 'Install'")
        print("4. Wait for installation to complete")
        print("5. Open Pydroid 3 and install packages")
        
        print("\n🔄 Alternative: Run interactive installer")
        print("python interactive_fdroid_installer.py")
        
        return True
    else:
        print("❌ Automation failed")
        return False

if __name__ == '__main__':
    success = main()
    if success:
        print("\n✅ F-Droid automation ready!")
    else:
        print("\n❌ F-Droid automation failed") 
#!/usr/bin/env python3
"""
Install F-Droid First Strategy
F-Droid → Python → U3CP System
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

def download_fdroid_apk():
    """Download F-Droid APK from official source"""
    print("📥 Downloading F-Droid APK...")
    
    # Download F-Droid from official source
    download_cmd = "shell wget -O /sdcard/fdroid.apk https://f-droid.org/F-Droid.apk"
    result = execute_adb_command(download_cmd)
    
    if result['success']:
        print("✅ F-Droid APK downloaded successfully")
        return True
    else:
        print(f"❌ Failed to download F-Droid: {result['error']}")
        return False

def install_fdroid():
    """Install F-Droid APK"""
    print("📱 Installing F-Droid...")
    
    install_cmd = "install /sdcard/fdroid.apk"
    result = execute_adb_command(install_cmd)
    
    if result['success']:
        print("✅ F-Droid installed successfully")
        return True
    else:
        print(f"❌ Failed to install F-Droid: {result['error']}")
        return False

def verify_fdroid_installation():
    """Verify F-Droid is installed and accessible"""
    print("🔍 Verifying F-Droid installation...")
    
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
    
    launch_cmd = "shell am start -n org.fdroid.fdroid/.MainActivity"
    result = execute_adb_command(launch_cmd)
    
    if result['success']:
        print("✅ F-Droid launched successfully")
        return True
    else:
        print(f"❌ Failed to launch F-Droid: {result['error']}")
        return False

def install_python_via_fdroid():
    """Install Python through F-Droid"""
    print("🐍 Installing Python via F-Droid...")
    
    # F-Droid has several Python apps available
    python_apps = [
        "org.qpython.qpy3",  # QPython 3
        "com.hipipal.qpyplus",  # QPython+
        "org.pydroid3",  # Pydroid 3
        "com.chaquo.python"  # Chaquopy
    ]
    
    for app in python_apps:
        print(f"📱 Attempting to install {app}...")
        
        # Try to install via F-Droid
        install_cmd = f"shell am start -a android.intent.action.VIEW -d fdroid://app/{app}"
        result = execute_adb_command(install_cmd)
        
        if result['success']:
            print(f"✅ Launched F-Droid for {app}")
            time.sleep(5)  # Give time for F-Droid to process
            break
        else:
            print(f"❌ Failed to launch F-Droid for {app}")

def create_fdroid_installation_guide():
    """Create a guide for manual F-Droid installation"""
    print("📝 Creating F-Droid installation guide...")
    
    guide_content = """
# F-Droid Installation Guide for Samsung Galaxy J3

## Step 1: Install F-Droid
1. Open your device's browser
2. Go to: https://f-droid.org/
3. Download the F-Droid APK
4. Install the APK (allow unknown sources if needed)

## Step 2: Install Python Apps
Once F-Droid is installed, search for and install:
- **Pydroid 3** (Python IDE with packages)
- **QPython 3** (Python interpreter)
- **Termux** (Linux terminal)

## Step 3: Install Python Packages
In Pydroid 3 or Termux, install:
```
pip install flask
pip install requests
pip install psutil
pip install pillow
```

## Step 4: Run U3CP System
After Python is installed, you can run:
```
python /sdcard/real_system_dashboard.py
```

## Alternative: Manual APK Installation
If F-Droid doesn't work, download these APKs directly:
- Pydroid 3: https://play.google.com/store/apps/details?id=org.pydroid3
- Termux: https://f-droid.org/packages/com.termux/
"""
    
    with open('FDROID_INSTALLATION_GUIDE.txt', 'w') as f:
        f.write(guide_content)
    
    print("✅ Installation guide created: FDROID_INSTALLATION_GUIDE.txt")

def push_installation_files():
    """Push all necessary files to device"""
    print("📤 Pushing installation files to device...")
    
    files_to_push = [
        'real_system_dashboard.py',
        'unified_u3cp_system.py',
        'pure_html_u3cp.html',
        'FDROID_INSTALLATION_GUIDE.txt'
    ]
    
    for file in files_to_push:
        if os.path.exists(file):
            push_cmd = f"push {file} /sdcard/"
            result = execute_adb_command(push_cmd)
            
            if result['success']:
                print(f"✅ Pushed {file}")
            else:
                print(f"❌ Failed to push {file}: {result['error']}")

def main():
    """Main F-Droid installation process"""
    print("🚀 F-Droid First Installation Strategy")
    print("=" * 50)
    print("Strategy: F-Droid → Python → U3CP System")
    print()
    
    # Step 1: Download F-Droid
    if not download_fdroid_apk():
        print("❌ Cannot proceed without F-Droid APK")
        create_fdroid_installation_guide()
        return False
    
    # Step 2: Install F-Droid
    if not install_fdroid():
        print("❌ Cannot proceed without F-Droid installation")
        create_fdroid_installation_guide()
        return False
    
    # Step 3: Verify F-Droid
    if not verify_fdroid_installation():
        print("❌ F-Droid installation verification failed")
        create_fdroid_installation_guide()
        return False
    
    # Step 4: Launch F-Droid
    if not launch_fdroid():
        print("⚠️ F-Droid launch failed, but installation may still work")
    
    # Step 5: Install Python via F-Droid
    install_python_via_fdroid()
    
    # Step 6: Create installation guide
    create_fdroid_installation_guide()
    
    # Step 7: Push files
    push_installation_files()
    
    print("\n🎉 F-Droid installation completed!")
    print("📱 Next steps:")
    print("1. Open F-Droid on your device")
    print("2. Search for 'Python' or 'Pydroid'")
    print("3. Install Pydroid 3 or QPython 3")
    print("4. Install required packages")
    print("5. Run: python /sdcard/real_system_dashboard.py")
    
    return True

if __name__ == '__main__':
    success = main()
    if success:
        print("\n✅ F-Droid strategy ready!")
    else:
        print("\n❌ F-Droid installation failed - see guide above") 
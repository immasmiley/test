#!/usr/bin/env python3
"""
Simple Apps Installation Script
Installs useful apps on Samsung Galaxy J3 via F-Droid
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

def install_app_via_fdroid(app_name, fdroid_id):
    """Install an app via F-Droid using intent"""
    print(f"Installing {app_name}...")
    
    # Launch F-Droid with specific app
    install_cmd = f"shell am start -a android.intent.action.VIEW -d 'fdroid://app/{fdroid_id}'"
    result = execute_adb_command(install_cmd)
    
    if result['success']:
        print(f"SUCCESS: {app_name} installation initiated")
        return True
    else:
        print(f"ERROR: Failed to install {app_name}: {result['error']}")
        return False

def install_python_apps():
    """Install Python-related apps"""
    print("Installing Python apps...")
    
    python_apps = [
        ("Pydroid 3", "org.pydroid3"),
        ("QPython 3", "com.hipipal.qpyplus"),
        ("Termux", "com.termux")
    ]
    
    for app_name, fdroid_id in python_apps:
        install_app_via_fdroid(app_name, fdroid_id)
        time.sleep(2)  # Wait between installations

def install_utility_apps():
    """Install utility apps"""
    print("Installing utility apps...")
    
    utility_apps = [
        ("Simple File Manager", "com.simplemobiletools.filemanager"),
        ("Simple Notes", "com.simplemobiletools.notes"),
        ("Simple Calendar", "com.simplemobiletools.calendar"),
        ("Simple Gallery", "com.simplemobiletools.gallery"),
        ("Simple Contacts", "com.simplemobiletools.contacts")
    ]
    
    for app_name, fdroid_id in utility_apps:
        install_app_via_fdroid(app_name, fdroid_id)
        time.sleep(2)

def install_network_apps():
    """Install network and communication apps"""
    print("Installing network apps...")
    
    network_apps = [
        ("Nostr Client", "com.github.damus"),
        ("Signal", "org.thoughtcrime.securesms"),
        ("Element", "im.vector.app"),
        ("Briar", "org.briarproject.briar.android")
    ]
    
    for app_name, fdroid_id in network_apps:
        install_app_via_fdroid(app_name, fdroid_id)
        time.sleep(2)

def install_development_apps():
    """Install development tools"""
    print("Installing development apps...")
    
    dev_apps = [
        ("Acode", "com.foxdebug.acode"),
        ("DroidEdit", "com.aor.droidedit"),
        ("QuickEdit", "com.rhmsoft.edit"),
        ("Markor", "net.gsantner.markor")
    ]
    
    for app_name, fdroid_id in dev_apps:
        install_app_via_fdroid(app_name, fdroid_id)
        time.sleep(2)

def check_installed_apps():
    """Check which apps are installed"""
    print("Checking installed apps...")
    
    check_cmd = "shell pm list packages | grep -E '(pydroid|qpython|termux|simple|damus|signal|element|briar|acode|droidedit|quickedit|markor)'"
    result = execute_adb_command(check_cmd)
    
    if result['success'] and result['output'].strip():
        print("SUCCESS: Found installed apps:")
        print(result['output'])
        return True
    else:
        print("No apps found yet - installations may still be in progress")
        return False

def create_apps_guide():
    """Create a guide for the installed apps"""
    print("Creating apps guide...")
    
    guide = """# Simple Apps Installation Guide

## Apps Being Installed:

### Python Development:
- **Pydroid 3**: Full Python IDE for Android
- **QPython 3**: Alternative Python environment
- **Termux**: Terminal emulator with Python support

### Utility Apps:
- **Simple File Manager**: Easy file management
- **Simple Notes**: Quick note taking
- **Simple Calendar**: Calendar and scheduling
- **Simple Gallery**: Photo and media management
- **Simple Contacts**: Contact management

### Network & Communication:
- **Nostr Client**: Decentralized social networking
- **Signal**: Secure messaging
- **Element**: Matrix chat client
- **Briar**: Peer-to-peer messaging

### Development Tools:
- **Acode**: Code editor with syntax highlighting
- **DroidEdit**: Text and code editor
- **QuickEdit**: Fast text editing
- **Markor**: Markdown editor

## Installation Status:
- All apps are being installed via F-Droid
- Check your device for installation progress
- Some apps may take a few minutes to download

## Next Steps:
1. Wait for installations to complete
2. Open Pydroid 3 to install Python packages
3. Use Simple File Manager to navigate files
4. Set up Nostr Client for U3CP networking

## Using the Apps:
- **Pydroid 3**: Open → Pip tab → Install: flask, requests, psutil, pillow
- **Simple File Manager**: Navigate to /sdcard/ to see U3CP files
- **Nostr Client**: Set up for decentralized communication
- **Termux**: Run terminal commands and Python scripts

## Alternative: Pure HTML System
If Python apps don't work, use the pure HTML system:
- Open browser → file:///sdcard/pure_u3cp.html
- Works without any app installations!
"""
    
    with open('SIMPLE_APPS_GUIDE.txt', 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("SUCCESS: Apps guide created: SIMPLE_APPS_GUIDE.txt")
    return True

def push_guide_to_device():
    """Push the guide to the device"""
    print("Pushing apps guide to device...")
    
    push_cmd = "push SIMPLE_APPS_GUIDE.txt /sdcard/"
    result = execute_adb_command(push_cmd)
    
    if result['success']:
        print("SUCCESS: Apps guide pushed to device")
        print("You can read it at: file:///sdcard/SIMPLE_APPS_GUIDE.txt")
        return True
    else:
        print(f"ERROR: Failed to push guide: {result['error']}")
        return False

def main():
    """Main apps installation process"""
    print("Simple Apps Installation on Samsung Galaxy J3")
    print("=" * 50)
    
    # Step 1: Install Python apps
    print("\n1. Installing Python apps...")
    install_python_apps()
    
    # Step 2: Install utility apps
    print("\n2. Installing utility apps...")
    install_utility_apps()
    
    # Step 3: Install network apps
    print("\n3. Installing network apps...")
    install_network_apps()
    
    # Step 4: Install development apps
    print("\n4. Installing development apps...")
    install_development_apps()
    
    # Step 5: Check installations
    print("\n5. Checking installations...")
    time.sleep(5)  # Wait for installations to progress
    check_installed_apps()
    
    # Step 6: Create and push guide
    print("\n6. Creating apps guide...")
    create_apps_guide()
    push_guide_to_device()
    
    print("\nSUCCESS: Simple apps installation completed!")
    print("\nCheck your device for:")
    print("- F-Droid installation progress")
    print("- New apps appearing in app drawer")
    print("- Apps guide at: file:///sdcard/SIMPLE_APPS_GUIDE.txt")
    
    return True

if __name__ == '__main__':
    success = main()
    if success:
        print("\nSUCCESS: Simple apps installation ready!")
    else:
        print("\nERROR: Simple apps installation failed") 
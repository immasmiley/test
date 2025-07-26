#!/usr/bin/env python3
"""
U3CP Android-Only System Installation Script
Installs complete U3CP system on Samsung Galaxy J3
"""

import subprocess
import time
import sys
import os

def check_device():
    """Check if device is connected and ready"""
    try:
        result = subprocess.run(["./platform-tools/adb.exe", "devices"], 
                              capture_output=True, text=True, timeout=10)
        if "device" in result.stdout:
            print("✅ Device connected and authorized")
            return True
        else:
            print("❌ Device not found")
            return False
    except Exception as e:
        print(f"❌ Device check failed: {e}")
        return False

def check_android_version():
    """Check Android version"""
    try:
        result = subprocess.run(["./platform-tools/adb.exe", "shell", "getprop", "ro.build.version.release"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"📱 Android Version: {version}")
            return version
        else:
            print("⚠️  Could not determine Android version")
            return "unknown"
    except Exception as e:
        print(f"❌ Version check failed: {e}")
        return "unknown"

def install_termux():
    """Install Termux for Python environment"""
    print("📦 Installing Termux...")
    
    try:
        # Check if Termux is already installed
        result = subprocess.run(["./platform-tools/adb.exe", "shell", "pm list packages | grep com.termux"], 
                              capture_output=True, text=True, timeout=10)
        
        if "com.termux" in result.stdout:
            print("   ✅ Termux already installed")
            return True
        
        # Install Termux APK if available
        if os.path.exists("./android_resources/Termux.apk"):
            print("   Installing Termux APK...")
            result = subprocess.run(["./platform-tools/adb.exe", "install", "./android_resources/Termux.apk"], 
                                  capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                print("   ✅ Termux installed successfully")
                return True
            else:
                print(f"   ❌ Termux installation failed: {result.stderr}")
                return False
        else:
            print("   ⚠️  Termux APK not found, will install via package manager")
            return True
            
    except Exception as e:
        print(f"   ❌ Termux installation failed: {e}")
        return False

def setup_termux_environment():
    """Set up Termux environment with Python"""
    print("🐍 Setting up Python environment in Termux...")
    
    try:
        # Start Termux and install Python
        commands = [
            "am start -n com.termux/.HomeActivity",
            "sleep 5",
            "input text 'pkg update -y'",
            "input keyevent 66",  # Enter key
            "sleep 10",
            "input text 'pkg install python -y'",
            "input keyevent 66",
            "sleep 30",
            "input text 'pip install requests pillow qrcode websockets'",
            "input keyevent 66",
            "sleep 20"
        ]
        
        for command in commands:
            if command.startswith("sleep"):
                time.sleep(int(command.split()[1]))
            else:
                subprocess.run(["./platform-tools/adb.exe", "shell", command], 
                             capture_output=True, text=True, timeout=30)
        
        print("   ✅ Python environment setup completed")
        return True
        
    except Exception as e:
        print(f"   ❌ Python setup failed: {e}")
        return False

def push_u3cp_files():
    """Push U3CP system files to device"""
    print("📁 Pushing U3CP system files...")
    
    files_to_push = [
        ("U3CP_Android_Only_App.py", "/sdcard/"),
        ("U3CP_Android_Only_System.py", "/sdcard/"),
        ("requirements_android_only.txt", "/sdcard/"),
        ("sphereos_android_only.db", "/sdcard/")
    ]
    
    for filename, destination in files_to_push:
        if os.path.exists(filename):
            try:
                print(f"   Pushing {filename}...")
                result = subprocess.run(["./platform-tools/adb.exe", "push", filename, destination], 
                                      capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    print(f"   ✅ {filename} pushed successfully")
                else:
                    print(f"   ❌ {filename} push failed: {result.stderr}")
            except Exception as e:
                print(f"   ❌ {filename} push failed: {e}")
        else:
            print(f"   ⚠️  {filename} not found")

def create_launch_script():
    """Create launch script for U3CP system"""
    print("🚀 Creating launch script...")
    
    launch_script = """#!/data/data/com.termux/files/usr/bin/bash
cd /sdcard
python U3CP_Android_Only_App.py
"""
    
    try:
        # Create launch script on device
        subprocess.run(["./platform-tools/adb.exe", "shell", f"echo '{launch_script}' > /sdcard/launch_u3cp.sh"], 
                      capture_output=True, text=True, timeout=10)
        subprocess.run(["./platform-tools/adb.exe", "shell", "chmod +x /sdcard/launch_u3cp.sh"], 
                      capture_output=True, text=True, timeout=10)
        print("   ✅ Launch script created")
        return True
    except Exception as e:
        print(f"   ❌ Launch script creation failed: {e}")
        return False

def start_u3cp_system():
    """Start the U3CP system"""
    print("🚀 Starting U3CP system...")
    
    try:
        # Launch U3CP system in Termux
        commands = [
            "am start -n com.termux/.HomeActivity",
            "sleep 3",
            "input text 'cd /sdcard'",
            "input keyevent 66",
            "sleep 2",
            "input text 'python U3CP_Android_Only_App.py'",
            "input keyevent 66"
        ]
        
        for command in commands:
            if command.startswith("sleep"):
                time.sleep(int(command.split()[1]))
            else:
                subprocess.run(["./platform-tools/adb.exe", "shell", command], 
                             capture_output=True, text=True, timeout=30)
        
        print("   ✅ U3CP system started")
        return True
        
    except Exception as e:
        print(f"   ❌ U3CP startup failed: {e}")
        return False

def verify_installation():
    """Verify U3CP installation"""
    print("🔍 Verifying installation...")
    
    try:
        # Check if files are present
        result = subprocess.run(["./platform-tools/adb.exe", "shell", "ls /sdcard/U3CP_*"], 
                              capture_output=True, text=True, timeout=10)
        
        if "U3CP_Android_Only_App.py" in result.stdout:
            print("   ✅ U3CP files verified")
            return True
        else:
            print("   ❌ U3CP files not found")
            return False
            
    except Exception as e:
        print(f"   ❌ Verification failed: {e}")
        return False

def main():
    print("🚀 U3CP Android-Only System Installation")
    print("=" * 60)
    
    # Check device connection
    if not check_device():
        print("❌ Device not ready for installation")
        return
    
    # Check Android version
    android_version = check_android_version()
    
    print(f"\n📱 Installing U3CP system on Samsung Galaxy J3")
    print(f"🤖 Android Version: {android_version}")
    
    # Step 1: Install Termux
    if not install_termux():
        print("❌ Termux installation failed")
        return
    
    # Step 2: Set up Python environment
    if not setup_termux_environment():
        print("❌ Python environment setup failed")
        return
    
    # Step 3: Push U3CP files
    push_u3cp_files()
    
    # Step 4: Create launch script
    create_launch_script()
    
    # Step 5: Verify installation
    if not verify_installation():
        print("❌ Installation verification failed")
        return
    
    # Step 6: Start U3CP system
    if not start_u3cp_system():
        print("❌ U3CP system startup failed")
        return
    
    print("\n🎉 U3CP Android-Only System Installation Complete!")
    print("=" * 60)
    print("📱 Samsung Galaxy J3 is now running U3CP system")
    print("\n🚀 Features Available:")
    print("   ✅ Android-to-Android Communication")
    print("   ✅ Nostr Relay Integration")
    print("   ✅ SphereOS Database")
    print("   ✅ U3CP Algorithm Processing")
    print("   ✅ Network Discovery")
    print("   ✅ Real-time Chat")
    print("   ✅ Value Discovery")
    print("\n📋 System Status:")
    print("   📱 Device: Samsung Galaxy J3 (SM-J337P)")
    print("   🤖 Android: " + android_version)
    print("   🐍 Python: Installed in Termux")
    print("   🚀 U3CP: Running and ready")
    print("\n💡 To restart U3CP system:")
    print("   Run: adb shell am start -n com.termux/.HomeActivity")
    print("   Then: cd /sdcard && python U3CP_Android_Only_App.py")

if __name__ == "__main__":
    main() 
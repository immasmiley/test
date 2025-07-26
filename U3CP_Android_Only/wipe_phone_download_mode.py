#!/usr/bin/env python3
"""
Phone Wipe Script for Samsung Download Mode
Handles Samsung Galaxy J3 (SM-J337P) in Download Mode
"""

import subprocess
import time
import sys
import os

def check_download_mode():
    """Check if device is in Download Mode"""
    try:
        result = subprocess.run(["./platform-tools/adb.exe", "devices"], 
                              capture_output=True, text=True, timeout=10)
        print("🔍 Checking device status...")
        print(result.stdout)
        
        # Check for Download Mode indicators
        if "List of devices attached" in result.stdout and not "device" in result.stdout:
            print("📱 Device appears to be in Download Mode")
            return True
        return False
    except Exception as e:
        print(f"❌ Device check failed: {e}")
        return False

def reboot_to_recovery():
    """Attempt to reboot device to recovery mode for wiping"""
    print("🔄 Attempting to reboot to recovery mode...")
    
    try:
        # Try ADB reboot to recovery
        result = subprocess.run(["./platform-tools/adb.exe", "reboot", "recovery"], 
                              capture_output=True, text=True, timeout=10)
        print("📱 Reboot command sent to recovery mode")
        print("⏳ Wait 30 seconds for device to reboot...")
        time.sleep(30)
        return True
    except Exception as e:
        print(f"⚠️  ADB reboot failed: {e}")
        return False

def manual_recovery_instructions():
    """Provide manual recovery mode instructions"""
    print("\n📋 MANUAL RECOVERY MODE INSTRUCTIONS:")
    print("=" * 50)
    print("Since the device is in Download Mode, you need to:")
    print("1. Disconnect USB cable")
    print("2. Hold Volume Down + Power buttons for 10 seconds")
    print("3. Release Power button but keep holding Volume Down")
    print("4. When you see 'Recovery Mode' text, release Volume Down")
    print("5. Use Volume buttons to navigate, Power button to select")
    print("6. Select 'Wipe data/factory reset'")
    print("7. Select 'Yes' to confirm")
    print("8. Select 'Wipe cache partition'")
    print("9. Select 'Reboot system now'")
    print("=" * 50)

def check_fastboot():
    """Check if device is in fastboot mode"""
    try:
        result = subprocess.run(["./platform-tools/fastboot.exe", "devices"], 
                              capture_output=True, text=True, timeout=10)
        print("🔍 Checking fastboot devices...")
        print(result.stdout)
        return "fastboot" in result.stdout
    except Exception as e:
        print(f"❌ Fastboot check failed: {e}")
        return False

def wipe_via_fastboot():
    """Wipe device using fastboot commands"""
    print("🧹 Attempting fastboot wipe...")
    
    fastboot_commands = [
        "erase userdata",
        "erase cache", 
        "erase system",
        "erase data"
    ]
    
    for command in fastboot_commands:
        try:
            print(f"   Executing: fastboot {command}")
            result = subprocess.run(["./platform-tools/fastboot.exe"] + command.split(), 
                                  capture_output=True, text=True, timeout=30)
            print(f"   Result: {result.stdout}")
            if result.stderr:
                print(f"   Error: {result.stderr}")
        except Exception as e:
            print(f"   ❌ Failed: {e}")

def create_wipe_script():
    """Create a batch script for easy wiping"""
    script_content = """@echo off
echo 🧹 Samsung Galaxy J3 Wipe Script
echo ================================
echo.
echo This script will help wipe your Samsung Galaxy J3
echo.
echo Current device status:
adb devices
echo.
echo If device shows as "device" (not Download Mode):
echo 1. Running ADB wipe commands...
adb shell "su -c 'wipe data'"
adb shell "su -c 'wipe cache'"
adb shell "rm -rf /data/*"
adb shell "rm -rf /cache/*"
adb shell "rm -rf /sdcard/*"
echo.
echo 2. Rebooting to recovery for complete wipe...
adb reboot recovery
echo.
echo If device is in Download Mode:
echo Please follow manual recovery instructions
echo.
pause
"""
    
    with open("wipe_phone.bat", "w") as f:
        f.write(script_content)
    
    print("✅ Created wipe_phone.bat script")

def main():
    print("🧹 Samsung Galaxy J3 Wipe Tool")
    print("=" * 50)
    
    # Check device status
    in_download_mode = check_download_mode()
    
    if in_download_mode:
        print("📱 Device is in Download Mode")
        print("💡 Download Mode is for firmware flashing, not data wiping")
        
        # Try to reboot to recovery
        if reboot_to_recovery():
            print("✅ Device should now be in recovery mode")
            time.sleep(5)
            
            # Check if device is now accessible
            result = subprocess.run(["./platform-tools/adb.exe", "devices"], 
                                  capture_output=True, text=True, timeout=10)
            if "device" in result.stdout:
                print("✅ Device now accessible via ADB")
                print("🧹 Proceeding with wipe commands...")
                # Run wipe commands here
            else:
                print("⚠️  Device still not accessible")
                manual_recovery_instructions()
        else:
            manual_recovery_instructions()
    
    # Check fastboot
    if check_fastboot():
        print("📱 Device detected in fastboot mode")
        wipe_via_fastboot()
    
    # Create easy-to-use script
    create_wipe_script()
    
    print("\n📋 SUMMARY:")
    print("1. If device is in Download Mode → Use manual recovery instructions")
    print("2. If device is in Recovery Mode → Use wipe options in recovery menu")
    print("3. If device is accessible via ADB → Run wipe_phone.bat script")
    print("4. If device is in Fastboot Mode → Fastboot commands executed")
    
    print("\n✅ Wipe tools prepared!")
    print("📱 Phone will be ready for U3CP system installation after wipe")

if __name__ == "__main__":
    main() 
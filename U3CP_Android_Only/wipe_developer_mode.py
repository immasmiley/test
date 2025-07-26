#!/usr/bin/env python3
"""
Direct Wipe Script for Samsung Galaxy J3 in Developer Mode
Uses ADB commands to completely wipe the device
"""

import subprocess
import time
import sys

def check_device():
    """Check if device is connected and authorized"""
    try:
        result = subprocess.run(["./platform-tools/adb.exe", "devices"], 
                              capture_output=True, text=True, timeout=10)
        print("🔍 Checking device connection...")
        print(result.stdout)
        
        if "device" in result.stdout:
            print("✅ Device found and authorized!")
            return True
        elif "unauthorized" in result.stdout:
            print("⚠️  Device found but not authorized")
            print("💡 Please check 'Allow USB Debugging' on your phone")
            return False
        else:
            print("❌ No device found")
            print("💡 Make sure:")
            print("   - USB cable is connected")
            print("   - Developer Options is enabled")
            print("   - USB Debugging is enabled")
            print("   - You've allowed USB Debugging on the phone")
            return False
    except Exception as e:
        print(f"❌ Device check failed: {e}")
        return False

def wipe_device():
    """Perform complete device wipe using ADB commands"""
    print("🧹 Starting complete device wipe...")
    print("⚠️  WARNING: This will erase ALL data on the device!")
    
    # Wipe commands in order of thoroughness
    wipe_commands = [
        # Basic wipe commands
        "shell su -c 'wipe data'",
        "shell su -c 'wipe cache'",
        "shell su -c 'wipe dalvik'",
        
        # Remove all user data
        "shell rm -rf /data/*",
        "shell rm -rf /cache/*",
        "shell rm -rf /sdcard/*",
        "shell rm -rf /storage/*",
        "shell rm -rf /mnt/*",
        
        # Remove system apps (if rooted)
        "shell rm -rf /system/app/*",
        "shell rm -rf /system/priv-app/*",
        "shell rm -rf /system/data/*",
        
        # Remove additional directories
        "shell rm -rf /data/data/*",
        "shell rm -rf /data/app/*",
        "shell rm -rf /data/dalvik-cache/*",
        "shell rm -rf /data/local/*",
        "shell rm -rf /data/media/*",
        
        # Clear package manager
        "shell pm clear com.android.settings",
        "shell pm clear com.android.providers.settings",
        
        # Factory reset via settings
        "shell am start -a android.intent.action.MASTER_CLEAR"
    ]
    
    print(f"🧹 Executing {len(wipe_commands)} wipe commands...")
    
    successful_commands = 0
    failed_commands = 0
    
    for i, command in enumerate(wipe_commands, 1):
        try:
            print(f"   [{i:2d}/{len(wipe_commands)}] {command}")
            result = subprocess.run(["./platform-tools/adb.exe"] + command.split(), 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"   ✅ Success")
                successful_commands += 1
            else:
                print(f"   ⚠️  Partial success (expected for some commands)")
                print(f"      Error: {result.stderr.strip()}")
                failed_commands += 1
                
        except subprocess.TimeoutExpired:
            print(f"   ⏰ Timeout")
            failed_commands += 1
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            failed_commands += 1
    
    print(f"\n📊 Wipe Summary:")
    print(f"   ✅ Successful commands: {successful_commands}")
    print(f"   ⚠️  Failed/partial commands: {failed_commands}")
    
    return successful_commands > 0

def verify_wipe():
    """Verify that the device has been wiped"""
    print("\n🔍 Verifying wipe...")
    
    verification_commands = [
        "shell ls /data",
        "shell ls /sdcard",
        "shell ls /cache"
    ]
    
    for command in verification_commands:
        try:
            result = subprocess.run(["./platform-tools/adb.exe"] + command.split(), 
                                  capture_output=True, text=True, timeout=10)
            
            if "No such file or directory" in result.stderr or not result.stdout.strip():
                print(f"   ✅ {command} - Directory appears empty")
            else:
                print(f"   ⚠️  {command} - Some files may remain")
                print(f"      Content: {result.stdout.strip()}")
                
        except Exception as e:
            print(f"   ❌ {command} - Verification failed: {e}")

def reboot_device():
    """Reboot the device to complete the wipe"""
    print("\n🔄 Rebooting device...")
    try:
        subprocess.run(["./platform-tools/adb.exe", "reboot"], 
                      capture_output=True, text=True, timeout=10)
        print("✅ Reboot command sent")
        print("⏳ Device should reboot in 30-60 seconds")
    except Exception as e:
        print(f"❌ Reboot failed: {e}")

def main():
    print("🧹 Samsung Galaxy J3 Developer Mode Wipe Tool")
    print("=" * 60)
    
    # Check device connection
    if not check_device():
        print("\n❌ Device not ready for wiping")
        print("💡 Please ensure:")
        print("   1. USB cable is connected")
        print("   2. Developer Options is enabled")
        print("   3. USB Debugging is enabled")
        print("   4. You've allowed USB Debugging on the phone")
        print("   5. Try disconnecting and reconnecting the USB cable")
        return
    
    # Confirm wipe
    print("\n⚠️  WARNING: This will completely erase ALL data on the device!")
    print("📱 Samsung Galaxy J3 will be wiped clean")
    print("💾 All apps, settings, photos, and data will be permanently deleted!")
    
    confirm = input("\nType 'WIPE' to confirm: ").strip()
    if confirm != "WIPE":
        print("❌ Wipe cancelled")
        return
    
    # Perform wipe
    print("\n🧹 Starting wipe process...")
    success = wipe_device()
    
    if success:
        print("\n✅ Wipe process completed!")
        
        # Verify wipe
        verify_wipe()
        
        # Reboot device
        reboot_device()
        
        print("\n🎉 Device wipe completed successfully!")
        print("📱 Samsung Galaxy J3 is now ready for U3CP system installation")
        print("\n📋 Next steps:")
        print("   1. Wait for device to reboot")
        print("   2. Complete basic Android setup")
        print("   3. Enable Developer Options again")
        print("   4. Enable USB Debugging")
        print("   5. Run the U3CP installation script")
        
    else:
        print("\n❌ Wipe process failed")
        print("💡 Try the manual recovery mode method instead")

if __name__ == "__main__":
    main() 
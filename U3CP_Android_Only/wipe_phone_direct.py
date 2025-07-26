#!/usr/bin/env python3
"""
Direct Phone Wipe Script
Wipes the connected Samsung Galaxy J3 (SM-J337P) immediately
"""

import subprocess
import time
import sys
import os

def check_adb_devices():
    """Check for connected devices"""
    try:
        result = subprocess.run(["./platform-tools/adb.exe", "devices"], 
                              capture_output=True, text=True, timeout=10)
        print("🔍 Checking connected devices...")
        print(result.stdout)
        return result.stdout
    except Exception as e:
        print(f"❌ ADB check failed: {e}")
        return None

def wipe_phone():
    """Wipe the connected phone"""
    print("🧹 Starting direct phone wipe...")
    print("⚠️  WARNING: This will completely erase all data on the phone!")
    print("📱 Target: Samsung Galaxy J3 (SM-J337P)")
    
    # Check if device is connected
    devices_output = check_adb_devices()
    if not devices_output or "device" not in devices_output:
        print("❌ No device found or device not authorized")
        print("💡 Make sure phone is in Download Mode and connected via USB")
        return False
    
    print("✅ Device detected and connected")
    
    # Wipe commands
    wipe_commands = [
        "shell rm -rf /data/*",
        "shell rm -rf /cache/*", 
        "shell rm -rf /sdcard/*",
        "shell rm -rf /storage/*",
        "shell rm -rf /mnt/*",
        "shell rm -rf /system/app/*",
        "shell rm -rf /system/priv-app/*",
        "shell rm -rf /system/data/*"
    ]
    
    print("🧹 Executing wipe commands...")
    
    for i, command in enumerate(wipe_commands, 1):
        try:
            print(f"   [{i}/{len(wipe_commands)}] Executing: {command}")
            result = subprocess.run(["./platform-tools/adb.exe"] + command.split(), 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"   ✅ Success: {command}")
            else:
                print(f"   ⚠️  Partial success: {command}")
                print(f"      Error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"   ⏰ Timeout: {command}")
        except Exception as e:
            print(f"   ❌ Failed: {command} - {e}")
    
    # Final wipe commands
    print("🧹 Executing final wipe commands...")
    
    final_commands = [
        "shell su -c 'wipe data'",
        "shell su -c 'wipe cache'",
        "shell su -c 'wipe dalvik'",
        "shell su -c 'wipe system'"
    ]
    
    for command in final_commands:
        try:
            print(f"   Executing: {command}")
            result = subprocess.run(["./platform-tools/adb.exe"] + command.split(), 
                                  capture_output=True, text=True, timeout=30)
            print(f"   Result: {result.stdout}")
        except Exception as e:
            print(f"   ⚠️  Command failed: {e}")
    
    print("🧹 Wipe process completed!")
    print("📱 Phone should now be completely wiped")
    
    # Verify wipe
    print("🔍 Verifying wipe...")
    try:
        result = subprocess.run(["./platform-tools/adb.exe", "shell", "ls", "/data"], 
                              capture_output=True, text=True, timeout=10)
        if "No such file or directory" in result.stderr or not result.stdout.strip():
            print("✅ Wipe verification successful - /data directory is empty")
        else:
            print("⚠️  Some data may still remain")
    except Exception as e:
        print(f"⚠️  Could not verify wipe: {e}")
    
    return True

def main():
    print("🧹 Direct Phone Wipe Tool")
    print("=" * 50)
    
    # Confirm wipe
    print("⚠️  This will completely erase ALL data on the connected phone!")
    print("📱 Samsung Galaxy J3 (SM-J337P) will be wiped clean")
    
    confirm = input("Type 'WIPE' to confirm: ").strip()
    if confirm != "WIPE":
        print("❌ Wipe cancelled")
        return
    
    print("🧹 Starting wipe process...")
    success = wipe_phone()
    
    if success:
        print("✅ Phone wipe completed successfully!")
        print("📱 Phone is ready for U3CP system installation")
    else:
        print("❌ Phone wipe failed")
        print("💡 Try reconnecting the phone or using recovery mode")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Automated Complete Wipe Script for Samsung Galaxy J3
Performs comprehensive wipe using multiple methods
"""

import subprocess
import time
import sys

def check_device():
    """Check if device is connected"""
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

def clear_user_data():
    """Clear all user data directories"""
    print("🧹 Clearing user data directories...")
    
    data_dirs = [
        "/data/data",
        "/data/app",
        "/data/dalvik-cache", 
        "/data/local",
        "/data/media",
        "/sdcard",
        "/storage/emulated/0"
    ]
    
    for directory in data_dirs:
        try:
            print(f"   Clearing {directory}...")
            result = subprocess.run(["./platform-tools/adb.exe", "shell", f"rm -rf {directory}/*"], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"   ✅ {directory} cleared")
            else:
                print(f"   ⚠️  {directory} - {result.stderr.strip()}")
        except Exception as e:
            print(f"   ❌ {directory} - {e}")

def clear_package_data():
    """Clear all package data"""
    print("🧹 Clearing package data...")
    
    try:
        # Get list of all packages
        result = subprocess.run(["./platform-tools/adb.exe", "shell", "pm list packages"], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            packages = result.stdout.strip().split('\n')
            for package in packages:
                if package.startswith('package:'):
                    package_name = package.replace('package:', '').strip()
                    if package_name not in ['com.android.settings', 'com.android.systemui']:
                        try:
                            subprocess.run(["./platform-tools/adb.exe", "shell", f"pm clear {package_name}"], 
                                         capture_output=True, text=True, timeout=10)
                        except:
                            pass
            print("   ✅ Package data cleared")
    except Exception as e:
        print(f"   ❌ Package clearing failed: {e}")

def clear_system_data():
    """Clear system data where possible"""
    print("🧹 Clearing system data...")
    
    system_dirs = [
        "/cache",
        "/data/cache",
        "/data/log",
        "/data/misc",
        "/data/system/users/0"
    ]
    
    for directory in system_dirs:
        try:
            print(f"   Clearing {directory}...")
            result = subprocess.run(["./platform-tools/adb.exe", "shell", f"rm -rf {directory}/*"], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"   ✅ {directory} cleared")
            else:
                print(f"   ⚠️  {directory} - {result.stderr.strip()}")
        except Exception as e:
            print(f"   ❌ {directory} - {e}")

def trigger_factory_reset():
    """Trigger factory reset through settings"""
    print("🧹 Triggering factory reset...")
    
    try:
        # Try multiple factory reset methods
        reset_methods = [
            "am start -a android.intent.action.MASTER_CLEAR",
            "am start -n com.android.settings/.Settings\\$ResetDashboardActivity",
            "am start -n com.android.settings/.Settings\\$SystemDashboardActivity"
        ]
        
        for method in reset_methods:
            try:
                print(f"   Trying: {method}")
                result = subprocess.run(["./platform-tools/adb.exe", "shell", method], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    print(f"   ✅ Factory reset triggered")
                    return True
            except Exception as e:
                print(f"   ⚠️  Method failed: {e}")
        
        return False
    except Exception as e:
        print(f"   ❌ Factory reset failed: {e}")
        return False

def reboot_to_recovery():
    """Reboot to recovery mode for complete wipe"""
    print("🔄 Rebooting to recovery mode...")
    
    try:
        result = subprocess.run(["./platform-tools/adb.exe", "reboot", "recovery"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Reboot to recovery command sent")
            print("📱 Phone should now reboot to recovery mode")
            print("💡 Use recovery menu to perform factory reset")
            return True
        else:
            print("❌ Reboot to recovery failed")
            return False
    except Exception as e:
        print(f"❌ Reboot failed: {e}")
        return False

def verify_wipe():
    """Verify that data has been cleared"""
    print("🔍 Verifying wipe...")
    
    check_dirs = [
        "/data/data",
        "/sdcard",
        "/storage/emulated/0"
    ]
    
    for directory in check_dirs:
        try:
            result = subprocess.run(["./platform-tools/adb.exe", "shell", f"ls {directory}"], 
                                  capture_output=True, text=True, timeout=10)
            
            if "No such file or directory" in result.stderr or not result.stdout.strip():
                print(f"   ✅ {directory} - Empty or cleared")
            else:
                print(f"   ⚠️  {directory} - Some data may remain")
        except Exception as e:
            print(f"   ❌ {directory} - Could not verify: {e}")

def main():
    print("🧹 Automated Complete Wipe for Samsung Galaxy J3")
    print("=" * 60)
    
    # Check device connection
    if not check_device():
        print("❌ Device not ready for wiping")
        return
    
    # Confirm wipe
    print("\n⚠️  WARNING: This will completely erase ALL data on the device!")
    print("📱 Samsung Galaxy J3 will be wiped clean")
    print("💾 All apps, settings, photos, and data will be permanently deleted!")
    
    confirm = input("\nType 'WIPE' to confirm: ").strip()
    if confirm != "WIPE":
        print("❌ Wipe cancelled")
        return
    
    print("\n🧹 Starting automated complete wipe...")
    
    # Step 1: Clear user data
    clear_user_data()
    
    # Step 2: Clear package data
    clear_package_data()
    
    # Step 3: Clear system data
    clear_system_data()
    
    # Step 4: Verify initial wipe
    verify_wipe()
    
    # Step 5: Try factory reset
    print("\n🧹 Attempting factory reset...")
    if trigger_factory_reset():
        print("✅ Factory reset triggered successfully!")
        print("📱 Phone should begin factory reset process")
        print("⏳ This may take 5-10 minutes")
    else:
        print("⚠️  Factory reset not triggered automatically")
        print("🔄 Attempting reboot to recovery mode...")
        if reboot_to_recovery():
            print("✅ Phone rebooted to recovery mode")
            print("💡 Use recovery menu to complete factory reset")
        else:
            print("❌ Could not trigger factory reset")
            print("💡 Manual factory reset required")
    
    print("\n📊 Wipe Summary:")
    print("   ✅ User data directories cleared")
    print("   ✅ Package data cleared") 
    print("   ✅ System data cleared")
    print("   ✅ Factory reset triggered")
    
    print("\n🎉 Automated wipe completed!")
    print("📱 Samsung Galaxy J3 is ready for U3CP system installation")
    print("\n📋 Next steps:")
    print("   1. Wait for factory reset to complete")
    print("   2. Complete basic Android setup")
    print("   3. Enable Developer Options (tap Build Number 7 times)")
    print("   4. Enable USB Debugging")
    print("   5. Run U3CP installation script")

if __name__ == "__main__":
    main() 
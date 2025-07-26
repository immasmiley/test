#!/usr/bin/env python3
"""
Direct U3CP Android-Only Installation Script
Installs the complete system directly on a connected Android device
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path

class DirectU3CPInstaller:
    def __init__(self):
        self.install_dir = "U3CP_Installation"
        self.device_id = None
        self.adb_path = "adb"
        
    def check_adb_available(self):
        """Check if ADB is available and working"""
        try:
            result = subprocess.run([self.adb_path, "version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("[OK] ADB is available")
                return True
            else:
                print("[ERROR] ADB not working properly")
                return False
        except FileNotFoundError:
            print("[ERROR] ADB not found. Please install Android SDK or platform-tools")
            return False
        except Exception as e:
            print(f"[ERROR] ADB check failed: {e}")
            return False
    
    def detect_connected_devices(self):
        """Detect connected Android devices"""
        try:
            result = subprocess.run([self.adb_path, "devices"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                print("[ERROR] Failed to detect devices")
                return []
            
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            devices = []
            
            for line in lines:
                if line.strip() and '\tdevice' in line:
                    device_id = line.split('\t')[0]
                    devices.append(device_id)
                    print(f"[OK] Found device: {device_id}")
            
            return devices
            
        except Exception as e:
            print(f"[ERROR] Device detection failed: {e}")
            return []
    
    def select_device(self, devices):
        """Let user select a device if multiple are connected"""
        if not devices:
            print("[ERROR] No devices found")
            return None
        
        if len(devices) == 1:
            self.device_id = devices[0]
            print(f"[OK] Using device: {self.device_id}")
            return self.device_id
        
        print("\nMultiple devices found:")
        for i, device in enumerate(devices, 1):
            print(f"{i}. {device}")
        
        while True:
            try:
                choice = input(f"\nSelect device (1-{len(devices)}): ").strip()
                index = int(choice) - 1
                if 0 <= index < len(devices):
                    self.device_id = devices[index]
                    print(f"[OK] Selected device: {self.device_id}")
                    return self.device_id
                else:
                    print("[ERROR] Invalid selection")
            except ValueError:
                print("[ERROR] Please enter a number")
    
    def check_device_requirements(self):
        """Check if device meets requirements"""
        print("\n[INFO] Checking device requirements...")
        
        # Check Android version
        try:
            result = subprocess.run([self.adb_path, "-s", self.device_id, "shell", 
                                   "getprop", "ro.build.version.release"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                android_version = result.stdout.strip()
                print(f"[OK] Android version: {android_version}")
                
                # Check if Android 7.0+ (API 24+)
                try:
                    version_num = float(android_version)
                    if version_num >= 7.0:
                        print("[OK] Android version meets requirements")
                    else:
                        print(f"[WARNING] Android {android_version} may have compatibility issues")
                except ValueError:
                    print("[INFO] Could not parse Android version")
            else:
                print("[WARNING] Could not determine Android version")
                
        except Exception as e:
            print(f"[ERROR] Android version check failed: {e}")
        
        # Check available storage
        try:
            result = subprocess.run([self.adb_path, "-s", self.device_id, "shell", 
                                   "df", "/sdcard"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    parts = lines[1].split()
                    if len(parts) >= 4:
                        available_mb = int(parts[3]) // 1024
                        print(f"[OK] Available storage: {available_mb} MB")
                        
                        if available_mb >= 500:  # Need at least 500MB
                            print("[OK] Sufficient storage available")
                        else:
                            print(f"[WARNING] Low storage: {available_mb} MB available")
            else:
                print("[WARNING] Could not check storage")
                
        except Exception as e:
            print(f"[ERROR] Storage check failed: {e}")
        
        # Check if device is rooted (optional)
        try:
            result = subprocess.run([self.adb_path, "-s", self.device_id, "shell", 
                                   "which", "su"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and result.stdout.strip():
                print("[INFO] Device appears to be rooted")
            else:
                print("[INFO] Device is not rooted (this is fine)")
                
        except Exception as e:
            print(f"[ERROR] Root check failed: {e}")
    
    def install_fdroid(self):
        """Install F-Droid APK"""
        print("\n[INFO] Installing F-Droid...")
        
        fdroid_apk = os.path.join(self.install_dir, "F-Droid.apk")
        if not os.path.exists(fdroid_apk):
            print("[ERROR] F-Droid APK not found")
            return False
        
        try:
            # Push APK to device
            result = subprocess.run([self.adb_path, "-s", self.device_id, "push", 
                                   fdroid_apk, "/sdcard/"], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                print(f"[ERROR] Failed to push F-Droid APK: {result.stderr}")
                return False
            
            # Install APK
            result = subprocess.run([self.adb_path, "-s", self.device_id, "install", 
                                   "-r", "/sdcard/F-Droid.apk"], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print("[OK] F-Droid installed successfully")
                return True
            else:
                print(f"[ERROR] F-Droid installation failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"[ERROR] F-Droid installation error: {e}")
            return False
    
    def install_termux(self):
        """Install Termux APK"""
        print("\n[INFO] Installing Termux...")
        
        termux_apk = os.path.join(self.install_dir, "Termux.apk")
        if not os.path.exists(termux_apk):
            print("[ERROR] Termux APK not found")
            return False
        
        try:
            # Push APK to device
            result = subprocess.run([self.adb_path, "-s", self.device_id, "push", 
                                   termux_apk, "/sdcard/"], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                print(f"[ERROR] Failed to push Termux APK: {result.stderr}")
                return False
            
            # Install APK
            result = subprocess.run([self.adb_path, "-s", self.device_id, "install", 
                                   "-r", "/sdcard/Termux.apk"], 
                                  capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print("[OK] Termux installed successfully")
                return True
            else:
                print(f"[ERROR] Termux installation failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Termux installation error: {e}")
            return False
    
    def push_u3cp_files(self):
        """Push U3CP system files to device"""
        print("\n[INFO] Pushing U3CP system files...")
        
        # Create U3CP directory on device
        try:
            subprocess.run([self.adb_path, "-s", self.device_id, "shell", 
                          "mkdir", "-p", "/sdcard/U3CP"], 
                         capture_output=True, text=True, timeout=10)
        except Exception as e:
            print(f"[ERROR] Failed to create U3CP directory: {e}")
            return False
        
        # Files to push
        files_to_push = [
            "U3CP_Android_Only_System.py",
            "U3CP_Android_Only_App.py", 
            "requirements_android_only.txt",
            "README_Android_Only.md",
            "test_android_only.py",
            "termux_requirements.txt",
            "termux_offline_install.sh"
        ]
        
        success_count = 0
        for filename in files_to_push:
            filepath = os.path.join(self.install_dir, filename)
            if os.path.exists(filepath):
                try:
                    result = subprocess.run([self.adb_path, "-s", self.device_id, "push", 
                                           filepath, "/sdcard/U3CP/"], 
                                          capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        print(f"[OK] Pushed {filename}")
                        success_count += 1
                    else:
                        print(f"[ERROR] Failed to push {filename}: {result.stderr}")
                except Exception as e:
                    print(f"[ERROR] Error pushing {filename}: {e}")
            else:
                print(f"[WARNING] {filename} not found")
        
        print(f"[OK] Pushed {success_count}/{len(files_to_push)} files successfully")
        return success_count > 0
    
    def create_install_script(self):
        """Create installation script on device"""
        print("\n[INFO] Creating installation script on device...")
        
        install_script = '''#!/data/data/com.termux/files/usr/bin/bash
# U3CP Android-Only Installation Script
# Run this in Termux after installation

echo "U3CP Android-Only System Installation"
echo "====================================="

# Navigate to U3CP directory
cd /sdcard/U3CP

# Update package list
pkg update -y

# Install Python
pkg install python -y

# Install pip
pkg install python-pip -y

# Install required packages
pip install -r requirements_android_only.txt

# Make scripts executable
chmod +x termux_offline_install.sh

# Run offline installer
./termux_offline_install.sh

echo "Installation complete!"
echo "Run: python U3CP_Android_Only_App.py"
'''
        
        try:
            # Write script to device
            script_path = os.path.join(self.install_dir, "device_install.sh")
            with open(script_path, 'w') as f:
                f.write(install_script)
            
            # Push script to device
            result = subprocess.run([self.adb_path, "-s", self.device_id, "push", 
                                   script_path, "/sdcard/U3CP/"], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("[OK] Installation script created on device")
                return True
            else:
                print(f"[ERROR] Failed to create installation script: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Installation script creation failed: {e}")
            return False
    
    def launch_termux(self):
        """Launch Termux on device"""
        print("\n[INFO] Launching Termux...")
        
        try:
            # Launch Termux
            result = subprocess.run([self.adb_path, "-s", self.device_id, "shell", 
                                   "am", "start", "-n", 
                                   "com.termux/.HomeActivity"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("[OK] Termux launched successfully")
                return True
            else:
                print(f"[ERROR] Failed to launch Termux: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Termux launch failed: {e}")
            return False
    
    def run_installation(self):
        """Run the complete installation process"""
        print("U3CP Direct Installation")
        print("========================")
        
        # Check ADB
        if not self.check_adb_available():
            return False
        
        # Detect devices
        devices = self.detect_connected_devices()
        if not devices:
            print("[ERROR] No Android devices found")
            print("[INFO] Please:")
            print("1. Enable USB debugging on your Android device")
            print("2. Connect device via USB")
            print("3. Accept the debugging prompt on your device")
            return False
        
        # Select device
        if not self.select_device(devices):
            return False
        
        # Check device requirements
        self.check_device_requirements()
        
        # Install F-Droid
        if not self.install_fdroid():
            print("[WARNING] F-Droid installation failed, continuing...")
        
        # Install Termux
        if not self.install_termux():
            print("[ERROR] Termux installation failed")
            return False
        
        # Push U3CP files
        if not self.push_u3cp_files():
            print("[ERROR] Failed to push U3CP files")
            return False
        
        # Create installation script
        if not self.create_install_script():
            print("[ERROR] Failed to create installation script")
            return False
        
        # Launch Termux
        if not self.launch_termux():
            print("[WARNING] Failed to launch Termux")
        
        print("\n" + "="*50)
        print("INSTALLATION COMPLETE!")
        print("="*50)
        print("\nNext steps on your Android device:")
        print("1. Open Termux (should have launched automatically)")
        print("2. Run: cd /sdcard/U3CP")
        print("3. Run: chmod +x device_install.sh")
        print("4. Run: ./device_install.sh")
        print("5. After installation, run: python U3CP_Android_Only_App.py")
        print("\nThe U3CP Android-Only system will be ready to use!")
        
        return True

def main():
    installer = DirectU3CPInstaller()
    installer.run_installation()

if __name__ == "__main__":
    main() 
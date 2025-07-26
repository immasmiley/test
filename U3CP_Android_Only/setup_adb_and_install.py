#!/usr/bin/env python3
"""
Setup ADB and Direct U3CP Installation
Downloads ADB, installs it, and then performs direct installation
"""

import os
import sys
import subprocess
import zipfile
import urllib.request
import shutil
from pathlib import Path

class ADBSetupAndInstall:
    def __init__(self):
        self.adb_dir = "platform-tools"
        self.adb_path = os.path.join(self.adb_dir, "adb.exe")
        self.download_url = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
        self.zip_file = "platform-tools.zip"
        
    def download_platform_tools(self):
        """Download Android platform-tools (includes ADB)"""
        print("[INFO] Downloading Android platform-tools...")
        
        try:
            print(f"[INFO] Downloading from: {self.download_url}")
            urllib.request.urlretrieve(self.download_url, self.zip_file)
            print("[OK] Download completed")
            return True
        except Exception as e:
            print(f"[ERROR] Download failed: {e}")
            return False
    
    def extract_platform_tools(self):
        """Extract the platform-tools zip file"""
        print("[INFO] Extracting platform-tools...")
        
        try:
            with zipfile.ZipFile(self.zip_file, 'r') as zip_ref:
                zip_ref.extractall(".")
            print("[OK] Extraction completed")
            return True
        except Exception as e:
            print(f"[ERROR] Extraction failed: {e}")
            return False
    
    def verify_adb_installation(self):
        """Verify that ADB is working"""
        print("[INFO] Verifying ADB installation...")
        
        try:
            result = subprocess.run([self.adb_path, "version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("[OK] ADB is working correctly")
                print(f"[INFO] ADB version: {result.stdout.strip()}")
                return True
            else:
                print(f"[ERROR] ADB verification failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"[ERROR] ADB verification error: {e}")
            return False
    
    def setup_adb(self):
        """Download and setup ADB"""
        print("Setting up ADB for U3CP Installation")
        print("====================================")
        
        # Check if ADB already exists
        if os.path.exists(self.adb_path):
            print("[INFO] ADB already exists, verifying...")
            if self.verify_adb_installation():
                return True
            else:
                print("[INFO] Existing ADB not working, will reinstall...")
        
        # Download platform-tools
        if not self.download_platform_tools():
            return False
        
        # Extract platform-tools
        if not self.extract_platform_tools():
            return False
        
        # Verify installation
        if not self.verify_adb_installation():
            return False
        
        # Clean up zip file
        try:
            os.remove(self.zip_file)
            print("[OK] Cleaned up download file")
        except:
            pass
        
        return True
    
    def run_direct_installation(self):
        """Run the direct installation after ADB is set up"""
        print("\n" + "="*50)
        print("Starting Direct U3CP Installation")
        print("="*50)
        
        # Import and run the direct installer
        try:
            from direct_install import DirectU3CPInstaller
            
            # Create installer with correct ADB path
            installer = DirectU3CPInstaller()
            installer.adb_path = self.adb_path
            
            # Run installation
            return installer.run_installation()
            
        except ImportError:
            print("[ERROR] Could not import direct_install module")
            return False
        except Exception as e:
            print(f"[ERROR] Direct installation failed: {e}")
            return False
    
    def run_complete_setup(self):
        """Run the complete setup and installation process"""
        print("U3CP Complete Setup and Installation")
        print("====================================")
        print("\nThis will:")
        print("1. Download and install ADB")
        print("2. Detect your connected Android device")
        print("3. Install F-Droid and Termux")
        print("4. Push U3CP system files")
        print("5. Set up the complete U3CP Android-Only system")
        print("\nRequirements:")
        print("- Android device connected via USB")
        print("- USB debugging enabled on your device")
        print("- Internet connection for ADB download")
        print("\nPress Enter to continue...")
        input()
        
        # Setup ADB
        if not self.setup_adb():
            print("[ERROR] ADB setup failed")
            return False
        
        # Run direct installation
        if not self.run_direct_installation():
            print("[ERROR] Direct installation failed")
            return False
        
        print("\n" + "="*50)
        print("SETUP COMPLETE!")
        print("="*50)
        print("\nYour U3CP Android-Only system is now installed!")
        print("\nNext steps:")
        print("1. Open Termux on your Android device")
        print("2. Navigate to: cd /sdcard/U3CP")
        print("3. Run the installation script: ./device_install.sh")
        print("4. Start U3CP: python U3CP_Android_Only_App.py")
        print("\nEnjoy your open-source, Google-free Android system!")
        
        return True

def main():
    setup = ADBSetupAndInstall()
    setup.run_complete_setup()

if __name__ == "__main__":
    main() 
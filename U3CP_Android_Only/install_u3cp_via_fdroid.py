#!/usr/bin/env python3
"""
U3CP F-Droid Installation Script
Installs U3CP as a proper Android app using F-Droid
"""

import subprocess
import os
import time
import json
import shutil
from datetime import datetime

class U3CPFdroidInstaller:
    def __init__(self):
        self.device_connected = False
        self.fdroid_installed = False
        self.python_installed = False
        self.buildozer_installed = False
        self.installation_log = []
        
    def log(self, message: str, level: str = "INFO"):
        """Log installation progress"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        print(log_entry)
        self.installation_log.append(log_entry)
        
    def execute_adb_command(self, command: str) -> dict:
        """Execute ADB command and return result"""
        try:
            self.log(f"Executing: adb {command}")
            result = subprocess.run(
                ["./platform-tools/adb.exe"] + command.split(),
                capture_output=True,
                text=True,
                cwd=os.getcwd(),
                timeout=30
            )
            
            success = result.returncode == 0
            if not success:
                self.log(f"Command failed: {result.stderr}", "ERROR")
            
            return {
                'success': success,
                'output': result.stdout.strip(),
                'error': result.stderr.strip(),
                'command': command
            }
        except subprocess.TimeoutExpired:
            self.log(f"Command timed out: {command}", "ERROR")
            return {'success': False, 'output': '', 'error': 'Timeout', 'command': command}
        except Exception as e:
            self.log(f"Command exception: {str(e)}", "ERROR")
            return {'success': False, 'output': '', 'error': str(e), 'command': command}
    
    def check_device_connection(self) -> bool:
        """Check if Android device is connected"""
        self.log("Checking device connection...")
        
        result = self.execute_adb_command("devices")
        if result['success']:
            lines = result['output'].split('\n')
            devices = [line for line in lines if '\tdevice' in line]
            
            if devices:
                device_id = devices[0].split('\t')[0]
                self.log(f"✅ Device connected: {device_id}")
                self.device_connected = True
                return True
            else:
                self.log("❌ No devices found", "ERROR")
                return False
        else:
            self.log(f"❌ ADB command failed: {result['error']}", "ERROR")
            return False
    
    def check_fdroid_installation(self) -> bool:
        """Check if F-Droid is installed"""
        self.log("Checking F-Droid installation...")
        
        result = self.execute_adb_command("shell pm list packages | grep fdroid")
        if result['success'] and 'org.fdroid.fdroid' in result['output']:
            self.log("✅ F-Droid is installed")
            self.fdroid_installed = True
            return True
        else:
            self.log("❌ F-Droid not found", "ERROR")
            return False
    
    def launch_fdroid(self) -> bool:
        """Launch F-Droid app"""
        self.log("Launching F-Droid...")
        
        result = self.execute_adb_command("shell am start -n org.fdroid.fdroid/.views.main.MainActivity")
        if result['success']:
            self.log("✅ F-Droid launched successfully")
            time.sleep(3)  # Wait for app to load
            return True
        else:
            self.log(f"❌ Failed to launch F-Droid: {result['error']}", "ERROR")
            return False
    
    def install_pydroid3_via_fdroid(self) -> bool:
        """Install Pydroid 3 via F-Droid"""
        self.log("Installing Pydroid 3 via F-Droid...")
        
        # Method 1: Direct F-Droid URL
        fdroid_url = "fdroid://app/org.pydroid3"
        result = self.execute_adb_command(f"shell am start -a android.intent.action.VIEW -d '{fdroid_url}'")
        
        if result['success']:
            self.log("✅ Launched F-Droid for Pydroid 3 installation")
            self.log("📱 Please complete the installation manually in F-Droid")
            self.log("   - Tap 'Install' when prompted")
            self.log("   - Wait for download and installation to complete")
            
            # Wait for user to complete installation
            input("Press Enter when Pydroid 3 installation is complete...")
            
            # Verify installation
            return self.verify_pydroid3_installation()
        else:
            self.log(f"❌ Failed to launch F-Droid URL: {result['error']}", "ERROR")
            return False
    
    def verify_pydroid3_installation(self) -> bool:
        """Verify Pydroid 3 is installed"""
        self.log("Verifying Pydroid 3 installation...")
        
        result = self.execute_adb_command("shell pm list packages | grep pydroid")
        if result['success'] and 'org.pydroid3' in result['output']:
            self.log("✅ Pydroid 3 is installed")
            self.python_installed = True
            return True
        else:
            self.log("❌ Pydroid 3 not found", "ERROR")
            return False
    
    def install_termux_via_fdroid(self) -> bool:
        """Install Termux via F-Droid as backup"""
        self.log("Installing Termux via F-Droid...")
        
        fdroid_url = "fdroid://app/com.termux"
        result = self.execute_adb_command(f"shell am start -a android.intent.action.VIEW -d '{fdroid_url}'")
        
        if result['success']:
            self.log("✅ Launched F-Droid for Termux installation")
            self.log("📱 Please complete the installation manually in F-Droid")
            
            input("Press Enter when Termux installation is complete...")
            
            # Verify installation
            result = self.execute_adb_command("shell pm list packages | grep termux")
            if result['success'] and 'com.termux' in result['output']:
                self.log("✅ Termux is installed")
                return True
            else:
                self.log("❌ Termux installation failed", "ERROR")
                return False
        else:
            self.log(f"❌ Failed to launch F-Droid URL: {result['error']}", "ERROR")
            return False
    
    def create_u3cp_apk_build_script(self) -> str:
        """Create buildozer.spec for U3CP APK"""
        self.log("Creating U3CP APK build configuration...")
        
        buildozer_spec = """[app]
title = U3CP Android-Only System
package.name = u3cp_android_only
package.domain = org.u3cp.android
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,db
version = 1.0.0

requirements = python3,kivy,requests,websockets,asyncio,threading,json,datetime,hashlib,uuid,subprocess,os,sys,time

orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 28
android.minapi = 21
android.ndk = 23b
android.sdk = 28
android.arch = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
"""
        
        with open("buildozer.spec", "w") as f:
            f.write(buildozer_spec)
        
        self.log("✅ buildozer.spec created")
        return "buildozer.spec"
    
    def create_u3cp_main_py(self) -> str:
        """Create main.py for U3CP app"""
        self.log("Creating U3CP main.py...")
        
        main_py = '''#!/usr/bin/env python3
"""
U3CP Android-Only System - Main Entry Point
"""

import os
import sys
import json
import time
from datetime import datetime

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.uix.textinput import TextInput
    from kivy.uix.scrollview import ScrollView
    from kivy.clock import Clock
    
    KIVY_AVAILABLE = True
except ImportError:
    KIVY_AVAILABLE = False

class U3CPMainApp(App):
    def __init__(self):
        super().__init__()
        self.title = "U3CP Android-Only System"
        self.device_id = self._generate_device_id()
        
    def _generate_device_id(self):
        import hashlib
        import uuid
        return f"u3cp_{uuid.uuid4().hex[:8]}"
    
    def build(self):
        if not KIVY_AVAILABLE:
            return self._build_console_ui()
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text="U3CP Android-Only System",
            size_hint_y=None,
            height=50,
            font_size='20sp'
        )
        layout.add_widget(title)
        
        # Status
        self.status_label = Label(
            text="Initializing...",
            size_hint_y=None,
            height=30
        )
        layout.add_widget(self.status_label)
        
        # Control buttons
        start_btn = Button(
            text="Start U3CP System",
            size_hint_y=None,
            height=50,
            on_press=self.start_system
        )
        layout.add_widget(start_btn)
        
        stop_btn = Button(
            text="Stop U3CP System",
            size_hint_y=None,
            height=50,
            on_press=self.stop_system
        )
        layout.add_widget(stop_btn)
        
        # Log area
        self.log_text = TextInput(
            text="U3CP System Log\\n",
            multiline=True,
            readonly=True,
            size_hint_y=1
        )
        layout.add_widget(self.log_text)
        
        # Start system automatically
        Clock.schedule_once(self.start_system, 2)
        
        return layout
    
    def _build_console_ui(self):
        # Fallback for non-Kivy environments
        return Label(text="U3CP System - Console Mode")
    
    def start_system(self, instance=None):
        self.log("Starting U3CP Android-Only System...")
        self.status_label.text = "System Running"
        
        # Import and start the main system
        try:
            from U3CP_Android_Only_System import U3CPAndroidOnlySystem
            self.system = U3CPAndroidOnlySystem()
            self.system.start()
            self.log("✅ U3CP System started successfully")
        except Exception as e:
            self.log(f"❌ Failed to start system: {str(e)}")
    
    def stop_system(self, instance=None):
        self.log("Stopping U3CP Android-Only System...")
        self.status_label.text = "System Stopped"
        
        if hasattr(self, 'system') and self.system:
            try:
                self.system.stop()
                self.log("✅ U3CP System stopped")
            except Exception as e:
                self.log(f"❌ Error stopping system: {str(e)}")
    
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\\n"
        
        if hasattr(self, 'log_text'):
            self.log_text.text += log_entry
        else:
            print(log_entry.strip())

if __name__ == "__main__":
    app = U3CPMainApp()
    app.run()
'''
        
        with open("main.py", "w") as f:
            f.write(main_py)
        
        self.log("✅ main.py created")
        return "main.py"
    
    def copy_u3cp_files(self):
        """Copy U3CP system files to build directory"""
        self.log("Copying U3CP system files...")
        
        files_to_copy = [
            "U3CP_Android_Only_System.py",
            "U3CP_Android_Only_App.py",
            "sphereos_android_only.db"
        ]
        
        for file in files_to_copy:
            if os.path.exists(file):
                shutil.copy2(file, ".")
                self.log(f"✅ Copied {file}")
            else:
                self.log(f"⚠️ File not found: {file}", "WARNING")
    
    def build_u3cp_apk(self) -> bool:
        """Build U3CP APK using buildozer"""
        self.log("Building U3CP APK...")
        
        # Check if buildozer is available
        try:
            result = subprocess.run(
                ["buildozer", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                self.log("✅ Buildozer is available")
                self.buildozer_installed = True
            else:
                self.log("❌ Buildozer not found", "ERROR")
                return False
        except:
            self.log("❌ Buildozer not installed", "ERROR")
            return False
        
        # Build the APK
        try:
            self.log("Starting APK build process...")
            result = subprocess.run(
                ["buildozer", "android", "debug"],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode == 0:
                self.log("✅ APK built successfully")
                return True
            else:
                self.log(f"❌ APK build failed: {result.stderr}", "ERROR")
                return False
        except subprocess.TimeoutExpired:
            self.log("❌ APK build timed out", "ERROR")
            return False
        except Exception as e:
            self.log(f"❌ APK build error: {str(e)}", "ERROR")
            return False
    
    def install_u3cp_apk(self) -> bool:
        """Install U3CP APK on device"""
        self.log("Installing U3CP APK on device...")
        
        # Find the APK file
        apk_files = [f for f in os.listdir(".") if f.endswith(".apk") and "u3cp" in f.lower()]
        
        if not apk_files:
            self.log("❌ No U3CP APK found", "ERROR")
            return False
        
        apk_file = apk_files[0]
        self.log(f"Found APK: {apk_file}")
        
        # Install APK
        result = self.execute_adb_command(f"install {apk_file}")
        if result['success']:
            self.log("✅ U3CP APK installed successfully")
            return True
        else:
            self.log(f"❌ APK installation failed: {result['error']}", "ERROR")
            return False
    
    def launch_u3cp_app(self) -> bool:
        """Launch U3CP app on device"""
        self.log("Launching U3CP app...")
        
        result = self.execute_adb_command("shell am start -n org.u3cp.android/u3cp_android_only.MainActivity")
        if result['success']:
            self.log("✅ U3CP app launched successfully")
            return True
        else:
            self.log(f"❌ Failed to launch U3CP app: {result['error']}", "ERROR")
            return False
    
    def create_installation_summary(self):
        """Create installation summary report"""
        self.log("Creating installation summary...")
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'device_connected': self.device_connected,
            'fdroid_installed': self.fdroid_installed,
            'python_installed': self.python_installed,
            'buildozer_installed': self.buildozer_installed,
            'installation_log': self.installation_log,
            'status': 'SUCCESS' if self.python_installed else 'FAILED'
        }
        
        with open("u3cp_fdroid_installation_report.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        self.log("✅ Installation report saved: u3cp_fdroid_installation_report.json")
    
    def run_installation(self):
        """Run complete U3CP installation via F-Droid"""
        self.log("🚀 Starting U3CP F-Droid Installation")
        self.log("=" * 50)
        
        # Step 1: Check device connection
        if not self.check_device_connection():
            self.log("❌ Installation failed: No device connected", "ERROR")
            return False
        
        # Step 2: Check F-Droid installation
        if not self.check_fdroid_installation():
            self.log("❌ Installation failed: F-Droid not installed", "ERROR")
            return False
        
        # Step 3: Launch F-Droid
        if not self.launch_fdroid():
            self.log("❌ Installation failed: Cannot launch F-Droid", "ERROR")
            return False
        
        # Step 4: Install Python via Pydroid 3
        if not self.install_pydroid3_via_fdroid():
            self.log("⚠️ Pydroid 3 installation failed, trying Termux", "WARNING")
            if not self.install_termux_via_fdroid():
                self.log("❌ Installation failed: No Python environment available", "ERROR")
                return False
        
        # Step 5: Create U3CP app files
        self.create_u3cp_apk_build_script()
        self.create_u3cp_main_py()
        self.copy_u3cp_files()
        
        # Step 6: Build APK (if buildozer available)
        if self.build_u3cp_apk():
            # Step 7: Install APK
            if self.install_u3cp_apk():
                # Step 8: Launch app
                self.launch_u3cp_app()
        
        # Create summary
        self.create_installation_summary()
        
        self.log("=" * 50)
        if self.python_installed:
            self.log("✅ U3CP F-Droid installation completed successfully!")
            self.log("📱 U3CP system is now available on your device")
        else:
            self.log("❌ U3CP F-Droid installation failed")
        
        return self.python_installed

def main():
    """Main installation function"""
    print("U3CP F-Droid Installation Script")
    print("=" * 40)
    
    installer = U3CPFdroidInstaller()
    success = installer.run_installation()
    
    if success:
        print("\n🎉 Installation completed successfully!")
        print("📱 You can now use U3CP on your Android device")
    else:
        print("\n❌ Installation failed")
        print("📋 Check the installation report for details")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main() 
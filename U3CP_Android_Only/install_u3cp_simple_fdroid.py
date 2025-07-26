#!/usr/bin/env python3
"""
Simple U3CP F-Droid Installation
Installs Python via F-Droid and runs U3CP directly
"""

import subprocess
import os
import time
import json
import shutil
from datetime import datetime

class SimpleU3CPFdroidInstaller:
    def __init__(self):
        self.device_connected = False
        self.fdroid_installed = False
        self.python_installed = False
        self.u3cp_deployed = False
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
            self.log("   - Pydroid 3 will provide a Python environment")
            
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
    
    def create_u3cp_launcher_script(self) -> str:
        """Create a launcher script for U3CP"""
        self.log("Creating U3CP launcher script...")
        
        launcher_script = '''#!/usr/bin/env python3
"""
U3CP Android-Only System Launcher
Runs U3CP system in Pydroid 3 or Termux
"""

import os
import sys
import time
from datetime import datetime

def main():
    print("🚀 U3CP Android-Only System Launcher")
    print("=" * 40)
    
    # Add current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    
    try:
        # Import U3CP system
        from U3CP_Android_Only_System import U3CPAndroidOnlySystem
        
        print("✅ U3CP system imported successfully")
        
        # Create and start system
        system = U3CPAndroidOnlySystem()
        print("✅ U3CP system created")
        
        # Start the system
        system.start()
        print("✅ U3CP system started")
        
        # Keep running
        print("📱 U3CP system is now running")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\\n🛑 Stopping U3CP system...")
            system.stop()
            print("✅ U3CP system stopped")
            
    except ImportError as e:
        print(f"❌ Failed to import U3CP system: {e}")
        print("Make sure all U3CP files are in the same directory")
        return False
    except Exception as e:
        print(f"❌ Error running U3CP system: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
'''
        
        with open("u3cp_launcher.py", "w") as f:
            f.write(launcher_script)
        
        self.log("✅ u3cp_launcher.py created")
        return "u3cp_launcher.py"
    
    def create_u3cp_requirements(self) -> str:
        """Create requirements.txt for U3CP"""
        self.log("Creating U3CP requirements file...")
        
        requirements = '''# U3CP Android-Only System Requirements
# Core Python modules (usually available)
# requests
# websockets
# asyncio
# threading
# json
# datetime
# hashlib
# uuid
# subprocess
# os
# sys
# time

# Optional: Kivy for GUI (if available)
# kivy

# Optional: Additional networking
# aiohttp
# websocket-client
'''
        
        with open("requirements_u3cp.txt", "w") as f:
            f.write(requirements)
        
        self.log("✅ requirements_u3cp.txt created")
        return "requirements_u3cp.txt"
    
    def deploy_u3cp_to_device(self) -> bool:
        """Deploy U3CP files to device"""
        self.log("Deploying U3CP files to device...")
        
        # Create a deployment directory on device
        deploy_dir = "/sdcard/u3cp_android_only"
        
        # Create directory
        result = self.execute_adb_command(f"shell mkdir -p {deploy_dir}")
        if not result['success']:
            self.log(f"❌ Failed to create deployment directory: {result['error']}", "ERROR")
            return False
        
        # Files to deploy
        files_to_deploy = [
            "U3CP_Android_Only_System.py",
            "U3CP_Android_Only_App.py",
            "sphereos_android_only.db",
            "u3cp_launcher.py",
            "requirements_u3cp.txt"
        ]
        
        deployed_count = 0
        for file in files_to_deploy:
            if os.path.exists(file):
                # Push file to device
                result = self.execute_adb_command(f"push {file} {deploy_dir}/")
                if result['success']:
                    self.log(f"✅ Deployed {file}")
                    deployed_count += 1
                else:
                    self.log(f"❌ Failed to deploy {file}: {result['error']}", "ERROR")
            else:
                self.log(f"⚠️ File not found: {file}", "WARNING")
        
        if deployed_count > 0:
            self.log(f"✅ Deployed {deployed_count} files to {deploy_dir}")
            self.u3cp_deployed = True
            return True
        else:
            self.log("❌ No files deployed", "ERROR")
            return False
    
    def create_pydroid3_launcher(self) -> bool:
        """Create Pydroid 3 launcher for U3CP"""
        self.log("Creating Pydroid 3 launcher...")
        
        # Create a simple HTML launcher that opens Pydroid 3
        html_launcher = '''<!DOCTYPE html>
<html>
<head>
    <title>U3CP Android-Only System</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f0f0f0; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
        .button { background: #007bff; color: white; padding: 15px 30px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; margin: 10px 5px; }
        .button:hover { background: #0056b3; }
        .info { background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 15px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 U3CP Android-Only System</h1>
        
        <div class="info">
            <h3>Installation Complete!</h3>
            <p>U3CP system has been deployed to your device.</p>
            <p>Location: <code>/sdcard/u3cp_android_only/</code></p>
        </div>
        
        <h3>Launch Options:</h3>
        
        <button class="button" onclick="launchPydroid3()">
            📱 Launch in Pydroid 3
        </button>
        
        <button class="button" onclick="launchTermux()">
            💻 Launch in Termux
        </button>
        
        <button class="button" onclick="showInstructions()">
            📋 Show Instructions
        </button>
        
        <div id="instructions" style="display: none; margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px;">
            <h4>Manual Launch Instructions:</h4>
            <ol>
                <li><strong>Pydroid 3:</strong>
                    <ul>
                        <li>Open Pydroid 3 app</li>
                        <li>Navigate to <code>/sdcard/u3cp_android_only/</code></li>
                        <li>Open <code>u3cp_launcher.py</code></li>
                        <li>Tap the play button to run</li>
                    </ul>
                </li>
                <li><strong>Termux:</strong>
                    <ul>
                        <li>Open Termux app</li>
                        <li>Run: <code>cd /sdcard/u3cp_android_only</code></li>
                        <li>Run: <code>python u3cp_launcher.py</code></li>
                    </ul>
                </li>
            </ol>
        </div>
    </div>
    
    <script>
        function launchPydroid3() {
            // Try to launch Pydroid 3 with U3CP file
            try {
                window.location.href = 'pydroid3://open?file=/sdcard/u3cp_android_only/u3cp_launcher.py';
            } catch (e) {
                alert('Please open Pydroid 3 manually and navigate to /sdcard/u3cp_android_only/u3cp_launcher.py');
            }
        }
        
        function launchTermux() {
            // Try to launch Termux
            try {
                window.location.href = 'termux://open?command=cd /sdcard/u3cp_android_only && python u3cp_launcher.py';
            } catch (e) {
                alert('Please open Termux manually and run: cd /sdcard/u3cp_android_only && python u3cp_launcher.py');
            }
        }
        
        function showInstructions() {
            const instructions = document.getElementById('instructions');
            instructions.style.display = instructions.style.display === 'none' ? 'block' : 'none';
        }
    </script>
</body>
</html>'''
        
        with open("u3cp_pydroid3_launcher.html", "w") as f:
            f.write(html_launcher)
        
        self.log("✅ u3cp_pydroid3_launcher.html created")
        return True
    
    def create_installation_summary(self):
        """Create installation summary report"""
        self.log("Creating installation summary...")
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'device_connected': self.device_connected,
            'fdroid_installed': self.fdroid_installed,
            'python_installed': self.python_installed,
            'u3cp_deployed': self.u3cp_deployed,
            'installation_log': self.installation_log,
            'deployment_location': '/sdcard/u3cp_android_only/',
            'launcher_files': [
                'u3cp_launcher.py',
                'u3cp_pydroid3_launcher.html'
            ],
            'status': 'SUCCESS' if self.python_installed and self.u3cp_deployed else 'FAILED'
        }
        
        with open("u3cp_simple_fdroid_installation_report.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        self.log("✅ Installation report saved: u3cp_simple_fdroid_installation_report.json")
    
    def run_installation(self):
        """Run complete simple U3CP installation via F-Droid"""
        self.log("🚀 Starting Simple U3CP F-Droid Installation")
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
        
        # Step 5: Create U3CP launcher files
        self.create_u3cp_launcher_script()
        self.create_u3cp_requirements()
        
        # Step 6: Deploy U3CP to device
        if not self.deploy_u3cp_to_device():
            self.log("❌ Installation failed: Cannot deploy U3CP files", "ERROR")
            return False
        
        # Step 7: Create Pydroid 3 launcher
        self.create_pydroid3_launcher()
        
        # Create summary
        self.create_installation_summary()
        
        self.log("=" * 50)
        if self.python_installed and self.u3cp_deployed:
            self.log("✅ Simple U3CP F-Droid installation completed successfully!")
            self.log("📱 U3CP system deployed to: /sdcard/u3cp_android_only/")
            self.log("🚀 Launch options:")
            self.log("   - Open u3cp_pydroid3_launcher.html in browser")
            self.log("   - Use Pydroid 3 to open u3cp_launcher.py")
            self.log("   - Use Termux: cd /sdcard/u3cp_android_only && python u3cp_launcher.py")
        else:
            self.log("❌ Simple U3CP F-Droid installation failed")
        
        return self.python_installed and self.u3cp_deployed

def main():
    """Main installation function"""
    print("Simple U3CP F-Droid Installation Script")
    print("=" * 40)
    
    installer = SimpleU3CPFdroidInstaller()
    success = installer.run_installation()
    
    if success:
        print("\n🎉 Installation completed successfully!")
        print("📱 U3CP system is deployed and ready to use")
        print("🚀 Open u3cp_pydroid3_launcher.html to get started")
    else:
        print("\n❌ Installation failed")
        print("📋 Check the installation report for details")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main() 
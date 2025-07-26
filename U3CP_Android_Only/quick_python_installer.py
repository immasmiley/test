#!/usr/bin/env python3
"""
Quick Python Installer for U3CP
Checks multiple Python options and installs the best available one
"""

import subprocess
import os
import time
import json
from datetime import datetime

class QuickPythonInstaller:
    def __init__(self):
        self.device_connected = False
        self.python_options = []
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
    
    def check_available_python_options(self) -> list:
        """Check what Python options are available"""
        self.log("Checking available Python options...")
        
        python_options = [
            {
                'name': 'Pydroid 3',
                'package': 'org.pydroid3',
                'description': 'Full Python IDE with package manager',
                'priority': 1,
                'fdroid_url': 'fdroid://app/org.pydroid3'
            },
            {
                'name': 'QPython 3',
                'package': 'org.qpython.qpy3',
                'description': 'Lightweight Python interpreter',
                'priority': 2,
                'fdroid_url': 'fdroid://app/org.qpython.qpy3'
            },
            {
                'name': 'Termux',
                'package': 'com.termux',
                'description': 'Linux terminal with Python',
                'priority': 3,
                'fdroid_url': 'fdroid://app/com.termux'
            },
            {
                'name': 'Kivy Launcher',
                'package': 'org.kivy.pygame',
                'description': 'Python/Kivy app launcher',
                'priority': 4,
                'fdroid_url': 'fdroid://app/org.kivy.pygame'
            }
        ]
        
        # Check which ones are already installed
        result = self.execute_adb_command("shell pm list packages")
        if result['success']:
            installed_packages = result['output'].lower()
            
            for option in python_options:
                if option['package'] in installed_packages:
                    option['installed'] = True
                    self.log(f"✅ {option['name']} is already installed")
                else:
                    option['installed'] = False
                    self.log(f"📦 {option['name']} available for installation")
        
        self.python_options = python_options
        return python_options
    
    def install_best_python_option(self) -> bool:
        """Install the best available Python option"""
        self.log("Installing best Python option...")
        
        # Find the best option (highest priority, not installed)
        best_option = None
        for option in self.python_options:
            if not option.get('installed', False):
                if best_option is None or option['priority'] < best_option['priority']:
                    best_option = option
        
        if best_option is None:
            self.log("✅ Python environment already available")
            return True
        
        self.log(f"🎯 Installing {best_option['name']}...")
        
        # Try F-Droid installation
        fdroid_url = best_option['fdroid_url']
        result = self.execute_adb_command(f"shell am start -a android.intent.action.VIEW -d '{fdroid_url}'")
        
        if result['success']:
            self.log(f"✅ Launched F-Droid for {best_option['name']} installation")
            self.log("📱 Please complete the installation manually in F-Droid")
            self.log(f"   - Tap 'Install' for {best_option['name']}")
            self.log("   - Wait for download and installation to complete")
            
            # Wait for user to complete installation
            input(f"Press Enter when {best_option['name']} installation is complete...")
            
            # Verify installation
            return self.verify_python_installation(best_option['package'])
        else:
            self.log(f"❌ Failed to launch F-Droid for {best_option['name']}: {result['error']}", "ERROR")
            return False
    
    def verify_python_installation(self, package: str) -> bool:
        """Verify Python installation"""
        self.log(f"Verifying Python installation...")
        
        result = self.execute_adb_command(f"shell pm list packages | grep {package}")
        if result['success'] and package in result['output']:
            self.log(f"✅ Python environment installed successfully")
            return True
        else:
            self.log(f"❌ Python installation verification failed", "ERROR")
            return False
    
    def create_u3cp_launcher(self) -> bool:
        """Create U3CP launcher for the installed Python environment"""
        self.log("Creating U3CP launcher...")
        
        # Find which Python option is installed
        installed_option = None
        for option in self.python_options:
            if option.get('installed', False):
                installed_option = option
                break
        
        if not installed_option:
            self.log("❌ No Python environment found", "ERROR")
            return False
        
        # Create appropriate launcher based on installed option
        if installed_option['name'] == 'Pydroid 3':
            return self.create_pydroid3_launcher()
        elif installed_option['name'] == 'Termux':
            return self.create_termux_launcher()
        else:
            return self.create_generic_launcher()
    
    def create_pydroid3_launcher(self) -> bool:
        """Create Pydroid 3 specific launcher"""
        self.log("Creating Pydroid 3 launcher...")
        
        launcher_html = '''<!DOCTYPE html>
<html>
<head>
    <title>U3CP Python Launcher</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f0f0f0; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
        .button { background: #007bff; color: white; padding: 15px 30px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; margin: 10px 5px; }
        .button:hover { background: #0056b3; }
        .success { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 15px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 U3CP Python Launcher</h1>
        
        <div class="success">
            <h3>✅ Python Environment Ready!</h3>
            <p>Pydroid 3 is installed and ready to run U3CP.</p>
        </div>
        
        <h3>Launch Options:</h3>
        
        <button class="button" onclick="launchPydroid3()">
            📱 Launch in Pydroid 3
        </button>
        
        <button class="button" onclick="showInstructions()">
            📋 Show Instructions
        </button>
        
        <div id="instructions" style="display: none; margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px;">
            <h4>Manual Launch Instructions:</h4>
            <ol>
                <li><strong>Open Pydroid 3</strong> on your device</li>
                <li><strong>Navigate to</strong> <code>/sdcard/u3cp_android_only/</code></li>
                <li><strong>Open</strong> <code>u3cp_launcher.py</code></li>
                <li><strong>Tap the play button</strong> to run U3CP</li>
            </ol>
        </div>
    </div>
    
    <script>
        function launchPydroid3() {
            try {
                window.location.href = 'pydroid3://open?file=/sdcard/u3cp_android_only/u3cp_launcher.py';
            } catch (e) {
                alert('Please open Pydroid 3 manually and navigate to /sdcard/u3cp_android_only/u3cp_launcher.py');
            }
        }
        
        function showInstructions() {
            const instructions = document.getElementById('instructions');
            instructions.style.display = instructions.style.display === 'none' ? 'block' : 'none';
        }
    </script>
</body>
</html>'''
        
        with open("u3cp_python_launcher.html", "w") as f:
            f.write(launcher_html)
        
        self.log("✅ u3cp_python_launcher.html created")
        return True
    
    def create_termux_launcher(self) -> bool:
        """Create Termux specific launcher"""
        self.log("Creating Termux launcher...")
        
        launcher_html = '''<!DOCTYPE html>
<html>
<head>
    <title>U3CP Termux Launcher</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f0f0f0; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
        .button { background: #28a745; color: white; padding: 15px 30px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; margin: 10px 5px; }
        .button:hover { background: #218838; }
        .success { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 15px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 U3CP Termux Launcher</h1>
        
        <div class="success">
            <h3>✅ Python Environment Ready!</h3>
            <p>Termux is installed and ready to run U3CP.</p>
        </div>
        
        <h3>Launch Options:</h3>
        
        <button class="button" onclick="launchTermux()">
            💻 Launch in Termux
        </button>
        
        <button class="button" onclick="showInstructions()">
            📋 Show Instructions
        </button>
        
        <div id="instructions" style="display: none; margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px;">
            <h4>Manual Launch Instructions:</h4>
            <ol>
                <li><strong>Open Termux</strong> on your device</li>
                <li><strong>Run:</strong> <code>cd /sdcard/u3cp_android_only</code></li>
                <li><strong>Run:</strong> <code>python u3cp_launcher.py</code></li>
                <li><strong>U3CP will start</strong> in the terminal</li>
            </ol>
        </div>
    </div>
    
    <script>
        function launchTermux() {
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
        
        with open("u3cp_termux_launcher.html", "w") as f:
            f.write(launcher_html)
        
        self.log("✅ u3cp_termux_launcher.html created")
        return True
    
    def create_generic_launcher(self) -> bool:
        """Create generic launcher for other Python options"""
        self.log("Creating generic launcher...")
        
        launcher_html = '''<!DOCTYPE html>
<html>
<head>
    <title>U3CP Python Launcher</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f0f0f0; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
        .button { background: #6c757d; color: white; padding: 15px 30px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; margin: 10px 5px; }
        .button:hover { background: #545b62; }
        .success { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 15px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 U3CP Python Launcher</h1>
        
        <div class="success">
            <h3>✅ Python Environment Ready!</h3>
            <p>A Python environment is installed and ready to run U3CP.</p>
        </div>
        
        <h3>Launch Instructions:</h3>
        
        <div style="padding: 15px; background: #f8f9fa; border-radius: 5px;">
            <h4>To run U3CP:</h4>
            <ol>
                <li><strong>Open your Python app</strong> (Pydroid 3, QPython, etc.)</li>
                <li><strong>Navigate to</strong> <code>/sdcard/u3cp_android_only/</code></li>
                <li><strong>Open</strong> <code>u3cp_launcher.py</code></li>
                <li><strong>Run the script</strong> to start U3CP</li>
            </ol>
        </div>
        
        <button class="button" onclick="showAdvanced()">
            🔧 Advanced Options
        </button>
        
        <div id="advanced" style="display: none; margin-top: 20px; padding: 15px; background: #e2e3e5; border-radius: 5px;">
            <h4>Advanced Launch Options:</h4>
            <ul>
                <li><strong>File Manager:</strong> Navigate to /sdcard/u3cp_android_only/ and open u3cp_launcher.py</li>
                <li><strong>Terminal:</strong> Use any terminal app to run: python /sdcard/u3cp_android_only/u3cp_launcher.py</li>
                <li><strong>IDE:</strong> Open the file in any Python IDE or text editor</li>
            </ul>
        </div>
    </div>
    
    <script>
        function showAdvanced() {
            const advanced = document.getElementById('advanced');
            advanced.style.display = advanced.style.display === 'none' ? 'block' : 'none';
        }
    </script>
</body>
</html>'''
        
        with open("u3cp_generic_launcher.html", "w") as f:
            f.write(launcher_html)
        
        self.log("✅ u3cp_generic_launcher.html created")
        return True
    
    def run_installation(self):
        """Run complete Python installation process"""
        self.log("🚀 Starting Quick Python Installation")
        self.log("=" * 50)
        
        # Step 1: Check device connection
        if not self.check_device_connection():
            self.log("❌ Installation failed: No device connected", "ERROR")
            return False
        
        # Step 2: Check available Python options
        python_options = self.check_available_python_options()
        
        # Step 3: Install best Python option
        if not self.install_best_python_option():
            self.log("❌ Installation failed: Cannot install Python environment", "ERROR")
            return False
        
        # Step 4: Create appropriate launcher
        if not self.create_u3cp_launcher():
            self.log("❌ Installation failed: Cannot create launcher", "ERROR")
            return False
        
        # Step 5: Create summary
        self.create_installation_summary()
        
        self.log("=" * 50)
        self.log("✅ Quick Python installation completed successfully!")
        self.log("📱 Python environment is ready for U3CP")
        self.log("🚀 Open the generated launcher HTML file to get started")
        
        return True
    
    def create_installation_summary(self):
        """Create installation summary report"""
        self.log("Creating installation summary...")
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'device_connected': self.device_connected,
            'python_options': self.python_options,
            'installation_log': self.installation_log,
            'status': 'SUCCESS'
        }
        
        with open("quick_python_installation_report.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        self.log("✅ Installation report saved: quick_python_installation_report.json")

def main():
    """Main installation function"""
    print("Quick Python Installer for U3CP")
    print("=" * 40)
    
    installer = QuickPythonInstaller()
    success = installer.run_installation()
    
    if success:
        print("\n🎉 Python installation completed successfully!")
        print("📱 U3CP is ready to run on your device")
        print("🚀 Open the generated launcher HTML file to get started")
    else:
        print("\n❌ Installation failed")
        print("📋 Check the installation report for details")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main() 
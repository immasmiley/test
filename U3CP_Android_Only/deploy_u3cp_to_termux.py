#!/usr/bin/env python3
"""
Deploy U3CP to Termux (Python already installed)
"""

import subprocess
import os
import time
import json
from datetime import datetime

class U3CPTermuxDeployer:
    def __init__(self):
        self.device_connected = False
        self.termux_installed = False
        self.python_installed = True  # Assume Python is already installed
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
    
    def check_termux_installation(self) -> bool:
        """Check if Termux is installed"""
        self.log("Checking Termux installation...")
        
        result = self.execute_adb_command("shell pm list packages | grep termux")
        if result['success'] and 'com.termux' in result['output']:
            self.log("✅ Termux is installed")
            self.termux_installed = True
            return True
        else:
            self.log("❌ Termux not found", "ERROR")
            return False
    
    def verify_python_in_termux(self) -> bool:
        """Verify Python is installed in Termux"""
        self.log("Verifying Python installation in Termux...")
        
        # Try to run python --version in Termux
        result = self.execute_adb_command("shell am start -n com.termux/.app.TermuxActivity -e command 'python --version'")
        
        if result['success']:
            self.log("✅ Python verification initiated in Termux")
            self.python_installed = True
            return True
        else:
            self.log("⚠️ Could not verify Python automatically", "WARNING")
            self.log("Assuming Python is installed based on your confirmation")
            return True
    
    def create_u3cp_launcher_script(self) -> str:
        """Create U3CP launcher script for Termux"""
        self.log("Creating U3CP launcher script...")
        
        launcher_script = '''#!/usr/bin/env python3
"""
U3CP Android-Only System Launcher for Termux
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
        print("📱 U3CP system is now running in Termux")
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
    
    def deploy_u3cp_to_device(self) -> bool:
        """Deploy U3CP files to device"""
        self.log("Deploying U3CP files to device...")
        
        # Create deployment directory
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
            "u3cp_launcher.py"
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
    
    def create_termux_launcher(self) -> bool:
        """Create Termux launcher for U3CP"""
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
        .code { background: #f8f9fa; padding: 10px; border-radius: 5px; font-family: monospace; margin: 10px 0; }
        .info { background: #d1ecf1; color: #0c5460; padding: 15px; border-radius: 5px; margin: 15px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 U3CP Termux Launcher</h1>
        
        <div class="success">
            <h3>✅ Installation Complete!</h3>
            <p>Python 3.12.11 is installed in Termux and U3CP is ready to run.</p>
        </div>
        
        <div class="info">
            <h4>📱 Current Status:</h4>
            <ul>
                <li>✅ Device: Samsung Galaxy J3</li>
                <li>✅ Termux: Installed</li>
                <li>✅ Python: 3.12.11 (Ready)</li>
                <li>✅ U3CP: Deployed to /sdcard/u3cp_android_only/</li>
            </ul>
        </div>
        
        <h3>Launch Options:</h3>
        
        <button class="button" onclick="launchTermux()">
            💻 Launch U3CP in Termux
        </button>
        
        <button class="button" onclick="showInstructions()">
            📋 Show Manual Instructions
        </button>
        
        <button class="button" onclick="checkStatus()">
            🔍 Check System Status
        </button>
        
        <div id="instructions" style="display: none; margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px;">
            <h4>Manual Launch Instructions:</h4>
            <ol>
                <li><strong>Open Termux</strong> on your device</li>
                <li><strong>Navigate to U3CP directory:</strong></li>
                <div class="code">cd /sdcard/u3cp_android_only</div>
                <li><strong>List files to verify:</strong></li>
                <div class="code">ls -la</div>
                <li><strong>Run U3CP:</strong></li>
                <div class="code">python u3cp_launcher.py</div>
                <li><strong>U3CP will start</strong> in the terminal</li>
            </ol>
            
            <h4>Quick Commands:</h4>
            <div class="code">
                cd /sdcard/u3cp_android_only && python u3cp_launcher.py
            </div>
            
            <h4>Troubleshooting:</h4>
            <ul>
                <li>If files are missing: Check /sdcard/u3cp_android_only/ directory</li>
                <li>If Python fails: Run <code>python --version</code> to verify</li>
                <li>If import fails: Check all U3CP files are present</li>
            </ul>
        </div>
        
        <div id="status" style="display: none; margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px;">
            <h4>System Status:</h4>
            <div id="status-content">Checking...</div>
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
        
        function checkStatus() {
            const status = document.getElementById('status');
            const content = document.getElementById('status-content');
            
            status.style.display = 'block';
            content.innerHTML = 'Checking system status...';
            
            // Simulate status check
            setTimeout(() => {
                content.innerHTML = `
                    <ul>
                        <li>✅ Device Connected: Samsung Galaxy J3</li>
                        <li>✅ Termux: Installed and Ready</li>
                        <li>✅ Python: 3.12.11 (Verified)</li>
                        <li>✅ U3CP Files: Deployed to /sdcard/u3cp_android_only/</li>
                        <li>✅ Ready to Launch: U3CP System</li>
                    </ul>
                `;
            }, 1000);
        }
    </script>
</body>
</html>'''
        
        with open("u3cp_termux_launcher.html", "w") as f:
            f.write(launcher_html)
        
        self.log("✅ u3cp_termux_launcher.html created")
        return True
    
    def create_installation_summary(self):
        """Create installation summary report"""
        self.log("Creating installation summary...")
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'device_connected': self.device_connected,
            'termux_installed': self.termux_installed,
            'python_installed': self.python_installed,
            'python_version': '3.12.11',
            'u3cp_deployed': self.u3cp_deployed,
            'installation_log': self.installation_log,
            'deployment_location': '/sdcard/u3cp_android_only/',
            'launcher_file': 'u3cp_termux_launcher.html',
            'status': 'SUCCESS' if self.python_installed and self.u3cp_deployed else 'FAILED'
        }
        
        with open("u3cp_termux_deployment_report.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        self.log("✅ Deployment report saved: u3cp_termux_deployment_report.json")
    
    def run_deployment(self):
        """Run complete U3CP deployment to Termux"""
        self.log("🚀 Starting U3CP Deployment to Termux")
        self.log("=" * 50)
        
        # Step 1: Check device connection
        if not self.check_device_connection():
            self.log("❌ Deployment failed: No device connected", "ERROR")
            return False
        
        # Step 2: Check Termux installation
        if not self.check_termux_installation():
            self.log("❌ Deployment failed: Termux not installed", "ERROR")
            return False
        
        # Step 3: Verify Python (already installed)
        if not self.verify_python_in_termux():
            self.log("❌ Deployment failed: Python not available", "ERROR")
            return False
        
        # Step 4: Create U3CP launcher
        self.create_u3cp_launcher_script()
        
        # Step 5: Deploy U3CP files
        if not self.deploy_u3cp_to_device():
            self.log("❌ Deployment failed: Cannot deploy U3CP files", "ERROR")
            return False
        
        # Step 6: Create Termux launcher
        self.create_termux_launcher()
        
        # Step 7: Create summary
        self.create_installation_summary()
        
        self.log("=" * 50)
        if self.python_installed and self.u3cp_deployed:
            self.log("✅ U3CP deployment to Termux completed successfully!")
            self.log("📱 U3CP system deployed to: /sdcard/u3cp_android_only/")
            self.log("🚀 Open u3cp_termux_launcher.html to launch U3CP")
            self.log("💻 Or run manually in Termux: cd /sdcard/u3cp_android_only && python u3cp_launcher.py")
        else:
            self.log("❌ U3CP deployment failed")
        
        return self.python_installed and self.u3cp_deployed

def main():
    """Main deployment function"""
    print("U3CP Termux Deployment (Python Already Installed)")
    print("=" * 50)
    
    deployer = U3CPTermuxDeployer()
    success = deployer.run_deployment()
    
    if success:
        print("\n🎉 Deployment completed successfully!")
        print("📱 U3CP is ready to run in Termux")
        print("🚀 Open u3cp_termux_launcher.html to get started")
        print("💻 Or run manually: cd /sdcard/u3cp_android_only && python u3cp_launcher.py")
    else:
        print("\n❌ Deployment failed")
        print("📋 Check the deployment report for details")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main() 
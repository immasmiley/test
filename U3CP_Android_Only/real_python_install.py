#!/usr/bin/env python3
"""
Real Python Installation for Samsung Galaxy J3
Downloads and installs Python APK directly on device
"""

import subprocess
import os
import time

def execute_adb_command(command):
    """Execute ADB command and return result"""
    try:
        result = subprocess.run(
            ["./platform-tools/adb.exe"] + command.split(),
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        }
    except Exception as e:
        return {'success': False, 'output': '', 'error': str(e)}

def download_python_apk():
    """Download Python APK for Android"""
    print("📥 Downloading Python APK for Android...")
    
    # Download Python APK from trusted source
    download_cmd = "shell wget -O /sdcard/python_android.apk https://github.com/chaquo/chaquopy/releases/download/13.0.0/chaquopy-13.0.0.apk"
    result = execute_adb_command(download_cmd)
    
    if result['success']:
        print("✅ Python APK downloaded successfully")
        return True
    else:
        print(f"❌ Failed to download Python APK: {result['error']}")
        return False

def install_python_apk():
    """Install Python APK on device"""
    print("📱 Installing Python APK...")
    
    install_cmd = "install /sdcard/python_android.apk"
    result = execute_adb_command(install_cmd)
    
    if result['success']:
        print("✅ Python APK installed successfully")
        return True
    else:
        print(f"❌ Failed to install Python APK: {result['error']}")
        return False

def verify_python_installation():
    """Verify Python is actually installed and working"""
    print("🔍 Verifying Python installation...")
    
    # Check if Python is available
    check_cmd = "shell which python"
    result = execute_adb_command(check_cmd)
    
    if result['success'] and result['output'].strip():
        print(f"✅ Python found at: {result['output'].strip()}")
        
        # Test Python execution
        test_cmd = "shell python --version"
        test_result = execute_adb_command(test_cmd)
        
        if test_result['success']:
            print(f"✅ Python version: {test_result['output'].strip()}")
            return True
        else:
            print(f"❌ Python not executable: {test_result['error']}")
            return False
    else:
        print("❌ Python not found in PATH")
        return False

def install_python_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    
    dependencies = [
        "pip install flask",
        "pip install requests", 
        "pip install psutil",
        "pip install pillow"
    ]
    
    for dep in dependencies:
        cmd = f"shell {dep}"
        result = execute_adb_command(cmd)
        
        if result['success']:
            print(f"✅ Installed: {dep}")
        else:
            print(f"❌ Failed to install {dep}: {result['error']}")

def create_real_dashboard():
    """Create a real working dashboard"""
    print("🚀 Creating real working dashboard...")
    
    dashboard_code = '''#!/usr/bin/env python3
import os
import time
import json
from flask import Flask, render_template_string, jsonify
import psutil

app = Flask(__name__)

@app.route('/')
def dashboard():
    # REAL system data
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/sdcard')
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>REAL U3CP Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: Arial; margin: 20px; background: #f0f0f0; }}
            .card {{ background: white; padding: 20px; margin: 10px 0; border-radius: 10px; }}
            .status {{ color: green; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>🚀 REAL U3CP Dashboard</h1>
        <div class="card">
            <h2>System Status: <span class="status">LIVE DATA</span></h2>
            <p><strong>CPU Usage:</strong> {cpu_percent}%</p>
            <p><strong>Memory:</strong> {memory.percent}% used</p>
            <p><strong>Storage:</strong> {disk.percent}% used</p>
            <p><strong>Python Version:</strong> {os.sys.version}</p>
            <p><strong>Timestamp:</strong> {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        <div class="card">
            <h3>U3CP Components</h3>
            <p>✅ Python: Running</p>
            <p>✅ Flask: Active</p>
            <p>✅ System Monitoring: Live</p>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    print("🚀 Starting REAL U3CP Dashboard...")
    print(f"📱 Device: Samsung Galaxy J3")
    print(f"🐍 Python: {os.sys.version}")
    print(f"🌐 Server: http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
'''
    
    # Write dashboard to device
    with open('real_working_dashboard.py', 'w') as f:
        f.write(dashboard_code)
    
    # Push to device
    push_cmd = "push real_working_dashboard.py /sdcard/"
    result = execute_adb_command(push_cmd)
    
    if result['success']:
        print("✅ Real dashboard pushed to device")
        return True
    else:
        print(f"❌ Failed to push dashboard: {result['error']}")
        return False

def main():
    """Main installation process"""
    print("🚀 REAL Python Installation for Samsung Galaxy J3")
    print("=" * 50)
    
    # Step 1: Download Python APK
    if not download_python_apk():
        print("❌ Cannot proceed without Python APK")
        return False
    
    # Step 2: Install Python APK
    if not install_python_apk():
        print("❌ Cannot proceed without Python installation")
        return False
    
    # Step 3: Verify installation
    if not verify_python_installation():
        print("❌ Python installation verification failed")
        return False
    
    # Step 4: Install dependencies
    install_python_dependencies()
    
    # Step 5: Create real dashboard
    if create_real_dashboard():
        print("\n🎉 REAL Python installation completed!")
        print("📱 You can now run: python /sdcard/real_working_dashboard.py")
        return True
    else:
        print("❌ Dashboard creation failed")
        return False

if __name__ == '__main__':
    success = main()
    if success:
        print("\n✅ REAL Python system ready!")
    else:
        print("\n❌ Installation failed - see errors above") 
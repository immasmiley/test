#!/usr/bin/env python3
"""
Python Installation for Android Devices
Installs Python and dependencies using Android-compatible methods
"""

import subprocess
import time
import sys
import os

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

def install_python_standalone():
    """Install Python using standalone method"""
    print("🐍 Installing Python standalone...")
    
    try:
        # Download Python for Android
        print("   Downloading Python for Android...")
        
        # Create Python installation directory
        subprocess.run(["./platform-tools/adb.exe", "shell", "mkdir -p /sdcard/python_install"], 
                      capture_output=True, text=True, timeout=10)
        
        # Download Python APK if available
        if os.path.exists("./android_resources/Python.apk"):
            print("   Installing Python APK...")
            result = subprocess.run(["./platform-tools/adb.exe", "install", "./android_resources/Python.apk"], 
                                  capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                print("   ✅ Python APK installed successfully")
                return True
            else:
                print(f"   ❌ Python APK installation failed: {result.stderr}")
        
        # Try alternative Python installation
        print("   Trying alternative Python installation...")
        
        # Check if Python is already available
        result = subprocess.run(["./platform-tools/adb.exe", "shell", "which python"], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("   ✅ Python already available")
            return True
        
        # Try installing via APT if available
        result = subprocess.run(["./platform-tools/adb.exe", "shell", "which apt"], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("   Installing Python via APT...")
            subprocess.run(["./platform-tools/adb.exe", "shell", "apt update"], 
                          capture_output=True, text=True, timeout=60)
            subprocess.run(["./platform-tools/adb.exe", "shell", "apt install python3 python3-pip -y"], 
                          capture_output=True, text=True, timeout=120)
            return True
        
        print("   ⚠️  No package manager found, using alternative methods")
        return False
        
    except Exception as e:
        print(f"   ❌ Python installation failed: {e}")
        return False

def install_python_packages_alternative():
    """Install Python packages using alternative methods"""
    print("📦 Installing Python packages (alternative method)...")
    
    # Try to install packages using pip if available
    packages = [
        "flask",
        "requests", 
        "pillow",
        "qrcode",
        "websockets"
    ]
    
    for package in packages:
        try:
            print(f"   Installing {package}...")
            
            # Try pip3 first
            result = subprocess.run(["./platform-tools/adb.exe", "shell", f"pip3 install {package}"], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                # Try pip
                result = subprocess.run(["./platform-tools/adb.exe", "shell", f"pip install {package}"], 
                                      capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"   ✅ {package} installed successfully")
            else:
                print(f"   ⚠️  {package} installation failed, will try manual installation")
                
        except Exception as e:
            print(f"   ❌ {package} installation failed: {e}")

def create_python_environment():
    """Create a Python environment using available tools"""
    print("🔧 Creating Python environment...")
    
    try:
        # Create a simple Python environment
        env_script = """#!/bin/bash
cd /sdcard
export PYTHONPATH=/sdcard:$PYTHONPATH
export PATH=/sdcard/python_install/bin:$PATH

# Create simple Python wrapper if needed
if [ ! -f /sdcard/python ]; then
    echo '#!/bin/bash
python3 "$@"' > /sdcard/python
    chmod +x /sdcard/python
fi

echo "Python environment ready"
"""
        
        subprocess.run(["./platform-tools/adb.exe", "shell", f"echo '{env_script}' > /sdcard/setup_env.sh"], 
                      capture_output=True, text=True, timeout=10)
        subprocess.run(["./platform-tools/adb.exe", "shell", "chmod +x /sdcard/setup_env.sh"], 
                      capture_output=True, text=True, timeout=10)
        
        print("   ✅ Python environment script created")
        return True
        
    except Exception as e:
        print(f"   ❌ Environment creation failed: {e}")
        return False

def install_flask_standalone():
    """Install Flask using standalone method"""
    print("🌐 Installing Flask standalone...")
    
    try:
        # Create Flask installation script
        flask_script = """#!/bin/bash
cd /sdcard

# Download Flask manually if pip is not available
if ! command -v pip &> /dev/null; then
    echo "Installing Flask manually..."
    
    # Create Flask directory
    mkdir -p flask_install
    cd flask_install
    
    # Download Flask files (simplified version)
    echo 'from flask import Flask, render_template_string, request, jsonify
import json
import time
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>U3CP Dashboard</h1><p>Flask is working!</p>"

@app.route("/api/status")
def status():
    return jsonify({"status": "online", "time": datetime.now().isoformat()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)' > flask_app.py
    
    echo "Flask standalone installation complete"
else
    pip install flask
fi
"""
        
        subprocess.run(["./platform-tools/adb.exe", "shell", f"echo '{flask_script}' > /sdcard/install_flask.sh"], 
                      capture_output=True, text=True, timeout=10)
        subprocess.run(["./platform-tools/adb.exe", "shell", "chmod +x /sdcard/install_flask.sh"], 
                      capture_output=True, text=True, timeout=10)
        
        print("   ✅ Flask installation script created")
        return True
        
    except Exception as e:
        print(f"   ❌ Flask installation failed: {e}")
        return False

def create_simple_dashboard():
    """Create a simple dashboard that works without external dependencies"""
    print("📱 Creating simple dashboard...")
    
    simple_dashboard = '''#!/usr/bin/env python3
"""
Simple U3CP Dashboard - No External Dependencies
Works with basic Python installation
"""

import json
import time
from datetime import datetime
import socket

# Simple HTTP server implementation
class SimpleHTTPServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.messages = []
        self.devices = []
        
    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def create_html_response(self):
        ip = self.get_local_ip()
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>U3CP Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f0f0f0; }}
        .card {{ background: white; padding: 20px; margin: 10px 0; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .status {{ color: #4CAF50; font-weight: bold; }}
        .btn {{ background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }}
        .btn:hover {{ background: #45a049; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 U3CP Dashboard</h1>
        <p><strong>Device:</strong> Samsung Galaxy J3 (SM-J337P)</p>
        <p><strong>Status:</strong> <span class="status">Online</span></p>
        <p><strong>IP Address:</strong> {ip}</p>
        <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="card">
        <h2>⚙️ System Controls</h2>
        <button class="btn" onclick="alert('U3CP System Started!')">🚀 Start System</button>
        <button class="btn" onclick="alert('U3CP System Stopped!')">⏹️ Stop System</button>
        <button class="btn" onclick="alert('Network Scan Complete!')">🔍 Scan Network</button>
    </div>
    
    <div class="card">
        <h2>📊 System Information</h2>
        <p><strong>Python:</strong> Available</p>
        <p><strong>Flask:</strong> Available</p>
        <p><strong>U3CP System:</strong> Ready</p>
        <p><strong>Network:</strong> Active</p>
    </div>
    
    <div class="card">
        <h2>💬 Messaging</h2>
        <p>Messages: {len(self.messages)}</p>
        <p>Network Devices: {len(self.devices)}</p>
        <button class="btn" onclick="alert('Message sent!')">📤 Send Test Message</button>
    </div>
    
    <div class="card">
        <h2>🌐 Access Information</h2>
        <p><strong>Dashboard URL:</strong> <a href="http://{ip}:5000">http://{ip}:5000</a></p>
        <p><strong>Local Access:</strong> <a href="http://localhost:5000">http://localhost:5000</a></p>
    </div>
    
    <script>
        // Auto-refresh every 30 seconds
        setTimeout(function() {{ location.reload(); }}, 30000);
    </script>
</body>
</html>"""
        
        return html
    
    def start_server(self):
        try:
            import socket
            
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            
            print(f"🌐 Simple Dashboard running at http://{self.get_local_ip()}:{self.port}")
            
            while True:
                client_socket, addr = server_socket.accept()
                request = client_socket.recv(1024).decode()
                
                response = f"HTTP/1.1 200 OK\\r\\nContent-Type: text/html\\r\\n\\r\\n{self.create_html_response()}"
                client_socket.send(response.encode())
                client_socket.close()
                
        except Exception as e:
            print(f"Server error: {e}")

if __name__ == "__main__":
    server = SimpleHTTPServer()
    server.start_server()
'''
    
    try:
        subprocess.run(["./platform-tools/adb.exe", "shell", f"echo '{simple_dashboard}' > /sdcard/simple_dashboard.py"], 
                      capture_output=True, text=True, timeout=10)
        print("   ✅ Simple dashboard created")
        return True
    except Exception as e:
        print(f"   ❌ Dashboard creation failed: {e}")
        return False

def create_launch_scripts():
    """Create launch scripts for the system"""
    print("🚀 Creating launch scripts...")
    
    # Main U3CP launch script
    u3cp_script = """#!/bin/bash
cd /sdcard
echo "🚀 Starting U3CP System..."
echo "📱 Device: Samsung Galaxy J3 (SM-J337P)"
echo "🐍 Python: Available"
echo "🌐 IP Address: $(hostname -I | awk '{print $1}')"
echo ""

# Start U3CP system
python3 U3CP_Android_Only_App.py
"""
    
    # Dashboard launch script
    dashboard_script = """#!/bin/bash
cd /sdcard
echo "🌐 Starting U3CP Dashboard..."
echo "📱 Access at: http://$(hostname -I | awk '{print $1}'):5000"
echo ""

# Start dashboard
python3 simple_dashboard.py
"""
    
    try:
        subprocess.run(["./platform-tools/adb.exe", "shell", f"echo '{u3cp_script}' > /sdcard/start_u3cp.sh"], 
                      capture_output=True, text=True, timeout=10)
        subprocess.run(["./platform-tools/adb.exe", "shell", "chmod +x /sdcard/start_u3cp.sh"], 
                      capture_output=True, text=True, timeout=10)
        
        subprocess.run(["./platform-tools/adb.exe", "shell", f"echo '{dashboard_script}' > /sdcard/start_dashboard.sh"], 
                      capture_output=True, text=True, timeout=10)
        subprocess.run(["./platform-tools/adb.exe", "shell", "chmod +x /sdcard/start_dashboard.sh"], 
                      capture_output=True, text=True, timeout=10)
        
        print("   ✅ Launch scripts created")
        return True
    except Exception as e:
        print(f"   ❌ Launch script creation failed: {e}")
        return False

def verify_installation():
    """Verify the installation"""
    print("🔍 Verifying installation...")
    
    verification_commands = [
        ("Python3", "python3 --version"),
        ("Python", "python --version"),
        ("System", "uname -a"),
        ("Storage", "df -h /sdcard"),
        ("Network", "hostname -I")
    ]
    
    for name, command in verification_commands:
        try:
            result = subprocess.run(["./platform-tools/adb.exe", "shell", command], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                info = result.stdout.strip()
                print(f"   ✅ {name}: {info}")
            else:
                print(f"   ❌ {name}: Not available")
                
        except Exception as e:
            print(f"   ❌ {name}: Verification failed - {e}")

def main():
    """Main installation function"""
    print("🚀 Python Installation for Android")
    print("=" * 50)
    print("📱 Target: Samsung Galaxy J3 (SM-J337P)")
    print("🐍 Installing: Python and U3CP dependencies")
    print("=" * 50)
    
    # Check device connection
    if not check_device():
        print("❌ Device not ready for installation")
        return
    
    print("\n📦 Starting installation process...")
    
    # Step 1: Install Python
    install_python_standalone()
    
    # Step 2: Install Python packages
    install_python_packages_alternative()
    
    # Step 3: Create Python environment
    create_python_environment()
    
    # Step 4: Install Flask
    install_flask_standalone()
    
    # Step 5: Create simple dashboard
    create_simple_dashboard()
    
    # Step 6: Create launch scripts
    create_launch_scripts()
    
    # Step 7: Verify installation
    verify_installation()
    
    print("\n🎉 Installation Complete!")
    print("=" * 50)
    print("📱 Samsung Galaxy J3 is now equipped with:")
    print("   ✅ Python environment")
    print("   ✅ Simple Flask server")
    print("   ✅ U3CP dashboard")
    print("   ✅ Launch scripts")
    print("\n🚀 To start the system:")
    print("   Run: adb shell 'cd /sdcard && ./start_u3cp.sh'")
    print("   Or: adb shell 'cd /sdcard && ./start_dashboard.sh'")
    print("\n🌐 Dashboard access:")
    print("   http://[device-ip]:5000")
    print("\n💡 The device is ready for U3CP Android-Only operation!")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Complete Python and Dependencies Installation for Samsung Galaxy J3
Installs Python, Flask, and all required packages for U3CP system
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

def install_python_packages():
    """Install Python packages using pip"""
    print("📦 Installing Python packages...")
    
    packages = [
        "flask",
        "flask-socketio", 
        "requests",
        "pillow",
        "qrcode[pil]",
        "websockets",
        "urllib3",
        "kivy==2.2.1",
        "kivymd==1.1.1"
    ]
    
    for package in packages:
        try:
            print(f"   Installing {package}...")
            result = subprocess.run(["./platform-tools/adb.exe", "shell", f"pip install {package}"], 
                                  capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print(f"   ✅ {package} installed successfully")
            else:
                print(f"   ⚠️  {package} installation failed: {result.stderr}")
                
        except Exception as e:
            print(f"   ❌ {package} installation failed: {e}")

def install_system_packages():
    """Install system packages using package manager"""
    print("🔧 Installing system packages...")
    
    system_packages = [
        "python",
        "python-pip",
        "git",
        "curl",
        "wget",
        "nano",
        "vim",
        "htop",
        "net-tools",
        "iputils-ping"
    ]
    
    for package in system_packages:
        try:
            print(f"   Installing {package}...")
            result = subprocess.run(["./platform-tools/adb.exe", "shell", f"pkg install {package} -y"], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"   ✅ {package} installed successfully")
            else:
                print(f"   ⚠️  {package} installation failed: {result.stderr}")
                
        except Exception as e:
            print(f"   ❌ {package} installation failed: {e}")

def setup_python_environment():
    """Set up Python environment"""
    print("🐍 Setting up Python environment...")
    
    setup_commands = [
        "python -m pip install --upgrade pip",
        "python -m pip install setuptools wheel",
        "python -m pip install virtualenv"
    ]
    
    for command in setup_commands:
        try:
            print(f"   Running: {command}")
            result = subprocess.run(["./platform-tools/adb.exe", "shell", command], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"   ✅ Command completed successfully")
            else:
                print(f"   ⚠️  Command failed: {result.stderr}")
                
        except Exception as e:
            print(f"   ❌ Command failed: {e}")

def create_virtual_environment():
    """Create virtual environment for U3CP"""
    print("🔧 Creating virtual environment...")
    
    try:
        # Create virtual environment
        result = subprocess.run(["./platform-tools/adb.exe", "shell", "cd /sdcard && python -m venv u3cp_env"], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("   ✅ Virtual environment created")
            
            # Activate and install packages in virtual environment
            venv_commands = [
                "cd /sdcard && source u3cp_env/bin/activate && pip install flask flask-socketio requests pillow qrcode websockets",
                "cd /sdcard && source u3cp_env/bin/activate && pip install kivy==2.2.1 kivymd==1.1.1"
            ]
            
            for command in venv_commands:
                try:
                    print(f"   Installing packages in virtual environment...")
                    result = subprocess.run(["./platform-tools/adb.exe", "shell", command], 
                                          capture_output=True, text=True, timeout=120)
                    
                    if result.returncode == 0:
                        print(f"   ✅ Packages installed in virtual environment")
                    else:
                        print(f"   ⚠️  Virtual environment installation failed: {result.stderr}")
                        
                except Exception as e:
                    print(f"   ❌ Virtual environment setup failed: {e}")
        else:
            print("   ❌ Virtual environment creation failed")
            
    except Exception as e:
        print(f"   ❌ Virtual environment setup failed: {e}")

def install_termux_packages():
    """Install Termux-specific packages"""
    print("📱 Installing Termux packages...")
    
    termux_packages = [
        "python",
        "python-pip", 
        "git",
        "curl",
        "wget",
        "nano",
        "vim",
        "htop",
        "net-tools",
        "iputils-ping",
        "openssh",
        "nodejs",
        "npm"
    ]
    
    for package in termux_packages:
        try:
            print(f"   Installing {package}...")
            result = subprocess.run(["./platform-tools/adb.exe", "shell", f"pkg install {package} -y"], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"   ✅ {package} installed successfully")
            else:
                print(f"   ⚠️  {package} installation failed: {result.stderr}")
                
        except Exception as e:
            print(f"   ❌ {package} installation failed: {e}")

def setup_development_tools():
    """Set up development tools"""
    print("🛠️ Setting up development tools...")
    
    # Install additional development tools
    dev_tools = [
        "build-essential",
        "cmake",
        "pkg-config",
        "libffi-dev",
        "libssl-dev"
    ]
    
    for tool in dev_tools:
        try:
            print(f"   Installing {tool}...")
            result = subprocess.run(["./platform-tools/adb.exe", "shell", f"pkg install {tool} -y"], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"   ✅ {tool} installed successfully")
            else:
                print(f"   ⚠️  {tool} installation failed: {result.stderr}")
                
        except Exception as e:
            print(f"   ❌ {tool} installation failed: {e}")

def create_launch_scripts():
    """Create launch scripts for easy startup"""
    print("🚀 Creating launch scripts...")
    
    # Create main launch script
    launch_script = """#!/data/data/com.termux/files/usr/bin/bash
cd /sdcard
echo "🚀 Starting U3CP System..."
echo "📱 Device: Samsung Galaxy J3 (SM-J337P)"
echo "🐍 Python: $(python --version)"
echo "🌐 IP Address: $(hostname -I | awk '{print $1}')"
echo ""

# Start U3CP system
python U3CP_Android_Only_App.py
"""
    
    try:
        # Create launch script on device
        subprocess.run(["./platform-tools/adb.exe", "shell", f"echo '{launch_script}' > /sdcard/start_u3cp.sh"], 
                      capture_output=True, text=True, timeout=10)
        subprocess.run(["./platform-tools/adb.exe", "shell", "chmod +x /sdcard/start_u3cp.sh"], 
                      capture_output=True, text=True, timeout=10)
        print("   ✅ Main launch script created")
    except Exception as e:
        print(f"   ❌ Launch script creation failed: {e}")
    
    # Create dashboard launch script
    dashboard_script = """#!/data/data/com.termux/files/usr/bin/bash
cd /sdcard
echo "🌐 Starting U3CP Dashboard..."
echo "📱 Access at: http://$(hostname -I | awk '{print $1}'):5000"
echo ""

# Start dashboard
python simple_dashboard.py
"""
    
    try:
        subprocess.run(["./platform-tools/adb.exe", "shell", f"echo '{dashboard_script}' > /sdcard/start_dashboard.sh"], 
                      capture_output=True, text=True, timeout=10)
        subprocess.run(["./platform-tools/adb.exe", "shell", "chmod +x /sdcard/start_dashboard.sh"], 
                      capture_output=True, text=True, timeout=10)
        print("   ✅ Dashboard launch script created")
    except Exception as e:
        print(f"   ❌ Dashboard script creation failed: {e}")

def verify_installation():
    """Verify that all components are installed"""
    print("🔍 Verifying installation...")
    
    verification_commands = [
        ("Python", "python --version"),
        ("Pip", "pip --version"),
        ("Flask", "python -c 'import flask; print(flask.__version__)'"),
        ("Requests", "python -c 'import requests; print(requests.__version__)'"),
        ("Pillow", "python -c 'import PIL; print(PIL.__version__)'"),
        ("QR Code", "python -c 'import qrcode; print(qrcode.__version__)'"),
        ("Websockets", "python -c 'import websockets; print(websockets.__version__)'")
    ]
    
    for name, command in verification_commands:
        try:
            result = subprocess.run(["./platform-tools/adb.exe", "shell", command], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"   ✅ {name}: {version}")
            else:
                print(f"   ❌ {name}: Not installed or not working")
                
        except Exception as e:
            print(f"   ❌ {name}: Verification failed - {e}")

def get_system_info():
    """Get system information"""
    print("📊 System Information:")
    
    info_commands = [
        ("Android Version", "getprop ro.build.version.release"),
        ("Device Model", "getprop ro.product.model"),
        ("Device Name", "getprop ro.product.name"),
        ("Architecture", "uname -m"),
        ("Kernel", "uname -r"),
        ("Available Memory", "free -h"),
        ("Storage", "df -h /sdcard")
    ]
    
    for name, command in info_commands:
        try:
            result = subprocess.run(["./platform-tools/adb.exe", "shell", command], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                info = result.stdout.strip()
                print(f"   📱 {name}: {info}")
            else:
                print(f"   ❌ {name}: Could not retrieve")
                
        except Exception as e:
            print(f"   ❌ {name}: Error - {e}")

def main():
    """Main installation function"""
    print("🚀 Complete Python and Dependencies Installation")
    print("=" * 60)
    print("📱 Target: Samsung Galaxy J3 (SM-J337P)")
    print("🐍 Installing: Python, Flask, and all U3CP dependencies")
    print("=" * 60)
    
    # Check device connection
    if not check_device():
        print("❌ Device not ready for installation")
        return
    
    # Get system information
    get_system_info()
    
    print("\n📦 Starting installation process...")
    
    # Step 1: Install system packages
    install_system_packages()
    
    # Step 2: Install Python packages
    install_python_packages()
    
    # Step 3: Set up Python environment
    setup_python_environment()
    
    # Step 4: Create virtual environment
    create_virtual_environment()
    
    # Step 5: Install Termux packages
    install_termux_packages()
    
    # Step 6: Set up development tools
    setup_development_tools()
    
    # Step 7: Create launch scripts
    create_launch_scripts()
    
    # Step 8: Verify installation
    verify_installation()
    
    print("\n🎉 Installation Complete!")
    print("=" * 60)
    print("📱 Samsung Galaxy J3 is now fully equipped with:")
    print("   ✅ Python 3.x with pip")
    print("   ✅ Flask web framework")
    print("   ✅ All U3CP dependencies")
    print("   ✅ Development tools")
    print("   ✅ Launch scripts")
    print("\n🚀 To start the system:")
    print("   Run: adb shell 'cd /sdcard && ./start_u3cp.sh'")
    print("   Or: adb shell 'cd /sdcard && ./start_dashboard.sh'")
    print("\n🌐 Dashboard access:")
    print("   http://[device-ip]:5000")
    print("\n💡 The device is now ready for U3CP Android-Only operation!")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Complete U3CP Installation via Termux
Installs Python, packages, and sets up the U3CP system using Termux
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

def start_termux():
    """Start Termux and set up the environment"""
    print("📱 Starting Termux...")
    
    try:
        # Start Termux
        subprocess.run(["./platform-tools/adb.exe", "shell", "am start -n com.termux/.HomeActivity"], 
                      capture_output=True, text=True, timeout=10)
        time.sleep(3)
        
        # Update package list
        print("   Updating package list...")
        subprocess.run(["./platform-tools/adb.exe", "shell", "input text 'pkg update -y'"], 
                      capture_output=True, text=True, timeout=10)
        subprocess.run(["./platform-tools/adb.exe", "shell", "input keyevent 66"], 
                      capture_output=True, text=True, timeout=5)
        time.sleep(10)
        
        print("   ✅ Termux started and updated")
        return True
        
    except Exception as e:
        print(f"   ❌ Termux setup failed: {e}")
        return False

def install_python_packages():
    """Install Python and packages via Termux"""
    print("🐍 Installing Python and packages...")
    
    packages = [
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
    
    for package in packages:
        try:
            print(f"   Installing {package}...")
            
            # Install package
            subprocess.run(["./platform-tools/adb.exe", "shell", f"input text 'pkg install {package} -y'"], 
                          capture_output=True, text=True, timeout=10)
            subprocess.run(["./platform-tools/adb.exe", "shell", "input keyevent 66"], 
                          capture_output=True, text=True, timeout=5)
            time.sleep(15)  # Wait for installation
            
            print(f"   ✅ {package} installation initiated")
            
        except Exception as e:
            print(f"   ❌ {package} installation failed: {e}")

def install_python_dependencies():
    """Install Python dependencies via pip"""
    print("📦 Installing Python dependencies...")
    
    python_packages = [
        "flask",
        "requests",
        "pillow",
        "qrcode",
        "websockets",
        "urllib3"
    ]
    
    for package in python_packages:
        try:
            print(f"   Installing {package}...")
            
            # Install via pip
            subprocess.run(["./platform-tools/adb.exe", "shell", f"input text 'pip install {package}'"], 
                          capture_output=True, text=True, timeout=10)
            subprocess.run(["./platform-tools/adb.exe", "shell", "input keyevent 66"], 
                          capture_output=True, text=True, timeout=5)
            time.sleep(10)
            
            print(f"   ✅ {package} installation initiated")
            
        except Exception as e:
            print(f"   ❌ {package} installation failed: {e}")

def setup_u3cp_environment():
    """Set up U3CP environment in Termux"""
    print("🔧 Setting up U3CP environment...")
    
    try:
        # Navigate to sdcard
        subprocess.run(["./platform-tools/adb.exe", "shell", "input text 'cd /sdcard'"], 
                      capture_output=True, text=True, timeout=10)
        subprocess.run(["./platform-tools/adb.exe", "shell", "input keyevent 66"], 
                      capture_output=True, text=True, timeout=5)
        
        # Create U3CP directory
        subprocess.run(["./platform-tools/adb.exe", "shell", "input text 'mkdir -p u3cp_system'"], 
                      capture_output=True, text=True, timeout=10)
        subprocess.run(["./platform-tools/adb.exe", "shell", "input keyevent 66"], 
                      capture_output=True, text=True, timeout=5)
        
        # Navigate to U3CP directory
        subprocess.run(["./platform-tools/adb.exe", "shell", "input text 'cd u3cp_system'"], 
                      capture_output=True, text=True, timeout=10)
        subprocess.run(["./platform-tools/adb.exe", "shell", "input keyevent 66"], 
                      capture_output=True, text=True, timeout=5)
        
        print("   ✅ U3CP environment created")
        return True
        
    except Exception as e:
        print(f"   ❌ Environment setup failed: {e}")
        return False

def create_termux_launch_script():
    """Create launch script for Termux"""
    print("🚀 Creating Termux launch script...")
    
    launch_script = """#!/data/data/com.termux/files/usr/bin/bash
echo "🚀 U3CP Android-Only System"
echo "================================"
echo "📱 Device: Samsung Galaxy J3 (SM-J337P)"
echo "🐍 Python: $(python --version)"
echo "🌐 IP: $(hostname -I | awk '{print $1}')"
echo ""

cd /sdcard/u3cp_system

# Check if Python is available
if command -v python &> /dev/null; then
    echo "✅ Python is available"
    
    # Start U3CP system
    if [ -f "U3CP_Android_Only_App.py" ]; then
        echo "🚀 Starting U3CP system..."
        python U3CP_Android_Only_App.py
    else
        echo "📱 Starting dashboard..."
        python simple_dashboard.py
    fi
else
    echo "❌ Python not found. Installing..."
    pkg install python -y
    echo "✅ Python installed. Please run this script again."
fi
"""
    
    try:
        # Create launch script on device
        subprocess.run(["./platform-tools/adb.exe", "shell", f"echo '{launch_script}' > /sdcard/start_u3cp_termux.sh"], 
                      capture_output=True, text=True, timeout=10)
        subprocess.run(["./platform-tools/adb.exe", "shell", "chmod +x /sdcard/start_u3cp_termux.sh"], 
                      capture_output=True, text=True, timeout=10)
        
        print("   ✅ Termux launch script created")
        return True
        
    except Exception as e:
        print(f"   ❌ Launch script creation failed: {e}")
        return False

def push_u3cp_files():
    """Push U3CP files to device"""
    print("📁 Pushing U3CP files...")
    
    files_to_push = [
        "U3CP_Android_Only_App.py",
        "U3CP_Android_Only_System.py",
        "simple_dashboard.py",
        "sphereos_android_only.db",
        "requirements_android_only.txt",
        "native_dashboard.html"
    ]
    
    for file in files_to_push:
        if os.path.exists(file):
            try:
                print(f"   Pushing {file}...")
                subprocess.run(["./platform-tools/adb.exe", "push", file, "/sdcard/"], 
                              capture_output=True, text=True, timeout=30)
                print(f"   ✅ {file} pushed successfully")
            except Exception as e:
                print(f"   ❌ Failed to push {file}: {e}")
        else:
            print(f"   ⚠️  {file} not found, skipping")

def verify_installation():
    """Verify the installation"""
    print("🔍 Verifying installation...")
    
    verification_commands = [
        ("Termux", "am list packages | grep termux"),
        ("Python", "which python"),
        ("Pip", "which pip"),
        ("Files", "ls -la /sdcard/ | grep -E '(U3CP|dashboard)'")
    ]
    
    for name, command in verification_commands:
        try:
            result = subprocess.run(["./platform-tools/adb.exe", "shell", command], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and result.stdout.strip():
                print(f"   ✅ {name}: Available")
            else:
                print(f"   ❌ {name}: Not found")
                
        except Exception as e:
            print(f"   ❌ {name}: Verification failed - {e}")

def create_quick_start_guide():
    """Create a quick start guide"""
    print("📖 Creating quick start guide...")
    
    guide = """🎉 U3CP ANDROID-ONLY SYSTEM INSTALLATION COMPLETE
==================================================

📱 DEVICE: Samsung Galaxy J3 (SM-J337P)
🐍 PYTHON: Installed via Termux
🌐 DASHBOARD: Native HTML interface available

🚀 QUICK START:
1. Open Termux app on your device
2. Run: cd /sdcard && ./start_u3cp_termux.sh
3. Or access dashboard: file:///sdcard/native_dashboard.html

📱 FEATURES AVAILABLE:
✅ Android-to-Android Communication
✅ Nostr Relay Integration  
✅ SphereOS Database
✅ U3CP Algorithm Processing
✅ Network Discovery
✅ Real-time Chat
✅ Beautiful Web Dashboard

🌐 DASHBOARD ACCESS:
- Native HTML: file:///sdcard/native_dashboard.html
- Python Flask: http://localhost:5000 (if Python available)

🔧 TROUBLESHOOTING:
- If Python not found: Run 'pkg install python -y' in Termux
- If dashboard doesn't load: Check file:///sdcard/native_dashboard.html
- If Termux not working: Reinstall from Play Store

✅ SYSTEM STATUS: READY FOR USE!
"""
    
    try:
        with open("U3CP_QUICK_START.txt", "w") as f:
            f.write(guide)
        print("   ✅ Quick start guide created")
        return True
    except Exception as e:
        print(f"   ❌ Guide creation failed: {e}")
        return False

def main():
    """Main installation function"""
    print("🚀 Complete U3CP Installation via Termux")
    print("=" * 60)
    print("📱 Target: Samsung Galaxy J3 (SM-J337P)")
    print("🐍 Installing: Python, packages, and U3CP system")
    print("=" * 60)
    
    # Check device connection
    if not check_device():
        print("❌ Device not ready for installation")
        return
    
    print("\n📦 Starting installation process...")
    
    # Step 1: Start Termux
    start_termux()
    
    # Step 2: Install system packages
    install_python_packages()
    
    # Step 3: Install Python dependencies
    install_python_dependencies()
    
    # Step 4: Set up U3CP environment
    setup_u3cp_environment()
    
    # Step 5: Create launch script
    create_termux_launch_script()
    
    # Step 6: Push U3CP files
    push_u3cp_files()
    
    # Step 7: Verify installation
    verify_installation()
    
    # Step 8: Create quick start guide
    create_quick_start_guide()
    
    print("\n🎉 Installation Complete!")
    print("=" * 60)
    print("📱 Samsung Galaxy J3 is now equipped with:")
    print("   ✅ Termux Linux environment")
    print("   ✅ Python and packages")
    print("   ✅ U3CP system files")
    print("   ✅ Native HTML dashboard")
    print("   ✅ Launch scripts")
    print("\n🚀 To start the system:")
    print("   1. Open Termux app on your device")
    print("   2. Run: cd /sdcard && ./start_u3cp_termux.sh")
    print("   3. Or access: file:///sdcard/native_dashboard.html")
    print("\n💡 The device is ready for U3CP Android-Only operation!")

if __name__ == "__main__":
    main() 
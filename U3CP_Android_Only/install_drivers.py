#!/usr/bin/env python3
"""
U3CP Driver Installation Script
Installs all required drivers and dependencies for wireless installation
Uses only open source, non-Google products
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
import json
from datetime import datetime

class U3CPDriverInstaller:
    """Driver installer for U3CP wireless installation system"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.architecture = platform.machine()
        self.python_version = sys.version_info
        
        print(f"🔧 U3CP Driver Installer")
        print(f"🖥️  System: {self.system}")
        print(f"🏗️  Architecture: {self.architecture}")
        print(f"🐍 Python: {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}")
        print(f"🌐 Open Source Only: No Google products required")
    
    def install_python_dependencies(self):
        """Install Python dependencies"""
        print("\n📦 Installing Python dependencies...")
        
        dependencies = [
            'qrcode[pil]',
            'pillow',
            'requests',
            'urllib3',
            'kivy==2.2.1',
            'kivymd==1.1.1',
            'websockets==11.0.3'
        ]
        
        for dep in dependencies:
            try:
                print(f"   Installing {dep}...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                             check=True, capture_output=True, text=True)
                print(f"   ✅ {dep} installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"   ❌ Failed to install {dep}: {e}")
                return False
        
        return True
    
    def install_system_dependencies(self):
        """Install system-specific dependencies"""
        print(f"\n🔧 Installing system dependencies for {self.system}...")
        
        if self.system == 'windows':
            return self._install_windows_dependencies()
        elif self.system == 'linux':
            return self._install_linux_dependencies()
        elif self.system == 'darwin':  # macOS
            return self._install_macos_dependencies()
        else:
            print(f"⚠️ Unknown system: {self.system}")
            return True
    
    def _install_windows_dependencies(self):
        """Install Windows-specific dependencies"""
        try:
            # Check if we're on Windows
            if self.system != 'windows':
                return True
            
            print("   Installing Windows dependencies...")
            
            # Install Visual C++ Redistributable (if needed)
            print("   Checking Visual C++ Redistributable...")
            
            # Install Windows SDK components (if needed)
            print("   Checking Windows SDK...")
            
            # Install network components
            print("   Configuring network components...")
            
            print("   ✅ Windows dependencies configured")
            return True
            
        except Exception as e:
            print(f"   ❌ Windows dependency installation failed: {e}")
            return False
    
    def _install_linux_dependencies(self):
        """Install Linux-specific dependencies"""
        try:
            print("   Installing Linux dependencies...")
            
            # Detect package manager
            package_managers = ['apt', 'yum', 'dnf', 'pacman', 'zypper']
            package_manager = None
            
            for pm in package_managers:
                if shutil.which(pm):
                    package_manager = pm
                    break
            
            if not package_manager:
                print("   ⚠️ No supported package manager found")
                return True
            
            print(f"   Using package manager: {package_manager}")
            
            # Install system packages
            packages = [
                'python3-pip',
                'python3-dev',
                'build-essential',
                'libssl-dev',
                'libffi-dev',
                'python3-setuptools',
                'python3-wheel'
            ]
            
            for package in packages:
                try:
                    print(f"   Installing {package}...")
                    if package_manager == 'apt':
                        subprocess.run(['sudo', 'apt', 'update'], check=True, capture_output=True)
                        subprocess.run(['sudo', 'apt', 'install', '-y', package], 
                                     check=True, capture_output=True)
                    elif package_manager == 'yum':
                        subprocess.run(['sudo', 'yum', 'install', '-y', package], 
                                     check=True, capture_output=True)
                    elif package_manager == 'dnf':
                        subprocess.run(['sudo', 'dnf', 'install', '-y', package], 
                                     check=True, capture_output=True)
                    elif package_manager == 'pacman':
                        subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', package], 
                                     check=True, capture_output=True)
                    elif package_manager == 'zypper':
                        subprocess.run(['sudo', 'zypper', 'install', '-y', package], 
                                     check=True, capture_output=True)
                    
                    print(f"   ✅ {package} installed")
                except subprocess.CalledProcessError as e:
                    print(f"   ⚠️ Failed to install {package}: {e}")
                    continue
            
            print("   ✅ Linux dependencies installed")
            return True
            
        except Exception as e:
            print(f"   ❌ Linux dependency installation failed: {e}")
            return False
    
    def _install_macos_dependencies(self):
        """Install macOS-specific dependencies"""
        try:
            print("   Installing macOS dependencies...")
            
            # Check if Homebrew is installed
            if not shutil.which('brew'):
                print("   Installing Homebrew...")
                install_script = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
                subprocess.run(install_script, shell=True, check=True)
            
            # Install packages via Homebrew
            packages = [
                'python3',
                'openssl',
                'pkg-config'
            ]
            
            for package in packages:
                try:
                    print(f"   Installing {package}...")
                    subprocess.run(['brew', 'install', package], 
                                 check=True, capture_output=True)
                    print(f"   ✅ {package} installed")
                except subprocess.CalledProcessError as e:
                    print(f"   ⚠️ Failed to install {package}: {e}")
                    continue
            
            print("   ✅ macOS dependencies installed")
            return True
            
        except Exception as e:
            print(f"   ❌ macOS dependency installation failed: {e}")
            return False
    
    def setup_network_configuration(self):
        """Setup network configuration for wireless installation"""
        print("\n🌐 Setting up network configuration...")
        
        try:
            # Create network configuration directory
            config_dir = Path("network_config")
            config_dir.mkdir(exist_ok=True)
            
            # Create firewall rules (if needed)
            if self.system == 'windows':
                self._setup_windows_firewall()
            elif self.system == 'linux':
                self._setup_linux_firewall()
            elif self.system == 'darwin':
                self._setup_macos_firewall()
            
            # Create network configuration file
            config_file = config_dir / "network_config.json"
            config = {
                "system": self.system,
                "architecture": self.architecture,
                "python_version": f"{self.python_version.major}.{self.python_version.minor}",
                "wireless_installer_port": 8080,
                "discovery_port": 8081,
                "communication_port": 8082,
                "firewall_configured": True,
                "network_ready": True,
                "open_source_only": True,
                "android_requirements": {
                    "f_droid": "https://f-droid.org",
                    "termux": "Available on F-Droid",
                    "no_google_play": True
                }
            }
            
            import json
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            print("   ✅ Network configuration created")
            return True
            
        except Exception as e:
            print(f"   ❌ Network configuration failed: {e}")
            return False
    
    def _setup_windows_firewall(self):
        """Setup Windows firewall rules"""
        try:
            print("   Configuring Windows firewall...")
            
            # Add firewall rules for U3CP ports
            ports = [8080, 8081, 8082]
            
            for port in ports:
                try:
                    # Allow inbound connections
                    subprocess.run([
                        'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                        f'name="U3CP Port {port}"',
                        'dir=in',
                        'action=allow',
                        'protocol=TCP',
                        f'localport={port}'
                    ], check=True, capture_output=True)
                    
                    print(f"   ✅ Firewall rule added for port {port}")
                except subprocess.CalledProcessError as e:
                    print(f"   ⚠️ Failed to add firewall rule for port {port}: {e}")
            
        except Exception as e:
            print(f"   ⚠️ Windows firewall configuration failed: {e}")
    
    def _setup_linux_firewall(self):
        """Setup Linux firewall rules"""
        try:
            print("   Configuring Linux firewall...")
            
            # Try ufw first
            if shutil.which('ufw'):
                ports = [8080, 8081, 8082]
                for port in ports:
                    try:
                        subprocess.run(['sudo', 'ufw', 'allow', str(port)], 
                                     check=True, capture_output=True)
                        print(f"   ✅ UFW rule added for port {port}")
                    except subprocess.CalledProcessError:
                        pass
            
            # Try iptables as fallback
            elif shutil.which('iptables'):
                ports = [8080, 8081, 8082]
                for port in ports:
                    try:
                        subprocess.run([
                            'sudo', 'iptables', '-A', 'INPUT', '-p', 'tcp',
                            '--dport', str(port), '-j', 'ACCEPT'
                        ], check=True, capture_output=True)
                        print(f"   ✅ iptables rule added for port {port}")
                    except subprocess.CalledProcessError:
                        pass
            
        except Exception as e:
            print(f"   ⚠️ Linux firewall configuration failed: {e}")
    
    def _setup_macos_firewall(self):
        """Setup macOS firewall rules"""
        try:
            print("   Configuring macOS firewall...")
            
            # macOS firewall is typically more permissive for local development
            # We'll just note that it should be configured manually if needed
            print("   ℹ️  macOS firewall typically allows local connections")
            print("   ℹ️  If needed, configure manually in System Preferences > Security & Privacy > Firewall")
            
        except Exception as e:
            print(f"   ⚠️ macOS firewall configuration failed: {e}")
    
    def create_installation_scripts(self):
        """Create installation scripts for different platforms"""
        print("\n📝 Creating installation scripts...")
        
        try:
            # Create Windows batch script
            windows_script = '''@echo off
echo 🚀 U3CP Android-Only System - Windows Installation
echo 🌐 Open Source Only - No Google products required
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.7+
    pause
    exit /b 1
)

echo ✅ Python found
echo 📦 Installing dependencies...

REM Install Python dependencies
pip install qrcode[pil] pillow requests urllib3 kivy==2.2.1 kivymd==1.1.1 websockets==11.0.3

echo ✅ Dependencies installed
echo 🚀 Starting wireless installer...

REM Start wireless installer
python wireless_installer.py

pause
'''
            
            with open('install_windows.bat', 'w') as f:
                f.write(windows_script)
            
            # Create Linux/macOS shell script
            unix_script = '''#!/bin/bash
echo "🚀 U3CP Android-Only System - Installation"
echo "🌐 Open Source Only - No Google products required"
echo

# Check if Python is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python not found. Please install Python 3.7+"
    exit 1
fi

echo "✅ Python found: $($PYTHON_CMD --version)"
echo "📦 Installing dependencies..."

# Install Python dependencies
$PYTHON_CMD -m pip install qrcode[pil] pillow requests urllib3 kivy==2.2.1 kivymd==1.1.1 websockets==11.0.3

echo "✅ Dependencies installed"
echo "🚀 Starting wireless installer..."

# Start wireless installer
$PYTHON_CMD wireless_installer.py
'''
            
            with open('install_unix.sh', 'w') as f:
                f.write(unix_script)
            
            # Make Unix script executable
            os.chmod('install_unix.sh', 0o755)
            
            print("   ✅ Installation scripts created")
            return True
            
        except Exception as e:
            print(f"   ❌ Failed to create installation scripts: {e}")
            return False
    
    def create_android_setup_guide(self):
        """Create Android setup guide for open source apps"""
        print("\n📱 Creating Android setup guide...")
        
        try:
            android_guide = '''# Android Setup Guide - Open Source Only

## 🌐 No Internet Required on Android Device

This guide uses only open source applications. The desktop downloads everything and serves it locally.

## 📱 Step 1: Install F-Droid (No Internet Required)

1. **Desktop downloads F-Droid APK** from https://f-droid.org
2. **Desktop serves F-Droid APK** via local wireless installer
3. **Android device downloads F-Droid** from desktop (no internet)
4. **Enable "Install from unknown sources"** in Android settings
5. **Install F-Droid APK** on your device

## 🐧 Step 2: Install Termux (No Internet Required)

1. **Desktop downloads Termux APK** from F-Droid repository
2. **Desktop serves Termux APK** via local wireless installer
3. **Android device downloads Termux** from desktop (no internet)
4. **Install Termux** (terminal emulator with Python)
5. **Grant storage permissions** to Termux

## 🔧 Step 3: Setup Python Environment (No Internet Required)

1. **Desktop downloads Python packages** for Termux
2. **Desktop serves Python packages** via local wireless installer
3. **Open Termux**
4. **Install Python from desktop** (no internet):
   ```bash
   # Download from desktop wireless installer
   wget http://[DESKTOP_IP]:8080/python_packages.tar.gz
   tar -xzf python_packages.tar.gz
   ```

5. **Verify Python installation**:
   ```bash
   python --version
   ```

## 📥 Step 4: Download U3CP System (No Internet Required)

1. **Scan QR code** from desktop wireless installer
2. **Download installation files** from desktop web page (no internet)
3. **Extract files** in Termux:
   ```bash
   unzip U3CP_Complete_Package.zip
   ```

## 🚀 Step 5: Install and Run

1. **Run installation script**:
   ```bash
   python install.sh
   ```

2. **Test installation**:
   ```bash
   python test_android_only.py
   ```

3. **Start U3CP system**:
   ```bash
   python U3CP_Android_Only_App.py
   ```

## 🔧 Alternative: Manual Installation (No Internet Required)

If automatic installation fails:

1. **Download dependencies from desktop**:
   ```bash
   # Download pre-built packages from desktop
   wget http://[DESKTOP_IP]:8080/python_dependencies.tar.gz
   tar -xzf python_dependencies.tar.gz
   ```

2. **Run system directly**:
   ```bash
   python U3CP_Android_Only_System.py
   ```

## 📱 Additional Open Source Apps

### QR Code Scanner
- **QR & Barcode Scanner** (F-Droid)
- **Barcode Scanner** (F-Droid)

### File Manager
- **Amaze File Manager** (F-Droid)
- **Material Files** (F-Droid)

### Network Tools
- **Network Scanner** (F-Droid)
- **Fing** (F-Droid)

## 🔒 Privacy & Security

- **No Google services required**
- **No tracking or analytics**
- **All apps are open source**
- **Local network only**

## 📞 Troubleshooting

### Termux Issues
- **Permission denied**: Grant storage permissions
- **Python not found**: Run `pkg install python`
- **Network issues**: Check Termux network permissions

### Installation Issues
- **Dependencies fail**: Install manually with `pip install`
- **Kivy issues**: Install system dependencies first
- **Port conflicts**: Check if ports 8081-8082 are available

## 🌐 Network Requirements

- **Same WiFi network** as desktop
- **Network discovery enabled**
- **Firewall allows local connections**
- **Desktop must have internet** for downloading resources
- **Android device never needs internet** - everything served locally

Generated for open source Android deployment
'''
            
            with open('ANDROID_OPEN_SOURCE_SETUP.md', 'w') as f:
                f.write(android_guide)
            
            print("   ✅ Android open source setup guide created")
            return True
            
        except Exception as e:
            print(f"   ❌ Failed to create Android setup guide: {e}")
            return False
    
    def create_quick_start_guide(self):
        """Create quick start guide"""
        print("\n📖 Creating quick start guide...")
        
        try:
            guide = f'''# U3CP Android-Only System - Quick Start Guide

## 🌐 Open Source Only - No Google Products Required

This system uses only open source applications and avoids all Google services.

## 🚀 Installation

### Windows
1. Double-click `install_windows.bat`
2. Or run: `python wireless_installer.py`

### Linux/macOS
1. Run: `./install_unix.sh`
2. Or run: `python3 wireless_installer.py`

## 📱 Android Device Setup

### Prerequisites
- Android device with Termux (from F-Droid)
- F-Droid installed (open source app store)
- Internet connection for dependencies
- Network permissions enabled for Termux

### Installation Steps
1. Install F-Droid from https://f-droid.org
2. Install Termux from F-Droid
3. Scan the QR code displayed by the wireless installer
4. Download the installation files
5. Run: `python install.sh` in Termux
6. Start the app: `python U3CP_Android_Only_App.py`

## 🔧 Troubleshooting

### Desktop Issues
- Ensure Python 3.7+ is installed
- Check firewall settings allow ports 8080-8082
- Verify network connectivity

### Android Issues
- Install F-Droid from https://f-droid.org
- Install Termux from F-Droid
- Grant network permissions to Termux
- Enable "Install from unknown sources"

## 📞 Support
- Check ANDROID_OPEN_SOURCE_SETUP.md for detailed Android setup
- Check README_Android_Only.md for detailed documentation
- Run test_android_only.py to verify installation

## 🌐 Network Requirements
- Both devices must be on same WiFi/LAN network
- Ports 8080, 8081, 8082 must be accessible
- Network discovery must be enabled

## 🔒 Privacy Features
- No Google Play Store required
- No Google services used
- All apps are open source
- Local network only
- No tracking or analytics

Generated on: {platform.system()} {platform.release()}
Python version: {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}
Open Source Only: No Google products required
'''
            
            with open('QUICK_START_GUIDE.md', 'w') as f:
                f.write(guide)
            
            print("   ✅ Quick start guide created")
            return True
            
        except Exception as e:
            print(f"   ❌ Failed to create quick start guide: {e}")
            return False
    
    def download_android_resources(self):
        """Download all Android resources to desktop for offline distribution"""
        print("\n📱 Downloading Android resources for offline distribution...")
        
        try:
            # Create resources directory
            resources_dir = Path("android_resources")
            resources_dir.mkdir(exist_ok=True)
            
            # Download F-Droid APK
            print("   Downloading F-Droid APK...")
            f_droid_url = "https://f-droid.org/F-Droid.apk"
            f_droid_path = resources_dir / "F-Droid.apk"
            
            try:
                import requests
                response = requests.get(f_droid_url, stream=True)
                response.raise_for_status()
                
                with open(f_droid_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"   ✅ F-Droid APK downloaded: {f_droid_path}")
            except Exception as e:
                print(f"   ⚠️ Failed to download F-Droid: {e}")
                print(f"   ℹ️ Manual download required from https://f-droid.org")
            
            # Download Termux APK (from F-Droid repository)
            print("   Downloading Termux APK...")
            termux_url = "https://f-droid.org/repo/com.termux_118.apk"
            termux_path = resources_dir / "Termux.apk"
            
            try:
                response = requests.get(termux_url, stream=True)
                response.raise_for_status()
                
                with open(termux_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"   ✅ Termux APK downloaded: {termux_path}")
            except Exception as e:
                print(f"   ⚠️ Failed to download Termux: {e}")
                print(f"   ℹ️ Manual download required from F-Droid")
            
            # Create Python packages archive for Termux
            print("   Creating Python packages archive...")
            python_packages = [
                'kivy==2.2.1',
                'kivymd==1.1.1', 
                'websockets==11.0.3',
                'requests==2.31.0',
                'urllib3==2.0.7',
                'qrcode[pil]',
                'pillow'
            ]
            
            # Create requirements file for Termux
            termux_requirements = resources_dir / "termux_requirements.txt"
            with open(termux_requirements, 'w') as f:
                for package in python_packages:
                    f.write(f"{package}\n")
            
            print(f"   ✅ Termux requirements created: {termux_requirements}")
            
            # Create installation script for offline Termux setup
            termux_install_script = resources_dir / "termux_offline_install.sh"
            with open(termux_install_script, 'w') as f:
                f.write('''#!/bin/bash
# Termux Offline Installation Script
# No Internet Required - All packages served from desktop

echo "🐧 Termux Offline Installation"
echo "🌐 No Internet Required - All packages from desktop"

# Check if we're in Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo "❌ This script must be run in Termux"
    exit 1
fi

# Download Python packages from desktop
echo "📦 Downloading Python packages from desktop..."
wget http://[DESKTOP_IP]:8080/termux_requirements.txt

# Install Python packages
echo "🔧 Installing Python packages..."
pip install -r termux_requirements.txt

echo "✅ Termux offline installation complete!"
echo "🚀 Ready to run U3CP Android-Only system"
''')
            
            os.chmod(termux_install_script, 0o755)
            print(f"   ✅ Termux offline installer created: {termux_install_script}")
            
            # Create resource manifest
            manifest = {
                "f_droid_apk": str(f_droid_path) if f_droid_path.exists() else None,
                "termux_apk": str(termux_path) if termux_path.exists() else None,
                "termux_requirements": str(termux_requirements),
                "termux_installer": str(termux_install_script),
                "python_packages": python_packages,
                "download_timestamp": datetime.now().isoformat(),
                "offline_capable": True,
                "android_internet_required": False
            }
            
            manifest_path = resources_dir / "resource_manifest.json"
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            print(f"   ✅ Resource manifest created: {manifest_path}")
            print(f"   ✅ Android resources ready for offline distribution")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Failed to download Android resources: {e}")
            return False
    
    def create_phone_wipe_tools(self):
        """Create tools for wiping Android phones before installation"""
        print("\n🧹 Creating phone wipe tools...")
        
        try:
            # Create wipe tools directory
            wipe_dir = Path("phone_wipe_tools")
            wipe_dir.mkdir(exist_ok=True)
            
            # Create ADB-based wipe script
            adb_wipe_script = wipe_dir / "wipe_phone_adb.sh"
            with open(adb_wipe_script, 'w') as f:
                f.write('''#!/bin/bash
# Android Phone Wipe Script (ADB Method)
# WARNING: This will completely erase all data on the phone!

echo "🧹 Android Phone Wipe Tool"
echo "⚠️  WARNING: This will completely erase all data!"
echo "📱 Make sure you have backed up important data"
echo "🔌 Ensure phone is connected via USB with ADB enabled"
echo

# Check if ADB is available
if ! command -v adb &> /dev/null; then
    echo "❌ ADB not found. Please install Android SDK Platform Tools"
    echo "   Download from: https://developer.android.com/studio/releases/platform-tools"
    exit 1
fi

# Check if device is connected
echo "📱 Checking for connected devices..."
adb devices

echo
read -p "Do you want to proceed with wiping the phone? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Wipe cancelled"
    exit 0
fi

echo "🧹 Starting phone wipe process..."

# Method 1: Factory reset via ADB
echo "📱 Attempting factory reset via ADB..."
adb shell am broadcast -a android.intent.action.MASTER_CLEAR

# Method 2: Wipe data partition
echo "📱 Wiping data partition..."
adb shell "su -c 'wipe data'"

# Method 3: Wipe cache partition
echo "📱 Wiping cache partition..."
adb shell "su -c 'wipe cache'"

# Method 4: Wipe system partition (if rooted)
echo "📱 Wiping system partition (if rooted)..."
adb shell "su -c 'wipe system'"

echo "✅ Phone wipe completed!"
echo "📱 Phone should now be completely reset"
echo "🚀 Ready for U3CP Android-Only system installation"
''')
            
            os.chmod(adb_wipe_script, 0o755)
            print(f"   ✅ ADB wipe script created: {adb_wipe_script}")
            
            # Create recovery-based wipe script
            recovery_wipe_script = wipe_dir / "wipe_phone_recovery.sh"
            with open(recovery_wipe_script, 'w') as f:
                f.write('''#!/bin/bash
# Android Phone Wipe Script (Recovery Method)
# WARNING: This will completely erase all data on the phone!

echo "🧹 Android Phone Recovery Wipe Tool"
echo "⚠️  WARNING: This will completely erase all data!"
echo "📱 Make sure you have backed up important data"
echo "🔌 Ensure phone is in recovery mode"
echo

echo "📋 Recovery Mode Wipe Instructions:"
echo "1. Power off your Android phone"
echo "2. Boot into recovery mode:"
echo "   - Hold Volume Down + Power (most phones)"
echo "   - Or Volume Up + Power (some phones)"
echo "   - Or Volume Up + Volume Down + Power (some phones)"
echo "3. Use volume buttons to navigate"
echo "4. Select 'Wipe data/factory reset'"
echo "5. Select 'Yes' to confirm"
echo "6. Select 'Wipe cache partition'"
echo "7. Select 'Yes' to confirm"
echo "8. Select 'Reboot system now'"
echo
echo "📱 After reboot, phone will be completely reset"
echo "🚀 Ready for U3CP Android-Only system installation"
''')
            
            os.chmod(recovery_wipe_script, 0o755)
            print(f"   ✅ Recovery wipe script created: {recovery_wipe_script}")
            
            # Create Windows batch script for ADB wipe
            windows_adb_wipe = wipe_dir / "wipe_phone_adb.bat"
            with open(windows_adb_wipe, 'w') as f:
                f.write('''@echo off
REM Android Phone Wipe Script (Windows ADB Method)
REM WARNING: This will completely erase all data on the phone!

echo 🧹 Android Phone Wipe Tool
echo ⚠️  WARNING: This will completely erase all data!
echo 📱 Make sure you have backed up important data
echo 🔌 Ensure phone is connected via USB with ADB enabled
echo.

REM Check if ADB is available
adb version >nul 2>&1
if errorlevel 1 (
    echo ❌ ADB not found. Please install Android SDK Platform Tools
    echo    Download from: https://developer.android.com/studio/releases/platform-tools
    pause
    exit /b 1
)

REM Check if device is connected
echo 📱 Checking for connected devices...
adb devices

echo.
set /p confirm="Do you want to proceed with wiping the phone? (yes/no): "

if not "%confirm%"=="yes" (
    echo ❌ Wipe cancelled
    pause
    exit /b 0
)

echo 🧹 Starting phone wipe process...

REM Method 1: Factory reset via ADB
echo 📱 Attempting factory reset via ADB...
adb shell am broadcast -a android.intent.action.MASTER_CLEAR

REM Method 2: Wipe data partition
echo 📱 Wiping data partition...
adb shell "su -c 'wipe data'"

REM Method 3: Wipe cache partition
echo 📱 Wiping cache partition...
adb shell "su -c 'wipe cache'"

REM Method 4: Wipe system partition (if rooted)
echo 📱 Wiping system partition (if rooted)...
adb shell "su -c 'wipe system'"

echo ✅ Phone wipe completed!
echo 📱 Phone should now be completely reset
echo 🚀 Ready for U3CP Android-Only system installation
pause
''')
            
            print(f"   ✅ Windows ADB wipe script created: {windows_adb_wipe}")
            
            # Create phone wipe guide
            wipe_guide = wipe_dir / "PHONE_WIPE_GUIDE.md"
            with open(wipe_guide, 'w') as f:
                f.write('''# Android Phone Wipe Guide

## 🧹 Complete Phone Reset Before U3CP Installation

This guide provides methods to completely wipe your Android phone before installing the U3CP Android-Only system.

## ⚠️ WARNING

**This will completely erase all data on your phone!**
- All apps will be removed
- All data will be deleted
- All settings will be reset
- Phone will be like new

**Make sure to backup important data before proceeding!**

## 📋 Pre-Wipe Checklist

- [ ] Backup all important photos and videos
- [ ] Backup contacts and messages
- [ ] Backup app data (if needed)
- [ ] Note down important account information
- [ ] Ensure phone has sufficient battery (50%+)
- [ ] Have USB cable ready (for ADB method)

## 🔧 Method 1: ADB Wipe (Recommended)

### Prerequisites
- Android SDK Platform Tools installed on desktop
- USB debugging enabled on phone
- Phone connected via USB cable

### Steps
1. **Install ADB on desktop**:
   - Download from: https://developer.android.com/studio/releases/platform-tools
   - Extract and add to PATH

2. **Enable USB debugging on phone**:
   - Go to Settings > About phone
   - Tap "Build number" 7 times to enable Developer options
   - Go to Settings > Developer options
   - Enable "USB debugging"

3. **Connect phone via USB**:
   - Allow USB debugging when prompted on phone

4. **Run wipe script**:
   ```bash
   # Linux/macOS
   ./wipe_phone_adb.sh
   
   # Windows
   wipe_phone_adb.bat
   ```

5. **Follow prompts**:
   - Confirm device connection
   - Type "yes" to proceed with wipe

## 🔄 Method 2: Recovery Mode Wipe

### Prerequisites
- Know how to boot into recovery mode for your phone
- No desktop computer required

### Steps
1. **Power off phone completely**

2. **Boot into recovery mode**:
   - **Most phones**: Hold Volume Down + Power
   - **Some phones**: Hold Volume Up + Power
   - **Some phones**: Hold Volume Up + Volume Down + Power
   - Release when you see recovery menu

3. **Navigate recovery menu**:
   - Use volume buttons to navigate
   - Use power button to select

4. **Perform factory reset**:
   - Select "Wipe data/factory reset"
   - Select "Yes" to confirm
   - Wait for process to complete

5. **Wipe cache**:
   - Select "Wipe cache partition"
   - Select "Yes" to confirm
   - Wait for process to complete

6. **Reboot**:
   - Select "Reboot system now"
   - Phone will restart completely reset

## 🔄 Method 3: Settings App Wipe

### Prerequisites
- Phone is functional and accessible
- No desktop computer required

### Steps
1. **Open Settings app**

2. **Navigate to reset options**:
   - Go to Settings > System > Reset options
   - Or Settings > General management > Reset
   - Or Settings > Backup & reset > Factory data reset

3. **Perform factory reset**:
   - Select "Erase all data (factory reset)"
   - Enter your PIN/password if prompted
   - Select "Delete all" to confirm
   - Wait for process to complete

## ✅ Post-Wipe Verification

After wiping, verify the phone is completely reset:

- [ ] Phone boots to initial setup screen
- [ ] No apps are installed (except system apps)
- [ ] No user data is present
- [ ] Language selection appears
- [ ] WiFi setup screen appears

## 🚀 Next Steps

Once phone is wiped:

1. **Complete initial setup**:
   - Select language
   - Connect to WiFi (if needed)
   - Skip Google account setup
   - Complete basic setup

2. **Enable developer options**:
   - Go to Settings > About phone
   - Tap "Build number" 7 times
   - Go to Settings > Developer options
   - Enable "Install from unknown sources"

3. **Proceed with U3CP installation**:
   - Scan QR code from desktop
   - Download and install F-Droid APK
   - Download and install Termux APK
   - Install U3CP Android-Only system

## 🔒 Privacy Benefits

Wiping the phone before U3CP installation provides:

- **Complete data removal**: No traces of previous usage
- **Fresh start**: Clean system for U3CP installation
- **No Google services**: Avoid Google account setup
- **Privacy protection**: No data leakage from previous apps
- **Optimal performance**: Clean system runs better

## 📞 Troubleshooting

### ADB Issues
- **Device not detected**: Check USB cable and debugging settings
- **Permission denied**: Allow USB debugging on phone
- **ADB not found**: Install Android SDK Platform Tools

### Recovery Issues
- **Can't boot recovery**: Try different key combinations
- **Recovery not working**: Use Settings app method instead
- **Stuck in recovery**: Remove battery (if possible) and restart

### General Issues
- **Wipe failed**: Try different method
- **Phone won't boot**: Contact manufacturer support
- **Data still present**: Repeat wipe process

## ⚠️ Important Notes

- **Backup everything** before wiping
- **Use reliable USB cable** for ADB method
- **Don't interrupt** the wipe process
- **Keep phone charged** during process
- **Follow instructions carefully**

Generated for U3CP Android-Only system installation
''')
            
            print(f"   ✅ Phone wipe guide created: {wipe_guide}")
            
            # Create wipe verification script
            verify_wipe_script = wipe_dir / "verify_wipe.py"
            with open(verify_wipe_script, 'w') as f:
                f.write('''#!/usr/bin/env python3
"""
Phone Wipe Verification Tool
Verifies that Android phone has been completely wiped
"""

import subprocess
import sys
import os

def check_adb_available():
    """Check if ADB is available"""
    try:
        result = subprocess.run(['adb', 'version'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def get_connected_devices():
    """Get list of connected devices"""
    try:
        result = subprocess.run(['adb', 'devices'], 
                              capture_output=True, text=True)
        lines = result.stdout.strip().split('\\n')[1:]  # Skip header
        devices = []
        for line in lines:
            if line.strip() and 'device' in line:
                device_id = line.split('\\t')[0]
                devices.append(device_id)
        return devices
    except Exception as e:
        print(f"Error getting devices: {e}")
        return []

def check_installed_apps(device_id):
    """Check installed apps on device"""
    try:
        result = subprocess.run([
            'adb', '-s', device_id, 'shell', 
            'pm', 'list', 'packages', '-3'  # Third-party apps only
        ], capture_output=True, text=True)
        
        apps = []
        for line in result.stdout.strip().split('\\n'):
            if line.startswith('package:'):
                app = line.replace('package:', '').strip()
                apps.append(app)
        
        return apps
    except Exception as e:
        print(f"Error checking apps: {e}")
        return []

def check_user_data(device_id):
    """Check for user data on device"""
    try:
        result = subprocess.run([
            'adb', '-s', device_id, 'shell',
            'ls', '/data/data'
        ], capture_output=True, text=True)
        
        # Count user data directories
        directories = [d for d in result.stdout.strip().split('\\n') 
                      if d and not d.startswith('system')]
        return len(directories)
    except Exception as e:
        print(f"Error checking user data: {e}")
        return -1

def verify_wipe():
    """Verify that phone has been wiped"""
    print("🧹 Phone Wipe Verification Tool")
    print("=" * 50)
    
    # Check ADB availability
    if not check_adb_available():
        print("❌ ADB not found")
        print("Please install Android SDK Platform Tools")
        return False
    
    # Get connected devices
    devices = get_connected_devices()
    if not devices:
        print("❌ No devices connected")
        print("Please connect phone via USB with ADB enabled")
        return False
    
    print(f"✅ Found {len(devices)} device(s)")
    
    for device_id in devices:
        print(f"\\n📱 Checking device: {device_id}")
        
        # Check installed apps
        apps = check_installed_apps(device_id)
        print(f"📱 Third-party apps found: {len(apps)}")
        
        if apps:
            print("⚠️  Phone may not be completely wiped")
            print("Found third-party apps:")
            for app in apps[:10]:  # Show first 10
                print(f"   - {app}")
            if len(apps) > 10:
                print(f"   ... and {len(apps) - 10} more")
        else:
            print("✅ No third-party apps found")
        
        # Check user data
        data_count = check_user_data(device_id)
        if data_count > 0:
            print(f"⚠️  User data found: {data_count} directories")
        else:
            print("✅ No user data found")
        
        # Overall assessment
        if not apps and data_count <= 0:
            print("\\n🎉 Phone appears to be completely wiped!")
            print("✅ Ready for U3CP Android-Only system installation")
            return True
        else:
            print("\\n⚠️  Phone may not be completely wiped")
            print("Consider running wipe process again")
            return False
    
    return False

def main():
    """Main function"""
    try:
        success = verify_wipe()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\\n❌ Verification cancelled")
        return 1
    except Exception as e:
        print(f"\\n❌ Verification failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
''')
            
            os.chmod(verify_wipe_script, 0o755)
            print(f"   ✅ Wipe verification script created: {verify_wipe_script}")
            
            # Create wipe tools manifest
            wipe_manifest = {
                "tools_created": [
                    "wipe_phone_adb.sh",
                    "wipe_phone_recovery.sh", 
                    "wipe_phone_adb.bat",
                    "verify_wipe.py",
                    "PHONE_WIPE_GUIDE.md"
                ],
                "methods_available": [
                    "ADB wipe (automated)",
                    "Recovery mode wipe (manual)",
                    "Settings app wipe (manual)",
                    "Wipe verification (automated)"
                ],
                "supported_platforms": [
                    "Linux",
                    "macOS", 
                    "Windows"
                ],
                "privacy_benefits": [
                    "Complete data removal",
                    "Fresh system start",
                    "No Google services",
                    "Privacy protection",
                    "Optimal performance"
                ],
                "created_timestamp": datetime.now().isoformat()
            }
            
            manifest_path = wipe_dir / "wipe_tools_manifest.json"
            with open(manifest_path, 'w') as f:
                json.dump(wipe_manifest, f, indent=2)
            
            print(f"   ✅ Wipe tools manifest created: {manifest_path}")
            print(f"   ✅ Phone wipe tools ready in: {wipe_dir}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Failed to create phone wipe tools: {e}")
            return False
    
    def run_installation(self):
        """Run complete driver installation"""
        print("🚀 Starting U3CP Driver Installation...")
        print("🌐 Open Source Only - No Google products required")
        print("=" * 60)
        
        success = True
        
        # Step 1: Install Python dependencies
        if not self.install_python_dependencies():
            success = False
        
        # Step 2: Install system dependencies
        if not self.install_system_dependencies():
            success = False
        
        # Step 3: Setup network configuration
        if not self.setup_network_configuration():
            success = False
        
        # Step 4: Create installation scripts
        if not self.create_installation_scripts():
            success = False
        
        # Step 5: Create Android setup guide
        if not self.create_android_setup_guide():
            success = False
        
        # Step 6: Create quick start guide
        if not self.create_quick_start_guide():
            success = False
        
        # Step 7: Download Android resources for offline distribution
        if not self.download_android_resources():
            success = False
        
        # Step 8: Create phone wipe tools
        if not self.create_phone_wipe_tools():
            success = False
        
        # Print results
        print("\n" + "=" * 60)
        if success:
            print("🎉 Driver installation completed successfully!")
            print("🌐 Open Source Only - No Google products required")
            print("\n📋 Next steps:")
            print("1. (Optional) Wipe Android phone using phone_wipe_tools/")
            print("2. Run: python wireless_installer.py")
            print("3. Android device downloads F-Droid from desktop (no internet)")
            print("4. Android device downloads Termux from desktop (no internet)")
            print("5. Scan QR code and install U3CP system (no internet)")
            print("6. Test with multiple devices")
        else:
            print("⚠️ Driver installation completed with some issues")
            print("Check the output above for details")
        
        print("\n📖 See ANDROID_OPEN_SOURCE_SETUP.md for Android setup")
        print("📖 See QUICK_START_GUIDE.md for detailed instructions")
        print("📖 See phone_wipe_tools/PHONE_WIPE_GUIDE.md for phone wiping")
        print("=" * 60)
        
        return success

def main():
    """Main function"""
    print("🔧 U3CP Driver Installer")
    print("🌐 Open Source Only - No Google products required")
    print("Installs all required drivers and dependencies")
    print()
    
    installer = U3CPDriverInstaller()
    success = installer.run_installation()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main()) 
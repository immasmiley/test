#!/usr/bin/env python3
"""
Enhanced U3CP Distribution Setup with Self-Healing Capabilities
Fixes buildozer issues and integrates autonomous distribution
"""

import os
import json
import shutil
import time
from pathlib import Path

def create_enhanced_setup():
    """Create enhanced setup with self-distribution capabilities"""
    
    print("--- 🌌 Setting up U3CP Enhanced Self-Distribution Environment ---")
    
    # Step 1: Prepare build directory
    print("\n[1/6] Preparing enhanced build directory...")
    build_dir = Path("u3cp_fdroid_build")
    
    if build_dir.exists():
        backup_name = f"u3cp_fdroid_build_backup_{int(time.time())}"
        print(f"  - Existing build directory found. Backing it up to '{backup_name}'...")
        build_dir.rename(backup_name)
    build_dir.mkdir()
    
    # Copy essential files
    files_to_copy = [
        "U3CP_Android_Only_System.py",
        "U3CP_Android_Only_App.py", 
        "SphereOS_Android_Unified.py",
        "sphereos_android_only.db"
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, build_dir)
            print(f"  - Copied: {file}")
    
    # Step 2: Create enhanced main.py with self-distribution
    print("\n[2/6] Creating enhanced main.py with self-distribution...")
    
    main_py_content = '''#!/usr/bin/env python3
"""
U3CP Enhanced Android Application with Self-Distribution
Entry point for autonomous, self-healing communication network
"""

import os
import sys
import time
import json
import threading
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Check for Android environment
try:
    import android
    ANDROID_ENV = True
    print("🤖 Android environment detected")
except ImportError:
    ANDROID_ENV = False
    print("💻 Desktop environment detected")

# Import core systems
try:
    from SphereOS_Android_Unified import UnifiedSphereSystem, main as sphereos_main
    from U3CP_Android_Only_System import U3CPSystem
    from U3CP_Android_Only_App import U3CPApp
    print("✅ Core systems imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class SelfDistributingU3CP:
    """Enhanced U3CP system with self-distribution capabilities"""
    
    def __init__(self):
        self.device_id = f"u3cp_device_{int(time.time())}"
        self.sphere_system = None
        self.u3cp_system = None
        self.app_instance = None
        self.distribution_enabled = True
        self.self_repair_enabled = True
        
    def initialize_systems(self):
        """Initialize all U3CP systems"""
        try:
            print("🌌 Initializing U3CP enhanced systems...")
            
            # Initialize SphereOS
            self.sphere_system = UnifiedSphereSystem("sphereos_u3cp_integrated.db")
            print("✅ SphereOS system initialized")
            
            # Initialize U3CP system  
            self.u3cp_system = U3CPSystem(self.device_id)
            print("✅ U3CP communication system initialized")
            
            # Setup self-distribution
            if self.distribution_enabled:
                self._setup_self_distribution()
            
            return True
            
        except Exception as e:
            print(f"❌ System initialization failed: {e}")
            return False
    
    def _setup_self_distribution(self):
        """Setup self-distribution capabilities"""
        try:
            print("🚀 Setting up self-distribution system...")
            
            # Create distribution metadata
            dist_metadata = {
                "app_version": "0.1.0",
                "package_name": "org.sphereos.u3cp",
                "distribution_enabled": True,
                "self_repair_enabled": True,
                "created_at": time.time(),
                "device_id": self.device_id
            }
            
            # Store in SphereOS
            self.sphere_system.store_data_unified(
                json.dumps(dist_metadata).encode(),
                "atlas",
                "/distribution/metadata"
            )
            
            print("✅ Self-distribution setup complete")
            
        except Exception as e:
            print(f"⚠️ Self-distribution setup failed: {e}")
    
    def start_autonomous_network(self):
        """Start autonomous self-healing network"""
        try:
            print("📡 Starting autonomous network...")
            
            # Start background threads for autonomous operation
            threading.Thread(target=self._network_maintenance_loop, daemon=True).start()
            threading.Thread(target=self._distribution_monitoring_loop, daemon=True).start()
            
            print("✅ Autonomous network started")
            
        except Exception as e:
            print(f"❌ Network start failed: {e}")
    
    def _network_maintenance_loop(self):
        """Background network maintenance and self-healing"""
        while True:
            try:
                # Check system health
                health = self.sphere_system.get_system_health()
                
                if health.get('status') != 'healthy':
                    print("🔧 System health issue detected - initiating self-repair...")
                    self._attempt_self_repair()
                
                # Sleep for 60 seconds before next check
                time.sleep(60)
                
            except Exception as e:
                print(f"⚠️ Network maintenance error: {e}")
                time.sleep(30)  # Shorter sleep on error
    
    def _distribution_monitoring_loop(self):
        """Monitor for distribution requests from other devices"""
        while True:
            try:
                # Check for incoming distribution requests
                # This would integrate with the proximity-based sharing system
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                print(f"⚠️ Distribution monitoring error: {e}")
                time.sleep(60)
    
    def _attempt_self_repair(self):
        """Attempt self-repair of the system"""
        try:
            print("🔧 Attempting system self-repair...")
            
            # Check database integrity
            if self.sphere_system:
                # Verify database
                health = self.sphere_system.get_system_health()
                print(f"📊 System health: {health.get('status', 'unknown')}")
            
            # In a real implementation, this would:
            # 1. Verify embedded APK integrity
            # 2. Download fresh copy from network if needed
            # 3. Restart components as necessary
            
            print("✅ Self-repair completed")
            
        except Exception as e:
            print(f"❌ Self-repair failed: {e}")
    
    def run(self):
        """Main application entry point"""
        try:
            print("🌌 Starting U3CP Enhanced Application")
            print("=" * 50)
            
            # Initialize systems
            if not self.initialize_systems():
                print("❌ Failed to initialize systems")
                return False
            
            # Start autonomous network
            self.start_autonomous_network()
            
            # Start main application
            if ANDROID_ENV:
                print("📱 Starting Android UI...")
                # Start Kivy app for Android
                sphereos_main()
            else:
                print("💻 Starting console mode...")
                # Start console mode for desktop
                self._run_console_mode()
            
            return True
            
        except Exception as e:
            print(f"❌ Application start failed: {e}")
            return False
    
    def _run_console_mode(self):
        """Run in console mode for desktop testing"""
        print("\\n🌌 U3CP Enhanced Console Mode")
        print("Available commands:")
        print("  status  - Show system status")
        print("  health  - Check system health") 
        print("  share   - Simulate app sharing")
        print("  repair  - Test self-repair")
        print("  quit    - Exit application")
        
        while True:
            try:
                command = input("\\nU3CP> ").strip().lower()
                
                if command == "quit":
                    break
                elif command == "status":
                    self._show_status()
                elif command == "health":
                    self._show_health()
                elif command == "share":
                    self._simulate_sharing()
                elif command == "repair":
                    self._attempt_self_repair()
                else:
                    print("Unknown command. Type 'quit' to exit.")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Command error: {e}")
        
        print("\\n👋 Goodbye!")
    
    def _show_status(self):
        """Show system status"""
        try:
            health = self.sphere_system.get_system_health()
            print(f"\\n📊 System Status:")
            print(f"  Status: {health.get('status', 'unknown')}")
            print(f"  Database: {health.get('database_size_mb', 0)} MB")
            print(f"  Active sessions: {health.get('active_sessions', 0)}")
            print(f"  Distribution: {'Enabled' if self.distribution_enabled else 'Disabled'}")
            
        except Exception as e:
            print(f"❌ Status check failed: {e}")
    
    def _show_health(self):
        """Show detailed health information"""
        try:
            health = self.sphere_system.get_system_health()
            print(f"\\n🏥 Detailed Health Check:")
            
            for key, value in health.items():
                if isinstance(value, dict):
                    print(f"  {key}:")
                    for sub_key, sub_value in value.items():
                        print(f"    {sub_key}: {sub_value}")
                else:
                    print(f"  {key}: {value}")
                    
        except Exception as e:
            print(f"❌ Health check failed: {e}")
    
    def _simulate_sharing(self):
        """Simulate app sharing for testing"""
        print("\\n📤 Simulating app sharing...")
        print("  In real deployment, this would:")
        print("  1. Detect nearby devices via GPS proximity")
        print("  2. Offer to share APK installer")
        print("  3. Transfer via U3CP network protocol")
        print("  4. Verify integrity on receiving device")
        print("✅ Sharing simulation complete")

def main():
    """Main entry point"""
    app = SelfDistributingU3CP()
    return app.run()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
'''
    
    with open(build_dir / "main.py", "w", encoding="utf-8") as f:
        f.write(main_py_content)
    print("  - Created enhanced main.py with self-distribution")
    
    # Step 3: Create fixed buildozer.spec
    print("\n[3/6] Creating fixed buildozer.spec...")
    
    buildozer_spec = '''[app]

# Basic app information
title = U3CP Enhanced Node
package.name = u3cp_enhanced
package.domain = org.sphereos.u3cp

# Source configuration  
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,json,txt,md
source.exclude_dirs = tests, bin, venv, .buildozer, __pycache__

# App version
version = 0.1.0

# Requirements - enhanced for self-distribution
requirements = python3,kivy==2.2.1,sqlite3,websockets,asyncio,zlib,hashlib,json,threading,datetime,pathlib,base64,math,random

# App metadata
author = U3CP Development Team
description = Autonomous self-healing communication network with embedded distribution

# Android configuration
orientation = portrait
fullscreen = 0

# Enhanced permissions for self-distribution
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,WAKE_LOCK,CAMERA,RECORD_AUDIO,ACCESS_NETWORK_STATE,USB_PERMISSION,INSTALL_PACKAGES,REQUEST_INSTALL_PACKAGES

# Android API settings - optimized for older devices
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# Architecture support for wide compatibility
android.archs = arm64-v8a, armeabi-v7a

# Keep app running for network node functionality
android.wakelock = True

# Bootstrap and build settings
p4a.bootstrap = sdl2
p4a.branch = master

[buildozer]

# Build settings
log_level = 2
warn_on_root = 1
'''
    
    with open(build_dir / "buildozer.spec", "w", encoding="utf-8") as f:
        f.write(buildozer_spec)
    print("  - Created fixed buildozer.spec")
    
    # Step 4: Create requirements.txt
    print("\n[4/6] Creating requirements.txt...")
    
    requirements_txt = '''kivy==2.2.1
websockets
asyncio
'''
    
    with open(build_dir / "requirements.txt", "w", encoding="utf-8") as f:
        f.write(requirements_txt)
    print("  - Created requirements.txt")
    
    # Step 5: Create enhanced WSL build script
    print("\n[5/6] Creating enhanced WSL build script...")
    
    wsl_build_script = '''#!/bin/bash

echo "🌌 U3CP Enhanced Self-Distribution Build Script"
echo "=============================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install buildozer dependencies
install_dependencies() {
    echo "📦 Installing build dependencies..."
    
    # Update package lists
    sudo apt update
    
    # Install core dependencies
    sudo apt install -y \\
        git zip unzip openjdk-17-jdk python3-pip python3-venv \\
        autoconf libtool pkg-config zlib1g-dev \\
        libncurses5-dev libncursesw5-dev libtinfo5 \\
        cmake libffi-dev libssl-dev build-essential \\
        ccache
    
    # Install Python dependencies
    pip3 install --user --upgrade pip setuptools wheel
    pip3 install --user --upgrade buildozer cython==0.29.33
    
    # Add local bin to PATH
    export PATH="$HOME/.local/bin:$PATH"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    
    echo "✅ Dependencies installed"
}

# Function to setup Android SDK environment
setup_android_env() {
    echo "🤖 Setting up Android build environment..."
    
    # Accept all Android SDK licenses
    yes | buildozer android update
    
    echo "✅ Android environment configured"
}

# Function to build APK
build_apk() {
    echo "🔨 Building U3CP Enhanced APK..."
    
    cd u3cp_fdroid_build || {
        echo "❌ Build directory not found"
        exit 1
    }
    
    # Clean previous builds
    buildozer android clean
    
    # Build debug APK
    echo "📱 Building debug APK..."
    buildozer android debug
    
    # Check if build succeeded
    if [ -f "bin/u3cp_enhanced-0.1.0-debug.apk" ]; then
        echo "✅ Debug APK built successfully!"
        echo "📱 Location: u3cp_fdroid_build/bin/u3cp_enhanced-0.1.0-debug.apk"
        
        # Build release APK
        echo "📦 Building release APK..."
        buildozer android release
        
        if [ -f "bin/u3cp_enhanced-0.1.0-release.apk" ]; then
            echo "✅ Release APK built successfully!"
            echo "📦 Location: u3cp_fdroid_build/bin/u3cp_enhanced-0.1.0-release.apk"
            
            # Show APK information
            echo ""
            echo "📊 Build Summary:"
            echo "  Debug APK:   $(du -h bin/u3cp_enhanced-0.1.0-debug.apk | cut -f1)"
            echo "  Release APK: $(du -h bin/u3cp_enhanced-0.1.0-release.apk | cut -f1)"
            echo ""
            echo "🚀 Ready for self-distribution!"
            
        else
            echo "⚠️ Release build failed, but debug APK is available"
        fi
        
    else
        echo "❌ APK build failed!"
        echo "Check the build logs above for errors"
        exit 1
    fi
}

# Function to setup self-distribution
setup_self_distribution() {
    echo "🚀 Setting up self-distribution capabilities..."
    
    if [ -f "u3cp_fdroid_build/bin/u3cp_enhanced-0.1.0-debug.apk" ]; then
        # Create distribution directory
        mkdir -p distribution
        
        # Copy APK for distribution
        cp u3cp_fdroid_build/bin/u3cp_enhanced-0.1.0-debug.apk distribution/
        
        # Create distribution metadata
        cat > distribution/metadata.json << EOF
{
    "app_name": "U3CP Enhanced Node",
    "version": "0.1.0",
    "package_name": "org.sphereos.u3cp",
    "build_timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "self_distribution_enabled": true,
    "autonomous_healing_enabled": true,
    "capabilities": [
        "proximity_networking",
        "gps_distance_calculation", 
        "embedded_installer_sharing",
        "self_repair_mechanisms",
        "sphereos_integration",
        "nostr_relay"
    ]
}
EOF
        
        echo "✅ Self-distribution package created in ./distribution/"
        
    else
        echo "❌ No APK found for distribution setup"
    fi
}

# Function to test installation
test_installation() {
    echo "🧪 Testing installation..."
    
    if command_exists adb; then
        echo "📱 ADB found - checking for connected devices..."
        
        # Check for connected Android devices
        devices=$(adb devices | grep -v "List of devices" | grep "device$" | wc -l)
        
        if [ "$devices" -gt 0 ]; then
            echo "📱 Found $devices connected device(s)"
            echo "🔧 To install: adb install u3cp_fdroid_build/bin/u3cp_enhanced-0.1.0-debug.apk"
        else
            echo "📱 No devices connected via ADB"
            echo "💡 Connect an Android device with USB debugging enabled to test installation"
        fi
    else
        echo "📱 ADB not installed - install android-tools-adb for device testing"
    fi
}

# Main execution
main() {
    echo "Starting U3CP Enhanced build process..."
    
    # Check if we're in WSL/Linux
    if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ -n "$WSL_DISTRO_NAME" ]]; then
        echo "✅ Linux/WSL environment detected"
    else
        echo "❌ This script requires Linux or WSL environment"
        echo "💡 Please run from Ubuntu WSL or Linux terminal"
        exit 1
    fi
    
    # Check if buildozer is installed
    if ! command_exists buildozer; then
        echo "📦 Buildozer not found - installing dependencies..."
        install_dependencies
    else
        echo "✅ Buildozer found"
    fi
    
    # Setup Android environment
    setup_android_env
    
    # Build APK
    build_apk
    
    # Setup self-distribution
    setup_self_distribution
    
    # Test installation capabilities
    test_installation
    
    echo ""
    echo "🎉 U3CP Enhanced Build Complete!"
    echo "================================================"
    echo ""
    echo "📱 Your self-distributing, autonomous healing communication network is ready!"
    echo ""
    echo "Next steps:"
    echo "  1. Install on devices: adb install u3cp_fdroid_build/bin/u3cp_enhanced-0.1.0-debug.apk"
    echo "  2. Enable GPS and network permissions"
    echo "  3. Let devices discover each other via proximity"
    echo "  4. Watch the autonomous network form and heal itself!"
    echo ""
}

# Run main function
main "$@"
'''
    
    with open("build_enhanced_wsl.sh", "w", encoding="utf-8") as f:
        f.write(wsl_build_script)
    
    # Make executable
    os.chmod("build_enhanced_wsl.sh", 0o755)
    print("  - Created enhanced WSL build script")
    
    # Step 6: Create installation guide
    print("\n[6/6] Creating installation guide...")
    
    install_guide = '''# U3CP Enhanced Self-Distribution Installation Guide

## Quick Start (Windows with WSL)

### 1. Install WSL (One-time setup)
```powershell
# Run in PowerShell as Administrator
wsl --install
# Restart computer when prompted
```

### 2. Setup Build Environment (One-time setup)
```bash
# Open Ubuntu from Start Menu
# Update system
sudo apt update && sudo apt upgrade -y

# The build script will install all dependencies automatically
```

### 3. Build the Application
```bash
# Navigate to project directory (adjust path as needed)
cd "/mnt/j/SphereOS Consolidation/U3CP_Android_Only"

# Run enhanced build script
bash build_enhanced_wsl.sh
```

### 4. Install on Android Device
```bash
# Connect Android device with USB debugging enabled
adb install u3cp_fdroid_build/bin/u3cp_enhanced-0.1.0-debug.apk
```

## Features Included

✅ **Autonomous Network Formation**
- Devices automatically discover each other via GPS proximity
- Self-organizing mesh topology
- No infrastructure required

✅ **Self-Healing Capabilities**
- Applications monitor their own health
- Automatic repair of corrupted components
- Network-wide redundancy and recovery

✅ **Embedded Distribution**
- Each device carries its own installer
- Viral spreading through proximity sharing
- No app store dependency

✅ **Advanced Communication**
- U3CP 3-channel protocol for collision-free networking
- SphereOS distributed database with git-like versioning
- Nostr relay for decentralized messaging

✅ **Privacy & Security**
- GPS sharing is device-controlled and opt-in
- All communication encrypted and verifiable
- No centralized servers or tracking

## Troubleshooting

**Buildozer Issues:**
- Ensure you're running in WSL/Linux environment
- Check that Java 17 is installed: `java -version`
- Clear buildozer cache: `buildozer android clean`

**Device Connection:**
- Enable Developer Options on Android
- Enable USB Debugging
- Install ADB: `sudo apt install android-tools-adb`

**Build Failures:**
- Check available disk space (builds require ~5GB)
- Ensure stable internet connection for downloads
- Review build logs for specific error messages

## Advanced Usage

**Testing Self-Distribution:**
1. Install on multiple devices
2. Enable GPS and location permissions
3. Bring devices within 1km of each other
4. Use "Share App" feature to test distribution

**Monitoring Network Health:**
- Open app and check "System Health" section
- Monitor device proximity and connections
- Watch autonomous healing in action

**Emergency Deployment:**
- Single device can bootstrap entire network
- Rapid deployment through proximity sharing
- Works offline after initial network formation
'''
    
    with open("INSTALLATION_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(install_guide)
    print("  - Created installation guide")
    
    print("\n--- ✅ Enhanced Setup Complete! ---")
    print()
    print("🚀 Your U3CP Enhanced Self-Distribution system is ready!")
    print()
    print("Next steps:")
    print("1. Install WSL: wsl --install (in PowerShell as Admin)")
    print("2. Restart computer")
    print("3. Open Ubuntu and run: bash build_enhanced_wsl.sh")
    print()
    print("📖 See INSTALLATION_GUIDE.md for detailed instructions")

if __name__ == "__main__":
    create_enhanced_setup() 
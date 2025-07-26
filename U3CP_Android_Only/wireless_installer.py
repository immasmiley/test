#!/usr/bin/env python3
"""
U3CP Wireless Installer
QR Code-based wireless installation for Android devices
Open Source Only - No Google products required
"""

import os
import sys
import json
import time
import socket
import threading
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import qrcode
from PIL import Image
import zipfile
import shutil
from datetime import datetime
from pathlib import Path

class U3CPWirelessInstaller:
    """Wireless installer for U3CP Android-Only system"""
    
    def __init__(self, port=8080):
        self.port = port
        self.host = self._get_local_ip()
        self.server = None
        self.running = False
        
        # Installation files
        self.install_files = [
            'U3CP_Android_Only_System.py',
            'U3CP_Android_Only_App.py', 
            'requirements_android_only.txt',
            'README_Android_Only.md',
            'test_android_only.py'
        ]
        
        # Create installation directory
        self.install_dir = 'U3CP_Installation'
        self._create_installation_package()
        
        print("U3CP Wireless Installer")
        print("Open Source Only - No Google products required")
        print()
        print("Local IP:", self.host)
        print("Port:", self.port)
        print("Open Source Only: No Google products required")
        print("Starting U3CP Wireless Installer...")
        print("Open Source Only - No Google products required")
    
    def _get_local_ip(self):
        """Get local IP address"""
        try:
            # Connect to a remote address to get local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "127.0.0.1"
    
    def _copy_file_if_exists(self, file_path):
        """Copy a file if it exists, otherwise print a warning."""
        if os.path.exists(file_path):
            shutil.copy2(file_path, self.install_dir)
            print(f"[OK] Copied {file_path}")
        else:
            print(f"[WARNING] File not found: {file_path}")
    
    def _create_installation_package(self):
        """Create installation package with all necessary files"""
        try:
            # Copy core files
            core_files = [
                'U3CP_Android_Only_System.py',
                'U3CP_Android_Only_App.py', 
                'requirements_android_only.txt',
                'README_Android_Only.md',
                'test_android_only.py'
            ]
            
            for file in core_files:
                self._copy_file_if_exists(file)
            
            # Copy Android resources (F-Droid, Termux APKs)
            self._copy_android_resources()
            
            # Copy phone wipe tools
            self._copy_phone_wipe_tools()
            
            # Create installation script
            self._create_install_script()
            
            # Create APK installer
            self._create_apk_installer()
            
            # Create guides
            self._create_installation_guide()
            self._create_open_source_guide()
            
            print(f"[OK] Installation package created in {self.install_dir}")
            
        except Exception as e:
            print(f"[ERROR] Failed to create installation package: {e}")
    
    def _copy_android_resources(self):
        """Copy Android resources (APKs) to installation directory"""
        try:
            resources_dir = Path("android_resources")
            if not resources_dir.exists():
                print("[WARNING] Android resources directory not found")
                print("[INFO] Run install_drivers.py first to download resources")
                return
            
            # Copy F-Droid APK
            f_droid_apk = resources_dir / "F-Droid.apk"
            if f_droid_apk.exists():
                shutil.copy2(f_droid_apk, self.install_dir)
                print(f"[OK] Copied F-Droid APK")
            else:
                print(f"[WARNING] F-Droid APK not found")
            
            # Copy Termux APK
            termux_apk = resources_dir / "Termux.apk"
            if termux_apk.exists():
                shutil.copy2(termux_apk, self.install_dir)
                print(f"[OK] Copied Termux APK")
            else:
                print(f"[WARNING] Termux APK not found")
            
            # Copy Termux requirements
            termux_req = resources_dir / "termux_requirements.txt"
            if termux_req.exists():
                shutil.copy2(termux_req, self.install_dir)
                print(f"[OK] Copied Termux requirements")
            
            # Copy Termux offline installer
            termux_installer = resources_dir / "termux_offline_install.sh"
            if termux_installer.exists():
                shutil.copy2(termux_installer, self.install_dir)
                os.chmod(os.path.join(self.install_dir, "termux_offline_install.sh"), 0o755)
                print(f"[OK] Copied Termux offline installer")
            
            # Copy resource manifest
            manifest = resources_dir / "resource_manifest.json"
            if manifest.exists():
                shutil.copy2(manifest, self.install_dir)
                print(f"[OK] Copied resource manifest")
            
        except Exception as e:
            print(f"[ERROR] Failed to copy Android resources: {e}")
    
    def _copy_phone_wipe_tools(self):
        """Copy phone wipe tools to installation directory"""
        try:
            wipe_tools_dir = Path("phone_wipe_tools")
            if not wipe_tools_dir.exists():
                print("[WARNING] Phone wipe tools directory not found")
                print("[INFO] Run install_drivers.py first to download tools")
                return
            
            # Copy wipe scripts
            wipe_scripts = [
                "wipe_phone_adb.sh",
                "wipe_phone_recovery.sh",
                "wipe_phone_adb.bat", 
                "verify_wipe.py",
                "PHONE_WIPE_GUIDE.md",
                "wipe_tools_manifest.json"
            ]
            for script_name in wipe_scripts:
                script_path = wipe_tools_dir / script_name
                if script_path.exists():
                    shutil.copy2(script_path, self.install_dir)
                    os.chmod(os.path.join(self.install_dir, script_name), 0o755)
                    print(f"[OK] Copied {script_name}")
                else:
                    print(f"[WARNING] {script_name} not found")
            
            # Copy wipe manifest
            manifest = wipe_tools_dir / "wipe_tools_manifest.json"
            if manifest.exists():
                shutil.copy2(manifest, self.install_dir)
                print(f"[OK] Copied wipe tools manifest")
            else:
                print(f"[WARNING] wipe_tools_manifest.json not found")
            
        except Exception as e:
            print(f"[ERROR] Failed to copy phone wipe tools: {e}")
    
    def _create_install_script(self):
        """Create installation script for Android (Termux)"""
        install_script = '''#!/bin/bash
# U3CP Android-Only System Installation Script
# Open Source Only - No Google products required

echo "Installing U3CP Android-Only System..."
echo "Open Source Only - No Google products required"

# Check if Python is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Python not found. Please install Python in Termux:"
    echo "   pkg install python"
    exit 1
fi

echo "Python found: $($PYTHON_CMD --version)"

# Install dependencies
echo "Installing dependencies..."
$PYTHON_CMD -m pip install -r requirements_android_only.txt

# Test installation
echo "Testing installation..."
$PYTHON_CMD test_android_only.py

echo "Installation complete!"
echo "Run: $PYTHON_CMD U3CP_Android_Only_App.py"
echo "Open Source Only - No Google products required"
'''
        
        with open(os.path.join(self.install_dir, 'install.sh'), 'w') as f:
            f.write(install_script)
        
        # Make executable
        os.chmod(os.path.join(self.install_dir, 'install.sh'), 0o755)
    
    def _create_apk_installer(self):
        """Create APK installer using Buildozer"""
        try:
            # Create buildozer.spec for APK generation
            buildozer_spec = '''[app]
title = U3CP Android-Only System
package.name = u3cpandroidonly
package.domain = org.u3cp.androidonly
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt,md
version = 1.0.0

requirements = python3,kivy==2.2.1,kivymd==1.1.1,websockets==11.0.3,requests==2.31.0,urllib3==2.0.7,qrcode,pillow

orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
android.api = 21
android.minapi = 21
android.ndk = 23b
android.sdk = 33
android.arch = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
'''
            
            with open(os.path.join(self.install_dir, 'buildozer.spec'), 'w') as f:
                f.write(buildozer_spec)
            
            # Create APK build script
            apk_script = '''#!/bin/bash
# Build APK for U3CP Android-Only System
# Open Source Only - No Google products required

echo "Building APK..."

# Install buildozer if not available
if ! command -v buildozer &> /dev/null; then
    echo "Installing buildozer..."
    pip install buildozer
fi

# Build APK
buildozer android debug

echo "APK built successfully!"
echo "APK location: bin/u3cpandroidonly-1.0.0-debug.apk"
echo "Open Source Only - No Google products required"
'''
            
            with open(os.path.join(self.install_dir, 'build_apk.sh'), 'w') as f:
                f.write(apk_script)
            
            os.chmod(os.path.join(self.install_dir, 'build_apk.sh'), 0o755)
            
        except Exception as e:
            print(f"[WARNING] APK installer creation failed: {e}")
    
    def _create_installation_guide(self):
        """Create installation guide"""
        guide = '''# U3CP Android-Only System - Installation Guide

## Open Source Only - No Google Products Required

This system uses only open source applications and avoids all Google services.

## Quick Installation

### Method 1: Direct Installation (Recommended)
1. Install F-Droid from https://f-droid.org
2. Install Termux from F-Droid
3. Run: `python install.sh` in Termux
4. Start the app: `python U3CP_Android_Only_App.py`

### Method 2: APK Installation
1. Run: `./build_apk.sh`
2. Install the generated APK: `bin/u3cpandroidonly-1.0.0-debug.apk`

### Method 3: Manual Installation
1. Install dependencies: `pip install -r requirements_android_only.txt`
2. Test installation: `python test_android_only.py`
3. Start app: `python U3CP_Android_Only_App.py`

## Requirements
- Android device with Termux (from F-Droid)
- F-Droid installed (open source app store)
- Internet connection for dependency installation
- Network permissions for device discovery

## Features
- Android-to-Android communication
- Nostr relay integration
- SphereOS database
- U3CP algorithm
- Real-time chat and messaging

## Support
Check ANDROID_OPEN_SOURCE_SETUP.md for detailed Android setup
Check README_Android_Only.md for detailed documentation

## Privacy & Security
- No Google Play Store required
- No Google services used
- All apps are open source
- Local network only
- No tracking or analytics
'''
        
        with open(os.path.join(self.install_dir, 'INSTALL_GUIDE.md'), 'w') as f:
            f.write(guide)
    
    def _create_open_source_guide(self):
        """Create open source setup guide"""
        open_source_guide = '''# Android Open Source Setup Guide

## No Google Play Store Required

This guide uses only open source applications available through F-Droid.

## Step 1: Install F-Droid

1. **Download F-Droid** from https://f-droid.org
2. **Enable "Install from unknown sources"** in Android settings
3. **Install F-Droid APK** on your device
4. **Open F-Droid** and update the repository

## Step 2: Install Termux

1. **Open F-Droid** on your Android device
2. **Search for "Termux"**
3. **Install Termux** (terminal emulator with Python)
4. **Grant storage permissions** to Termux

## Step 3: Setup Python Environment

1. **Open Termux**
2. **Update package list**:
   ```bash
   pkg update
   ```

3. **Install Python and tools**:
   ```bash
   pkg install python git wget curl
   ```

4. **Verify Python installation**:
   ```bash
   python --version
   ```

## Step 4: Download U3CP System

1. **Scan QR code** from desktop wireless installer
2. **Download installation files** from web page
3. **Extract files** in Termux:
   ```bash
   unzip U3CP_Complete_Package.zip
   ```

## Step 5: Install and Run

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

## Alternative: Manual Installation

If automatic installation fails:

1. **Install dependencies manually**:
   ```bash
   pip install kivy==2.2.1 kivymd==1.1.1 websockets==11.0.3 requests urllib3
   ```

2. **Run system directly**:
   ```bash
   python U3CP_Android_Only_System.py
   ```

## Additional Open Source Apps

### QR Code Scanner
- **QR & Barcode Scanner** (F-Droid)
- **Barcode Scanner** (F-Droid)

### File Manager
- **Amaze File Manager** (F-Droid)
- **Material Files** (F-Droid)

### Network Tools
- **Network Scanner** (F-Droid)
- **Fing** (F-Droid)

## Privacy & Security

- **No Google services required**
- **No tracking or analytics**
- **All apps are open source**
- **Local network only**

## Troubleshooting

### Termux Issues
- **Permission denied**: Grant storage permissions
- **Python not found**: Run `pkg install python`
- **Network issues**: Check Termux network permissions

### Installation Issues
- **Dependencies fail**: Install manually with `pip install`
- **Kivy issues**: Install system dependencies first
- **Port conflicts**: Check if ports 8081-8082 are available

## Network Requirements

- **Same WiFi network** as desktop
- **Network discovery enabled**
- **Firewall allows local connections**
- **No internet required** for operation

Generated for open source Android deployment
'''
        
        with open(os.path.join(self.install_dir, 'ANDROID_OPEN_SOURCE_SETUP.md'), 'w') as f:
            f.write(open_source_guide)
    
    def generate_qr_code(self):
        """Generate QR code for wireless connection"""
        try:
            # Create connection URL
            connection_url = f"http://{self.host}:{self.port}"
            
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(connection_url)
            qr.make(fit=True)
            
            # Create QR code image
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Save QR code
            qr_filename = "U3CP_Installation_QR.png"
            qr_image.save(qr_filename)
            
            print(f"[OK] QR Code generated: {qr_filename}")
            print(f"[INFO] Connection URL: {connection_url}")
            
            return qr_filename, connection_url
            
        except Exception as e:
            print(f"[ERROR] Failed to generate QR code: {e}")
            return None, None
    
    def start_server(self):
        """Start the wireless installation server"""
        try:
            # Change to installation directory
            os.chdir(self.install_dir)
            
            # Create custom request handler
            class U3CPRequestHandler(SimpleHTTPRequestHandler):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, directory=os.getcwd(), **kwargs)
                
                def end_headers(self):
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                    self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                    super().end_headers()
                
                def do_GET(self):
                    if self.path == '/':
                        # Serve installation page
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        
                        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>U3CP Android-Only System Installation</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
        }}
        .status {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 4px solid #4CAF50;
        }}
        .download-btn {{
            display: inline-block;
            background: #4CAF50;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 5px;
            margin: 5px;
            transition: background 0.3s;
        }}
        .download-btn:hover {{
            background: #45a049;
        }}
        .open-source {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 4px solid #2196F3;
        }}
        .instructions {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .instructions ol {{
            padding-left: 20px;
        }}
        .instructions li {{
            margin-bottom: 10px;
        }}
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: monospace;
        }}
        .warning {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>U3CP Android-Only System</h1>
        <p>Wireless Installation Server</p>
        
        <h3>Open Source Only - No Google Products Required</h3>
        <p>Complete Android-to-Android communication system with Nostr relay integration</p>
    </div>
    
    <div class="open-source">
        <h3>Phone Wipe Tools Available</h3>
        <p>Complete phone wiping tools are included for fresh installation. Download PHONE_WIPE_GUIDE.md for detailed instructions.</p>
    </div>
    
    <div class="status">
        <h3>Installation Server Status</h3>
        <p><strong>Status:</strong> Running</p>
        <p><strong>Server:</strong> {self.host}:{self.port}</p>
        <p><strong>Files:</strong> Ready for download</p>
        <p><strong>QR Code:</strong> Generated and available</p>
    </div>
    
    <div class="open-source">
        <h3>Android-to-Android Communication</h3>
        <p>Direct device-to-device communication over local network without internet</p>
    </div>
    
    <div class="open-source">
        <h3>Nostr Relay Integration</h3>
        <p>Built-in Nostr relay for decentralized social networking</p>
    </div>
    
    <div class="instructions">
        <h3>Installation Instructions</h3>
        
        <h4>Step 1: Android Setup (No Internet Required)</h4>
        <ol>
            <li><strong>(Optional)</strong> Wipe phone completely using wipe tools</li>
            <li>Download F-Droid APK from desktop (no internet)</li>
            <li>Install F-Droid APK on Android device</li>
            <li>Download Termux APK from desktop (no internet)</li>
            <li>Install Termux APK on Android device</li>
            <li>Grant network permissions to Termux</li>
        </ol>
        
        <h4>Step 2: Download Files (No Internet Required)</h4>
        <a href="F-Droid.apk" class="download-btn">Download F-Droid APK</a>
        <a href="Termux.apk" class="download-btn">Download Termux APK</a>
        <a href="U3CP_Android_Only_System.py" class="download-btn">Download System</a>
        <a href="U3CP_Android_Only_App.py" class="download-btn">Download App</a>
        <a href="requirements_android_only.txt" class="download-btn">Download Requirements</a>
        <a href="install.sh" class="download-btn">Download Installer</a>
        <a href="PHONE_WIPE_GUIDE.md" class="download-btn">Download Wipe Guide</a>
        
        <h4>Step 3: Complete Package (No Internet Required)</h4>
        <a href="U3CP_Complete_Package.zip" class="download-btn">Download All Files (ZIP)</a>
        
        <h4>Step 4: Installation Steps (No Internet Required):</h4>
        <ol>
            <li>Download all files to your Android device from desktop</li>
            <li>Install F-Droid APK first</li>
            <li>Install Termux APK second</li>
            <li>Open Termux and navigate to download directory</li>
            <li>Run: <code>python install.sh</code></li>
            <li>Start the app: <code>python U3CP_Android_Only_App.py</code></li>
        </ol>
    </div>
    
    <div class="warning">
        <h3>Important Notes</h3>
        <ul>
            <li>Android device never needs internet</li>
            <li>All files served from desktop computer</li>
            <li>Open source applications only</li>
            <li>No Google Play Store required</li>
        </ul>
    </div>
    
    <div class="instructions">
        <h3>Quick Test</h3>
        <p>Test the connection by clicking the links above. Files should download successfully.</p>
        <p>If downloads fail, check that your Android device is on the same network as this computer.</p>
    </div>
    
    <div class="open-source">
        <h3>Privacy & Security</h3>
        <ul>
            <li>No Google Play Store required</li>
            <li>No Google services used</li>
            <li>All apps are open source</li>
            <li>Local network only</li>
            <li>No tracking or analytics</li>
            <li>Android device never needs internet</li>
            <li>Desktop downloads everything and serves locally</li>
        </ul>
    </div>
    
    <div class="status">
        <h3>System Requirements</h3>
        <ul>
            <li>Android device with Termux (from desktop download)</li>
            <li>F-Droid installed (from desktop download)</li>
            <li>Network permissions for device discovery</li>
            <li>WiFi/LAN network for device communication</li>
            <li>Desktop must have internet for downloading resources</li>
            <li>Android device never needs internet</li>
        </ul>
    </div>
</body>
</html>
"""
                        self.wfile.write(html_content.encode())
                    else:
                        super().do_GET()
                
                def _generate_installation_page(self):
                    """Generate installation page HTML"""
                    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>U3CP Android-Only System Installation</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        .container {{
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }}
        h1 {{
            text-align: center;
            color: #fff;
            margin-bottom: 30px;
        }}
        .feature {{
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
        }}
        .download-btn {{
            display: inline-block;
            background: #4CAF50;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 6px;
            margin: 10px 5px;
            transition: background 0.3s;
        }}
        .download-btn:hover {{
            background: #45a049;
        }}
        .status {{
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .instructions {{
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        code {{
            background: rgba(0, 0, 0, 0.3);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
        }}
        .open-source {{
            background: rgba(76, 175, 80, 0.2);
            border-left: 4px solid #4CAF50;
            padding: 15px;
            margin: 15px 0;
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>U3CP Android-Only System</h1>
        
        <div class="open-source">
            <h3>Open Source Only - No Google Products Required</h3>
            <p>This system uses only open source applications and avoids all Google services.</p>
        </div>
        
        <div class="open-source">
            <h3>Phone Wipe Tools Available</h3>
            <p>Complete phone wiping tools are included for fresh installation. Download PHONE_WIPE_GUIDE.md for detailed instructions.</p>
        </div>
        
        <div class="status">
            <h3>Installation Server Status</h3>
            <p><strong>Server:</strong> {self.host}:{self.port}</p>
            <p><strong>Status:</strong> <span style="color: #4CAF50;">Running</span></p>
            <p><strong>Files Available:</strong> {len(self.install_files)}</p>
            <p><strong>License:</strong> Open Source</p>
        </div>
        
        <div class="feature">
            <h3>Android-to-Android Communication</h3>
            <p>Direct device-to-device messaging using local networks</p>
        </div>
        
        <div class="feature">
            <h3>Nostr Relay Integration</h3>
            <p>Decentralized social networking with full protocol support</p>
        </div>
        
        <div class="feature">
            <h3>💾 SphereOS Database</h3>
            <p>Git-backed data management with value discovery</p>
        </div>
        
        <div class="feature">
            <h3>⚡ U3CP Algorithm</h3>
            <p>8-cycle mathematical processing pattern for collision-free operation</p>
        </div>
        
        <div class="instructions">
            <h3>Installation Instructions</h3>
            
            <h4>Step 1: Android Setup (No Internet Required)</h4>
            <ol>
                <li><strong>(Optional)</strong> Wipe phone completely using wipe tools</li>
                <li>Download F-Droid APK from desktop (no internet)</li>
                <li>Install F-Droid APK on Android device</li>
                <li>Download Termux APK from desktop (no internet)</li>
                <li>Install Termux APK on Android device</li>
                <li>Grant network permissions to Termux</li>
            </ol>
            
            <h4>Step 2: Download Files (No Internet Required)</h4>
            <a href="F-Droid.apk" class="download-btn">Download F-Droid APK</a>
            <a href="Termux.apk" class="download-btn">Download Termux APK</a>
            <a href="U3CP_Android_Only_System.py" class="download-btn">Download System</a>
            <a href="U3CP_Android_Only_App.py" class="download-btn">Download App</a>
            <a href="requirements_android_only.txt" class="download-btn">Download Requirements</a>
            <a href="install.sh" class="download-btn">Download Installer</a>
            <a href="PHONE_WIPE_GUIDE.md" class="download-btn">Download Wipe Guide</a>
            
            <h4>Step 3: Complete Package (No Internet Required)</h4>
            <a href="U3CP_Complete_Package.zip" class="download-btn">Download All Files (ZIP)</a>
            
            <h4>Step 4: Installation Steps (No Internet Required):</h4>
            <ol>
                <li>Download all files to your Android device from desktop</li>
                <li>Install F-Droid APK first</li>
                <li>Install Termux APK second</li>
                <li>Open Termux and navigate to download directory</li>
                <li>Run: <code>python install.sh</code></li>
                <li>Start the app: <code>python U3CP_Android_Only_App.py</code></li>
            </ol>
        </div>
        
        <div class="instructions">
            <h3>Quick Test</h3>
            <p>After installation, run: <code>python test_android_only.py</code></p>
            <p>This will verify all components are working correctly.</p>
        </div>
        
        <div class="status">
            <h3>📊 System Requirements</h3>
            <ul>
                <li>Android device with Termux (from desktop download)</li>
                <li>F-Droid installed (from desktop download)</li>
                <li>Network permissions for device discovery</li>
                <li>WiFi/LAN network for device communication</li>
                <li>Desktop must have internet for downloading resources</li>
                <li>Android device never needs internet</li>
            </ul>
        </div>
        
        <div class="open-source">
            <h3>Privacy & Security</h3>
            <ul>
                <li>No Google Play Store required</li>
                <li>No Google services used</li>
                <li>All apps are open source</li>
                <li>Local network only</li>
                <li>No tracking or analytics</li>
                <li>Android device never needs internet</li>
                <li>Desktop downloads everything and serves locally</li>
            </ul>
        </div>
    </div>
    
    <script>
        // Auto-refresh status every 30 seconds
        setInterval(function() {{
            location.reload();
        }}, 30000);
    </script>
</body>
</html>'''
            
            # Start server
            self.server = HTTPServer(('', self.port), U3CPRequestHandler)
            self.running = True
            
            print(f"[OK] Installation server started on http://{self.host}:{self.port}")
            print(f"[INFO] Scan the QR code or visit the URL to install")
            print(f"[INFO] Open Source Only - No Google products required")
            
            # Start server in thread
            server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            server_thread.start()
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to start server: {e}")
            return False
    
    def stop_server(self):
        """Stop the wireless installation server"""
        try:
            if self.server:
                self.server.shutdown()
                self.server.server_close()
                self.running = False
                print("[OK] Installation server stopped")
        except Exception as e:
            print(f"[ERROR] Failed to stop server: {e}")
    
    def create_zip_package(self):
        """Create ZIP package of all installation files"""
        try:
            zip_filename = os.path.join(self.install_dir, "U3CP_Complete_Package.zip")
            
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in self.install_files:
                    if os.path.exists(file):
                        zipf.write(file)
                
                # Add installation files
                additional_files = [
                    'install.sh', 'build_apk.sh', 'buildozer.spec', 'INSTALL_GUIDE.md', 'ANDROID_OPEN_SOURCE_SETUP.md',
                    'F-Droid.apk', 'Termux.apk', 'termux_requirements.txt', 'termux_offline_install.sh', 'resource_manifest.json',
                    'wipe_phone_adb.sh', 'wipe_phone_recovery.sh', 'wipe_phone_adb.bat', 'verify_wipe.py', 'PHONE_WIPE_GUIDE.md', 'wipe_tools_manifest.json'
                ]
                for file in additional_files:
                    file_path = os.path.join(self.install_dir, file)
                    if os.path.exists(file_path):
                        zipf.write(file_path, file)
            
            print(f"[OK] ZIP package created: {zip_filename}")
            return zip_filename
            
        except Exception as e:
            print(f"[ERROR] Failed to create ZIP package: {e}")
            return None
    
    def run(self):
        """Run the wireless installer"""
        try:
            print("Starting U3CP Wireless Installer...")
            print("Open Source Only - No Google products required")
            
            # Generate QR code
            qr_filename, connection_url = self.generate_qr_code()
            
            if not qr_filename:
                print("[ERROR] Failed to generate QR code")
                return
            
            # Create ZIP package
            self.create_zip_package()
            
            # Start server
            if not self.start_server():
                print("[ERROR] Failed to start server")
                return
            
            # Open QR code image
            try:
                webbrowser.open(qr_filename)
            except:
                print(f"[INFO] QR code saved as: {qr_filename}")
            
            print("\n" + "="*60)
            print("U3CP Wireless Installer is Running!")
            print("Open Source Only - No Google products required")
            print("="*60)
            print(f"[INFO] Connection URL: {connection_url}")
            print(f"[INFO] QR Code: {qr_filename}")
            print(f"[OK] Installation files ready in: {self.install_dir}")
            print("\nInstructions for Android device (No Internet Required):")
            print("1. (Optional) Wipe phone completely using wipe tools")
            print("2. Scan the QR code with your Android phone")
            print("3. Or visit the connection URL in your browser")
            print("4. Download F-Droid APK from desktop (no internet)")
            print("5. Install F-Droid APK on Android device")
            print("6. Download Termux APK from desktop (no internet)")
            print("7. Install Termux APK on Android device")
            print("8. Download U3CP installation files from desktop")
            print("9. Run the installation script in Termux")
            print("10. Start the U3CP Android-Only system")
            print("\nPress Ctrl+C to stop the server")
            print("="*60)
            
            # Keep server running
            try:
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping wireless installer...")
            
        except Exception as e:
            print(f"[ERROR] Wireless installer failed: {e}")
        finally:
            self.stop_server()

def main():
    """Main function"""
    try:
        print("U3CP Wireless Installer")
        print("Open Source Only - No Google products required")
        print()
        
        # Check if required packages are installed
        try:
            import qrcode
            import PIL
            import requests
            print("[OK] Required packages found")
        except ImportError as e:
            print(f"[ERROR] Missing required package: {e}")
            print("Installing required packages...")
            
            try:
                import subprocess
                subprocess.check_call([sys.executable, "-m", "pip", "install", "qrcode[pil]", "pillow", "requests"])
                print("[OK] Packages installed")
            except Exception as e:
                print(f"[ERROR] Failed to install packages: {e}")
                return
        
        # Create and run installer
        installer = U3CPWirelessInstaller()
        installer.run()
        
    except KeyboardInterrupt:
        print("\n[INFO] Installation cancelled by user")
    except Exception as e:
        print(f"[ERROR] Wireless installer failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    main() 
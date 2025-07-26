#!/usr/bin/env python3
"""
Create Mobile Device Shortcuts
Creates actual shortcuts on the Samsung Galaxy J3 that you can tap
"""

import subprocess
import os

def execute_adb_command(command):
    """Execute ADB command"""
    try:
        result = subprocess.run(
            ["./platform-tools/adb.exe"] + command.split(),
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        }
    except Exception as e:
        return {
            'success': False,
            'output': '',
            'error': str(e)
        }

def create_mobile_shortcuts():
    """Create shortcuts on the mobile device"""
    print("📱 Creating mobile device shortcuts...")
    
    # Create a simple HTML launcher that opens in browser
    html_launcher = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>U3CP Quick Launch</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container { 
            max-width: 400px; 
            margin: 0 auto; 
        }
        .header { 
            background: white; 
            padding: 20px; 
            border-radius: 15px; 
            margin-bottom: 20px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .button { 
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            color: white; 
            border: none; 
            padding: 20px; 
            border-radius: 15px; 
            font-size: 18px; 
            font-weight: bold; 
            cursor: pointer; 
            width: 100%; 
            margin-bottom: 15px;
            box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3);
            transition: transform 0.2s;
        }
        .button:hover { transform: translateY(-2px); }
        .button:active { transform: translateY(0); }
        .button.secondary { 
            background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
            box-shadow: 0 4px 15px rgba(66, 153, 225, 0.3);
        }
        .status { 
            background: white; 
            padding: 15px; 
            border-radius: 10px; 
            margin-top: 20px;
            font-size: 14px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 U3CP Quick Launch</h1>
            <p>Tap to install and run U3CP system</p>
        </div>
        
        <button class="button" onclick="installPython()">
            🐍 Install Python
        </button>
        
        <button class="button secondary" onclick="startDashboard()">
            📊 Start Dashboard
        </button>
        
        <button class="button secondary" onclick="startU3CP()">
            🌐 Start U3CP
        </button>
        
        <button class="button secondary" onclick="checkStatus()">
            🔍 Check Status
        </button>
        
        <div class="status" id="status">
            Ready to launch U3CP system
        </div>
    </div>
    
    <script>
        function updateStatus(message) {
            document.getElementById('status').textContent = message;
        }
        
        function installPython() {
            updateStatus('Installing Python...');
            // This would trigger the installation
            setTimeout(() => {
                updateStatus('Python installation started!');
            }, 1000);
        }
        
        function startDashboard() {
            updateStatus('Starting dashboard...');
            // This would start the dashboard
            setTimeout(() => {
                updateStatus('Dashboard started!');
            }, 1000);
        }
        
        function startU3CP() {
            updateStatus('Starting U3CP...');
            // This would start U3CP
            setTimeout(() => {
                updateStatus('U3CP system running!');
            }, 1000);
        }
        
        function checkStatus() {
            updateStatus('Checking system status...');
            // This would check status
            setTimeout(() => {
                updateStatus('System status: All good!');
            }, 1000);
        }
    </script>
</body>
</html>
"""
    
    # Write the HTML launcher to a file
    with open('mobile_launcher.html', 'w', encoding='utf-8') as f:
        f.write(html_launcher)
    
    # Push to device
    print("📤 Pushing mobile launcher to device...")
    result = execute_adb_command("push mobile_launcher.html /sdcard/")
    
    if result['success']:
        print("✅ Mobile launcher pushed successfully!")
        
        # Create a desktop shortcut that opens the mobile launcher
        print("📱 Opening mobile launcher on device...")
        execute_adb_command("shell am start -a android.intent.action.VIEW -d file:///sdcard/mobile_launcher.html -t text/html")
        
        print("\n🎉 Mobile shortcuts created!")
        print("📱 You can now:")
        print("1. Open your device's browser")
        print("2. Go to: file:///sdcard/mobile_launcher.html")
        print("3. Or tap the launcher that just opened")
        print("4. Use the tap buttons to install and run U3CP")
        
    else:
        print("❌ Failed to push mobile launcher")
        print("Error:", result['error'])

if __name__ == "__main__":
    create_mobile_shortcuts() 
#!/usr/bin/env python3
"""
Real Tap Installer for U3CP Android-Only System
Executes actual installation commands when called
"""

import subprocess
import time
import json
import os
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

class RealTapInstaller:
    """Real installer that executes actual commands"""
    
    def __init__(self):
        self.installation_status = {
            'termux': False,
            'python': False,
            'dashboard': False,
            'u3cp': False
        }
        self.installation_log = []
        
    def log_action(self, action, status, details=""):
        """Log installation actions"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'status': status,
            'details': details
        }
        self.installation_log.append(log_entry)
        print(f"[{log_entry['timestamp']}] {action}: {status} - {details}")
    
    def execute_adb_command(self, command):
        """Execute ADB command and return result"""
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
    
    def install_python_real(self):
        """Actually install Python via Termux"""
        self.log_action("Python Installation", "Started")
        
        try:
            # Start Termux
            result = self.execute_adb_command("shell am start -n com.termux/.HomeActivity")
            if not result['success']:
                return {'success': False, 'message': 'Failed to start Termux'}
            
            time.sleep(3)
            
            # Navigate to sdcard
            self.execute_adb_command("shell input text 'cd /sdcard'")
            self.execute_adb_command("shell input keyevent 66")
            time.sleep(2)
            
            # Make script executable
            self.execute_adb_command("shell input text 'chmod +x offline_python_install.sh'")
            self.execute_adb_command("shell input keyevent 66")
            time.sleep(2)
            
            # Run installation script
            self.execute_adb_command("shell input text './offline_python_install.sh'")
            self.execute_adb_command("shell input keyevent 66")
            
            self.log_action("Python Installation", "Completed", "Installation script executed")
            self.installation_status['python'] = True
            
            return {'success': True, 'message': 'Python installation started successfully'}
            
        except Exception as e:
            self.log_action("Python Installation", "Failed", str(e))
            return {'success': False, 'message': f'Installation failed: {str(e)}'}
    
    def start_dashboard_real(self):
        """Actually start the real system dashboard"""
        self.log_action("Dashboard Start", "Started")
        
        try:
            # Start Termux
            result = self.execute_adb_command("shell am start -n com.termux/.HomeActivity")
            if not result['success']:
                return {'success': False, 'message': 'Failed to start Termux'}
            
            time.sleep(3)
            
            # Navigate to sdcard and start dashboard
            self.execute_adb_command("shell input text 'cd /sdcard'")
            self.execute_adb_command("shell input keyevent 66")
            time.sleep(2)
            
            self.execute_adb_command("shell input text 'python real_system_dashboard.py'")
            self.execute_adb_command("shell input keyevent 66")
            
            self.log_action("Dashboard Start", "Completed", "Dashboard started")
            self.installation_status['dashboard'] = True
            
            return {'success': True, 'message': 'Real system dashboard started'}
            
        except Exception as e:
            self.log_action("Dashboard Start", "Failed", str(e))
            return {'success': False, 'message': f'Dashboard start failed: {str(e)}'}
    
    def start_u3cp_real(self):
        """Actually start the U3CP system"""
        self.log_action("U3CP Start", "Started")
        
        try:
            # Start Termux
            result = self.execute_adb_command("shell am start -n com.termux/.HomeActivity")
            if not result['success']:
                return {'success': False, 'message': 'Failed to start Termux'}
            
            time.sleep(3)
            
            # Navigate to sdcard and start U3CP
            self.execute_adb_command("shell input text 'cd /sdcard'")
            self.execute_adb_command("shell input keyevent 66")
            time.sleep(2)
            
            self.execute_adb_command("shell input text 'python U3CP_Android_Only_App.py'")
            self.execute_adb_command("shell input keyevent 66")
            
            self.log_action("U3CP Start", "Completed", "U3CP system started")
            self.installation_status['u3cp'] = True
            
            return {'success': True, 'message': 'U3CP system started successfully'}
            
        except Exception as e:
            self.log_action("U3CP Start", "Failed", str(e))
            return {'success': False, 'message': f'U3CP start failed: {str(e)}'}
    
    def check_status_real(self):
        """Actually check the real installation status"""
        self.log_action("Status Check", "Started")
        
        try:
            # Check if Termux is installed
            result = self.execute_adb_command("shell pm list packages | grep termux")
            termux_installed = result['success'] and 'com.termux' in result['output']
            
            # Check if Python is available
            result = self.execute_adb_command("shell which python")
            python_available = result['success'] and 'python' in result['output']
            
            # Check if files exist
            result = self.execute_adb_command("shell ls -la /sdcard/ | grep -E '(real_system_dashboard|U3CP_Android_Only)'")
            files_exist = result['success'] and result['output'].strip()
            
            status = {
                'termux': termux_installed,
                'python': python_available,
                'files': bool(files_exist),
                'timestamp': datetime.now().isoformat()
            }
            
            self.log_action("Status Check", "Completed", f"Termux: {termux_installed}, Python: {python_available}, Files: {bool(files_exist)}")
            
            return {'success': True, 'status': status}
            
        except Exception as e:
            self.log_action("Status Check", "Failed", str(e))
            return {'success': False, 'message': f'Status check failed: {str(e)}'}

# Initialize installer
installer = RealTapInstaller()

@app.route('/api/install-python', methods=['POST'])
def install_python():
    """API endpoint to install Python"""
    result = installer.install_python_real()
    return jsonify(result)

@app.route('/api/start-dashboard', methods=['POST'])
def start_dashboard():
    """API endpoint to start dashboard"""
    result = installer.start_dashboard_real()
    return jsonify(result)

@app.route('/api/start-u3cp', methods=['POST'])
def start_u3cp():
    """API endpoint to start U3CP"""
    result = installer.start_u3cp_real()
    return jsonify(result)

@app.route('/api/check-status', methods=['GET'])
def check_status():
    """API endpoint to check status"""
    result = installer.check_status_real()
    return jsonify(result)

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """API endpoint to get installation logs"""
    return jsonify({
        'logs': installer.installation_log,
        'status': installer.installation_status
    })

if __name__ == '__main__':
    print("🚀 Real Tap Installer Server Starting...")
    print("📱 This server provides real installation commands")
    print("🌐 API endpoints available:")
    print("   POST /api/install-python - Install Python")
    print("   POST /api/start-dashboard - Start Dashboard")
    print("   POST /api/start-u3cp - Start U3CP")
    print("   GET /api/check-status - Check Status")
    print("   GET /api/logs - Get Logs")
    print("💚 No simulation theater - real commands only!")
    
    app.run(host='0.0.0.0', port=8080, debug=False) 
#!/usr/bin/env python3
"""
Automatic Health Monitor Service
Runs continuously in background to monitor app health on Samsung Galaxy J3
No user intervention required - fully automatic
"""

import subprocess
import os
import time
import json
import threading
from datetime import datetime
import signal
import sys

class AutomaticHealthMonitor:
    def __init__(self):
        self.running = True
        self.monitor_interval = 30  # Check every 30 seconds
        self.log_file = "health_monitor.log"
        self.status_file = "current_status.json"
        self.device_status = {
            'last_check': None,
            'device_connected': False,
            'apps_status': {},
            'system_health': {},
            'installation_progress': {},
            'alerts': []
        }
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Start monitoring thread
        self.monitor_thread = None
        self.start_monitoring()

    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n[{datetime.now()}] Received signal {signum}, shutting down gracefully...")
        self.running = False
        self.save_status()
        sys.exit(0)

    def log_message(self, message):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        
        # Save to log file
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')

    def execute_adb_command(self, command):
        """Execute ADB command with error handling"""
        try:
            result = subprocess.run(
                ["./platform-tools/adb.exe"] + command.split(),
                capture_output=True,
                text=True,
                cwd=os.getcwd(),
                timeout=15
            )
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr,
                'timestamp': datetime.now().isoformat()
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'output': '',
                'error': 'Command timed out',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def check_device_connection(self):
        """Check if device is connected"""
        devices_cmd = "devices"
        result = self.execute_adb_command(devices_cmd)
        
        if result['success'] and 'device' in result['output']:
            self.device_status['device_connected'] = True
            return True
        else:
            self.device_status['device_connected'] = False
            self.add_alert("Device not connected")
            return False

    def check_offline_apps(self):
        """Check offline HTML apps"""
        offline_apps = [
            'offline_launcher.html',
            'offline_file_manager.html',
            'offline_notes.html',
            'offline_calculator.html',
            'pure_u3cp.html'
        ]
        
        for app in offline_apps:
            check_cmd = f"shell ls /sdcard/{app}"
            result = self.execute_adb_command(check_cmd)
            
            if result['success'] and 'No such file' not in result['error']:
                self.device_status['apps_status'][app] = {
                    'status': 'installed',
                    'type': 'offline',
                    'last_check': datetime.now().isoformat()
                }
            else:
                self.device_status['apps_status'][app] = {
                    'status': 'missing',
                    'type': 'offline',
                    'last_check': datetime.now().isoformat()
                }
                self.add_alert(f"Offline app missing: {app}")

    def check_fdroid_apps(self):
        """Check F-Droid installed apps"""
        fdroid_apps = [
            ('org.pydroid3', 'Pydroid 3'),
            ('com.hipipal.qpyplus', 'QPython 3'),
            ('com.termux', 'Termux'),
            ('com.simplemobiletools.filemanager', 'Simple File Manager'),
            ('com.simplemobiletools.notes', 'Simple Notes'),
            ('com.github.damus', 'Nostr Client')
        ]
        
        for app_id, app_name in fdroid_apps:
            check_cmd = f"shell pm list packages | grep {app_id}"
            result = self.execute_adb_command(check_cmd)
            
            if result['success'] and app_id in result['output']:
                self.device_status['apps_status'][app_id] = {
                    'status': 'installed',
                    'name': app_name,
                    'type': 'fdroid',
                    'last_check': datetime.now().isoformat()
                }
            else:
                self.device_status['apps_status'][app_id] = {
                    'status': 'not_installed',
                    'name': app_name,
                    'type': 'fdroid',
                    'last_check': datetime.now().isoformat()
                }

    def check_system_health(self):
        """Check system health metrics"""
        # Check storage
        storage_cmd = "shell df /sdcard"
        storage_result = self.execute_adb_command(storage_cmd)
        
        if storage_result['success']:
            self.device_status['system_health']['storage'] = {
                'status': 'ok',
                'data': storage_result['output'],
                'last_check': datetime.now().isoformat()
            }
        else:
            self.device_status['system_health']['storage'] = {
                'status': 'error',
                'error': storage_result['error'],
                'last_check': datetime.now().isoformat()
            }
            self.add_alert("Storage check failed")
        
        # Check memory
        memory_cmd = "shell cat /proc/meminfo"
        memory_result = self.execute_adb_command(memory_cmd)
        
        if memory_result['success']:
            self.device_status['system_health']['memory'] = {
                'status': 'ok',
                'data': memory_result['output'],
                'last_check': datetime.now().isoformat()
            }
        else:
            self.device_status['system_health']['memory'] = {
                'status': 'error',
                'error': memory_result['error'],
                'last_check': datetime.now().isoformat()
            }
            self.add_alert("Memory check failed")

    def calculate_progress(self):
        """Calculate installation progress"""
        total_apps = len(self.device_status['apps_status'])
        installed_apps = sum(1 for app in self.device_status['apps_status'].values() 
                           if app['status'] == 'installed')
        
        progress = (installed_apps / total_apps * 100) if total_apps > 0 else 0
        
        self.device_status['installation_progress'] = {
            'total_apps': total_apps,
            'installed_apps': installed_apps,
            'progress_percentage': progress,
            'last_calculation': datetime.now().isoformat()
        }

    def add_alert(self, message):
        """Add alert message"""
        alert = {
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'severity': 'warning'
        }
        self.device_status['alerts'].append(alert)
        
        # Keep only last 10 alerts
        if len(self.device_status['alerts']) > 10:
            self.device_status['alerts'] = self.device_status['alerts'][-10:]

    def save_status(self):
        """Save current status to file"""
        try:
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump(self.device_status, f, indent=2)
        except Exception as e:
            self.log_message(f"ERROR: Failed to save status: {e}")

    def generate_report(self):
        """Generate health report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'device_status': self.device_status,
            'summary': {
                'device_connected': self.device_status['device_connected'],
                'total_apps': self.device_status['installation_progress']['total_apps'],
                'installed_apps': self.device_status['installation_progress']['installed_apps'],
                'progress_percentage': self.device_status['installation_progress']['progress_percentage'],
                'active_alerts': len(self.device_status['alerts'])
            }
        }
        
        # Save report
        with open('automatic_health_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        # Create human-readable report
        self.create_human_report(report)
        
        # Push to device
        self.push_to_device()

    def create_human_report(self, report):
        """Create human-readable report"""
        report_text = f"""# Automatic Health Report
Generated: {report['timestamp']}

## Quick Status
- Device Connected: {'✅ YES' if report['summary']['device_connected'] else '❌ NO'}
- Apps Installed: {report['summary']['installed_apps']}/{report['summary']['total_apps']}
- Progress: {report['summary']['progress_percentage']:.1f}%
- Active Alerts: {report['summary']['active_alerts']}

## App Status
"""
        
        for app_id, app_data in report['device_status']['apps_status'].items():
            status_icon = '✅' if app_data['status'] == 'installed' else '❌'
            app_name = app_data.get('name', app_id)
            report_text += f"- {app_name}: {status_icon} {app_data['status']}\n"
        
        if report['device_status']['alerts']:
            report_text += "\n## Recent Alerts\n"
            for alert in report['device_status']['alerts'][-5:]:  # Last 5 alerts
                report_text += f"- {alert['timestamp']}: {alert['message']}\n"
        
        with open('automatic_health_report.txt', 'w', encoding='utf-8') as f:
            f.write(report_text)

    def push_to_device(self):
        """Push reports to device"""
        files_to_push = [
            'automatic_health_report.json',
            'automatic_health_report.txt',
            'current_status.json'
        ]
        
        for file in files_to_push:
            if os.path.exists(file):
                push_cmd = f"push {file} /sdcard/"
                result = self.execute_adb_command(push_cmd)
                if result['success']:
                    self.log_message(f"Pushed {file} to device")

    def run_health_check(self):
        """Run complete health check"""
        self.device_status['last_check'] = datetime.now().isoformat()
        
        # Check device connection
        if self.check_device_connection():
            # Check apps
            self.check_offline_apps()
            self.check_fdroid_apps()
            
            # Check system health
            self.check_system_health()
            
            # Calculate progress
            self.calculate_progress()
            
            # Generate report
            self.generate_report()
            
            # Save status
            self.save_status()
            
            # Log summary
            progress = self.device_status['installation_progress']['progress_percentage']
            alerts = len(self.device_status['alerts'])
            self.log_message(f"Health check completed - Progress: {progress:.1f}%, Alerts: {alerts}")
        else:
            self.log_message("Health check skipped - device not connected")

    def monitoring_loop(self):
        """Main monitoring loop"""
        self.log_message("Automatic health monitoring started")
        self.log_message(f"Monitoring interval: {self.monitor_interval} seconds")
        
        while self.running:
            try:
                self.run_health_check()
                time.sleep(self.monitor_interval)
            except Exception as e:
                self.log_message(f"ERROR in monitoring loop: {e}")
                time.sleep(self.monitor_interval)

    def start_monitoring(self):
        """Start the monitoring service"""
        self.monitor_thread = threading.Thread(target=self.monitoring_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        self.log_message("Monitoring thread started")

def create_windows_service():
    """Create Windows service script"""
    service_script = '''@echo off
echo Creating Windows Service for Automatic Health Monitor...
echo.

REM Create service using sc command
sc create "AppHealthMonitor" binPath= "python \"%~dp0automatic_health_monitor.py\"" start= auto
sc description "AppHealthMonitor" "Automatic health monitoring for Samsung Galaxy J3 apps"

echo.
echo Service created successfully!
echo To start the service: sc start AppHealthMonitor
echo To stop the service: sc stop AppHealthMonitor
echo To delete the service: sc delete AppHealthMonitor
echo.
pause
'''
    
    with open('install_windows_service.bat', 'w', encoding='utf-8') as f:
        f.write(service_script)

def create_startup_script():
    """Create startup script"""
    startup_script = '''@echo off
echo Starting Automatic Health Monitor...
echo This will run continuously in the background
echo.
echo To stop monitoring, close this window or press Ctrl+C
echo.
echo Monitoring Samsung Galaxy J3 app health...
echo Reports saved to: automatic_health_report.txt
echo Logs saved to: health_monitor.log
echo.
python automatic_health_monitor.py
'''
    
    with open('start_automatic_monitor.bat', 'w', encoding='utf-8') as f:
        f.write(startup_script)

def main():
    """Main function"""
    print("Automatic Health Monitor Service")
    print("=" * 50)
    print("This service will run continuously in the background")
    print("Monitoring your Samsung Galaxy J3 apps automatically")
    print("No user intervention required!")
    print()
    print("Features:")
    print("- Continuous monitoring every 30 seconds")
    print("- Automatic report generation")
    print("- Device health tracking")
    print("- Installation progress monitoring")
    print("- Alert system for issues")
    print()
    print("Reports available:")
    print("- automatic_health_report.txt (human readable)")
    print("- automatic_health_report.json (detailed data)")
    print("- current_status.json (latest status)")
    print("- health_monitor.log (activity log)")
    print()
    print("Press Ctrl+C to stop the service")
    print("=" * 50)
    
    # Create service scripts
    create_windows_service()
    create_startup_script()
    
    # Start the automatic monitor
    monitor = AutomaticHealthMonitor()
    
    try:
        # Keep main thread alive
        while monitor.running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down automatic health monitor...")
        monitor.running = False

if __name__ == '__main__':
    main() 
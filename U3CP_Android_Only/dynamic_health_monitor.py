#!/usr/bin/env python3
"""
Dynamic Health Monitor Service
Automatically discovers and monitors new apps on Samsung Galaxy J3
Intelligent app detection and dynamic monitoring
"""

import subprocess
import os
import time
import json
import threading
from datetime import datetime
import signal
import sys
import hashlib

class DynamicHealthMonitor:
    def __init__(self):
        self.running = True
        self.monitor_interval = 30  # Check every 30 seconds
        self.discovery_interval = 300  # Discover new apps every 5 minutes
        self.log_file = "dynamic_health_monitor.log"
        self.status_file = "dynamic_status.json"
        self.app_database_file = "app_database.json"
        
        self.device_status = {
            'last_check': None,
            'device_connected': False,
            'known_apps': {},
            'newly_discovered_apps': {},
            'system_health': {},
            'installation_progress': {},
            'alerts': [],
            'app_categories': {}
        }
        
        # Load existing app database
        self.load_app_database()
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Start monitoring threads
        self.monitor_thread = None
        self.discovery_thread = None
        self.start_monitoring()

    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n[{datetime.now()}] Received signal {signum}, shutting down gracefully...")
        self.running = False
        self.save_status()
        self.save_app_database()
        sys.exit(0)

    def log_message(self, message):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        
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

    def load_app_database(self):
        """Load existing app database"""
        try:
            if os.path.exists(self.app_database_file):
                with open(self.app_database_file, 'r', encoding='utf-8') as f:
                    self.device_status['known_apps'] = json.load(f)
                self.log_message(f"Loaded {len(self.device_status['known_apps'])} known apps from database")
            else:
                self.device_status['known_apps'] = {}
                self.log_message("No existing app database found, starting fresh")
        except Exception as e:
            self.log_message(f"ERROR loading app database: {e}")
            self.device_status['known_apps'] = {}

    def save_app_database(self):
        """Save app database to file"""
        try:
            with open(self.app_database_file, 'w', encoding='utf-8') as f:
                json.dump(self.device_status['known_apps'], f, indent=2)
            self.log_message("App database saved")
        except Exception as e:
            self.log_message(f"ERROR saving app database: {e}")

    def discover_new_apps(self):
        """Discover all installed apps on device"""
        self.log_message("Discovering new apps...")
        
        # Get all installed packages
        packages_cmd = "shell pm list packages -3"  # -3 for third-party apps
        result = self.execute_adb_command(packages_cmd)
        
        if not result['success']:
            self.log_message("ERROR: Failed to get package list")
            return
        
        current_apps = set()
        new_apps = []
        
        for line in result['output'].split('\n'):
            if line.startswith('package:'):
                package_name = line.replace('package:', '').strip()
                current_apps.add(package_name)
                
                # Check if this is a new app
                if package_name not in self.device_status['known_apps']:
                    new_apps.append(package_name)
                    self.analyze_new_app(package_name)
        
        # Check for removed apps
        removed_apps = set(self.device_status['known_apps'].keys()) - current_apps
        for app in removed_apps:
            self.log_message(f"App removed: {app}")
            del self.device_status['known_apps'][app]
        
        if new_apps:
            self.log_message(f"Discovered {len(new_apps)} new apps: {', '.join(new_apps)}")
            self.add_alert(f"New apps discovered: {len(new_apps)}")
        else:
            self.log_message("No new apps discovered")

    def analyze_new_app(self, package_name):
        """Analyze a newly discovered app"""
        self.log_message(f"Analyzing new app: {package_name}")
        
        app_info = {
            'package_name': package_name,
            'discovery_time': datetime.now().isoformat(),
            'category': self.categorize_app(package_name),
            'status': 'installed',
            'last_check': datetime.now().isoformat(),
            'metadata': {}
        }
        
        # Get app metadata
        try:
            # Get app label
            label_cmd = f"shell pm dump {package_name} | grep -A 1 'applicationLabel'"
            label_result = self.execute_adb_command(label_cmd)
            if label_result['success']:
                for line in label_result['output'].split('\n'):
                    if 'applicationLabel' in line:
                        app_info['metadata']['label'] = line.split('=')[1].strip() if '=' in line else package_name
                        break
            
            # Get app version
            version_cmd = f"shell pm dump {package_name} | grep versionName"
            version_result = self.execute_adb_command(version_cmd)
            if version_result['success']:
                for line in version_result['output'].split('\n'):
                    if 'versionName' in line:
                        app_info['metadata']['version'] = line.split('=')[1].strip() if '=' in line else 'unknown'
                        break
            
            # Get app size
            size_cmd = f"shell pm path {package_name}"
            size_result = self.execute_adb_command(size_cmd)
            if size_result['success']:
                for line in size_result['output'].split('\n'):
                    if 'package:' in line:
                        apk_path = line.replace('package:', '').strip()
                        if apk_path:
                            # Get file size
                            file_size_cmd = f"shell ls -l {apk_path}"
                            file_size_result = self.execute_adb_command(file_size_cmd)
                            if file_size_result['success']:
                                try:
                                    size_str = file_size_result['output'].split()[4]
                                    app_info['metadata']['size'] = size_str
                                except:
                                    app_info['metadata']['size'] = 'unknown'
                        break
            
        except Exception as e:
            self.log_message(f"ERROR analyzing app {package_name}: {e}")
        
        # Add to known apps
        self.device_status['known_apps'][package_name] = app_info
        self.device_status['newly_discovered_apps'][package_name] = app_info
        
        # Categorize and track
        self.categorize_and_track_app(package_name, app_info)

    def categorize_app(self, package_name):
        """Categorize app based on package name"""
        package_lower = package_name.lower()
        
        # Python apps
        if any(keyword in package_lower for keyword in ['python', 'pydroid', 'qpython', 'termux']):
            return 'python_development'
        
        # File management
        if any(keyword in package_lower for keyword in ['file', 'manager', 'explorer']):
            return 'file_management'
        
        # Notes and text
        if any(keyword in package_lower for keyword in ['note', 'text', 'editor', 'markdown']):
            return 'text_editing'
        
        # Network and communication
        if any(keyword in package_lower for keyword in ['nostr', 'signal', 'element', 'briar', 'chat', 'message']):
            return 'communication'
        
        # System utilities
        if any(keyword in package_lower for keyword in ['system', 'utility', 'tool', 'manager']):
            return 'system_utility'
        
        # Media
        if any(keyword in package_lower for keyword in ['gallery', 'photo', 'video', 'media', 'player']):
            return 'media'
        
        # Development
        if any(keyword in package_lower for keyword in ['code', 'editor', 'ide', 'development', 'programming']):
            return 'development'
        
        # Unknown category
        return 'unknown'

    def categorize_and_track_app(self, package_name, app_info):
        """Categorize and track app in appropriate category"""
        category = app_info['category']
        
        if category not in self.device_status['app_categories']:
            self.device_status['app_categories'][category] = []
        
        if package_name not in self.device_status['app_categories'][category]:
            self.device_status['app_categories'][category].append(package_name)
            self.log_message(f"Added {package_name} to category: {category}")

    def check_app_health(self, package_name, app_info):
        """Check health of specific app"""
        try:
            # Check if app is still installed
            check_cmd = f"shell pm list packages | grep {package_name}"
            result = self.execute_adb_command(check_cmd)
            
            if result['success'] and package_name in result['output']:
                app_info['status'] = 'installed'
                app_info['last_check'] = datetime.now().isoformat()
                
                # Test app functionality based on category
                self.test_app_functionality(package_name, app_info)
            else:
                app_info['status'] = 'not_installed'
                app_info['last_check'] = datetime.now().isoformat()
                self.add_alert(f"App no longer installed: {package_name}")
                
        except Exception as e:
            self.log_message(f"ERROR checking app health for {package_name}: {e}")

    def test_app_functionality(self, package_name, app_info):
        """Test app functionality based on category"""
        category = app_info.get('category', 'unknown')
        
        try:
            if category == 'python_development':
                # Test Python functionality
                if 'pydroid' in package_name.lower():
                    test_cmd = f"shell am start -n {package_name}/.MainActivity"
                    result = self.execute_adb_command(test_cmd)
                    if result['success']:
                        app_info['functionality_test'] = 'passed'
                    else:
                        app_info['functionality_test'] = 'failed'
            
            elif category == 'file_management':
                # Test file manager functionality
                test_cmd = f"shell am start -n {package_name}/.MainActivity"
                result = self.execute_adb_command(test_cmd)
                if result['success']:
                    app_info['functionality_test'] = 'passed'
                else:
                    app_info['functionality_test'] = 'failed'
            
            elif category == 'communication':
                # Test communication app functionality
                test_cmd = f"shell am start -n {package_name}/.MainActivity"
                result = self.execute_adb_command(test_cmd)
                if result['success']:
                    app_info['functionality_test'] = 'passed'
                else:
                    app_info['functionality_test'] = 'failed'
            
            else:
                # Generic test for other categories
                test_cmd = f"shell am start -n {package_name}/.MainActivity"
                result = self.execute_adb_command(test_cmd)
                if result['success']:
                    app_info['functionality_test'] = 'passed'
                else:
                    app_info['functionality_test'] = 'failed'
                    
        except Exception as e:
            self.log_message(f"ERROR testing functionality for {package_name}: {e}")
            app_info['functionality_test'] = 'error'

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
                if app not in self.device_status['known_apps']:
                    self.device_status['known_apps'][app] = {
                        'package_name': app,
                        'discovery_time': datetime.now().isoformat(),
                        'category': 'offline_html',
                        'status': 'installed',
                        'last_check': datetime.now().isoformat(),
                        'metadata': {'type': 'html_app'}
                    }
                else:
                    self.device_status['known_apps'][app]['status'] = 'installed'
                    self.device_status['known_apps'][app]['last_check'] = datetime.now().isoformat()
            else:
                if app in self.device_status['known_apps']:
                    self.device_status['known_apps'][app]['status'] = 'missing'
                    self.device_status['known_apps'][app]['last_check'] = datetime.now().isoformat()

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
        total_apps = len(self.device_status['known_apps'])
        installed_apps = sum(1 for app in self.device_status['known_apps'].values() 
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
        
        # Keep only last 20 alerts
        if len(self.device_status['alerts']) > 20:
            self.device_status['alerts'] = self.device_status['alerts'][-20:]

    def save_status(self):
        """Save current status to file"""
        try:
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump(self.device_status, f, indent=2)
        except Exception as e:
            self.log_message(f"ERROR: Failed to save status: {e}")

    def generate_dynamic_report(self):
        """Generate dynamic health report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'device_status': self.device_status,
            'summary': {
                'device_connected': self.device_status['device_connected'],
                'total_apps': self.device_status['installation_progress']['total_apps'],
                'installed_apps': self.device_status['installation_progress']['installed_apps'],
                'progress_percentage': self.device_status['installation_progress']['progress_percentage'],
                'active_alerts': len(self.device_status['alerts']),
                'newly_discovered': len(self.device_status['newly_discovered_apps'])
            }
        }
        
        # Save report
        with open('dynamic_health_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        # Create human-readable report
        self.create_human_report(report)
        
        # Push to device
        self.push_to_device()

    def create_human_report(self, report):
        """Create human-readable report"""
        report_text = f"""# Dynamic Health Report
Generated: {report['timestamp']}

## Quick Status
- Device Connected: {'✅ YES' if report['summary']['device_connected'] else '❌ NO'}
- Total Apps: {report['summary']['total_apps']}
- Installed Apps: {report['summary']['installed_apps']}
- Progress: {report['summary']['progress_percentage']:.1f}%
- Active Alerts: {report['summary']['active_alerts']}
- Newly Discovered: {report['summary']['newly_discovered']}

## App Categories
"""
        
        for category, apps in report['device_status']['app_categories'].items():
            installed_count = sum(1 for app in apps 
                                if report['device_status']['known_apps'].get(app, {}).get('status') == 'installed')
            report_text += f"- {category.replace('_', ' ').title()}: {installed_count}/{len(apps)} apps\n"
        
        report_text += "\n## Recently Discovered Apps\n"
        
        for app_id, app_data in list(report['device_status']['newly_discovered_apps'].items())[-5:]:
            status_icon = '✅' if app_data['status'] == 'installed' else '❌'
            app_name = app_data.get('metadata', {}).get('label', app_id)
            category = app_data.get('category', 'unknown')
            report_text += f"- {app_name} ({category}): {status_icon} {app_data['status']}\n"
        
        if report['device_status']['alerts']:
            report_text += "\n## Recent Alerts\n"
            for alert in report['device_status']['alerts'][-5:]:
                report_text += f"- {alert['timestamp']}: {alert['message']}\n"
        
        with open('dynamic_health_report.txt', 'w', encoding='utf-8') as f:
            f.write(report_text)

    def push_to_device(self):
        """Push reports to device"""
        files_to_push = [
            'dynamic_health_report.json',
            'dynamic_health_report.txt',
            'dynamic_status.json',
            'app_database.json'
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
        
        if self.check_device_connection():
            # Check known apps
            for package_name, app_info in self.device_status['known_apps'].items():
                self.check_app_health(package_name, app_info)
            
            # Check offline apps
            self.check_offline_apps()
            
            # Check system health
            self.check_system_health()
            
            # Calculate progress
            self.calculate_progress()
            
            # Generate report
            self.generate_dynamic_report()
            
            # Save status
            self.save_status()
            
            # Log summary
            progress = self.device_status['installation_progress']['progress_percentage']
            alerts = len(self.device_status['alerts'])
            new_apps = len(self.device_status['newly_discovered_apps'])
            self.log_message(f"Health check completed - Progress: {progress:.1f}%, Alerts: {alerts}, New apps: {new_apps}")
        else:
            self.log_message("Health check skipped - device not connected")

    def discovery_loop(self):
        """App discovery loop"""
        self.log_message("App discovery loop started")
        
        while self.running:
            try:
                if self.device_status['device_connected']:
                    self.discover_new_apps()
                    self.save_app_database()
                time.sleep(self.discovery_interval)
            except Exception as e:
                self.log_message(f"ERROR in discovery loop: {e}")
                time.sleep(self.discovery_interval)

    def monitoring_loop(self):
        """Main monitoring loop"""
        self.log_message("Dynamic health monitoring started")
        self.log_message(f"Monitoring interval: {self.monitor_interval} seconds")
        self.log_message(f"Discovery interval: {self.discovery_interval} seconds")
        
        while self.running:
            try:
                self.run_health_check()
                time.sleep(self.monitor_interval)
            except Exception as e:
                self.log_message(f"ERROR in monitoring loop: {e}")
                time.sleep(self.monitor_interval)

    def start_monitoring(self):
        """Start the monitoring service"""
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitoring_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        self.log_message("Monitoring thread started")
        
        # Start discovery thread
        self.discovery_thread = threading.Thread(target=self.discovery_loop)
        self.discovery_thread.daemon = True
        self.discovery_thread.start()
        self.log_message("Discovery thread started")

def main():
    """Main function"""
    print("Dynamic Health Monitor Service")
    print("=" * 50)
    print("This service automatically discovers and monitors")
    print("ALL apps on your Samsung Galaxy J3")
    print("No user intervention required!")
    print()
    print("Features:")
    print("- Automatic app discovery every 5 minutes")
    print("- Dynamic categorization of new apps")
    print("- Continuous health monitoring every 30 seconds")
    print("- Intelligent app functionality testing")
    print("- Persistent app database")
    print("- Real-time alerts for new apps")
    print()
    print("Reports available:")
    print("- dynamic_health_report.txt (human readable)")
    print("- dynamic_health_report.json (detailed data)")
    print("- dynamic_status.json (latest status)")
    print("- app_database.json (app catalog)")
    print("- dynamic_health_monitor.log (activity log)")
    print()
    print("Press Ctrl+C to stop the service")
    print("=" * 50)
    
    # Start the dynamic monitor
    monitor = DynamicHealthMonitor()
    
    try:
        # Keep main thread alive
        while monitor.running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down dynamic health monitor...")
        monitor.running = False

if __name__ == '__main__':
    main() 
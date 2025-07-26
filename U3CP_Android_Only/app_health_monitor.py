#!/usr/bin/env python3
"""
App Health Monitor Script
Continuously monitors installation and health of all apps on Samsung Galaxy J3
"""

import subprocess
import os
import time
import json
from datetime import datetime
import threading

class AppHealthMonitor:
    def __init__(self):
        self.device_status = {
            'last_check': None,
            'device_connected': False,
            'fdroid_status': 'unknown',
            'python_status': 'unknown',
            'offline_apps': {},
            'fdroid_apps': {},
            'system_health': {},
            'installation_progress': {},
            'test_results': {}
        }
        
        self.app_definitions = {
            'offline_apps': {
                'offline_launcher.html': {
                    'name': 'Offline Launcher',
                    'type': 'html',
                    'url': 'file:///sdcard/offline_launcher.html',
                    'required': True
                },
                'offline_file_manager.html': {
                    'name': 'File Manager',
                    'type': 'html',
                    'url': 'file:///sdcard/offline_file_manager.html',
                    'required': True
                },
                'offline_notes.html': {
                    'name': 'Notes App',
                    'type': 'html',
                    'url': 'file:///sdcard/offline_notes.html',
                    'required': True
                },
                'offline_calculator.html': {
                    'name': 'Calculator',
                    'type': 'html',
                    'url': 'file:///sdcard/offline_calculator.html',
                    'required': True
                },
                'pure_u3cp.html': {
                    'name': 'U3CP System',
                    'type': 'html',
                    'url': 'file:///sdcard/pure_u3cp.html',
                    'required': True
                }
            },
            'fdroid_apps': {
                'org.pydroid3': {
                    'name': 'Pydroid 3',
                    'type': 'python',
                    'required': True,
                    'test_command': 'python --version'
                },
                'com.hipipal.qpyplus': {
                    'name': 'QPython 3',
                    'type': 'python',
                    'required': False,
                    'test_command': 'python3 --version'
                },
                'com.termux': {
                    'name': 'Termux',
                    'type': 'terminal',
                    'required': True,
                    'test_command': 'pkg --version'
                },
                'com.simplemobiletools.filemanager': {
                    'name': 'Simple File Manager',
                    'type': 'utility',
                    'required': False
                },
                'com.simplemobiletools.notes': {
                    'name': 'Simple Notes',
                    'type': 'utility',
                    'required': False
                },
                'com.github.damus': {
                    'name': 'Nostr Client',
                    'type': 'network',
                    'required': False
                }
            }
        }
        
        self.monitoring_active = False
        self.monitor_thread = None

    def execute_adb_command(self, command):
        """Execute ADB command and return result"""
        try:
            result = subprocess.run(
                ["./platform-tools/adb.exe"] + command.split(),
                capture_output=True,
                text=True,
                cwd=os.getcwd(),
                timeout=30
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
        """Check if device is connected and accessible"""
        print("Checking device connection...")
        
        devices_cmd = "devices"
        result = self.execute_adb_command(devices_cmd)
        
        if result['success'] and 'device' in result['output']:
            self.device_status['device_connected'] = True
            print("SUCCESS: Device connected")
            return True
        else:
            self.device_status['device_connected'] = False
            print("ERROR: Device not connected")
            return False

    def check_fdroid_status(self):
        """Check F-Droid installation and status"""
        print("Checking F-Droid status...")
        
        check_cmd = "shell pm list packages | grep fdroid"
        result = self.execute_adb_command(check_cmd)
        
        if result['success'] and 'fdroid' in result['output'].lower():
            self.device_status['fdroid_status'] = 'installed'
            print("SUCCESS: F-Droid installed")
            
            # Check if F-Droid is running
            running_cmd = "shell ps | grep fdroid"
            running_result = self.execute_adb_command(running_cmd)
            if running_result['success'] and 'fdroid' in running_result['output']:
                self.device_status['fdroid_status'] = 'running'
                print("SUCCESS: F-Droid is running")
            
            return True
        else:
            self.device_status['fdroid_status'] = 'not_installed'
            print("ERROR: F-Droid not installed")
            return False

    def check_python_status(self):
        """Check Python installation status"""
        print("Checking Python status...")
        
        # Check for Python apps
        python_apps = ['org.pydroid3', 'com.hipipal.qpyplus', 'com.termux']
        python_found = False
        
        for app in python_apps:
            check_cmd = f"shell pm list packages | grep {app}"
            result = self.execute_adb_command(check_cmd)
            
            if result['success'] and app in result['output']:
                self.device_status['fdroid_apps'][app] = {
                    'status': 'installed',
                    'last_check': datetime.now().isoformat()
                }
                python_found = True
                print(f"SUCCESS: {app} installed")
            else:
                self.device_status['fdroid_apps'][app] = {
                    'status': 'not_installed',
                    'last_check': datetime.now().isoformat()
                }
                print(f"ERROR: {app} not installed")
        
        if python_found:
            self.device_status['python_status'] = 'available'
        else:
            self.device_status['python_status'] = 'not_available'
        
        return python_found

    def check_offline_apps(self):
        """Check offline HTML apps"""
        print("Checking offline apps...")
        
        for filename, app_info in self.app_definitions['offline_apps'].items():
            check_cmd = f"shell ls /sdcard/{filename}"
            result = self.execute_adb_command(check_cmd)
            
            if result['success'] and 'No such file' not in result['error']:
                self.device_status['offline_apps'][filename] = {
                    'status': 'installed',
                    'name': app_info['name'],
                    'url': app_info['url'],
                    'last_check': datetime.now().isoformat(),
                    'test_result': 'pending'
                }
                print(f"SUCCESS: {app_info['name']} found")
            else:
                self.device_status['offline_apps'][filename] = {
                    'status': 'not_installed',
                    'name': app_info['name'],
                    'url': app_info['url'],
                    'last_check': datetime.now().isoformat(),
                    'test_result': 'failed'
                }
                print(f"ERROR: {app_info['name']} not found")

    def test_app_functionality(self):
        """Test app functionality"""
        print("Testing app functionality...")
        
        # Test offline apps by opening them
        for filename, app_data in self.device_status['offline_apps'].items():
            if app_data['status'] == 'installed':
                print(f"Testing {app_data['name']}...")
                
                # Try to open the app
                open_cmd = f"shell am start -a android.intent.action.VIEW -d '{app_data['url']}' -t text/html"
                result = self.execute_adb_command(open_cmd)
                
                if result['success']:
                    app_data['test_result'] = 'passed'
                    app_data['last_test'] = datetime.now().isoformat()
                    print(f"SUCCESS: {app_data['name']} test passed")
                else:
                    app_data['test_result'] = 'failed'
                    app_data['last_test'] = datetime.now().isoformat()
                    app_data['test_error'] = result['error']
                    print(f"ERROR: {app_data['name']} test failed")

    def check_system_health(self):
        """Check overall system health"""
        print("Checking system health...")
        
        # Check storage
        storage_cmd = "shell df /sdcard"
        storage_result = self.execute_adb_command(storage_cmd)
        
        if storage_result['success']:
            self.device_status['system_health']['storage'] = {
                'status': 'ok',
                'data': storage_result['output'],
                'last_check': datetime.now().isoformat()
            }
            print("SUCCESS: Storage check passed")
        else:
            self.device_status['system_health']['storage'] = {
                'status': 'error',
                'error': storage_result['error'],
                'last_check': datetime.now().isoformat()
            }
            print("ERROR: Storage check failed")
        
        # Check memory
        memory_cmd = "shell cat /proc/meminfo"
        memory_result = self.execute_adb_command(memory_cmd)
        
        if memory_result['success']:
            self.device_status['system_health']['memory'] = {
                'status': 'ok',
                'data': memory_result['output'],
                'last_check': datetime.now().isoformat()
            }
            print("SUCCESS: Memory check passed")
        else:
            self.device_status['system_health']['memory'] = {
                'status': 'error',
                'error': memory_result['error'],
                'last_check': datetime.now().isoformat()
            }
            print("ERROR: Memory check failed")

    def calculate_installation_progress(self):
        """Calculate overall installation progress"""
        print("Calculating installation progress...")
        
        total_apps = len(self.app_definitions['offline_apps']) + len(self.app_definitions['fdroid_apps'])
        installed_apps = 0
        
        # Count offline apps
        for app_data in self.device_status['offline_apps'].values():
            if app_data['status'] == 'installed':
                installed_apps += 1
        
        # Count F-Droid apps
        for app_data in self.device_status['fdroid_apps'].values():
            if app_data['status'] == 'installed':
                installed_apps += 1
        
        progress_percentage = (installed_apps / total_apps) * 100 if total_apps > 0 else 0
        
        self.device_status['installation_progress'] = {
            'total_apps': total_apps,
            'installed_apps': installed_apps,
            'progress_percentage': progress_percentage,
            'last_calculation': datetime.now().isoformat()
        }
        
        print(f"Progress: {installed_apps}/{total_apps} apps installed ({progress_percentage:.1f}%)")

    def generate_health_report(self):
        """Generate comprehensive health report"""
        print("Generating health report...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'device_status': self.device_status,
            'summary': {
                'device_connected': self.device_status['device_connected'],
                'fdroid_working': self.device_status['fdroid_status'] in ['installed', 'running'],
                'python_available': self.device_status['python_status'] == 'available',
                'offline_apps_working': all(app['status'] == 'installed' for app in self.device_status['offline_apps'].values()),
                'overall_health': 'good' if self.device_status['device_connected'] else 'poor'
            }
        }
        
        # Save report to file
        with open('app_health_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        # Create human-readable report
        human_report = self.create_human_readable_report(report)
        with open('app_health_report.txt', 'w', encoding='utf-8') as f:
            f.write(human_report)
        
        # Push reports to device
        self.push_reports_to_device()
        
        print("SUCCESS: Health report generated")
        return report

    def create_human_readable_report(self, report):
        """Create human-readable health report"""
        report_text = f"""# App Health Report
Generated: {report['timestamp']}

## Device Status
- Device Connected: {'✅ YES' if report['summary']['device_connected'] else '❌ NO'}
- F-Droid Working: {'✅ YES' if report['summary']['fdroid_working'] else '❌ NO'}
- Python Available: {'✅ YES' if report['summary']['python_available'] else '❌ NO'}
- Offline Apps Working: {'✅ YES' if report['summary']['offline_apps_working'] else '❌ NO'}
- Overall Health: {report['summary']['overall_health'].upper()}

## Installation Progress
- Total Apps: {report['device_status']['installation_progress']['total_apps']}
- Installed Apps: {report['device_status']['installation_progress']['installed_apps']}
- Progress: {report['device_status']['installation_progress']['progress_percentage']:.1f}%

## Offline Apps Status
"""
        
        for filename, app_data in report['device_status']['offline_apps'].items():
            status_icon = '✅' if app_data['status'] == 'installed' else '❌'
            test_icon = '✅' if app_data.get('test_result') == 'passed' else '❌'
            report_text += f"- {app_data['name']}: {status_icon} Installed, {test_icon} Tested\n"
        
        report_text += "\n## F-Droid Apps Status\n"
        
        for app_id, app_data in report['device_status']['fdroid_apps'].items():
            status_icon = '✅' if app_data['status'] == 'installed' else '❌'
            app_name = self.app_definitions['fdroid_apps'].get(app_id, {}).get('name', app_id)
            report_text += f"- {app_name}: {status_icon} Installed\n"
        
        report_text += f"\n## System Health
- Storage: {report['device_status']['system_health']['storage']['status']}
- Memory: {report['device_status']['system_health']['memory']['status']}

## Recommendations
"""
        
        if not report['summary']['device_connected']:
            report_text += "- Connect device via USB and enable ADB\n"
        
        if not report['summary']['fdroid_working']:
            report_text += "- Install F-Droid to get Python apps\n"
        
        if not report['summary']['offline_apps_working']:
            report_text += "- Re-run offline apps installation\n"
        
        if report['summary']['overall_health'] == 'good':
            report_text += "- All systems operational! 🎉\n"
        
        return report_text

    def push_reports_to_device(self):
        """Push health reports to device"""
        print("Pushing health reports to device...")
        
        reports = ['app_health_report.json', 'app_health_report.txt']
        
        for report in reports:
            if os.path.exists(report):
                push_cmd = f"push {report} /sdcard/"
                result = self.execute_adb_command(push_cmd)
                
                if result['success']:
                    print(f"SUCCESS: {report} pushed to device")
                else:
                    print(f"ERROR: Failed to push {report}")

    def run_full_health_check(self):
        """Run complete health check"""
        print("Running full health check...")
        print("=" * 50)
        
        self.device_status['last_check'] = datetime.now().isoformat()
        
        # Check device connection
        if not self.check_device_connection():
            print("ERROR: Cannot proceed without device connection")
            return False
        
        # Check F-Droid status
        self.check_fdroid_status()
        
        # Check Python status
        self.check_python_status()
        
        # Check offline apps
        self.check_offline_apps()
        
        # Test app functionality
        self.test_app_functionality()
        
        # Check system health
        self.check_system_health()
        
        # Calculate progress
        self.calculate_installation_progress()
        
        # Generate report
        report = self.generate_health_report()
        
        print("=" * 50)
        print("Health check completed!")
        print(f"Overall Health: {report['summary']['overall_health'].upper()}")
        print(f"Progress: {report['device_status']['installation_progress']['progress_percentage']:.1f}%")
        
        return True

    def start_continuous_monitoring(self, interval_seconds=60):
        """Start continuous monitoring"""
        print(f"Starting continuous monitoring (check every {interval_seconds} seconds)...")
        
        self.monitoring_active = True
        
        def monitor_loop():
            while self.monitoring_active:
                try:
                    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running health check...")
                    self.run_full_health_check()
                    
                    # Wait for next check
                    time.sleep(interval_seconds)
                    
                except KeyboardInterrupt:
                    print("\nMonitoring stopped by user")
                    break
                except Exception as e:
                    print(f"ERROR in monitoring loop: {e}")
                    time.sleep(interval_seconds)
        
        self.monitor_thread = threading.Thread(target=monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        print("Continuous monitoring started!")
        print("Press Ctrl+C to stop monitoring")

    def stop_monitoring(self):
        """Stop continuous monitoring"""
        print("Stopping continuous monitoring...")
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        print("Monitoring stopped")

def main():
    """Main health monitoring process"""
    print("App Health Monitor for Samsung Galaxy J3")
    print("=" * 50)
    
    monitor = AppHealthMonitor()
    
    try:
        # Run initial health check
        print("Running initial health check...")
        monitor.run_full_health_check()
        
        # Ask user if they want continuous monitoring
        print("\nHealth check completed!")
        print("Would you like to start continuous monitoring?")
        print("This will check app health every 60 seconds.")
        print("Press Enter to start monitoring, or Ctrl+C to exit...")
        
        input()  # Wait for user input
        
        # Start continuous monitoring
        monitor.start_continuous_monitoring()
        
        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping monitoring...")
            monitor.stop_monitoring()
    
    except KeyboardInterrupt:
        print("\nHealth monitoring stopped by user")
    except Exception as e:
        print(f"ERROR: {e}")
        monitor.stop_monitoring()

if __name__ == '__main__':
    main() 
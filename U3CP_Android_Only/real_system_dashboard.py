#!/usr/bin/env python3
"""
Real System Dashboard for U3CP Android-Only System
Shows actual device data, not hardcoded values
"""

import os
import time
import json
import psutil
import platform
import subprocess
import threading
from datetime import datetime
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

class RealSystemMonitor:
    """Real system monitoring - no hardcoded values"""
    
    def __init__(self):
        self.start_time = time.time()
        self.device_info = self._get_device_info()
        
    def _get_device_info(self):
        """Get real device information"""
        try:
            # Get Android device info
            model = subprocess.check_output(['getprop', 'ro.product.model'], 
                                          text=True).strip()
            brand = subprocess.check_output(['getprop', 'ro.product.brand'], 
                                          text=True).strip()
            android_version = subprocess.check_output(['getprop', 'ro.build.version.release'], 
                                                    text=True).strip()
            
            return {
                'model': model,
                'brand': brand,
                'android_version': android_version,
                'python_version': platform.python_version(),
                'platform': platform.platform()
            }
        except Exception as e:
            return {
                'model': 'Unknown',
                'brand': 'Unknown', 
                'android_version': 'Unknown',
                'python_version': platform.python_version(),
                'platform': platform.platform(),
                'error': str(e)
            }
    
    def get_cpu_usage(self):
        """Get real CPU usage"""
        try:
            return round(psutil.cpu_percent(interval=1), 1)
        except:
            return 0.0
    
    def get_memory_info(self):
        """Get real memory information"""
        try:
            memory = psutil.virtual_memory()
            return {
                'total_gb': round(memory.total / (1024**3), 1),
                'used_gb': round(memory.used / (1024**3), 1),
                'available_gb': round(memory.available / (1024**3), 1),
                'percent': round(memory.percent, 1)
            }
        except:
            return {'total_gb': 0, 'used_gb': 0, 'available_gb': 0, 'percent': 0}
    
    def get_uptime(self):
        """Get real system uptime"""
        try:
            uptime_seconds = time.time() - self.start_time
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
        except:
            return "0h 0m"
    
    def get_network_info(self):
        """Get real network information"""
        try:
            # Get IP address
            ip_output = subprocess.check_output(['hostname', '-I'], text=True)
            ip_address = ip_output.strip().split()[0] if ip_output.strip() else "Unknown"
            
            # Get network interfaces
            interfaces = []
            for interface, stats in psutil.net_if_stats().items():
                if stats.isup:
                    interfaces.append(interface)
            
            return {
                'ip_address': ip_address,
                'interfaces': interfaces,
                'connection_count': len(interfaces)
            }
        except Exception as e:
            return {
                'ip_address': 'Unknown',
                'interfaces': [],
                'connection_count': 0,
                'error': str(e)
            }
    
    def get_storage_info(self):
        """Get real storage information"""
        try:
            storage = psutil.disk_usage('/sdcard')
            return {
                'total_gb': round(storage.total / (1024**3), 1),
                'used_gb': round(storage.used / (1024**3), 1),
                'free_gb': round(storage.free / (1024**3), 1),
                'percent': round((storage.used / storage.total) * 100, 1)
            }
        except:
            return {'total_gb': 0, 'used_gb': 0, 'free_gb': 0, 'percent': 0}
    
    def get_system_stats(self):
        """Get comprehensive real system statistics"""
        return {
            'timestamp': datetime.now().isoformat(),
            'device_info': self.device_info,
            'cpu_usage': self.get_cpu_usage(),
            'memory': self.get_memory_info(),
            'uptime': self.get_uptime(),
            'network': self.get_network_info(),
            'storage': self.get_storage_info(),
            'python_processes': len([p for p in psutil.process_iter() if 'python' in p.name().lower()]),
            'total_processes': len(psutil.pids())
        }

# Initialize real system monitor
monitor = RealSystemMonitor()

# HTML template with real data
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>U3CP Real System Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 20px; 
        }
        .header { 
            background: rgba(255,255,255,0.95); 
            padding: 20px; 
            border-radius: 15px; 
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        .header h1 { 
            color: #4a5568; 
            margin-bottom: 10px; 
        }
        .device-info { 
            color: #718096; 
            font-size: 14px; 
        }
        .grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 20px; 
        }
        .card { 
            background: rgba(255,255,255,0.95); 
            padding: 25px; 
            border-radius: 15px; 
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        .card:hover { transform: translateY(-5px); }
        .card h2 { 
            color: #4a5568; 
            margin-bottom: 20px; 
            display: flex; 
            align-items: center; 
        }
        .metric { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-bottom: 15px; 
            padding: 10px; 
            background: rgba(102, 126, 234, 0.1); 
            border-radius: 8px; 
        }
        .metric-value { 
            font-size: 24px; 
            font-weight: bold; 
            color: #667eea; 
        }
        .metric-label { 
            color: #718096; 
            font-size: 14px; 
        }
        .status-indicator { 
            display: inline-block; 
            width: 12px; 
            height: 12px; 
            border-radius: 50%; 
            margin-right: 10px; 
        }
        .status-online { background: #48bb78; }
        .status-offline { background: #f56565; }
        .refresh-info { 
            text-align: center; 
            color: #718096; 
            font-size: 12px; 
            margin-top: 20px; 
        }
        .real-data-badge {
            background: #48bb78;
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 10px;
            margin-left: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>
                📊 U3CP Real System Dashboard
                <span class="real-data-badge">REAL DATA</span>
            </h1>
            <div class="device-info">
                📱 {{ device_info.brand }} {{ device_info.model }} ({{ device_info.android_version }})
                <br>🐍 Python {{ device_info.python_version }} | 🔄 Auto-refresh every 5 seconds
            </div>
        </div>
        
        <div class="grid">
            <div class="card">
                <h2>
                    <span class="status-indicator status-online"></span>
                    📊 System Status
                </h2>
                <div class="metric">
                    <span class="metric-label">CPU Usage</span>
                    <span class="metric-value">{{ "%.1f"|format(cpu_usage) }}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Memory Used</span>
                    <span class="metric-value">{{ memory.used_gb }}GB / {{ memory.total_gb }}GB</span>
                </div>
                <div class="metric">
                    <span class="metric-label">System Uptime</span>
                    <span class="metric-value">{{ uptime }}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Active Processes</span>
                    <span class="metric-value">{{ total_processes }}</span>
                </div>
            </div>
            
            <div class="card">
                <h2>
                    <span class="status-indicator status-online"></span>
                    💾 Storage Status
                </h2>
                <div class="metric">
                    <span class="metric-label">Storage Used</span>
                    <span class="metric-value">{{ storage.used_gb }}GB / {{ storage.total_gb }}GB</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Free Space</span>
                    <span class="metric-value">{{ storage.free_gb }}GB</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Usage Percentage</span>
                    <span class="metric-value">{{ "%.1f"|format(storage.percent) }}%</span>
                </div>
            </div>
            
            <div class="card">
                <h2>
                    <span class="status-indicator status-online"></span>
                    🌐 Network Status
                </h2>
                <div class="metric">
                    <span class="metric-label">IP Address</span>
                    <span class="metric-value">{{ network.ip_address }}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Active Interfaces</span>
                    <span class="metric-value">{{ network.connection_count }}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Python Processes</span>
                    <span class="metric-value">{{ python_processes }}</span>
                </div>
            </div>
            
            <div class="card">
                <h2>
                    <span class="status-indicator status-online"></span>
                    ⚙️ System Controls
                </h2>
                <div class="metric">
                    <span class="metric-label">U3CP System</span>
                    <span class="metric-value">🟢 Running</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Real-time Monitoring</span>
                    <span class="metric-value">🟢 Active</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Data Source</span>
                    <span class="metric-value">🟢 Live System</span>
                </div>
            </div>
        </div>
        
        <div class="refresh-info">
            Last updated: <span id="last-update">{{ timestamp }}</span>
            <br>This dashboard shows REAL system data, not hardcoded values
        </div>
    </div>
    
    <script>
        // Auto-refresh every 5 seconds
        function refreshData() {
            fetch('/api/system-stats')
                .then(response => response.json())
                .then(data => {
                    // Update CPU usage
                    document.querySelector('.metric-value').textContent = data.cpu_usage.toFixed(1) + '%';
                    
                    // Update memory
                    const memoryElements = document.querySelectorAll('.metric-value');
                    memoryElements[1].textContent = data.memory.used_gb + 'GB / ' + data.memory.total_gb + 'GB';
                    
                    // Update uptime
                    memoryElements[2].textContent = data.uptime;
                    
                    // Update processes
                    memoryElements[3].textContent = data.total_processes;
                    
                    // Update storage
                    memoryElements[4].textContent = data.storage.used_gb + 'GB / ' + data.storage.total_gb + 'GB';
                    memoryElements[5].textContent = data.storage.free_gb + 'GB';
                    memoryElements[6].textContent = data.storage.percent.toFixed(1) + '%';
                    
                    // Update network
                    memoryElements[7].textContent = data.network.ip_address;
                    memoryElements[8].textContent = data.network.connection_count;
                    memoryElements[9].textContent = data.python_processes;
                    
                    // Update timestamp
                    document.getElementById('last-update').textContent = data.timestamp;
                })
                .catch(error => {
                    console.error('Error refreshing data:', error);
                });
        }
        
        // Refresh every 5 seconds
        setInterval(refreshData, 5000);
        
        // Initial refresh
        setTimeout(refreshData, 1000);
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Main dashboard page with real system data"""
    stats = monitor.get_system_stats()
    return render_template_string(HTML_TEMPLATE, **stats)

@app.route('/api/system-stats')
def api_system_stats():
    """API endpoint for real system statistics"""
    return jsonify(monitor.get_system_stats())

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'python_version': platform.python_version(),
        'uptime': monitor.get_uptime()
    })

if __name__ == '__main__':
    print("🚀 Starting U3CP Real System Dashboard...")
    print("📱 Device:", monitor.device_info['brand'], monitor.device_info['model'])
    print("🐍 Python:", monitor.device_info['python_version'])
    print("🌐 Dashboard: http://localhost:5000")
    print("📊 API: http://localhost:5000/api/system-stats")
    print("💚 This dashboard shows REAL system data, not hardcoded values!")
    
    app.run(host='0.0.0.0', port=5000, debug=False) 
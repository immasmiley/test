#!/usr/bin/env python3
"""
U3CP Web Dashboard Interface
Provides a user-friendly web interface for the U3CP Android-Only system
"""

import os
import json
import time
import threading
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import qrcode
import base64
from io import BytesIO

# Import U3CP system components
from U3CP_Android_Only_System import U3CPAndroidOnlySystem

app = Flask(__name__)
app.config['SECRET_KEY'] = 'u3cp_dashboard_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

class U3CPDashboard:
    def __init__(self):
        self.u3cp_system = U3CPAndroidOnlySystem()
        self.device_info = {
            'name': 'Samsung Galaxy J3',
            'model': 'SM-J337P',
            'android_version': '9',
            'status': 'Online',
            'uptime': 0,
            'network_devices': [],
            'messages': [],
            'system_stats': {}
        }
        self.start_time = time.time()
        
    def get_device_info(self):
        """Get current device information"""
        uptime = int(time.time() - self.start_time)
        hours = uptime // 3600
        minutes = (uptime % 3600) // 60
        seconds = uptime % 60
        
        return {
            'name': self.device_info['name'],
            'model': self.device_info['model'],
            'android_version': self.device_info['android_version'],
            'status': self.device_info['status'],
            'uptime': f"{hours:02d}:{minutes:02d}:{seconds:02d}",
            'ip_address': self.get_local_ip(),
            'network_devices_count': len(self.device_info['network_devices']),
            'messages_count': len(self.device_info['messages'])
        }
    
    def get_local_ip(self):
        """Get local IP address"""
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def generate_qr_code(self, data):
        """Generate QR code for easy connection"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        return base64.b64encode(buffer.getvalue()).decode()

# Initialize dashboard
dashboard = U3CPDashboard()

@app.route('/')
def index():
    """Main dashboard page"""
    device_info = dashboard.get_device_info()
    qr_code = dashboard.generate_qr_code(f"http://{device_info['ip_address']}:5000")
    
    return render_template('dashboard.html', 
                         device_info=device_info,
                         qr_code=qr_code)

@app.route('/api/device-info')
def api_device_info():
    """API endpoint for device information"""
    return jsonify(dashboard.get_device_info())

@app.route('/api/network-devices')
def api_network_devices():
    """API endpoint for network devices"""
    return jsonify(dashboard.device_info['network_devices'])

@app.route('/api/messages')
def api_messages():
    """API endpoint for messages"""
    return jsonify(dashboard.device_info['messages'])

@app.route('/api/system-stats')
def api_system_stats():
    """API endpoint for system statistics"""
    return jsonify(dashboard.device_info['system_stats'])

@app.route('/api/send-message', methods=['POST'])
def api_send_message():
    """API endpoint to send message"""
    data = request.json
    message = data.get('message', '')
    target_device = data.get('target_device', 'broadcast')
    
    if message:
        # Add to messages list
        dashboard.device_info['messages'].append({
            'id': len(dashboard.device_info['messages']) + 1,
            'content': message,
            'sender': dashboard.device_info['name'],
            'target': target_device,
            'timestamp': datetime.now().isoformat(),
            'type': 'sent'
        })
        
        # Send via U3CP system
        try:
            dashboard.u3cp_system.send_message(message, target_device)
        except Exception as e:
            print(f"Error sending message: {e}")
    
    return jsonify({'status': 'success'})

@app.route('/api/start-system')
def api_start_system():
    """API endpoint to start U3CP system"""
    try:
        dashboard.u3cp_system.start()
        dashboard.device_info['status'] = 'Running'
        return jsonify({'status': 'success', 'message': 'U3CP system started'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/stop-system')
def api_stop_system():
    """API endpoint to stop U3CP system"""
    try:
        dashboard.u3cp_system.stop()
        dashboard.device_info['status'] = 'Stopped'
        return jsonify({'status': 'success', 'message': 'U3CP system stopped'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/scan-network')
def api_scan_network():
    """API endpoint to scan network for devices"""
    try:
        devices = dashboard.u3cp_system.scan_network()
        dashboard.device_info['network_devices'] = devices
        return jsonify({'status': 'success', 'devices': devices})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    print('Client connected')
    emit('status', {'message': 'Connected to U3CP Dashboard'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    print('Client disconnected')

def update_dashboard():
    """Background task to update dashboard data"""
    while True:
        try:
            # Update system stats
            dashboard.device_info['system_stats'] = {
                'cpu_usage': dashboard.u3cp_system.get_cpu_usage(),
                'memory_usage': dashboard.u3cp_system.get_memory_usage(),
                'network_activity': dashboard.u3cp_system.get_network_activity(),
                'u3cp_cycles': dashboard.u3cp_system.get_cycle_count()
            }
            
            # Emit updates to connected clients
            socketio.emit('dashboard_update', dashboard.get_device_info())
            socketio.emit('system_stats_update', dashboard.device_info['system_stats'])
            
            time.sleep(5)  # Update every 5 seconds
            
        except Exception as e:
            print(f"Dashboard update error: {e}")
            time.sleep(10)

def create_templates():
    """Create HTML templates for the dashboard"""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # Create dashboard.html template
    dashboard_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>U3CP Dashboard</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .header h1 {
            color: #4a5568;
            margin-bottom: 10px;
            font-size: 2.5em;
            text-align: center;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-online { background-color: #48bb78; }
        .status-offline { background-color: #f56565; }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .card h3 {
            color: #4a5568;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .device-info {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }
        
        .info-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .info-item:last-child {
            border-bottom: none;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            margin: 5px;
            transition: transform 0.2s;
        }
        
        .btn:hover {
            transform: translateY(-2px);
        }
        
        .btn-danger {
            background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
        }
        
        .btn-success {
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        }
        
        .message-container {
            max-height: 300px;
            overflow-y: auto;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 10px;
        }
        
        .message {
            padding: 8px;
            margin: 5px 0;
            border-radius: 8px;
            background: #f7fafc;
        }
        
        .message.sent {
            background: #e6fffa;
            border-left: 4px solid #48bb78;
        }
        
        .message.received {
            background: #fff5f5;
            border-left: 4px solid #f56565;
        }
        
        .message-input {
            width: 100%;
            padding: 12px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            margin-top: 10px;
            font-size: 14px;
        }
        
        .qr-container {
            text-align: center;
            margin-top: 20px;
        }
        
        .qr-code {
            max-width: 200px;
            border-radius: 10px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        
        .stat-item {
            text-align: center;
            padding: 15px;
            background: #f7fafc;
            border-radius: 10px;
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #4a5568;
        }
        
        .stat-label {
            color: #718096;
            font-size: 0.9em;
            margin-top: 5px;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
            
            .device-info {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 U3CP Dashboard</h1>
            <p style="text-align: center; color: #718096;">
                Samsung Galaxy J3 - Android-to-Android Communication System
            </p>
        </div>
        
        <div class="dashboard-grid">
            <!-- Device Information Card -->
            <div class="card">
                <h3>📱 Device Information</h3>
                <div class="device-info" id="device-info">
                    <div class="info-item">
                        <span>Name:</span>
                        <span id="device-name">{{ device_info.name }}</span>
                    </div>
                    <div class="info-item">
                        <span>Model:</span>
                        <span id="device-model">{{ device_info.model }}</span>
                    </div>
                    <div class="info-item">
                        <span>Android:</span>
                        <span id="android-version">{{ device_info.android_version }}</span>
                    </div>
                    <div class="info-item">
                        <span>Status:</span>
                        <span>
                            <span class="status-indicator status-{{ device_info.status.lower() }}"></span>
                            <span id="device-status">{{ device_info.status }}</span>
                        </span>
                    </div>
                    <div class="info-item">
                        <span>Uptime:</span>
                        <span id="device-uptime">{{ device_info.uptime }}</span>
                    </div>
                    <div class="info-item">
                        <span>IP Address:</span>
                        <span id="device-ip">{{ device_info.ip_address }}</span>
                    </div>
                </div>
                
                <div class="qr-container">
                    <h4>📱 Connect via QR Code</h4>
                    <img src="data:image/png;base64,{{ qr_code }}" alt="QR Code" class="qr-code">
                    <p style="margin-top: 10px; color: #718096; font-size: 0.9em;">
                        Scan with another device to connect
                    </p>
                </div>
            </div>
            
            <!-- System Controls Card -->
            <div class="card">
                <h3>⚙️ System Controls</h3>
                <div style="text-align: center; margin-bottom: 20px;">
                    <button class="btn btn-success" onclick="startSystem()">🚀 Start System</button>
                    <button class="btn btn-danger" onclick="stopSystem()">⏹️ Stop System</button>
                    <button class="btn" onclick="scanNetwork()">🔍 Scan Network</button>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-value" id="network-devices">{{ device_info.network_devices_count }}</div>
                        <div class="stat-label">Network Devices</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="messages-count">{{ device_info.messages_count }}</div>
                        <div class="stat-label">Messages</div>
                    </div>
                </div>
            </div>
            
            <!-- System Statistics Card -->
            <div class="card">
                <h3>📊 System Statistics</h3>
                <canvas id="statsChart" width="400" height="200"></canvas>
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-value" id="cpu-usage">0%</div>
                        <div class="stat-label">CPU Usage</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="memory-usage">0%</div>
                        <div class="stat-label">Memory Usage</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="network-activity">0</div>
                        <div class="stat-label">Network Activity</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="u3cp-cycles">0</div>
                        <div class="stat-label">U3CP Cycles</div>
                    </div>
                </div>
            </div>
            
            <!-- Network Devices Card -->
            <div class="card">
                <h3>🌐 Network Devices</h3>
                <div id="network-devices-list" style="max-height: 200px; overflow-y: auto;">
                    <p style="color: #718096; text-align: center;">No devices found</p>
                </div>
            </div>
            
            <!-- Messaging Card -->
            <div class="card">
                <h3>💬 Messaging</h3>
                <div class="message-container" id="messages-container">
                    <p style="color: #718096; text-align: center;">No messages yet</p>
                </div>
                <input type="text" class="message-input" id="message-input" placeholder="Type your message...">
                <button class="btn" onclick="sendMessage()" style="width: 100%; margin-top: 10px;">📤 Send Message</button>
            </div>
        </div>
    </div>
    
    <script>
        // Connect to WebSocket
        const socket = io();
        
        // Chart.js setup
        const ctx = document.getElementById('statsChart').getContext('2d');
        const statsChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'CPU Usage',
                    data: [],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4
                }, {
                    label: 'Memory Usage',
                    data: [],
                    borderColor: '#764ba2',
                    backgroundColor: 'rgba(118, 75, 162, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
        
        // Update dashboard data
        function updateDashboard(data) {
            document.getElementById('device-status').textContent = data.status;
            document.getElementById('device-uptime').textContent = data.uptime;
            document.getElementById('network-devices').textContent = data.network_devices_count;
            document.getElementById('messages-count').textContent = data.messages_count;
            
            // Update status indicator
            const indicator = document.querySelector('.status-indicator');
            indicator.className = `status-indicator status-${data.status.toLowerCase()}`;
        }
        
        // Update system statistics
        function updateSystemStats(stats) {
            document.getElementById('cpu-usage').textContent = stats.cpu_usage + '%';
            document.getElementById('memory-usage').textContent = stats.memory_usage + '%';
            document.getElementById('network-activity').textContent = stats.network_activity;
            document.getElementById('u3cp-cycles').textContent = stats.u3cp_cycles;
            
            // Update chart
            const now = new Date().toLocaleTimeString();
            statsChart.data.labels.push(now);
            statsChart.data.datasets[0].data.push(stats.cpu_usage);
            statsChart.data.datasets[1].data.push(stats.memory_usage);
            
            if (statsChart.data.labels.length > 20) {
                statsChart.data.labels.shift();
                statsChart.data.datasets[0].data.shift();
                statsChart.data.datasets[1].data.shift();
            }
            
            statsChart.update();
        }
        
        // System control functions
        function startSystem() {
            fetch('/api/start-system')
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('U3CP system started successfully!');
                    } else {
                        alert('Error: ' + data.message);
                    }
                });
        }
        
        function stopSystem() {
            fetch('/api/stop-system')
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('U3CP system stopped successfully!');
                    } else {
                        alert('Error: ' + data.message);
                    }
                });
        }
        
        function scanNetwork() {
            fetch('/api/scan-network')
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        updateNetworkDevices(data.devices);
                    } else {
                        alert('Error: ' + data.message);
                    }
                });
        }
        
        function updateNetworkDevices(devices) {
            const container = document.getElementById('network-devices-list');
            if (devices.length === 0) {
                container.innerHTML = '<p style="color: #718096; text-align: center;">No devices found</p>';
                return;
            }
            
            container.innerHTML = devices.map(device => `
                <div style="padding: 10px; border-bottom: 1px solid #e2e8f0;">
                    <strong>${device.name}</strong><br>
                    <small>${device.ip}:${device.port}</small>
                </div>
            `).join('');
        }
        
        function sendMessage() {
            const input = document.getElementById('message-input');
            const message = input.value.trim();
            
            if (message) {
                fetch('/api/send-message', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        message: message,
                        target_device: 'broadcast'
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        input.value = '';
                        loadMessages();
                    }
                });
            }
        }
        
        function loadMessages() {
            fetch('/api/messages')
                .then(response => response.json())
                .then(messages => {
                    const container = document.getElementById('messages-container');
                    if (messages.length === 0) {
                        container.innerHTML = '<p style="color: #718096; text-align: center;">No messages yet</p>';
                        return;
                    }
                    
                    container.innerHTML = messages.map(msg => `
                        <div class="message ${msg.type}">
                            <strong>${msg.sender}</strong> → ${msg.target}<br>
                            <span>${msg.content}</span><br>
                            <small>${new Date(msg.timestamp).toLocaleString()}</small>
                        </div>
                    `).join('');
                    
                    container.scrollTop = container.scrollHeight;
                });
        }
        
        // WebSocket event handlers
        socket.on('dashboard_update', updateDashboard);
        socket.on('system_stats_update', updateSystemStats);
        
        // Enter key to send message
        document.getElementById('message-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Load initial data
        loadMessages();
        
        // Auto-refresh every 30 seconds
        setInterval(loadMessages, 30000);
    </script>
</body>
</html>'''
    
    with open(os.path.join(templates_dir, 'dashboard.html'), 'w', encoding='utf-8') as f:
        f.write(dashboard_html)

def main():
    """Main function to start the dashboard"""
    print("🚀 Starting U3CP Web Dashboard...")
    
    # Create templates
    create_templates()
    
    # Start background update thread
    update_thread = threading.Thread(target=update_dashboard, daemon=True)
    update_thread.start()
    
    # Get device info
    device_info = dashboard.get_device_info()
    print(f"📱 Dashboard available at: http://{device_info['ip_address']}:5000")
    print(f"📱 QR Code generated for easy connection")
    
    # Start Flask app
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    main() 
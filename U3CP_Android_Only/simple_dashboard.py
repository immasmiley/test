#!/usr/bin/env python3
"""
Simple U3CP Dashboard
A lightweight web interface for the U3CP Android-Only system
"""

import os
import json
import time
import threading
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify
import socket

app = Flask(__name__)

# HTML template for the dashboard
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>U3CP Dashboard</title>
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
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        .header h1 {
            color: #4a5568;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        .card h3 {
            color: #4a5568;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .status-item {
            text-align: center;
            padding: 15px;
            background: #f7fafc;
            border-radius: 10px;
        }
        
        .status-value {
            font-size: 2em;
            font-weight: bold;
            color: #4a5568;
        }
        
        .status-label {
            color: #718096;
            font-size: 0.9em;
            margin-top: 5px;
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
        
        .btn-success {
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        }
        
        .btn-danger {
            background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
        }
        
        .message-container {
            max-height: 300px;
            overflow-y: auto;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 15px;
        }
        
        .message {
            padding: 8px;
            margin: 5px 0;
            border-radius: 8px;
            background: #f7fafc;
        }
        
        .message-input {
            width: 100%;
            padding: 12px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            margin-bottom: 10px;
            font-size: 14px;
        }
        
        .device-list {
            max-height: 200px;
            overflow-y: auto;
        }
        
        .device-item {
            padding: 10px;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .device-item:last-child {
            border-bottom: none;
        }
        
        .online-indicator {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #48bb78;
            display: inline-block;
            margin-right: 10px;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .status-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 U3CP Dashboard</h1>
            <p>Samsung Galaxy J3 - Android-to-Android Communication System</p>
        </div>
        
        <div class="card">
            <h3>📱 Device Status</h3>
            <div class="status-grid">
                <div class="status-item">
                    <div class="status-value" id="device-status">Online</div>
                    <div class="status-label">Status</div>
                </div>
                <div class="status-item">
                    <div class="status-value" id="uptime">00:00:00</div>
                    <div class="status-label">Uptime</div>
                </div>
                <div class="status-item">
                    <div class="status-value" id="network-devices">0</div>
                    <div class="status-label">Network Devices</div>
                </div>
                <div class="status-item">
                    <div class="status-value" id="messages-count">0</div>
                    <div class="status-label">Messages</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h3>⚙️ System Controls</h3>
            <div style="text-align: center;">
                <button class="btn btn-success" onclick="startSystem()">🚀 Start System</button>
                <button class="btn btn-danger" onclick="stopSystem()">⏹️ Stop System</button>
                <button class="btn" onclick="scanNetwork()">🔍 Scan Network</button>
                <button class="btn" onclick="refreshData()">🔄 Refresh</button>
            </div>
        </div>
        
        <div class="card">
            <h3>🌐 Network Devices</h3>
            <div class="device-list" id="network-devices-list">
                <p style="color: #718096; text-align: center;">No devices found</p>
            </div>
        </div>
        
        <div class="card">
            <h3>💬 Messaging</h3>
            <div class="message-container" id="messages-container">
                <p style="color: #718096; text-align: center;">No messages yet</p>
            </div>
            <input type="text" class="message-input" id="message-input" placeholder="Type your message...">
            <button class="btn" onclick="sendMessage()" style="width: 100%;">📤 Send Message</button>
        </div>
        
        <div class="card">
            <h3>📊 System Information</h3>
            <div class="status-grid">
                <div class="status-item">
                    <div class="status-value" id="cpu-usage">0%</div>
                    <div class="status-label">CPU Usage</div>
                </div>
                <div class="status-item">
                    <div class="status-value" id="memory-usage">0%</div>
                    <div class="status-label">Memory Usage</div>
                </div>
                <div class="status-item">
                    <div class="status-value" id="u3cp-cycles">0</div>
                    <div class="status-label">U3CP Cycles</div>
                </div>
                <div class="status-item">
                    <div class="status-value" id="ip-address">Loading...</div>
                    <div class="status-label">IP Address</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let startTime = Date.now();
        
        function updateUptime() {
            const now = Date.now();
            const diff = now - startTime;
            const hours = Math.floor(diff / 3600000);
            const minutes = Math.floor((diff % 3600000) / 60000);
            const seconds = Math.floor((diff % 60000) / 1000);
            document.getElementById('uptime').textContent = 
                `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }
        
        function startSystem() {
            fetch('/api/start')
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('U3CP system started successfully!');
                        refreshData();
                    } else {
                        alert('Error: ' + data.message);
                    }
                });
        }
        
        function stopSystem() {
            fetch('/api/stop')
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('U3CP system stopped successfully!');
                        refreshData();
                    } else {
                        alert('Error: ' + data.message);
                    }
                });
        }
        
        function scanNetwork() {
            fetch('/api/scan')
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        updateNetworkDevices(data.devices);
                    } else {
                        alert('Error: ' + data.message);
                    }
                });
        }
        
        function sendMessage() {
            const input = document.getElementById('message-input');
            const message = input.value.trim();
            
            if (message) {
                fetch('/api/send', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({message: message})
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
        
        function updateNetworkDevices(devices) {
            const container = document.getElementById('network-devices-list');
            document.getElementById('network-devices').textContent = devices.length;
            
            if (devices.length === 0) {
                container.innerHTML = '<p style="color: #718096; text-align: center;">No devices found</p>';
                return;
            }
            
            container.innerHTML = devices.map(device => `
                <div class="device-item">
                    <div>
                        <span class="online-indicator"></span>
                        <strong>${device.name}</strong>
                    </div>
                    <div>${device.ip}:${device.port}</div>
                </div>
            `).join('');
        }
        
        function loadMessages() {
            fetch('/api/messages')
                .then(response => response.json())
                .then(messages => {
                    const container = document.getElementById('messages-container');
                    document.getElementById('messages-count').textContent = messages.length;
                    
                    if (messages.length === 0) {
                        container.innerHTML = '<p style="color: #718096; text-align: center;">No messages yet</p>';
                        return;
                    }
                    
                    container.innerHTML = messages.map(msg => `
                        <div class="message">
                            <strong>${msg.sender}</strong> → ${msg.target}<br>
                            <span>${msg.content}</span><br>
                            <small>${new Date(msg.timestamp).toLocaleString()}</small>
                        </div>
                    `).join('');
                    
                    container.scrollTop = container.scrollHeight;
                });
        }
        
        function refreshData() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('device-status').textContent = data.status;
                    document.getElementById('cpu-usage').textContent = data.cpu_usage + '%';
                    document.getElementById('memory-usage').textContent = data.memory_usage + '%';
                    document.getElementById('u3cp-cycles').textContent = data.u3cp_cycles;
                    document.getElementById('ip-address').textContent = data.ip_address;
                });
            
            loadMessages();
        }
        
        // Enter key to send message
        document.getElementById('message-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Auto-refresh
        setInterval(updateUptime, 1000);
        setInterval(refreshData, 10000);
        
        // Initial load
        refreshData();
    </script>
</body>
</html>
'''

class U3CPDashboard:
    def __init__(self):
        self.start_time = time.time()
        self.messages = []
        self.network_devices = []
        self.system_status = "Online"
        
    def get_status(self):
        """Get current system status"""
        uptime = int(time.time() - self.start_time)
        hours = uptime // 3600
        minutes = (uptime % 3600) // 60
        
        return {
            'status': self.system_status,
            'uptime': f"{hours:02d}:{minutes:02d}:00",
            'cpu_usage': 25,  # Mock data
            'memory_usage': 45,  # Mock data
            'u3cp_cycles': len(self.messages) * 2,  # Mock data
            'ip_address': self.get_local_ip()
        }
    
    def get_local_ip(self):
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

# Initialize dashboard
dashboard = U3CPDashboard()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/status')
def api_status():
    """API endpoint for system status"""
    return jsonify(dashboard.get_status())

@app.route('/api/messages')
def api_messages():
    """API endpoint for messages"""
    return jsonify(dashboard.messages)

@app.route('/api/start')
def api_start():
    """API endpoint to start system"""
    dashboard.system_status = "Running"
    return jsonify({'status': 'success', 'message': 'System started'})

@app.route('/api/stop')
def api_stop():
    """API endpoint to stop system"""
    dashboard.system_status = "Stopped"
    return jsonify({'status': 'success', 'message': 'System stopped'})

@app.route('/api/scan')
def api_scan():
    """API endpoint to scan network"""
    # Mock network devices
    dashboard.network_devices = [
        {'name': 'Device 1', 'ip': '192.168.1.100', 'port': 8080},
        {'name': 'Device 2', 'ip': '192.168.1.101', 'port': 8080}
    ]
    return jsonify({'status': 'success', 'devices': dashboard.network_devices})

@app.route('/api/send', methods=['POST'])
def api_send():
    """API endpoint to send message"""
    data = request.json
    message = data.get('message', '')
    
    if message:
        dashboard.messages.append({
            'id': len(dashboard.messages) + 1,
            'content': message,
            'sender': 'Samsung Galaxy J3',
            'target': 'broadcast',
            'timestamp': datetime.now().isoformat(),
            'type': 'sent'
        })
    
    return jsonify({'status': 'success'})

def main():
    """Main function to start the dashboard"""
    print("🚀 Starting U3CP Simple Dashboard...")
    
    # Get local IP
    local_ip = dashboard.get_local_ip()
    print(f"📱 Dashboard available at: http://{local_ip}:5000")
    print(f"📱 Local access: http://localhost:5000")
    
    # Start Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    main() 
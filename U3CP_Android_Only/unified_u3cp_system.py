#!/usr/bin/env python3
"""
Unified U3CP System - 108-Sphere Lattice Integration
Integrates all SphereOS components into a single cohesive system
"""

import os
import sys
import time
import json
import sqlite3
import threading
import subprocess
from datetime import datetime
from flask import Flask, render_template_string, jsonify, request
import psutil
import platform

class UnifiedU3CPSystem:
    """Unified system integrating all SphereOS components with 108-Sphere Lattice"""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.system_name = "Unified U3CP System"
        self.version = "1.0.0"
        self.start_time = time.time()
        
        # 108-Sphere Lattice Core
        self.sphere_lattice = SphereLattice108()
        
        # Component Integration
        self.components = {
            'database': SphereOSDatabase(),
            'network': U3CPNetwork(),
            'messaging': NostrRelay(),
            'value_framework': ValueFramework(),
            'calendar': GPSCalendar(),
            'social': SocialSystem(),
            'transactions': TransactionAnalyzer()
        }
        
        # System Status
        self.status = {
            'running': True,
            'components_active': {},
            'last_update': datetime.now().isoformat(),
            'uptime': 0
        }
        
        self.setup_routes()
        self.initialize_components()
    
    def initialize_components(self):
        """Initialize all system components"""
        print(f"🚀 Initializing {self.system_name} v{self.version}")
        
        for name, component in self.components.items():
            try:
                component.initialize()
                self.status['components_active'][name] = True
                print(f"✅ {name}: Initialized")
            except Exception as e:
                self.status['components_active'][name] = False
                print(f"❌ {name}: Failed - {e}")
    
    def setup_routes(self):
        """Setup Flask routes for unified interface"""
        
        @self.app.route('/')
        def unified_dashboard():
            return render_template_string(UNIFIED_DASHBOARD_HTML, 
                                        system=self, 
                                        status=self.status,
                                        components=self.components)
        
        @self.app.route('/api/system-status')
        def api_system_status():
            return jsonify({
                'system': self.system_name,
                'version': self.version,
                'uptime': time.time() - self.start_time,
                'status': self.status,
                'components': {name: comp.get_status() for name, comp in self.components.items()},
                'sphere_lattice': self.sphere_lattice.get_status()
            })
        
        @self.app.route('/api/component/<component_name>')
        def api_component(component_name):
            if component_name in self.components:
                return jsonify(self.components[component_name].get_data())
            return jsonify({'error': 'Component not found'}), 404
        
        @self.app.route('/api/sphere/<position>')
        def api_sphere_data(position):
            try:
                pos = int(position)
                data = self.sphere_lattice.get_sphere_data(pos)
                return jsonify({'position': pos, 'data': data})
            except ValueError:
                return jsonify({'error': 'Invalid sphere position'}), 400
        
        @self.app.route('/api/install-component', methods=['POST'])
        def api_install_component():
            data = request.get_json()
            component_name = data.get('component')
            
            if component_name in self.components:
                try:
                    self.components[component_name].install()
                    return jsonify({'success': True, 'message': f'{component_name} installed'})
                except Exception as e:
                    return jsonify({'success': False, 'error': str(e)})
            
            return jsonify({'success': False, 'error': 'Component not found'})
    
    def run(self, host='0.0.0.0', port=5000):
        """Run the unified system"""
        print(f"🌐 Starting {self.system_name} on {host}:{port}")
        self.app.run(host=host, port=port, debug=False)

class SphereLattice108:
    """108-Sphere Lattice Core Architecture"""
    
    def __init__(self):
        self.spheres = {}
        self.relationships = {}
        self.anchors = [0, 9, 18, 27, 36, 45, 54, 63, 72, 81, 90, 99, 108]
        self.initialize_lattice()
    
    def initialize_lattice(self):
        """Initialize the 108-sphere lattice structure"""
        # Create all 108 spheres
        for i in range(1, 109):
            self.spheres[i] = {
                'id': i,
                'is_anchor': i in self.anchors,
                'data': None,
                'connections': [],
                'status': 'active'
            }
        
        # Define mathematical relationships
        self.relationships = {
            1: [18, -9, -8], 2: [-7, -6, 15], 3: [16, -7, -6],
            4: [-5, -4, 13], 5: [14, -5, -4], 6: [-3, -2, 11],
            7: [12, -3, -2], 8: [-1, 0, 9], 10: [1, 2, 7],
            # ... more relationships
        }
    
    def get_sphere_data(self, position):
        """Get data from specific sphere position"""
        if position in self.spheres:
            return self.spheres[position]
        return None
    
    def store_data(self, position, data):
        """Store data in sphere position"""
        if position in self.spheres:
            self.spheres[position]['data'] = data
            self.spheres[position]['last_updated'] = datetime.now().isoformat()
            return True
        return False
    
    def get_status(self):
        """Get lattice status"""
        active_spheres = sum(1 for s in self.spheres.values() if s['status'] == 'active')
        data_spheres = sum(1 for s in self.spheres.values() if s['data'] is not None)
        
        return {
            'total_spheres': 108,
            'active_spheres': active_spheres,
            'data_spheres': data_spheres,
            'anchors': len(self.anchors),
            'relationships': len(self.relationships)
        }

class SphereOSDatabase:
    """Unified database system"""
    
    def __init__(self):
        self.db_path = 'sphereos_unified.db'
        self.initialize_database()
    
    def initialize_database(self):
        """Initialize unified database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create unified tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                npub TEXT UNIQUE,
                name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                sender_npub TEXT,
                receiver_npub TEXT,
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                sphere_position INTEGER
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sphere_data (
                position INTEGER PRIMARY KEY,
                data_type TEXT,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_status(self):
        return {'status': 'active', 'database': self.db_path}
    
    def get_data(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM messages")
        message_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM sphere_data")
        sphere_data_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'users': user_count,
            'messages': message_count,
            'sphere_data': sphere_data_count
        }

class U3CPNetwork:
    """U3CP Network Communication"""
    
    def __init__(self):
        self.connected_devices = []
        self.network_status = 'initializing'
    
    def initialize(self):
        """Initialize U3CP network"""
        self.network_status = 'active'
        # Simulate device discovery
        self.connected_devices = [
            {'id': '52004cbceeee45d1', 'name': 'Samsung Galaxy J3', 'status': 'connected'}
        ]
    
    def get_status(self):
        return {'status': self.network_status, 'devices': len(self.connected_devices)}
    
    def get_data(self):
        return {
            'network_status': self.network_status,
            'connected_devices': self.connected_devices,
            'protocol': 'U3CP v1.0'
        }

class NostrRelay:
    """Nostr Relay Integration"""
    
    def __init__(self):
        self.relay_status = 'initializing'
        self.message_queue = []
    
    def initialize(self):
        """Initialize Nostr relay"""
        self.relay_status = 'active'
    
    def get_status(self):
        return {'status': self.relay_status, 'queue_size': len(self.message_queue)}
    
    def get_data(self):
        return {
            'relay_status': self.relay_status,
            'message_queue': len(self.message_queue),
            'protocol': 'Nostr'
        }

class ValueFramework:
    """Universal Value Framework"""
    
    def __init__(self):
        self.values = {}
        self.framework_status = 'initializing'
    
    def initialize(self):
        """Initialize value framework"""
        self.framework_status = 'active'
        self.values = {
            'trust': 0.8,
            'efficiency': 0.9,
            'security': 0.85,
            'privacy': 0.9
        }
    
    def get_status(self):
        return {'status': self.framework_status, 'values_tracked': len(self.values)}
    
    def get_data(self):
        return {
            'framework_status': self.framework_status,
            'values': self.values,
            'total_metrics': len(self.values)
        }

class GPSCalendar:
    """GPS Calendar Integration"""
    
    def __init__(self):
        self.calendar_status = 'initializing'
        self.events = []
    
    def initialize(self):
        """Initialize GPS calendar"""
        self.calendar_status = 'active'
        self.events = [
            {'title': 'U3CP System Launch', 'location': 'Current Device', 'time': datetime.now().isoformat()}
        ]
    
    def get_status(self):
        return {'status': self.calendar_status, 'events': len(self.events)}
    
    def get_data(self):
        return {
            'calendar_status': self.calendar_status,
            'events': self.events,
            'gps_enabled': True
        }

class SocialSystem:
    """Social System Integration"""
    
    def __init__(self):
        self.social_status = 'initializing'
        self.connections = []
    
    def initialize(self):
        """Initialize social system"""
        self.social_status = 'active'
        self.connections = [
            {'type': 'device', 'id': '52004cbceeee45d1', 'status': 'connected'}
        ]
    
    def get_status(self):
        return {'status': self.social_status, 'connections': len(self.connections)}
    
    def get_data(self):
        return {
            'social_status': self.social_status,
            'connections': self.connections,
            'network_type': 'U3CP Social'
        }

class TransactionAnalyzer:
    """Transaction Cost Analyzer"""
    
    def __init__(self):
        self.analyzer_status = 'initializing'
        self.transactions = []
    
    def initialize(self):
        """Initialize transaction analyzer"""
        self.analyzer_status = 'active'
        self.transactions = [
            {'type': 'system_startup', 'cost': 0.001, 'timestamp': datetime.now().isoformat()}
        ]
    
    def get_status(self):
        return {'status': self.analyzer_status, 'transactions': len(self.transactions)}
    
    def get_data(self):
        return {
            'analyzer_status': self.analyzer_status,
            'transactions': self.transactions,
            'total_cost': sum(t['cost'] for t in self.transactions)
        }

# Unified Dashboard HTML Template
UNIFIED_DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ system.system_name }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
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
            background: rgba(255,255,255,0.95); 
            padding: 30px; 
            border-radius: 20px; 
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }
        .header h1 { 
            font-size: 2.5em; 
            color: #4a5568; 
            margin-bottom: 10px;
        }
        .header p { 
            font-size: 1.2em; 
            color: #718096;
        }
        .grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px;
        }
        .card { 
            background: rgba(255,255,255,0.95); 
            padding: 25px; 
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease;
        }
        .card:hover { transform: translateY(-5px); }
        .card h3 { 
            color: #2d3748; 
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        .status-indicator { 
            display: inline-block; 
            width: 12px; 
            height: 12px; 
            border-radius: 50%; 
            margin-right: 8px;
        }
        .status-active { background: #48bb78; }
        .status-inactive { background: #f56565; }
        .sphere-lattice { 
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            color: white;
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 30px;
        }
        .sphere-lattice h2 { 
            font-size: 2em; 
            margin-bottom: 15px;
        }
        .sphere-grid { 
            display: grid; 
            grid-template-columns: repeat(12, 1fr); 
            gap: 5px; 
            margin: 20px 0;
        }
        .sphere { 
            width: 20px; 
            height: 20px; 
            background: rgba(255,255,255,0.3); 
            border-radius: 50%;
            transition: all 0.3s ease;
        }
        .sphere.active { background: rgba(255,255,255,0.8); }
        .sphere.anchor { background: #f6ad55; }
        .button { 
            background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
            color: white; 
            border: none; 
            padding: 12px 24px; 
            border-radius: 10px; 
            cursor: pointer; 
            font-size: 16px;
            margin: 5px;
            transition: transform 0.2s;
        }
        .button:hover { transform: translateY(-2px); }
        .progress-bar { 
            width: 100%; 
            height: 8px; 
            background: #e2e8f0; 
            border-radius: 4px; 
            overflow: hidden; 
            margin: 10px 0;
        }
        .progress-fill { 
            height: 100%; 
            background: linear-gradient(90deg, #48bb78, #38a169);
            transition: width 0.3s ease;
        }
        .stats { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
            gap: 15px; 
            margin-top: 20px;
        }
        .stat { 
            text-align: center; 
            padding: 15px; 
            background: rgba(255,255,255,0.1); 
            border-radius: 10px;
        }
        .stat-value { 
            font-size: 2em; 
            font-weight: bold; 
            color: white;
        }
        .stat-label { 
            font-size: 0.9em; 
            color: rgba(255,255,255,0.8);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 {{ system.system_name }}</h1>
            <p>Unified 108-Sphere Lattice System v{{ system.version }}</p>
            <div class="stats">
                <div class="stat">
                    <div class="stat-value" id="uptime">0</div>
                    <div class="stat-label">Uptime (s)</div>
                </div>
                <div class="stat">
                    <div class="stat-value" id="active-components">0</div>
                    <div class="stat-label">Active Components</div>
                </div>
                <div class="stat">
                    <div class="stat-value" id="sphere-data">0</div>
                    <div class="stat-label">Sphere Data</div>
                </div>
            </div>
        </div>

        <div class="sphere-lattice">
            <h2>🌐 108-Sphere Lattice</h2>
            <p>Mathematical foundation connecting all components</p>
            <div class="sphere-grid" id="sphere-grid">
                <!-- Spheres will be generated by JavaScript -->
            </div>
            <div class="progress-bar">
                <div class="progress-fill" id="lattice-progress" style="width: 0%"></div>
            </div>
        </div>

        <div class="grid">
            <div class="card">
                <h3><span class="status-indicator status-active"></span>Database System</h3>
                <p>Unified data storage with sphere addressing</p>
                <div id="database-stats">Loading...</div>
                <button class="button" onclick="installComponent('database')">Install</button>
            </div>

            <div class="card">
                <h3><span class="status-indicator status-active"></span>U3CP Network</h3>
                <p>Android-to-Android communication protocol</p>
                <div id="network-stats">Loading...</div>
                <button class="button" onclick="installComponent('network')">Install</button>
            </div>

            <div class="card">
                <h3><span class="status-indicator status-active"></span>Nostr Relay</h3>
                <p>Decentralized messaging infrastructure</p>
                <div id="nostr-stats">Loading...</div>
                <button class="button" onclick="installComponent('nostr')">Install</button>
            </div>

            <div class="card">
                <h3><span class="status-indicator status-active"></span>Value Framework</h3>
                <p>Universal value measurement system</p>
                <div id="value-stats">Loading...</div>
                <button class="button" onclick="installComponent('value')">Install</button>
            </div>

            <div class="card">
                <h3><span class="status-indicator status-active"></span>GPS Calendar</h3>
                <p>Location-aware scheduling system</p>
                <div id="calendar-stats">Loading...</div>
                <button class="button" onclick="installComponent('calendar')">Install</button>
            </div>

            <div class="card">
                <h3><span class="status-indicator status-active"></span>Social System</h3>
                <p>U3CP-based social networking</p>
                <div id="social-stats">Loading...</div>
                <button class="button" onclick="installComponent('social')">Install</button>
            </div>

            <div class="card">
                <h3><span class="status-indicator status-active"></span>Transaction Analyzer</h3>
                <p>Cost and efficiency analysis</p>
                <div id="transaction-stats">Loading...</div>
                <button class="button" onclick="installComponent('transactions')">Install</button>
            </div>
        </div>
    </div>

    <script>
        let startTime = Date.now();
        
        function updateStats() {
            // Update uptime
            const uptime = Math.floor((Date.now() - startTime) / 1000);
            document.getElementById('uptime').textContent = uptime;
            
            // Update system stats
            fetch('/api/system-status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('active-components').textContent = 
                        Object.values(data.components).filter(c => c.status === 'active').length;
                    
                    // Update component stats
                    updateComponentStats('database', data.components.database);
                    updateComponentStats('network', data.components.network);
                    updateComponentStats('nostr', data.components.nostr);
                    updateComponentStats('value', data.components.value);
                    updateComponentStats('calendar', data.components.calendar);
                    updateComponentStats('social', data.components.social);
                    updateComponentStats('transaction', data.components.transactions);
                    
                    // Update sphere data count
                    document.getElementById('sphere-data').textContent = 
                        data.sphere_lattice.data_spheres || 0;
                    
                    // Update lattice progress
                    const progress = (data.sphere_lattice.data_spheres / 108) * 100;
                    document.getElementById('lattice-progress').style.width = progress + '%';
                })
                .catch(error => console.error('Error updating stats:', error));
        }
        
        function updateComponentStats(component, data) {
            const element = document.getElementById(component + '-stats');
            if (element && data) {
                element.innerHTML = `
                    <p><strong>Status:</strong> ${data.status}</p>
                    <p><strong>Data:</strong> ${JSON.stringify(data.data || {})}</p>
                `;
            }
        }
        
        function installComponent(component) {
            fetch('/api/install-component', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({component: component})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(`${component} installed successfully!`);
                    updateStats();
                } else {
                    alert(`Failed to install ${component}: ${data.error}`);
                }
            })
            .catch(error => {
                alert(`Error installing ${component}: ${error}`);
            });
        }
        
        function generateSphereGrid() {
            const grid = document.getElementById('sphere-grid');
            for (let i = 1; i <= 108; i++) {
                const sphere = document.createElement('div');
                sphere.className = 'sphere';
                if (i % 9 === 0) sphere.classList.add('anchor');
                sphere.title = `Sphere ${i}`;
                grid.appendChild(sphere);
            }
        }
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            generateSphereGrid();
            updateStats();
            setInterval(updateStats, 5000); // Update every 5 seconds
        });
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    system = UnifiedU3CPSystem()
    system.run() 
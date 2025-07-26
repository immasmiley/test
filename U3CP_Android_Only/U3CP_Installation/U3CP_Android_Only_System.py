#!/usr/bin/env python3
"""
U3CP Android-Only System
Android-to-Android communication without LoRa hardware
Includes Nostr relay integration and SphereOS database
"""

import os
import sys
import json
import time
import threading
import asyncio
import hashlib
import sqlite3
import socket
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# Import SphereOS components
try:
    sys.path.append('..')
    from SphereOS_Android_Unified import (
        UnifiedSphereSystem, NostrRelay, NostrEvent, 
        ValueDiscoveryEngine, ValueArea
    )
    SPHEREOS_AVAILABLE = True
except ImportError:
    SPHEREOS_AVAILABLE = False
    print("⚠️ SphereOS not available, using simplified database")

# ============================================================================
# ANDROID-ONLY COMMUNICATION SYSTEM
# ============================================================================

@dataclass
class AndroidMessage:
    """Android-to-Android message structure"""
    message_id: str
    source_device: str
    destination_device: Optional[str]
    message_type: str  # 'nostr_event', 'sphereos_data', 'network_control', 'chat'
    payload: bytes
    timestamp: float
    priority: int  # 1-5, 5 being highest
    checksum: str

class AndroidCommunicationSystem:
    """Android-to-Android communication system (no LoRa hardware)"""
    
    def __init__(self, device_id: str, sphere_system=None):
        self.device_id = device_id
        self.sphere_system = sphere_system
        self.u3cp = U3CPAlgorithm()
        self.message_queue = []
        self.received_messages = []
        self.connected_devices = {}  # device_id -> last_seen
        self.running = False
        
        # Network discovery
        self.discovery_port = 8081
        self.communication_port = 8082
        self.discovery_socket = None
        self.communication_socket = None
        
        # Message history
        self.message_history = []
        
        print(f"📱 Android communication system initialized for device: {self.device_id}")
    
    def start_communication(self):
        """Start the Android communication system"""
        self.running = True
        print(f"📱 Android communication started for device: {self.device_id}")
        
        # Start network discovery
        threading.Thread(target=self._discovery_server, daemon=True).start()
        
        # Start communication server
        threading.Thread(target=self._communication_server, daemon=True).start()
        
        # Start message processing
        threading.Thread(target=self._message_processing_loop, daemon=True).start()
        
        # Start device discovery
        threading.Thread(target=self._device_discovery_loop, daemon=True).start()
    
    def stop_communication(self):
        """Stop the Android communication system"""
        self.running = False
        
        if self.discovery_socket:
            self.discovery_socket.close()
        if self.communication_socket:
            self.communication_socket.close()
        
        print(f"🛑 Android communication stopped for device: {self.device_id}")
    
    def _discovery_server(self):
        """Run network discovery server"""
        try:
            self.discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.discovery_socket.bind(('', self.discovery_port))
            
            print(f"🔍 Discovery server listening on port {self.discovery_port}")
            
            while self.running:
                try:
                    data, addr = self.discovery_socket.recvfrom(1024)
                    self._handle_discovery_message(data, addr)
                except Exception as e:
                    if self.running:
                        print(f"❌ Discovery error: {e}")
                        
        except Exception as e:
            print(f"❌ Failed to start discovery server: {e}")
    
    def _communication_server(self):
        """Run communication server"""
        try:
            self.communication_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.communication_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.communication_socket.bind(('', self.communication_port))
            self.communication_socket.listen(5)
            
            print(f"📡 Communication server listening on port {self.communication_port}")
            
            while self.running:
                try:
                    client_socket, addr = self.communication_socket.accept()
                    threading.Thread(target=self._handle_client_connection, 
                                  args=(client_socket, addr), daemon=True).start()
                except Exception as e:
                    if self.running:
                        print(f"❌ Communication error: {e}")
                        
        except Exception as e:
            print(f"❌ Failed to start communication server: {e}")
    
    def _handle_discovery_message(self, data: bytes, addr):
        """Handle discovery messages"""
        try:
            message = json.loads(data.decode('utf-8'))
            
            if message.get('type') == 'discovery_broadcast':
                device_id = message.get('device_id')
                if device_id != self.device_id:
                    self.connected_devices[device_id] = {
                        'address': addr[0],
                        'port': message.get('port', self.communication_port),
                        'last_seen': time.time()
                    }
                    print(f"📱 Discovered device: {device_id} at {addr[0]}")
                    
                    # Send response
                    response = {
                        'type': 'discovery_response',
                        'device_id': self.device_id,
                        'port': self.communication_port,
                        'timestamp': time.time()
                    }
                    self.discovery_socket.sendto(json.dumps(response).encode(), addr)
                    
        except Exception as e:
            print(f"❌ Discovery message handling failed: {e}")
    
    def _handle_client_connection(self, client_socket, addr):
        """Handle client connection"""
        try:
            print(f"📱 Client connected from {addr}")
            
            while self.running:
                data = client_socket.recv(4096)
                if not data:
                    break
                
                self._handle_received_message(data)
                
        except Exception as e:
            print(f"❌ Client connection error: {e}")
        finally:
            client_socket.close()
    
    def _handle_received_message(self, data: bytes):
        """Handle received message"""
        try:
            message_data = json.loads(data.decode('utf-8'))
            
            # Create AndroidMessage object
            message = AndroidMessage(
                message_id=message_data.get('message_id', ''),
                source_device=message_data.get('source_device', ''),
                destination_device=message_data.get('destination_device'),
                message_type=message_data.get('message_type', ''),
                payload=message_data.get('payload', '').encode(),
                timestamp=message_data.get('timestamp', time.time()),
                priority=message_data.get('priority', 1),
                checksum=message_data.get('checksum', '')
            )
            
            # Add to received messages
            self.received_messages.append(message)
            self.message_history.append({
                'direction': 'received',
                'message': message,
                'timestamp': time.time()
            })
            
            # Handle based on message type
            if message.message_type == "nostr_event":
                self._handle_nostr_event(message)
            elif message.message_type == "sphereos_data":
                self._handle_sphereos_data(message)
            elif message.message_type == "network_control":
                self._handle_network_control(message)
            elif message.message_type == "chat":
                self._handle_chat_message(message)
            
            print(f"📥 Received {message.message_type} from {message.source_device}")
            
        except Exception as e:
            print(f"❌ Message handling failed: {e}")
    
    def _handle_nostr_event(self, message: AndroidMessage):
        """Handle received Nostr event"""
        try:
            if self.sphere_system and self.sphere_system.nostr_relay:
                # Decode Nostr event
                event_data = json.loads(message.payload.decode('utf-8'))
                nostr_event = NostrEvent(**event_data)
                
                # Store in Nostr relay
                asyncio.run(self.sphere_system.nostr_relay._store_event(nostr_event))
                
                print(f"📥 Stored Nostr event: {nostr_event.id[:8]}...")
                
        except Exception as e:
            print(f"❌ Nostr event handling failed: {e}")
    
    def _handle_sphereos_data(self, message: AndroidMessage):
        """Handle received SphereOS data"""
        try:
            if self.sphere_system:
                # Decode SphereOS data
                data = json.loads(message.payload.decode('utf-8'))
                
                # Store in SphereOS database
                self.sphere_system.store_data_unified(
                    message.payload,
                    data.get('reference_type', 'content'),
                    data.get('reference_value', message.message_id)
                )
                
                print(f"📥 Stored SphereOS data: {message.message_id}")
                
        except Exception as e:
            print(f"❌ SphereOS data handling failed: {e}")
    
    def _handle_network_control(self, message: AndroidMessage):
        """Handle network control messages"""
        try:
            control_data = json.loads(message.payload.decode('utf-8'))
            command = control_data.get('command')
            
            if command == 'health_check':
                self._send_health_response(message.source_device)
            elif command == 'network_sync':
                self._sync_network_state(message.source_device)
            else:
                print(f"⚠️ Unknown network command: {command}")
                
        except Exception as e:
            print(f"❌ Network control handling failed: {e}")
    
    def _handle_chat_message(self, message: AndroidMessage):
        """Handle chat messages"""
        try:
            chat_data = json.loads(message.payload.decode('utf-8'))
            print(f"💬 Chat from {message.source_device}: {chat_data.get('message', '')}")
            
        except Exception as e:
            print(f"❌ Chat message handling failed: {e}")
    
    def _message_processing_loop(self):
        """Main message processing loop using U3CP timing"""
        while self.running:
            try:
                current_cycle = self.u3cp.get_current_cycle()
                
                if self.u3cp.is_transmission_cycle(current_cycle):
                    # Even cycles: Transmit messages
                    self._transmit_pending_messages()
                
                elif self.u3cp.is_processing_cycle(current_cycle):
                    # Odd cycles: Process received messages
                    self._process_received_messages()
                
                time.sleep(0.01)  # 10ms interval
                
            except Exception as e:
                print(f"❌ Message processing error: {e}")
                time.sleep(1)
    
    def _device_discovery_loop(self):
        """Periodic device discovery"""
        while self.running:
            try:
                # Broadcast discovery message
                discovery_message = {
                    'type': 'discovery_broadcast',
                    'device_id': self.device_id,
                    'port': self.communication_port,
                    'timestamp': time.time()
                }
                
                # Broadcast to local network
                self._broadcast_discovery(discovery_message)
                
                # Clean up stale devices
                current_time = time.time()
                stale_devices = [
                    device_id for device_id, info in self.connected_devices.items()
                    if current_time - info['last_seen'] > 300  # 5 minutes
                ]
                
                for device_id in stale_devices:
                    del self.connected_devices[device_id]
                    print(f"📱 Device left network: {device_id}")
                
                time.sleep(30)  # Discover every 30 seconds
                
            except Exception as e:
                print(f"❌ Device discovery error: {e}")
                time.sleep(60)
    
    def _broadcast_discovery(self, message: Dict):
        """Broadcast discovery message to local network"""
        try:
            # Get local network addresses
            local_addresses = self._get_local_addresses()
            
            for addr in local_addresses:
                try:
                    if self.discovery_socket:
                        self.discovery_socket.sendto(
                            json.dumps(message).encode(),
                            (addr, self.discovery_port)
                        )
                except Exception as e:
                    continue  # Skip failed addresses
                    
        except Exception as e:
            print(f"❌ Discovery broadcast failed: {e}")
    
    def _get_local_addresses(self) -> List[str]:
        """Get local network addresses"""
        addresses = []
        
        try:
            # Get local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            
            # Add local IP
            addresses.append(local_ip)
            
            # Add localhost
            addresses.append("127.0.0.1")
            
            # Add broadcast address
            if '.' in local_ip:
                parts = local_ip.split('.')
                broadcast_ip = f"{parts[0]}.{parts[1]}.{parts[2]}.255"
                addresses.append(broadcast_ip)
                
        except Exception as e:
            print(f"❌ Failed to get local addresses: {e}")
            addresses = ["127.0.0.1"]  # Fallback to localhost
        
        return addresses
    
    def _transmit_pending_messages(self):
        """Transmit pending messages from queue"""
        if not self.message_queue:
            return
        
        # Sort by priority (highest first)
        self.message_queue.sort(key=lambda x: x.priority, reverse=True)
        
        # Transmit highest priority message
        message = self.message_queue.pop(0)
        
        try:
            # Convert to JSON
            message_data = {
                'message_id': message.message_id,
                'source_device': message.source_device,
                'destination_device': message.destination_device,
                'message_type': message.message_type,
                'payload': message.payload.decode('utf-8'),
                'timestamp': message.timestamp,
                'priority': message.priority,
                'checksum': message.checksum
            }
            
            # Send to connected devices
            if message.destination_device:
                # Send to specific device
                self._send_to_device(message.destination_device, message_data)
            else:
                # Broadcast to all devices
                self._broadcast_message(message_data)
            
            # Store transmission log
            self._store_transmission_log(message)
            
            print(f"📤 Transmitted: {message.message_type} (Priority: {message.priority})")
            
        except Exception as e:
            print(f"❌ Transmission failed: {e}")
            # Re-queue message for retry
            self.message_queue.append(message)
    
    def _send_to_device(self, device_id: str, message_data: Dict):
        """Send message to specific device"""
        try:
            if device_id in self.connected_devices:
                device_info = self.connected_devices[device_id]
                
                # Create socket connection
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)
                s.connect((device_info['address'], device_info['port']))
                
                # Send message
                s.send(json.dumps(message_data).encode())
                s.close()
                
        except Exception as e:
            print(f"❌ Failed to send to device {device_id}: {e}")
    
    def _broadcast_message(self, message_data: Dict):
        """Broadcast message to all connected devices"""
        for device_id in list(self.connected_devices.keys()):
            self._send_to_device(device_id, message_data)
    
    def _process_received_messages(self):
        """Process received messages during processing cycles"""
        # Process any messages in received queue
        while self.received_messages:
            message = self.received_messages.pop(0)
            # Messages are already handled in _handle_received_message
            pass
    
    def transmit_nostr_event(self, nostr_event, priority: int = 3):
        """Transmit Nostr event via Android network"""
        try:
            # Create Android message
            message = AndroidMessage(
                message_id=hashlib.sha256(f"{nostr_event.id}_{time.time()}".encode()).hexdigest()[:16],
                source_device=self.device_id,
                destination_device=None,  # Broadcast
                message_type="nostr_event",
                payload=json.dumps(asdict(nostr_event)).encode('utf-8'),
                timestamp=time.time(),
                priority=priority,
                checksum=hashlib.sha256(json.dumps(asdict(nostr_event)).encode()).hexdigest()[:8]
            )
            
            # Add to transmission queue
            self.message_queue.append(message)
            
            print(f"📤 Queued Nostr event for transmission: {nostr_event.id[:8]}...")
            
        except Exception as e:
            print(f"❌ Failed to queue Nostr event: {e}")
    
    def transmit_sphereos_data(self, data: bytes, reference_type: str, reference_value: str, priority: int = 2):
        """Transmit SphereOS data via Android network"""
        try:
            # Create Android message
            message = AndroidMessage(
                message_id=hashlib.sha256(f"{reference_value}_{time.time()}".encode()).hexdigest()[:16],
                source_device=self.device_id,
                destination_device=None,  # Broadcast
                message_type="sphereos_data",
                payload=json.dumps({
                    'reference_type': reference_type,
                    'reference_value': reference_value,
                    'data': data.hex()  # Convert to hex for JSON
                }).encode('utf-8'),
                timestamp=time.time(),
                priority=priority,
                checksum=hashlib.sha256(data).hexdigest()[:8]
            )
            
            # Add to transmission queue
            self.message_queue.append(message)
            
            print(f"📤 Queued SphereOS data for transmission: {reference_value}")
            
        except Exception as e:
            print(f"❌ Failed to queue SphereOS data: {e}")
    
    def send_chat_message(self, message_text: str, destination_device: str = None, priority: int = 1):
        """Send chat message"""
        try:
            chat_data = {
                'message': message_text,
                'timestamp': time.time(),
                'device_id': self.device_id
            }
            
            message = AndroidMessage(
                message_id=hashlib.sha256(f"chat_{time.time()}".encode()).hexdigest()[:16],
                source_device=self.device_id,
                destination_device=destination_device,
                message_type="chat",
                payload=json.dumps(chat_data).encode('utf-8'),
                timestamp=time.time(),
                priority=priority,
                checksum=hashlib.sha256(message_text.encode()).hexdigest()[:8]
            )
            
            self.message_queue.append(message)
            print(f"📤 Queued chat message: {message_text[:50]}...")
            
        except Exception as e:
            print(f"❌ Failed to queue chat message: {e}")
    
    def _send_health_response(self, target_device: str):
        """Send health response"""
        try:
            health_data = {
                'device_id': self.device_id,
                'status': 'healthy',
                'timestamp': time.time(),
                'queue_size': len(self.message_queue),
                'received_count': len(self.received_messages),
                'connected_devices': len(self.connected_devices)
            }
            
            message = AndroidMessage(
                message_id=hashlib.sha256(f"health_{time.time()}".encode()).hexdigest()[:16],
                source_device=self.device_id,
                destination_device=target_device,
                message_type="network_control",
                payload=json.dumps({
                    'command': 'health_response',
                    'data': health_data
                }).encode('utf-8'),
                timestamp=time.time(),
                priority=1,
                checksum=hashlib.sha256(json.dumps(health_data).encode()).hexdigest()[:8]
            )
            
            self.message_queue.append(message)
            
        except Exception as e:
            print(f"❌ Failed to send health response: {e}")
    
    def _sync_network_state(self, target_device: str):
        """Sync network state"""
        try:
            if self.sphere_system:
                health = self.sphere_system.get_system_health()
                relay_info = self.sphere_system.nostr_relay.get_relay_info()
            else:
                health = {'status': 'no_sphereos'}
                relay_info = {'name': 'no_relay'}
            
            sync_data = {
                'device_id': self.device_id,
                'sphereos_health': health,
                'nostr_relay': relay_info,
                'connected_devices': list(self.connected_devices.keys()),
                'timestamp': time.time()
            }
            
            message = AndroidMessage(
                message_id=hashlib.sha256(f"sync_{time.time()}".encode()).hexdigest()[:16],
                source_device=self.device_id,
                destination_device=target_device,
                message_type="network_control",
                payload=json.dumps({
                    'command': 'network_sync_response',
                    'data': sync_data
                }).encode('utf-8'),
                timestamp=time.time(),
                priority=2,
                checksum=hashlib.sha256(json.dumps(sync_data).encode()).hexdigest()[:8]
            )
            
            self.message_queue.append(message)
            
        except Exception as e:
            print(f"❌ Failed to sync network state: {e}")
    
    def _store_transmission_log(self, message: AndroidMessage):
        """Store transmission log"""
        try:
            if self.sphere_system:
                log_data = {
                    'message_id': message.message_id,
                    'source_device': message.source_device,
                    'message_type': message.message_type,
                    'timestamp': message.timestamp,
                    'priority': message.priority,
                    'status': 'transmitted'
                }
                
                self.sphere_system.store_data_unified(
                    json.dumps(log_data).encode('utf-8'),
                    "atlas",
                    f"/android/transmissions/{message.message_id}"
                )
                
        except Exception as e:
            print(f"❌ Failed to store transmission log: {e}")
    
    def get_network_status(self) -> Dict:
        """Get network status"""
        return {
            'device_id': self.device_id,
            'running': self.running,
            'connected_devices': len(self.connected_devices),
            'message_queue_size': len(self.message_queue),
            'received_messages': len(self.received_messages),
            'message_history': len(self.message_history),
            'current_cycle': self.u3cp.get_current_cycle(),
            'timestamp': time.time()
        }

# ============================================================================
# U3CP ALGORITHM (SAME AS BEFORE)
# ============================================================================

class U3CPAlgorithm:
    """8-cycle mathematical processing pattern for unified signal processing"""
    
    def __init__(self):
        # Core 8-cycle coefficient pattern
        self.coefficients = [
            [16.67, -8.33, -7.41],   # Cycle 0: Zone A transmits
            [-6.48, -5.56, 13.89],   # Cycle 1: Audio processing  
            [14.81, -6.48, -5.56],   # Cycle 2: Zone A transmits
            [-4.63, -3.70, 12.04],   # Cycle 3: Video processing
            [12.96, -4.63, -3.70],   # Cycle 4: Zone A transmits
            [-2.78, -1.85, 10.19],   # Cycle 5: Audio processing
            [11.11, -2.78, -1.85],   # Cycle 6: Zone A transmits
            [-0.93, 0.00, 8.33]      # Cycle 7: Video processing
        ]
        
        self.current_cycle = 0
        self.cycle_duration = 0.125  # 125ms per cycle
        self.last_cycle_time = time.time()
        
    def get_current_cycle(self) -> int:
        """Get current cycle based on time"""
        elapsed = time.time() - self.last_cycle_time
        cycle = int((elapsed / self.cycle_duration) % 8)
        return cycle
    
    def get_cycle_coefficients(self, cycle: int) -> List[float]:
        """Get coefficients for specific cycle"""
        return self.coefficients[cycle % 8]
    
    def is_transmission_cycle(self, cycle: int) -> bool:
        """Check if cycle is for transmission (even cycles)"""
        return cycle % 2 == 0
    
    def is_processing_cycle(self, cycle: int) -> bool:
        """Check if cycle is for processing (odd cycles)"""
        return cycle % 2 == 1

# ============================================================================
# INTEGRATED ANDROID-ONLY SYSTEM
# ============================================================================

class U3CPAndroidOnlySystem:
    """Complete integrated system: U3CP + SphereOS + Nostr + Android Communication"""
    
    def __init__(self, device_id: str, db_path: str = "sphereos_android_only.db"):
        self.device_id = device_id
        
        # Initialize core systems
        if SPHEREOS_AVAILABLE:
            self.sphere_system = UnifiedSphereSystem(db_path)
        else:
            self.sphere_system = None
            print("⚠️ Using simplified database (SphereOS not available)")
        
        self.android_comm = AndroidCommunicationSystem(device_id, self.sphere_system)
        self.u3cp = U3CPAlgorithm()
        
        # Integration status
        self.integration_active = False
        
        print(f"📱 U3CP Android-Only system initialized for device: {device_id}")
    
    def start_integrated_system(self):
        """Start the complete integrated system"""
        try:
            # Start Android communication
            self.android_comm.start_communication()
            
            # Start Nostr relay if available
            if self.sphere_system and self.sphere_system.nostr_relay:
                self._start_nostr_relay_async()
            
            # Start integration loop
            self.integration_active = True
            threading.Thread(target=self._integration_loop, daemon=True).start()
            
            print(f"🚀 Android-only system started for device: {self.device_id}")
            
        except Exception as e:
            print(f"❌ Failed to start integrated system: {e}")
    
    def stop_integrated_system(self):
        """Stop the complete integrated system"""
        try:
            self.integration_active = False
            self.android_comm.stop_communication()
            
            if self.sphere_system and self.sphere_system.nostr_relay:
                self.sphere_system.nostr_relay.stop_relay()
            
            print(f"🛑 Android-only system stopped for device: {self.device_id}")
            
        except Exception as e:
            print(f"❌ Failed to stop integrated system: {e}")
    
    def _start_nostr_relay_async(self):
        """Start Nostr relay asynchronously"""
        def start_relay():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.sphere_system.nostr_relay.start_relay())
            except Exception as e:
                print(f"❌ Nostr relay start failed: {e}")
        
        threading.Thread(target=start_relay, daemon=True).start()
    
    def _integration_loop(self):
        """Main integration loop"""
        while self.integration_active:
            try:
                current_cycle = self.u3cp.get_current_cycle()
                
                if self.u3cp.is_transmission_cycle(current_cycle):
                    # Even cycles: Transmit data
                    self._transmit_integrated_data()
                
                elif self.u3cp.is_processing_cycle(current_cycle):
                    # Odd cycles: Process data and value discovery
                    self._process_integrated_data()
                
                time.sleep(0.01)  # 10ms interval
                
            except Exception as e:
                print(f"❌ Integration loop error: {e}")
                time.sleep(1)  # Wait before retry
    
    def _transmit_integrated_data(self):
        """Transmit integrated data during transmission cycles"""
        try:
            # Transmit Nostr events via Android network
            self._transmit_nostr_events()
            
            # Transmit SphereOS value opportunities
            self._transmit_value_opportunities()
            
            # Transmit network health data
            self._transmit_network_health()
            
        except Exception as e:
            print(f"❌ Transmission error: {e}")
    
    def _process_integrated_data(self):
        """Process integrated data during processing cycles"""
        try:
            # Run value discovery if SphereOS available
            if self.sphere_system:
                self._run_value_discovery()
            
            # Process network synchronization
            self._process_network_sync()
            
            # Update network state
            self._update_network_state()
            
        except Exception as e:
            print(f"❌ Processing error: {e}")
    
    def _transmit_nostr_events(self):
        """Transmit Nostr events via Android network"""
        try:
            if self.sphere_system and self.sphere_system.nostr_relay:
                # Get recent Nostr events from relay
                events = list(self.sphere_system.nostr_relay.events.values())
                
                # Transmit recent events (last 10)
                for event in events[-10:]:
                    self.android_comm.transmit_nostr_event(event, priority=3)
                    
        except Exception as e:
            print(f"❌ Nostr event transmission failed: {e}")
    
    def _transmit_value_opportunities(self):
        """Transmit value opportunities via Android network"""
        try:
            if self.sphere_system:
                # Get value opportunities from SphereOS
                opportunities = self.sphere_system.scan_value_opportunities()
                
                if opportunities.get('opportunities'):
                    # Transmit opportunities as SphereOS data
                    self.android_comm.transmit_sphereos_data(
                        json.dumps(opportunities).encode('utf-8'),
                        "atlas",
                        f"/value_opportunities/{int(time.time())}",
                        priority=4
                    )
                    
        except Exception as e:
            print(f"❌ Value opportunity transmission failed: {e}")
    
    def _transmit_network_health(self):
        """Transmit network health data"""
        try:
            # Get system health
            if self.sphere_system:
                health = self.sphere_system.get_system_health()
            else:
                health = {'status': 'no_sphereos'}
            
            # Transmit health data
            self.android_comm.transmit_sphereos_data(
                json.dumps(health).encode('utf-8'),
                "atlas",
                f"/network_health/{self.device_id}/{int(time.time())}",
                priority=1
            )
            
        except Exception as e:
            print(f"❌ Network health transmission failed: {e}")
    
    def _run_value_discovery(self):
        """Run value discovery during processing cycles"""
        try:
            if self.sphere_system:
                # Scan for value opportunities
                opportunities = self.sphere_system.scan_value_opportunities()
                
                # Create Nostr events for significant opportunities
                for opp in opportunities.get('opportunities', []):
                    if opp.get('value_potential', 0) > 10000:  # High-value opportunities
                        self._create_opportunity_nostr_event(opp)
                        
        except Exception as e:
            print(f"❌ Value discovery failed: {e}")
    
    def _create_opportunity_nostr_event(self, opportunity: Dict):
        """Create Nostr event for value opportunity"""
        try:
            if self.sphere_system and self.sphere_system.nostr_relay:
                # Create Nostr event
                event = NostrEvent(
                    id=hashlib.sha256(f"opportunity_{opportunity['opportunity_id']}".encode()).hexdigest(),
                    pubkey=self.device_id,
                    created_at=int(time.time()),
                    kind=30000,  # Custom kind for value opportunities
                    tags=[
                        ["opportunity_id", opportunity['opportunity_id']],
                        ["area", opportunity['area']],
                        ["value_potential", str(opportunity['value_potential'])],
                        ["confidence_score", str(opportunity['confidence_score'])]
                    ],
                    content=json.dumps(opportunity),
                    sig="placeholder_signature"  # In real implementation, add proper signature
                )
                
                # Store in Nostr relay
                asyncio.run(self.sphere_system.nostr_relay._store_event(event))
                
                print(f"💡 Created Nostr event for opportunity: {opportunity['opportunity_id']}")
                
        except Exception as e:
            print(f"❌ Failed to create opportunity Nostr event: {e}")
    
    def _process_network_sync(self):
        """Process network synchronization"""
        try:
            # Send periodic sync requests
            if int(time.time()) % 60 == 0:  # Every minute
                sync_message = AndroidMessage(
                    message_id=hashlib.sha256(f"sync_request_{time.time()}".encode()).hexdigest()[:16],
                    source_device=self.device_id,
                    destination_device=None,
                    message_type="network_control",
                    payload=json.dumps({
                        'command': 'network_sync',
                        'timestamp': time.time()
                    }).encode('utf-8'),
                    timestamp=time.time(),
                    priority=2,
                    checksum=hashlib.sha256(f"sync_request_{time.time()}".encode()).hexdigest()[:8]
                )
                
                self.android_comm.message_queue.append(sync_message)
                
        except Exception as e:
            print(f"❌ Network sync processing failed: {e}")
    
    def _update_network_state(self):
        """Update network state"""
        try:
            # Update device tracking
            current_time = time.time()
            
            # Remove stale devices (not seen in 5 minutes)
            stale_devices = [
                device_id for device_id, info in self.android_comm.connected_devices.items()
                if current_time - info['last_seen'] > 300
            ]
            
            for device_id in stale_devices:
                del self.android_comm.connected_devices[device_id]
                print(f"📱 Device left network: {device_id}")
            
        except Exception as e:
            print(f"❌ Network state update failed: {e}")
    
    def send_chat_message(self, message_text: str, destination_device: str = None):
        """Send chat message"""
        self.android_comm.send_chat_message(message_text, destination_device)
    
    def get_system_status(self) -> Dict:
        """Get complete system status"""
        try:
            status = {
                'device_id': self.device_id,
                'integration_active': self.integration_active,
                'current_cycle': self.u3cp.get_current_cycle(),
                'android_network': self.android_comm.get_network_status(),
                'timestamp': time.time()
            }
            
            if self.sphere_system:
                status['sphereos_health'] = self.sphere_system.get_system_health()
                if self.sphere_system.nostr_relay:
                    status['nostr_relay'] = self.sphere_system.nostr_relay.get_relay_info()
            
            return status
            
        except Exception as e:
            return {'error': str(e)}

# ============================================================================
# USAGE EXAMPLE
# ============================================================================

def main():
    """Example usage of the Android-only system"""
    print("📱 U3CP Android-Only System Example")
    print("=" * 50)
    
    # Create integrated system
    device_id = f"android_{hashlib.sha256(str(time.time()).encode()).hexdigest()[:8]}"
    system = U3CPAndroidOnlySystem(device_id)
    
    # Start the system
    system.start_integrated_system()
    
    try:
        # Run for 60 seconds
        print("🚀 System running for 60 seconds...")
        time.sleep(60)
        
    except KeyboardInterrupt:
        print("\n⏹️ Stopping system...")
    
    finally:
        # Stop the system
        system.stop_integrated_system()
        
        # Show final status
        status = system.get_system_status()
        print("\n📊 Final System Status:")
        print(json.dumps(status, indent=2))

if __name__ == "__main__":
    main() 
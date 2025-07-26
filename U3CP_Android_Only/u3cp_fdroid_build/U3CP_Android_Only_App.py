#!/usr/bin/env python3
"""
U3CP Android-Only App
Mobile application for Android-to-Android communication
Includes Nostr relay and SphereOS integration
"""

import os
import sys
import json
import time
import threading
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any

# Kivy imports for Android UI
try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.gridlayout import GridLayout
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.uix.textinput import TextInput
    from kivy.uix.scrollview import ScrollView
    from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
    from kivy.uix.progressbar import ProgressBar
    from kivy.uix.switch import Switch
    from kivy.clock import Clock
    from kivy.core.window import Window
    from kivy.metrics import dp
    from kivy.utils import platform
    
    KIVY_AVAILABLE = True
except ImportError:
    KIVY_AVAILABLE = False
    print("⚠️ Kivy not available, running in console mode")

# Import our Android-only system
try:
    from U3CP_Android_Only_System import U3CPAndroidOnlySystem
    U3CP_AVAILABLE = True
except ImportError:
    U3CP_AVAILABLE = False
    print("⚠️ U3CP Android-only system not available")

# ============================================================================
# ANDROID-ONLY APP MAIN CLASS
# ============================================================================

class U3CPAndroidOnlyApp(App):
    """Main Android application for U3CP Android-Only System"""
    
    def __init__(self):
        super().__init__()
        self.title = "U3CP Android-Only System"
        self.system = None
        self.device_id = self._generate_device_id()
        self.app_running = False
        
        # UI state
        self.status_text = ""
        self.network_devices = []
        self.message_log = []
        self.value_opportunities = []
        self.chat_messages = []
        
        print(f"📱 U3CP Android-Only App initialized for device: {self.device_id}")
    
    def _generate_device_id(self) -> str:
        """Generate unique device ID"""
        import hashlib
        import uuid
        
        # Use Android device ID if available
        if platform == 'android':
            try:
                from jnius import autoclass
                Context = autoclass('android.content.Context')
                TelephonyManager = autoclass('android.telephony.TelephonyManager')
                context = autoclass('org.kivy.android.PythonActivity').mActivity
                telephony = context.getSystemService(Context.TELEPHONY_SERVICE)
                device_id = telephony.getDeviceId()
                if device_id:
                    return f"android_{device_id[-8:]}"
            except:
                pass
        
        # Fallback to UUID
        return f"android_{uuid.uuid4().hex[:8]}"
    
    def build(self):
        """Build the Android UI"""
        if not KIVY_AVAILABLE:
            return self._build_console_ui()
        
        # Set window size for Android
        if platform == 'android':
            Window.softinput_mode = 'below_target'
        
        # Create main layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Create tabbed interface
        tabs = TabbedPanel(do_default_tab=False)
        
        # Main Control Tab
        main_tab = TabbedPanelItem(text='Main Control')
        main_tab.add_widget(self._build_main_control_ui())
        tabs.add_widget(main_tab)
        
        # Network Tab
        network_tab = TabbedPanelItem(text='Network')
        network_tab.add_widget(self._build_network_ui())
        tabs.add_widget(network_tab)
        
        # Chat Tab
        chat_tab = TabbedPanelItem(text='Chat')
        chat_tab.add_widget(self._build_chat_ui())
        tabs.add_widget(chat_tab)
        
        # Messages Tab
        messages_tab = TabbedPanelItem(text='Messages')
        messages_tab.add_widget(self._build_messages_ui())
        tabs.add_widget(messages_tab)
        
        # Value Discovery Tab
        value_tab = TabbedPanelItem(text='Value Discovery')
        value_tab.add_widget(self._build_value_ui())
        tabs.add_widget(value_tab)
        
        # Settings Tab
        settings_tab = TabbedPanelItem(text='Settings')
        settings_tab.add_widget(self._build_settings_ui())
        tabs.add_widget(settings_tab)
        
        main_layout.add_widget(tabs)
        
        return main_layout
    
    def _build_main_control_ui(self):
        """Build main control interface"""
        layout = BoxLayout(orientation='vertical', spacing=dp(10))
        
        # Status section
        status_layout = BoxLayout(orientation='vertical', size_hint_y=0.3)
        status_layout.add_widget(Label(text='System Status', size_hint_y=0.2))
        
        self.status_label = Label(
            text='System: Stopped\nDevice ID: ' + self.device_id,
            size_hint_y=0.8,
            text_size=(Window.width - dp(20), None),
            halign='left',
            valign='top'
        )
        status_layout.add_widget(self.status_label)
        layout.add_widget(status_layout)
        
        # Control buttons
        control_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=0.4)
        
        self.start_button = Button(
            text='Start System',
            background_color=(0.2, 0.8, 0.2, 1),
            on_press=self.start_system
        )
        control_layout.add_widget(self.start_button)
        
        self.stop_button = Button(
            text='Stop System',
            background_color=(0.8, 0.2, 0.2, 1),
            on_press=self.stop_system,
            disabled=True
        )
        control_layout.add_widget(self.stop_button)
        
        self.test_button = Button(
            text='Test Network',
            background_color=(0.2, 0.2, 0.8, 1),
            on_press=self.test_network
        )
        control_layout.add_widget(self.test_button)
        
        self.health_button = Button(
            text='System Health',
            background_color=(0.8, 0.8, 0.2, 1),
            on_press=self.show_health
        )
        control_layout.add_widget(self.health_button)
        
        layout.add_widget(control_layout)
        
        # Current cycle display
        cycle_layout = BoxLayout(orientation='vertical', size_hint_y=0.3)
        cycle_layout.add_widget(Label(text='U3CP Cycle Status', size_hint_y=0.3))
        
        self.cycle_label = Label(
            text='Current Cycle: 0\nMode: Stopped',
            size_hint_y=0.7
        )
        cycle_layout.add_widget(self.cycle_label)
        layout.add_widget(cycle_layout)
        
        return layout
    
    def _build_network_ui(self):
        """Build network interface"""
        layout = BoxLayout(orientation='vertical', spacing=dp(10))
        
        # Network status
        network_status_layout = BoxLayout(orientation='vertical', size_hint_y=0.3)
        network_status_layout.add_widget(Label(text='Network Status', size_hint_y=0.2))
        
        self.network_status_label = Label(
            text='Network: Disconnected\nDevices: 0\nRange: Local Network',
            size_hint_y=0.8
        )
        network_status_layout.add_widget(self.network_status_label)
        layout.add_widget(network_status_layout)
        
        # Network controls
        network_controls = GridLayout(cols=2, spacing=dp(10), size_hint_y=0.3)
        
        self.scan_button = Button(
            text='Scan Network',
            on_press=self.scan_network
        )
        network_controls.add_widget(self.scan_button)
        
        self.broadcast_button = Button(
            text='Broadcast Message',
            on_press=self.broadcast_message
        )
        network_controls.add_widget(self.broadcast_button)
        
        layout.add_widget(network_controls)
        
        # Device list
        devices_layout = BoxLayout(orientation='vertical', size_hint_y=0.4)
        devices_layout.add_widget(Label(text='Connected Devices', size_hint_y=0.2))
        
        self.devices_label = Label(
            text='No devices connected',
            size_hint_y=0.8
        )
        devices_layout.add_widget(self.devices_label)
        layout.add_widget(devices_layout)
        
        return layout
    
    def _build_chat_ui(self):
        """Build chat interface"""
        layout = BoxLayout(orientation='vertical', spacing=dp(10))
        
        # Chat input
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2)
        input_layout.add_widget(Label(text='Message:', size_hint_x=0.2))
        
        self.chat_input = TextInput(
            multiline=False,
            size_hint_x=0.6
        )
        input_layout.add_widget(self.chat_input)
        
        self.send_chat_button = Button(
            text='Send',
            size_hint_x=0.2,
            on_press=self.send_chat_message
        )
        input_layout.add_widget(self.send_chat_button)
        
        layout.add_widget(input_layout)
        
        # Chat log
        chat_log_layout = BoxLayout(orientation='vertical', size_hint_y=0.8)
        chat_log_layout.add_widget(Label(text='Chat Messages', size_hint_y=0.1))
        
        self.chat_log_label = Label(
            text='No messages',
            size_hint_y=0.9,
            text_size=(Window.width - dp(20), None),
            halign='left',
            valign='top'
        )
        chat_log_layout.add_widget(self.chat_log_label)
        layout.add_widget(chat_log_layout)
        
        return layout
    
    def _build_messages_ui(self):
        """Build messages interface"""
        layout = BoxLayout(orientation='vertical', spacing=dp(10))
        
        # Message input
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2)
        input_layout.add_widget(Label(text='Message:', size_hint_x=0.2))
        
        self.message_input = TextInput(
            multiline=False,
            size_hint_x=0.6
        )
        input_layout.add_widget(self.message_input)
        
        self.send_button = Button(
            text='Send',
            size_hint_x=0.2,
            on_press=self.send_message
        )
        input_layout.add_widget(self.send_button)
        
        layout.add_widget(input_layout)
        
        # Message log
        log_layout = BoxLayout(orientation='vertical', size_hint_y=0.8)
        log_layout.add_widget(Label(text='System Messages', size_hint_y=0.1))
        
        self.message_log_label = Label(
            text='No messages',
            size_hint_y=0.9,
            text_size=(Window.width - dp(20), None),
            halign='left',
            valign='top'
        )
        log_layout.add_widget(self.message_log_label)
        layout.add_widget(log_layout)
        
        return layout
    
    def _build_value_ui(self):
        """Build value discovery interface"""
        layout = BoxLayout(orientation='vertical', spacing=dp(10))
        
        # Value discovery controls
        controls_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2)
        
        self.scan_values_button = Button(
            text='Scan Values',
            on_press=self.scan_values
        )
        controls_layout.add_widget(self.scan_values_button)
        
        self.share_opportunities_button = Button(
            text='Share Opportunities',
            on_press=self.share_opportunities
        )
        controls_layout.add_widget(self.share_opportunities_button)
        
        layout.add_widget(controls_layout)
        
        # Value opportunities display
        opportunities_layout = BoxLayout(orientation='vertical', size_hint_y=0.8)
        opportunities_layout.add_widget(Label(text='Value Opportunities', size_hint_y=0.1))
        
        self.opportunities_label = Label(
            text='No opportunities found',
            size_hint_y=0.9,
            text_size=(Window.width - dp(20), None),
            halign='left',
            valign='top'
        )
        opportunities_layout.add_widget(self.opportunities_label)
        layout.add_widget(opportunities_layout)
        
        return layout
    
    def _build_settings_ui(self):
        """Build settings interface"""
        layout = BoxLayout(orientation='vertical', spacing=dp(10))
        
        # Device settings
        device_layout = BoxLayout(orientation='vertical', size_hint_y=0.4)
        device_layout.add_widget(Label(text='Device Settings', size_hint_y=0.2))
        
        device_id_layout = BoxLayout(orientation='horizontal', size_hint_y=0.4)
        device_id_layout.add_widget(Label(text='Device ID:', size_hint_x=0.3))
        self.device_id_input = TextInput(
            text=self.device_id,
            multiline=False,
            size_hint_x=0.7
        )
        device_id_layout.add_widget(self.device_id_input)
        device_layout.add_widget(device_id_layout)
        
        # Network settings
        network_layout = BoxLayout(orientation='vertical', size_hint_y=0.6)
        network_layout.add_widget(Label(text='Network Settings', size_hint_y=0.2))
        
        discovery_port_layout = BoxLayout(orientation='horizontal', size_hint_y=0.4)
        discovery_port_layout.add_widget(Label(text='Discovery Port:', size_hint_x=0.3))
        self.discovery_port_input = TextInput(
            text='8081',
            multiline=False,
            size_hint_x=0.7
        )
        discovery_port_layout.add_widget(self.discovery_port_input)
        network_layout.add_widget(discovery_port_layout)
        
        comm_port_layout = BoxLayout(orientation='horizontal', size_hint_y=0.4)
        comm_port_layout.add_widget(Label(text='Comm Port:', size_hint_x=0.3))
        self.comm_port_input = TextInput(
            text='8082',
            multiline=False,
            size_hint_x=0.7
        )
        comm_port_layout.add_widget(self.comm_port_input)
        network_layout.add_widget(comm_port_layout)
        
        layout.add_widget(device_layout)
        layout.add_widget(network_layout)
        
        # Save button
        save_button = Button(
            text='Save Settings',
            on_press=self.save_settings
        )
        layout.add_widget(save_button)
        
        return layout
    
    def _build_console_ui(self):
        """Build console UI for non-Kivy environments"""
        return Label(text='Console mode - use command line interface')
    
    # ============================================================================
    # SYSTEM CONTROL METHODS
    # ============================================================================
    
    def start_system(self, instance=None):
        """Start the U3CP Android-only system"""
        try:
            if not U3CP_AVAILABLE:
                self._update_status("❌ U3CP Android-only system not available")
                return
            
            # Initialize system
            self.system = U3CPAndroidOnlySystem(self.device_id)
            self.system.start_integrated_system()
            
            # Update UI
            self.app_running = True
            self.start_button.disabled = True
            self.stop_button.disabled = False
            
            self._update_status("✅ Android-only system started successfully")
            
            # Start UI update loop
            Clock.schedule_interval(self._update_ui, 1.0)
            
        except Exception as e:
            self._update_status(f"❌ Failed to start system: {e}")
    
    def stop_system(self, instance=None):
        """Stop the U3CP Android-only system"""
        try:
            if self.system:
                self.system.stop_integrated_system()
                self.system = None
            
            # Update UI
            self.app_running = False
            self.start_button.disabled = False
            self.stop_button.disabled = True
            
            self._update_status("🛑 System stopped")
            
            # Stop UI update loop
            Clock.unschedule(self._update_ui)
            
        except Exception as e:
            self._update_status(f"❌ Failed to stop system: {e}")
    
    def test_network(self, instance=None):
        """Test Android network communication"""
        try:
            if not self.system:
                self._update_status("❌ System not started")
                return
            
            # Create test message
            test_message = {
                'type': 'test',
                'device_id': self.device_id,
                'timestamp': time.time(),
                'message': 'Android network test message'
            }
            
            # Transmit via Android network
            self.system.android_comm.transmit_sphereos_data(
                json.dumps(test_message).encode('utf-8'),
                "atlas",
                f"/test/{int(time.time())}",
                priority=5
            )
            
            self._update_status("📤 Android network test message sent")
            self._add_message_log("Sent: Android network test message")
            
        except Exception as e:
            self._update_status(f"❌ Android network test failed: {e}")
    
    def show_health(self, instance=None):
        """Show system health"""
        try:
            if not self.system:
                self._update_status("❌ System not started")
                return
            
            health = self.system.get_system_status()
            health_text = json.dumps(health, indent=2)
            
            self._update_status("📊 System health retrieved")
            self._add_message_log(f"Health: {health_text}")
            
        except Exception as e:
            self._update_status(f"❌ Health check failed: {e}")
    
    # ============================================================================
    # NETWORK METHODS
    # ============================================================================
    
    def scan_network(self, instance=None):
        """Scan for network devices"""
        try:
            if not self.system:
                self._update_status("❌ System not started")
                return
            
            # Get connected devices from system
            network_status = self.system.android_comm.get_network_status()
            connected_count = network_status.get('connected_devices', 0)
            
            self._update_network_status()
            self._update_status(f"📡 Network scan completed - {connected_count} devices found")
            
        except Exception as e:
            self._update_status(f"❌ Network scan failed: {e}")
    
    def broadcast_message(self, instance=None):
        """Broadcast message to network"""
        try:
            if not self.system:
                self._update_status("❌ System not started")
                return
            
            message = {
                'type': 'broadcast',
                'device_id': self.device_id,
                'timestamp': time.time(),
                'message': 'Hello from Android-only U3CP network!'
            }
            
            # Transmit via Android network
            self.system.android_comm.transmit_sphereos_data(
                json.dumps(message).encode('utf-8'),
                "atlas",
                f"/broadcast/{int(time.time())}",
                priority=3
            )
            
            self._update_status("📤 Broadcast message sent")
            self._add_message_log("Sent: Broadcast message")
            
        except Exception as e:
            self._update_status(f"❌ Broadcast failed: {e}")
    
    # ============================================================================
    # CHAT METHODS
    # ============================================================================
    
    def send_chat_message(self, instance=None):
        """Send chat message"""
        try:
            if not self.system:
                self._update_status("❌ System not started")
                return
            
            message_text = self.chat_input.text.strip()
            if not message_text:
                self._update_status("❌ No message to send")
                return
            
            # Send chat message
            self.system.send_chat_message(message_text)
            
            # Add to chat log
            self._add_chat_message(f"Me: {message_text}")
            self.chat_input.text = ""
            self._update_status("📤 Chat message sent")
            
        except Exception as e:
            self._update_status(f"❌ Chat message send failed: {e}")
    
    # ============================================================================
    # MESSAGE METHODS
    # ============================================================================
    
    def send_message(self, instance=None):
        """Send system message"""
        try:
            if not self.system:
                self._update_status("❌ System not started")
                return
            
            message_text = self.message_input.text.strip()
            if not message_text:
                self._update_status("❌ No message to send")
                return
            
            message = {
                'type': 'user_message',
                'device_id': self.device_id,
                'timestamp': time.time(),
                'message': message_text
            }
            
            # Transmit via Android network
            self.system.android_comm.transmit_sphereos_data(
                json.dumps(message).encode('utf-8'),
                "atlas",
                f"/message/{int(time.time())}",
                priority=2
            )
            
            self._add_message_log(f"Sent: {message_text}")
            self.message_input.text = ""
            self._update_status("📤 Message sent")
            
        except Exception as e:
            self._update_status(f"❌ Message send failed: {e}")
    
    # ============================================================================
    # VALUE DISCOVERY METHODS
    # ============================================================================
    
    def scan_values(self, instance=None):
        """Scan for value opportunities"""
        try:
            if not self.system:
                self._update_status("❌ System not started")
                return
            
            if not self.system.sphere_system:
                self._update_status("❌ SphereOS not available")
                return
            
            # Run value discovery
            opportunities = self.system.sphere_system.scan_value_opportunities()
            
            if opportunities.get('opportunities'):
                self.value_opportunities = opportunities['opportunities']
                self._update_opportunities_display()
                self._update_status(f"💡 Found {len(self.value_opportunities)} opportunities")
            else:
                self._update_status("💡 No value opportunities found")
            
        except Exception as e:
            self._update_status(f"❌ Value scan failed: {e}")
    
    def share_opportunities(self, instance=None):
        """Share value opportunities with network"""
        try:
            if not self.system or not self.value_opportunities:
                self._update_status("❌ No opportunities to share")
                return
            
            # Create opportunity message
            opportunity_data = {
                'type': 'value_opportunities',
                'device_id': self.device_id,
                'timestamp': time.time(),
                'opportunities': self.value_opportunities
            }
            
            # Transmit via Android network
            self.system.android_comm.transmit_sphereos_data(
                json.dumps(opportunity_data).encode('utf-8'),
                "atlas",
                f"/opportunities/{int(time.time())}",
                priority=4
            )
            
            self._update_status(f"📤 Shared {len(self.value_opportunities)} opportunities")
            self._add_message_log(f"Shared: {len(self.value_opportunities)} opportunities")
            
        except Exception as e:
            self._update_status(f"❌ Opportunity sharing failed: {e}")
    
    # ============================================================================
    # SETTINGS METHODS
    # ============================================================================
    
    def save_settings(self, instance=None):
        """Save application settings"""
        try:
            # Update device ID
            new_device_id = self.device_id_input.text.strip()
            if new_device_id:
                self.device_id = new_device_id
            
            # Save settings to file
            settings = {
                'device_id': self.device_id,
                'discovery_port': int(self.discovery_port_input.text),
                'communication_port': int(self.comm_port_input.text),
                'timestamp': time.time()
            }
            
            with open('u3cp_android_only_settings.json', 'w') as f:
                json.dump(settings, f, indent=2)
            
            self._update_status("✅ Settings saved")
            
        except Exception as e:
            self._update_status(f"❌ Settings save failed: {e}")
    
    # ============================================================================
    # UI UPDATE METHODS
    # ============================================================================
    
    def _update_ui(self, dt):
        """Update UI elements"""
        if not self.system:
            return
        
        try:
            # Update cycle display
            current_cycle = self.system.u3cp.get_current_cycle()
            cycle_mode = "Transmitting" if self.system.u3cp.is_transmission_cycle(current_cycle) else "Processing"
            
            if hasattr(self, 'cycle_label'):
                self.cycle_label.text = f'Current Cycle: {current_cycle}\nMode: {cycle_mode}'
            
            # Update network status
            if hasattr(self, 'network_status_label'):
                network_status = self.system.android_comm.get_network_status()
                device_count = network_status.get('connected_devices', 0)
                self.network_status_label.text = f'Network: Connected\nDevices: {device_count}\nRange: Local Network'
            
        except Exception as e:
            print(f"UI update error: {e}")
    
    def _update_status(self, status: str):
        """Update status display"""
        self.status_text = status
        if hasattr(self, 'status_label'):
            self.status_label.text = f'System: {"Running" if self.app_running else "Stopped"}\nDevice ID: {self.device_id}\nStatus: {status}'
        print(f"Status: {status}")
    
    def _update_network_status(self):
        """Update network status display"""
        if hasattr(self, 'devices_label'):
            if self.system:
                network_status = self.system.android_comm.get_network_status()
                device_count = network_status.get('connected_devices', 0)
                if device_count > 0:
                    self.devices_label.text = f"{device_count} devices connected"
                else:
                    self.devices_label.text = "No devices connected"
            else:
                self.devices_label.text = "No devices connected"
    
    def _update_opportunities_display(self):
        """Update opportunities display"""
        if hasattr(self, 'opportunities_label'):
            if self.value_opportunities:
                opportunities_text = "\n".join([
                    f"{opp['opportunity_id']}: {opp['area']} (${opp['value_potential']})"
                    for opp in self.value_opportunities[:10]  # Show first 10
                ])
                self.opportunities_label.text = opportunities_text
            else:
                self.opportunities_label.text = "No opportunities found"
    
    def _add_message_log(self, message: str):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.message_log.append(log_entry)
        
        # Keep only last 50 messages
        if len(self.message_log) > 50:
            self.message_log = self.message_log[-50:]
        
        # Update display
        if hasattr(self, 'message_log_label'):
            log_text = "\n".join(self.message_log[-20:])  # Show last 20
            self.message_log_label.text = log_text
    
    def _add_chat_message(self, message: str):
        """Add chat message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        chat_entry = f"[{timestamp}] {message}"
        self.chat_messages.append(chat_entry)
        
        # Keep only last 50 messages
        if len(self.chat_messages) > 50:
            self.chat_messages = self.chat_messages[-50:]
        
        # Update display
        if hasattr(self, 'chat_log_label'):
            chat_text = "\n".join(self.chat_messages[-20:])  # Show last 20
            self.chat_log_label.text = chat_text
    
    def on_stop(self):
        """Called when app is stopped"""
        if self.system:
            self.stop_system()

# ============================================================================
# CONSOLE MODE
# ============================================================================

class ConsoleU3CPAndroidOnlyApp:
    """Console version of U3CP Android-only app for non-Android environments"""
    
    def __init__(self):
        self.device_id = f"console_{int(time.time())}"
        self.system = None
        self.running = False
    
    def run(self):
        """Run console interface"""
        print("📱 U3CP Android-Only System - Console Mode")
        print("=" * 50)
        
        while True:
            print("\n📱 U3CP Android-Only Console Menu:")
            print("1. Start System")
            print("2. Stop System")
            print("3. Test Network")
            print("4. Show Health")
            print("5. Send Chat Message")
            print("6. Send System Message")
            print("7. Scan Values")
            print("8. Network Status")
            print("9. Exit")
            
            choice = input("\nEnter choice (1-9): ").strip()
            
            if choice == '1':
                self.start_system()
            elif choice == '2':
                self.stop_system()
            elif choice == '3':
                self.test_network()
            elif choice == '4':
                self.show_health()
            elif choice == '5':
                self.send_chat_message()
            elif choice == '6':
                self.send_system_message()
            elif choice == '7':
                self.scan_values()
            elif choice == '8':
                self.show_network_status()
            elif choice == '9':
                self.stop_system()
                break
            else:
                print("❌ Invalid choice")
    
    def start_system(self):
        """Start the system"""
        try:
            if not U3CP_AVAILABLE:
                print("❌ U3CP Android-only system not available")
                return
            
            self.system = U3CPAndroidOnlySystem(self.device_id)
            self.system.start_integrated_system()
            self.running = True
            print("✅ Android-only system started")
            
        except Exception as e:
            print(f"❌ Failed to start system: {e}")
    
    def stop_system(self):
        """Stop the system"""
        try:
            if self.system:
                self.system.stop_integrated_system()
                self.system = None
            self.running = False
            print("🛑 System stopped")
            
        except Exception as e:
            print(f"❌ Failed to stop system: {e}")
    
    def test_network(self):
        """Test Android network communication"""
        try:
            if not self.system:
                print("❌ System not started")
                return
            
            test_message = {
                'type': 'test',
                'device_id': self.device_id,
                'timestamp': time.time(),
                'message': 'Android network test message'
            }
            
            self.system.android_comm.transmit_sphereos_data(
                json.dumps(test_message).encode('utf-8'),
                "atlas",
                f"/test/{int(time.time())}",
                priority=5
            )
            
            print("📤 Android network test message sent")
            
        except Exception as e:
            print(f"❌ Android network test failed: {e}")
    
    def show_health(self):
        """Show system health"""
        try:
            if not self.system:
                print("❌ System not started")
                return
            
            health = self.system.get_system_status()
            print("📊 System Health:")
            print(json.dumps(health, indent=2))
            
        except Exception as e:
            print(f"❌ Health check failed: {e}")
    
    def send_chat_message(self):
        """Send chat message"""
        try:
            if not self.system:
                print("❌ System not started")
                return
            
            message = input("Enter chat message: ").strip()
            if not message:
                print("❌ No message entered")
                return
            
            self.system.send_chat_message(message)
            print("📤 Chat message sent")
            
        except Exception as e:
            print(f"❌ Chat message send failed: {e}")
    
    def send_system_message(self):
        """Send system message"""
        try:
            if not self.system:
                print("❌ System not started")
                return
            
            message = input("Enter system message: ").strip()
            if not message:
                print("❌ No message entered")
                return
            
            message_data = {
                'type': 'user_message',
                'device_id': self.device_id,
                'timestamp': time.time(),
                'message': message
            }
            
            self.system.android_comm.transmit_sphereos_data(
                json.dumps(message_data).encode('utf-8'),
                "atlas",
                f"/message/{int(time.time())}",
                priority=2
            )
            
            print("📤 System message sent")
            
        except Exception as e:
            print(f"❌ System message send failed: {e}")
    
    def scan_values(self):
        """Scan for value opportunities"""
        try:
            if not self.system:
                print("❌ System not started")
                return
            
            if not self.system.sphere_system:
                print("❌ SphereOS not available")
                return
            
            opportunities = self.system.sphere_system.scan_value_opportunities()
            
            if opportunities.get('opportunities'):
                print(f"💡 Found {len(opportunities['opportunities'])} opportunities:")
                for opp in opportunities['opportunities'][:5]:  # Show first 5
                    print(f"  - {opp['opportunity_id']}: {opp['area']} (${opp['value_potential']})")
            else:
                print("💡 No value opportunities found")
            
        except Exception as e:
            print(f"❌ Value scan failed: {e}")
    
    def show_network_status(self):
        """Show network status"""
        try:
            if not self.system:
                print("❌ System not started")
                return
            
            network_status = self.system.android_comm.get_network_status()
            device_count = network_status.get('connected_devices', 0)
            print(f"📡 Network Status:")
            print(f"  Connected devices: {device_count}")
            print(f"  Range: Local Network")
            print(f"  Status: {'Connected' if self.running else 'Disconnected'}")
            
        except Exception as e:
            print(f"❌ Network status failed: {e}")

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Main function"""
    print("📱 U3CP Android-Only App Starting...")
    
    if KIVY_AVAILABLE:
        # Run Kivy app
        app = U3CPAndroidOnlyApp()
        app.run()
    else:
        # Run console app
        console_app = ConsoleU3CPAndroidOnlyApp()
        console_app.run()

if __name__ == "__main__":
    main() 
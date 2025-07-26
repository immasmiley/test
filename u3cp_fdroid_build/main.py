#!/usr/bin/env python3
"""
U3CP Enhanced Android Application with Self-Distribution
Entry point for autonomous, self-healing communication network
"""

import os
import sys
import time
import json
import threading
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Check for Android environment
try:
    import android
    ANDROID_ENV = True
    print("🤖 Android environment detected")
except ImportError:
    ANDROID_ENV = False
    print("💻 Desktop environment detected")

# Import core systems
try:
    from SphereOS_Android_Unified import UnifiedSphereSystem, main as sphereos_main
    from U3CP_Android_Only_System import U3CPSystem
    from U3CP_Android_Only_App import U3CPApp
    print("✅ Core systems imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class SelfDistributingU3CP:
    """Enhanced U3CP system with self-distribution capabilities"""
    
    def __init__(self):
        self.device_id = f"u3cp_device_{int(time.time())}"
        self.sphere_system = None
        self.u3cp_system = None
        self.app_instance = None
        self.distribution_enabled = True
        self.self_repair_enabled = True
        
    def initialize_systems(self):
        """Initialize all U3CP systems"""
        try:
            print("🌌 Initializing U3CP enhanced systems...")
            
            # Initialize SphereOS
            self.sphere_system = UnifiedSphereSystem("sphereos_u3cp_integrated.db")
            print("✅ SphereOS system initialized")
            
            # Initialize U3CP system  
            self.u3cp_system = U3CPSystem(self.device_id)
            print("✅ U3CP communication system initialized")
            
            # Setup self-distribution
            if self.distribution_enabled:
                self._setup_self_distribution()
            
            return True
            
        except Exception as e:
            print(f"❌ System initialization failed: {e}")
            return False
    
    def _setup_self_distribution(self):
        """Setup self-distribution capabilities"""
        try:
            print("🚀 Setting up self-distribution system...")
            
            # Create distribution metadata
            dist_metadata = {
                "app_version": "0.1.0",
                "package_name": "org.sphereos.u3cp",
                "distribution_enabled": True,
                "self_repair_enabled": True,
                "created_at": time.time(),
                "device_id": self.device_id
            }
            
            # Store in SphereOS
            self.sphere_system.store_data_unified(
                json.dumps(dist_metadata).encode(),
                "atlas",
                "/distribution/metadata"
            )
            
            print("✅ Self-distribution setup complete")
            
        except Exception as e:
            print(f"⚠️ Self-distribution setup failed: {e}")
    
    def start_autonomous_network(self):
        """Start autonomous self-healing network"""
        try:
            print("📡 Starting autonomous network...")
            
            # Start background threads for autonomous operation
            threading.Thread(target=self._network_maintenance_loop, daemon=True).start()
            threading.Thread(target=self._distribution_monitoring_loop, daemon=True).start()
            
            print("✅ Autonomous network started")
            
        except Exception as e:
            print(f"❌ Network start failed: {e}")
    
    def _network_maintenance_loop(self):
        """Background network maintenance and self-healing"""
        while True:
            try:
                # Check system health
                health = self.sphere_system.get_system_health()
                
                if health.get('status') != 'healthy':
                    print("🔧 System health issue detected - initiating self-repair...")
                    self._attempt_self_repair()
                
                # Sleep for 60 seconds before next check
                time.sleep(60)
                
            except Exception as e:
                print(f"⚠️ Network maintenance error: {e}")
                time.sleep(30)  # Shorter sleep on error
    
    def _distribution_monitoring_loop(self):
        """Monitor for distribution requests from other devices"""
        while True:
            try:
                # Check for incoming distribution requests
                # This would integrate with the proximity-based sharing system
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                print(f"⚠️ Distribution monitoring error: {e}")
                time.sleep(60)
    
    def _attempt_self_repair(self):
        """Attempt self-repair of the system"""
        try:
            print("🔧 Attempting system self-repair...")
            
            # Check database integrity
            if self.sphere_system:
                # Verify database
                health = self.sphere_system.get_system_health()
                print(f"📊 System health: {health.get('status', 'unknown')}")
            
            # In a real implementation, this would:
            # 1. Verify embedded APK integrity
            # 2. Download fresh copy from network if needed
            # 3. Restart components as necessary
            
            print("✅ Self-repair completed")
            
        except Exception as e:
            print(f"❌ Self-repair failed: {e}")
    
    def run(self):
        """Main application entry point"""
        try:
            print("🌌 Starting U3CP Enhanced Application")
            print("=" * 50)
            
            # Initialize systems
            if not self.initialize_systems():
                print("❌ Failed to initialize systems")
                return False
            
            # Start autonomous network
            self.start_autonomous_network()
            
            # Start main application
            if ANDROID_ENV:
                print("📱 Starting Android UI...")
                # Start Kivy app for Android
                sphereos_main()
            else:
                print("💻 Starting console mode...")
                # Start console mode for desktop
                self._run_console_mode()
            
            return True
            
        except Exception as e:
            print(f"❌ Application start failed: {e}")
            return False
    
    def _run_console_mode(self):
        """Run in console mode for desktop testing"""
        print("\n🌌 U3CP Enhanced Console Mode")
        print("Available commands:")
        print("  status  - Show system status")
        print("  health  - Check system health") 
        print("  share   - Simulate app sharing")
        print("  repair  - Test self-repair")
        print("  quit    - Exit application")
        
        while True:
            try:
                command = input("\nU3CP> ").strip().lower()
                
                if command == "quit":
                    break
                elif command == "status":
                    self._show_status()
                elif command == "health":
                    self._show_health()
                elif command == "share":
                    self._simulate_sharing()
                elif command == "repair":
                    self._attempt_self_repair()
                else:
                    print("Unknown command. Type 'quit' to exit.")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Command error: {e}")
        
        print("\n👋 Goodbye!")
    
    def _show_status(self):
        """Show system status"""
        try:
            health = self.sphere_system.get_system_health()
            print(f"\n📊 System Status:")
            print(f"  Status: {health.get('status', 'unknown')}")
            print(f"  Database: {health.get('database_size_mb', 0)} MB")
            print(f"  Active sessions: {health.get('active_sessions', 0)}")
            print(f"  Distribution: {'Enabled' if self.distribution_enabled else 'Disabled'}")
            
        except Exception as e:
            print(f"❌ Status check failed: {e}")
    
    def _show_health(self):
        """Show detailed health information"""
        try:
            health = self.sphere_system.get_system_health()
            print(f"\n🏥 Detailed Health Check:")
            
            for key, value in health.items():
                if isinstance(value, dict):
                    print(f"  {key}:")
                    for sub_key, sub_value in value.items():
                        print(f"    {sub_key}: {sub_value}")
                else:
                    print(f"  {key}: {value}")
                    
        except Exception as e:
            print(f"❌ Health check failed: {e}")
    
    def _simulate_sharing(self):
        """Simulate app sharing for testing"""
        print("\n📤 Simulating app sharing...")
        print("  In real deployment, this would:")
        print("  1. Detect nearby devices via GPS proximity")
        print("  2. Offer to share APK installer")
        print("  3. Transfer via U3CP network protocol")
        print("  4. Verify integrity on receiving device")
        print("✅ Sharing simulation complete")

def main():
    """Main entry point"""
    app = SelfDistributingU3CP()
    return app.run()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

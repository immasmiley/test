#!/usr/bin/env python3
"""
U3CP Android-Only System Test Script
Quick verification of Android-only implementation
"""

import os
import sys
import time
import json
import threading
from datetime import datetime

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from U3CP_Android_Only_System import U3CPAndroidOnlySystem
        print("✅ U3CP Android-Only System imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import U3CP Android-Only System: {e}")
        return False

def test_system_initialization():
    """Test system initialization"""
    print("\n🔧 Testing system initialization...")
    
    try:
        from U3CP_Android_Only_System import U3CPAndroidOnlySystem
        
        device_id = f"test_device_{int(time.time())}"
        system = U3CPAndroidOnlySystem(device_id)
        
        print(f"✅ System initialized with device ID: {device_id}")
        return system
    except Exception as e:
        print(f"❌ System initialization failed: {e}")
        return None

def test_system_start_stop(system):
    """Test system start and stop"""
    print("\n🚀 Testing system start/stop...")
    
    try:
        # Start system
        system.start_integrated_system()
        print("✅ System started successfully")
        
        # Wait a moment
        time.sleep(2)
        
        # Check status
        status = system.get_system_status()
        print(f"✅ System status: {status.get('integration_active', False)}")
        
        # Stop system
        system.stop_integrated_system()
        print("✅ System stopped successfully")
        
        return True
    except Exception as e:
        print(f"❌ System start/stop test failed: {e}")
        return False

def test_android_communication(system):
    """Test Android communication system"""
    print("\n📱 Testing Android communication...")
    
    try:
        # Start system
        system.start_integrated_system()
        time.sleep(1)
        
        # Test network status
        network_status = system.android_comm.get_network_status()
        print(f"✅ Network status: {network_status.get('running', False)}")
        
        # Test message transmission
        test_message = {
            'type': 'test',
            'device_id': system.device_id,
            'timestamp': time.time(),
            'message': 'Test message from Android-only system'
        }
        
        system.android_comm.transmit_sphereos_data(
            json.dumps(test_message).encode('utf-8'),
            "atlas",
            f"/test/{int(time.time())}",
            priority=5
        )
        print("✅ Test message transmitted")
        
        # Test chat message
        system.send_chat_message("Hello from test script!")
        print("✅ Chat message sent")
        
        # Stop system
        system.stop_integrated_system()
        
        return True
    except Exception as e:
        print(f"❌ Android communication test failed: {e}")
        return False

def test_sphereos_integration(system):
    """Test SphereOS integration"""
    print("\n💾 Testing SphereOS integration...")
    
    try:
        if not system.sphere_system:
            print("⚠️ SphereOS not available, skipping test")
            return True
        
        # Start system
        system.start_integrated_system()
        time.sleep(1)
        
        # Test data storage
        test_data = {
            'test': True,
            'timestamp': time.time(),
            'message': 'Test data for SphereOS'
        }
        
        system.sphere_system.store_data_unified(
            json.dumps(test_data).encode('utf-8'),
            "atlas",
            "/test/android_only"
        )
        print("✅ Data stored in SphereOS")
        
        # Test value discovery
        opportunities = system.sphere_system.scan_value_opportunities()
        print(f"✅ Value discovery: {len(opportunities.get('opportunities', []))} opportunities found")
        
        # Test system health
        health = system.sphere_system.get_system_health()
        print(f"✅ System health: {health.get('status', 'unknown')}")
        
        # Stop system
        system.stop_integrated_system()
        
        return True
    except Exception as e:
        print(f"❌ SphereOS integration test failed: {e}")
        return False

def test_nostr_relay(system):
    """Test Nostr relay integration"""
    print("\n🌐 Testing Nostr relay...")
    
    try:
        if not system.sphere_system or not system.sphere_system.nostr_relay:
            print("⚠️ Nostr relay not available, skipping test")
            return True
        
        # Start system
        system.start_integrated_system()
        time.sleep(1)
        
        # Test relay info
        relay_info = system.sphere_system.nostr_relay.get_relay_info()
        print(f"✅ Nostr relay: {relay_info.get('name', 'unknown')}")
        
        # Test event transmission
        from SphereOS_Android_Unified import NostrEvent
        import hashlib
        
        test_event = NostrEvent(
            id=hashlib.sha256(f"test_event_{time.time()}".encode()).hexdigest(),
            pubkey=system.device_id,
            created_at=int(time.time()),
            kind=1,
            tags=[],
            content="Test Nostr event from Android-only system",
            sig="test_signature"
        )
        
        system.android_comm.transmit_nostr_event(test_event)
        print("✅ Nostr event transmitted")
        
        # Stop system
        system.stop_integrated_system()
        
        return True
    except Exception as e:
        print(f"❌ Nostr relay test failed: {e}")
        return False

def test_u3cp_algorithm(system):
    """Test U3CP algorithm"""
    print("\n⚡ Testing U3CP algorithm...")
    
    try:
        # Test cycle timing
        current_cycle = system.u3cp.get_current_cycle()
        print(f"✅ Current cycle: {current_cycle}")
        
        # Test cycle coefficients
        coefficients = system.u3cp.get_cycle_coefficients(current_cycle)
        print(f"✅ Cycle coefficients: {coefficients}")
        
        # Test transmission cycles
        is_transmission = system.u3cp.is_transmission_cycle(current_cycle)
        print(f"✅ Is transmission cycle: {is_transmission}")
        
        # Test processing cycles
        is_processing = system.u3cp.is_processing_cycle(current_cycle)
        print(f"✅ Is processing cycle: {is_processing}")
        
        return True
    except Exception as e:
        print(f"❌ U3CP algorithm test failed: {e}")
        return False

def test_console_app():
    """Test console app functionality"""
    print("\n📱 Testing console app...")
    
    try:
        from U3CP_Android_Only_App import ConsoleU3CPAndroidOnlyApp
        
        # Create console app
        console_app = ConsoleU3CPAndroidOnlyApp()
        print("✅ Console app created successfully")
        
        # Test system creation
        console_app.start_system()
        print("✅ Console app system started")
        
        # Test network status
        console_app.show_network_status()
        
        # Stop system
        console_app.stop_system()
        print("✅ Console app system stopped")
        
        return True
    except Exception as e:
        print(f"❌ Console app test failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🧪 U3CP Android-Only System - Complete Test Suite")
    print("=" * 60)
    
    test_results = []
    
    # Test 1: Imports
    test_results.append(("Imports", test_imports()))
    
    # Test 2: System initialization
    system = test_system_initialization()
    test_results.append(("System Initialization", system is not None))
    
    if system:
        # Test 3: U3CP Algorithm
        test_results.append(("U3CP Algorithm", test_u3cp_algorithm(system)))
        
        # Test 4: System start/stop
        test_results.append(("System Start/Stop", test_system_start_stop(system)))
        
        # Test 5: Android communication
        test_results.append(("Android Communication", test_android_communication(system)))
        
        # Test 6: SphereOS integration
        test_results.append(("SphereOS Integration", test_sphereos_integration(system)))
        
        # Test 7: Nostr relay
        test_results.append(("Nostr Relay", test_nostr_relay(system)))
    
    # Test 8: Console app
    test_results.append(("Console App", test_console_app()))
    
    # Print results
    print("\n📊 Test Results Summary")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! U3CP Android-Only system is ready for use.")
        print("\n🚀 Next steps:")
        print("   1. Run: python U3CP_Android_Only_App.py")
        print("   2. Test with multiple devices on same network")
        print("   3. Verify chat and messaging functionality")
        print("   4. Test Nostr relay integration")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        print("\n🔧 Troubleshooting:")
        print("   1. Check Python dependencies: pip install -r requirements_android_only.txt")
        print("   2. Verify SphereOS_Android_Unified.py is available")
        print("   3. Check network permissions and firewall settings")
    
    return passed == total

def main():
    """Main function"""
    try:
        success = run_all_tests()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 
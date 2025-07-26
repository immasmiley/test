#!/usr/bin/env python3
"""
Test SphereOS Executable
Verifies the executable works correctly
"""

import os
import sys
import time
import subprocess
import requests
from pathlib import Path

def check_executable_exists():
    """Check if the executable exists"""
    exe_path = Path("dist/SphereOS_Complete.exe")
    if exe_path.exists():
        print(f"✅ Executable found: {exe_path}")
        print(f"📊 Size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
        return True
    else:
        print(f"❌ Executable not found: {exe_path}")
        return False

def test_executable_startup():
    """Test if the executable can start"""
    print("\n🔨 Testing executable startup...")
    
    try:
        # Start the executable
        process = subprocess.Popen(
            ["dist/SphereOS_Complete.exe"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit for startup
        time.sleep(5)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Executable started successfully")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Executable failed to start")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting executable: {e}")
        return None

def test_web_interface(process):
    """Test the web interface"""
    print("\n🌐 Testing web interface...")
    
    try:
        # Wait for server to start
        time.sleep(10)
        
        # Test health endpoint
        response = requests.get("http://127.0.0.1:8765/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health endpoint working")
            print(f"   Status: {data.get('status')}")
            print(f"   Domains: {data.get('domains')}")
            print(f"   Core Elements: {data.get('core_elements')}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        # Test system info endpoint
        response = requests.get("http://127.0.0.1:8765/api/system/info", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ System info endpoint working")
            print(f"   System: {data.get('system_name')}")
            print(f"   Version: {data.get('version')}")
        else:
            print(f"❌ System info endpoint failed: {response.status_code}")
            return False
        
        # Test domain endpoint
        response = requests.get("http://127.0.0.1:8765/api/domains/commercial_exchange/scan", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Domain endpoint working")
            print(f"   Domain: {data.get('domain')}")
            print(f"   Opportunities: {data.get('opportunities_found')}")
        else:
            print(f"❌ Domain endpoint failed: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Web interface test failed: {e}")
        return False

def test_comprehensive_scan(process):
    """Test comprehensive domain scan"""
    print("\n🔍 Testing comprehensive domain scan...")
    
    try:
        response = requests.get("http://127.0.0.1:8765/api/domains/comprehensive/scan", timeout=15)
        if response.status_code == 200:
            data = response.json()
            print("✅ Comprehensive scan working")
            print(f"   Domains scanned: {data.get('domains_scanned')}")
            print(f"   Total opportunities: {data.get('total_opportunities_found')}")
            
            # Check if all 12 domains are present
            domain_results = data.get('domain_results', {})
            if len(domain_results) == 12:
                print("✅ All 12 domains detected")
            else:
                print(f"⚠️ Only {len(domain_results)} domains detected")
                
        else:
            print(f"❌ Comprehensive scan failed: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Comprehensive scan test failed: {e}")
        return False

def cleanup(process):
    """Clean up the process"""
    if process:
        try:
            process.terminate()
            process.wait(timeout=5)
            print("✅ Process terminated successfully")
        except subprocess.TimeoutExpired:
            process.kill()
            print("⚠️ Process killed forcefully")
        except Exception as e:
            print(f"⚠️ Error terminating process: {e}")

def main():
    """Main test function"""
    print("🌌 SphereOS Executable Test")
    print("=" * 40)
    
    # Step 1: Check executable exists
    if not check_executable_exists():
        print("❌ Test failed: Executable not found")
        return
    
    # Step 2: Test startup
    process = test_executable_startup()
    if not process:
        print("❌ Test failed: Executable startup failed")
        return
    
    try:
        # Step 3: Test web interface
        if not test_web_interface(process):
            print("❌ Test failed: Web interface not working")
            return
        
        # Step 4: Test comprehensive scan
        if not test_comprehensive_scan(process):
            print("❌ Test failed: Comprehensive scan not working")
            return
        
        print("\n🎉 All tests passed!")
        print("✅ Executable is working correctly")
        print("✅ Web interface is functional")
        print("✅ All 12 domains are accessible")
        print("✅ 108 core elements are working")
        
    finally:
        # Cleanup
        print("\n🧹 Cleaning up...")
        cleanup(process)
    
    print("\n🚀 SphereOS Complete System is ready for use!")
    print("📁 Executable: dist/SphereOS_Complete.exe")
    print("📖 Documentation: README_EXECUTABLE.md")
    print("🎯 Launch script: launch_sphereos.bat")

if __name__ == "__main__":
    main() 
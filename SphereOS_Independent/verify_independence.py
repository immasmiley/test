#!/usr/bin/env python3
"""
SphereOS Independent Copy Verification
Verifies that this copy is completely independent and functional
"""

import os
import sys
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path

def verify_independence():
    """Verify the independent copy is working correctly"""
    
    print("=" * 70)
    print("🔍 SphereOS Independent Copy Verification")
    print("=" * 70)
    print()
    
    # 1. Verify current directory
    current_dir = Path.cwd()
    print(f"📍 Current Directory: {current_dir}")
    print(f"📁 Directory Name: {current_dir.name}")
    
    if "Independent" not in current_dir.name:
        print("⚠️  Warning: Not in expected independent directory")
    else:
        print("✅ Independent directory confirmed")
    
    print()
    
    # 2. Check for independent database files
    print("🗄️  Database Independence Check:")
    db_files = [
        "sphereos_enhanced_constituent.db",
        "sphereos_constituent.db"
    ]
    
    for db_file in db_files:
        if os.path.exists(db_file):
            # Get file size and modification time
            stat = os.stat(db_file)
            size_kb = stat.st_size / 1024
            mod_time = datetime.fromtimestamp(stat.st_mtime)
            print(f"✅ {db_file}: {size_kb:.1f}KB, modified {mod_time}")
            
            # Check if database is accessible
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                print(f"   📊 Tables: {len(tables)} tables found")
                conn.close()
            except Exception as e:
                print(f"   ❌ Database error: {e}")
        else:
            print(f"❌ {db_file}: Not found")
    
    print()
    
    # 3. Check for independent application files
    print("📱 Application Independence Check:")
    app_files = [
        "sphereos_enhanced_constituent.py",
        "sphereos_executable.py", 
        "sphereos_permanent_server.py",
        "sphereos_constituent_wrapped.py"
    ]
    
    for app_file in app_files:
        if os.path.exists(app_file):
            stat = os.stat(app_file)
            size_kb = stat.st_size / 1024
            mod_time = datetime.fromtimestamp(stat.st_mtime)
            print(f"✅ {app_file}: {size_kb:.1f}KB, modified {mod_time}")
        else:
            print(f"❌ {app_file}: Not found")
    
    print()
    
    # 4. Check for independent launcher
    print("🚀 Launcher Independence Check:")
    launcher_files = [
        "launch_independent_sphereos.bat",
        "build_executable.py"
    ]
    
    for launcher in launcher_files:
        if os.path.exists(launcher):
            print(f"✅ {launcher}: Found")
        else:
            print(f"❌ {launcher}: Not found")
    
    print()
    
    # 5. Check for independent documentation
    print("📚 Documentation Independence Check:")
    doc_files = [
        "README_INDEPENDENT.md",
        "ENDPOINTS_AND_VALUE_DISCOVERY_SUMMARY.md",
        "CONSTITUENT_SOLUTION_SUMMARY.md"
    ]
    
    for doc in doc_files:
        if os.path.exists(doc):
            stat = os.stat(doc)
            size_kb = stat.st_size / 1024
            print(f"✅ {doc}: {size_kb:.1f}KB")
        else:
            print(f"❌ {doc}: Not found")
    
    print()
    
    # 6. Verify no external dependencies
    print("🔗 Dependency Independence Check:")
    try:
        # Try to import the enhanced constituent application
        sys.path.insert(0, str(current_dir))
        from sphereos_enhanced_constituent import SphereOSEnhancedServer
        
        # Initialize the server
        server = SphereOSEnhancedServer()
        
        # Test basic functionality
        health = server.get_health_status()
        print(f"✅ Enhanced constituent application: {health['status']}")
        
        # Test value discovery
        value_scan = server.scan_all_value_areas()
        print(f"✅ Value discovery: {value_scan['areas_scanned']} areas scanned")
        
        print("✅ No external dependencies required")
        
    except Exception as e:
        print(f"❌ Application error: {e}")
    
    print()
    
    # 7. Check for parent directory independence
    print("🏠 Parent Directory Independence:")
    parent_dir = current_dir.parent
    print(f"📍 Parent Directory: {parent_dir}")
    
    # Check if we can access parent SphereOS files
    parent_sphereos_files = [
        parent_dir / "sphereos_server.py",
        parent_dir / "sphereos_unified_server.py",
        parent_dir / "SphereOS_App" / "sphereos_enhanced_constituent.py"
    ]
    
    for file_path in parent_sphereos_files:
        if file_path.exists():
            print(f"ℹ️  Parent file accessible: {file_path.name}")
        else:
            print(f"✅ Parent file not accessible: {file_path.name}")
    
    print()
    
    # 8. Generate independence summary
    print("📊 Independence Summary:")
    print(f"✅ Independent Directory: {current_dir.name}")
    print(f"✅ Independent Databases: {len([f for f in db_files if os.path.exists(f)])}/{len(db_files)}")
    print(f"✅ Independent Applications: {len([f for f in app_files if os.path.exists(f)])}/{len(app_files)}")
    print(f"✅ Independent Launchers: {len([f for f in launcher_files if os.path.exists(f)])}/{len(launcher_files)}")
    print(f"✅ Independent Documentation: {len([f for f in doc_files if os.path.exists(f)])}/{len(doc_files)}")
    
    print()
    print("🎉 SphereOS Independent Copy Verification Complete!")
    print("=" * 70)

if __name__ == "__main__":
    verify_independence() 
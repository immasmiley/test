#!/usr/bin/env python3
"""
Build Script for SphereOS Executable
Creates a standalone .exe file with all dependencies
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_executable.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False
    return True

def create_executable():
    """Create the .exe file using PyInstaller"""
    print("🔨 Creating executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window (optional)
        "--name=SphereOS_Complete",  # Executable name
        "--add-data=sphereos_domain_endpoints.py;.",  # Include domain endpoints
        "--add-data=sphereos_combined_endpoints.py;.",  # Include combined endpoints
        "--add-data=sphereos_unified_system.py;.",  # Include unified system
        "--hidden-import=uvicorn.logging",
        "--hidden-import=uvicorn.loops",
        "--hidden-import=uvicorn.loops.auto",
        "--hidden-import=uvicorn.protocols",
        "--hidden-import=uvicorn.protocols.http",
        "--hidden-import=uvicorn.protocols.http.auto",
        "--hidden-import=uvicorn.protocols.websockets",
        "--hidden-import=uvicorn.protocols.websockets.auto",
        "--hidden-import=uvicorn.lifespan",
        "--hidden-import=uvicorn.lifespan.on",
        "sphereos_executable.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ Executable created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create executable: {e}")
        return False

def create_simple_executable():
    """Create a simpler executable without complex dependencies"""
    print("🔨 Creating simple executable...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name=SphereOS_Simple",
        "--hidden-import=fastapi",
        "--hidden-import=uvicorn",
        "--hidden-import=pydantic",
        "sphereos_executable.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ Simple executable created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create simple executable: {e}")
        return False

def cleanup():
    """Clean up build files"""
    print("🧹 Cleaning up build files...")
    try:
        # Remove build directory
        if os.path.exists("build"):
            shutil.rmtree("build")
        
        # Remove spec file
        for spec_file in Path(".").glob("*.spec"):
            spec_file.unlink()
            
        print("✅ Cleanup completed")
    except Exception as e:
        print(f"⚠️ Cleanup warning: {e}")

def main():
    """Main build process"""
    print("🌌 SphereOS Executable Builder")
    print("=" * 40)
    
    # Step 1: Install requirements
    if not install_requirements():
        print("❌ Build failed at requirements installation")
        return
    
    # Step 2: Try to create full executable
    print("\n🔨 Attempting to create full executable...")
    if create_executable():
        print("✅ Full executable created successfully!")
        print("📁 Check the 'dist' folder for SphereOS_Complete.exe")
    else:
        print("⚠️ Full executable failed, trying simple version...")
        if create_simple_executable():
            print("✅ Simple executable created successfully!")
            print("📁 Check the 'dist' folder for SphereOS_Simple.exe")
        else:
            print("❌ Both executable creation attempts failed")
            return
    
    # Step 3: Cleanup
    cleanup()
    
    print("\n🎉 Build process completed!")
    print("📁 Executable files are in the 'dist' folder")
    print("🚀 You can now run the .exe file directly")

if __name__ == "__main__":
    main() 
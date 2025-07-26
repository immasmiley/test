#!/usr/bin/env python3
"""
U3CP Self-Distribution Setup Script

This single script creates all necessary files and directories for building the U3CP app
and preparing it for a SphereOS-integrated F-Droid distribution model.
"""

import os
import shutil
from pathlib import Path

# --- Configuration ---
BUILD_DIR = "u3cp_fdroid_build"
# --- FIX 1: Corrected, Robust Path ---
SCRIPT_DIR = Path(__file__).parent.resolve()
REAL_SPHEREOS_SYSTEM_PATH = SCRIPT_DIR.parent / "SphereOS_Android_Unified.py" # Corrected Path
ESSENTIAL_FILES = [
    "U3CP_Android_Only_System.py",
    "U3CP_Android_Only_App.py",
    "sphereos_android_only.db"
]

def write_file(filepath, content):
    """Helper to write content to a file, creating directories if needed."""
    dir_path = os.path.dirname(filepath)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  - Created: {filepath}")

def main():
    print("--- 🌌 Setting up U3CP REAL Distribution Environment ---")
    
    # --- Part 1: Prepare Build Directory ---
    print(f"\n[1/5] Preparing build directory: '{BUILD_DIR}'...")
    os.makedirs(BUILD_DIR, exist_ok=True)
    
    for filename in ESSENTIAL_FILES:
        if os.path.exists(filename):
            shutil.copy(filename, os.path.join(BUILD_DIR, filename))
            print(f"  - Copied: {filename}")
        else:
            print(f"  - WARNING: Essential file not found: {filename}")

    # --- Part 2: Integrate REAL SphereOS System ---
    print(f"\n[2/5] Integrating real SphereOS system...")
    if REAL_SPHEREOS_SYSTEM_PATH.exists():
        shutil.copy(REAL_SPHEREOS_SYSTEM_PATH, os.path.join(BUILD_DIR, "SphereOS_Android_Unified.py"))
        print(f"  - INTEGRATED: {REAL_SPHEREOS_SYSTEM_PATH.name}")
    else:
        print(f"  - FATAL ERROR: Real SphereOS system not found at '{REAL_SPHEREOS_SYSTEM_PATH}'")
        # --- FIX 2: Exit on Failure ---
        import sys
        sys.exit(1)
            
    main_py_content = """from U3CP_Android_Only_App import U3CPAndroidOnlyApp
if __name__ == '__main__':
    U3CPAndroidOnlyApp().run()
"""
    write_file(os.path.join(BUILD_DIR, "main.py"), main_py_content)

    # --- Part 3: Create Buildozer Spec ---
    print(f"\n[3/5] Creating 'buildozer.spec' file...")
    # (Content is the same, no changes needed here)
    buildozer_spec_content = """[app]
title = U3CP Network Node
package.name = u3cp_node
package.domain = org.sphereos.u3cp
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,json,txt,md
requirements = python3,kivy==2.2.1,sqlite3,websockets,asyncio,cryptography,qrcode,zlib,hashlib,json,threading,datetime,dataclasses,enum,pathlib,base64,math,random
version = 0.1.0
author = U3CP Development Team
description = Distributed communication network using 3-channel protocol
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,WAKE_LOCK,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION
android.api = 28
android.minapi = 21
android.archs = armeabi-v7a, arm64-v8a
android.wakelock = True
[buildozer]
log_level = 2
"""
    write_file(os.path.join(BUILD_DIR, "buildozer.spec"), buildozer_spec_content)
    
    # --- Part 4: Create REAL Git Bridge and Bootstrap ---
    print(f"\n[4/5] Creating REAL SphereOS bridge and bootstrap scripts...")
    git_bridge_content = r'''#!/usr/bin/env python3
import os, sys, json, subprocess, tarfile, io, time
from pathlib import Path
from SphereOS_Android_Unified import UnifiedSphereSystem

class SphereOSGitBridge:
    def __init__(self):
        script_dir = Path(__file__).parent.resolve()
        self.db_path = script_dir.parent / "sphereos_u3cp_integrated.db"
        if not self.db_path.exists():
            print("  - Bridge: Creating new SphereOS DB for build...")
            # The constructor of the real system handles initialization.
            system = UnifiedSphereSystem(self.db_path)
        
    def _get_system(self):
        # Helper to get a fresh instance that reads the latest DB file
        return UnifiedSphereSystem(self.db_path)

    def clone_from_sphereos(self, url, target):
        system = self._get_system()
        print(f"🌌 Cloning from SphereOS: {url}")
        path = f"/{url.replace('sphereos://', '')}"
        # --- THIS IS THE FIX ---
        # The database returns raw bytes, so we use them directly.
        source_data = system.retrieve_data_unified("path", path)
        if not source_data:
            print(f"❌ Repo not found in DB: {url}")
            return False
        
        os.makedirs(target, exist_ok=True)
        with tarfile.open(fileobj=io.BytesIO(source_data), mode='r:*') as tar:
            tar.extractall(path=target)
        
        repo_path = str(Path(target).resolve())
        os.chdir(target)
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "config", "--global", "--add", "safe.directory", repo_path], check=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit from SphereOS"], check=True, capture_output=True)
        print(f"✅ Cloned to {target}")
        return True

    def push_to_sphereos(self, source, url):
        system = self._get_system()
        print(f"🌌 Pushing '{source}' to SphereOS URL: {url}")
        path = f"/{url.replace('sphereos://', '')}"
        out = io.BytesIO()
        with tarfile.open(fileobj=out, mode='w:gz') as tar: tar.add(source, arcname='.')
        result = system.store_data_unified(out.getvalue(), "path", path)
        if result.get('success'):
            print("✅ Push successful.")
            return True
        return False

def main():
    if len(sys.argv) < 4:
        print("Usage: SCRIPT <clone|push> <source> <destination>")
        sys.exit(1)
    command, arg1, arg2 = sys.argv[1], sys.argv[2], sys.argv[3]
    bridge = SphereOSGitBridge()
    if command == "clone":
        success = bridge.clone_from_sphereos(url=arg1, target=arg2)
    elif command == "push":
        success = bridge.push_to_sphereos(source=arg1, url=arg2)
    else:
        print(f"Unknown command: {command}"); success = False
    sys.exit(0 if success else 1)
if __name__ == "__main__": main()
'''
    write_file(os.path.join(BUILD_DIR, "sphereos_git_bridge.py"), git_bridge_content)

    bootstrap_content = """#!/usr/bin/env python3
import os, json, time
from SphereOS_Android_Unified import UnifiedSphereSystem
print("🌌 Initializing REAL SphereOS for F-Droid build environment...")
sphere_system = UnifiedSphereSystem("sphereos_build.db")
sphere_system.store_data_unified(json.dumps({"build_system": "f-droid"}).encode(), "path", "/build/metadata")
print("✅ SphereOS build environment is ready.")
"""
    write_file(os.path.join(BUILD_DIR, "bootstrap_sphereos.py"), bootstrap_content)

    # --- Part 5: Create the REAL Build & Distribute Script ---
    print(f"\n[5/5] Creating REAL 'build_and_distribute.sh' file...")
    build_script_content = r"""#!/bin/bash
set -e
echo "🌌 Starting U3CP REAL Self-Distribution Pipeline..."
echo "================================================"
BUILD_DIR="u3cp_fdroid_build"
SPHEREOS_REPO_URL="sphereos://content/repositories/u3cp-android.git"
APP_VERSION="0.1.0"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo -e "\n[Step 1/3] Pushing source code to Local SphereOS Database..."
cd "$SCRIPT_DIR"
python "$BUILD_DIR/sphereos_git_bridge.py" push "$BUILD_DIR" "$SPHEREOS_REPO_URL"
echo "✅ Source code stored in local database."
echo -e "\n[Step 2/3] Running Local F-Droid Build Process..."
BUILD_SERVER_DIR="local_fdroid_server"
rm -rf "$BUILD_SERVER_DIR" && mkdir -p "$BUILD_SERVER_DIR" && cd "$BUILD_SERVER_DIR"
echo "  - Cloning source from local database..."
python3 "$SCRIPT_DIR/$BUILD_DIR/sphereos_git_bridge.py" clone "$SPHEREOS_REPO_URL" "cloned_source"
cd cloned_source || exit 1

echo "  - Verifying build environment..."
if ! command -v buildozer &> /dev/null; then
    echo "  - FATAL ERROR: 'buildozer' not found."
    echo "  - Please install it inside your WSL environment: pip install --user buildozer"
    echo "  - You may also need to install dependencies first. See instructions."
    exit 1
fi

echo "  - Buildozer found. Starting release build..."
# We no longer need Docker, as this script is intended to be run inside a proper Linux (WSL) environment
buildozer android release


echo "✅ APK build process complete."
echo -e "\n[Step 3/3] Verifying build artifact..."
if [ -f "bin/u3cp_node-${APP_VERSION}-release.apk" ]; then
    echo "  - SUCCESS: Release APK found at bin/u3cp_node-${APP_VERSION}-release.apk"
else
    echo "  - FATAL ERROR: Release APK not found after build!" && exit 1
fi
echo -e "\n🎉 =============================================="
echo "✅ U3CP REAL Distribution Pipeline executed successfully!"
echo "================================================"
cd "$SCRIPT_DIR"
"""
    write_file("build_and_distribute.sh", build_script_content)
    os.chmod("build_and_distribute.sh", 0o755)

    print("\n\n--- ✅ REAL Setup Complete! ---")
    print("All mock logic has been removed.")
    print("\nYou can now run the REAL process with one command:")
    print("bash build_and_distribute.sh")

if __name__ == "__main__":
    import sys
    main() 
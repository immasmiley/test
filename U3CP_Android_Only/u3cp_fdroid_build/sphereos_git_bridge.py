#!/usr/bin/env python3
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

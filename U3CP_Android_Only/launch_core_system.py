#!/usr/bin/env python3
"""
U3CP Android-Only CORE System Launcher
This script runs the main background system without the Kivy GUI.
"""

import os
import sys
import time
import uuid
import hashlib

def generate_device_id():
    """Generates a unique, persistent device ID."""
    # Use a combination of sources to create a stable ID
    # In a real app, this might use Android ID, but this is a stable alternative
    try:
        # A simple persistent seed file
        id_seed_path = os.path.join(os.path.dirname(__file__), '.device_id_seed')
        if os.path.exists(id_seed_path):
            with open(id_seed_path, 'r') as f:
                seed = f.read()
        else:
            seed = str(uuid.uuid4())
            with open(id_seed_path, 'w') as f:
                f.write(seed)
        
        # Hash the seed to create the final ID
        return hashlib.sha256(seed.encode()).hexdigest()[:16]
    except Exception as e:
        print(f"[WARNING] Could not generate persistent device ID: {e}")
        print("[INFO] Using a temporary random ID instead.")
        return uuid.uuid4().hex[:16]

def main():
    print("--- U3CP Core System Launcher ---")
    
    # Add the current directory to the Python path to find the module
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    print(f"[*] Adding {current_dir} to path")
    
    try:
        print("[*] Importing U3CPAndroidOnlySystem...")
        # We only import the System, not the App
        from U3CP_Android_Only_System import U3CPAndroidOnlySystem
        print("[+] U3CP system module imported successfully.")

        # Generate the required device_id
        print("[*] Generating device ID...")
        device_id = generate_device_id()
        print(f"[+] Device ID: {device_id}")
        
        # Create an instance of the system
        print("[*] Creating U3CP system instance...")
        system = U3CPAndroidOnlySystem(device_id=device_id)
        print("[+] System instance created.")
        
        # Start the system's core logic
        print("[*] Starting U3CP core services...")
        system.start_integrated_system() # Assuming this method starts background threads/tasks
        print("[+] U3CP core system is now running.")
        
        # Keep the script alive to let background tasks run
        print("\n--- System is active. Press Ctrl+C to stop. ---")
        while True:
            time.sleep(1)
            
    except ImportError as e:
        print(f"\n[ERROR] Failed to import U3CP system: {e}")
        print("[INFO] Make sure 'U3CP_Android_Only_System.py' is in the same directory.")
        return
    except KeyboardInterrupt:
        print("\n[*] Ctrl+C detected. Shutting down the system.")
        # We can add a system.stop() method here if it exists
        if 'system' in locals() and hasattr(system, 'stop_integrated_system'):
            system.stop_integrated_system()
        print("[+] System shut down.")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")
        return

if __name__ == "__main__":
    main() 
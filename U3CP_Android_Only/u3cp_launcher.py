#!/usr/bin/env python3
"""
U3CP Android-Only System Launcher for Termux
"""

import os
import sys
import time
from datetime import datetime

def main():
    print("U3CP Android-Only System Launcher")
    print("=" * 40)
    
    # Add current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    
    try:
        # Import U3CP system
        from U3CP_Android_Only_System import U3CPAndroidOnlySystem
        
        print("U3CP system imported successfully")
        
        # Create and start system
        system = U3CPAndroidOnlySystem()
        print("U3CP system created")
        
        # Start the system
        system.start()
        print("U3CP system started")
        
        # Keep running
        print("U3CP system is now running in Termux")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping U3CP system...")
            system.stop()
            print("U3CP system stopped")
            
    except ImportError as e:
        print(f"Failed to import U3CP system: {e}")
        print("Make sure all U3CP files are in the same directory")
        return False
    except Exception as e:
        print(f"Error running U3CP system: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()

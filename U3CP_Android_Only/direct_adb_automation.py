#!/usr/bin/env python3
"""
Direct ADB F-Droid Automation
Uses direct ADB commands instead of shell script
"""

import subprocess
import time

def execute_adb(command):
    try:
        result = subprocess.run(
            ["./platform-tools/adb.exe"] + command.split(),
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("Direct ADB F-Droid Automation")
    print("=" * 40)
    
    commands = [
        "shell am start -n org.fdroid.fdroid/.views.main.MainActivity",
        "shell sleep 3", 
        "shell am start -a android.intent.action.VIEW -d fdroid://app/org.pydroid3"
    ]
    
    for i, cmd in enumerate(commands, 1):
        print(f"Step {i}: Executing {cmd}")
        success, output, error = execute_adb(cmd)
        
        if success:
            print(f"SUCCESS: Step {i} completed")
        else:
            print(f"ERROR: Step {i} failed: {error}")
    
    print("\nAutomation completed!")
    print("Check your device for F-Droid activity")

if __name__ == "__main__":
    main()

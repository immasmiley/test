import os
import shutil

# --- Configuration ---
SOURCE_DIR = "."
BUILD_DIR = "u3cp_fdroid_build"
ESSENTIAL_FILES = [
    "U3CP_Android_Only_System.py",
    "U3CP_Android_Only_App.py", # The Kivy App is now essential
    "sphereos_android_only.db"  # Include the database
]
# --- End Configuration ---

def main():
    print("--- Preparing F-Droid Build Directory ---")
    
    # Ensure build directory exists and is clean
    if os.path.exists(BUILD_DIR):
        print(f"[*] Removing old build directory: {BUILD_DIR}")
        shutil.rmtree(BUILD_DIR)
    print(f"[*] Creating new build directory: {BUILD_DIR}")
    os.makedirs(BUILD_DIR)
    
    # Copy essential files
    print("[*] Copying essential application files...")
    for filename in ESSENTIAL_FILES:
        source_path = os.path.join(SOURCE_DIR, filename)
        dest_path = os.path.join(BUILD_DIR, filename)
        if os.path.exists(source_path):
            shutil.copy(source_path, dest_path)
            print(f"  - Copied: {filename}")
        else:
            print(f"  - WARNING: Essential file not found: {filename}")
            
    # Create the main.py entry point for Buildozer
    print("[*] Creating main.py entry point...")
    main_py_content = """
from U3CP_Android_Only_App import U3CPAndroidOnlyApp

if __name__ == '__main__':
    U3CPAndroidOnlyApp().run()
"""
    with open(os.path.join(BUILD_DIR, "main.py"), "w") as f:
        f.write(main_py_content)
    print("  - Created: main.py")
    
    print("\n[+] Build directory is ready.")
    print(f"All necessary files are located in: '{BUILD_DIR}'")

if __name__ == "__main__":
    main() 
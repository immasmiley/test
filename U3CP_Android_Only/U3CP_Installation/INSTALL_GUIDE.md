# U3CP Android-Only System - Installation Guide

## Open Source Only - No Google Products Required

This system uses only open source applications and avoids all Google services.

## Quick Installation

### Method 1: Direct Installation (Recommended)
1. Install F-Droid from https://f-droid.org
2. Install Termux from F-Droid
3. Run: `python install.sh` in Termux
4. Start the app: `python U3CP_Android_Only_App.py`

### Method 2: APK Installation
1. Run: `./build_apk.sh`
2. Install the generated APK: `bin/u3cpandroidonly-1.0.0-debug.apk`

### Method 3: Manual Installation
1. Install dependencies: `pip install -r requirements_android_only.txt`
2. Test installation: `python test_android_only.py`
3. Start app: `python U3CP_Android_Only_App.py`

## Requirements
- Android device with Termux (from F-Droid)
- F-Droid installed (open source app store)
- Internet connection for dependency installation
- Network permissions for device discovery

## Features
- Android-to-Android communication
- Nostr relay integration
- SphereOS database
- U3CP algorithm
- Real-time chat and messaging

## Support
Check ANDROID_OPEN_SOURCE_SETUP.md for detailed Android setup
Check README_Android_Only.md for detailed documentation

## Privacy & Security
- No Google Play Store required
- No Google services used
- All apps are open source
- Local network only
- No tracking or analytics

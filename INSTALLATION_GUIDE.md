# U3CP Enhanced Self-Distribution Installation Guide

## Quick Start (Windows with WSL)

### 1. Install WSL (One-time setup)
```powershell
# Run in PowerShell as Administrator
wsl --install
# Restart computer when prompted
```

### 2. Setup Build Environment (One-time setup)
```bash
# Open Ubuntu from Start Menu
# Update system
sudo apt update && sudo apt upgrade -y

# The build script will install all dependencies automatically
```

### 3. Build the Application
```bash
# Navigate to project directory (adjust path as needed)
cd "/mnt/j/SphereOS Consolidation/U3CP_Android_Only"

# Run enhanced build script
bash build_enhanced_wsl.sh
```

### 4. Install on Android Device
```bash
# Connect Android device with USB debugging enabled
adb install u3cp_fdroid_build/bin/u3cp_enhanced-0.1.0-debug.apk
```

## Features Included

✅ **Autonomous Network Formation**
- Devices automatically discover each other via GPS proximity
- Self-organizing mesh topology
- No infrastructure required

✅ **Self-Healing Capabilities**
- Applications monitor their own health
- Automatic repair of corrupted components
- Network-wide redundancy and recovery

✅ **Embedded Distribution**
- Each device carries its own installer
- Viral spreading through proximity sharing
- No app store dependency

✅ **Advanced Communication**
- U3CP 3-channel protocol for collision-free networking
- SphereOS distributed database with git-like versioning
- Nostr relay for decentralized messaging

✅ **Privacy & Security**
- GPS sharing is device-controlled and opt-in
- All communication encrypted and verifiable
- No centralized servers or tracking

## Troubleshooting

**Buildozer Issues:**
- Ensure you're running in WSL/Linux environment
- Check that Java 17 is installed: `java -version`
- Clear buildozer cache: `buildozer android clean`

**Device Connection:**
- Enable Developer Options on Android
- Enable USB Debugging
- Install ADB: `sudo apt install android-tools-adb`

**Build Failures:**
- Check available disk space (builds require ~5GB)
- Ensure stable internet connection for downloads
- Review build logs for specific error messages

## Advanced Usage

**Testing Self-Distribution:**
1. Install on multiple devices
2. Enable GPS and location permissions
3. Bring devices within 1km of each other
4. Use "Share App" feature to test distribution

**Monitoring Network Health:**
- Open app and check "System Health" section
- Monitor device proximity and connections
- Watch autonomous healing in action

**Emergency Deployment:**
- Single device can bootstrap entire network
- Rapid deployment through proximity sharing
- Works offline after initial network formation

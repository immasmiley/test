# Android Open Source Setup Guide

## No Google Play Store Required

This guide uses only open source applications available through F-Droid.

## Step 1: Install F-Droid

1. **Download F-Droid** from https://f-droid.org
2. **Enable "Install from unknown sources"** in Android settings
3. **Install F-Droid APK** on your device
4. **Open F-Droid** and update the repository

## Step 2: Install Termux

1. **Open F-Droid** on your Android device
2. **Search for "Termux"**
3. **Install Termux** (terminal emulator with Python)
4. **Grant storage permissions** to Termux

## Step 3: Setup Python Environment

1. **Open Termux**
2. **Update package list**:
   ```bash
   pkg update
   ```

3. **Install Python and tools**:
   ```bash
   pkg install python git wget curl
   ```

4. **Verify Python installation**:
   ```bash
   python --version
   ```

## Step 4: Download U3CP System

1. **Scan QR code** from desktop wireless installer
2. **Download installation files** from web page
3. **Extract files** in Termux:
   ```bash
   unzip U3CP_Complete_Package.zip
   ```

## Step 5: Install and Run

1. **Run installation script**:
   ```bash
   python install.sh
   ```

2. **Test installation**:
   ```bash
   python test_android_only.py
   ```

3. **Start U3CP system**:
   ```bash
   python U3CP_Android_Only_App.py
   ```

## Alternative: Manual Installation

If automatic installation fails:

1. **Install dependencies manually**:
   ```bash
   pip install kivy==2.2.1 kivymd==1.1.1 websockets==11.0.3 requests urllib3
   ```

2. **Run system directly**:
   ```bash
   python U3CP_Android_Only_System.py
   ```

## Additional Open Source Apps

### QR Code Scanner
- **QR & Barcode Scanner** (F-Droid)
- **Barcode Scanner** (F-Droid)

### File Manager
- **Amaze File Manager** (F-Droid)
- **Material Files** (F-Droid)

### Network Tools
- **Network Scanner** (F-Droid)
- **Fing** (F-Droid)

## Privacy & Security

- **No Google services required**
- **No tracking or analytics**
- **All apps are open source**
- **Local network only**

## Troubleshooting

### Termux Issues
- **Permission denied**: Grant storage permissions
- **Python not found**: Run `pkg install python`
- **Network issues**: Check Termux network permissions

### Installation Issues
- **Dependencies fail**: Install manually with `pip install`
- **Kivy issues**: Install system dependencies first
- **Port conflicts**: Check if ports 8081-8082 are available

## Network Requirements

- **Same WiFi network** as desktop
- **Network discovery enabled**
- **Firewall allows local connections**
- **No internet required** for operation

Generated for open source Android deployment

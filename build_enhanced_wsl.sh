#!/bin/bash

echo "🌌 U3CP Enhanced Self-Distribution Build Script"
echo "=============================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install buildozer dependencies
install_dependencies() {
    echo "📦 Installing build dependencies..."
    
    # Update package lists
    sudo apt update
    
    # Install core dependencies
    sudo apt install -y \
        git zip unzip openjdk-17-jdk python3-pip python3-venv \
        autoconf libtool pkg-config zlib1g-dev \
        libncurses5-dev libncursesw5-dev libtinfo5 \
        cmake libffi-dev libssl-dev build-essential \
        ccache
    
    # Install Python dependencies
    pip3 install --user --upgrade pip setuptools wheel
    pip3 install --user --upgrade buildozer cython==0.29.33
    
    # Add local bin to PATH
    export PATH="$HOME/.local/bin:$PATH"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    
    echo "✅ Dependencies installed"
}

# Function to setup Android SDK environment
setup_android_env() {
    echo "🤖 Setting up Android build environment..."
    
    # Accept all Android SDK licenses
    yes | buildozer android update
    
    echo "✅ Android environment configured"
}

# Function to build APK
build_apk() {
    echo "🔨 Building U3CP Enhanced APK..."
    
    cd u3cp_fdroid_build || {
        echo "❌ Build directory not found"
        exit 1
    }
    
    # Clean previous builds
    buildozer android clean
    
    # Build debug APK
    echo "📱 Building debug APK..."
    buildozer android debug
    
    # Check if build succeeded
    if [ -f "bin/u3cp_enhanced-0.1.0-debug.apk" ]; then
        echo "✅ Debug APK built successfully!"
        echo "📱 Location: u3cp_fdroid_build/bin/u3cp_enhanced-0.1.0-debug.apk"
        
        # Build release APK
        echo "📦 Building release APK..."
        buildozer android release
        
        if [ -f "bin/u3cp_enhanced-0.1.0-release.apk" ]; then
            echo "✅ Release APK built successfully!"
            echo "📦 Location: u3cp_fdroid_build/bin/u3cp_enhanced-0.1.0-release.apk"
            
            # Show APK information
            echo ""
            echo "📊 Build Summary:"
            echo "  Debug APK:   $(du -h bin/u3cp_enhanced-0.1.0-debug.apk | cut -f1)"
            echo "  Release APK: $(du -h bin/u3cp_enhanced-0.1.0-release.apk | cut -f1)"
            echo ""
            echo "🚀 Ready for self-distribution!"
            
        else
            echo "⚠️ Release build failed, but debug APK is available"
        fi
        
    else
        echo "❌ APK build failed!"
        echo "Check the build logs above for errors"
        exit 1
    fi
}

# Function to setup self-distribution
setup_self_distribution() {
    echo "🚀 Setting up self-distribution capabilities..."
    
    if [ -f "u3cp_fdroid_build/bin/u3cp_enhanced-0.1.0-debug.apk" ]; then
        # Create distribution directory
        mkdir -p distribution
        
        # Copy APK for distribution
        cp u3cp_fdroid_build/bin/u3cp_enhanced-0.1.0-debug.apk distribution/
        
        # Create distribution metadata
        cat > distribution/metadata.json << EOF
{
    "app_name": "U3CP Enhanced Node",
    "version": "0.1.0",
    "package_name": "org.sphereos.u3cp",
    "build_timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "self_distribution_enabled": true,
    "autonomous_healing_enabled": true,
    "capabilities": [
        "proximity_networking",
        "gps_distance_calculation", 
        "embedded_installer_sharing",
        "self_repair_mechanisms",
        "sphereos_integration",
        "nostr_relay"
    ]
}
EOF
        
        echo "✅ Self-distribution package created in ./distribution/"
        
    else
        echo "❌ No APK found for distribution setup"
    fi
}

# Function to test installation
test_installation() {
    echo "🧪 Testing installation..."
    
    if command_exists adb; then
        echo "📱 ADB found - checking for connected devices..."
        
        # Check for connected Android devices
        devices=$(adb devices | grep -v "List of devices" | grep "device$" | wc -l)
        
        if [ "$devices" -gt 0 ]; then
            echo "📱 Found $devices connected device(s)"
            echo "🔧 To install: adb install u3cp_fdroid_build/bin/u3cp_enhanced-0.1.0-debug.apk"
        else
            echo "📱 No devices connected via ADB"
            echo "💡 Connect an Android device with USB debugging enabled to test installation"
        fi
    else
        echo "📱 ADB not installed - install android-tools-adb for device testing"
    fi
}

# Main execution
main() {
    echo "Starting U3CP Enhanced build process..."
    
    # Check if we're in WSL/Linux
    if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ -n "$WSL_DISTRO_NAME" ]]; then
        echo "✅ Linux/WSL environment detected"
    else
        echo "❌ This script requires Linux or WSL environment"
        echo "💡 Please run from Ubuntu WSL or Linux terminal"
        exit 1
    fi
    
    # Check if buildozer is installed
    if ! command_exists buildozer; then
        echo "📦 Buildozer not found - installing dependencies..."
        install_dependencies
    else
        echo "✅ Buildozer found"
    fi
    
    # Setup Android environment
    setup_android_env
    
    # Build APK
    build_apk
    
    # Setup self-distribution
    setup_self_distribution
    
    # Test installation capabilities
    test_installation
    
    echo ""
    echo "🎉 U3CP Enhanced Build Complete!"
    echo "================================================"
    echo ""
    echo "📱 Your self-distributing, autonomous healing communication network is ready!"
    echo ""
    echo "Next steps:"
    echo "  1. Install on devices: adb install u3cp_fdroid_build/bin/u3cp_enhanced-0.1.0-debug.apk"
    echo "  2. Enable GPS and network permissions"
    echo "  3. Let devices discover each other via proximity"
    echo "  4. Watch the autonomous network form and heal itself!"
    echo ""
}

# Run main function
main "$@"

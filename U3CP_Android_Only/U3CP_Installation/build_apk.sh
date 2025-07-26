#!/bin/bash
# Build APK for U3CP Android-Only System
# Open Source Only - No Google products required

echo "Building APK..."

# Install buildozer if not available
if ! command -v buildozer &> /dev/null; then
    echo "Installing buildozer..."
    pip install buildozer
fi

# Build APK
buildozer android debug

echo "APK built successfully!"
echo "APK location: bin/u3cpandroidonly-1.0.0-debug.apk"
echo "Open Source Only - No Google products required"

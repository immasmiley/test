#!/bin/bash
set -e
echo "🌌 Starting U3CP REAL Self-Distribution Pipeline..."
echo "================================================"
BUILD_DIR="u3cp_fdroid_build"
SPHEREOS_REPO_URL="sphereos://content/repositories/u3cp-android.git"
APP_VERSION="0.1.0"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo -e "\n[Step 1/3] Pushing source code to Local SphereOS Database..."
cd "$SCRIPT_DIR"
python "$BUILD_DIR/sphereos_git_bridge.py" push "$BUILD_DIR" "$SPHEREOS_REPO_URL"
echo "✅ Source code stored in local database."
echo -e "\n[Step 2/3] Running Local F-Droid Build Process..."
BUILD_SERVER_DIR="local_fdroid_server"
rm -rf "$BUILD_SERVER_DIR" && mkdir -p "$BUILD_SERVER_DIR" && cd "$BUILD_SERVER_DIR"
echo "  - Cloning source from local database..."
python "$SCRIPT_DIR/$BUILD_DIR/sphereos_git_bridge.py" clone "$SPHEREOS_REPO_URL" "cloned_source"
cd cloned_source
echo "  - Verifying build environment..."
if ! command -v buildozer &> /dev/null; then
    echo "  - FATAL ERROR: 'buildozer' not found. Please install via: pip install buildozer"
    exit 1
fi
echo "  - Buildozer found. Starting release build..."
buildozer android release
echo "✅ APK build process complete."
echo -e "\n[Step 3/3] Verifying build artifact..."
if [ -f "bin/u3cp_node-${APP_VERSION}-release.apk" ]; then
    echo "  - SUCCESS: Release APK found at bin/u3cp_node-${APP_VERSION}-release.apk"
else
    echo "  - FATAL ERROR: Release APK not found after build!" && exit 1
fi
echo -e "\n🎉 =============================================="
echo "✅ U3CP REAL Distribution Pipeline executed successfully!"
echo "================================================"
cd "$SCRIPT_DIR"

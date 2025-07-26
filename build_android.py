#!/usr/bin/env python3
"""
Buildozer configuration and build script for SphereOS Android app
Optimized for old Android phones
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_buildozer_spec():
    """Create buildozer.spec configuration file"""
    
    buildozer_spec = """[app]

# (str) Title of your application
title = SphereOS Unified

# (str) Package name
package.name = sphereos_unified

# (str) Package domain (needed for android/ios packaging)
package.domain = org.sphereos

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,db

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 1.0.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.2.1,sqlite3

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#

#
# author = © Copyright Info

# change the major version of python used by the app
osx.python_version = 3

# Kivy version to use
osx.kivy_version = 1.9.1

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
#android.presplash_color = #FFFFFF

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 21

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 21

# (str) Android NDK version to use
android.ndk = 23b

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
# android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only. If set to False,
# the default, you will be shown the license when first running
# buildozer.
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Android Activity
# use that parameter together with android.entrypoint to set custom Java class instead of PythonActivity
#android.activity_class_name = org.kivy.android.PythonActivity

# (str) Extra xml to write directly inside the <manifest> element of AndroidManifest.xml
# use that parameter to provide a filename from where to load your custom XML code
#android.extra_manifest_xml = ./src/android/extra_manifest.xml

# (str) Extra xml to write directly inside the <manifest><application> tag of AndroidManifest.xml
# use that parameter to provide a filename from where to load your custom XML arguments:
#android.extra_manifest_application_arguments = ./src/android/extra_manifest_application_arguments.xml

# (list) Pattern to whitelist for the whole project
#android.whitelist =

# (str) Path to a custom whitelist file
#android.whitelist_src =

# (str) Path to a custom blacklist file
#android.blacklist_src =

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, for example:
# OUYA-ODK/libs/*.jar
#android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
#android.add_src =

# (list) Android AAR archives to add
#android.add_aars =

# (list) Put these files or directories in the apk assets directory.
# Either form may be used, and assets need not be in 'source.include_exts'.
# 1) android.add_assets = source_asset_relative_path
# 2) android.add_assets = source_asset_path:target_asset_relative_path
#android.add_assets =

# (list) Put these files or directories in the apk res directory.
# The option may be used in three ways, the value may contain one or zero ':'
# Some examples:
# 1) A file to add to resources, legal resource names contain ['a-z','0-9','_']
# android.add_resources = my_icons/all-inclusive.png:drawable/all_inclusive.png
# 2) A directory, here  'legal_icons' must contain resources of one kind
# android.add_resources = legal_icons:drawable
# 3) A directory, here 'legal_resources' must contain one or more directories, 
# each of a resource kind
# android.add_resources = legal_resources
#android.add_resources =

# (list) Put these files or directories in the apk libs/armeabi directory
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/android-v7/*.so
#android.add_libs_arm64_v8a = libs/android-v8/*.so
#android.add_libs_x86 = libs/android-x86/*.so
#android.add_libs_mips = libs/android-mips/*.so

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
# android.wakelock = False

# (list) Android application meta-data to set (key=value format)
#android.meta_data =

# (list) Android library project to add (will be added in the
# project.properties automatically.)
#android.library_references =

# (list) Android shared libraries which will be added to AndroidManifest.xml using <uses-library> tag
#android.uses_library =

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Android logcat only display log for activity's pid
#android.logcat_pid_only = False

# (str) Android additional adb arguments
#android.adb_args = -H host.docker.internal

# (bool) Copy library instead of making a libs symlink
#android.copy_libs = 1

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# In past, was `android.arch` as we weren't supporting builds for multiple archs at the same time.
android.archs = armeabi-v7a, arm64-v8a

# (int) overrides automatic versionCode computation (used in build.gradle)
# this is not the same as app version and should only be edited if you know what you're doing
# android.numeric_version = 1

#
# Python for android (p4a) specific
#

# (str) python-for-android URL to use for checkout
#p4a.url =

# (str) python-for-android fork to use in case if p4a.url is not specified, defaults to upstream (kivy)
#p4a.fork = kivy

# (str) python-for-android branch to use, defaults to master
#p4a.branch = master

# (str) python-for-android specific commit to use, defaults to HEAD, must be within p4a.branch
#p4a.commit = HEAD

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
#p4a.source_dir =

# (str) The directory in which python-for-android should look for your own build recipes (if any)
#p4a.local_recipes =

# (str) Filename to the hook for p4a
#p4a.hook =

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (int) port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
#p4a.port =

#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_dir = ../kivy-ios
# Alternately, specify the URL and branch of a git checkout:
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

# Another platform dependency: ios-deploy
# Uncomment to use a custom checkout
#ios.ios_deploy_dir = ../ios_deploy
# Or specify URL and branch
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.7.0

# (bool) Whether or not to sign the code
ios.codesign.identity = iPhone Developer: <lastname> <firstname> (<hexstring>)

# (str) The name of the provisioning profile to use for signing the app (can be verified in your Apple Developer account)
#ios.provisioning_profile = 

# (str) Path to the certificate to use for signing the app
#ios.certificate = 

# (str) Path to the certificate password
#ios.certificate_password = 

# (str) Path to the push notification certificate
#ios.push_certificate = 

# (str) Push notification certificate password
#ios.push_certificate_password = 

# (list) List of custom plist files to be included in the app bundle
#ios.info_plist_list = 

# (list) List of custom entitlements to be included in the app bundle
#ios.entitlements_list = 

#
# Apple TV specific
#

# (str) Path to the icon
#tvos.icon.filename = %(source.dir)s/icon.png

# (str) Path to the top level app directory
#tvos.app_dir = %(source.dir)s

# (str) Application name
#tvos.app_name = %(source.dir)s

# (str) Application version
#tvos.version = 1.0

# (str) Application bundle identifier
#tvos.bundle_identifier = org.test

# (str) Path to the entitlements file
#tvos.entitlements = %(source.dir)s/entitlements.plist

# (str) Path to the Info.plist file
#tvos.info_plist = %(source.dir)s/Info.plist

# (str) Path to the main file
#tvos.main_file = %(source.dir)s/main.py

# (str) Path to the provisioning profile
#tvos.provisioning_profile = %(source.dir)s/profile.mobileprovision

# (str) Team identifier
#tvos.team_identifier = 

# (str) Apple TV platform to build for (choices: appletvos, appletvsimulator)
#tvos.platform = appletvos

# (int) Apple TV SDK version to build for
#tvos.deployment_target = 9.0

# (bool) Indicate if the application should be fullscreen or not
#tvos.fullscreen = 1

# (bool) Indicate if the application should support the Apple TV remote
#tvos.remote_support = 1

#
# tvOS specific
#

# (str) Path to the icon
#tvos.icon.filename = %(source.dir)s/icon.png

# (str) Path to the top level app directory
#tvos.app_dir = %(source.dir)s

# (str) Application name
#tvos.app_name = %(source.dir)s

# (str) Application version
#tvos.version = 1.0

# (str) Application bundle identifier
#tvos.bundle_identifier = org.test

# (str) Path to the entitlements file
#tvos.entitlements = %(source.dir)s/entitlements.plist

# (str) Path to the Info.plist file
#tvos.info_plist = %(source.dir)s/Info.plist

# (str) Path to the main file
#tvos.main_file = %(source.dir)s/main.py

# (str) Path to the provisioning profile
#tvos.provisioning_profile = %(source.dir)s/profile.mobileprovision

# (str) Team identifier
#tvos.team_identifier = 

# (str) Apple TV platform to build for (choices: appletvos, appletvsimulator)
#tvos.platform = appletvos

# (int) Apple TV SDK version to build for
#tvos.deployment_target = 9.0

# (bool) Indicate if the application should be fullscreen or not
#tvos.fullscreen = 1

# (bool) Indicate if the application should support the Apple TV remote
#tvos.remote_support = 1

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin

#    -----------------------------------------------------------------------------
#    List as sections
#
#    You can define all the "list" as [section:key].
#    Each line will be considered as a option to the list.
#    Let's take [app] / source.exclude_patterns.
#    Instead of doing:
#
#[app]
#source.exclude_patterns = license,data/audio/*.wav,data/images/original/*
#
#    This can be translated into:
#
#[app:source.exclude_patterns]
#license
#data/audio/*.wav
#data/images/original/*
#

#    -----------------------------------------------------------------------------
#    Profiles
#
#    You can extend section / key with a profile
#    For example, you want to deploy a demo version of your application without
#    HD content. You could first change the title to add "(demo)" in the name
#    and extend the excluded directories to remove the HD content.
#
#[app@demo]
#title = My Application (demo)
#
#[app:source.exclude_patterns@demo]
#images/hd/*
#
#    Then, invoke the command line with the "demo" profile:
#
#buildozer --profile demo android debug
"""
    
    with open('buildozer.spec', 'w') as f:
        f.write(buildozer_spec)
    
    print("✅ Created buildozer.spec configuration file")

def install_buildozer():
    """Install buildozer if not already installed"""
    try:
        import buildozer
        print("✅ Buildozer already installed")
        return True
    except ImportError:
        print("📦 Installing buildozer...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'buildozer'], check=True)
            print("✅ Buildozer installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install buildozer: {e}")
            return False

def build_android_apk():
    """Build Android APK using buildozer"""
    print("🔨 Building Android APK...")
    
    try:
        # Run buildozer android debug
        result = subprocess.run(['buildozer', 'android', 'debug'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Android APK built successfully!")
            print("📱 APK location: bin/sphereos_unified-1.0.0-debug.apk")
            return True
        else:
            print(f"❌ Build failed: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ Buildozer not found. Please install it first.")
        return False
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def main():
    """Main build process"""
    print("🚀 SphereOS Android Build Process")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('SphereOS_Android_Unified.py'):
        print("❌ SphereOS_Android_Unified.py not found in current directory")
        print("Please run this script from the directory containing the main app file")
        return
    
    # Create buildozer.spec
    create_buildozer_spec()
    
    # Install buildozer if needed
    if not install_buildozer():
        print("❌ Cannot proceed without buildozer")
        return
    
    # Build the APK
    if build_android_apk():
        print("\n🎉 Build completed successfully!")
        print("\nNext steps:")
        print("1. Transfer the APK to your Android device")
        print("2. Enable 'Install from unknown sources' in Android settings")
        print("3. Install the APK on your device")
        print("4. Launch SphereOS Unified!")
    else:
        print("\n❌ Build failed. Check the error messages above.")

if __name__ == "__main__":
    main() 
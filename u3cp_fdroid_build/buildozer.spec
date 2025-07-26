[app]

# Basic app information
title = U3CP Enhanced Node
package.name = u3cp_enhanced
package.domain = org.sphereos.u3cp

# Source configuration  
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,json,txt,md
source.exclude_dirs = tests, bin, venv, .buildozer, __pycache__

# App version
version = 0.1.0

# Requirements - enhanced for self-distribution
requirements = python3,kivy==2.2.1,sqlite3,websockets,asyncio,zlib,hashlib,json,threading,datetime,pathlib,base64,math,random

# App metadata
author = U3CP Development Team
description = Autonomous self-healing communication network with embedded distribution

# Android configuration
orientation = portrait
fullscreen = 0

# Enhanced permissions for self-distribution
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,WAKE_LOCK,CAMERA,RECORD_AUDIO,ACCESS_NETWORK_STATE,USB_PERMISSION,INSTALL_PACKAGES,REQUEST_INSTALL_PACKAGES

# Android API settings - optimized for older devices
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# Architecture support for wide compatibility
android.archs = arm64-v8a, armeabi-v7a

# Keep app running for network node functionality
android.wakelock = True

# Bootstrap and build settings
p4a.bootstrap = sdl2
p4a.branch = master

[buildozer]

# Build settings
log_level = 2
warn_on_root = 1

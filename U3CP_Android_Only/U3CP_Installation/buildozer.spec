[app]
title = U3CP Android-Only System
package.name = u3cpandroidonly
package.domain = org.u3cp.androidonly
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt,md
version = 1.0.0

requirements = python3,kivy==2.2.1,kivymd==1.1.1,websockets==11.0.3,requests==2.31.0,urllib3==2.0.7,qrcode,pillow

orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
android.api = 21
android.minapi = 21
android.ndk = 23b
android.sdk = 33
android.arch = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1

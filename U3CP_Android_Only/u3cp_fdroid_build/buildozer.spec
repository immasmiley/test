[app]
title = U3CP Network Node
package.name = u3cp_node
package.domain = org.sphereos.u3cp
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,json,txt,md
requirements = python3,kivy==2.2.1,sqlite3,websockets,asyncio,cryptography,qrcode,zlib,hashlib,json,threading,datetime,dataclasses,enum,pathlib,base64,math,random
version = 0.1.0
author = U3CP Development Team
description = Distributed communication network using 3-channel protocol
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,WAKE_LOCK,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION
android.api = 28
android.minapi = 21
android.archs = armeabi-v7a, arm64-v8a
android.wakelock = True
[buildozer]
log_level = 2

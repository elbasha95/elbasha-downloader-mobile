[app]
title = Elbasha Downloader
package.name = elbashadownloader
package.domain = org.elbasha
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 1.0.0
requirements = python3,kivy==2.3.1,yt-dlp,requests
orientation = portrait

[buildozer]
log_level = 2

[android]
android.api = 31
android.minapi = 21
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE
android.archs = arm64-v8a
android.accept_sdk_license = True

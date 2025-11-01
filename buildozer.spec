[app]
title = Elbasha Downloader
package.name = elbashadownloader
package.domain = org.elbasha
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 1.0.0
requirements = python3,kivy==2.3.1,yt-dlp,requests
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b
android.accept_sdk_license = True
android.skip_update = False
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE
android.archs = arm64-v8a,armeabi-v7a
android.entrypoint = org.kivy.android.PythonActivity
android.apptheme = @android:style/Theme.NoTitleBar
android.copy_libs = 1
p4a.bootstrap = sdl2
android.gradle_dependencies =
android.add_gradle_repositories =

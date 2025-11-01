[app]

# Application title
title = Elbasha Downloader

# Package name
package.name = elbashadownloader

# Package domain (for Android)
package.domain = org.elbasha

# Source code directory
source.dir = .

# Source files to include
source.include_exts = py,png,jpg,kv,atlas,ttf

# Application version
version = 1.0.0

# Application requirements - SIMPLIFIED FOR ANDROID
requirements = python3,kivy==2.3.1,yt-dlp,requests

# Supported orientations
orientation = portrait

# Enable fullscreen
fullscreen = 0

# Presplash background color
#presplash.filename = %(source.dir)s/presplash.png

# Icon filename
#icon.filename = %(source.dir)s/icon.png

# Permissions and features
#permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Buildozer settings
[buildozer]
log_level = 2
warn_on_root = 1

# Android settings
[android]

# Android API version (use 31 to avoid compatibility issues)
android.api = 31

# Minimum API version
android.minapi = 21

# Android SDK version
android.sdk = 31

# Android NDK version
android.ndk = 25b

# Accept SDK license automatically
android.accept_sdk_license = True

# Skip update of Android SDK/NDK (Let Buildozer handle everything)
android.skip_update = False

# Android permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE

# Android architectures (support 64-bit and 32-bit)
android.archs = arm64-v8a,armeabi-v7a

# Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# Android app theme
android.apptheme = @android:style/Theme.NoTitleBar

# Don't copy libs
android.copy_libs = 1

# Bootstrap
p4a.bootstrap = sdl2

# Gradle dependencies (leave empty - not needed)
android.gradle_dependencies =

# Add Java options (leave empty - not needed)
android.add_gradle_repositories =

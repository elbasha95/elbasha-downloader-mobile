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

# Application requirements
# Note: ffmpeg is handled via p4a recipe, yt-dlp works without ffmpeg on Android for most videos
requirements = python3,kivy==2.3.1,yt-dlp,requests,pyjnius,android

# Supported orientations
orientation = portrait

# Enable fullscreen
fullscreen = 0

# Presplash background color
#presplash.filename = %(source.dir)s/presplash.png

# Icon filename
#icon.filename = %(source.dir)s/icon.png

# Android specific settings
[buildozer]
log_level = 2
warn_on_root = 1

[android]
# Android API version
android.api = 31

# Minimum API version
android.minapi = 21

# Android SDK version
android.sdk = 31

# Android NDK version
android.ndk = 25b

# Accept SDK license automatically
android.accept_sdk_license = True

# Android permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE

# Android architectures
android.archs = arm64-v8a,armeabi-v7a

# Skip update of Android SDK/NDK
android.skip_update = False

# Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# Android app theme
android.apptheme = "@android:style/Theme.NoTitleBar"

# Don't copy libs
android.copy_libs = 1

# Gradle dependencies
android.gradle_dependencies =

# Add Java options
android.add_gradle_repositories =

# Bootstrap
p4a.bootstrap = sdl2

# python-for-android directory
#p4a.source_dir =

# python-for-android recipe
#p4a.local_recipes =

# python-for-android hook
#p4a.hook =

# python-for-android port
#p4a.port =

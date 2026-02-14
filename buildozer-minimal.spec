[app]
title = AntiGravity AI
package.name = antigravityai
package.domain = com.antigravity
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0

# Minimal requirements for testing
requirements = python3,kivy==2.3.1,kivymd==1.2.0,pillow,requests,setuptools

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 29
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

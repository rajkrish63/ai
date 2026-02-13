[app]

# (str) Title of your application
title = AntiGravity AI

# (str) Package name
package.name = antigravityai

# (str) Package domain (needed for android/ios packaging)
package.domain = com.antigravity

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json,onnx,tflite

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

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.3.1,kivymd==1.2.0,numpy,onnxruntime==1.17.0,tokenizers,pillow,requests,flatbuffers,protobuf,pyjnius,vosk,pypdf2,python-docx

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
#android.presplash_color = #FFFFFF

# (string) Presplash animation using Lottie format.
# see https://lottiefiles.com/ for examples and https://airbnb.io/lottie/
# for documentation.
# Lottie layout icon must be one of the following values:
# center, aspectFill, aspectFit, width, height, scaleDown
#android.presplash_lottie = "path/to/lottie/file.json"

# (string) Presplash lottie image
# from the lottie file, often called "images" or "assets"
#android.presplash_lottie_image = "path/to/lottie/images"

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,RECORD_AUDIO,CAMERA

# (int) Target Android API, should be as high as possible (distutils)
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 29

# (int) Android SDK version to use
#android.sdk = 20

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess internet downloads or save time
# when an update is due and you just want to test/build your package
# android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only. If set to False,
# the default, you will be shown the license when first running
# buildozer.
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme, default is ok for Kivy-based app
# android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) Pattern to exclude from the compilation. This is strictly a
# glob pattern, so it matches file from the source directory.
#android.whitelist =

# (str) Path to a custom whitelist file
#android.whitelist_src =

# (str) Path to a custom blacklist file
#android.blacklist_src =

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, for example:
# OUYA-ODK/libs/*.jar
#android.add_jars = foo.jar,bar.jar,common/acra.jar,./libs/*.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
#android.add_src =

# (list) Android AAR archives to add
#android.add_aars =

# (list) Put these files or directories in the apk assets directory.
# Either form may be used, and they may be used simultaneously.
# at least one entry must be present - android.assets_path is deprecated
#android.add_assets = assets

# (list) Gradle dependencies to add
android.gradle_dependencies = com.google.mlkit:text-recognition:16.0.0

# (bool) Enable AndroidX support. Enable when 'android.gradle_dependencies'
# contains an 'androidx' package, or any package that depends on AndroidX.
#android.enable_androidx = True

# (list) Add java compile options
# this can for example be necessary when importing certain java libraries using the 'android.gradle_dependencies' option
# see https://developer.android.com/studio/write/java8-support for more information
# android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"

# (list) Gradle repositories to add {can be necessary for some android.gradle_dependencies}
# please enclose in double quotes 
#android.gradle_repositories = "maven { url 'https://jitpack.io' }"

# (list) Packaging options
#android.packaging_options = "exclude 'META-INF/common.kotlin_module'", "exclude 'META-INF/*.kotlin_module'"

# (list) Java classes to add as activities to the manifest 
#android.add_activities = com.example.ExampleActivity

# (str) OUYA Console category. Should be one of GAME or APP
# The default is GAME, but it is better to set this explicitly.
#ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
#android.manifest.intent_filters =

# (str) launchMode to set for the main activity
#android.manifest.launch_mode = standard

# (list) Android additional libraries to copy into libs/armeabi
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/android-v7/*.so
#android.add_libs_arm64_v8a = libs/android-v8/*.so
#android.add_libs_x86 = libs/android-x86/*.so
#android.add_libs_mips = libs/android-mips/*.so

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
#android.wakelock = False

# (list) Android application meta-data to set (key=value format)
#android.meta_data =

# (list) Android library project to add (will be added in the
# project.properties automatically.)
#android.library_references =

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = arm64-v8a

# (int) overrides automatic number of workers used to build the apk
#android.numeric_workers = 1

# (bool) enable/disable debug symbols for native libraries
#android.debug_symbols = True

# (bool) enable/disable build of gdbserver
#android.build_gdbserver = True

# (bool) enable/disable build of python with a custom user config
#android.python_use_custom_config = False

# (str) Custom python user config (path to the config.site file)
#android.python_custom_config_path = 

# (str) The directory in which the python-for-android build takes place.
# If this isn't provided, the build takes place in the buildozer directory
# p4a.build_dir = 

# (str) The directory in which the python-for-android distribution is installed
# If this isn't provided, it is installed in the buildozer directory
# p4a.dist_dir = 

# (str) The directory in which python-for-android should look for some recipes.
# p4a.local_recipes = ./p4a_recipes

# (str) The directory in which python-for-android should look for some docutils.
# p4a.hook = ./p4a_hooks

# (str) Filename of the hook to run when the compilation finishes
#p4a.post_build_hook =

# (str) Filename of the hook to run when the compilation starts
#p4a.pre_build_hook =

# (str) Path to the user-supplied recipes (if any)
#p4a.local_recipes =

# (str) Path to the custom python-for-android fork
#p4a.fork =

# (str) Branch of the custom python-for-android fork
#p4a.branch = master

# (str) Path to the custom python-for-android remote
#p4a.remote = https://github.com/kivy/python-for-android

# (list) List of modules to exclude from the python-for-android build
#p4a.exclude_modules = 

# (list) List of modules to include in the python-for-android build
#p4a.include_modules = 

# (list) List of site-packages to include in the python-for-android build
#p4a.include_site_packages = 

# (list) List of python packages to install
#p4a.install_requires = 

# (list) List of python packages to install in the python-for-android build
#p4a.requirements =

#
# Python for android (p4a) specific
#

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
#p4a.source_dir =

# (str) The directory where python-for-android should look for your own recipes
#p4a.local_recipes =

# (str) Filename to the hook for the new python-for-android toolchain
#p4a.hook =

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (int) port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
#p4a.port =


#
# iOS specific
#

# (str) Path to the custom kivy-ios folder
#ios.kivy_ios_dir = ../kivy-ios
# Alternately, specify the URL and branch of a git checkout:
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: security find-identity -v -p codesigning
#ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) Name of the certificate to use for signing the release version
#ios.codesign.release = %(ios.codesign.debug)s


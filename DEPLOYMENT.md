# AntiGravity AI - Deployment Guide

## Prerequisites

### System Requirements
- **OS**: Linux (Ubuntu 20.04+ recommended) or WSL2 on Windows
- **Python**: 3.11
- **Java**: JDK 17 or higher
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 20GB free space for Android SDK/NDK

### Install Dependencies

#### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install -y python3-pip git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

#### On Windows (WSL2):
1. Install WSL2 with Ubuntu 20.04+
2. Follow Ubuntu instructions above

## Installation

### 1. Install Buildozer
```bash
pip install --upgrade buildozer
pip install --upgrade cython
```

### 2. Install Project Dependencies
```bash
cd c:\dev\Ai  # or your project path
pip install -r requirements.txt
```

## Building the APK

### First-Time Build
```bash
# Clean any previous builds (optional)
buildozer android clean

# Build debug APK
buildozer android debug
```

**Note**: First build will take 30-60 minutes as it downloads:
- Android SDK
- Android NDK
- Python-for-Android
- All dependencies

### Subsequent Builds
```bash
buildozer android debug
```

Subsequent builds are much faster (5-10 minutes).

## Build Output

The APK will be generated at:
```
bin/AntiGravityAI-1.0.0-arm64-v8a-debug.apk
```

## Installation on Device

### Via USB (ADB)
```bash
# Install ADB tools
sudo apt install android-tools-adb

# Connect device with USB debugging enabled
adb devices

# Install APK
adb install -r bin/AntiGravityAI-1.0.0-arm64-v8a-debug.apk

# Run the app
adb shell am start -n com.antigravity.antigravityai/org.kivy.android.PythonActivity
```

### Via File Transfer
1. Copy APK to device
2. Open with file manager
3. Allow installation from unknown sources
4. Install

## Permissions

The app requires the following permissions:
- **INTERNET**: For model downloads
- **STORAGE**: For document uploads and model storage
- **CAMERA**: For OCR from camera
- **RECORD_AUDIO**: For voice input

Grant all permissions when prompted on first launch.

## Post-Installation Setup

### 1. Download Models
On first launch:
1. Go to Model Selection screen
2. Download at least one model (SmolLM2-135M recommended for testing)
3. Wait for download to complete

### 2. Test Core Features
- Send a test message
- Try voice input (if Vosk model available)
- Upload a test document (PDF/DOCX)
- Test OCR (camera required)

## Troubleshooting

### Build Errors

**"Command failed: ./distribute.sh"**
- Clean the build: `buildozer android clean`
- Check Java version: `java -version` (should be 17+)

**"NDK not found"**
- Buildozer will auto-download NDK
- If fails, manually download NDK 25b and set path in buildozer.spec

**"Python version mismatch"**
- Ensure Python 3.11 is installed
- Use virtual environment: `python3.11 -m venv venv`

### Runtime Errors

**App crashes on startup**
- Check logs: `adb logcat | grep python`
- Common cause: Missing dependencies in buildozer.spec

**Models not loading**
- Check storage permissions
- Verify model files are complete
- Check available RAM (need 2GB+ for SmolLM2-135M)

**ONNX Runtime errors**
- Ensure onnxruntime is in requirements
- Try downgrading to compatible version

## Release Build

### 1. Generate Keystore
```bash
keytool -genkey -v -keystore antigravity-release.keystore -alias antigravity -keyalg RSA -keysize 2048 -validity 10000
```

### 2. Update buildozer.spec
Add to `[app]` section:
```ini
android.release_artifact = apk
android.keystore = /path/to/antigravity-release.keystore
android.keyalias = antigravity
android.keystore_password = your-password
android.keyalias_password = your-password
```

### 3. Build Release APK
```bash
buildozer android release
```

## Distribution

### Google Play Store
1. Create developer account ($25 one-time fee)
2. Create new app listing
3. Upload APK or AAB
4. Complete store listing
5. Submit for review

### Alternative Distribution
- Direct download from website
- F-Droid (open source apps)
- Amazon App Store
- Samsung Galaxy Store

## App Size Optimization

Current APK size: ~50-70MB (without models)

**Reduce size:**
1. Remove unused dependencies from buildozer.spec
2. Use ProGuard for code minification
3. Enable APK splits for different architectures
4. Don't bundle models in APK (download on demand)

## Performance Optimization

**For production:**
1. Use INT8 quantized models
2. Implement model caching
3. Lazy load heavy dependencies
4. Use thread pooling for inference
5. Implement request batching

## Security Considerations

**Before releasing:**
- [ ] Use HTTPS for all network requests
- [ ] Validate all user inputs
- [ ] Secure model download URLs
- [ ] Implement checksum verification for downloads
- [ ] Add ProGuard for code obfuscation
- [ ] Remove debug logs
- [ ] Implement secure storage for user data

## Maintenance

### Updating Dependencies
```bash
# Update requirements.txt
pip install --upgrade <package>

# Rebuild
buildozer android clean
buildozer android debug
```

### Version Updates
1. Update `version` in buildozer.spec
2. Rebuild APK
3. Test thoroughly
4. Deploy to store

## Support

For build issues:
- Buildozer: https://buildozer.readthedocs.io/
- Python-for-Android: https://python-for-android.readthedocs.io/
- Kivy: https://kivy.org/doc/stable/

For app-specific issues:
- Check logs: `adb logcat`
- Review TESTING.md for performance benchmarks
- Check GitHub issues (if applicable)

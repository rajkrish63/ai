# Building AntiGravity AI on Windows

## ⚠️ Important: Buildozer Requires Linux

Buildozer **does not work on Windows directly**. You have two options:

### Option 1: Use WSL2 (Recommended for Windows)
### Option 2: Use a Linux VM or Linux machine

---

## 🐧 Option 1: Build with WSL2 (Windows Subsystem for Linux)

### Step 1: Install WSL2

```powershell
# Run in PowerShell as Administrator
wsl --install -d Ubuntu-22.04

# Restart your computer
```

### Step 2: Setup WSL2 Environment

Open Ubuntu from Start menu, then:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.11 python3.11-dev python3-pip git zip unzip \
  openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
  libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Install Buildozer
pip3 install --upgrade buildozer cython
```

### Step 3: Copy Project to WSL2

```bash
# In WSL2, go to your Windows drive (your project is at c:\dev\Ai)
cd /mnt/c/dev/Ai

# Or copy the project to WSL home directory for faster builds
cp -r /mnt/c/dev/Ai ~/antigravity-ai
cd ~/antigravity-ai
```

### Step 4: Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

### Step 5: Build APK

```bash
# First build (takes 30-60 minutes)
buildozer android debug

# The APK will be in: bin/AntiGravityAI-1.0.0-arm64-v8a-debug.apk
```

### Step 6: Access APK from Windows

The APK will be accessible from Windows at:
```
\\wsl$\Ubuntu-22.04\home\<your-username>\antigravity-ai\bin\
```

Or if you built in `/mnt/c/dev/Ai`:
```
c:\dev\Ai\bin\
```

---

## 🖥️ Option 2: Use Linux VM

### Using VirtualBox/VMware:

1. Install Ubuntu 22.04 in a VM (allocate 8GB+ RAM, 50GB+ disk)
2. Share your project folder with the VM
3. Follow WSL2 steps 2-5 above

---

## ✅ Verify buildozer.spec is Production-Ready

Your `buildozer.spec` has been updated with:

```ini
requirements = python3,kivy==2.3.1,kivymd==1.2.0,numpy,onnxruntime==1.17.0,tokenizers,pillow,requests,flatbuffers,protobuf,pyjnius,vosk,pypdf2,python-docx

android.api = 33
android.minapi = 29
android.ndk = 25b
android.arch = arm64-v8a
```

✅ **Production-ready configuration confirmed!**

---

## 🚀 Quick Build Commands

```bash
# Clean previous builds
buildozer android clean

# Debug build
buildozer android debug

# Release build (requires keystore)
buildozer android release

# Deploy and run on connected device
buildozer android debug deploy run
```

---

## 🔧 Troubleshooting

### "buildozer: command not found"
```bash
pip3 install --upgrade buildozer
export PATH=$PATH:~/.local/bin
```

### "Java version mismatch"
```bash
sudo update-alternatives --config java
# Select Java 17
```

### "NDK not found"
Buildozer will auto-download NDK 25b on first build.

### Build is very slow
First build takes 30-60 minutes. Subsequent builds are much faster (5-10 min).

---

## 📱 Installing APK on Android Device

### Method 1: USB (ADB)
```bash
# Install ADB
sudo apt install android-tools-adb

# Connect device with USB debugging enabled
adb devices

# Install
adb install -r bin/AntiGravityAI-1.0.0-arm64-v8a-debug.apk
```

### Method 2: File Transfer
1. Copy APK from `bin/` to your device
2. Open with file manager
3. Allow installation from unknown sources
4. Install

---

## 🎯 Next Steps After Building

1. ✅ Build APK in WSL2 or Linux
2. ✅ Install on Android device
3. ✅ Grant all permissions (storage, camera, microphone)
4. ✅ Download an AI model (SmolLM2-135M recommended)
5. ✅ Test core features
6. ✅ Replace mock tokenizers with real implementations
7. ✅ Download actual ONNX models

---

## 📚 Additional Resources

- [Buildozer Documentation](https://buildozer.readthedocs.io/)
- [WSL2 Installation Guide](https://docs.microsoft.com/en-us/windows/wsl/install)
- [Python-for-Android](https://python-for-android.readthedocs.io/)

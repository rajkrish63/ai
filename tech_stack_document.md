# Technology Stack Document
# AntiGravity AI - Offline Android AI Chatbot

---

## 1. Complete Technology Stack Overview

### 1.1 Architecture Pattern
**MVVM (Model-View-ViewModel)** adapted for Kivy/KivyMD
- **View**: KivyMD screens and widgets
- **ViewModel**: Screen controllers with observable properties
- **Model**: Data services and business logic

---

## 2. Frontend Stack (UI Layer)

### 2.1 Primary Framework

**Kivy 2.3.1**
- Cross-platform Python framework
- OpenGL-based rendering
- Event-driven architecture
- Touch and gesture support
- Custom widget creation

**Installation:**
```bash
pip install kivy==2.3.1
```

**Key Features Used:**
- Screen Manager (navigation)
- RecycleView (efficient lists)
- Properties (reactive data binding)
- Clock (scheduling and animations)
- FileChooser (file selection)

### 2.2 UI Framework

**KivyMD 1.2.0**
- Material Design 3 implementation
- Pre-built MD components
- Theming system
- Icon support (Material Icons)
- Elevation and shadows

**Installation:**
```bash
pip install kivymd==1.2.0
```

**Core Components Used:**
- MDNavigationDrawer (side menu)
- MDTopAppBar (header)
- MDTextField (input)
- MDCard (message bubbles)
- MDList (chat history, models)
- MDDialog (popups)
- MDProgressBar (downloads)
- MDButton (actions)
- MDChip (tags/labels)
- MDSpinner (loading)

### 2.3 UI Architecture

```python
# Main App Structure
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen

class AntiGravityAI(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return ScreenManager()

# Screen Example
class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chat_service = ChatService()
        self.model_manager = ModelManager()
```

---

## 3. Backend Stack (Logic Layer)

### 3.1 Core Language

**Python 3.11**
- Type hints support
- Async/await for concurrent operations
- Pattern matching
- Performance improvements over 3.10

**Key Libraries:**
```
python==3.11
kivy==2.3.1
kivymd==1.2.0
onnxruntime==1.17.0
numpy==1.24.3
pillow==10.2.0
requests==2.31.0
```

### 3.2 Concurrency & Async

**Threading for Background Tasks:**
```python
import threading
from kivy.clock import Clock

class ModelDownloader:
    def download_async(self, model_id, callback):
        thread = threading.Thread(
            target=self._download_worker,
            args=(model_id, callback)
        )
        thread.daemon = True
        thread.start()
    
    def _download_worker(self, model_id, callback):
        # Download logic
        Clock.schedule_once(lambda dt: callback(result), 0)
```

**Kivy Clock for UI Updates:**
- Schedule callbacks on main thread
- Periodic updates (progress bars)
- Delayed execution

---

## 4. AI Runtime Stack

### 4.1 ONNX Runtime

**ONNX Runtime Mobile 1.17.0**
- Cross-platform inference engine
- CPU-optimized execution
- INT8 quantization support
- Minimal dependencies

**Installation:**
```bash
pip install onnxruntime==1.17.0
```

**Android Integration:**
```python
import onnxruntime as ort

class ONNXInferenceEngine:
    def __init__(self, model_path):
        self.session = ort.InferenceSession(
            model_path,
            providers=['CPUExecutionProvider']
        )
    
    def generate(self, input_ids):
        outputs = self.session.run(
            None,
            {'input_ids': input_ids}
        )
        return outputs[0]
```

**Execution Providers:**
- **CPUExecutionProvider**: Default, runs on all devices
- **XNNPACKExecutionProvider**: Optimized for ARM (optional)

**Performance Tips:**
- Use INT8 quantized models
- Batch size = 1 for mobile
- Limit context window (512-1024 tokens)
- Enable session optimization

### 4.2 Model Format & Quantization

**Model Preparation:**
```bash
# Convert to ONNX (done offline)
python -m transformers.onnx --model=SmolLM2-135M-Instruct onnx/

# Quantize to INT8
python -m onnxruntime.quantization.quantize_dynamic \
    model.onnx \
    model_int8.onnx \
    --per_channel
```

**Recommended Models:**

| Model | Size | RAM | Speed | Accuracy |
|-------|------|-----|-------|----------|
| SmolLM2-135M (INT8) | 95MB | 2GB | Fast | Moderate |
| SmolLM2-360M (INT8) | 250MB | 3GB | Medium | Good |
| Gemma-1B-Instruct (Q4) | 650MB | 4GB | Slow | High |

---

## 5. RAG (Retrieval-Augmented Generation) Stack

### 5.1 Embedding Model

**all-MiniLM-L6-v2 (ONNX)**
- Size: 85MB (INT8)
- Embedding dimension: 384
- Fast inference on CPU
- Good semantic understanding

**Implementation:**
```python
import numpy as np
import onnxruntime as ort

class EmbeddingEngine:
    def __init__(self, model_path):
        self.session = ort.InferenceSession(model_path)
    
    def encode(self, text_chunks):
        # Tokenize and encode
        embeddings = []
        for chunk in text_chunks:
            tokens = self.tokenize(chunk)
            output = self.session.run(None, {'input_ids': tokens})
            embeddings.append(output[0])
        return np.array(embeddings)
```

### 5.2 Vector Search

**Cosine Similarity (NumPy)**
```python
def cosine_similarity(vec1, vec2):
    dot = np.dot(vec1, vec2)
    norm = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    return dot / norm

def search_similar(query_embedding, doc_embeddings, top_k=3):
    similarities = [
        cosine_similarity(query_embedding, emb)
        for emb in doc_embeddings
    ]
    indices = np.argsort(similarities)[-top_k:][::-1]
    return indices
```

**Why not FAISS/ChromaDB?**
- Too heavy for mobile
- NumPy sufficient for <10K chunks
- Simple and reliable

### 5.3 Document Processing

**Text Extraction:**
```python
# PDF
import PyPDF2
def extract_pdf(path):
    with open(path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# DOCX
import docx
def extract_docx(path):
    doc = docx.Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

# TXT
def extract_txt(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()
```

**Text Chunking:**
```python
def chunk_text(text, chunk_size=512, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks
```

---

## 6. OCR Stack

### 6.1 Google ML Kit (Recommended)

**ML Kit Text Recognition v2**
- Offline capability
- Fast and accurate
- Supports 50+ languages
- Free to use

**Android Integration (via Pyjnius):**
```python
from jnius import autoclass

TextRecognition = autoclass('com.google.mlkit.vision.text.TextRecognition')
InputImage = autoclass('com.google.mlkit.vision.common.InputImage')

class OCREngine:
    def __init__(self):
        self.recognizer = TextRecognition.getClient()
    
    def extract_text(self, image_path):
        image = InputImage.fromFilePath(context, Uri.parse(image_path))
        result = self.recognizer.process(image).getResult()
        return result.getText()
```

**Dependencies (buildozer.spec):**
```
requirements = python3,kivy,kivymd,pyjnius,android
android.gradle_dependencies = com.google.mlkit:text-recognition:16.0.0
```

### 6.2 Alternative: Tesseract OCR

**pytesseract (if ML Kit unavailable)**
```bash
pip install pytesseract
```

**Requires:**
- Tesseract binary (bundled in APK)
- Language data files (eng.traineddata)
- Larger APK size (+15MB)

---

## 7. Speech-to-Text Stack

### 7.1 Vosk (Recommended)

**Vosk-API**
- Fully offline
- Small models (50MB - 1.5GB)
- Real-time recognition
- Multiple language support

**Installation:**
```bash
pip install vosk
```

**Implementation:**
```python
from vosk import Model, KaldiRecognizer
import json

class VoiceRecognizer:
    def __init__(self, model_path):
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
    
    def recognize(self, audio_data):
        if self.recognizer.AcceptWaveform(audio_data):
            result = json.loads(self.recognizer.Result())
            return result.get('text', '')
        return ''
```

**Model Selection:**
- **vosk-model-small-en-us-0.15**: 40MB, fast, moderate accuracy
- **vosk-model-en-in-0.5**: 250MB, Indian English, better accuracy
- **vosk-model-small-hi-0.22**: 45MB, Hindi support

### 7.2 Alternative: Whisper.cpp (Advanced)

**whisper.cpp (Python bindings)**
- Higher accuracy
- Larger models (75MB - 1.5GB)
- Slower on CPU
- Better for non-English

**Trade-off:**
- Vosk: Fast, smaller, good enough
- Whisper: Slower, larger, excellent accuracy

**Recommendation:** Start with Vosk, upgrade to Whisper if needed

---

## 8. Storage & Data Persistence

### 8.1 File System Structure

```
/Android/data/com.antigravity.ai/files/
├── models/
│   ├── smollm2-135m/
│   │   ├── model_int8.onnx
│   │   ├── tokenizer.json
│   │   ├── config.json
│   │   └── manifest.json
│   └── gemma-1b-instruct/
│       └── (same structure)
├── embeddings/
│   └── minilm-l6-v2/
│       └── model.onnx
├── rag/
│   ├── documents/
│   │   ├── doc_001.json (metadata)
│   │   └── doc_001_chunks.npy (embeddings)
│   └── index.json
├── chat_history/
│   ├── chat_001.json
│   └── chat_002.json
├── cache/
│   └── (temporary files)
├── downloads/
│   └── (in-progress downloads)
└── settings.json
```

### 8.2 Data Storage Patterns

**Settings Storage (JSON):**
```python
import json

class SettingsManager:
    def __init__(self, path):
        self.path = path
        self.settings = self.load()
    
    def load(self):
        try:
            with open(self.path, 'r') as f:
                return json.load(f)
        except:
            return self.get_defaults()
    
    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def get_defaults(self):
        return {
            "selected_model": "smollm2-135m",
            "temperature": 0.7,
            "max_tokens": 512,
            "theme": "dark"
        }
```

**Chat History Storage:**
```python
class ChatManager:
    def save_chat(self, chat_id, messages):
        chat_data = {
            "id": chat_id,
            "timestamp": time.time(),
            "model": self.current_model,
            "messages": messages
        }
        path = f"chat_history/chat_{chat_id}.json"
        with open(path, 'w') as f:
            json.dump(chat_data, f)
    
    def load_chat(self, chat_id):
        path = f"chat_history/chat_{chat_id}.json"
        with open(path, 'r') as f:
            return json.load(f)
```

**RAG Index Storage (NumPy):**
```python
import numpy as np

class RAGIndexer:
    def save_embeddings(self, doc_id, embeddings, chunks):
        # Save embeddings as numpy array
        np.save(f"rag/documents/{doc_id}_chunks.npy", embeddings)
        
        # Save metadata
        metadata = {
            "id": doc_id,
            "chunks": chunks,
            "embedding_dim": embeddings.shape[1],
            "timestamp": time.time()
        }
        with open(f"rag/documents/{doc_id}.json", 'w') as f:
            json.dump(metadata, f)
```

---

## 9. Model Download & Management

### 9.1 Download System

**HTTP Downloader with Progress:**
```python
import requests

class ModelDownloader:
    def download(self, url, save_path, callback):
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                progress = (downloaded / total_size) * 100
                callback(progress)
```

**Model Verification:**
```python
import hashlib

def verify_checksum(file_path, expected_sha256):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest() == expected_sha256
```

**Model Extraction (tar.gz):**
```python
import tarfile

def extract_model(archive_path, destination):
    with tarfile.open(archive_path, 'r:gz') as tar:
        tar.extractall(destination)
```

### 9.2 Model Manifest Format

```json
{
  "name": "smollm2-135m",
  "version": "1.0",
  "size_bytes": 99614720,
  "sha256": "a1b2c3d4e5f6...",
  "min_ram_gb": 2,
  "recommended_ram_gb": 4,
  "speed": "fast",
  "accuracy": "moderate",
  "files": [
    "model_int8.onnx",
    "tokenizer.json",
    "config.json"
  ],
  "download_url": "https://github.com/user/repo/releases/download/v1.0/smollm2-135m.tar.gz"
}
```

---

## 10. Android Build Stack

### 10.1 Buildozer

**buildozer 1.5.0**
- Automates Android APK building
- Handles NDK, SDK, dependencies
- Generates signed APKs

**Installation:**
```bash
pip install buildozer
```

**buildozer.spec Configuration:**
```ini
[app]
title = AntiGravity AI
package.name = antigravityai
package.domain = com.antigravity

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,onnx

version = 1.0.0

requirements = python3==3.11,kivy==2.3.1,kivymd==1.2.0,onnxruntime,numpy,pillow,requests,pyjnius,vosk

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,RECORD_AUDIO,CAMERA

android.api = 31
android.minapi = 26
android.ndk = 25b
android.gradle_dependencies = com.google.mlkit:text-recognition:16.0.0

android.arch = arm64-v8a
```

**Build Commands:**
```bash
# Initialize
buildozer android debug

# Build release APK
buildozer android release

# Deploy to connected device
buildozer android deploy run
```

### 10.2 Dependencies for Build

**System Requirements (Linux/WSL):**
```bash
sudo apt install -y \
    python3-pip \
    build-essential \
    git \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    openjdk-11-jdk \
    autoconf \
    libtool
```

---

## 11. Complete Development Stack Summary

### 11.1 Core Technologies

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| UI Framework | Kivy | 2.3.1 | Base framework |
| UI Components | KivyMD | 1.2.0 | Material Design |
| Language | Python | 3.11 | App logic |
| AI Runtime | ONNX Runtime | 1.17.0 | Model inference |
| OCR | ML Kit | 16.0.0 | Text recognition |
| STT | Vosk | Latest | Voice recognition |
| Build Tool | Buildozer | 1.5.0 | APK generation |

### 11.2 Python Libraries

```
# requirements.txt
kivy==2.3.1
kivymd==1.2.0
onnxruntime==1.17.0
numpy==1.24.3
pillow==10.2.0
requests==2.31.0
pyjnius==1.5.0
vosk==0.3.45
PyPDF2==3.0.1
python-docx==1.1.0
```

### 11.3 Asset Requirements

**Models to Host:**
- SmolLM2-135M (INT8) - 95MB
- MiniLM-L6-v2 (INT8) - 85MB
- Vosk-small-en-us - 40MB

**Total Initial Download:** ~220MB

**Icons & Images:**
- App icon (512x512)
- Material icons (included in KivyMD)

---

## 12. Why This Stack? (Justification)

### 12.1 Kivy + KivyMD vs Kotlin + Compose

| Aspect | Kivy/KivyMD | Kotlin/Compose |
|--------|-------------|----------------|
| Learning Curve | Easy (Python) | Steeper (Kotlin + Android) |
| Development Speed | Fast | Medium |
| ONNX Integration | Direct (Python) | Requires JNI |
| Cross-platform | Yes (Python code) | Android only |
| Community | Smaller | Larger |
| Performance | Good enough | Better |

**Verdict:** Kivy is better for rapid prototyping and academic projects with Python expertise.

### 12.2 ONNX Runtime vs TensorFlow Lite

| Aspect | ONNX | TFLite |
|--------|------|--------|
| Model Support | Broad (PyTorch, HF) | TensorFlow only |
| Quantization | INT8, Q4 | INT8, FP16 |
| Mobile Optimization | Good | Excellent |
| Python API | Excellent | Limited |

**Verdict:** ONNX for flexibility, TFLite for maximum performance.

### 12.3 Vosk vs Whisper

| Aspect | Vosk | Whisper |
|--------|------|---------|
| Size | 40-250MB | 75MB-1.5GB |
| Speed | Fast | Slower |
| Accuracy | Good | Excellent |
| Languages | 20+ | 50+ |

**Verdict:** Vosk for real-time, Whisper for accuracy.

---

## 13. Performance Benchmarks (Expected)

### On 4GB RAM Android Device

| Operation | Time | RAM Usage |
|-----------|------|-----------|
| App Launch | 3-5s | 150MB |
| Model Load (135M) | 2-3s | +200MB |
| Chat Response (50 tokens) | 5-8s | +100MB |
| OCR (1 page) | 1-2s | +50MB |
| STT (5 sec audio) | 2-3s | +80MB |
| RAG Search (1000 chunks) | 0.5s | +30MB |

**Total RAM:** ~500-600MB (safe for 4GB devices)

---

## 14. Development Tools & Environment

### 14.1 IDE Recommendations
- **PyCharm** (best Python IDE)
- **VS Code** (lightweight, good extensions)
- **Android Studio** (for debugging APK)

### 14.2 Testing Tools
- **Android Emulator** (API 30+)
- **Physical Device** (4GB RAM Android 10+)
- **ADB** (logcat for debugging)

### 14.3 Version Control
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <repo-url>
git push -u origin main
```

**.gitignore:**
```
*.pyc
__pycache__/
.buildozer/
bin/
.gradle/
local.properties
*.apk
*.keystore
models/
```

---

## 15. Deployment Strategy

### 15.1 Release Process

1. **Test thoroughly** on multiple devices
2. **Optimize** (remove debug code, compress assets)
3. **Generate signed APK**:
   ```bash
   buildozer android release
   jarsigner -verbose -sigalg SHA256withRSA \
       -digestalg SHA-256 \
       -keystore my-release-key.keystore \
       bin/*.apk alias_name
   zipalign -v 4 bin/unsigned.apk bin/signed.apk
   ```
4. **Upload to GitHub Releases**
5. **Create release notes**

### 15.2 Distribution Channels

**Primary:**
- GitHub Releases (direct APK)
- Personal website

**Future:**
- Google Play Store (requires developer account $25)
- F-Droid (open-source app store)

---

## 16. Final Recommendation

**For Your Academic Project:**

✅ **USE THIS STACK:**
- Kivy 2.3.1 + KivyMD 1.2.0 (UI)
- ONNX Runtime (AI)
- ML Kit (OCR)
- Vosk (STT)
- NumPy (RAG search)
- Buildozer (Build)

**REASON:**
- Fast development
- Python-friendly
- Good documentation
- Sufficient performance for demo
- Easy to explain in viva
- Complete offline capability

**If you have 3+ months and want production-ready:**
- Consider Kotlin + Jetpack Compose
- But require more Android knowledge

---

**Document Version**: 1.0  
**Last Updated**: February 13, 2025  
**Status**: Complete - Ready for Implementation

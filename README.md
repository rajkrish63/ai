# AntiGravity AI

An offline-first AI chatbot for Android with document Q&A, OCR, and voice capabilities.

## Features

✨ **Offline AI Chat**: Run language models locally on your device  
📄 **Document Q&A (RAG)**: Ask questions about your PDFs, DOCX, and TXT files  
🔍 **OCR**: Extract text from images using Google ML Kit  
🎤 **Voice Input**: Speech-to-text using Vosk (offline)  
🔒 **Privacy-First**: All processing happens on-device, no data sent to cloud  
📱 **Lightweight**: Optimized for mobile with 2GB+ RAM devices

## Quick Start

### For Users

1. **Download APK**: Get the latest APK from releases
2. **Install**: Enable installation from unknown sources if needed
3. **Grant Permissions**: Allow storage, camera, and microphone access
4. **Download Model**: On first launch, download an AI model (SmolLM2-135M recommended)
5. **Start Chatting**: Ask questions, upload documents, or use voice input

### For Developers

```bash
# Clone repository
git clone <repository-url>
cd Ai

# Install dependencies
pip install -r requirements.txt

# Run tests
python run_tests.py

# Build APK
buildozer android debug
```

## System Requirements

**Minimum:**
- Android 8.0 (API 26) or higher
- 2GB RAM
- 500MB free storage (+ models)

**Recommended:**
- Android 10+ (API 29)
- 4GB+ RAM
- 2GB free storage

## Supported Models

| Model | Size | RAM | Speed | Accuracy |
|-------|------|-----|-------|----------|
| SmolLM2-135M | 95 MB | 2GB | Fast | Moderate |
| SmolLM2-360M | 250 MB | 3GB | Medium | Good |
| Gemma-1B | 650 MB | 4GB | Slow | High |

## Architecture

```
AntiGravity AI/
├── main.py                 # App entry point
├── buildozer.spec          # Build configuration
├── requirements.txt        # Python dependencies
├── libs/
│   ├── app_theme.py        # Theme configuration
│   ├── components/         # Reusable UI components
│   │   ├── chat_bubble.py
│   │   └── model_card.py
│   ├── screens/            # App screens
│   │   ├── chat_screen.py
│   │   ├── model_selection_screen.py
│   │   ├── chat_history_screen.py
│   │   ├── settings_screen.py
│   │   └── document_upload_screen.py
│   └── services/           # Business logic
│       ├── chat_manager.py
│       ├── settings_manager.py
│       ├── storage_manager.py
│       ├── model_manager.py
│       ├── model_downloader.py
│       ├── onnx_inference_engine.py
│       ├── document_service.py
│       ├── embedding_engine.py
│       ├── vector_store.py
│       ├── ocr_engine.py
│       └── voice_recognizer.py
└── tests/                  # Unit tests
```

## Technology Stack

**Frontend:**
- Kivy 2.3.1 (UI framework)
- KivyMD 1.2.0 (Material Design 3)

**Backend:**
- ONNX Runtime 1.17.0 (AI inference)
- NumPy (RAG vector search)
- PyPDF2, python-docx (document parsing)

**Advanced Features:**
- Google ML Kit (OCR)
- Vosk 0.3.45 (speech-to-text)

**Build Tools:**
- Buildozer 1.5.0 (APK packaging)
- Python 3.11

## Documentation

- [Deployment Guide](DEPLOYMENT.md) - Building and releasing the APK
- [Testing Guide](TESTING.md) - Running tests and performance benchmarks
- [PRW Document](PRW_Document.md) - Product requirements
- [Design Document](design_document.md) - UI/UX specifications
- [Tech Stack Document](tech_stack_document.md) - Technical architecture

## Development

### Project Structure

**Phase 1**: Project Setup & Core Architecture ✅  
**Phase 2**: Core UI Implementation ✅  
**Phase 3**: Business Logic & Data Layer ✅  
**Phase 4**: AI Engine Integration ✅  
**Phase 5**: RAG System Implementation ✅  
**Phase 6**: Advanced Features (OCR & Voice) ✅  
**Phase 7**: Testing & Optimization ✅  
**Phase 8**: Build & Deployment ✅

### Running Tests

```bash
# Run all tests
python run_tests.py

# Run specific test
python -m unittest tests.test_chat_manager
```

### Building

```bash
# Debug build
buildozer android debug

# Release build (requires keystore)
buildozer android release
```

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## Known Limitations

1. **Mock Implementations**: Tokenizers and embeddings use placeholders - replace with actual models
2. **CPU-Only**: No GPU acceleration yet (slower inference)
3. **Storage**: Models require significant space (100-700MB each)
4. **Android-Only**: Currently supports Android; iOS planned

## Roadmap

- [ ] GPU acceleration support
- [ ] Additional model formats (GGUF)
- [ ] Web UI for desktop
- [ ] iOS support
- [ ] Model quantization wizard
- [ ] Cloud sync (optional)

## Performance

**Target Metrics (4GB RAM device with SmolLM2-135M):**
- Model loading: < 3 seconds
- First token: < 500ms
- Tokens/second: 8-12
- Total response (50 tokens): 5-8 seconds
- Memory usage: < 600MB

## Privacy

- ✅ All AI processing on-device
- ✅ No telemetry or analytics
- ✅ No internet required (except model downloads)
- ✅ User data stored locally only

## License

[Add your license here]

## Acknowledgments

- Kivy Team for the excellent mobile framework
- ONNX Runtime for efficient ML inference
- Google ML Kit for OCR capabilities
- Vosk for offline speech recognition

## Support

For issues and questions:
- GitHub Issues: [Repository URL]
- Documentation: See docs/ folder
- Email: [Your email]

---

**Built with ❤️ for privacy-conscious mobile AI users**

# AntiGravity AI - Testing & Performance Guide

## Running Unit Tests

### Run All Tests
```bash
python run_tests.py
```

### Run Specific Test File
```bash
python -m unittest tests.test_chat_manager
python -m unittest tests.test_settings_manager
python -m unittest tests.test_storage_manager
```

### Run Single Test Case
```bash
python -m unittest tests.test_chat_manager.TestChatManager.test_create_chat
```

## Performance Testing

### Memory Profiling (Desktop Testing)

Install memory profiler:
```bash
pip install memory-profiler
```

Create a profiling script:
```python
from memory_profiler import profile

@profile
def test_model_loading():
    from libs.services.onnx_inference_engine import ONNXInferenceEngine
    engine = ONNXInferenceEngine("models/smollm2-135m")
    engine.load()
    # Test inference
    engine.generate("Hello, how are you?", max_tokens=50)
    engine.unload()

if __name__ == '__main__':
    test_model_loading()
```

Run with:
```bash
python -m memory_profiler test_performance.py
```

### Performance Benchmarks (Target Metrics)

**On 4GB RAM Device (SmolLM2-135M):**
- Model loading: < 3 seconds
- First token latency: < 500ms
- Tokens per second: 8-12
- Total response time (50 tokens): 5-8 seconds
- Memory usage: < 600MB total

**RAG Performance:**
- Document indexing: < 1s per 1000 chunks
- Similarity search: < 500ms for 1000 chunks
- Total RAG query time: < 2s

## Android Testing

### Build APK
```bash
buildozer android debug
```

### Install on Device
```bash
buildozer android deploy run
```

### Monitor Logs
```bash
adb logcat | grep python
```

### Memory Monitoring
```bash
# Monitor app memory usage
adb shell dumpsys meminfo com.antigravity.ai

# Continuous monitoring
watch -n 1 'adb shell dumpsys meminfo com.antigravity.ai | grep TOTAL'
```

### Performance Profiling on Android
```bash
# CPU profiling
adb shell simpleperf record -a -g --app com.antigravity.ai

# Memory snapshots
adb shell am dumpheap com.antigravity.ai /data/local/tmp/heap.hprof
adb pull /data/local/tmp/heap.hprof
```

## Offline Capability Testing

1. **Enable Airplane Mode** on test device
2. **Verify all features work:**
   - Chat generation
   - Document Q&A
   - Voice input (Vosk)
   - OCR (ML Kit)
   - Model download should fail gracefully
3. **Test error handling** for offline scenarios

## Test Checklist

- [ ] Unit tests pass
- [ ] Chat functionality works
- [ ] Model loading and inference work
- [ ] RAG document upload and search work
- [ ] Settings persist correctly
- [ ] Storage management functions
- [ ] OCR extracts text (Android only)
- [ ] Voice recognition works (with Vosk model)
- [ ] App works completely offline
- [ ] Memory usage within target (< 600MB)
- [ ] No crashes or ANR
- [ ] UI responsive during inference

## Known Limitations

1. **Mock Implementations:**
   - ONNX tokenizer (placeholder)
   - Embedding engine (returns random vectors)
   - OCR requires Android device
   - Voice requires Vosk model download

2. **Performance:**
   - CPU-only inference (no GPU acceleration yet)
   - Slower than cloud-based solutions

3. **Storage:**
   - Models require 100MB-700MB each
   - Documents take additional space

## Next Steps for Production

1. Replace mock tokenizers with real implementations
2. Download and integrate actual ONNX models
3. Add proper error handling for edge cases
4. Implement model quantization for smaller sizes
5. Add comprehensive integration tests
6. Performance optimization (caching, lazy loading)

# Design Document
# AntiGravity AI - Offline Android AI Chatbot

---

## 1. Project Overview

**AntiGravity AI** is an offline-first Android AI chatbot application that provides intelligent conversational assistance without requiring internet connectivity. The app features dynamic model management, document-based Q&A, OCR capabilities, and voice input - all running locally on Android devices.

---

## 2. Application Requirements

### 2.1 Core Features

#### Chat Interface
- **No Account Required**: Anonymous, privacy-focused usage
- **Temporary Chat Sessions**: No persistent login required
- **New Chat Creation**: Start fresh conversations instantly
- **Chat History**: Access previous conversations from menu
- **Model Selection**: Choose between available AI models
- **File Attachment**: Upload documents for context-aware responses
- **Additional Options**: Settings, clear history, export chat

#### Menu Structure
```
Menu
├── New Chat
├── Chat History
│   ├── Today
│   ├── Yesterday
│   └── Last 7 Days
├── Settings
│   ├── Model Selection
│   ├── Temperature Control
│   ├── Max Tokens
│   └── Theme
└── About
```

### 2.2 User Interface Specifications

#### Primary Pages

1. **Chat Screen** (Main Interface)
   - Message input field with file attachment button
   - Send button
   - Chat history display (scrollable)
   - Model indicator at top
   - Menu access (hamburger/sidebar)
   - Token streaming display

2. **Model Selection Screen**
   - List of available models
   - Download status indicators
   - Model specifications (size, RAM requirement)
   - Download/Delete actions
   - Active model indicator

3. **Chat History Screen**
   - Grouped by date
   - Search functionality
   - Delete individual chats
   - Export chat option

4. **Document Upload Screen**
   - File picker integration
   - Supported formats: PDF, DOCX, TXT
   - Processing status
   - Document management

5. **Settings Screen**
   - Model parameters (temperature, top-k, top-p)
   - Theme selection (Light/Dark)
   - Storage management
   - Clear cache option

#### Shared Components

1. **Navigation System**
   - Side drawer navigation
   - Material Design 3 compliance
   - Smooth transitions

2. **Header/Top Bar**
   - App title/logo
   - Current model indicator
   - Menu toggle
   - Action buttons (context-sensitive)

3. **Bottom Action Bar** (Chat Screen)
   - Text input field
   - Attachment button (file, image, voice)
   - Send button
   - Typing indicator

#### Modals/Popups

1. **Model Download Dialog**
   - Model details
   - Size and RAM warning
   - Download progress
   - Pause/Resume controls
   - Checksum verification status

2. **File Upload Dialog**
   - File selection
   - Upload progress
   - Processing status

3. **Settings Adjustment Dialog**
   - Sliders for parameters
   - Real-time preview
   - Reset to defaults

4. **Confirmation Dialogs**
   - Delete chat history
   - Clear cache
   - Delete model

---

## 3. Technical Architecture

### 3.1 Framework Stack

#### Frontend Framework
- **Kivy**: 2.3.1
- **KivyMD**: 1.2.0
- **Python**: 3.11

#### UI Components
- Material Design 3 widgets
- Custom themed components
- Responsive layouts
- Animation support

### 3.2 Application Architecture

```
┌─────────────────────────────────────┐
│         Presentation Layer          │
│  (KivyMD UI Components + Screens)   │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│        Business Logic Layer         │
│  (Chat Manager, Model Manager,      │
│   RAG Engine, OCR Handler)          │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│         Data Access Layer           │
│  (File Storage, Model Loader,       │
│   Document Indexer, Cache Manager)  │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│        Infrastructure Layer         │
│  (ONNX Runtime, ML Kit, Vosk,       │
│   Storage Manager, WorkManager)     │
└─────────────────────────────────────┘
```

### 3.3 Component Reusability

#### Reusable Components

1. **ChatBubble Widget**
   - User message bubble
   - AI response bubble
   - Timestamp
   - Copy/Share actions

2. **ModelCard Widget**
   - Model information display
   - Download button
   - Status indicator
   - Action menu

3. **FileAttachment Widget**
   - File preview
   - Remove button
   - Processing indicator

4. **ProgressDialog Widget**
   - Indeterminate progress
   - Determinate progress with percentage
   - Cancel button
   - Status message

5. **SettingsSlider Widget**
   - Value display
   - Min/Max labels
   - Real-time update

### 3.4 URL-Based Routing (Screen Navigation)

```python
# Navigation structure
screens = {
    'chat': 'ChatScreen',
    'models': 'ModelSelectionScreen',
    'history': 'ChatHistoryScreen',
    'documents': 'DocumentScreen',
    'settings': 'SettingsScreen',
    'about': 'AboutScreen'
}

# Navigation handler
def navigate_to(screen_name, **params):
    # Screen transition logic
    # Parameter passing
    # History stack management
```

### 3.5 Data Handling Architecture

#### API-like Service Layer (Local)

```python
class ModelService:
    """Handles model management operations"""
    - list_available_models()
    - download_model(model_id)
    - delete_model(model_id)
    - get_model_info(model_id)
    - verify_model(model_id)

class ChatService:
    """Manages chat operations"""
    - create_chat()
    - get_chat_history()
    - delete_chat(chat_id)
    - export_chat(chat_id)
    - generate_response(prompt, context)

class DocumentService:
    """Handles document processing"""
    - upload_document(file_path)
    - extract_text(file_path)
    - generate_embeddings(text)
    - search_similar(query)
    - delete_document(doc_id)

class StorageService:
    """Manages app storage"""
    - get_storage_info()
    - clear_cache()
    - export_data()
    - import_data()
```

#### Mock Data Structure

```json
{
  "models": [
    {
      "id": "smollm2-135m",
      "name": "SmolLM2 135M",
      "size_mb": 95,
      "min_ram_gb": 2,
      "status": "downloaded",
      "accuracy": "moderate",
      "speed": "fast",
      "files": {
        "model": "model_int8.onnx",
        "tokenizer": "tokenizer.json",
        "config": "config.json"
      }
    },
    {
      "id": "gemma-1b-instruct",
      "name": "Gemma 1B Instruct",
      "size_mb": 650,
      "min_ram_gb": 4,
      "status": "available",
      "accuracy": "high",
      "speed": "moderate"
    }
  ],
  "chat_history": [
    {
      "id": "chat_001",
      "timestamp": "2025-02-13T10:30:00",
      "title": "Python basics",
      "model_used": "smollm2-135m",
      "messages": [
        {
          "role": "user",
          "content": "Explain Python decorators",
          "timestamp": "2025-02-13T10:30:00"
        },
        {
          "role": "assistant",
          "content": "A decorator is...",
          "timestamp": "2025-02-13T10:30:15"
        }
      ]
    }
  ],
  "documents": [
    {
      "id": "doc_001",
      "name": "research_paper.pdf",
      "size_kb": 2048,
      "upload_date": "2025-02-13",
      "status": "indexed",
      "chunk_count": 45
    }
  ]
}
```

---

## 4. Technical Requirements

### 4.1 Styling Framework
- **KivyMD Material Design 3**
- Custom theme configuration
- Color palette: Primary, Secondary, Error, Background
- Typography scale
- Elevation and shadows
- Rounded corners and padding standards

### 4.2 Component Reusability Principles
- Single responsibility per component
- Props-based configuration
- Event-driven communication
- Stateless where possible
- Documented interfaces

### 4.3 Routing Implementation
- Screen manager with stack
- Named routes
- Parameter passing via kwargs
- Back stack management
- Deep linking support (future)

### 4.4 Data Services
- Singleton service instances
- Async operations for I/O
- Error handling and retry logic
- Caching strategies
- Background task scheduling

### 4.5 Fully Functional End-to-End Flow

#### Example: User Downloads Model and Chats

1. **User opens app** → Default screen (Chat)
2. **No model available** → Show prompt to download
3. **User taps "Select Model"** → Navigate to Model Selection
4. **User selects "SmolLM2 135M"** → Show download dialog
5. **User confirms download** → WorkManager starts background download
6. **Download completes** → Model extracted and verified
7. **Navigate back to Chat** → Model loaded into ONNX Runtime
8. **User types message** → Tokenized and sent to model
9. **Model generates response** → Streamed token-by-token to UI
10. **Response displayed** → User can continue conversation

---

## 5. Additional Technical Considerations

### 5.1 Performance Optimization
- Lazy loading of screens
- Virtual scrolling for long chat history
- Image compression for attachments
- Model caching in memory
- Background thread for inference

### 5.2 Storage Management
- App-private directory (`/Android/data/<package>/files/`)
- Organized folder structure
- Automatic cache cleanup
- Storage quota monitoring
- User-initiated data export

### 5.3 Error Handling
- Network unavailable (for downloads)
- Insufficient storage
- Model corruption
- Out of memory
- Invalid file formats
- User-friendly error messages

### 5.4 Accessibility
- Screen reader support
- High contrast mode
- Adjustable font sizes
- Keyboard navigation
- Color-blind friendly palette

### 5.5 Security & Privacy
- No external API calls during inference
- Local-only data storage
- No analytics or tracking
- Scoped storage compliance (Android 11+)
- No user data collection

---

## 6. Development Workflow

### 6.1 Development Phases

**Phase 1: Core UI (Week 1-2)**
- Implement screens and navigation
- Build reusable components
- Setup theme and styling

**Phase 2: Model Integration (Week 3-4)**
- ONNX Runtime integration
- Model download system
- Inference engine

**Phase 3: Features (Week 5-6)**
- RAG implementation
- OCR integration
- Voice input

**Phase 4: Testing & Polish (Week 7-8)**
- Bug fixes
- Performance optimization
- Documentation

### 6.2 Testing Strategy
- Unit tests for services
- UI tests for critical flows
- Manual testing on multiple devices
- Performance benchmarking
- Storage stress testing

---

## 7. Deliverables

1. **Functional APK**
   - Signed and optimized
   - Version controlled
   - Release notes

2. **Documentation**
   - User manual
   - Developer guide
   - API documentation

3. **Project Artifacts**
   - Source code repository
   - Design mockups
   - Test reports
   - Presentation materials

---

## 8. Success Criteria

- ✅ Runs offline without internet
- ✅ Works smoothly on 4GB RAM devices
- ✅ Model download and management functional
- ✅ Chat responses generate in real-time
- ✅ Document Q&A provides contextual answers
- ✅ OCR extracts text accurately
- ✅ Voice input converts speech correctly
- ✅ No crashes or ANR (Application Not Responding)
- ✅ Storage management prevents disk full issues
- ✅ User-friendly and intuitive interface

---

**Document Version**: 1.0  
**Last Updated**: February 13, 2025  
**Status**: Design Complete - Ready for Implementation

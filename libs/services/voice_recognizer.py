"""
Voice Recognition using Vosk offline speech-to-text.
"""
import os
import json
from typing import Optional, Callable

class VoiceRecognizer:
    """
    Offline speech-to-text using Vosk API.
    Supports real-time audio processing and transcription.
    """
    
    def __init__(self, model_path: str = "models/vosk-model-small-en-us-0.15"):
        """
        Initialize voice recognizer.
        
        Args:
            model_path: Path to Vosk model directory
        """
        self.model_path = model_path
        self.model = None
        self.recognizer = None
        self.is_loaded = False
        self.sample_rate = 16000  # Vosk recommended sample rate
    
    def load(self) -> bool:
        """Load the Vosk model."""
        try:
            from vosk import Model, KaldiRecognizer
            
            if not os.path.exists(self.model_path):
                print(f"Vosk model not found: {self.model_path}")
                return False
            
            # Load model
            self.model = Model(self.model_path)
            
            # Create recognizer
            self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
            
            self.is_loaded = True
            return True
            
        except ImportError:
            print("Vosk not installed. Run: pip install vosk")
            return False
        except Exception as e:
            print(f"Failed to load Vosk model: {e}")
            return False
    
    def recognize_from_audio_data(self, audio_data: bytes) -> Optional[str]:
        """
        Recognize speech from raw audio data.
        
        Args:
            audio_data: Raw audio bytes (16-bit PCM, 16kHz)
            
        Returns:
            Recognized text or None
        """
        if not self.is_loaded:
            return None
        
        try:
            if self.recognizer.AcceptWaveform(audio_data):
                result = json.loads(self.recognizer.Result())
                return result.get('text', '')
            else:
                # Partial result
                partial = json.loads(self.recognizer.PartialResult())
                return partial.get('partial', '')
                
        except Exception as e:
            print(f"Recognition error: {e}")
            return None
    
    def recognize_from_file(self, audio_file: str) -> Optional[str]:
        """
        Recognize speech from audio file.
        
        Args:
            audio_file: Path to WAV file (16-bit PCM, 16kHz)
            
        Returns:
            Recognized text
        """
        if not self.is_loaded:
            return None
        
        try:
            import wave
            
            wf = wave.open(audio_file, "rb")
            
            # Check format
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != self.sample_rate:
                print(f"Audio must be WAV format mono PCM, 16kHz, 16-bit")
                return None
            
            # Process audio
            results = []
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get('text', '')
                    if text:
                        results.append(text)
            
            # Get final result
            final_result = json.loads(self.recognizer.FinalResult())
            text = final_result.get('text', '')
            if text:
                results.append(text)
            
            wf.close()
            
            return ' '.join(results)
            
        except Exception as e:
            print(f"File recognition error: {e}")
            return None
    
    def start_continuous_recognition(self, audio_callback: Callable[[bytes], None],
                                    text_callback: Callable[[str], None]) -> None:
        """
        Start continuous speech recognition.
        
        Args:
            audio_callback: Function to get audio data chunks
            text_callback: Function to receive recognized text
        """
        if not self.is_loaded:
            text_callback("Error: Model not loaded")
            return
        
        # This would typically run in a separate thread
        # and continuously process audio from microphone
        
        # Placeholder - actual implementation needs:
        # 1. Microphone access (via plyer or android API)
        # 2. Audio streaming thread
        # 3. Continuous processing loop
        
        text_callback("Continuous recognition not yet fully implemented")
    
    def reset(self) -> None:
        """Reset the recognizer state."""
        if self.is_loaded and self.recognizer:
            from vosk import KaldiRecognizer
            self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
    
    def unload(self) -> None:
        """Unload the model to free memory."""
        self.model = None
        self.recognizer = None
        self.is_loaded = False


# Stub implementation for testing
class VoiceRecognizerStub:
    """
    Stub voice recognizer for testing without Vosk.
    """
    
    def __init__(self, model_path: str = ""):
        self.is_loaded = False
    
    def load(self) -> bool:
        print("Using Voice Recognizer stub (Vosk required for real STT)")
        self.is_loaded = True
        return True
    
    def recognize_from_audio_data(self, audio_data: bytes) -> Optional[str]:
        return "Mock recognized text from audio data"
    
    def recognize_from_file(self, audio_file: str) -> Optional[str]:
        return "Mock recognized text from file"
    
    def start_continuous_recognition(self, audio_callback, text_callback):
        text_callback("Mock continuous recognition")
    
    def reset(self) -> None:
        pass
    
    def unload(self) -> None:
        self.is_loaded = False

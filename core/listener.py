"""
AlfredX Listener Module
=======================
Handles speech recognition using Vosk for offline processing.
Supports both English and Turkish.
ROBUST VERSION WITH PROPER THREADING.
"""

import json
import queue
import threading
import time
from typing import Optional, Callable
import sounddevice as sd
import numpy as np

# Vosk import with error handling
try:
    from vosk import Model, KaldiRecognizer, SetLogLevel
    SetLogLevel(-1)  # Suppress Vosk logs
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False
    print("⚠️ Vosk not available")

from config.settings import Settings


class Listener:
    """
    Speech recognition using Vosk.
    Supports English and Turkish with automatic language switching.
    """
    
    def __init__(self, language: str = "en"):
        """
        Initialize the listener.
        
        Args:
            language: Initial language ("en" or "tr")
        """
        self.language = language
        self.is_listening = False
        self.audio_queue = queue.Queue()
        self._stop_event = threading.Event()
        self._stream = None
        self._listen_thread = None
        
        # Load models
        self.models = {}
        self.recognizers = {}
        self._load_models()
        
        # Callbacks
        self.on_speech_recognized: Optional[Callable[[str], None]] = None
        self.on_partial_result: Optional[Callable[[str], None]] = None
        self.on_listening_started: Optional[Callable[[], None]] = None
        self.on_listening_stopped: Optional[Callable[[], None]] = None
        self.on_error: Optional[Callable[[str], None]] = None
    
    def _load_models(self):
        """Load Vosk models for all supported languages."""
        if not VOSK_AVAILABLE:
            print("❌ Vosk not available - speech recognition disabled")
            return
        
        # English model
        model_en_path = Settings.MODEL_EN_PATH
        if model_en_path.exists():
            try:
                print(f"  Loading English model from {model_en_path}...")
                self.models["en"] = Model(str(model_en_path))
                self.recognizers["en"] = KaldiRecognizer(
                    self.models["en"], 
                    Settings.SAMPLE_RATE
                )
                self.recognizers["en"].SetWords(True)
                print("  ✅ English Vosk model loaded")
            except Exception as e:
                print(f"  ❌ Failed to load English model: {e}")
        else:
            print(f"  ⚠️ English model not found at {model_en_path}")
        
        # Turkish model
        model_tr_path = Settings.MODEL_TR_PATH
        if model_tr_path.exists():
            try:
                print(f"  Loading Turkish model from {model_tr_path}...")
                self.models["tr"] = Model(str(model_tr_path))
                self.recognizers["tr"] = KaldiRecognizer(
                    self.models["tr"], 
                    Settings.SAMPLE_RATE
                )
                self.recognizers["tr"].SetWords(True)
                print("  ✅ Turkish Vosk model loaded")
            except Exception as e:
                print(f"  ❌ Failed to load Turkish model: {e}")
        else:
            print(f"  ⚠️ Turkish model not found at {model_tr_path}")
    
    def set_language(self, language: str):
        """
        Switch recognition language.
        
        Args:
            language: "en" or "tr"
        """
        if language in self.models:
            self.language = language
            print(f"🌐 Language switched to: {language}")
        else:
            print(f"⚠️ Language {language} not available")
    
    def _audio_callback(self, indata, frames, time_info, status):
        """Callback for audio input stream."""
        if status:
            print(f"Audio status: {status}")
        if self.is_listening:
            self.audio_queue.put(bytes(indata))
    
    def start_listening(self):
        """Start listening for speech."""
        if self.is_listening:
            print("Already listening")
            return
        
        if not VOSK_AVAILABLE:
            if self.on_error:
                self.on_error("Vosk not available")
            return
        
        if self.language not in self.recognizers:
            error_msg = f"No recognizer for language: {self.language}"
            print(f"❌ {error_msg}")
            if self.on_error:
                self.on_error(error_msg)
            return
        
        print(f"🎤 Starting listener for language: {self.language}")
        
        self.is_listening = True
        self._stop_event.clear()
        
        # Clear the audio queue
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except queue.Empty:
                break
        
        # Start audio stream and processing in thread
        self._listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._listen_thread.start()
    
    def _listen_loop(self):
        """Main listening loop in separate thread."""
        print("  🎤 Listen loop started")
        
        if self.on_listening_started:
            self.on_listening_started()
        
        try:
            # Open audio stream
            with sd.RawInputStream(
                samplerate=Settings.SAMPLE_RATE,
                blocksize=8000,
                dtype="int16",
                channels=1,
                callback=self._audio_callback
            ) as stream:
                print("  ✅ Audio stream opened")
                
                recognizer = self.recognizers[self.language]
                
                while not self._stop_event.is_set() and self.is_listening:
                    try:
                        # Get audio data with timeout
                        data = self.audio_queue.get(timeout=0.5)
                    except queue.Empty:
                        continue
                    
                    # Process audio
                    if recognizer.AcceptWaveform(data):
                        # Final result
                        result = json.loads(recognizer.Result())
                        text = result.get("text", "").strip()
                        
                        if text:
                            print(f"  📝 Final: {text}")
                            if self.on_speech_recognized:
                                self.on_speech_recognized(text)
                    else:
                        # Partial result
                        partial = json.loads(recognizer.PartialResult())
                        partial_text = partial.get("partial", "").strip()
                        
                        if partial_text and self.on_partial_result:
                            self.on_partial_result(partial_text)
        
        except sd.PortAudioError as e:
            error_msg = f"Audio device error: {e}"
            print(f"  ❌ {error_msg}")
            if self.on_error:
                self.on_error(error_msg)
        except Exception as e:
            error_msg = f"Listener error: {e}"
            print(f"  ❌ {error_msg}")
            if self.on_error:
                self.on_error(error_msg)
        finally:
            print("  🎤 Listen loop ended")
            self.is_listening = False
            if self.on_listening_stopped:
                self.on_listening_stopped()
    
    def stop_listening(self):
        """Stop listening for speech."""
        print("🎤 Stopping listener...")
        self._stop_event.set()
        self.is_listening = False
        
        # Clear the queue to unblock the thread
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except queue.Empty:
                break
        
        # Wait for thread to finish
        if self._listen_thread and self._listen_thread.is_alive():
            self._listen_thread.join(timeout=2.0)
    
    def listen_once(self, timeout: float = 5.0) -> Optional[str]:
        """
        Listen for a single utterance.
        
        Args:
            timeout: Maximum time to wait for speech
            
        Returns:
            Recognized text or None
        """
        result_text = None
        result_event = threading.Event()
        
        def on_result(text):
            nonlocal result_text
            result_text = text
            result_event.set()
        
        # Temporarily set callback
        old_callback = self.on_speech_recognized
        self.on_speech_recognized = on_result
        
        self.start_listening()
        
        # Wait for result or timeout
        result_event.wait(timeout=timeout)
        
        self.stop_listening()
        
        # Restore callback
        self.on_speech_recognized = old_callback
        
        return result_text
    
    def is_available(self) -> bool:
        """Check if listener is properly initialized."""
        return VOSK_AVAILABLE and len(self.models) > 0


class ActivationListener(Listener):
    """
    Special listener for Winter Soldier activation sequence.
    Validates words in order.
    """
    
    def __init__(self):
        super().__init__(language="en")  # Activation is always in English
        self.current_word_index = 0
        self.on_word_validated: Optional[Callable[[int, str], None]] = None
        self.on_activation_complete: Optional[Callable[[], None]] = None
        self.on_activation_failed: Optional[Callable[[str], None]] = None
    
    def reset(self):
        """Reset activation sequence."""
        self.current_word_index = 0
    
    def validate_word(self, spoken_text: str) -> bool:
        """
        Validate spoken word against expected sequence.
        
        Args:
            spoken_text: Text that was spoken
            
        Returns:
            True if word was valid and sequence continues
        """
        from config.activation_words import ActivationWords
        
        # Check each word in the spoken text
        words = spoken_text.lower().split()
        
        for word in words:
            if ActivationWords.validate_word(word, self.current_word_index):
                if self.on_word_validated:
                    self.on_word_validated(self.current_word_index, word)
                
                self.current_word_index += 1
                
                # Check if sequence complete
                if self.current_word_index >= len(ActivationWords.SEQUENCE):
                    if self.on_activation_complete:
                        self.on_activation_complete()
                    return True
        
        return False


# Test function
def test_listener():
    """Test the listener."""
    print("🎤 Testing listener...")
    
    listener = Listener(language="en")
    
    if not listener.is_available():
        print("❌ Listener not available")
        return
    
    print("✅ Listener is available")
    print("🎤 Listening for 10 seconds... Speak something!")
    
    def on_speech(text):
        print(f"   Heard: {text}")
    
    def on_partial(text):
        print(f"   Partial: {text}")
    
    listener.on_speech_recognized = on_speech
    listener.on_partial_result = on_partial
    
    listener.start_listening()
    
    # Listen for 10 seconds
    time.sleep(10)
    
    listener.stop_listening()
    print("🎤 Test complete")


if __name__ == "__main__":
    test_listener()

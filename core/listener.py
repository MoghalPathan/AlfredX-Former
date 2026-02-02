"""
AlfredX Listener Module
=======================
Handles speech recognition using Vosk for offline processing.
Supports both English and Turkish.
"""

import json
import queue
import threading
from typing import Optional, Callable
import sounddevice as sd
import numpy as np
from vosk import Model, KaldiRecognizer

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
        
        # Load models
        self.models = {}
        self.recognizers = {}
        self._load_models()
        
        # Callbacks
        self.on_speech_recognized: Optional[Callable[[str], None]] = None
        self.on_partial_result: Optional[Callable[[str], None]] = None
        self.on_listening_started: Optional[Callable[[], None]] = None
        self.on_listening_stopped: Optional[Callable[[], None]] = None
    
    def _load_models(self):
        """Load Vosk models for all supported languages."""
        # English model
        if Settings.MODEL_EN_PATH.exists():
            try:
                self.models["en"] = Model(str(Settings.MODEL_EN_PATH))
                self.recognizers["en"] = KaldiRecognizer(
                    self.models["en"], 
                    Settings.SAMPLE_RATE
                )
                self.recognizers["en"].SetWords(True)
                print("✅ English Vosk model loaded")
            except Exception as e:
                print(f"❌ Failed to load English model: {e}")
        
        # Turkish model
        if Settings.MODEL_TR_PATH.exists():
            try:
                self.models["tr"] = Model(str(Settings.MODEL_TR_PATH))
                self.recognizers["tr"] = KaldiRecognizer(
                    self.models["tr"], 
                    Settings.SAMPLE_RATE
                )
                self.recognizers["tr"].SetWords(True)
                print("✅ Turkish Vosk model loaded")
            except Exception as e:
                print(f"❌ Failed to load Turkish model: {e}")
    
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
    
    def _audio_callback(self, indata, frames, time, status):
        """Callback for audio input stream."""
        if status:
            print(f"Audio status: {status}")
        self.audio_queue.put(bytes(indata))
    
    def start_listening(self):
        """Start listening for speech."""
        if self.is_listening:
            return
        
        if self.language not in self.recognizers:
            print(f"❌ No recognizer for language: {self.language}")
            return
        
        self.is_listening = True
        self._stop_event.clear()
        
        if self.on_listening_started:
            self.on_listening_started()
        
        # Start audio stream
        self._listen_thread = threading.Thread(target=self._listen_loop)
        self._listen_thread.daemon = True
        self._listen_thread.start()
    
    def _listen_loop(self):
        """Main listening loop in separate thread."""
        try:
            with sd.RawInputStream(
                samplerate=Settings.SAMPLE_RATE,
                blocksize=8000,
                dtype="int16",
                channels=1,
                callback=self._audio_callback
            ):
                while not self._stop_event.is_set():
                    try:
                        data = self.audio_queue.get(timeout=0.5)
                    except queue.Empty:
                        continue
                    
                    recognizer = self.recognizers[self.language]
                    
                    if recognizer.AcceptWaveform(data):
                        # Final result
                        result = json.loads(recognizer.Result())
                        text = result.get("text", "").strip()
                        
                        if text and self.on_speech_recognized:
                            self.on_speech_recognized(text)
                    else:
                        # Partial result
                        partial = json.loads(recognizer.PartialResult())
                        partial_text = partial.get("partial", "").strip()
                        
                        if partial_text and self.on_partial_result:
                            self.on_partial_result(partial_text)
        
        except Exception as e:
            print(f"❌ Listener error: {e}")
        finally:
            self.is_listening = False
            if self.on_listening_stopped:
                self.on_listening_stopped()
    
    def stop_listening(self):
        """Stop listening for speech."""
        self._stop_event.set()
        self.is_listening = False
        
        # Clear the queue
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except queue.Empty:
                break
    
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
    
    def get_audio_level(self) -> float:
        """
        Get current audio input level (0.0 to 1.0).
        Useful for visual feedback.
        """
        try:
            # Read a small chunk of audio
            chunk = sd.rec(
                frames=1024, 
                samplerate=Settings.SAMPLE_RATE, 
                channels=1, 
                dtype="int16"
            )
            sd.wait()
            
            # Calculate RMS level
            rms = np.sqrt(np.mean(chunk.astype(float) ** 2))
            # Normalize to 0-1 range
            level = min(1.0, rms / 10000)
            return level
        except:
            return 0.0
    
    def is_available(self) -> bool:
        """Check if listener is properly initialized."""
        return len(self.models) > 0


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

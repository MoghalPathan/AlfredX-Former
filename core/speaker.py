"""
AlfredX Speaker Module
======================
Handles text-to-speech using Edge-TTS (Microsoft voices).
Supports both English (British butler) and Turkish (casual).
"""

import asyncio
import tempfile
import threading
from pathlib import Path
from typing import Optional, Callable
import edge_tts
import pygame

from config.settings import Settings


class Speaker:
    """
    Text-to-speech using Microsoft Edge-TTS.
    Free, high-quality voices for English and Turkish.
    """
    
    def __init__(self):
        """Initialize the speaker."""
        self.language = "en"
        self.is_speaking = False
        self._stop_event = threading.Event()
        
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
        
        # Voice settings
        self.voices = {
            "en": Settings.VOICE_EN,  # British voice
            "tr": Settings.VOICE_TR,  # Turkish voice
        }
        
        # Speech rate and pitch
        self.rate = "+0%"  # Normal speed
        self.pitch = "+0Hz"  # Normal pitch
        
        # Callbacks
        self.on_speaking_started: Optional[Callable[[], None]] = None
        self.on_speaking_finished: Optional[Callable[[], None]] = None
        
        # Temp directory for audio files
        self.temp_dir = Path(tempfile.gettempdir()) / "alfredx_audio"
        self.temp_dir.mkdir(exist_ok=True)
    
    def set_language(self, language: str):
        """
        Switch TTS language.
        
        Args:
            language: "en" or "tr"
        """
        if language in self.voices:
            self.language = language
            print(f"🔊 Voice switched to: {self.voices[language]}")
    
    def set_rate(self, rate: int):
        """
        Set speech rate.
        
        Args:
            rate: Percentage (-50 to +50)
        """
        self.rate = f"{rate:+d}%"
    
    def set_pitch(self, pitch: int):
        """
        Set speech pitch.
        
        Args:
            pitch: Hz adjustment (-50 to +50)
        """
        self.pitch = f"{pitch:+d}Hz"
    
    async def _generate_speech(self, text: str) -> Optional[Path]:
        """
        Generate speech audio file.
        
        Args:
            text: Text to convert to speech
            
        Returns:
            Path to generated audio file
        """
        try:
            voice = self.voices.get(self.language, self.voices["en"])
            
            communicate = edge_tts.Communicate(
                text=text,
                voice=voice,
                rate=self.rate,
                pitch=self.pitch
            )
            
            # Generate unique filename
            audio_file = self.temp_dir / f"speech_{hash(text)}.mp3"
            
            await communicate.save(str(audio_file))
            
            return audio_file
        
        except Exception as e:
            print(f"❌ TTS generation error: {e}")
            return None
    
    def _play_audio(self, audio_file: Path):
        """
        Play audio file using pygame.
        
        Args:
            audio_file: Path to audio file
        """
        try:
            pygame.mixer.music.load(str(audio_file))
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy() and not self._stop_event.is_set():
                pygame.time.Clock().tick(10)
        
        except Exception as e:
            print(f"❌ Audio playback error: {e}")
    
    def speak(self, text: str, block: bool = False):
        """
        Speak the given text.
        
        Args:
            text: Text to speak
            block: If True, wait until speech is complete
        """
        if self.is_speaking:
            self.stop()
        
        self._stop_event.clear()
        
        def _speak_thread():
            self.is_speaking = True
            
            if self.on_speaking_started:
                self.on_speaking_started()
            
            try:
                # Generate audio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                audio_file = loop.run_until_complete(self._generate_speech(text))
                loop.close()
                
                if audio_file and audio_file.exists():
                    self._play_audio(audio_file)
                    
                    # Clean up temp file
                    try:
                        audio_file.unlink()
                    except:
                        pass
            
            except Exception as e:
                print(f"❌ Speak error: {e}")
            
            finally:
                self.is_speaking = False
                if self.on_speaking_finished:
                    self.on_speaking_finished()
        
        thread = threading.Thread(target=_speak_thread)
        thread.daemon = True
        thread.start()
        
        if block:
            thread.join()
    
    def speak_async(self, text: str):
        """
        Speak without blocking (convenience method).
        
        Args:
            text: Text to speak
        """
        self.speak(text, block=False)
    
    def stop(self):
        """Stop current speech."""
        self._stop_event.set()
        try:
            pygame.mixer.music.stop()
        except:
            pass
        self.is_speaking = False
    
    def is_available(self) -> bool:
        """Check if speaker is properly initialized."""
        return pygame.mixer.get_init() is not None
    
    @staticmethod
    async def list_voices() -> list:
        """
        List all available Edge-TTS voices.
        
        Returns:
            List of voice dictionaries
        """
        voices = await edge_tts.list_voices()
        return voices
    
    @staticmethod
    def get_english_voices() -> list:
        """Get list of English voice names."""
        return [
            "en-GB-RyanNeural",      # British male (recommended)
            "en-GB-SoniaNeural",     # British female
            "en-GB-LibbyNeural",     # British female
            "en-US-GuyNeural",       # American male
            "en-US-JennyNeural",     # American female
            "en-AU-WilliamNeural",   # Australian male
        ]
    
    @staticmethod
    def get_turkish_voices() -> list:
        """Get list of Turkish voice names."""
        return [
            "tr-TR-AhmetNeural",     # Turkish male (recommended)
            "tr-TR-EmelNeural",      # Turkish female
        ]
    
    def cleanup(self):
        """Clean up temporary files and resources."""
        try:
            pygame.mixer.quit()
            # Remove temp audio files
            for f in self.temp_dir.glob("speech_*.mp3"):
                try:
                    f.unlink()
                except:
                    pass
        except:
            pass

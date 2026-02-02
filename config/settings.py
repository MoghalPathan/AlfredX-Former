"""
AlfredX Settings Configuration
==============================
Central configuration for the entire application.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings and configuration."""
    
    # ===== PATHS =====
    BASE_DIR = Path(__file__).parent.parent
    ASSETS_DIR = BASE_DIR / "assets"
    ICONS_DIR = ASSETS_DIR / "icons"
    SOUNDS_DIR = ASSETS_DIR / "sounds"
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    
    # Vosk Models
    MODEL_EN_PATH = BASE_DIR / "model-en"
    MODEL_TR_PATH = BASE_DIR / "model-tr"
    
    # ===== API KEYS =====
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
    
    # ===== AI SETTINGS =====
    AI_MODEL = "llama-3.1-70b-versatile"  # Groq model
    AI_MAX_TOKENS = 1024
    AI_TEMPERATURE = 0.7
    
    # ===== VOICE SETTINGS =====
    # English - British Butler voice
    VOICE_EN = os.getenv("ALFRED_VOICE_EN", "en-GB-RyanNeural")
    # Turkish - Normal voice
    VOICE_TR = os.getenv("ALFRED_VOICE_TR", "tr-TR-AhmetNeural")
    
    # Speech recognition
    SAMPLE_RATE = 16000
    SILENCE_THRESHOLD = 0.5  # seconds of silence to stop listening
    
    # ===== LANGUAGE SETTINGS =====
    DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "auto")
    SUPPORTED_LANGUAGES = ["en", "tr"]
    
    # ===== LOGIN SETTINGS =====
    TEXT_PASSWORD = "MEZEYAT"
    VOICE_ACTIVATION_TIMEOUT = 30  # seconds to complete voice activation
    
    # ===== GUI SETTINGS =====
    WINDOW_TITLE = "AlfredX: Waynecore Assistant"
    WINDOW_WIDTH = 1600
    WINDOW_HEIGHT = 900
    FULLSCREEN = False
    
    # ===== COLORS (JARVIS Theme) =====
    class Colors:
        CYAN = "#00f7ff"
        CYAN_BRIGHT = "#00ffff"
        CYAN_DIM = "#00a8b3"
        CYAN_DARK = "#005f66"
        TEAL = "#00d4aa"
        BLUE = "#0088ff"
        DARK = "#000000"
        DARK_BLUE = "#000a0f"
        PANEL_BG = "rgba(5, 10, 25, 0.85)"
        WHITE = "#ffffff"
        RED = "#ff3333"
        GREEN = "#00ff88"
        WARNING = "#ffaa00"
    
    # ===== SYSTEM COMMANDS =====
    # Apps that can be opened
    KNOWN_APPS = {
        "chrome": "chrome.exe",
        "firefox": "firefox.exe",
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "explorer": "explorer.exe",
        "vscode": "code",
        "vs code": "code",
        "spotify": "spotify.exe",
        "discord": "discord.exe",
        "word": "WINWORD.EXE",
        "excel": "EXCEL.EXE",
        "powerpoint": "POWERPNT.EXE",
        "terminal": "wt.exe",
        "cmd": "cmd.exe",
    }
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)
        cls.ASSETS_DIR.mkdir(exist_ok=True)
        cls.ICONS_DIR.mkdir(exist_ok=True)
        cls.SOUNDS_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def validate(cls):
        """Validate critical settings."""
        errors = []
        
        if not cls.GROQ_API_KEY:
            errors.append("GROQ_API_KEY not set in .env file")
        
        if not cls.MODEL_EN_PATH.exists():
            errors.append(f"English Vosk model not found at {cls.MODEL_EN_PATH}")
        
        if not cls.MODEL_TR_PATH.exists():
            errors.append(f"Turkish Vosk model not found at {cls.MODEL_TR_PATH}")
        
        return errors


# Initialize directories on import
Settings.ensure_directories()

"""
AlfredX Language Detector
=========================
Automatically detects whether user is speaking English or Turkish.
"""

import re
from typing import Tuple


class LanguageDetector:
    """
    Detects language from text input.
    Supports English and Turkish.
    """
    
    # Common Turkish-specific characters and words
    TURKISH_CHARS = set("çğıöşüÇĞİÖŞÜ")
    
    TURKISH_WORDS = {
        # Common words
        "ve", "bir", "bu", "da", "de", "için", "ile", "mi", "mı", "mu", "mü",
        "ne", "nasıl", "neden", "nerede", "kim", "hangi", "kaç",
        # Pronouns
        "ben", "sen", "biz", "siz", "onlar",
        # Verbs
        "aç", "kapat", "çalıştır", "başlat", "bul", "ara", "göster",
        "yap", "yapabilir", "yardım", "evet", "hayır", "tamam",
        # Greetings
        "merhaba", "selam", "günaydın", "iyi", "akşamlar", "geceler",
        "teşekkür", "teşekkürler", "sağol", "hoşçakal", "görüşürüz",
        # Common nouns
        "hava", "saat", "müzik", "dosya", "klasör", "bilgisayar",
        "ekran", "ses", "pencere", "program", "uygulama",
        # Question words
        "nasılsın", "napıyorsun", "naber",
    }
    
    ENGLISH_WORDS = {
        # Common words
        "the", "a", "an", "is", "are", "was", "were", "be", "been",
        "have", "has", "had", "do", "does", "did", "will", "would",
        "can", "could", "should", "may", "might", "must",
        # Pronouns
        "i", "you", "he", "she", "it", "we", "they", "my", "your",
        # Common verbs
        "open", "close", "start", "stop", "play", "pause", "find",
        "search", "show", "help", "please", "thanks", "thank",
        # Greetings
        "hello", "hi", "hey", "good", "morning", "evening", "night",
        "bye", "goodbye", "yes", "no", "okay",
        # Questions
        "what", "where", "when", "why", "how", "who", "which",
        # Common nouns
        "weather", "time", "music", "file", "folder", "computer",
        "screen", "volume", "window", "app", "application",
    }
    
    @classmethod
    def detect(cls, text: str) -> Tuple[str, float]:
        """
        Detect language of given text.
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (language_code, confidence)
            language_code: "en" or "tr"
            confidence: 0.0 to 1.0
        """
        if not text:
            return "en", 0.0
        
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        if not words:
            return "en", 0.0
        
        # Check for Turkish-specific characters
        has_turkish_chars = any(char in cls.TURKISH_CHARS for char in text)
        
        # Count word matches
        turkish_count = sum(1 for word in words if word in cls.TURKISH_WORDS)
        english_count = sum(1 for word in words if word in cls.ENGLISH_WORDS)
        
        total_words = len(words)
        
        # Calculate scores
        turkish_score = turkish_count / total_words if total_words > 0 else 0
        english_score = english_count / total_words if total_words > 0 else 0
        
        # Boost Turkish score if Turkish characters found
        if has_turkish_chars:
            turkish_score += 0.5
        
        # Determine language
        if turkish_score > english_score:
            confidence = min(1.0, turkish_score)
            return "tr", confidence
        elif english_score > turkish_score:
            confidence = min(1.0, english_score)
            return "en", confidence
        else:
            # Default to English if uncertain
            return "en", 0.5
    
    @classmethod
    def is_turkish(cls, text: str) -> bool:
        """
        Quick check if text is likely Turkish.
        
        Args:
            text: Input text
            
        Returns:
            True if text appears to be Turkish
        """
        lang, conf = cls.detect(text)
        return lang == "tr" and conf > 0.3
    
    @classmethod
    def is_english(cls, text: str) -> bool:
        """
        Quick check if text is likely English.
        
        Args:
            text: Input text
            
        Returns:
            True if text appears to be English
        """
        lang, conf = cls.detect(text)
        return lang == "en" and conf > 0.3
    
    @classmethod
    def detect_and_switch(cls, text: str, current_language: str) -> Tuple[str, bool]:
        """
        Detect language and determine if switch is needed.
        
        Args:
            text: Input text
            current_language: Current language setting
            
        Returns:
            Tuple of (detected_language, should_switch)
        """
        detected, confidence = cls.detect(text)
        
        # Only switch if confidence is high enough
        should_switch = (
            detected != current_language 
            and confidence > 0.5
        )
        
        return detected, should_switch


# Quick test
if __name__ == "__main__":
    test_phrases = [
        "Open Chrome browser",
        "Merhaba nasılsın",
        "What's the weather like",
        "Müzik çal",
        "Play some music",
        "Saat kaç",
        "Hello Alfred",
        "Chrome'u aç",
    ]
    
    for phrase in test_phrases:
        lang, conf = LanguageDetector.detect(phrase)
        print(f"'{phrase}' -> {lang} ({conf:.2f})")

"""
AlfredX Command Parser
======================
Parses user commands and routes them to appropriate skills.
"""

import re
from typing import Dict, Optional, Callable, Any
from dataclasses import dataclass

from config.settings import Settings


@dataclass
class ParsedCommand:
    """Represents a parsed command."""
    intent: str
    action: str
    target: Optional[str] = None
    value: Optional[Any] = None
    confidence: float = 0.0
    original_text: str = ""
    language: str = "en"


class CommandParser:
    """
    Parses natural language commands into actionable intents.
    Supports both English and Turkish.
    """
    
    # Command patterns for English
    PATTERNS_EN = {
        "open_app": [
            r"(?:open|launch|start|run)\s+(?:the\s+)?(.+?)(?:\s+app|\s+application|\s+program)?$",
            r"(?:can you\s+)?open\s+(.+)",
        ],
        "close_app": [
            r"(?:close|exit|quit|kill|terminate)\s+(?:the\s+)?(.+?)(?:\s+app|\s+application|\s+program)?$",
        ],
        "search_web": [
            r"(?:search|google|look up|find)\s+(?:for\s+)?(.+)",
            r"(?:what is|who is|what are|where is)\s+(.+)",
        ],
        "play_media": [
            r"(?:play|start)\s+(?:some\s+)?(?:music|song|video|media)",
            r"play\s+(.+)",
        ],
        "pause_media": [
            r"(?:pause|stop)\s+(?:the\s+)?(?:music|song|video|media|playback)",
            r"pause",
            r"stop",
        ],
        "next_track": [
            r"(?:next|skip)\s+(?:track|song|video)?",
            r"skip",
        ],
        "previous_track": [
            r"(?:previous|last|back)\s+(?:track|song|video)?",
            r"go back",
        ],
        "volume_up": [
            r"(?:increase|raise|turn up|up)\s+(?:the\s+)?volume",
            r"volume up",
            r"louder",
        ],
        "volume_down": [
            r"(?:decrease|lower|turn down|down)\s+(?:the\s+)?volume",
            r"volume down",
            r"quieter",
        ],
        "volume_set": [
            r"set\s+(?:the\s+)?volume\s+(?:to\s+)?(\d+)",
            r"volume\s+(?:to\s+)?(\d+)",
        ],
        "mute": [
            r"mute",
            r"silence",
            r"shut up",
        ],
        "unmute": [
            r"unmute",
            r"sound on",
        ],
        "weather": [
            r"(?:what(?:'s| is)\s+(?:the\s+)?)?weather",
            r"(?:how(?:'s| is)\s+(?:the\s+)?)?weather",
            r"temperature",
            r"is it (?:going to\s+)?rain",
        ],
        "time": [
            r"(?:what(?:'s| is)\s+(?:the\s+)?)?time",
            r"what time is it",
            r"current time",
        ],
        "date": [
            r"(?:what(?:'s| is)\s+(?:the\s+|today(?:'s)?\s+)?)?date",
            r"what day is (?:it|today)",
        ],
        "screenshot": [
            r"(?:take\s+(?:a\s+)?)?screenshot",
            r"capture\s+(?:the\s+)?screen",
        ],
        "system_info": [
            r"(?:show\s+)?(?:system\s+)?(?:info|information|status|stats)",
            r"(?:how much\s+)?(?:cpu|memory|ram|disk)",
        ],
        "help": [
            r"(?:what\s+can\s+you\s+do|help|commands|abilities)",
            r"help me",
        ],
        "greeting": [
            r"^(?:hi|hello|hey|good\s+(?:morning|afternoon|evening|night))(?:\s+alfred)?$",
        ],
        "goodbye": [
            r"^(?:bye|goodbye|see you|exit|quit|farewell)(?:\s+alfred)?$",
        ],
        "thanks": [
            r"^(?:thanks|thank you|thx|cheers)(?:\s+alfred)?$",
        ],
        "switch_language": [
            r"(?:switch\s+(?:to\s+)?|speak\s+)(?:turkish|türkçe)",
            r"(?:switch\s+(?:to\s+)?|speak\s+)(?:english|ingilizce)",
        ],
    }
    
    # Command patterns for Turkish
    PATTERNS_TR = {
        "open_app": [
            r"(.+?)\s*(?:uygulamasını|programını)?\s*aç",
            r"(.+?)\s*(?:ı|i|u|ü)?\s*çalıştır",
            r"(.+?)\s*(?:ı|i|u|ü)?\s*başlat",
        ],
        "close_app": [
            r"(.+?)\s*(?:uygulamasını|programını)?\s*kapat",
            r"(.+?)\s*(?:ı|i|u|ü)?\s*(?:dan|den)\s*çık",
        ],
        "search_web": [
            r"(.+?)\s*(?:ı|i|u|ü)?\s*ara",
            r"(.+?)\s*(?:ı|i|u|ü)?\s*bul",
            r"(.+)\s+nedir",
            r"(.+)\s+kimdir",
        ],
        "play_media": [
            r"(?:müzik|şarkı|video)\s*(?:çal|oynat|başlat)",
            r"(.+?)\s*(?:ı|i|u|ü)?\s*çal",
        ],
        "pause_media": [
            r"(?:müzik|şarkı|video|oynatma)\s*(?:ı|i|u|ü)?\s*durdur",
            r"durdur",
            r"beklet",
        ],
        "volume_up": [
            r"ses(?:i)?\s*(?:aç|yükselt|artır)",
            r"daha\s+yüksek",
        ],
        "volume_down": [
            r"ses(?:i)?\s*(?:kıs|azalt|düşür)",
            r"daha\s+alçak",
        ],
        "mute": [
            r"sessiz",
            r"sustur",
            r"ses(?:i)?\s*kapat",
        ],
        "weather": [
            r"hava\s*(?:durumu|nasıl)?",
            r"sıcaklık",
            r"yağmur\s*(?:yağacak\s*mı)?",
        ],
        "time": [
            r"saat\s*(?:kaç)?",
            r"şu\s*an\s*saat",
        ],
        "date": [
            r"(?:bugün(?:ün)?\s*)?tarih(?:i)?",
            r"bugün\s+(?:günlerden\s+)?ne",
        ],
        "screenshot": [
            r"ekran\s*görüntüsü\s*(?:al)?",
        ],
        "system_info": [
            r"sistem\s*(?:bilgisi|durumu)?",
            r"(?:cpu|ram|disk)\s*(?:kullanımı|durumu)?",
        ],
        "help": [
            r"(?:ne\s+yapabilirsin|yardım|komutlar)",
        ],
        "greeting": [
            r"^(?:merhaba|selam|günaydın|iyi\s+(?:günler|akşamlar|geceler))(?:\s+alfred)?$",
        ],
        "goodbye": [
            r"^(?:görüşürüz|hoşça\s*kal|bay\s*bay|çıkış)(?:\s+alfred)?$",
        ],
        "thanks": [
            r"^(?:teşekkür(?:ler)?|sağ\s*ol)(?:\s+alfred)?$",
        ],
        "switch_language": [
            r"(?:ingilizce(?:ye)?|english)\s*(?:geç|konuş)",
            r"(?:türkçe(?:ye)?|turkish)\s*(?:geç|konuş)",
        ],
    }
    
    # App name mappings for Turkish
    APP_NAMES_TR = {
        "krom": "chrome",
        "tarayıcı": "chrome",
        "not defteri": "notepad",
        "hesap makinesi": "calculator",
        "dosyalar": "explorer",
        "dosya gezgini": "explorer",
        "terminal": "terminal",
        "komut satırı": "cmd",
    }
    
    def __init__(self):
        """Initialize the command parser."""
        self.language = "en"
        self.custom_commands: Dict[str, Callable] = {}
    
    def set_language(self, language: str):
        """Set parsing language."""
        self.language = language
    
    def parse(self, text: str) -> ParsedCommand:
        """
        Parse user input into a command.
        
        Args:
            text: User's spoken/typed text
            
        Returns:
            ParsedCommand object
        """
        text = text.strip().lower()
        
        patterns = self.PATTERNS_TR if self.language == "tr" else self.PATTERNS_EN
        
        for intent, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    target = None
                    value = None
                    
                    # Extract captured groups
                    if match.groups():
                        captured = match.group(1)
                        
                        # Check if it's a number (for volume)
                        if captured and captured.isdigit():
                            value = int(captured)
                        else:
                            target = captured
                            
                            # Translate Turkish app names
                            if self.language == "tr" and target in self.APP_NAMES_TR:
                                target = self.APP_NAMES_TR[target]
                    
                    return ParsedCommand(
                        intent=intent,
                        action=self._get_action(intent),
                        target=target,
                        value=value,
                        confidence=0.9,
                        original_text=text,
                        language=self.language
                    )
        
        # No pattern matched - return conversation intent
        return ParsedCommand(
            intent="conversation",
            action="chat",
            original_text=text,
            confidence=0.5,
            language=self.language
        )
    
    def _get_action(self, intent: str) -> str:
        """Map intent to action name."""
        action_map = {
            "open_app": "open",
            "close_app": "close",
            "search_web": "search",
            "play_media": "play",
            "pause_media": "pause",
            "next_track": "next",
            "previous_track": "previous",
            "volume_up": "volume_up",
            "volume_down": "volume_down",
            "volume_set": "volume_set",
            "mute": "mute",
            "unmute": "unmute",
            "weather": "weather",
            "time": "time",
            "date": "date",
            "screenshot": "screenshot",
            "system_info": "system_info",
            "help": "help",
            "greeting": "greet",
            "goodbye": "goodbye",
            "thanks": "thanks",
            "switch_language": "switch_language",
        }
        return action_map.get(intent, intent)
    
    def register_custom_command(self, pattern: str, callback: Callable):
        """
        Register a custom command pattern.
        
        Args:
            pattern: Regex pattern
            callback: Function to call when matched
        """
        self.custom_commands[pattern] = callback


# Quick test
if __name__ == "__main__":
    parser = CommandParser()
    
    test_commands = [
        ("en", "Open Chrome"),
        ("en", "What's the weather like"),
        ("en", "Play some music"),
        ("en", "Set volume to 50"),
        ("tr", "Chrome'u aç"),
        ("tr", "Hava durumu nasıl"),
        ("tr", "Müzik çal"),
        ("tr", "Sesi kıs"),
    ]
    
    for lang, cmd in test_commands:
        parser.set_language(lang)
        result = parser.parse(cmd)
        print(f"[{lang}] '{cmd}' -> {result.intent} (target: {result.target}, value: {result.value})")

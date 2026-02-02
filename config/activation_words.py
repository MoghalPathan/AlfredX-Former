"""
AlfredX Activation Words
========================
Winter Soldier Protocol - Batman Themed
10 words must be spoken in sequence to activate Alfred.
"""


class ActivationWords:
    """Batman-themed activation sequence (Winter Soldier Protocol)."""
    
    # The 10 activation words in order
    SEQUENCE = [
        "gotham",
        "shadow", 
        "knight",
        "legacy",
        "protocol",
        "guardian",
        "vengeance",
        "justice",
        "wayne",
        "activate"
    ]
    
    # Alternative accepted pronunciations (Vosk might hear differently)
    ALTERNATIVES = {
        "gotham": ["gotham", "goth am", "got ham"],
        "shadow": ["shadow", "shadows"],
        "knight": ["knight", "night", "knights"],
        "legacy": ["legacy", "legasy"],
        "protocol": ["protocol", "protocols"],
        "guardian": ["guardian", "guardians"],
        "vengeance": ["vengeance", "vengence", "revenge"],
        "justice": ["justice", "justis"],
        "wayne": ["wayne", "wane", "rain"],  # rain sounds similar
        "activate": ["activate", "activated", "activating"]
    }
    
    # Responses after each word (for dramatic effect)
    WORD_RESPONSES = {
        0: "◆ First protocol word accepted...",
        1: "◆ Shadows recognized...",
        2: "◆ Dark Knight protocol loading...",
        3: "◆ Wayne legacy confirmed...",
        4: "◆ Protocol sequence initiated...",
        5: "◆ Guardian status verified...",
        6: "◆ Vengeance protocol armed...",
        7: "◆ Justice system online...",
        8: "◆ Wayne identity confirmed...",
        9: "◆ ACTIVATION COMPLETE"
    }
    
    # Final activation message
    ACTIVATION_SUCCESS = """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║     🦇 ALFRED PROTOCOL INITIALIZED 🦇                    ║
    ║                                                          ║
    ║     Good evening, Master Wayne.                          ║
    ║     All systems operational.                             ║
    ║     How may I be of assistance?                          ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    
    ACTIVATION_FAILED = "Voice activation failed. Please try again or use text login."
    
    @classmethod
    def validate_word(cls, spoken_word: str, expected_index: int) -> bool:
        """
        Check if spoken word matches expected word in sequence.
        
        Args:
            spoken_word: The word that was spoken (lowercase)
            expected_index: Index of expected word in sequence
            
        Returns:
            True if word matches, False otherwise
        """
        if expected_index >= len(cls.SEQUENCE):
            return False
        
        expected_word = cls.SEQUENCE[expected_index]
        spoken_word = spoken_word.lower().strip()
        
        # Check exact match
        if spoken_word == expected_word:
            return True
        
        # Check alternatives
        if expected_word in cls.ALTERNATIVES:
            if spoken_word in cls.ALTERNATIVES[expected_word]:
                return True
        
        return False
    
    @classmethod
    def get_progress_text(cls, current_index: int) -> str:
        """Get progress indicator for current activation step."""
        total = len(cls.SEQUENCE)
        filled = "●" * current_index
        empty = "○" * (total - current_index)
        return f"[{filled}{empty}] {current_index}/{total}"
    
    @classmethod
    def get_hint(cls, index: int) -> str:
        """Get hint for next expected word (first letter only)."""
        if index >= len(cls.SEQUENCE):
            return ""
        word = cls.SEQUENCE[index]
        return f"Next word starts with: {word[0].upper()}..."

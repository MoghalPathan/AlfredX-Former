"""
AlfredX Brain Module
====================
AI integration using Groq API (Llama 3).
Handles conversation, intent recognition, and smart responses.
"""

from typing import Optional, List, Dict
from groq import Groq

from config.settings import Settings
from config.personas import Personas


class Brain:
    """
    AI brain using Groq's Llama 3 model.
    Handles natural language understanding and response generation.
    """
    
    def __init__(self):
        """Initialize the brain."""
        self.client = None
        self.language = "en"
        self.conversation_history: List[Dict] = []
        self.max_history = 10  # Keep last 10 exchanges
        
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Groq client."""
        if Settings.GROQ_API_KEY:
            try:
                self.client = Groq(api_key=Settings.GROQ_API_KEY)
                print("✅ Groq AI client initialized")
            except Exception as e:
                print(f"❌ Failed to initialize Groq client: {e}")
                self.client = None
        else:
            print("⚠️ GROQ_API_KEY not set - AI features disabled")
    
    def set_language(self, language: str):
        """
        Set conversation language.
        
        Args:
            language: "en" or "tr"
        """
        self.language = language
        # Clear history when language changes
        self.conversation_history = []
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for current language."""
        return Personas.get_system_prompt(self.language)
    
    def _build_messages(self, user_input: str) -> List[Dict]:
        """
        Build message list for API call.
        
        Args:
            user_input: User's message
            
        Returns:
            List of message dictionaries
        """
        messages = [
            {"role": "system", "content": self._get_system_prompt()}
        ]
        
        # Add conversation history
        messages.extend(self.conversation_history)
        
        # Add current user input
        messages.append({"role": "user", "content": user_input})
        
        return messages
    
    def think(self, user_input: str) -> str:
        """
        Process user input and generate response.
        
        Args:
            user_input: What the user said
            
        Returns:
            Alfred's response
        """
        if not self.client:
            return self._fallback_response(user_input)
        
        try:
            messages = self._build_messages(user_input)
            
            response = self.client.chat.completions.create(
                model=Settings.AI_MODEL,
                messages=messages,
                max_tokens=Settings.AI_MAX_TOKENS,
                temperature=Settings.AI_TEMPERATURE,
            )
            
            assistant_message = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            # Trim history if too long
            if len(self.conversation_history) > self.max_history * 2:
                self.conversation_history = self.conversation_history[-self.max_history * 2:]
            
            return assistant_message
        
        except Exception as e:
            print(f"❌ AI error: {e}")
            return self._fallback_response(user_input)
    
    def _fallback_response(self, user_input: str) -> str:
        """
        Generate fallback response when AI is unavailable.
        
        Args:
            user_input: User's message
            
        Returns:
            Simple fallback response
        """
        user_lower = user_input.lower()
        
        # Simple keyword matching for basic functionality
        if any(word in user_lower for word in ["hello", "hi", "hey", "merhaba", "selam"]):
            return Personas.get_greeting(self.language)
        
        if any(word in user_lower for word in ["bye", "goodbye", "exit", "quit", "görüşürüz", "hoşçakal"]):
            return Personas.get_goodbye(self.language)
        
        if any(word in user_lower for word in ["thanks", "thank you", "teşekkür", "sağol"]):
            if self.language == "tr":
                return "Rica ederim!"
            return "You're most welcome, sir."
        
        # Default response
        return Personas.get_not_understood(self.language)
    
    def analyze_intent(self, user_input: str) -> Dict:
        """
        Analyze user input to determine intent.
        
        Args:
            user_input: What the user said
            
        Returns:
            Dictionary with intent and entities
        """
        user_lower = user_input.lower()
        
        # Intent patterns
        intents = {
            "open_app": ["open", "launch", "start", "run", "aç", "başlat", "çalıştır"],
            "close_app": ["close", "exit", "quit", "kill", "kapat", "çık"],
            "search_web": ["search", "google", "look up", "find", "ara", "bul"],
            "play_media": ["play", "music", "video", "çal", "oynat", "müzik"],
            "pause_media": ["pause", "stop", "durdur", "beklet"],
            "volume_up": ["volume up", "louder", "sesi aç", "sesi yükselt"],
            "volume_down": ["volume down", "quieter", "sesi kıs", "sesi azalt"],
            "mute": ["mute", "silent", "sessiz", "sustur"],
            "weather": ["weather", "temperature", "hava", "sıcaklık"],
            "time": ["time", "clock", "saat", "zaman"],
            "screenshot": ["screenshot", "capture", "ekran görüntüsü"],
            "greeting": ["hello", "hi", "hey", "merhaba", "selam"],
            "goodbye": ["bye", "goodbye", "exit", "görüşürüz", "hoşçakal"],
            "help": ["help", "what can you do", "yardım", "ne yapabilirsin"],
            "system_info": ["cpu", "memory", "ram", "disk", "system", "sistem"],
            "switch_language": ["switch to turkish", "türkçe", "switch to english", "ingilizce"],
        }
        
        detected_intent = "conversation"  # Default
        confidence = 0.0
        entities = {}
        
        for intent, keywords in intents.items():
            for keyword in keywords:
                if keyword in user_lower:
                    detected_intent = intent
                    confidence = 0.8
                    
                    # Extract entities
                    if intent == "open_app":
                        # Try to find app name
                        for app in Settings.KNOWN_APPS.keys():
                            if app in user_lower:
                                entities["app"] = app
                                break
                    
                    break
            if detected_intent != "conversation":
                break
        
        return {
            "intent": detected_intent,
            "confidence": confidence,
            "entities": entities,
            "original_text": user_input
        }
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
    
    def is_available(self) -> bool:
        """Check if AI brain is available."""
        return self.client is not None

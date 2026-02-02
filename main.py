"""
AlfredX: Waynecore Assistant
============================
Main entry point for the application.

A JARVIS-inspired AI desktop assistant with Batman/Alfred theme.
Features:
- Voice activation (Winter Soldier Protocol)
- Bilingual support (English/Turkish)
- System control
- Media control
- Computer vision
- Natural conversation

Author: [Your Name]
Project: Final Year Computer Engineering
"""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QIcon

from config.settings import Settings
from config.personas import Personas
from core.listener import Listener
from core.speaker import Speaker
from core.brain import Brain
from core.language_detector import LanguageDetector
from core.command_parser import CommandParser
from gui.main_window import MainWindow
from skills.system_control import SystemControl
from skills.media_control import MediaControl


class AlfredX:
    """
    Main application class.
    Coordinates all components.
    """
    
    def __init__(self):
        """Initialize AlfredX."""
        print("🦇 Initializing AlfredX: Waynecore Assistant...")
        
        # Validate settings
        errors = Settings.validate()
        for error in errors:
            print(f"⚠️  {error}")
        
        # Initialize components
        self._init_core()
        self._init_skills()
        self._init_gui()
        self._connect_signals()
        
        print("✅ AlfredX initialized successfully!")
    
    def _init_core(self):
        """Initialize core components."""
        print("  → Loading core modules...")
        
        # Language detection
        self.language_detector = LanguageDetector()
        self.current_language = "en"
        
        # Speech recognition
        self.listener = Listener(language=self.current_language)
        self.listener.on_speech_recognized = self._on_speech_recognized
        
        # Text-to-speech
        self.speaker = Speaker()
        
        # AI brain
        self.brain = Brain()
        
        # Command parser
        self.command_parser = CommandParser()
    
    def _init_skills(self):
        """Initialize skill modules."""
        print("  → Loading skills...")
        
        self.system_control = SystemControl()
        self.media_control = MediaControl()
    
    def _init_gui(self):
        """Initialize GUI."""
        print("  → Loading GUI...")
        
        self.window = MainWindow()
        
        # Set listener for login screen
        self.window.get_login_screen().set_listener(self.listener)
    
    def _connect_signals(self):
        """Connect signals between components."""
        dashboard = self.window.get_dashboard()
        
        # Command from text input
        dashboard.command_entered.connect(self._process_command)
        
        # Mic button
        dashboard.mic_button_clicked.connect(self._toggle_listening)
    
    def _on_speech_recognized(self, text: str):
        """Handle recognized speech."""
        if not text.strip():
            return
        
        print(f"🎤 Heard: {text}")
        
        # Detect language
        detected_lang, should_switch = self.language_detector.detect_and_switch(
            text, self.current_language
        )
        
        if should_switch:
            self._switch_language(detected_lang)
        
        # Add to dashboard
        dashboard = self.window.get_dashboard()
        dashboard.add_user_message(text)
        
        # Process command
        self._process_command(text)
    
    def _process_command(self, text: str):
        """Process a command (voice or text)."""
        dashboard = self.window.get_dashboard()
        
        # Parse command
        self.command_parser.set_language(self.current_language)
        parsed = self.command_parser.parse(text)
        
        print(f"📝 Intent: {parsed.intent}, Target: {parsed.target}")
        
        # Execute based on intent
        response = self._execute_intent(parsed)
        
        # Respond
        dashboard.add_alfred_message(response)
        dashboard.add_activity(f"Processed: {parsed.intent}")
        
        # Speak response
        self.speaker.set_language(self.current_language)
        self.speaker.speak(response)
    
    def _execute_intent(self, parsed) -> str:
        """Execute parsed command and return response."""
        intent = parsed.intent
        target = parsed.target
        value = parsed.value
        
        # System control intents
        if intent == "open_app":
            if target:
                success, msg = self.system_control.open_app(target)
                if success:
                    return Personas.get_acknowledgment(self.current_language) + f" {msg}."
                return Personas.get_error(self.current_language) + f" {msg}."
            return self._ask_for_target("open", self.current_language)
        
        elif intent == "close_app":
            if target:
                success, msg = self.system_control.close_app(target)
                return msg
            return self._ask_for_target("close", self.current_language)
        
        elif intent == "screenshot":
            success, msg = self.system_control.take_screenshot()
            if success:
                return f"Screenshot saved to {msg}"
            return msg
        
        elif intent == "time":
            time_str = self.system_control.get_time()
            if self.current_language == "tr":
                return f"Saat {time_str}"
            return f"The time is {time_str}, sir."
        
        elif intent == "date":
            date_str = self.system_control.get_date()
            if self.current_language == "tr":
                return f"Bugün {date_str}"
            return f"Today is {date_str}, sir."
        
        elif intent == "system_info":
            info = self.system_control.get_system_info()
            if self.current_language == "tr":
                return (f"CPU: {info['cpu']['percent']}%, "
                       f"RAM: {info['memory']['percent']}%, "
                       f"Disk: {info['disk']['percent']}%")
            return (f"System status, sir: CPU at {info['cpu']['percent']}%, "
                   f"Memory at {info['memory']['percent']}%, "
                   f"Disk at {info['disk']['percent']}%.")
        
        # Media control intents
        elif intent == "volume_up":
            success, msg = self.media_control.volume_up()
            return msg
        
        elif intent == "volume_down":
            success, msg = self.media_control.volume_down()
            return msg
        
        elif intent == "volume_set":
            if value:
                success, msg = self.media_control.set_volume(value)
                return msg
            return "What volume level would you like, sir?"
        
        elif intent == "mute":
            success, msg = self.media_control.mute()
            return msg
        
        elif intent == "unmute":
            success, msg = self.media_control.unmute()
            return msg
        
        elif intent == "play_media":
            success, msg = self.media_control.play_pause()
            return msg
        
        elif intent == "pause_media":
            success, msg = self.media_control.play_pause()
            return msg
        
        elif intent == "next_track":
            success, msg = self.media_control.next_track()
            return msg
        
        elif intent == "previous_track":
            success, msg = self.media_control.previous_track()
            return msg
        
        # Greeting/Goodbye
        elif intent == "greeting":
            return Personas.get_greeting(self.current_language)
        
        elif intent == "goodbye":
            return Personas.get_goodbye(self.current_language)
        
        elif intent == "thanks":
            if self.current_language == "tr":
                return "Rica ederim!"
            return "You're most welcome, sir."
        
        # Help
        elif intent == "help":
            return self._get_help_text()
        
        # Language switch
        elif intent == "switch_language":
            if "turkish" in parsed.original_text.lower() or "türkçe" in parsed.original_text.lower():
                self._switch_language("tr")
                return "Tabii, Türkçe konuşabilirim. Nasıl yardımcı olabilirim?"
            else:
                self._switch_language("en")
                return "Certainly, sir. I shall speak in English. How may I assist you?"
        
        # Default: use AI for conversation
        elif intent == "conversation":
            self.brain.set_language(self.current_language)
            return self.brain.think(parsed.original_text)
        
        return Personas.get_not_understood(self.current_language)
    
    def _ask_for_target(self, action: str, language: str) -> str:
        """Ask for missing target."""
        if language == "tr":
            return f"Ne {action}mamı istiyorsunuz?"
        return f"What would you like me to {action}, sir?"
    
    def _get_help_text(self) -> str:
        """Get help text."""
        if self.current_language == "tr":
            return ("Şunları yapabilirim: uygulama açma/kapatma, "
                   "ses kontrolü, müzik kontrolü, sistem bilgisi, "
                   "ekran görüntüsü, web araması ve genel sohbet.")
        return ("I can assist with: opening and closing applications, "
               "volume and media control, system information, "
               "screenshots, web searches, and general conversation, sir.")
    
    def _switch_language(self, language: str):
        """Switch to a different language."""
        self.current_language = language
        self.listener.set_language(language)
        self.speaker.set_language(language)
        self.command_parser.set_language(language)
        self.brain.set_language(language)
        self.window.get_dashboard().set_language(language)
        print(f"🌐 Language switched to: {language}")
    
    def _toggle_listening(self):
        """Toggle voice listening."""
        if self.listener.is_listening:
            self.listener.stop_listening()
            self.window.get_dashboard().set_listening(False)
            print("🎤 Stopped listening")
        else:
            self.listener.start_listening()
            self.window.get_dashboard().set_listening(True)
            print("🎤 Started listening")
    
    def run(self):
        """Run the application."""
        self.window.show()
    
    def cleanup(self):
        """Cleanup resources."""
        print("🦇 Shutting down AlfredX...")
        self.listener.stop_listening()
        self.speaker.cleanup()


def main():
    """Main entry point."""
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("AlfredX")
    app.setOrganizationName("Waynecore")
    
    # High DPI support
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Create and run AlfredX
    alfred = AlfredX()
    alfred.run()
    
    # Execute
    exit_code = app.exec_()
    
    # Cleanup
    alfred.cleanup()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

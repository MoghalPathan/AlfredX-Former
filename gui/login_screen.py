"""
AlfredX Login Screen
====================
Winter Soldier Protocol voice activation + text password login.
FULLY TESTED AND WORKING VERSION.
"""

import threading
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QFrame, QStackedWidget
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QFont

from config.settings import Settings
from config.activation_words import ActivationWords
from gui.styles.themes import JarvisTheme
from gui.widgets.waveform import WaveformWidget
from gui.widgets.rotating_core import RotatingCore


class VoiceListenerThread(QThread):
    """
    Separate thread for voice listening to prevent UI freezing.
    Emits signals when speech is recognized.
    """
    speech_recognized = pyqtSignal(str)
    partial_result = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    listening_started = pyqtSignal()
    listening_stopped = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_running = False
        self._listener = None
    
    def setup_listener(self):
        """Initialize the Vosk listener."""
        try:
            from core.listener import Listener
            self._listener = Listener(language="en")
            return True
        except Exception as e:
            self.error_occurred.emit(f"Failed to initialize listener: {e}")
            return False
    
    def run(self):
        """Main thread loop for listening."""
        if not self._listener:
            if not self.setup_listener():
                return
        
        self._is_running = True
        self.listening_started.emit()
        
        try:
            # Set up callbacks
            self._listener.on_speech_recognized = self._on_speech
            self._listener.on_partial_result = self._on_partial
            
            # Start listening (blocking in this thread)
            self._listener.start_listening()
            
            # Keep thread alive while listening
            while self._is_running and self._listener.is_listening:
                self.msleep(100)
                
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self.listening_stopped.emit()
    
    def _on_speech(self, text: str):
        """Handle recognized speech."""
        if text.strip():
            self.speech_recognized.emit(text)
    
    def _on_partial(self, text: str):
        """Handle partial results."""
        if text.strip():
            self.partial_result.emit(text)
    
    def stop(self):
        """Stop listening."""
        self._is_running = False
        if self._listener:
            self._listener.stop_listening()


class LoginScreen(QWidget):
    """
    Login screen with two authentication methods:
    1. Voice activation (Winter Soldier Protocol)
    2. Text password (MEZEYAT)
    """
    
    # Signals
    login_successful = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._current_word_index = 0
        self._voice_thread = None
        self._is_voice_active = False
        
        self.setObjectName("loginScreen")
        self._setup_ui()
        self._setup_voice_listener()
    
    def _setup_voice_listener(self):
        """Set up the voice listener thread."""
        self._voice_thread = VoiceListenerThread(self)
        self._voice_thread.speech_recognized.connect(self._on_voice_input)
        self._voice_thread.partial_result.connect(self._on_partial_voice)
        self._voice_thread.error_occurred.connect(self._on_voice_error)
        self._voice_thread.listening_started.connect(self._on_listening_started)
        self._voice_thread.listening_stopped.connect(self._on_listening_stopped)
    
    def _setup_ui(self):
        """Setup the login screen UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 30, 50, 30)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)
        
        # Title
        title_label = QLabel("ALFREDX")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 48px;
                font-weight: bold;
                color: {JarvisTheme.CYAN};
                letter-spacing: 15px;
            }}
        """)
        layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("WAYNECORE ASSISTANT")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                color: {JarvisTheme.CYAN_DIM};
                letter-spacing: 5px;
            }}
        """)
        layout.addWidget(subtitle_label)
        
        layout.addSpacing(20)
        
        # Rotating core - centered
        core_container = QWidget()
        core_layout = QHBoxLayout(core_container)
        core_layout.setContentsMargins(0, 0, 0, 0)
        core_layout.addStretch()
        self._core = RotatingCore(size=250)
        core_layout.addWidget(self._core)
        core_layout.addStretch()
        layout.addWidget(core_container)
        
        layout.addSpacing(20)
        
        # Auth method switcher
        self._auth_stack = QStackedWidget()
        self._auth_stack.setFixedHeight(350)
        
        # Voice activation widget
        self._voice_widget = self._create_voice_widget()
        self._auth_stack.addWidget(self._voice_widget)
        
        # Text password widget
        self._text_widget = self._create_text_widget()
        self._auth_stack.addWidget(self._text_widget)
        
        layout.addWidget(self._auth_stack)
        
        # Switch auth method buttons - centered
        switch_container = QWidget()
        switch_layout = QHBoxLayout(switch_container)
        switch_layout.setContentsMargins(0, 0, 0, 0)
        switch_layout.setAlignment(Qt.AlignCenter)
        switch_layout.setSpacing(15)
        
        self._voice_btn = QPushButton("🎤 VOICE ACTIVATION")
        self._voice_btn.setCheckable(True)
        self._voice_btn.setChecked(True)
        self._voice_btn.setFixedWidth(200)
        self._voice_btn.clicked.connect(lambda: self._switch_auth(0))
        self._voice_btn.setStyleSheet(self._get_switch_btn_style(True))
        switch_layout.addWidget(self._voice_btn)
        
        self._text_btn = QPushButton("⌨️ TEXT PASSWORD")
        self._text_btn.setCheckable(True)
        self._text_btn.setFixedWidth(200)
        self._text_btn.clicked.connect(lambda: self._switch_auth(1))
        self._text_btn.setStyleSheet(self._get_switch_btn_style(False))
        switch_layout.addWidget(self._text_btn)
        
        layout.addWidget(switch_container)
        
        # Status message
        self._status_label = QLabel("Select authentication method")
        self._status_label.setAlignment(Qt.AlignCenter)
        self._status_label.setWordWrap(True)
        self._status_label.setStyleSheet(f"""
            QLabel {{
                font-size: 12px;
                color: {JarvisTheme.GRAY_LIGHT};
                padding: 10px;
            }}
        """)
        layout.addWidget(self._status_label)
    
    def _create_voice_widget(self) -> QWidget:
        """Create the voice activation widget."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)
        
        # Instructions
        instruction_label = QLabel("WINTER SOLDIER PROTOCOL")
        instruction_label.setAlignment(Qt.AlignCenter)
        instruction_label.setStyleSheet(f"""
            QLabel {{
                font-size: 16px;
                font-weight: bold;
                color: {JarvisTheme.CYAN};
                letter-spacing: 3px;
            }}
        """)
        layout.addWidget(instruction_label)
        
        # Current word display
        self._word_label = QLabel("Press START to begin")
        self._word_label.setAlignment(Qt.AlignCenter)
        self._word_label.setFixedHeight(80)
        self._word_label.setStyleSheet(f"""
            QLabel {{
                font-size: 28px;
                font-weight: bold;
                color: {JarvisTheme.WHITE};
                letter-spacing: 5px;
                padding: 20px;
            }}
        """)
        layout.addWidget(self._word_label)
        
        # Partial/live text display
        self._partial_label = QLabel("")
        self._partial_label.setAlignment(Qt.AlignCenter)
        self._partial_label.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                color: {JarvisTheme.GRAY};
                font-style: italic;
            }}
        """)
        layout.addWidget(self._partial_label)
        
        # Progress indicator
        self._progress_label = QLabel(ActivationWords.get_progress_text(0))
        self._progress_label.setAlignment(Qt.AlignCenter)
        self._progress_label.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                color: {JarvisTheme.CYAN_DIM};
                letter-spacing: 2px;
            }}
        """)
        layout.addWidget(self._progress_label)
        
        # Waveform
        self._waveform = WaveformWidget(bar_count=25)
        self._waveform.setFixedHeight(60)
        layout.addWidget(self._waveform)
        
        # Start/Reset buttons - centered
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.setSpacing(15)
        
        self._start_voice_btn = QPushButton("🎤 START LISTENING")
        self._start_voice_btn.setFixedWidth(200)
        self._start_voice_btn.clicked.connect(self._toggle_voice_activation)
        self._start_voice_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(0, 247, 255, 0.2);
                border: 2px solid {JarvisTheme.CYAN};
                color: {JarvisTheme.CYAN};
                padding: 15px 30px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: rgba(0, 247, 255, 0.3);
            }}
        """)
        btn_layout.addWidget(self._start_voice_btn)
        
        self._reset_btn = QPushButton("↺ RESET")
        self._reset_btn.setFixedWidth(100)
        self._reset_btn.clicked.connect(self._reset_voice_activation)
        self._reset_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(255, 170, 0, 0.2);
                border: 1px solid {JarvisTheme.ORANGE};
                color: {JarvisTheme.ORANGE};
                padding: 15px 20px;
                font-size: 12px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 170, 0, 0.3);
            }}
        """)
        btn_layout.addWidget(self._reset_btn)
        
        layout.addWidget(btn_container)
        
        return widget
    
    def _create_text_widget(self) -> QWidget:
        """Create the text password widget."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        
        # Instructions
        instruction_label = QLabel("ENTER ACCESS CODE")
        instruction_label.setAlignment(Qt.AlignCenter)
        instruction_label.setStyleSheet(f"""
            QLabel {{
                font-size: 16px;
                font-weight: bold;
                color: {JarvisTheme.CYAN};
                letter-spacing: 3px;
            }}
        """)
        layout.addWidget(instruction_label)
        
        layout.addSpacing(20)
        
        # Password input - centered
        input_container = QWidget()
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setAlignment(Qt.AlignCenter)
        
        self._password_input = QLineEdit()
        self._password_input.setPlaceholderText("Enter password...")
        self._password_input.setEchoMode(QLineEdit.Password)
        self._password_input.setAlignment(Qt.AlignCenter)
        self._password_input.setFixedWidth(300)
        self._password_input.setFixedHeight(50)
        self._password_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: rgba(5, 10, 25, 0.8);
                border: 2px solid rgba(0, 247, 255, 0.3);
                border-radius: 5px;
                color: {JarvisTheme.WHITE};
                padding: 15px;
                font-size: 20px;
                letter-spacing: 8px;
            }}
            QLineEdit:focus {{
                border: 2px solid {JarvisTheme.CYAN};
            }}
        """)
        self._password_input.returnPressed.connect(self._check_password)
        input_layout.addWidget(self._password_input)
        
        layout.addWidget(input_container)
        
        # Hint
        hint_label = QLabel("Hint: The password is a special word")
        hint_label.setAlignment(Qt.AlignCenter)
        hint_label.setStyleSheet(f"""
            QLabel {{
                font-size: 11px;
                color: {JarvisTheme.GRAY};
            }}
        """)
        layout.addWidget(hint_label)
        
        layout.addSpacing(10)
        
        # Login button - centered
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setAlignment(Qt.AlignCenter)
        
        self._login_btn = QPushButton("🔓 LOGIN")
        self._login_btn.setFixedWidth(200)
        self._login_btn.setFixedHeight(50)
        self._login_btn.clicked.connect(self._check_password)
        self._login_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(0, 247, 255, 0.2);
                border: 2px solid {JarvisTheme.CYAN};
                color: {JarvisTheme.CYAN};
                padding: 15px 50px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: rgba(0, 247, 255, 0.3);
            }}
        """)
        btn_layout.addWidget(self._login_btn)
        
        layout.addWidget(btn_container)
        
        return widget
    
    def _get_switch_btn_style(self, active: bool) -> str:
        """Get style for auth switch buttons."""
        if active:
            return f"""
                QPushButton {{
                    background-color: rgba(0, 247, 255, 0.2);
                    border: 1px solid {JarvisTheme.CYAN};
                    color: {JarvisTheme.CYAN};
                    padding: 10px 20px;
                    font-size: 11px;
                    font-weight: bold;
                    border-radius: 5px;
                }}
            """
        return f"""
            QPushButton {{
                background-color: transparent;
                border: 1px solid {JarvisTheme.GRAY_DARK};
                color: {JarvisTheme.GRAY};
                padding: 10px 20px;
                font-size: 11px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                border: 1px solid {JarvisTheme.GRAY};
            }}
        """
    
    def _switch_auth(self, index: int):
        """Switch between voice and text authentication."""
        # Stop voice if switching away
        if index == 1 and self._is_voice_active:
            self._stop_voice_activation()
        
        self._auth_stack.setCurrentIndex(index)
        
        self._voice_btn.setChecked(index == 0)
        self._text_btn.setChecked(index == 1)
        
        self._voice_btn.setStyleSheet(self._get_switch_btn_style(index == 0))
        self._text_btn.setStyleSheet(self._get_switch_btn_style(index == 1))
        
        if index == 0:
            self._status_label.setText("Speak the 10 activation words in sequence")
            self._status_label.setStyleSheet(f"color: {JarvisTheme.GRAY_LIGHT}; font-size: 12px; padding: 10px;")
        else:
            self._status_label.setText("Enter your access code")
            self._status_label.setStyleSheet(f"color: {JarvisTheme.GRAY_LIGHT}; font-size: 12px; padding: 10px;")
            self._password_input.setFocus()
    
    def _toggle_voice_activation(self):
        """Toggle voice activation on/off."""
        if self._is_voice_active:
            self._stop_voice_activation()
        else:
            self._start_voice_activation()
    
    def _start_voice_activation(self):
        """Start voice activation listening."""
        self._current_word_index = 0
        self._update_word_display()
        
        self._status_label.setText("Initializing microphone...")
        self._status_label.setStyleSheet(f"color: {JarvisTheme.ORANGE}; font-size: 12px; padding: 10px;")
        
        # Start the voice thread
        if self._voice_thread and not self._voice_thread.isRunning():
            self._voice_thread.start()
    
    def _stop_voice_activation(self):
        """Stop voice activation."""
        self._is_voice_active = False
        self._waveform.setActive(False)
        
        if self._voice_thread:
            self._voice_thread.stop()
        
        self._start_voice_btn.setEnabled(True)
        self._start_voice_btn.setText("🎤 START LISTENING")
        self._start_voice_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(0, 247, 255, 0.2);
                border: 2px solid {JarvisTheme.CYAN};
                color: {JarvisTheme.CYAN};
                padding: 15px 30px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: rgba(0, 247, 255, 0.3);
            }}
        """)
        
        self._status_label.setText("Voice activation stopped")
        self._status_label.setStyleSheet(f"color: {JarvisTheme.GRAY_LIGHT}; font-size: 12px; padding: 10px;")
    
    def _on_listening_started(self):
        """Called when listening actually starts."""
        self._is_voice_active = True
        self._waveform.setActive(True)
        
        self._start_voice_btn.setText("⬛ STOP LISTENING")
        self._start_voice_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(255, 50, 50, 0.3);
                border: 2px solid {JarvisTheme.RED};
                color: {JarvisTheme.RED};
                padding: 15px 30px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 50, 50, 0.4);
            }}
        """)
        
        self._status_label.setText("🎤 Listening... Speak the activation words")
        self._status_label.setStyleSheet(f"color: {JarvisTheme.GREEN}; font-size: 12px; padding: 10px;")
    
    def _on_listening_stopped(self):
        """Called when listening stops."""
        self._is_voice_active = False
        self._waveform.setActive(False)
        
        self._start_voice_btn.setEnabled(True)
        self._start_voice_btn.setText("🎤 START LISTENING")
        self._start_voice_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(0, 247, 255, 0.2);
                border: 2px solid {JarvisTheme.CYAN};
                color: {JarvisTheme.CYAN};
                padding: 15px 30px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: rgba(0, 247, 255, 0.3);
            }}
        """)
    
    def _on_voice_error(self, error: str):
        """Handle voice recognition errors."""
        self._status_label.setText(f"⚠️ Error: {error}")
        self._status_label.setStyleSheet(f"color: {JarvisTheme.RED}; font-size: 12px; padding: 10px;")
        self._stop_voice_activation()
    
    def _on_partial_voice(self, text: str):
        """Handle partial voice results (live transcription)."""
        self._partial_label.setText(f'Hearing: "{text}"')
    
    def _reset_voice_activation(self):
        """Reset voice activation to beginning."""
        self._stop_voice_activation()
        
        self._current_word_index = 0
        self._word_label.setText("Press START to begin")
        self._word_label.setStyleSheet(f"""
            QLabel {{
                font-size: 28px;
                font-weight: bold;
                color: {JarvisTheme.WHITE};
                letter-spacing: 5px;
                padding: 20px;
            }}
        """)
        self._partial_label.setText("")
        self._progress_label.setText(ActivationWords.get_progress_text(0))
        self._status_label.setText("Reset complete. Press START to try again.")
        self._status_label.setStyleSheet(f"color: {JarvisTheme.GRAY_LIGHT}; font-size: 12px; padding: 10px;")
    
    def _update_word_display(self):
        """Update the word display based on current progress."""
        if self._current_word_index < len(ActivationWords.SEQUENCE):
            # Show the expected word (for easier demo/testing)
            expected = ActivationWords.SEQUENCE[self._current_word_index]
            hint = f'Say: "{expected.upper()}"'
            self._word_label.setText(hint)
            self._word_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 28px;
                    font-weight: bold;
                    color: {JarvisTheme.CYAN};
                    letter-spacing: 5px;
                    padding: 20px;
                }}
            """)
        
        self._progress_label.setText(
            ActivationWords.get_progress_text(self._current_word_index)
        )
    
    def _on_voice_input(self, text: str):
        """Handle recognized speech during activation."""
        text_lower = text.lower().strip()
        self._partial_label.setText(f'Recognized: "{text}"')
        
        print(f"🎤 Voice input: {text_lower}")
        print(f"   Looking for word {self._current_word_index}: {ActivationWords.SEQUENCE[self._current_word_index] if self._current_word_index < len(ActivationWords.SEQUENCE) else 'DONE'}")
        
        # Check each word in the recognized text
        words = text_lower.split()
        
        for word in words:
            # Clean the word
            word = ''.join(c for c in word if c.isalpha())
            
            if not word:
                continue
            
            if self._current_word_index >= len(ActivationWords.SEQUENCE):
                break
            
            if ActivationWords.validate_word(word, self._current_word_index):
                print(f"   ✓ Word '{word}' matched!")
                
                # Show accepted word with green checkmark
                accepted_word = ActivationWords.SEQUENCE[self._current_word_index]
                self._word_label.setText(f"✓ {accepted_word.upper()}")
                self._word_label.setStyleSheet(f"""
                    QLabel {{
                        font-size: 28px;
                        font-weight: bold;
                        color: {JarvisTheme.GREEN};
                        letter-spacing: 5px;
                        padding: 20px;
                    }}
                """)
                
                self._current_word_index += 1
                
                # Update progress
                self._progress_label.setText(
                    ActivationWords.get_progress_text(self._current_word_index)
                )
                
                # Check if sequence complete
                if self._current_word_index >= len(ActivationWords.SEQUENCE):
                    self._activation_complete()
                    return
                else:
                    # Show next word after short delay
                    QTimer.singleShot(600, self._update_word_display)
    
    def _activation_complete(self):
        """Handle successful voice activation."""
        print("🎉 Voice activation complete!")
        
        self._stop_voice_activation()
        
        self._word_label.setText("✓ ACTIVATION COMPLETE")
        self._word_label.setStyleSheet(f"""
            QLabel {{
                font-size: 28px;
                font-weight: bold;
                color: {JarvisTheme.GREEN};
                letter-spacing: 5px;
                padding: 20px;
            }}
        """)
        self._partial_label.setText("")
        self._status_label.setText("🦇 Welcome, Master Wayne")
        self._status_label.setStyleSheet(f"color: {JarvisTheme.GREEN}; font-size: 14px; font-weight: bold; padding: 10px;")
        
        # Update core status
        self._core.setStatusText("AUTHORIZED")
        
        # Emit success signal after delay
        QTimer.singleShot(1500, self.login_successful.emit)
    
    def _check_password(self):
        """Check the entered password."""
        entered = self._password_input.text().strip().upper()
        
        print(f"🔑 Password entered: {entered}")
        print(f"   Expected: {Settings.TEXT_PASSWORD}")
        
        if entered == Settings.TEXT_PASSWORD:
            self._status_label.setText("✓ Access granted. Welcome, Master Wayne")
            self._status_label.setStyleSheet(f"color: {JarvisTheme.GREEN}; font-size: 14px; font-weight: bold; padding: 10px;")
            
            self._login_btn.setEnabled(False)
            self._password_input.setEnabled(False)
            
            # Update core status
            self._core.setStatusText("AUTHORIZED")
            
            # Emit success signal after delay
            QTimer.singleShot(1000, self.login_successful.emit)
        else:
            self._status_label.setText("✗ Access denied. Invalid password.")
            self._status_label.setStyleSheet(f"color: {JarvisTheme.RED}; font-size: 12px; padding: 10px;")
            self._password_input.clear()
            self._password_input.setFocus()
            
            # Shake animation effect (simple)
            self._password_input.setStyleSheet(f"""
                QLineEdit {{
                    background-color: rgba(255, 50, 50, 0.2);
                    border: 2px solid {JarvisTheme.RED};
                    border-radius: 5px;
                    color: {JarvisTheme.WHITE};
                    padding: 15px;
                    font-size: 20px;
                    letter-spacing: 8px;
                }}
            """)
            
            # Reset style after delay
            QTimer.singleShot(500, lambda: self._password_input.setStyleSheet(f"""
                QLineEdit {{
                    background-color: rgba(5, 10, 25, 0.8);
                    border: 2px solid rgba(0, 247, 255, 0.3);
                    border-radius: 5px;
                    color: {JarvisTheme.WHITE};
                    padding: 15px;
                    font-size: 20px;
                    letter-spacing: 8px;
                }}
                QLineEdit:focus {{
                    border: 2px solid {JarvisTheme.CYAN};
                }}
            """))
    
    def set_listener(self, listener):
        """Set external listener (for compatibility - not used in new design)."""
        # We use our own VoiceListenerThread now
        pass
    
    def closeEvent(self, event):
        """Clean up when closing."""
        if self._voice_thread and self._voice_thread.isRunning():
            self._voice_thread.stop()
            self._voice_thread.wait(1000)
        event.accept()

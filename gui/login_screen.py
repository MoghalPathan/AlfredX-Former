"""
AlfredX Login Screen
====================
Winter Soldier Protocol voice activation + text password login.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QFrame, QStackedWidget
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont

from config.settings import Settings
from config.activation_words import ActivationWords
from gui.styles.themes import JarvisTheme, StyleSheet
from gui.widgets.waveform import WaveformWidget
from gui.widgets.rotating_core import RotatingCore


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
        self._listener = None  # Will be set externally
        
        self.setObjectName("loginScreen")
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the login screen UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)
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
        
        layout.addSpacing(30)
        
        # Rotating core
        self._core = RotatingCore(size=250)
        layout.addWidget(self._core, alignment=Qt.AlignCenter)
        
        layout.addSpacing(30)
        
        # Auth method switcher
        self._auth_stack = QStackedWidget()
        
        # Voice activation widget
        self._voice_widget = self._create_voice_widget()
        self._auth_stack.addWidget(self._voice_widget)
        
        # Text password widget
        self._text_widget = self._create_text_widget()
        self._auth_stack.addWidget(self._text_widget)
        
        layout.addWidget(self._auth_stack)
        
        # Switch auth method buttons
        switch_layout = QHBoxLayout()
        switch_layout.setAlignment(Qt.AlignCenter)
        
        self._voice_btn = QPushButton("🎤 VOICE ACTIVATION")
        self._voice_btn.setCheckable(True)
        self._voice_btn.setChecked(True)
        self._voice_btn.clicked.connect(lambda: self._switch_auth(0))
        self._voice_btn.setStyleSheet(self._get_switch_btn_style(True))
        switch_layout.addWidget(self._voice_btn)
        
        self._text_btn = QPushButton("⌨️ TEXT PASSWORD")
        self._text_btn.setCheckable(True)
        self._text_btn.clicked.connect(lambda: self._switch_auth(1))
        self._text_btn.setStyleSheet(self._get_switch_btn_style(False))
        switch_layout.addWidget(self._text_btn)
        
        layout.addLayout(switch_layout)
        
        # Status message
        self._status_label = QLabel("Select authentication method")
        self._status_label.setAlignment(Qt.AlignCenter)
        self._status_label.setStyleSheet(f"""
            QLabel {{
                font-size: 12px;
                color: {JarvisTheme.GRAY_LIGHT};
            }}
        """)
        layout.addWidget(self._status_label)
    
    def _create_voice_widget(self) -> QWidget:
        """Create the voice activation widget."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        
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
        
        # Start/Reset buttons
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        
        self._start_voice_btn = QPushButton("🎤 START LISTENING")
        self._start_voice_btn.clicked.connect(self._start_voice_activation)
        self._start_voice_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(0, 247, 255, 0.2);
                border: 2px solid {JarvisTheme.CYAN};
                color: {JarvisTheme.CYAN};
                padding: 15px 30px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: rgba(0, 247, 255, 0.3);
            }}
        """)
        btn_layout.addWidget(self._start_voice_btn)
        
        self._reset_btn = QPushButton("↺ RESET")
        self._reset_btn.clicked.connect(self._reset_voice_activation)
        self._reset_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(255, 170, 0, 0.2);
                border: 1px solid {JarvisTheme.ORANGE};
                color: {JarvisTheme.ORANGE};
                padding: 15px 20px;
                font-size: 12px;
            }}
        """)
        btn_layout.addWidget(self._reset_btn)
        
        layout.addLayout(btn_layout)
        
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
        
        # Password input
        self._password_input = QLineEdit()
        self._password_input.setPlaceholderText("Enter password...")
        self._password_input.setEchoMode(QLineEdit.Password)
        self._password_input.setAlignment(Qt.AlignCenter)
        self._password_input.setFixedWidth(300)
        self._password_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: rgba(5, 10, 25, 0.8);
                border: 2px solid rgba(0, 247, 255, 0.3);
                border-radius: 5px;
                color: {JarvisTheme.WHITE};
                padding: 15px;
                font-size: 24px;
                letter-spacing: 10px;
            }}
            QLineEdit:focus {{
                border: 2px solid {JarvisTheme.CYAN};
            }}
        """)
        self._password_input.returnPressed.connect(self._check_password)
        layout.addWidget(self._password_input, alignment=Qt.AlignCenter)
        
        # Login button
        self._login_btn = QPushButton("🔓 LOGIN")
        self._login_btn.clicked.connect(self._check_password)
        self._login_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(0, 247, 255, 0.2);
                border: 2px solid {JarvisTheme.CYAN};
                color: {JarvisTheme.CYAN};
                padding: 15px 50px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: rgba(0, 247, 255, 0.3);
            }}
        """)
        layout.addWidget(self._login_btn, alignment=Qt.AlignCenter)
        
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
                }}
            """
        return f"""
            QPushButton {{
                background-color: transparent;
                border: 1px solid {JarvisTheme.GRAY_DARK};
                color: {JarvisTheme.GRAY};
                padding: 10px 20px;
                font-size: 11px;
            }}
            QPushButton:hover {{
                border: 1px solid {JarvisTheme.GRAY};
            }}
        """
    
    def _switch_auth(self, index: int):
        """Switch between voice and text authentication."""
        self._auth_stack.setCurrentIndex(index)
        
        self._voice_btn.setChecked(index == 0)
        self._text_btn.setChecked(index == 1)
        
        self._voice_btn.setStyleSheet(self._get_switch_btn_style(index == 0))
        self._text_btn.setStyleSheet(self._get_switch_btn_style(index == 1))
        
        if index == 0:
            self._status_label.setText("Speak the 10 activation words in sequence")
        else:
            self._status_label.setText("Enter your access code")
    
    def _start_voice_activation(self):
        """Start voice activation listening."""
        self._current_word_index = 0
        self._update_word_display()
        self._waveform.setActive(True)
        self._start_voice_btn.setEnabled(False)
        self._start_voice_btn.setText("🎤 LISTENING...")
        self._status_label.setText("Speak the activation words...")
        
        # Start listening (if listener is set)
        if self._listener:
            self._listener.on_speech_recognized = self._on_voice_input
            self._listener.start_listening()
    
    def _reset_voice_activation(self):
        """Reset voice activation."""
        self._current_word_index = 0
        self._update_word_display()
        self._waveform.setActive(False)
        self._start_voice_btn.setEnabled(True)
        self._start_voice_btn.setText("🎤 START LISTENING")
        self._word_label.setText("Press START to begin")
        self._status_label.setText("Speak the 10 activation words in sequence")
        
        # Stop listening
        if self._listener:
            self._listener.stop_listening()
    
    def _update_word_display(self):
        """Update the word display based on current progress."""
        if self._current_word_index < len(ActivationWords.SEQUENCE):
            hint = ActivationWords.get_hint(self._current_word_index)
            self._word_label.setText(hint)
        
        self._progress_label.setText(
            ActivationWords.get_progress_text(self._current_word_index)
        )
    
    def _on_voice_input(self, text: str):
        """Handle voice input during activation."""
        text_lower = text.lower()
        
        # Check if spoken word matches expected
        if ActivationWords.validate_word(text_lower, self._current_word_index):
            self._current_word_index += 1
            
            # Show accepted word
            accepted_word = ActivationWords.SEQUENCE[self._current_word_index - 1]
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
            
            # Update progress
            self._progress_label.setText(
                ActivationWords.get_progress_text(self._current_word_index)
            )
            
            # Check if complete
            if self._current_word_index >= len(ActivationWords.SEQUENCE):
                self._activation_complete()
            else:
                # Show next hint after delay
                QTimer.singleShot(800, self._show_next_hint)
    
    def _show_next_hint(self):
        """Show hint for next word."""
        self._word_label.setStyleSheet(f"""
            QLabel {{
                font-size: 28px;
                font-weight: bold;
                color: {JarvisTheme.WHITE};
                letter-spacing: 5px;
                padding: 20px;
            }}
        """)
        self._update_word_display()
    
    def _activation_complete(self):
        """Handle successful voice activation."""
        self._waveform.setActive(False)
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
        self._status_label.setText("Welcome, Master Wayne")
        
        if self._listener:
            self._listener.stop_listening()
        
        # Emit success signal after short delay
        QTimer.singleShot(1500, self.login_successful.emit)
    
    def _check_password(self):
        """Check the entered password."""
        entered = self._password_input.text().strip().upper()
        
        if entered == Settings.TEXT_PASSWORD:
            self._status_label.setText("Access granted. Welcome, Master Wayne")
            self._status_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 12px;
                    color: {JarvisTheme.GREEN};
                }}
            """)
            
            # Emit success signal after short delay
            QTimer.singleShot(1000, self.login_successful.emit)
        else:
            self._status_label.setText("Access denied. Invalid password.")
            self._status_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 12px;
                    color: {JarvisTheme.RED};
                }}
            """)
            self._password_input.clear()
    
    def set_listener(self, listener):
        """Set the voice listener for activation."""
        self._listener = listener

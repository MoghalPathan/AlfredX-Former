"""
AlfredX Login Screen
====================
Simple text password login - Compact & Centered
Password: MEZEYAT
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal

from config.settings import Settings
from gui.styles.themes import JarvisTheme
from gui.widgets.rotating_core import RotatingCore


class LoginScreen(QWidget):
    """Simple login screen - Password: MEZEYAT"""
    
    login_successful = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._listener = None
        self.setObjectName("loginScreen")
        self._setup_ui()
    
    def _setup_ui(self):
        """Compact centered UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Top spacer (pushes content to center)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Title
        title = QLabel("ALFREDX")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            QLabel {{
                font-size: 36px;
                font-weight: bold;
                color: {JarvisTheme.CYAN};
                letter-spacing: 10px;
            }}
        """)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("WAYNECORE ASSISTANT")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"""
            QLabel {{
                font-size: 10px;
                color: {JarvisTheme.CYAN_DIM};
                letter-spacing: 3px;
                margin-bottom: 15px;
            }}
        """)
        layout.addWidget(subtitle)
        
        # Rotating Core (smaller)
        self._core = RotatingCore(size=140)
        layout.addWidget(self._core, alignment=Qt.AlignCenter)
        
        # Spacer
        layout.addSpacing(15)
        
        # Access Code Label
        enter_label = QLabel("ENTER ACCESS CODE")
        enter_label.setAlignment(Qt.AlignCenter)
        enter_label.setStyleSheet(f"""
            QLabel {{
                font-size: 11px;
                font-weight: bold;
                color: {JarvisTheme.CYAN};
                letter-spacing: 2px;
            }}
        """)
        layout.addWidget(enter_label)
        
        # Password Input
        self._password_input = QLineEdit()
        self._password_input.setPlaceholderText("• • • • • • •")
        self._password_input.setEchoMode(QLineEdit.Password)
        self._password_input.setAlignment(Qt.AlignCenter)
        self._password_input.setFixedSize(220, 40)
        self._password_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: rgba(0, 20, 40, 0.9);
                border: 2px solid {JarvisTheme.CYAN};
                border-radius: 6px;
                color: {JarvisTheme.WHITE};
                font-size: 16px;
                letter-spacing: 6px;
            }}
            QLineEdit:focus {{
                border: 2px solid {JarvisTheme.WHITE};
            }}
        """)
        self._password_input.returnPressed.connect(self._check_password)
        layout.addWidget(self._password_input, alignment=Qt.AlignCenter)
        
        # Hint
        hint = QLabel("Hint: MEZEYAT")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet(f"QLabel {{ font-size: 9px; color: {JarvisTheme.GRAY}; }}")
        layout.addWidget(hint)
        
        # Spacer
        layout.addSpacing(10)
        
        # Login Button
        self._login_btn = QPushButton("LOGIN")
        self._login_btn.setFixedSize(150, 38)
        self._login_btn.setCursor(Qt.PointingHandCursor)
        self._login_btn.clicked.connect(self._check_password)
        self._login_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(0, 247, 255, 0.15);
                border: 2px solid {JarvisTheme.CYAN};
                border-radius: 6px;
                color: {JarvisTheme.CYAN};
                font-size: 13px;
                font-weight: bold;
                letter-spacing: 3px;
            }}
            QPushButton:hover {{
                background-color: rgba(0, 247, 255, 0.3);
            }}
            QPushButton:pressed {{
                background-color: rgba(0, 247, 255, 0.5);
            }}
        """)
        layout.addWidget(self._login_btn, alignment=Qt.AlignCenter)
        
        # Status Label
        self._status_label = QLabel("")
        self._status_label.setAlignment(Qt.AlignCenter)
        self._status_label.setFixedHeight(20)
        self._status_label.setStyleSheet(f"QLabel {{ font-size: 11px; color: {JarvisTheme.GRAY_LIGHT}; }}")
        layout.addWidget(self._status_label)
        
        # Bottom spacer (pushes content to center)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
    
    def _check_password(self):
        """Check password."""
        entered = self._password_input.text().strip().upper()
        
        if entered == Settings.TEXT_PASSWORD:
            self._status_label.setText("✓ Access Granted")
            self._status_label.setStyleSheet(f"QLabel {{ font-size: 11px; color: {JarvisTheme.GREEN}; }}")
            self._login_btn.setEnabled(False)
            self._password_input.setEnabled(False)
            QTimer.singleShot(800, self.login_successful.emit)
        else:
            self._status_label.setText("✗ Access Denied")
            self._status_label.setStyleSheet(f"QLabel {{ font-size: 11px; color: {JarvisTheme.RED}; }}")
            self._password_input.clear()
            self._password_input.setFocus()
    
    def set_listener(self, listener):
        """Kept for compatibility."""
        self._listener = listener

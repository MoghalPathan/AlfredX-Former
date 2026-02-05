"""
AlfredX Dashboard
=================
Main JARVIS-style interface - WORKING VERSION
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QFrame, QTextEdit,
    QGridLayout, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from datetime import datetime
import psutil
import os

from gui.styles.themes import JarvisTheme
from gui.widgets.circular_gauge import CircularGauge
from gui.widgets.rotating_core import RotatingCore


class Dashboard(QWidget):
    """Main dashboard interface."""
    
    command_entered = pyqtSignal(str)
    mic_button_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._language = "en"
        self._is_listening = False
        
        self.setObjectName("dashboard")
        self.setStyleSheet(f"background-color: {JarvisTheme.DARK};")
        
        self._setup_ui()
        self._start_timers()
    
    def _setup_ui(self):
        """Setup dashboard UI."""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Left Panel
        left = self._create_left_panel()
        main_layout.addWidget(left, stretch=1)
        
        # Center Panel
        center = self._create_center_panel()
        main_layout.addWidget(center, stretch=2)
        
        # Right Panel
        right = self._create_right_panel()
        main_layout.addWidget(right, stretch=1)
    
    def _create_panel(self, title: str) -> QFrame:
        """Create a styled panel."""
        panel = QFrame()
        panel.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(0, 20, 40, 0.7);
                border: 1px solid {JarvisTheme.CYAN};
                border-radius: 8px;
            }}
        """)
        return panel
    
    def _create_left_panel(self) -> QWidget:
        """Left panel - AI Core + System Stats."""
        panel = self._create_panel("AI CORE")
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        title = QLabel("AI CORE STATUS")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            QLabel {{
                color: {JarvisTheme.CYAN};
                font-size: 12px;
                font-weight: bold;
                letter-spacing: 2px;
            }}
        """)
        layout.addWidget(title)
        
        # AI Core Animation
        self._core = RotatingCore(size=120)
        layout.addWidget(self._core, alignment=Qt.AlignCenter)
        
        # System Performance Title
        perf_title = QLabel("SYSTEM PERFORMANCE")
        perf_title.setAlignment(Qt.AlignCenter)
        perf_title.setStyleSheet(f"""
            QLabel {{
                color: {JarvisTheme.CYAN};
                font-size: 11px;
                font-weight: bold;
                letter-spacing: 2px;
                margin-top: 10px;
            }}
        """)
        layout.addWidget(perf_title)
        
        # Gauges
        gauge_layout = QHBoxLayout()
        gauge_layout.setSpacing(5)
        
        self._cpu_gauge = CircularGauge(value=0, label="CPU", size=70, color=JarvisTheme.GREEN)
        self._ram_gauge = CircularGauge(value=0, label="RAM", size=70, color=JarvisTheme.CYAN)
        self._disk_gauge = CircularGauge(value=0, label="DISK", size=70, color=JarvisTheme.ORANGE)
        
        gauge_layout.addWidget(self._cpu_gauge)
        gauge_layout.addWidget(self._ram_gauge)
        gauge_layout.addWidget(self._disk_gauge)
        
        layout.addLayout(gauge_layout)
        
        # Network Status
        self._net_label = QLabel("● ONLINE")
        self._net_label.setAlignment(Qt.AlignCenter)
        self._net_label.setStyleSheet(f"color: {JarvisTheme.GREEN}; font-size: 11px;")
        layout.addWidget(self._net_label)
        
        layout.addStretch()
        
        return panel
    
    def _create_center_panel(self) -> QWidget:
        """Center panel - Chat interface."""
        panel = self._create_panel("COMMAND INTERFACE")
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        title = QLabel("COMMAND INTERFACE")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            QLabel {{
                color: {JarvisTheme.CYAN};
                font-size: 12px;
                font-weight: bold;
                letter-spacing: 2px;
            }}
        """)
        layout.addWidget(title)
        
        # Chat Area
        self._chat_area = QTextEdit()
        self._chat_area.setReadOnly(True)
        self._chat_area.setStyleSheet(f"""
            QTextEdit {{
                background-color: rgba(0, 10, 20, 0.8);
                border: 1px solid rgba(0, 247, 255, 0.3);
                border-radius: 5px;
                color: {JarvisTheme.WHITE};
                font-size: 13px;
                padding: 10px;
            }}
        """)
        layout.addWidget(self._chat_area, stretch=1)
        
        # Welcome message
        self._chat_area.append(
            f'<p style="color: {JarvisTheme.CYAN};">'
            f'<b>ALFRED:</b> Good evening, Master Wayne. All systems operational. How may I assist you?</p>'
        )
        
        # Input Area
        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)
        
        self._input_field = QLineEdit()
        self._input_field.setPlaceholderText("Type your command...")
        self._input_field.setStyleSheet(f"""
            QLineEdit {{
                background-color: rgba(0, 20, 40, 0.9);
                border: 2px solid {JarvisTheme.CYAN};
                border-radius: 5px;
                color: {JarvisTheme.WHITE};
                padding: 10px 15px;
                font-size: 13px;
            }}
            QLineEdit:focus {{
                border: 2px solid {JarvisTheme.WHITE};
            }}
        """)
        self._input_field.returnPressed.connect(self._on_send)
        input_layout.addWidget(self._input_field)
        
        # Mic Button
        self._mic_btn = QPushButton("🎤")
        self._mic_btn.setFixedSize(45, 45)
        self._mic_btn.setCursor(Qt.PointingHandCursor)
        self._mic_btn.clicked.connect(self._on_mic_clicked)
        self._mic_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(255, 50, 50, 0.2);
                border: 2px solid #ff5555;
                border-radius: 22px;
                font-size: 18px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 50, 50, 0.4);
            }}
        """)
        input_layout.addWidget(self._mic_btn)
        
        # Send Button
        self._send_btn = QPushButton("➤")
        self._send_btn.setFixedSize(45, 45)
        self._send_btn.setCursor(Qt.PointingHandCursor)
        self._send_btn.clicked.connect(self._on_send)
        self._send_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(0, 247, 255, 0.2);
                border: 2px solid {JarvisTheme.CYAN};
                border-radius: 22px;
                color: {JarvisTheme.CYAN};
                font-size: 18px;
            }}
            QPushButton:hover {{
                background-color: rgba(0, 247, 255, 0.4);
            }}
        """)
        input_layout.addWidget(self._send_btn)
        
        layout.addLayout(input_layout)
        
        return panel
    
    def _create_right_panel(self) -> QWidget:
        """Right panel - Quick commands + Time."""
        panel = self._create_panel("QUICK COMMANDS")
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        title = QLabel("QUICK COMMANDS")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            QLabel {{
                color: {JarvisTheme.CYAN};
                font-size: 12px;
                font-weight: bold;
                letter-spacing: 2px;
            }}
        """)
        layout.addWidget(title)
        
        # Quick Command Buttons
        commands = [
            ("🌐", "Browser", "open chrome"),
            ("📁", "Files", "open explorer"),
            ("🎵", "Music", "play music"),
            ("📷", "Screenshot", "take screenshot"),
            ("🔍", "Search", "search web"),
            ("⚙️", "Settings", "open settings"),
        ]
        
        grid = QGridLayout()
        grid.setSpacing(8)
        
        for i, (icon, label, cmd) in enumerate(commands):
            btn = QPushButton(f"{icon}\n{label}")
            btn.setFixedSize(65, 55)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, c=cmd: self._quick_command(c))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(0, 247, 255, 0.1);
                    border: 1px solid rgba(0, 247, 255, 0.3);
                    border-radius: 5px;
                    color: {JarvisTheme.CYAN};
                    font-size: 9px;
                }}
                QPushButton:hover {{
                    background-color: rgba(0, 247, 255, 0.2);
                    border: 1px solid {JarvisTheme.CYAN};
                }}
            """)
            grid.addWidget(btn, i // 3, i % 3)
        
        layout.addLayout(grid)
        
        # Activity Log Title
        log_title = QLabel("ACTIVITY LOG")
        log_title.setAlignment(Qt.AlignCenter)
        log_title.setStyleSheet(f"""
            QLabel {{
                color: {JarvisTheme.CYAN};
                font-size: 11px;
                font-weight: bold;
                letter-spacing: 2px;
                margin-top: 10px;
            }}
        """)
        layout.addWidget(log_title)
        
        # Activity Log
        self._activity_log = QTextEdit()
        self._activity_log.setReadOnly(True)
        self._activity_log.setMaximumHeight(120)
        self._activity_log.setStyleSheet(f"""
            QTextEdit {{
                background-color: rgba(0, 10, 20, 0.8);
                border: 1px solid rgba(0, 247, 255, 0.3);
                border-radius: 5px;
                color: {JarvisTheme.GRAY_LIGHT};
                font-size: 10px;
                font-family: monospace;
            }}
        """)
        layout.addWidget(self._activity_log)
        
        self.add_activity("System initialized")
        
        # Time Display
        time_title = QLabel("SYSTEM TIME")
        time_title.setAlignment(Qt.AlignCenter)
        time_title.setStyleSheet(f"""
            QLabel {{
                color: {JarvisTheme.CYAN};
                font-size: 11px;
                font-weight: bold;
                letter-spacing: 2px;
                margin-top: 10px;
            }}
        """)
        layout.addWidget(time_title)
        
        self._time_label = QLabel("00:00:00")
        self._time_label.setAlignment(Qt.AlignCenter)
        self._time_label.setStyleSheet(f"""
            QLabel {{
                color: {JarvisTheme.CYAN};
                font-size: 28px;
                font-weight: bold;
                letter-spacing: 3px;
            }}
        """)
        layout.addWidget(self._time_label)
        
        self._date_label = QLabel("Loading...")
        self._date_label.setAlignment(Qt.AlignCenter)
        self._date_label.setStyleSheet(f"color: {JarvisTheme.CYAN_DIM}; font-size: 10px;")
        layout.addWidget(self._date_label)
        
        layout.addStretch()
        
        return panel
    
    def _start_timers(self):
        """Start update timers."""
        # System stats timer
        self._stats_timer = QTimer(self)
        self._stats_timer.timeout.connect(self._update_stats)
        self._stats_timer.start(2000)
        
        # Time timer
        self._time_timer = QTimer(self)
        self._time_timer.timeout.connect(self._update_time)
        self._time_timer.start(1000)
        
        # Initial update
        self._update_stats()
        self._update_time()
    
    def _update_stats(self):
        """Update system statistics."""
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            
            if os.name == 'nt':
                disk = psutil.disk_usage('C:\\').percent
            else:
                disk = psutil.disk_usage('/').percent
            
            self._cpu_gauge.setValue(cpu)
            self._ram_gauge.setValue(ram)
            self._disk_gauge.setValue(disk)
        except Exception as e:
            print(f"Stats error: {e}")
    
    def _update_time(self):
        """Update time display."""
        now = datetime.now()
        self._time_label.setText(now.strftime("%H:%M:%S"))
        self._date_label.setText(now.strftime("%A, %B %d, %Y"))
    
    def _on_send(self):
        """Handle send button click."""
        text = self._input_field.text().strip()
        if text:
            self.add_user_message(text)
            self.command_entered.emit(text)
            self._input_field.clear()
    
    def _on_mic_clicked(self):
        """Handle mic button click."""
        self._is_listening = not self._is_listening
        
        if self._is_listening:
            self._mic_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(255, 50, 50, 0.5);
                    border: 2px solid #ff3333;
                    border-radius: 22px;
                    font-size: 18px;
                }}
            """)
            self.add_activity("Listening started")
        else:
            self._mic_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(255, 50, 50, 0.2);
                    border: 2px solid #ff5555;
                    border-radius: 22px;
                    font-size: 18px;
                }}
            """)
            self.add_activity("Listening stopped")
        
        self.mic_button_clicked.emit()
    
    def _quick_command(self, command: str):
        """Handle quick command button."""
        self.add_user_message(command)
        self.command_entered.emit(command)
    
    def add_user_message(self, text: str):
        """Add user message to chat."""
        self._chat_area.append(
            f'<p style="color: {JarvisTheme.TEAL}; margin: 5px 0;">'
            f'<b>YOU:</b> {text}</p>'
        )
    
    def add_alfred_message(self, text: str):
        """Add Alfred message to chat."""
        self._chat_area.append(
            f'<p style="color: {JarvisTheme.CYAN}; margin: 5px 0;">'
            f'<b>ALFRED:</b> {text}</p>'
        )
    
    def add_activity(self, text: str):
        """Add activity log entry."""
        time = datetime.now().strftime("%H:%M:%S")
        self._activity_log.append(f"[{time}] {text}")
    
    def set_listening(self, is_listening: bool):
        """Set listening state."""
        self._is_listening = is_listening
    
    def set_language(self, language: str):
        """Set current language."""
        self._language = language

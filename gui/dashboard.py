"""
AlfredX Dashboard
=================
Main JARVIS-style interface after login.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QFrame, QScrollArea,
    QGridLayout, QTextEdit
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal

from config.settings import Settings
from config.personas import Personas
from gui.styles.themes import JarvisTheme
from gui.widgets.circular_gauge import CircularGauge
from gui.widgets.waveform import WaveformWidget
from gui.widgets.rotating_core import RotatingCore
from gui.widgets.hud_panel import HUDPanel


class Dashboard(QWidget):
    """
    Main dashboard interface with JARVIS-style design.
    """
    
    # Signals
    command_entered = pyqtSignal(str)
    mic_button_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._language = "en"
        self._is_listening = False
        
        self.setObjectName("dashboard")
        self._setup_ui()
        self._start_system_monitor()
    
    def _setup_ui(self):
        """Setup the dashboard UI."""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Left panel
        left_panel = self._create_left_panel()
        main_layout.addWidget(left_panel)
        
        # Center panel
        center_panel = self._create_center_panel()
        main_layout.addWidget(center_panel, stretch=2)
        
        # Right panel
        right_panel = self._create_right_panel()
        main_layout.addWidget(right_panel)
    
    def _create_left_panel(self) -> QWidget:
        """Create the left panel with AI core and stats."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        # AI Core
        core_panel = HUDPanel(title="AI CORE STATUS")
        self._core = RotatingCore(size=200)
        
        # Create a container for centering
        core_container = QWidget()
        core_layout = QHBoxLayout(core_container)
        core_layout.setContentsMargins(0, 0, 0, 0)
        core_layout.addStretch()
        core_layout.addWidget(self._core)
        core_layout.addStretch()
        
        core_panel.addWidget(core_container)
        layout.addWidget(core_panel)
        
        # System Performance
        perf_panel = HUDPanel(title="SYSTEM PERFORMANCE")
        
        gauge_layout = QHBoxLayout()
        self._cpu_gauge = CircularGauge(value=0, label="CPU", size=80, color=JarvisTheme.GREEN)
        self._ram_gauge = CircularGauge(value=0, label="RAM", size=80, color=JarvisTheme.CYAN)
        self._disk_gauge = CircularGauge(value=0, label="DISK", size=80, color=JarvisTheme.ORANGE)
        
        gauge_layout.addWidget(self._cpu_gauge)
        gauge_layout.addWidget(self._ram_gauge)
        gauge_layout.addWidget(self._disk_gauge)
        
        perf_panel.addLayout(gauge_layout)
        layout.addWidget(perf_panel)
        
        # Network Status
        net_panel = HUDPanel(title="NETWORK", accent_color=JarvisTheme.TEAL)
        
        self._net_status = QLabel("● Connected")
        self._net_status.setStyleSheet(f"color: {JarvisTheme.GREEN}; font-size: 12px;")
        net_panel.addWidget(self._net_status)
        
        layout.addWidget(net_panel)
        layout.addStretch()
        
        return panel
    
    def _create_center_panel(self) -> QWidget:
        """Create the center panel with conversation."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        # Conversation Panel
        conv_panel = HUDPanel(title="COMMAND INTERFACE")
        
        # Messages area
        self._messages_area = QTextEdit()
        self._messages_area.setReadOnly(True)
        self._messages_area.setStyleSheet(f"""
            QTextEdit {{
                background-color: transparent;
                border: none;
                color: {JarvisTheme.WHITE};
                font-size: 14px;
            }}
        """)
        conv_panel.addWidget(self._messages_area)
        
        # Waveform
        self._waveform = WaveformWidget(bar_count=40)
        self._waveform.setFixedHeight(50)
        conv_panel.addWidget(self._waveform)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self._input_field = QLineEdit()
        self._input_field.setPlaceholderText("Enter command or speak to Alfred...")
        self._input_field.setStyleSheet(f"""
            QLineEdit {{
                background-color: rgba(5, 10, 25, 0.8);
                border: 2px solid rgba(0, 247, 255, 0.3);
                border-radius: 5px;
                color: {JarvisTheme.WHITE};
                padding: 12px 15px;
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border: 2px solid {JarvisTheme.CYAN};
            }}
        """)
        self._input_field.returnPressed.connect(self._on_command_entered)
        input_layout.addWidget(self._input_field)
        
        # Mic button
        self._mic_btn = QPushButton("🎤")
        self._mic_btn.setFixedSize(50, 50)
        self._mic_btn.clicked.connect(self._on_mic_clicked)
        self._mic_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(255, 50, 50, 0.2);
                border: 1px solid rgba(255, 50, 50, 0.5);
                border-radius: 25px;
                font-size: 20px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 50, 50, 0.3);
            }}
        """)
        input_layout.addWidget(self._mic_btn)
        
        # Send button
        self._send_btn = QPushButton("➤")
        self._send_btn.setFixedSize(50, 50)
        self._send_btn.clicked.connect(self._on_command_entered)
        self._send_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(0, 247, 255, 0.2);
                border: 1px solid {JarvisTheme.CYAN};
                border-radius: 25px;
                color: {JarvisTheme.CYAN};
                font-size: 20px;
            }}
            QPushButton:hover {{
                background-color: rgba(0, 247, 255, 0.3);
            }}
        """)
        input_layout.addWidget(self._send_btn)
        
        conv_panel.addLayout(input_layout)
        layout.addWidget(conv_panel, stretch=1)
        
        return panel
    
    def _create_right_panel(self) -> QWidget:
        """Create the right panel with quick commands."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        # Quick Commands
        cmd_panel = HUDPanel(title="QUICK COMMANDS")
        
        commands_grid = QGridLayout()
        commands_grid.setSpacing(8)
        
        commands = [
            ("🌐", "Browser"),
            ("💻", "Terminal"),
            ("🎵", "Music"),
            ("📁", "Files"),
            ("📷", "Vision"),
            ("🔍", "Search"),
            ("📊", "Stats"),
            ("⚙️", "Settings"),
            ("🔒", "Lock"),
        ]
        
        for i, (icon, label) in enumerate(commands):
            btn = self._create_command_button(icon, label)
            commands_grid.addWidget(btn, i // 3, i % 3)
        
        cmd_panel.addLayout(commands_grid)
        layout.addWidget(cmd_panel)
        
        # Activity Log
        log_panel = HUDPanel(title="ACTIVITY LOG")
        
        self._activity_log = QTextEdit()
        self._activity_log.setReadOnly(True)
        self._activity_log.setMaximumHeight(200)
        self._activity_log.setStyleSheet(f"""
            QTextEdit {{
                background-color: transparent;
                border: none;
                color: {JarvisTheme.GRAY_LIGHT};
                font-size: 11px;
                font-family: monospace;
            }}
        """)
        log_panel.addWidget(self._activity_log)
        layout.addWidget(log_panel)
        
        # Time/Date display
        time_panel = HUDPanel(title="SYSTEM TIME")
        
        self._time_label = QLabel("00:00:00")
        self._time_label.setAlignment(Qt.AlignCenter)
        self._time_label.setStyleSheet(f"""
            QLabel {{
                font-size: 32px;
                font-weight: bold;
                color: {JarvisTheme.CYAN};
                letter-spacing: 3px;
            }}
        """)
        time_panel.addWidget(self._time_label)
        
        self._date_label = QLabel("Loading...")
        self._date_label.setAlignment(Qt.AlignCenter)
        self._date_label.setStyleSheet(f"""
            QLabel {{
                font-size: 12px;
                color: {JarvisTheme.CYAN_DIM};
            }}
        """)
        time_panel.addWidget(self._date_label)
        
        layout.addWidget(time_panel)
        layout.addStretch()
        
        return panel
    
    def _create_command_button(self, icon: str, label: str) -> QPushButton:
        """Create a quick command button."""
        btn = QPushButton(f"{icon}\n{label}")
        btn.setFixedSize(70, 70)
        btn.clicked.connect(lambda: self._on_quick_command(label.lower()))
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(0, 247, 255, 0.05);
                border: 1px solid rgba(0, 247, 255, 0.3);
                border-radius: 5px;
                color: {JarvisTheme.CYAN};
                font-size: 10px;
            }}
            QPushButton:hover {{
                background-color: rgba(0, 247, 255, 0.15);
                border: 1px solid {JarvisTheme.CYAN};
            }}
        """)
        return btn
    
    def _start_system_monitor(self):
        """Start system monitoring updates."""
        self._update_timer = QTimer(self)
        self._update_timer.timeout.connect(self._update_system_stats)
        self._update_timer.start(2000)  # Update every 2 seconds
        
        self._time_timer = QTimer(self)
        self._time_timer.timeout.connect(self._update_time)
        self._time_timer.start(1000)  # Update every second
        
        self._update_system_stats()
        self._update_time()
    
    def _update_system_stats(self):
        """Update system statistics."""
        try:
            import psutil
            
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:\\').percent
            
            self._cpu_gauge.setValue(cpu)
            self._ram_gauge.setValue(ram)
            self._disk_gauge.setValue(disk)
        except Exception as e:
            pass
    
    def _update_time(self):
        """Update time display."""
        from datetime import datetime
        now = datetime.now()
        self._time_label.setText(now.strftime("%H:%M:%S"))
        self._date_label.setText(now.strftime("%A, %B %d, %Y"))
    
    def _on_command_entered(self):
        """Handle command input."""
        text = self._input_field.text().strip()
        if text:
            self.add_user_message(text)
            self.command_entered.emit(text)
            self._input_field.clear()
    
    def _on_mic_clicked(self):
        """Handle mic button click."""
        self._is_listening = not self._is_listening
        
        if self._is_listening:
            self._waveform.setActive(True)
            self._mic_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(255, 50, 50, 0.5);
                    border: 2px solid #ff3333;
                    border-radius: 25px;
                    font-size: 20px;
                }}
            """)
        else:
            self._waveform.setActive(False)
            self._mic_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(255, 50, 50, 0.2);
                    border: 1px solid rgba(255, 50, 50, 0.5);
                    border-radius: 25px;
                    font-size: 20px;
                }}
            """)
        
        self.mic_button_clicked.emit()
    
    def _on_quick_command(self, command: str):
        """Handle quick command button click."""
        command_map = {
            "browser": "open chrome",
            "terminal": "open terminal",
            "music": "play music",
            "files": "open explorer",
            "vision": "start camera",
            "search": "search web",
            "stats": "show system info",
            "settings": "open settings",
            "lock": "lock system",
        }
        
        if command in command_map:
            self.command_entered.emit(command_map[command])
    
    def add_user_message(self, text: str):
        """Add a user message to the conversation."""
        self._messages_area.append(
            f'<p style="color: {JarvisTheme.TEAL}; margin: 5px 0;">'
            f'<b>YOU:</b> {text}</p>'
        )
    
    def add_alfred_message(self, text: str):
        """Add an Alfred message to the conversation."""
        self._messages_area.append(
            f'<p style="color: {JarvisTheme.CYAN}; margin: 5px 0;">'
            f'<b>ALFRED:</b> {text}</p>'
        )
    
    def add_activity(self, text: str):
        """Add an entry to the activity log."""
        from datetime import datetime
        time = datetime.now().strftime("%H:%M:%S")
        self._activity_log.append(f"[{time}] {text}")
    
    def set_listening(self, is_listening: bool):
        """Set the listening state."""
        self._is_listening = is_listening
        self._waveform.setActive(is_listening)
    
    def set_language(self, language: str):
        """Set the current language."""
        self._language = language


# Need to import os for disk usage
import os

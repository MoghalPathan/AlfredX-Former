"""
AlfredX HUD Panel Widget
========================
JARVIS-style panel container with borders and glow effects.
"""

from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPen, QColor, QLinearGradient, QBrush

from gui.styles.themes import JarvisTheme


class HUDPanel(QFrame):
    """
    HUD-style panel container.
    Features glowing borders and header.
    """
    
    def __init__(
        self, 
        parent=None, 
        title: str = "",
        accent_color: str = JarvisTheme.CYAN,
        show_header: bool = True
    ):
        super().__init__(parent)
        
        self._title = title
        self._accent_color = QColor(accent_color)
        self._show_header = show_header
        self._glow_intensity = 0.3
        
        # Setup
        self._setup_ui()
        
        # Pulse animation
        self._pulse_timer = QTimer(self)
        self._pulse_timer.timeout.connect(self._pulse)
        self._pulse_direction = 1
    
    def _setup_ui(self):
        """Setup the panel UI."""
        self.setObjectName("hudPanel")
        
        # Main layout
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        
        # Header
        if self._show_header and self._title:
            self._header = QFrame()
            self._header.setObjectName("hudPanelHeader")
            self._header.setFixedHeight(35)
            
            header_layout = QVBoxLayout(self._header)
            header_layout.setContentsMargins(15, 8, 15, 8)
            
            self._title_label = QLabel(self._title.upper())
            self._title_label.setObjectName("hudPanelTitle")
            self._title_label.setStyleSheet(f"""
                QLabel {{
                    color: {self._accent_color.name()};
                    font-size: 11px;
                    font-weight: bold;
                    letter-spacing: 2px;
                    background: transparent;
                }}
            """)
            header_layout.addWidget(self._title_label)
            
            self._layout.addWidget(self._header)
        
        # Content area
        self._content = QFrame()
        self._content.setObjectName("hudPanelContent")
        self._content_layout = QVBoxLayout(self._content)
        self._content_layout.setContentsMargins(15, 15, 15, 15)
        self._content_layout.setSpacing(10)
        
        self._layout.addWidget(self._content)
        
        # Apply base style
        self.setStyleSheet(f"""
            QFrame#hudPanel {{
                background-color: rgba(5, 10, 25, 0.85);
                border: 1px solid rgba({self._accent_color.red()}, {self._accent_color.green()}, {self._accent_color.blue()}, 0.3);
                border-radius: 5px;
            }}
            QFrame#hudPanelHeader {{
                background-color: rgba({self._accent_color.red()}, {self._accent_color.green()}, {self._accent_color.blue()}, 0.1);
                border-bottom: 1px solid rgba({self._accent_color.red()}, {self._accent_color.green()}, {self._accent_color.blue()}, 0.2);
                border-radius: 5px 5px 0 0;
            }}
            QFrame#hudPanelContent {{
                background: transparent;
            }}
        """)
    
    def addWidget(self, widget: QWidget):
        """Add a widget to the panel content area."""
        self._content_layout.addWidget(widget)
    
    def addLayout(self, layout):
        """Add a layout to the panel content area."""
        self._content_layout.addLayout(layout)
    
    def addStretch(self, stretch: int = 1):
        """Add stretch to the content layout."""
        self._content_layout.addStretch(stretch)
    
    def setTitle(self, title: str):
        """Update the panel title."""
        self._title = title
        if hasattr(self, '_title_label'):
            self._title_label.setText(title.upper())
    
    def setAccentColor(self, color: str):
        """Update the accent color."""
        self._accent_color = QColor(color)
        self._setup_ui()  # Rebuild with new color
    
    def startPulse(self):
        """Start the glow pulse animation."""
        self._pulse_timer.start(50)
    
    def stopPulse(self):
        """Stop the glow pulse animation."""
        self._pulse_timer.stop()
        self._glow_intensity = 0.3
        self.update()
    
    def _pulse(self):
        """Update pulse animation."""
        self._glow_intensity += 0.02 * self._pulse_direction
        if self._glow_intensity >= 0.6:
            self._pulse_direction = -1
        elif self._glow_intensity <= 0.3:
            self._pulse_direction = 1
        self.update()
    
    def paintEvent(self, event):
        """Custom paint for glow effect."""
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw top glow line
        gradient = QLinearGradient(0, 0, self.width(), 0)
        glow_color = QColor(self._accent_color)
        glow_color.setAlphaF(self._glow_intensity)
        
        gradient.setColorAt(0, QColor(0, 0, 0, 0))
        gradient.setColorAt(0.5, glow_color)
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(gradient))
        painter.drawRect(0, 0, self.width(), 2)
        
        # Draw left accent line
        accent_pen = QPen(self._accent_color)
        accent_pen.setWidth(3)
        painter.setPen(accent_pen)
        painter.drawLine(0, 5, 0, self.height() - 5)
        
        painter.end()
    
    def contentLayout(self):
        """Get the content layout for direct manipulation."""
        return self._content_layout


class StatusPanel(HUDPanel):
    """Panel optimized for status display."""
    
    def __init__(self, parent=None, title: str = "STATUS"):
        super().__init__(parent, title=title, accent_color=JarvisTheme.GREEN)


class AlertPanel(HUDPanel):
    """Panel for alerts and warnings."""
    
    def __init__(self, parent=None, title: str = "ALERT"):
        super().__init__(parent, title=title, accent_color=JarvisTheme.ORANGE)
        self.startPulse()


# Test the widget
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QHBoxLayout, QPushButton
    
    app = QApplication(sys.argv)
    
    window = QWidget()
    window.setStyleSheet(f"background-color: {JarvisTheme.DARK};")
    window.setWindowTitle("HUD Panel Test")
    window.setMinimumSize(600, 400)
    
    layout = QHBoxLayout(window)
    
    # Test panels
    panel1 = HUDPanel(title="SYSTEM STATUS")
    panel1.addWidget(QLabel("CPU: 45%"))
    panel1.addWidget(QLabel("RAM: 62%"))
    panel1.addWidget(QLabel("DISK: 78%"))
    
    panel2 = StatusPanel(title="NETWORK")
    panel2.addWidget(QLabel("Connected"))
    panel2.addWidget(QLabel("Speed: 100 Mbps"))
    
    panel3 = AlertPanel(title="WARNINGS")
    panel3.addWidget(QLabel("High memory usage"))
    
    layout.addWidget(panel1)
    layout.addWidget(panel2)
    layout.addWidget(panel3)
    
    window.show()
    sys.exit(app.exec_())

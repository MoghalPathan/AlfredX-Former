"""
AlfredX Waveform Widget
=======================
Voice waveform visualization like JARVIS.
"""

import random
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QRectF
from PyQt5.QtGui import QPainter, QPen, QColor, QLinearGradient, QBrush

from gui.styles.themes import JarvisTheme


class WaveformWidget(QWidget):
    """
    Animated voice waveform visualization.
    Shows audio levels as animated bars.
    """
    
    def __init__(
        self, 
        parent=None,
        bar_count: int = 30,
        color: str = JarvisTheme.CYAN,
        min_height: int = 60
    ):
        super().__init__(parent)
        
        self._bar_count = bar_count
        self._color = QColor(color)
        self._bar_values = [0.1] * bar_count
        self._target_values = [0.1] * bar_count
        self._is_active = False
        
        # Widget settings
        self.setMinimumHeight(min_height)
        
        # Animation timer
        self._animation_timer = QTimer(self)
        self._animation_timer.timeout.connect(self._animate)
        self._animation_timer.start(30)  # ~33 FPS
    
    def setActive(self, active: bool):
        """Set whether the waveform is actively showing audio."""
        self._is_active = active
        if not active:
            self._target_values = [0.1] * self._bar_count
    
    def setLevels(self, levels: list):
        """Set target levels for each bar (0.0 to 1.0)."""
        if len(levels) == self._bar_count:
            self._target_values = levels
    
    def setRandomLevels(self):
        """Generate random levels (for demo/testing)."""
        if self._is_active:
            self._target_values = [
                random.uniform(0.2, 1.0) for _ in range(self._bar_count)
            ]
    
    def setColor(self, color: str):
        """Set the waveform color."""
        self._color = QColor(color)
    
    def _animate(self):
        """Animate bars toward target values."""
        changed = False
        for i in range(self._bar_count):
            diff = self._target_values[i] - self._bar_values[i]
            if abs(diff) > 0.01:
                self._bar_values[i] += diff * 0.3
                changed = True
        
        # Generate new random targets if active
        if self._is_active and random.random() > 0.7:
            self.setRandomLevels()
        
        if changed or self._is_active:
            self.update()
    
    def paintEvent(self, event):
        """Draw the waveform bars."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        
        # Calculate bar dimensions
        bar_width = width / (self._bar_count * 1.5)
        bar_spacing = bar_width * 0.5
        total_bar_width = bar_width + bar_spacing
        
        # Start position to center bars
        start_x = (width - total_bar_width * self._bar_count) / 2
        
        # Create gradient
        gradient = QLinearGradient(0, height, 0, 0)
        gradient.setColorAt(0, QColor(self._color.red(), self._color.green(), self._color.blue(), 100))
        gradient.setColorAt(0.5, self._color)
        gradient.setColorAt(1, QColor(self._color.lighter(150)))
        
        # Draw bars
        for i, value in enumerate(self._bar_values):
            x = start_x + i * total_bar_width
            bar_height = max(4, value * height * 0.9)
            y = (height - bar_height) / 2
            
            # Draw glow
            glow_color = QColor(self._color)
            glow_color.setAlpha(30)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(glow_color))
            painter.drawRoundedRect(
                QRectF(x - 2, y - 2, bar_width + 4, bar_height + 4),
                3, 3
            )
            
            # Draw bar
            painter.setBrush(QBrush(gradient))
            painter.drawRoundedRect(
                QRectF(x, y, bar_width, bar_height),
                2, 2
            )
        
        painter.end()


class CompactWaveform(WaveformWidget):
    """Smaller waveform for inline display."""
    
    def __init__(self, parent=None):
        super().__init__(parent, bar_count=15, min_height=30)


# Test the widget
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton
    
    app = QApplication(sys.argv)
    
    window = QWidget()
    window.setStyleSheet(f"background-color: {JarvisTheme.DARK};")
    window.setWindowTitle("Waveform Test")
    window.setMinimumSize(400, 200)
    
    layout = QVBoxLayout(window)
    
    waveform = WaveformWidget()
    layout.addWidget(waveform)
    
    # Toggle button
    def toggle_active():
        waveform.setActive(not waveform._is_active)
        btn.setText("Stop" if waveform._is_active else "Start")
    
    btn = QPushButton("Start")
    btn.clicked.connect(toggle_active)
    btn.setStyleSheet(f"""
        QPushButton {{
            background-color: rgba(0, 247, 255, 0.2);
            border: 1px solid {JarvisTheme.CYAN};
            color: {JarvisTheme.CYAN};
            padding: 10px;
        }}
    """)
    layout.addWidget(btn)
    
    window.show()
    sys.exit(app.exec_())

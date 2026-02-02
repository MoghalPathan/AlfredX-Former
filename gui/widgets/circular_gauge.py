"""
AlfredX Circular Gauge Widget
=============================
JARVIS-style circular progress indicator for CPU, RAM, etc.
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QRectF, pyqtProperty
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QBrush, QPainterPath

from gui.styles.themes import JarvisTheme


class CircularGauge(QWidget):
    """
    Circular gauge widget for displaying percentage values.
    Inspired by JARVIS HUD elements.
    """
    
    def __init__(
        self, 
        parent=None, 
        value: float = 0, 
        max_value: float = 100,
        label: str = "",
        size: int = 100,
        color: str = JarvisTheme.CYAN
    ):
        super().__init__(parent)
        
        self._value = value
        self._max_value = max_value
        self._label = label
        self._size = size
        self._color = QColor(color)
        self._bg_color = QColor(255, 255, 255, 25)
        self._text_color = QColor(JarvisTheme.WHITE)
        self._animated_value = 0
        
        # Widget settings
        self.setFixedSize(size, size)
        
        # Animation timer
        self._animation_timer = QTimer(self)
        self._animation_timer.timeout.connect(self._animate)
        self._animation_step = 0
    
    def setValue(self, value: float):
        """Set the gauge value with animation."""
        self._value = min(value, self._max_value)
        self._animation_step = (self._value - self._animated_value) / 20
        self._animation_timer.start(16)  # ~60 FPS
    
    def _animate(self):
        """Animate value change."""
        if abs(self._animated_value - self._value) < abs(self._animation_step):
            self._animated_value = self._value
            self._animation_timer.stop()
        else:
            self._animated_value += self._animation_step
        self.update()
    
    def setLabel(self, label: str):
        """Set the label text."""
        self._label = label
        self.update()
    
    def setColor(self, color: str):
        """Set the gauge color."""
        self._color = QColor(color)
        self.update()
    
    @pyqtProperty(float)
    def value(self):
        return self._value
    
    @value.setter
    def value(self, val):
        self.setValue(val)
    
    def paintEvent(self, event):
        """Draw the circular gauge."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Calculate dimensions
        width = self.width()
        height = self.height()
        side = min(width, height)
        
        # Center the drawing
        painter.translate(width / 2, height / 2)
        
        # Arc settings
        arc_width = side * 0.08
        arc_rect = QRectF(
            -side / 2 + arc_width,
            -side / 2 + arc_width,
            side - arc_width * 2,
            side - arc_width * 2
        )
        
        # Draw background arc
        bg_pen = QPen(self._bg_color)
        bg_pen.setWidth(int(arc_width))
        bg_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, 225 * 16, -270 * 16)
        
        # Draw value arc
        percentage = self._animated_value / self._max_value
        span_angle = int(-270 * 16 * percentage)
        
        value_pen = QPen(self._color)
        value_pen.setWidth(int(arc_width))
        value_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(value_pen)
        painter.drawArc(arc_rect, 225 * 16, span_angle)
        
        # Draw glow effect
        glow_color = QColor(self._color)
        glow_color.setAlpha(50)
        glow_pen = QPen(glow_color)
        glow_pen.setWidth(int(arc_width + 4))
        glow_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(glow_pen)
        painter.drawArc(arc_rect, 225 * 16, span_angle)
        
        # Draw center text (value)
        painter.setPen(self._color)
        value_font = QFont("Segoe UI", int(side * 0.18), QFont.Bold)
        painter.setFont(value_font)
        
        value_text = f"{int(self._animated_value)}%"
        painter.drawText(
            QRectF(-side / 2, -side * 0.15, side, side * 0.3),
            Qt.AlignCenter,
            value_text
        )
        
        # Draw label
        if self._label:
            label_color = QColor(self._text_color)
            label_color.setAlpha(180)
            painter.setPen(label_color)
            label_font = QFont("Segoe UI", int(side * 0.09))
            painter.setFont(label_font)
            
            painter.drawText(
                QRectF(-side / 2, side * 0.15, side, side * 0.2),
                Qt.AlignCenter,
                self._label
            )
        
        painter.end()


class MiniGauge(CircularGauge):
    """Smaller version of the circular gauge."""
    
    def __init__(self, parent=None, value: float = 0, label: str = ""):
        super().__init__(parent, value=value, label=label, size=60)


# Test the widget
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout
    
    app = QApplication(sys.argv)
    
    # Test window
    window = QWidget()
    window.setStyleSheet(f"background-color: {JarvisTheme.DARK};")
    window.setWindowTitle("Circular Gauge Test")
    
    layout = QHBoxLayout(window)
    
    # Create test gauges
    cpu_gauge = CircularGauge(value=45, label="CPU", color=JarvisTheme.GREEN)
    ram_gauge = CircularGauge(value=62, label="RAM", color=JarvisTheme.CYAN)
    disk_gauge = CircularGauge(value=78, label="DISK", color=JarvisTheme.ORANGE)
    
    layout.addWidget(cpu_gauge)
    layout.addWidget(ram_gauge)
    layout.addWidget(disk_gauge)
    
    window.show()
    
    # Animate values for testing
    def update_values():
        import random
        cpu_gauge.setValue(random.randint(20, 80))
        ram_gauge.setValue(random.randint(40, 90))
        disk_gauge.setValue(random.randint(60, 95))
    
    timer = QTimer()
    timer.timeout.connect(update_values)
    timer.start(2000)
    
    sys.exit(app.exec_())

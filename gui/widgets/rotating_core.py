"""
AlfredX Rotating Core Widget
============================
Central AI core with rotating rings - JARVIS style.
"""

import math
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QPointF, QRectF
from PyQt5.QtGui import (
    QPainter, QPen, QColor, QFont, QBrush, 
    QRadialGradient, QConicalGradient, QPainterPath
)

from gui.styles.themes import JarvisTheme


class RotatingCore(QWidget):
    """
    Central AI core widget with multiple rotating rings.
    Inspired by JARVIS/Iron Man HUD.
    """
    
    def __init__(self, parent=None, size: int = 300):
        super().__init__(parent)
        
        self._size = size
        self._rotation_angles = [0, 0, 0, 0, 0]  # 5 rings
        self._rotation_speeds = [0.5, -0.3, 0.2, -0.4, 0.15]  # Different speeds
        self._pulse_value = 0
        self._pulse_direction = 1
        self._is_active = True
        self._status_text = "ONLINE"
        
        # Widget settings
        self.setFixedSize(size, size)
        
        # Animation timer
        self._animation_timer = QTimer(self)
        self._animation_timer.timeout.connect(self._animate)
        self._animation_timer.start(16)  # ~60 FPS
    
    def setActive(self, active: bool):
        """Set whether the core is active."""
        self._is_active = active
        self._status_text = "ONLINE" if active else "STANDBY"
        self.update()
    
    def setStatusText(self, text: str):
        """Set the status text displayed."""
        self._status_text = text
        self.update()
    
    def _animate(self):
        """Animate rotation and pulse."""
        if not self._is_active:
            return
        
        # Update rotation angles
        for i in range(len(self._rotation_angles)):
            self._rotation_angles[i] += self._rotation_speeds[i]
            if self._rotation_angles[i] >= 360:
                self._rotation_angles[i] -= 360
            elif self._rotation_angles[i] < 0:
                self._rotation_angles[i] += 360
        
        # Update pulse
        self._pulse_value += 0.05 * self._pulse_direction
        if self._pulse_value >= 1:
            self._pulse_direction = -1
        elif self._pulse_value <= 0:
            self._pulse_direction = 1
        
        self.update()
    
    def paintEvent(self, event):
        """Draw the rotating core."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        painter.translate(center_x, center_y)
        
        # Draw outer rings
        self._draw_rings(painter)
        
        # Draw hexagonal core
        self._draw_hex_core(painter)
        
        # Draw center content
        self._draw_center(painter)
        
        painter.end()
    
    def _draw_rings(self, painter: QPainter):
        """Draw the rotating outer rings."""
        ring_configs = [
            (self._size * 0.48, 1, Qt.SolidLine, 0.15),   # Outermost
            (self._size * 0.44, 1, Qt.DashLine, 0.2),
            (self._size * 0.40, 2, Qt.SolidLine, 0.3),
            (self._size * 0.35, 1, Qt.DashDotLine, 0.25),
            (self._size * 0.30, 2, Qt.SolidLine, 0.4),    # Innermost
        ]
        
        for i, (radius, width, style, alpha) in enumerate(ring_configs):
            painter.save()
            painter.rotate(self._rotation_angles[i])
            
            color = QColor(JarvisTheme.CYAN)
            color.setAlphaF(alpha)
            
            pen = QPen(color)
            pen.setWidth(width)
            pen.setStyle(style)
            painter.setPen(pen)
            
            painter.drawEllipse(QPointF(0, 0), radius, radius)
            
            # Draw markers on some rings
            if i in [0, 2, 4]:
                self._draw_ring_markers(painter, radius, color)
            
            painter.restore()
    
    def _draw_ring_markers(self, painter: QPainter, radius: float, color: QColor):
        """Draw small markers on the ring."""
        marker_color = QColor(color)
        marker_color.setAlphaF(0.8)
        painter.setBrush(QBrush(marker_color))
        painter.setPen(Qt.NoPen)
        
        # Draw 4 markers at cardinal points
        for angle in [0, 90, 180, 270]:
            x = radius * math.cos(math.radians(angle))
            y = radius * math.sin(math.radians(angle))
            painter.drawEllipse(QPointF(x, y), 4, 4)
    
    def _draw_hex_core(self, painter: QPainter):
        """Draw the hexagonal core frame."""
        hex_radius = self._size * 0.22
        
        # Calculate hexagon points
        hex_path = QPainterPath()
        for i in range(6):
            angle = math.radians(60 * i - 30)
            x = hex_radius * math.cos(angle)
            y = hex_radius * math.sin(angle)
            if i == 0:
                hex_path.moveTo(x, y)
            else:
                hex_path.lineTo(x, y)
        hex_path.closeSubpath()
        
        # Draw glow
        glow_color = QColor(JarvisTheme.CYAN)
        glow_color.setAlpha(int(30 + 20 * self._pulse_value))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(glow_color))
        
        painter.save()
        painter.scale(1.1, 1.1)
        painter.drawPath(hex_path)
        painter.restore()
        
        # Draw fill
        gradient = QRadialGradient(0, 0, hex_radius)
        gradient.setColorAt(0, QColor(0, 50, 60, 100))
        gradient.setColorAt(1, QColor(0, 20, 30, 50))
        painter.setBrush(QBrush(gradient))
        
        # Draw border
        border_color = QColor(JarvisTheme.CYAN)
        border_color.setAlpha(int(150 + 50 * self._pulse_value))
        pen = QPen(border_color)
        pen.setWidth(2)
        painter.setPen(pen)
        
        painter.drawPath(hex_path)
    
    def _draw_center(self, painter: QPainter):
        """Draw the center text and icon."""
        # Draw "AI" or icon
        ai_color = QColor(JarvisTheme.CYAN)
        ai_color.setAlpha(int(200 + 55 * self._pulse_value))
        painter.setPen(ai_color)
        
        font = QFont("Segoe UI", int(self._size * 0.08), QFont.Bold)
        painter.setFont(font)
        
        painter.drawText(
            QRectF(-self._size * 0.2, -self._size * 0.08, self._size * 0.4, self._size * 0.12),
            Qt.AlignCenter,
            "ALFRED"
        )
        
        # Draw status text
        status_color = QColor(JarvisTheme.CYAN_DIM)
        painter.setPen(status_color)
        
        status_font = QFont("Segoe UI", int(self._size * 0.035))
        painter.setFont(status_font)
        
        painter.drawText(
            QRectF(-self._size * 0.2, self._size * 0.03, self._size * 0.4, self._size * 0.06),
            Qt.AlignCenter,
            self._status_text
        )


class MiniCore(RotatingCore):
    """Smaller version of the rotating core."""
    
    def __init__(self, parent=None):
        super().__init__(parent, size=150)


# Test the widget
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QVBoxLayout
    
    app = QApplication(sys.argv)
    
    window = QWidget()
    window.setStyleSheet(f"background-color: {JarvisTheme.DARK};")
    window.setWindowTitle("Rotating Core Test")
    window.setMinimumSize(400, 400)
    
    layout = QVBoxLayout(window)
    layout.setAlignment(Qt.AlignCenter)
    
    core = RotatingCore(size=350)
    layout.addWidget(core)
    
    window.show()
    sys.exit(app.exec_())

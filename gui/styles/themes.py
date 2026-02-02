"""
AlfredX GUI Themes
==================
JARVIS-inspired theme with cyan/teal colors.
Qt StyleSheet (QSS) definitions.
"""


class JarvisTheme:
    """JARVIS-inspired color palette."""
    
    # Primary colors
    CYAN = "#00f7ff"
    CYAN_BRIGHT = "#00ffff"
    CYAN_DIM = "#00a8b3"
    CYAN_DARK = "#005f66"
    
    # Secondary colors
    TEAL = "#00d4aa"
    BLUE = "#0088ff"
    PURPLE = "#8844ff"
    
    # Status colors
    GREEN = "#00ff88"
    RED = "#ff3333"
    ORANGE = "#ffaa00"
    YELLOW = "#ffff00"
    
    # Background colors
    DARK = "#000000"
    DARK_BLUE = "#000a0f"
    DARK_PANEL = "#050a10"
    PANEL_BG = "rgba(5, 10, 25, 0.85)"
    PANEL_BG_SOLID = "#050a19"
    
    # Text colors
    WHITE = "#ffffff"
    GRAY = "#888888"
    GRAY_LIGHT = "#aaaaaa"
    GRAY_DARK = "#444444"
    
    # Border colors
    BORDER = "rgba(0, 247, 255, 0.3)"
    BORDER_ACTIVE = "rgba(0, 247, 255, 0.6)"
    BORDER_HOVER = "rgba(0, 247, 255, 0.5)"
    
    # Glow effect (for custom painting)
    GLOW_COLOR = (0, 247, 255)  # RGB
    GLOW_ALPHA = 100


class StyleSheet:
    """Qt StyleSheet (QSS) definitions."""
    
    # Main application stylesheet
    MAIN = f"""
        /* ===== GLOBAL ===== */
        QWidget {{
            background-color: {JarvisTheme.DARK};
            color: {JarvisTheme.WHITE};
            font-family: 'Segoe UI', 'Rajdhani', sans-serif;
            font-size: 14px;
        }}
        
        /* ===== MAIN WINDOW ===== */
        QMainWindow {{
            background-color: {JarvisTheme.DARK};
        }}
        
        /* ===== LABELS ===== */
        QLabel {{
            color: {JarvisTheme.WHITE};
            background: transparent;
        }}
        
        QLabel[class="title"] {{
            font-size: 28px;
            font-weight: bold;
            color: {JarvisTheme.CYAN};
            letter-spacing: 5px;
        }}
        
        QLabel[class="subtitle"] {{
            font-size: 12px;
            color: {JarvisTheme.CYAN_DIM};
            letter-spacing: 2px;
        }}
        
        QLabel[class="panel-title"] {{
            font-size: 11px;
            font-weight: bold;
            color: {JarvisTheme.CYAN};
            letter-spacing: 2px;
            padding: 5px;
        }}
        
        QLabel[class="status-label"] {{
            font-size: 10px;
            color: {JarvisTheme.GREEN};
        }}
        
        QLabel[class="value-label"] {{
            font-size: 16px;
            font-weight: bold;
            color: {JarvisTheme.CYAN};
        }}
        
        /* ===== BUTTONS ===== */
        QPushButton {{
            background-color: rgba(0, 247, 255, 0.1);
            border: 1px solid rgba(0, 247, 255, 0.3);
            border-radius: 5px;
            color: {JarvisTheme.CYAN};
            padding: 10px 20px;
            font-size: 12px;
            font-weight: bold;
            letter-spacing: 1px;
        }}
        
        QPushButton:hover {{
            background-color: rgba(0, 247, 255, 0.2);
            border: 1px solid rgba(0, 247, 255, 0.6);
        }}
        
        QPushButton:pressed {{
            background-color: rgba(0, 247, 255, 0.3);
        }}
        
        QPushButton:disabled {{
            background-color: rgba(50, 50, 50, 0.5);
            border: 1px solid rgba(100, 100, 100, 0.3);
            color: {JarvisTheme.GRAY_DARK};
        }}
        
        QPushButton[class="primary"] {{
            background-color: rgba(0, 247, 255, 0.2);
            border: 2px solid {JarvisTheme.CYAN};
        }}
        
        QPushButton[class="danger"] {{
            background-color: rgba(255, 51, 51, 0.2);
            border: 1px solid rgba(255, 51, 51, 0.5);
            color: {JarvisTheme.RED};
        }}
        
        QPushButton[class="danger"]:hover {{
            background-color: rgba(255, 51, 51, 0.3);
            border: 1px solid {JarvisTheme.RED};
        }}
        
        /* ===== LINE EDIT (Input Fields) ===== */
        QLineEdit {{
            background-color: rgba(5, 10, 25, 0.8);
            border: 2px solid rgba(0, 247, 255, 0.3);
            border-radius: 5px;
            color: {JarvisTheme.WHITE};
            padding: 10px 15px;
            font-size: 14px;
            selection-background-color: {JarvisTheme.CYAN_DARK};
        }}
        
        QLineEdit:focus {{
            border: 2px solid {JarvisTheme.CYAN};
        }}
        
        QLineEdit:disabled {{
            background-color: rgba(30, 30, 30, 0.5);
            border: 1px solid rgba(100, 100, 100, 0.3);
            color: {JarvisTheme.GRAY_DARK};
        }}
        
        QLineEdit::placeholder {{
            color: {JarvisTheme.GRAY};
        }}
        
        /* ===== TEXT EDIT ===== */
        QTextEdit {{
            background-color: rgba(5, 10, 25, 0.8);
            border: 1px solid rgba(0, 247, 255, 0.3);
            border-radius: 5px;
            color: {JarvisTheme.WHITE};
            padding: 10px;
            font-size: 13px;
        }}
        
        QTextEdit:focus {{
            border: 1px solid {JarvisTheme.CYAN};
        }}
        
        /* ===== SCROLL AREA ===== */
        QScrollArea {{
            background: transparent;
            border: none;
        }}
        
        QScrollArea > QWidget > QWidget {{
            background: transparent;
        }}
        
        /* ===== SCROLLBAR ===== */
        QScrollBar:vertical {{
            background: rgba(0, 10, 20, 0.5);
            width: 8px;
            margin: 0;
        }}
        
        QScrollBar::handle:vertical {{
            background: {JarvisTheme.CYAN_DARK};
            border-radius: 4px;
            min-height: 30px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: {JarvisTheme.CYAN_DIM};
        }}
        
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {{
            height: 0;
        }}
        
        QScrollBar:horizontal {{
            background: rgba(0, 10, 20, 0.5);
            height: 8px;
            margin: 0;
        }}
        
        QScrollBar::handle:horizontal {{
            background: {JarvisTheme.CYAN_DARK};
            border-radius: 4px;
            min-width: 30px;
        }}
        
        /* ===== FRAME (Panels) ===== */
        QFrame {{
            background: transparent;
        }}
        
        QFrame[class="hud-panel"] {{
            background-color: rgba(5, 10, 25, 0.85);
            border: 1px solid rgba(0, 247, 255, 0.3);
            border-radius: 5px;
        }}
        
        QFrame[class="hud-panel-highlight"] {{
            background-color: rgba(5, 10, 25, 0.85);
            border: 1px solid rgba(0, 247, 255, 0.5);
            border-left: 3px solid {JarvisTheme.CYAN};
            border-radius: 5px;
        }}
        
        /* ===== PROGRESS BAR ===== */
        QProgressBar {{
            background-color: rgba(0, 247, 255, 0.1);
            border: 1px solid rgba(0, 247, 255, 0.3);
            border-radius: 3px;
            height: 6px;
            text-align: center;
        }}
        
        QProgressBar::chunk {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {JarvisTheme.CYAN_DARK},
                stop:1 {JarvisTheme.CYAN});
            border-radius: 3px;
        }}
        
        /* ===== LIST WIDGET ===== */
        QListWidget {{
            background-color: rgba(5, 10, 25, 0.8);
            border: 1px solid rgba(0, 247, 255, 0.3);
            border-radius: 5px;
            outline: none;
        }}
        
        QListWidget::item {{
            padding: 10px;
            border-bottom: 1px solid rgba(0, 247, 255, 0.1);
        }}
        
        QListWidget::item:hover {{
            background-color: rgba(0, 247, 255, 0.1);
        }}
        
        QListWidget::item:selected {{
            background-color: rgba(0, 247, 255, 0.2);
            border-left: 3px solid {JarvisTheme.CYAN};
        }}
        
        /* ===== TAB WIDGET ===== */
        QTabWidget::pane {{
            background-color: rgba(5, 10, 25, 0.85);
            border: 1px solid rgba(0, 247, 255, 0.3);
            border-top: none;
        }}
        
        QTabBar::tab {{
            background-color: rgba(5, 10, 25, 0.6);
            border: 1px solid rgba(0, 247, 255, 0.3);
            border-bottom: none;
            padding: 8px 20px;
            color: {JarvisTheme.CYAN_DIM};
            font-weight: bold;
        }}
        
        QTabBar::tab:selected {{
            background-color: rgba(0, 247, 255, 0.1);
            color: {JarvisTheme.CYAN};
            border-bottom: 2px solid {JarvisTheme.CYAN};
        }}
        
        QTabBar::tab:hover:!selected {{
            background-color: rgba(0, 247, 255, 0.05);
        }}
        
        /* ===== COMBO BOX ===== */
        QComboBox {{
            background-color: rgba(5, 10, 25, 0.8);
            border: 1px solid rgba(0, 247, 255, 0.3);
            border-radius: 5px;
            padding: 8px 15px;
            color: {JarvisTheme.WHITE};
        }}
        
        QComboBox:hover {{
            border: 1px solid rgba(0, 247, 255, 0.5);
        }}
        
        QComboBox::drop-down {{
            border: none;
            padding-right: 10px;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {JarvisTheme.DARK_PANEL};
            border: 1px solid rgba(0, 247, 255, 0.3);
            selection-background-color: rgba(0, 247, 255, 0.2);
        }}
        
        /* ===== SLIDER ===== */
        QSlider::groove:horizontal {{
            background: rgba(0, 247, 255, 0.1);
            height: 6px;
            border-radius: 3px;
        }}
        
        QSlider::handle:horizontal {{
            background: {JarvisTheme.CYAN};
            width: 16px;
            height: 16px;
            margin: -5px 0;
            border-radius: 8px;
        }}
        
        QSlider::handle:horizontal:hover {{
            background: {JarvisTheme.CYAN_BRIGHT};
        }}
        
        QSlider::sub-page:horizontal {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {JarvisTheme.CYAN_DARK},
                stop:1 {JarvisTheme.CYAN});
            border-radius: 3px;
        }}
        
        /* ===== TOOLTIP ===== */
        QToolTip {{
            background-color: {JarvisTheme.DARK_PANEL};
            border: 1px solid {JarvisTheme.CYAN_DIM};
            color: {JarvisTheme.WHITE};
            padding: 5px 10px;
            font-size: 12px;
        }}
        
        /* ===== MENU ===== */
        QMenu {{
            background-color: {JarvisTheme.DARK_PANEL};
            border: 1px solid rgba(0, 247, 255, 0.3);
            padding: 5px;
        }}
        
        QMenu::item {{
            padding: 8px 30px;
            color: {JarvisTheme.WHITE};
        }}
        
        QMenu::item:selected {{
            background-color: rgba(0, 247, 255, 0.2);
        }}
        
        QMenu::separator {{
            height: 1px;
            background: rgba(0, 247, 255, 0.2);
            margin: 5px 0;
        }}
    """
    
    # Login screen specific styles
    LOGIN = f"""
        QWidget#loginScreen {{
            background-color: {JarvisTheme.DARK};
        }}
        
        QLineEdit#passwordInput {{
            font-size: 24px;
            letter-spacing: 10px;
            text-align: center;
            padding: 15px;
        }}
        
        QLabel#activationWord {{
            font-size: 32px;
            font-weight: bold;
            color: {JarvisTheme.CYAN};
            letter-spacing: 8px;
        }}
        
        QLabel#activationProgress {{
            font-size: 18px;
            color: {JarvisTheme.CYAN_DIM};
        }}
    """
    
    # Dashboard specific styles
    DASHBOARD = f"""
        QWidget#dashboard {{
            background-color: {JarvisTheme.DARK};
        }}
        
        QLabel#aiName {{
            font-size: 36px;
            font-weight: bold;
            color: {JarvisTheme.CYAN};
            letter-spacing: 10px;
        }}
        
        QTextEdit#conversationArea {{
            background-color: transparent;
            border: none;
            font-size: 14px;
        }}
    """
    
    @staticmethod
    def get_glow_style(color: str = JarvisTheme.CYAN) -> str:
        """Generate a glow effect style string."""
        return f"box-shadow: 0 0 10px {color}, 0 0 20px {color};"

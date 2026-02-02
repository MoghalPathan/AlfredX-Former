"""
AlfredX Main Window
===================
Main application window that manages screens.
"""

from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QDesktopWidget
from PyQt5.QtCore import Qt

from config.settings import Settings
from gui.styles.themes import StyleSheet
from gui.login_screen import LoginScreen
from gui.dashboard import Dashboard


class MainWindow(QMainWindow):
    """
    Main application window.
    Manages login and dashboard screens.
    """
    
    def __init__(self):
        super().__init__()
        
        self._setup_window()
        self._setup_ui()
        self._connect_signals()
    
    def _setup_window(self):
        """Configure the main window."""
        self.setWindowTitle(Settings.WINDOW_TITLE)
        self.setMinimumSize(Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
        
        # Apply stylesheet
        self.setStyleSheet(StyleSheet.MAIN)
        
        # Remove window frame for custom look (optional)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Center on screen
        self._center_on_screen()
        
        # Set dark background
        self.setStyleSheet(self.styleSheet() + f"""
            QMainWindow {{
                background-color: {Settings.Colors.DARK};
            }}
        """)
    
    def _center_on_screen(self):
        """Center the window on the screen."""
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)
    
    def _setup_ui(self):
        """Setup the UI components."""
        # Stacked widget for screen management
        self._stack = QStackedWidget()
        self.setCentralWidget(self._stack)
        
        # Create screens
        self._login_screen = LoginScreen()
        self._dashboard = Dashboard()
        
        # Add to stack
        self._stack.addWidget(self._login_screen)
        self._stack.addWidget(self._dashboard)
        
        # Start with login
        self._stack.setCurrentWidget(self._login_screen)
    
    def _connect_signals(self):
        """Connect signals between components."""
        # Login successful -> show dashboard
        self._login_screen.login_successful.connect(self._on_login_success)
        
        # Dashboard signals
        self._dashboard.command_entered.connect(self._on_command)
        self._dashboard.mic_button_clicked.connect(self._on_mic_toggle)
    
    def _on_login_success(self):
        """Handle successful login."""
        self._stack.setCurrentWidget(self._dashboard)
        self._dashboard.add_alfred_message(
            "Good evening, Master Wayne. All systems operational. How may I assist you?"
        )
        self._dashboard.add_activity("System initialized")
    
    def _on_command(self, text: str):
        """Handle command from dashboard."""
        # This will be connected to the brain/skills in main.py
        pass
    
    def _on_mic_toggle(self):
        """Handle mic button toggle."""
        # This will be connected to the listener in main.py
        pass
    
    def get_login_screen(self) -> LoginScreen:
        """Get the login screen instance."""
        return self._login_screen
    
    def get_dashboard(self) -> Dashboard:
        """Get the dashboard instance."""
        return self._dashboard
    
    def show_dashboard(self):
        """Switch to dashboard view."""
        self._stack.setCurrentWidget(self._dashboard)
    
    def show_login(self):
        """Switch to login view."""
        self._stack.setCurrentWidget(self._login_screen)
    
    def closeEvent(self, event):
        """Handle window close."""
        # Cleanup code here
        event.accept()

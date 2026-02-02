"""
AlfredX System Control Skill
============================
Controls system operations: open apps, screenshots, system info, etc.
"""

import subprocess
import os
import psutil
from typing import Optional, Dict
from datetime import datetime

from config.settings import Settings


class SystemControl:
    """
    System control operations.
    Opens apps, takes screenshots, gets system info, etc.
    """
    
    def __init__(self):
        """Initialize system control."""
        self.known_apps = Settings.KNOWN_APPS
    
    def open_app(self, app_name: str) -> tuple[bool, str]:
        """
        Open an application.
        
        Args:
            app_name: Name of the application
            
        Returns:
            Tuple of (success, message)
        """
        app_name_lower = app_name.lower().strip()
        
        # Check if app is in known apps
        if app_name_lower in self.known_apps:
            executable = self.known_apps[app_name_lower]
        else:
            executable = app_name_lower
        
        try:
            # Try to open the app
            if os.name == 'nt':  # Windows
                subprocess.Popen(
                    f'start "" "{executable}"',
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            else:  # Linux/Mac
                subprocess.Popen(
                    [executable],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            
            return True, f"Opening {app_name}"
        
        except Exception as e:
            return False, f"Failed to open {app_name}: {str(e)}"
    
    def close_app(self, app_name: str) -> tuple[bool, str]:
        """
        Close an application.
        
        Args:
            app_name: Name of the application
            
        Returns:
            Tuple of (success, message)
        """
        app_name_lower = app_name.lower().strip()
        
        try:
            # Find and kill process
            for proc in psutil.process_iter(['name', 'pid']):
                if app_name_lower in proc.info['name'].lower():
                    proc.terminate()
                    return True, f"Closed {app_name}"
            
            return False, f"Could not find {app_name} running"
        
        except Exception as e:
            return False, f"Failed to close {app_name}: {str(e)}"
    
    def take_screenshot(self, filename: Optional[str] = None) -> tuple[bool, str]:
        """
        Take a screenshot.
        
        Args:
            filename: Optional filename (defaults to timestamp)
            
        Returns:
            Tuple of (success, filepath or error message)
        """
        try:
            import pyautogui
            from PIL import Image
            
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
            
            filepath = Settings.DATA_DIR / filename
            
            screenshot = pyautogui.screenshot()
            screenshot.save(str(filepath))
            
            return True, str(filepath)
        
        except Exception as e:
            return False, f"Failed to take screenshot: {str(e)}"
    
    def get_system_info(self) -> Dict:
        """
        Get current system information.
        
        Returns:
            Dictionary with system stats
        """
        try:
            cpu_percent = psutil.cpu_percent(interval=0.5)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Get battery info if available
            battery = None
            if hasattr(psutil, 'sensors_battery'):
                batt = psutil.sensors_battery()
                if batt:
                    battery = {
                        'percent': batt.percent,
                        'charging': batt.power_plugged
                    }
            
            return {
                'cpu': {
                    'percent': cpu_percent,
                    'cores': psutil.cpu_count()
                },
                'memory': {
                    'total': memory.total // (1024 ** 3),  # GB
                    'used': memory.used // (1024 ** 3),
                    'percent': memory.percent
                },
                'disk': {
                    'total': disk.total // (1024 ** 3),
                    'used': disk.used // (1024 ** 3),
                    'percent': disk.percent
                },
                'battery': battery
            }
        
        except Exception as e:
            return {'error': str(e)}
    
    def get_time(self) -> str:
        """Get current time as string."""
        now = datetime.now()
        return now.strftime("%I:%M %p")
    
    def get_date(self) -> str:
        """Get current date as string."""
        now = datetime.now()
        return now.strftime("%A, %B %d, %Y")
    
    def lock_screen(self) -> tuple[bool, str]:
        """Lock the screen."""
        try:
            if os.name == 'nt':  # Windows
                subprocess.run('rundll32.exe user32.dll,LockWorkStation', shell=True)
            else:
                # Linux (might vary by desktop environment)
                subprocess.run(['loginctl', 'lock-session'])
            
            return True, "Screen locked"
        
        except Exception as e:
            return False, f"Failed to lock screen: {str(e)}"
    
    def shutdown(self, delay: int = 60) -> tuple[bool, str]:
        """
        Schedule system shutdown.
        
        Args:
            delay: Delay in seconds (default 60)
        """
        try:
            if os.name == 'nt':
                subprocess.run(f'shutdown /s /t {delay}', shell=True)
            else:
                subprocess.run(['shutdown', '-h', f'+{delay // 60}'])
            
            return True, f"System will shutdown in {delay} seconds"
        
        except Exception as e:
            return False, f"Failed to schedule shutdown: {str(e)}"
    
    def cancel_shutdown(self) -> tuple[bool, str]:
        """Cancel scheduled shutdown."""
        try:
            if os.name == 'nt':
                subprocess.run('shutdown /a', shell=True)
            else:
                subprocess.run(['shutdown', '-c'])
            
            return True, "Shutdown cancelled"
        
        except Exception as e:
            return False, f"Failed to cancel shutdown: {str(e)}"

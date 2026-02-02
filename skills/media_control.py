"""
AlfredX Media Control Skill
===========================
Controls media playback and system volume.
"""

import subprocess
import os
from typing import Tuple

# Windows volume control
try:
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    PYCAW_AVAILABLE = True
except ImportError:
    PYCAW_AVAILABLE = False


class MediaControl:
    """
    Media control operations.
    Controls volume, playback, etc.
    """
    
    def __init__(self):
        """Initialize media control."""
        self._volume_interface = None
        self._init_volume_control()
    
    def _init_volume_control(self):
        """Initialize Windows volume control."""
        if PYCAW_AVAILABLE and os.name == 'nt':
            try:
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(
                    IAudioEndpointVolume._iid_, CLSCTX_ALL, None
                )
                self._volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
            except Exception as e:
                print(f"Volume control init failed: {e}")
    
    def get_volume(self) -> int:
        """
        Get current volume level (0-100).
        
        Returns:
            Volume percentage
        """
        if self._volume_interface:
            try:
                level = self._volume_interface.GetMasterVolumeLevelScalar()
                return int(level * 100)
            except:
                pass
        return 50  # Default
    
    def set_volume(self, level: int) -> Tuple[bool, str]:
        """
        Set volume level.
        
        Args:
            level: Volume percentage (0-100)
            
        Returns:
            Tuple of (success, message)
        """
        level = max(0, min(100, level))
        
        if self._volume_interface:
            try:
                self._volume_interface.SetMasterVolumeLevelScalar(level / 100, None)
                return True, f"Volume set to {level}%"
            except Exception as e:
                return False, f"Failed to set volume: {str(e)}"
        
        return False, "Volume control not available"
    
    def volume_up(self, step: int = 10) -> Tuple[bool, str]:
        """
        Increase volume.
        
        Args:
            step: Amount to increase
        """
        current = self.get_volume()
        return self.set_volume(current + step)
    
    def volume_down(self, step: int = 10) -> Tuple[bool, str]:
        """
        Decrease volume.
        
        Args:
            step: Amount to decrease
        """
        current = self.get_volume()
        return self.set_volume(current - step)
    
    def mute(self) -> Tuple[bool, str]:
        """Mute audio."""
        if self._volume_interface:
            try:
                self._volume_interface.SetMute(1, None)
                return True, "Audio muted"
            except Exception as e:
                return False, f"Failed to mute: {str(e)}"
        return False, "Volume control not available"
    
    def unmute(self) -> Tuple[bool, str]:
        """Unmute audio."""
        if self._volume_interface:
            try:
                self._volume_interface.SetMute(0, None)
                return True, "Audio unmuted"
            except Exception as e:
                return False, f"Failed to unmute: {str(e)}"
        return False, "Volume control not available"
    
    def is_muted(self) -> bool:
        """Check if audio is muted."""
        if self._volume_interface:
            try:
                return bool(self._volume_interface.GetMute())
            except:
                pass
        return False
    
    def play_pause(self) -> Tuple[bool, str]:
        """Send play/pause media key."""
        try:
            import pyautogui
            pyautogui.press('playpause')
            return True, "Toggled play/pause"
        except Exception as e:
            return False, f"Failed: {str(e)}"
    
    def next_track(self) -> Tuple[bool, str]:
        """Send next track media key."""
        try:
            import pyautogui
            pyautogui.press('nexttrack')
            return True, "Skipped to next track"
        except Exception as e:
            return False, f"Failed: {str(e)}"
    
    def previous_track(self) -> Tuple[bool, str]:
        """Send previous track media key."""
        try:
            import pyautogui
            pyautogui.press('prevtrack')
            return True, "Went to previous track"
        except Exception as e:
            return False, f"Failed: {str(e)}"
    
    def stop(self) -> Tuple[bool, str]:
        """Send stop media key."""
        try:
            import pyautogui
            pyautogui.press('stop')
            return True, "Stopped playback"
        except Exception as e:
            return False, f"Failed: {str(e)}"

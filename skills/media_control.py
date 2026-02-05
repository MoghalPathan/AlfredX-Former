"""
AlfredX Media Control Skill
===========================
Controls media playback and system volume.
"""

import subprocess
import os
from typing import Tuple

# Windows volume control
PYCAW_AVAILABLE = False
try:
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    PYCAW_AVAILABLE = True
except ImportError:
    print("⚠️ pycaw not available - volume control disabled")


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
        if not PYCAW_AVAILABLE:
            print("⚠️ Volume control not available (pycaw not installed)")
            return
            
        if os.name != 'nt':
            print("⚠️ Volume control only available on Windows")
            return
            
        try:
            # Get default audio device
            devices = AudioUtilities.GetSpeakers()
            
            # Try the new API first
            try:
                interface = devices.Activate(
                    IAudioEndpointVolume._iid_, 
                    CLSCTX_ALL, 
                    None
                )
                self._volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
                print("✅ Volume control initialized")
            except AttributeError:
                # Fallback for older pycaw versions
                try:
                    from pycaw.pycaw import ISimpleAudioVolume
                    sessions = AudioUtilities.GetAllSessions()
                    print("⚠️ Using fallback volume control")
                except:
                    print("⚠️ Volume control fallback failed")
                    
        except Exception as e:
            print(f"⚠️ Volume control init failed: {e}")
            self._volume_interface = None
    
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
            except Exception as e:
                print(f"Get volume error: {e}")
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
        
        # Fallback: use nircmd or PowerShell on Windows
        if os.name == 'nt':
            try:
                # PowerShell fallback
                ps_command = f'''
                $obj = new-object -com wscript.shell
                $obj.SendKeys([char]173)
                '''
                # This is limited, so just report unavailable
                return False, "Volume control not available. Please adjust manually."
            except:
                pass
        
        return False, "Volume control not available"
    
    def volume_up(self, step: int = 10) -> Tuple[bool, str]:
        """
        Increase volume.
        
        Args:
            step: Amount to increase
        """
        if self._volume_interface:
            current = self.get_volume()
            return self.set_volume(current + step)
        
        # Fallback: use keyboard media key
        try:
            import pyautogui
            pyautogui.press('volumeup')
            pyautogui.press('volumeup')
            return True, "Volume increased"
        except Exception as e:
            return False, f"Failed to increase volume: {e}"
    
    def volume_down(self, step: int = 10) -> Tuple[bool, str]:
        """
        Decrease volume.
        
        Args:
            step: Amount to decrease
        """
        if self._volume_interface:
            current = self.get_volume()
            return self.set_volume(current - step)
        
        # Fallback: use keyboard media key
        try:
            import pyautogui
            pyautogui.press('volumedown')
            pyautogui.press('volumedown')
            return True, "Volume decreased"
        except Exception as e:
            return False, f"Failed to decrease volume: {e}"
    
    def mute(self) -> Tuple[bool, str]:
        """Mute audio."""
        if self._volume_interface:
            try:
                self._volume_interface.SetMute(1, None)
                return True, "Audio muted"
            except Exception as e:
                pass
        
        # Fallback: use keyboard
        try:
            import pyautogui
            pyautogui.press('volumemute')
            return True, "Audio muted"
        except Exception as e:
            return False, f"Failed to mute: {str(e)}"
    
    def unmute(self) -> Tuple[bool, str]:
        """Unmute audio."""
        if self._volume_interface:
            try:
                self._volume_interface.SetMute(0, None)
                return True, "Audio unmuted"
            except Exception as e:
                pass
        
        # Fallback: use keyboard
        try:
            import pyautogui
            pyautogui.press('volumemute')
            return True, "Audio unmuted"
        except Exception as e:
            return False, f"Failed to unmute: {str(e)}"
    
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

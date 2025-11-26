import pyautogui
import subprocess
import time
import os
from typing import Dict, Any

class AutomationTools:
    def __init__(self):
        # Fail-safe: Move mouse to corner to abort
        pyautogui.FAILSAFE = True
        
    def execute(self, tool_name: str, params: str) -> str:
        """Execute automation tools"""
        try:
            if tool_name == "open_app":
                return self.open_app(params)
            elif tool_name == "type_text":
                return self.type_text(params)
            elif tool_name == "press_key":
                return self.press_key(params)
            elif tool_name == "click":
                return self.click()
            else:
                return f"Unknown automation tool: {tool_name}"
        except Exception as e:
            return f"Automation Error: {str(e)}"

    def open_app(self, app_name: str) -> str:
        """Open an application using Windows Run or Start Menu"""
        try:
            # Clean app name
            app_name = app_name.strip().lower()
            
            # Common mappings
            apps = {
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "chrome": "chrome.exe",
                "spotify": "spotify.exe",
                "explorer": "explorer.exe",
                "cmd": "cmd.exe",
                "powershell": "powershell.exe",
                "whatsapp": "start whatsapp:",
                "word": "start winword",
                "excel": "start excel"
            }
            
            target = apps.get(app_name, app_name)
            
            # Try to open via subprocess
            if target.startswith("start "):
                os.system(target)
                return f"Launched {app_name} via system command"
            else:
                subprocess.Popen(target, shell=True)
                return f"Launched {app_name}"
            
        except Exception as e:
            # Fallback: Use Start Menu search
            print(f"Direct launch failed: {e}. Trying Start Menu...")
            pyautogui.press('win')
            time.sleep(1)
            pyautogui.write(app_name)
            time.sleep(1)
            pyautogui.press('enter')
            return f"Attempted to launch {app_name} via Start Menu (Please verify it opened)"

    def type_text(self, text: str) -> str:
        """Type text at current cursor position"""
        pyautogui.write(text, interval=0.05)
        return f"Typed: {text}"

    def press_key(self, key: str) -> str:
        """Press a specific key"""
        pyautogui.press(key)
        return f"Pressed {key}"

    def click(self) -> str:
        """Click current mouse position"""
        pyautogui.click()
        return "Clicked mouse"

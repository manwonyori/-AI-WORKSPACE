"""
Action Executor for Computer Use Agent
Handles low-level execution of computer control actions
"""

import time
import logging
import subprocess
from typing import Any, Dict, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    import pyautogui
    import mss
    import keyboard
    import mouse
    from PIL import Image
    import cv2
    import numpy as np
    import pytesseract
    LIBS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Some libraries not available: {e}")
    LIBS_AVAILABLE = False


class ActionExecutor:
    """Executes low-level computer control actions"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.failsafe = self.config.get('failsafe', True)
        
        if LIBS_AVAILABLE:
            # Configure pyautogui
            pyautogui.FAILSAFE = self.failsafe
            pyautogui.PAUSE = self.config.get('action_delay', 0.1)
            
            # Initialize screen capture
            self.sct = mss.mss()
        
        logger.info("Action Executor initialized")
    
    def take_screenshot(self, region: Optional[Tuple[int, int, int, int]] = None, 
                       save_path: Optional[str] = None) -> Any:
        """Take a screenshot of the screen or specific region"""
        if not LIBS_AVAILABLE:
            logger.error("Screenshot libraries not available")
            return None
        
        try:
            if region:
                # Capture specific region
                monitor = {
                    "top": region[1],
                    "left": region[0],
                    "width": region[2],
                    "height": region[3]
                }
            else:
                # Capture entire primary screen
                monitor = self.sct.monitors[1]
            
            screenshot = self.sct.grab(monitor)
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            
            if save_path:
                img.save(save_path)
                logger.info(f"Screenshot saved to {save_path}")
            
            return img
            
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            return None
    
    def click(self, x: Optional[int] = None, y: Optional[int] = None,
             button: str = 'left', clicks: int = 1, interval: float = 0.0) -> bool:
        """Click at specified coordinates or current position"""
        if not LIBS_AVAILABLE:
            logger.error("Click libraries not available")
            return False
        
        try:
            if x is not None and y is not None:
                pyautogui.click(x, y, button=button, clicks=clicks, interval=interval)
                logger.info(f"Clicked at ({x}, {y}) with {button} button")
            else:
                pyautogui.click(button=button, clicks=clicks, interval=interval)
                logger.info(f"Clicked at current position with {button} button")
            return True
            
        except Exception as e:
            logger.error(f"Click failed: {e}")
            return False
    
    def type_text(self, text: str, interval: float = 0.0) -> bool:
        """Type text using keyboard"""
        if not LIBS_AVAILABLE:
            logger.error("Typing libraries not available")
            return False
        
        try:
            pyautogui.typewrite(text, interval=interval)
            logger.info(f"Typed text: {text[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Typing failed: {e}")
            return False
    
    def press_key(self, key: str, presses: int = 1, interval: float = 0.0) -> bool:
        """Press a keyboard key"""
        if not LIBS_AVAILABLE:
            logger.error("Keyboard libraries not available")
            return False
        
        try:
            pyautogui.press(key, presses=presses, interval=interval)
            logger.info(f"Pressed key: {key}")
            return True
            
        except Exception as e:
            logger.error(f"Key press failed: {e}")
            return False
    
    def hotkey(self, *keys) -> bool:
        """Press a keyboard hotkey combination"""
        if not LIBS_AVAILABLE:
            logger.error("Keyboard libraries not available")
            return False
        
        try:
            pyautogui.hotkey(*keys)
            logger.info(f"Pressed hotkey: {'+'.join(keys)}")
            return True
            
        except Exception as e:
            logger.error(f"Hotkey failed: {e}")
            return False
    
    def scroll(self, clicks: int, x: Optional[int] = None, 
              y: Optional[int] = None) -> bool:
        """Scroll the mouse wheel"""
        if not LIBS_AVAILABLE:
            logger.error("Scroll libraries not available")
            return False
        
        try:
            if x is not None and y is not None:
                pyautogui.moveTo(x, y)
            pyautogui.scroll(clicks)
            logger.info(f"Scrolled {clicks} clicks")
            return True
            
        except Exception as e:
            logger.error(f"Scroll failed: {e}")
            return False
    
    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int,
            duration: float = 0.5, button: str = 'left') -> bool:
        """Drag from one position to another"""
        if not LIBS_AVAILABLE:
            logger.error("Drag libraries not available")
            return False
        
        try:
            pyautogui.moveTo(start_x, start_y)
            pyautogui.dragTo(end_x, end_y, duration=duration, button=button)
            logger.info(f"Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})")
            return True
            
        except Exception as e:
            logger.error(f"Drag failed: {e}")
            return False
    
    def move_to(self, x: int, y: int, duration: float = 0.0) -> bool:
        """Move mouse to specified position"""
        if not LIBS_AVAILABLE:
            logger.error("Move libraries not available")
            return False
        
        try:
            pyautogui.moveTo(x, y, duration=duration)
            logger.info(f"Moved to ({x}, {y})")
            return True
            
        except Exception as e:
            logger.error(f"Move failed: {e}")
            return False
    
    def wait(self, seconds: float) -> bool:
        """Wait for specified seconds"""
        try:
            time.sleep(seconds)
            logger.info(f"Waited {seconds} seconds")
            return True
            
        except Exception as e:
            logger.error(f"Wait failed: {e}")
            return False
    
    def find_on_screen(self, image_path: Optional[str] = None,
                      query: Optional[str] = None,
                      confidence: float = 0.8) -> Optional[Dict]:
        """Find an element on screen by image or text"""
        if not LIBS_AVAILABLE:
            logger.error("Vision libraries not available")
            return None
        
        try:
            screenshot = self.take_screenshot()
            
            if image_path:
                # Find by image template matching
                template = Image.open(image_path)
                location = pyautogui.locateOnScreen(template, confidence=confidence)
                
                if location:
                    center = pyautogui.center(location)
                    return {
                        "found": True,
                        "x": center.x,
                        "y": center.y,
                        "width": location.width,
                        "height": location.height
                    }
            
            elif query:
                # Find by text using OCR
                text_data = self.read_screen()
                if query.lower() in text_data.lower():
                    # Simple text found indicator
                    # More sophisticated text location would require OCR with positions
                    return {
                        "found": True,
                        "text": query,
                        "full_text": text_data
                    }
            
            return {"found": False}
            
        except Exception as e:
            logger.error(f"Find on screen failed: {e}")
            return None
    
    def read_screen(self, region: Optional[Tuple[int, int, int, int]] = None) -> str:
        """Read text from screen using OCR"""
        if not LIBS_AVAILABLE:
            logger.error("OCR libraries not available")
            return ""
        
        try:
            screenshot = self.take_screenshot(region)
            
            if screenshot:
                # Convert PIL Image to numpy array for OCR
                img_array = np.array(screenshot)
                text = pytesseract.image_to_string(img_array)
                logger.info(f"Read {len(text)} characters from screen")
                return text
            
            return ""
            
        except Exception as e:
            logger.error(f"Screen reading failed: {e}")
            return ""
    
    def execute_command(self, command: str, shell: bool = True) -> Dict:
        """Execute a system command"""
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            logger.info(f"Executed command: {command}")
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out: {command}")
            return {
                "success": False,
                "error": "Command timed out"
            }
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_mouse_position(self) -> Tuple[int, int]:
        """Get current mouse position"""
        if not LIBS_AVAILABLE:
            return (0, 0)
        
        try:
            pos = pyautogui.position()
            return (pos.x, pos.y)
        except Exception as e:
            logger.error(f"Failed to get mouse position: {e}")
            return (0, 0)
    
    def get_screen_size(self) -> Tuple[int, int]:
        """Get screen dimensions"""
        if not LIBS_AVAILABLE:
            return (1920, 1080)  # Default fallback
        
        try:
            size = pyautogui.size()
            return (size.width, size.height)
        except Exception as e:
            logger.error(f"Failed to get screen size: {e}")
            return (1920, 1080)
    
    def is_on_screen(self, x: int, y: int) -> bool:
        """Check if coordinates are on screen"""
        width, height = self.get_screen_size()
        return 0 <= x < width and 0 <= y < height
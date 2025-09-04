"""
Main Computer Use Agent Implementation for Claude Code
"""

import time
import json
import logging
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path

from .base import BaseAgent, Action, ActionResult, ActionType
from .executor import ActionExecutor

logger = logging.getLogger(__name__)


class ComputerUseAgent(BaseAgent):
    """
    Claude Code Computer Use Agent
    Provides computer automation capabilities with vision and control
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.claude_api_key = self.config.get('claude_api_key')
        self.vision_model = None
        self.context_memory = []
        self.max_memory_size = 100
        super().__init__(config)
        self.executor = ActionExecutor(config)
        
    def _initialize(self):
        """Initialize the Computer Use Agent"""
        logger.info("Initializing Computer Use Agent")
        
        # Set up vision capabilities
        if self.config.get('enable_vision', True):
            self._setup_vision()
        
        # Set up Claude integration if API key provided
        if self.claude_api_key:
            self._setup_claude()
            
        logger.info("Computer Use Agent initialized successfully")
    
    def _setup_vision(self):
        """Set up computer vision capabilities"""
        try:
            from ..vision.processor import VisionProcessor
            self.vision_processor = VisionProcessor()
            logger.info("Vision capabilities enabled")
        except ImportError:
            logger.warning("Vision module not available")
            self.vision_processor = None
    
    def _setup_claude(self):
        """Set up Claude AI integration"""
        try:
            import anthropic
            self.claude_client = anthropic.Anthropic(api_key=self.claude_api_key)
            logger.info("Claude integration enabled")
        except ImportError:
            logger.warning("Anthropic library not installed")
            self.claude_client = None
    
    def execute_action(self, action: Action) -> ActionResult:
        """Execute a single action"""
        start_time = time.time()
        
        try:
            # Log action execution
            logger.info(f"Executing {action.type.value}: {action.parameters}")
            
            # Execute based on action type
            if action.type == ActionType.SCREENSHOT:
                result = self.executor.take_screenshot(**action.parameters)
            elif action.type == ActionType.CLICK:
                result = self.executor.click(**action.parameters)
            elif action.type == ActionType.TYPE:
                result = self.executor.type_text(**action.parameters)
            elif action.type == ActionType.KEY:
                result = self.executor.press_key(**action.parameters)
            elif action.type == ActionType.SCROLL:
                result = self.executor.scroll(**action.parameters)
            elif action.type == ActionType.DRAG:
                result = self.executor.drag(**action.parameters)
            elif action.type == ActionType.WAIT:
                result = self.executor.wait(**action.parameters)
            elif action.type == ActionType.FIND:
                result = self.executor.find_on_screen(**action.parameters)
            elif action.type == ActionType.READ:
                result = self.executor.read_screen(**action.parameters)
            elif action.type == ActionType.EXECUTE:
                result = self.executor.execute_command(**action.parameters)
            else:
                raise ValueError(f"Unknown action type: {action.type}")
            
            duration = time.time() - start_time
            return ActionResult(
                success=True,
                data=result,
                duration=duration
            )
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Action failed: {str(e)}")
            return ActionResult(
                success=False,
                error=str(e),
                duration=duration
            )
    
    def plan_actions(self, task: str) -> List[Action]:
        """Plan a sequence of actions for a given task"""
        logger.info(f"Planning actions for task: {task}")
        
        # If Claude is available, use it for planning
        if self.claude_client:
            return self._plan_with_claude(task)
        
        # Otherwise use rule-based planning
        return self._plan_rule_based(task)
    
    def _plan_with_claude(self, task: str) -> List[Action]:
        """Use Claude to plan actions"""
        try:
            # Take screenshot for context
            screenshot = self.capture_screenshot()
            
            # Create prompt for Claude
            prompt = f"""
            Task: {task}
            
            Current screen context is provided. Plan a sequence of actions to complete this task.
            Return actions in JSON format with type and parameters.
            
            Available action types:
            - screenshot: Capture screen
            - click: Click at coordinates or element
            - type: Type text
            - key: Press keyboard key
            - scroll: Scroll page
            - wait: Wait for seconds
            - find: Find element on screen
            - read: Read text from screen
            """
            
            # Get Claude's response
            response = self.claude_client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Parse actions from response
            actions = self._parse_claude_response(response.content)
            return actions
            
        except Exception as e:
            logger.error(f"Claude planning failed: {e}")
            return self._plan_rule_based(task)
    
    def _plan_rule_based(self, task: str) -> List[Action]:
        """Simple rule-based action planning"""
        actions = []
        
        # Basic planning based on keywords
        task_lower = task.lower()
        
        if "screenshot" in task_lower:
            actions.append(Action(
                type=ActionType.SCREENSHOT,
                parameters={},
                description="Capture current screen"
            ))
        
        if "click" in task_lower:
            actions.append(Action(
                type=ActionType.FIND,
                parameters={"query": "button"},
                description="Find clickable element"
            ))
            actions.append(Action(
                type=ActionType.CLICK,
                parameters={},
                description="Click found element"
            ))
        
        if "type" in task_lower or "write" in task_lower:
            actions.append(Action(
                type=ActionType.TYPE,
                parameters={"text": ""},
                description="Type text"
            ))
        
        if "read" in task_lower:
            actions.append(Action(
                type=ActionType.READ,
                parameters={},
                description="Read screen content"
            ))
        
        # Default: take screenshot if no specific actions
        if not actions:
            actions.append(Action(
                type=ActionType.SCREENSHOT,
                parameters={},
                description="Capture screen for analysis"
            ))
        
        return actions
    
    def _parse_claude_response(self, response: str) -> List[Action]:
        """Parse Claude's response into actions"""
        actions = []
        try:
            # Extract JSON from response
            import re
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                action_data = json.loads(json_match.group())
                for item in action_data:
                    action = Action(
                        type=ActionType(item['type']),
                        parameters=item.get('parameters', {}),
                        description=item.get('description')
                    )
                    actions.append(action)
        except Exception as e:
            logger.error(f"Failed to parse Claude response: {e}")
        
        return actions
    
    def capture_screenshot(self) -> Any:
        """Capture current screen"""
        return self.executor.take_screenshot()
    
    def find_element(self, query: str) -> Optional[Dict]:
        """Find an element on screen"""
        return self.executor.find_on_screen({"query": query})
    
    def analyze_screen(self, instruction: str = None) -> Dict:
        """Analyze current screen with optional instruction"""
        screenshot = self.capture_screenshot()
        
        analysis = {
            "timestamp": time.time(),
            "screenshot": screenshot,
            "elements": []
        }
        
        # Use vision processor if available
        if self.vision_processor:
            detected = self.vision_processor.detect_elements(screenshot)
            analysis["elements"] = detected
        
        # Use Claude for detailed analysis if available
        if self.claude_client and instruction:
            analysis["claude_analysis"] = self._analyze_with_claude(
                screenshot, instruction
            )
        
        return analysis
    
    def _analyze_with_claude(self, screenshot, instruction: str) -> str:
        """Use Claude to analyze screenshot"""
        try:
            response = self.claude_client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=500,
                messages=[
                    {
                        "role": "user",
                        "content": f"Analyze this screenshot. {instruction}"
                    }
                ]
            )
            return response.content
        except Exception as e:
            logger.error(f"Claude analysis failed: {e}")
            return ""
    
    def record_session(self, output_path: str = None):
        """Record all actions in a session"""
        if not output_path:
            output_path = f"session_{int(time.time())}.json"
        
        session_data = {
            "timestamp": time.time(),
            "config": self.config,
            "actions": [
                {
                    "action": action.to_dict(),
                    "result": result.to_dict()
                }
                for action, result in self.history
            ]
        }
        
        with open(output_path, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        logger.info(f"Session recorded to {output_path}")
        return output_path
    
    def replay_session(self, session_path: str) -> List[ActionResult]:
        """Replay a recorded session"""
        with open(session_path, 'r') as f:
            session_data = json.load(f)
        
        results = []
        for item in session_data['actions']:
            action_data = item['action']
            action = Action(
                type=ActionType(action_data['type']),
                parameters=action_data['parameters'],
                description=action_data.get('description'),
                timeout=action_data.get('timeout', 30.0)
            )
            result = self.execute_action(action)
            results.append(result)
            
            if not result.success:
                logger.error(f"Replay failed at action: {action.type.value}")
                break
        
        return results
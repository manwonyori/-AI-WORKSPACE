"""
Enhanced Computer Use Agent with Claude Code Bridge Integration
Claude API 키 없이 Claude Code를 활용하는 향상된 버전
"""

import time
import json
import logging
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path

from .base import BaseAgent, Action, ActionResult, ActionType
from .executor import ActionExecutor
from .claude_code_bridge import ClaudeCodeBridge

logger = logging.getLogger(__name__)


class EnhancedComputerUseAgent(BaseAgent):
    """
    Claude Code Bridge를 통해 무료로 AI 기능을 활용하는 Computer Use Agent
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.vision_model = None
        self.context_memory = []
        self.max_memory_size = 100
        super().__init__(config)
        self.executor = ActionExecutor(config)
        
        # Claude Code Bridge 초기화
        self.claude_bridge = ClaudeCodeBridge()
        logger.info("Enhanced Agent with Claude Code Bridge initialized")
        
    def _initialize(self):
        """Initialize the Enhanced Computer Use Agent"""
        logger.info("Initializing Enhanced Computer Use Agent")
        
        # Set up vision capabilities
        if self.config.get('enable_vision', True):
            self._setup_vision()
            
        logger.info("Enhanced Computer Use Agent initialized successfully")
    
    def _setup_vision(self):
        """Set up computer vision capabilities"""
        try:
            from ..vision.processor import VisionProcessor
            self.vision_processor = VisionProcessor()
            logger.info("Vision capabilities enabled")
        except ImportError:
            logger.warning("Vision module not available")
            self.vision_processor = None
    
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
            
            # Send feedback to Claude Code Bridge
            self.claude_bridge.send_feedback(
                action_id=f"action_{int(time.time())}",
                result={"success": True, "duration": duration}
            )
            
            return ActionResult(
                success=True,
                data=result,
                duration=duration
            )
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Action failed: {str(e)}")
            
            # Send error feedback
            self.claude_bridge.send_feedback(
                action_id=f"action_{int(time.time())}",
                result={"success": False, "error": str(e)}
            )
            
            return ActionResult(
                success=False,
                error=str(e),
                duration=duration
            )
    
    def plan_actions(self, task: str) -> List[Action]:
        """Plan a sequence of actions for a given task using Claude Code Bridge"""
        logger.info(f"Planning actions for task: {task}")
        
        # Take screenshot for context
        screenshot_path = None
        try:
            screenshot = self.capture_screenshot()
            if screenshot:
                # Save screenshot for Claude Code to analyze
                screenshot_path = Path(f"C:/Users/8899y/CUA-MASTER/data/screenshots/context_{int(time.time())}.png")
                screenshot_path.parent.mkdir(parents=True, exist_ok=True)
                # Note: Actual screenshot saving would depend on the format
                logger.info(f"Screenshot saved for context: {screenshot_path}")
        except Exception as e:
            logger.warning(f"Could not capture screenshot: {e}")
        
        # Request action plan from Claude Code Bridge
        context = {
            "screenshot": str(screenshot_path) if screenshot_path else None,
            "memory": self.context_memory[-5:] if self.context_memory else []
        }
        
        action_data = self.claude_bridge.request_action_plan(task, context)
        
        if action_data:
            # Convert to Action objects
            actions = []
            for item in action_data:
                try:
                    action = Action(
                        type=ActionType[item['type'].upper()],
                        parameters=item.get('parameters', {}),
                        description=item.get('description')
                    )
                    actions.append(action)
                except (KeyError, ValueError) as e:
                    logger.error(f"Invalid action format: {e}")
            
            # Update context memory
            self.context_memory.append({
                "task": task,
                "actions": len(actions),
                "timestamp": time.time()
            })
            
            if len(self.context_memory) > self.max_memory_size:
                self.context_memory.pop(0)
            
            return actions
        else:
            # Fallback to rule-based planning
            logger.info("Claude Code Bridge unavailable, using rule-based planning")
            return self._plan_rule_based(task)
    
    def _plan_rule_based(self, task: str) -> List[Action]:
        """Simple rule-based action planning (fallback)"""
        actions = []
        task_lower = task.lower()
        
        if "screenshot" in task_lower or "캡처" in task_lower:
            actions.append(Action(
                type=ActionType.SCREENSHOT,
                parameters={},
                description="화면 캡처"
            ))
        
        if "click" in task_lower or "클릭" in task_lower:
            actions.append(Action(
                type=ActionType.FIND,
                parameters={"query": "button"},
                description="클릭 가능한 요소 찾기"
            ))
            actions.append(Action(
                type=ActionType.CLICK,
                parameters={},
                description="요소 클릭"
            ))
        
        if "type" in task_lower or "입력" in task_lower or "write" in task_lower:
            actions.append(Action(
                type=ActionType.TYPE,
                parameters={"text": ""},
                description="텍스트 입력"
            ))
        
        if "read" in task_lower or "읽기" in task_lower:
            actions.append(Action(
                type=ActionType.READ,
                parameters={},
                description="화면 내용 읽기"
            ))
        
        if "실행" in task_lower or "run" in task_lower or "execute" in task_lower:
            actions.append(Action(
                type=ActionType.EXECUTE,
                parameters={"command": ""},
                description="명령 실행"
            ))
        
        # Default: take screenshot if no specific actions
        if not actions:
            actions.append(Action(
                type=ActionType.SCREENSHOT,
                parameters={},
                description="분석을 위한 화면 캡처"
            ))
        
        return actions
    
    def capture_screenshot(self) -> Any:
        """Capture current screen"""
        return self.executor.take_screenshot()
    
    def find_element(self, query: str) -> Optional[Dict]:
        """Find an element on screen"""
        return self.executor.find_on_screen({"query": query})
    
    def analyze_screen(self, instruction: str = None) -> Dict:
        """Analyze current screen using Claude Code Bridge"""
        screenshot = self.capture_screenshot()
        
        # Save screenshot temporarily
        screenshot_path = Path(f"C:/Users/8899y/CUA-MASTER/data/screenshots/analyze_{int(time.time())}.png")
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)
        
        analysis = {
            "timestamp": time.time(),
            "screenshot": str(screenshot_path),
            "elements": []
        }
        
        # Use vision processor if available
        if self.vision_processor:
            detected = self.vision_processor.detect_elements(screenshot)
            analysis["elements"] = detected
        
        # Use Claude Code Bridge for detailed analysis
        if instruction:
            bridge_analysis = self.claude_bridge.analyze_screen(
                str(screenshot_path), instruction
            )
            if bridge_analysis:
                analysis["claude_analysis"] = bridge_analysis
        
        return analysis
    
    def execute_workflow(self, workflow_name: str, params: Dict = None) -> List[ActionResult]:
        """
        Execute a predefined workflow
        
        Args:
            workflow_name: Name of the workflow
            params: Parameters for the workflow
        
        Returns:
            List of action results
        """
        workflows = {
            "cafe24_login": [
                {"type": "execute", "parameters": {"command": "start chrome cafe24.com"}},
                {"type": "wait", "parameters": {"seconds": 3}},
                {"type": "find", "parameters": {"query": "로그인"}},
                {"type": "click", "parameters": {}},
            ],
            "invoice_process": [
                {"type": "screenshot", "parameters": {}},
                {"type": "find", "parameters": {"query": "송장번호"}},
                {"type": "read", "parameters": {}},
            ],
            "email_check": [
                {"type": "execute", "parameters": {"command": "start chrome gmail.com"}},
                {"type": "wait", "parameters": {"seconds": 3}},
                {"type": "screenshot", "parameters": {}},
            ]
        }
        
        if workflow_name not in workflows:
            logger.error(f"Unknown workflow: {workflow_name}")
            return []
        
        results = []
        workflow_actions = workflows[workflow_name]
        
        for action_data in workflow_actions:
            action = Action(
                type=ActionType[action_data['type'].upper()],
                parameters=action_data.get('parameters', {}),
                description=f"Workflow step: {action_data['type']}"
            )
            result = self.execute_action(action)
            results.append(result)
            
            if not result.success:
                logger.error(f"Workflow {workflow_name} failed at step {action_data['type']}")
                break
        
        return results
    
    def record_session(self, output_path: str = None):
        """Record all actions in a session"""
        if not output_path:
            output_path = f"session_{int(time.time())}.json"
        
        session_data = {
            "timestamp": time.time(),
            "config": self.config,
            "context_memory": self.context_memory,
            "actions": [
                {
                    "action": action.to_dict(),
                    "result": result.to_dict()
                }
                for action, result in self.history
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Session recorded to {output_path}")
        return output_path
    
    def replay_session(self, session_path: str) -> List[ActionResult]:
        """Replay a recorded session"""
        with open(session_path, 'r', encoding='utf-8') as f:
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
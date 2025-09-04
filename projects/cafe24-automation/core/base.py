"""
Base Agent Interface for Computer Use
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ActionType(Enum):
    """Types of actions the agent can perform"""
    SCREENSHOT = "screenshot"
    CLICK = "click"
    TYPE = "type"
    KEY = "key"
    SCROLL = "scroll"
    DRAG = "drag"
    WAIT = "wait"
    FIND = "find"
    READ = "read"
    EXECUTE = "execute"


@dataclass
class Action:
    """Represents a single action to be performed"""
    type: ActionType
    parameters: Dict[str, Any]
    description: Optional[str] = None
    timeout: float = 30.0
    
    def to_dict(self) -> Dict:
        return {
            "type": self.type.value,
            "parameters": self.parameters,
            "description": self.description,
            "timeout": self.timeout
        }


@dataclass
class ActionResult:
    """Result of an action execution"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    screenshot: Optional[Any] = None
    duration: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "duration": self.duration
        }


class BaseAgent(ABC):
    """Base class for all computer use agents"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.history: List[Tuple[Action, ActionResult]] = []
        self.session_id = None
        self._initialize()
    
    @abstractmethod
    def _initialize(self):
        """Initialize the agent"""
        pass
    
    @abstractmethod
    def execute_action(self, action: Action) -> ActionResult:
        """Execute a single action"""
        pass
    
    @abstractmethod
    def plan_actions(self, task: str) -> List[Action]:
        """Plan a sequence of actions for a given task"""
        pass
    
    def execute_task(self, task: str) -> List[ActionResult]:
        """Execute a complete task"""
        logger.info(f"Executing task: {task}")
        actions = self.plan_actions(task)
        results = []
        
        for action in actions:
            logger.info(f"Executing action: {action.type.value}")
            result = self.execute_action(action)
            results.append(result)
            self.history.append((action, result))
            
            if not result.success:
                logger.error(f"Action failed: {result.error}")
                break
        
        return results
    
    def get_history(self) -> List[Tuple[Action, ActionResult]]:
        """Get execution history"""
        return self.history
    
    def clear_history(self):
        """Clear execution history"""
        self.history = []
    
    @abstractmethod
    def capture_screenshot(self) -> Any:
        """Capture current screen"""
        pass
    
    @abstractmethod
    def find_element(self, query: str) -> Optional[Dict]:
        """Find an element on screen"""
        pass
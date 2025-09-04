"""
Computer Use Agent Core Module
Claude Code Agent for computer automation and interaction
"""

from .agent import ComputerUseAgent
from .base import BaseAgent
from .executor import ActionExecutor

__version__ = "1.0.0"
__all__ = ["ComputerUseAgent", "BaseAgent", "ActionExecutor"]
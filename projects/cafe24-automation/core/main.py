"""
Computer Use Agent - Main Entry Point
Claude Code Agent for computer automation
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

from core import ComputerUseAgent
from core.base import ActionType

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ComputerUseAgentCLI:
    """Command-line interface for Computer Use Agent"""
    
    def __init__(self):
        self.config = self._load_config()
        self.agent = ComputerUseAgent(self.config)
        
    def _load_config(self) -> dict:
        """Load configuration from file or environment"""
        config = {
            'claude_api_key': os.getenv('ANTHROPIC_API_KEY'),
            'enable_vision': True,
            'failsafe': True,
            'action_delay': 0.1
        }
        
        # Try to load from config file
        config_path = Path('configs/config.json')
        if config_path.exists():
            with open(config_path, 'r') as f:
                file_config = json.load(f)
                config.update(file_config)
        
        return config
    
    def run_interactive(self):
        """Run interactive mode"""
        print("\n=== Computer Use Agent - Claude Code ===")
        print("Type 'help' for available commands or 'quit' to exit\n")
        
        while True:
            try:
                command = input("Agent> ").strip()
                
                if command.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                    
                elif command.lower() == 'help':
                    self._show_help()
                    
                elif command.lower() == 'screenshot':
                    self._take_screenshot()
                    
                elif command.lower().startswith('click '):
                    coords = command[6:].split(',')
                    if len(coords) == 2:
                        x, y = int(coords[0]), int(coords[1])
                        self._click(x, y)
                    
                elif command.lower().startswith('type '):
                    text = command[5:]
                    self._type_text(text)
                    
                elif command.lower().startswith('find '):
                    query = command[5:]
                    self._find_element(query)
                    
                elif command.lower() == 'analyze':
                    self._analyze_screen()
                    
                elif command.lower().startswith('task '):
                    task = command[5:]
                    self._execute_task(task)
                    
                elif command.lower() == 'record start':
                    print("Recording session...")
                    
                elif command.lower() == 'record stop':
                    path = self.agent.record_session()
                    print(f"Session saved to {path}")
                    
                elif command.lower() == 'history':
                    self._show_history()
                    
                else:
                    print(f"Unknown command: {command}")
                    print("Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                print("\nUse 'quit' to exit")
            except Exception as e:
                logger.error(f"Error: {e}")
                print(f"Error: {e}")
    
    def _show_help(self):
        """Show help information"""
        help_text = """
Available Commands:
-------------------
help                    - Show this help message
quit/exit               - Exit the program
screenshot              - Take a screenshot
click <x>,<y>          - Click at coordinates
type <text>            - Type text
find <query>           - Find element on screen
analyze                - Analyze current screen
task <description>     - Execute a task
record start/stop      - Start/stop recording session
history                - Show action history

Examples:
---------
click 500,300          - Click at position (500, 300)
type Hello World       - Type "Hello World"
find Submit button     - Find "Submit button" on screen
task Open calculator   - Execute task to open calculator
        """
        print(help_text)
    
    def _take_screenshot(self):
        """Take and save a screenshot"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"screenshot_{timestamp}.png"
        
        img = self.agent.capture_screenshot()
        if img:
            img.save(path)
            print(f"Screenshot saved to {path}")
        else:
            print("Failed to take screenshot")
    
    def _click(self, x: int, y: int):
        """Click at coordinates"""
        from core.base import Action
        action = Action(
            type=ActionType.CLICK,
            parameters={"x": x, "y": y}
        )
        result = self.agent.execute_action(action)
        
        if result.success:
            print(f"Clicked at ({x}, {y})")
        else:
            print(f"Click failed: {result.error}")
    
    def _type_text(self, text: str):
        """Type text"""
        from core.base import Action
        action = Action(
            type=ActionType.TYPE,
            parameters={"text": text}
        )
        result = self.agent.execute_action(action)
        
        if result.success:
            print(f"Typed: {text}")
        else:
            print(f"Typing failed: {result.error}")
    
    def _find_element(self, query: str):
        """Find element on screen"""
        result = self.agent.find_element(query)
        
        if result and result.get('found'):
            print(f"Found element: {result}")
        else:
            print(f"Element not found: {query}")
    
    def _analyze_screen(self):
        """Analyze current screen"""
        print("Analyzing screen...")
        analysis = self.agent.analyze_screen()
        
        print(f"Found {len(analysis.get('elements', []))} elements")
        for elem in analysis.get('elements', [])[:5]:  # Show first 5
            print(f"  - {elem['type']} at ({elem['x']}, {elem['y']})")
        
        if 'claude_analysis' in analysis:
            print(f"Claude Analysis: {analysis['claude_analysis']}")
    
    def _execute_task(self, task: str):
        """Execute a task"""
        print(f"Executing task: {task}")
        results = self.agent.execute_task(task)
        
        for i, result in enumerate(results):
            if result.success:
                print(f"  Step {i+1}: Success")
            else:
                print(f"  Step {i+1}: Failed - {result.error}")
    
    def _show_history(self):
        """Show action history"""
        history = self.agent.get_history()
        
        if not history:
            print("No actions in history")
            return
        
        print(f"\nAction History ({len(history)} actions):")
        print("-" * 50)
        
        for i, (action, result) in enumerate(history[-10:]):  # Show last 10
            status = "✓" if result.success else "✗"
            print(f"{i+1}. [{status}] {action.type.value}: {action.parameters}")
            if not result.success and result.error:
                print(f"     Error: {result.error}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Computer Use Agent - Claude Code')
    parser.add_argument('--task', type=str, help='Execute a specific task')
    parser.add_argument('--screenshot', action='store_true', help='Take a screenshot')
    parser.add_argument('--config', type=str, help='Path to config file')
    parser.add_argument('--replay', type=str, help='Replay a session file')
    
    args = parser.parse_args()
    
    cli = ComputerUseAgentCLI()
    
    if args.task:
        # Execute specific task
        print(f"Executing task: {args.task}")
        results = cli.agent.execute_task(args.task)
        for i, result in enumerate(results):
            print(f"Step {i+1}: {'Success' if result.success else 'Failed'}")
            
    elif args.screenshot:
        # Take screenshot
        cli._take_screenshot()
        
    elif args.replay:
        # Replay session
        print(f"Replaying session: {args.replay}")
        results = cli.agent.replay_session(args.replay)
        print(f"Replayed {len(results)} actions")
        
    else:
        # Run interactive mode
        cli.run_interactive()


if __name__ == "__main__":
    main()
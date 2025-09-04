"""
Cafe24 Complete Content Claude Bridge 
Claude Code AI    
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime

# CUA-MASTER  
sys.path.insert(0, r'C:\Users\8899y\CUA-MASTER')

from core.claude_code_bridge import ClaudeCodeBridge
from core.agent_enhanced import EnhancedComputerUseAgent

class Cafe24BridgeIntegration:
    """Cafe24  Claude Bridge """
    
    def __init__(self):
        self.bridge = ClaudeCodeBridge()
        self.agent = EnhancedComputerUseAgent()
        self.cafe24_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content")
        
    def request_html_download_plan(self, product_numbers):
        """HTML    """
        
        # Claude Code  
        request = {
            "task": "Cafe24 HTML  ",
            "context": {
                "product_numbers": product_numbers,
                "path": str(self.cafe24_path),
                "requirements": [
                    "1.  ",
                    "2.  HTML ",
                    "3.    ",
                    "4. TXT  "
                ]
            }
        }
        
        print(" Claude Bridge    ...")
        actions = self.bridge.request_action_plan(
            task=request["task"],
            context=request["context"]
        )
        
        if actions:
            print(f" {len(actions)}   ")
            return actions
        else:
            print(" Claude Bridge   ...")
            return self.fallback_html_download(product_numbers)
    
    def fallback_html_download(self, product_numbers):
        """:    """
        print("  html_downloader.py ")
        
        actions = [
            {
                "type": "execute",
                "parameters": {
                    "command": f"python {self.cafe24_path}/scripts/html_downloader.py"
                },
                "description": "HTML  "
            }
        ]
        return actions
    
    def request_txt_validation(self):
        """TXT    """
        
        request = {
            "task": "TXT      ",
            "context": {
                "txt_path": str(self.cafe24_path / "backup" / "txt_backup"),
                "validation_rules": [
                    " ",
                    "  ",
                    "HTML  ",
                    " "
                ]
            }
        }
        
        print(" TXT    ...")
        actions = self.bridge.request_action_plan(
            task=request["task"],
            context=request["context"]
        )
        
        return actions or self.fallback_txt_validation()
    
    def fallback_txt_validation(self):
        """:    """
        return [
            {
                "type": "execute",
                "parameters": {
                    "command": f"python {self.cafe24_path}/scripts/validate_temp_txt_files.py"
                },
                "description": "TXT  "
            },
            {
                "type": "execute",
                "parameters": {
                    "command": f"python {self.cafe24_path}/scripts/auto_fix_txt_files.py"
                },
                "description": "TXT  "
            }
        ]
    
    def request_brand_classification(self):
        """  """
        
        request = {
            "task": "   ",
            "context": {
                "html_path": str(self.cafe24_path / "html"),
                "brands": ["", "", ""],
                "classification_method": "product_name_analysis"
            }
        }
        
        print("    ...")
        actions = self.bridge.request_action_plan(
            task=request["task"],
            context=request["context"]
        )
        
        return actions or [
            {
                "type": "execute",
                "parameters": {
                    "command": f"python {self.cafe24_path}/scripts/classify_by_brand_name.py"
                },
                "description": "  "
            }
        ]
    
    def execute_workflow(self, workflow_type="full"):
        """  """
        
        workflows = {
            "full": [
                "html_download",
                "txt_validation", 
                "brand_classification"
            ],
            "download": ["html_download"],
            "validate": ["txt_validation"],
            "classify": ["brand_classification"]
        }
        
        selected_workflow = workflows.get(workflow_type, workflows["full"])
        
        print(f"\n{'='*60}")
        print(f"Cafe24 Bridge Integration - {workflow_type.upper()} Workflow")
        print(f"{'='*60}\n")
        
        for step in selected_workflow:
            print(f"\n  : {step}")
            
            if step == "html_download":
                #   
                product_numbers = ["P00000NB", "P00000NC", "P00000ND"]
                actions = self.request_html_download_plan(product_numbers)
                
            elif step == "txt_validation":
                actions = self.request_txt_validation()
                
            elif step == "brand_classification":
                actions = self.request_brand_classification()
            
            #  
            if actions:
                for action in actions:
                    print(f"  → {action.get('description', 'Action')}")
                    result = self.agent.execute_action_from_dict(action)
                    
                    #  
                    if result:
                        self.bridge.send_feedback(
                            action_id=f"{step}_{int(time.time())}",
                            result={"success": True, "step": step}
                        )
            
            time.sleep(1)
        
        print(f"\n {workflow_type.upper()}  !")
    
    def interactive_menu(self):
        """ """
        
        while True:
            print("\n" + "="*60)
            print("Cafe24 + Claude Bridge  ")
            print("="*60)
            print("\n1.  HTML  (AI )")
            print("2.  TXT    (AI )")
            print("3.    (AI )")
            print("4.    ")
            print("5.     (menu.py)")
            print("0. ")
            print("\n" + "-"*60)
            
            choice = input("\n: ").strip()
            
            if choice == "1":
                product_input = input("   ( ): ")
                products = [p.strip() for p in product_input.split(",")]
                actions = self.request_html_download_plan(products)
                self.execute_actions(actions)
                
            elif choice == "2":
                actions = self.request_txt_validation()
                self.execute_actions(actions)
                
            elif choice == "3":
                actions = self.request_brand_classification()
                self.execute_actions(actions)
                
            elif choice == "4":
                workflow_type = input("  (full/download/validate/classify): ")
                self.execute_workflow(workflow_type)
                
            elif choice == "5":
                import subprocess
                subprocess.run([sys.executable, str(self.cafe24_path / "menu.py")])
                
            elif choice == "0":
                print(" .")
                break
            
            else:
                print("  .")
    
    def execute_actions(self, actions):
        """  """
        if not actions:
            print("   .")
            return
        
        for i, action in enumerate(actions, 1):
            print(f"\n[{i}/{len(actions)}] {action.get('description', 'Action')}")
            result = self.agent.execute_action_from_dict(action)
            
            if result:
                print(f"   ")
            else:
                print(f"   ")
            
            time.sleep(0.5)


def main():
    """ """
    integration = Cafe24BridgeIntegration()
    
    #  
    import sys
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "download":
            actions = integration.request_html_download_plan(["P00000NB"])
            integration.execute_actions(actions)
            
        elif command == "validate":
            actions = integration.request_txt_validation()
            integration.execute_actions(actions)
            
        elif command == "classify":
            actions = integration.request_brand_classification()
            integration.execute_actions(actions)
            
        elif command == "workflow":
            workflow_type = sys.argv[2] if len(sys.argv) > 2 else "full"
            integration.execute_workflow(workflow_type)
            
        else:
            print(f"Unknown command: {command}")
            print("Usage: python cafe24_bridge_integration.py [download|validate|classify|workflow|menu]")
    else:
        #  
        integration.interactive_menu()


if __name__ == "__main__":
    main()
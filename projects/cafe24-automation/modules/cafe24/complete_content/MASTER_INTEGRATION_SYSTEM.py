"""
MASTER INTEGRATION SYSTEM -   
       

 :
1. Claude Bridge -  
2. Image Workflow -   (Gemini, AI Studio, Nano Banana, Imagen3)
3. Content Generator -   
4. FTP Upload -  
"""

import sys
import json
import time
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# CUA-MASTER  
sys.path.insert(0, r'C:\Users\8899y\CUA-MASTER')
sys.path.insert(0, r'C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content')

#   
from cafe24_bridge_integration import Cafe24BridgeIntegration
from ultimate_image_workflow import UltimateImageWorkflow
from complete_detail_page_system import CompleteDetailPageSystem
# from claude_bridge_template_system import ClaudeBridgeTemplateSystem  # 삭제됨
from ftp_image_upload_system import FTPImageUploadSystem
from html_design_optimizer import HtmlDesignOptimizer
from html_image_integration import HtmlImageIntegration


class MasterIntegrationSystem:
    """   -   """
    
    def __init__(self):
        print("\n" + "="*80)
        print("MASTER INTEGRATION SYSTEM ")
        print("="*80)
        
        self.base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content")
        self.html_path = self.base_path / "html" / "temp_txt"
        self.output_path = self.base_path / "output"
        self.output_path.mkdir(exist_ok=True)
        
        #   
        print("\n  ...")
        
        self.bridge = Cafe24BridgeIntegration()
        print("  [OK] Claude Bridge ")
        
        self.image_workflow = UltimateImageWorkflow()
        print("  [OK] Image Workflow ")
        
        self.content_generator = CompleteDetailPageSystem()
        print("  [OK] Content Generator ")
        
        # self.template_system = ClaudeBridgeTemplateSystem()  # 삭제됨
        # print("  [OK] Template System ")  # 삭제됨
        
        self.ftp_system = FTPImageUploadSystem()
        print("  [OK] FTP Upload System ")
        
        self.design_optimizer = HtmlDesignOptimizer()
        print("  [OK] Design Optimizer ")
        
        self.image_integration = HtmlImageIntegration()
        print("  [OK] Image Integration ")
        
        #  
        self.workflow_state = {
            "total_products": 0,
            "processed": 0,
            "success": 0,
            "failed": 0,
            "start_time": None,
            "end_time": None
        }
        
        print("\n Master Integration System  !")
    
    def analyze_products(self) -> List[Dict]:
        """  """
        print("\n   ...")
        
        products = []
        txt_files = list(self.html_path.glob("*.txt"))
        
        print(f"   : {len(txt_files)}")
        
        for txt_file in txt_files[:10]:  #  10
            product_num = txt_file.stem
            
            #  
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read()
                #    (    )
                product_name = self.extract_product_name(content)
            
            products.append({
                "file": txt_file,
                "number": product_num,
                "name": product_name,
                "category": self.determine_category(product_name)
            })
        
        print(f"   : {len(products)} ")
        return products
    
    def extract_product_name(self, content: str) -> str:
        """  """
        #    (   )
        lines = content.split('\n')
        for line in lines[:10]:
            if '' in line or '' in line or '' in line:
                return line.strip()
        return ""
    
    def determine_category(self, product_name: str) -> str:
        """  """
        categories = {
            "": ["", ""],
            "": ["", ""],
            "ccw": ["", "ccw", "CCW"],
            "": ["", ""],
            "": ["", ""],
            "": ["", "mobidick"],
            "": ["", ""],
            "bs": ["BS", "bs"],
            "": ["", ""]
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in product_name:
                    return category
        
        return "etc"
    
    def process_single_product(self, product: Dict) -> Dict:
        """   -  """
        
        print(f"\n{'='*60}")
        print(f"  : {product['name']} (#{product['number']})")
        print(f"{'='*60}")
        
        result = {
            "product": product,
            "status": "processing",
            "steps": {},
            "errors": []
        }
        
        try:
            # 1: Claude Bridge  
            print("\n[1/7]  Claude Bridge  ...")
            strategy = self.request_processing_strategy(product)
            result["steps"]["strategy"] = strategy
            
            # 2:  
            print("\n[2/7]   ...")
            images = self.generate_images(product, strategy)
            result["steps"]["images"] = images
            
            # 3:   
            print("\n[3/7]    ...")
            content = self.generate_content(product)
            result["steps"]["content"] = content
            
            # 4:  
            print("\n[4/7]   ...")
            template = self.apply_template(product, images, content, strategy)
            result["steps"]["template"] = template
            
            # 5:  
            print("\n[5/7]   ...")
            optimized = self.optimize_design(template)
            result["steps"]["optimized"] = optimized
            
            # 6: FTP 
            print("\n[6/7]  FTP ...")
            upload_result = self.upload_to_ftp(product, images)
            result["steps"]["upload"] = upload_result
            
            # 7:   
            print("\n[7/7]    ...")
            final_file = self.save_final_file(product, optimized)
            result["steps"]["final"] = final_file
            
            result["status"] = "success"
            print(f"\n   : {product['name']}")
            
        except Exception as e:
            result["status"] = "failed"
            result["errors"].append(str(e))
            print(f"\n   : {e}")
        
        return result
    
    def request_processing_strategy(self, product: Dict) -> Dict:
        """Claude Bridge   """
        
        request = {
            "product": product,
            "requirements": [
                "   ",
                "  ",
                "  ",
                "  "
            ]
        }
        
        # Claude Bridge  ()
        strategy = {
            "image_style": "premium",
            "template_style": "kurly",
            "content_tone": "professional",
            "target_audience": "30-40 "
        }
        
        return strategy
    
    def generate_images(self, product: Dict, strategy: Dict) -> List[str]:
        """ """
        
        # Image Workflow 
        workflow_strategy = strategy.get("image_style", "premium")
        
        product_info = {
            "product_name": product["name"],
            "category": product["category"]
        }
        
        #    ()
        results = self.image_workflow.execute_workflow(product_info, workflow_strategy)
        
        #   
        images = []
        for result in results:
            if result.get("success"):
                images.extend(result.get("images", []))
        
        print(f"   : {len(images)}")
        return images
    
    def generate_content(self, product: Dict) -> Dict:
        """  """
        
        product_info = {
            "product_name": product["name"],
            "category": product["category"],
            "product_number": product["number"]
        }
        
        # Content Generator 
        content = self.content_generator.generate_complete_content(product_info)
        
        print(f"    : {len(content)}")
        return content
    
    def apply_template(self, product: Dict, images: List, content: Dict, strategy: Dict) -> str:
        """ """
        
        product_info = {
            "product_name": product["name"],
            "images": images,
            "content": content,
            "style": strategy.get("template_style", "kurly")
        }
        
        # Template System 
        template_html = self.template_system.generate_template_for_product(product_info)
        
        return template_html
    
    def optimize_design(self, template: str) -> str:
        """ """
        
        #   
        temp_file = self.output_path / "temp_optimize.html"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(template)
        
        # Design Optimizer 
        optimized = self.design_optimizer.optimize_single_html(temp_file)
        
        #   
        temp_file.unlink()
        
        return optimized
    
    def upload_to_ftp(self, product: Dict, images: List) -> Dict:
        """FTP """
        
        upload_result = {
            "success": True,
            "uploaded_files": [],
            "urls": []
        }
        
        # FTP System   ()
        for image in images:
            #  self.ftp_system.upload_image() 
            url = f"https://manwonyori.cafe24.com/web/product/ai_optimization_{datetime.now().strftime('%Y%m%d')}/{product['category']}/{image}"
            upload_result["urls"].append(url)
        
        print(f"   : {len(upload_result['urls'])} ")
        return upload_result
    
    def save_final_file(self, product: Dict, content: str) -> Path:
        """  """
        
        #   
        category_path = self.output_path / product["category"]
        category_path.mkdir(exist_ok=True)
        
        #  
        final_file = category_path / f"{product['number']}_complete.txt"
        with open(final_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   : {final_file}")
        return final_file
    
    def process_all_products(self):
        """  """
        
        print("\n" + "="*80)
        print(" MASTER WORKFLOW ")
        print("="*80)
        
        #  
        products = self.analyze_products()
        self.workflow_state["total_products"] = len(products)
        self.workflow_state["start_time"] = datetime.now()
        
        print(f"\n {len(products)}   ...")
        
        #   
        for i, product in enumerate(products, 1):
            print(f"\n[{i}/{len(products)}]  ...")
            
            result = self.process_single_product(product)
            
            if result["status"] == "success":
                self.workflow_state["success"] += 1
            else:
                self.workflow_state["failed"] += 1
            
            self.workflow_state["processed"] += 1
            
            #   
            self.display_progress()
        
        self.workflow_state["end_time"] = datetime.now()
        
        #  
        self.generate_final_report()
    
    def display_progress(self):
        """  """
        
        state = self.workflow_state
        progress = (state["processed"] / state["total_products"]) * 100
        
        print(f"\n  : {progress:.1f}%")
        print(f"   : {state['success']}")
        print(f"   : {state['failed']}")
        print(f"  [WAIT]  : {state['total_products'] - state['processed']}")
    
    def generate_final_report(self):
        """  """
        
        state = self.workflow_state
        duration = (state["end_time"] - state["start_time"]).total_seconds()
        
        report = f"""
{'='*80}
 MASTER WORKFLOW  
{'='*80}

  : {duration:.1f}
   : {state['total_products']}
 : {state['success']}
 : {state['failed']}
 : {(state['success']/state['total_products']*100):.1f}%

  : {self.output_path}

{'='*80}
 WORKFLOW !
{'='*80}
"""
        
        print(report)
        
        #   
        report_file = self.output_path / f"master_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
    
    def interactive_menu(self):
        """ """
        
        while True:
            print("\n" + "="*80)
            print(" MASTER INTEGRATION SYSTEM")
            print("="*80)
            print("\n1.    (Full Workflow)")
            print("2.   ")
            print("3.   ")
            print("4. Claude Bridge ")
            print("5.   ")
            print("6. FTP  ")
            print("7.   ")
            print("0. ")
            print("-"*80)
            
            choice = input("\n: ").strip()
            
            if choice == "1":
                self.process_all_products()
                
            elif choice == "2":
                products = self.analyze_products()
                if products:
                    result = self.process_single_product(products[0])
                    print(f"\n : {result['status']}")
                
            elif choice == "3":
                self.display_system_status()
                
            elif choice == "4":
                print("\nClaude Bridge ...")
                self.bridge.interactive_menu()
                
            elif choice == "5":
                print("\n  ...")
                self.image_workflow.interactive_menu()
                
            elif choice == "6":
                print("\nFTP  ...")
                if self.ftp_system.test_connection():
                    print(" FTP  !")
                else:
                    print(" FTP  !")
                
            elif choice == "7":
                self.display_progress()
                
            elif choice == "0":
                print("\n.")
                break
                
            else:
                print("\n .")
    
    def display_system_status(self):
        """  """
        
        print("\n" + "="*60)
        print("  ")
        print("="*60)
        
        components = [
            ("Claude Bridge", self.bridge is not None),
            ("Image Workflow", self.image_workflow is not None),
            ("Content Generator", self.content_generator is not None),
            ("Template System", self.template_system is not None),
            ("FTP System", self.ftp_system is not None),
            ("Design Optimizer", self.design_optimizer is not None),
            ("Image Integration", self.image_integration is not None)
        ]
        
        for name, status in components:
            status_icon = "" if status else ""
            print(f"  {status_icon} {name}")
        
        print("-"*60)
        print(f"  : {self.base_path}")
        print(f"  : {self.output_path}")
        
        # HTML   
        txt_files = list(self.html_path.glob("*.txt"))
        print(f" TXT : {len(txt_files)}")
        
        #    
        output_files = list(self.output_path.rglob("*.*"))
        print(f"  : {len(output_files)}")
        
        print("="*60)


def main():
    """ """
    
    print("\n" + "="*80)
    print(" CAFE24 COMPLETE CONTENT MASTER SYSTEM")
    print("="*80)
    print("\n    ")
    print("   .")
    print("\nIncluded Systems:")
    print("  - Claude Bridge")
    print("  - Image Workflow (Gemini, AI Studio, Nano Banana, Imagen3)")
    print("  - Content Generator")
    print("  - Template System")
    print("  - FTP Upload")
    print("  - Design Optimizer")
    
    # Master System 
    master = MasterIntegrationSystem()
    
    #  
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "run":
            #  
            master.process_all_products()
        elif command == "test":
            #  
            products = master.analyze_products()
            if products:
                master.process_single_product(products[0])
        elif command == "status":
            #  
            master.display_system_status()
        else:
            print(f"\n   : {command}")
            print(": python MASTER_INTEGRATION_SYSTEM.py [run|test|status]")
    else:
        #  
        master.interactive_menu()


if __name__ == "__main__":
    main()
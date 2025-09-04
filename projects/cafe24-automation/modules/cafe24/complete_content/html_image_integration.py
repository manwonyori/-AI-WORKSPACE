"""
Cafe24 HTML + AI Image Studio   
    AI   
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime
import time

# CUA-MASTER  
sys.path.insert(0, r'C:\Users\8899y\CUA-MASTER')
sys.path.insert(0, r'C:\Users\8899y\CUA-MASTER\modules\ai-image-studio')
sys.path.insert(0, r'C:\Users\8899y\CUA-MASTER\modules\nano_banana')

from core.claude_code_bridge import ClaudeCodeBridge
from ai_studio_cli import AIStudioCLI
from imagen3_photorealistic_engine import Imagen3PhotorealisticEngine
from nano_banana_system import NanoBananaImageSystem

class HtmlImageIntegration:
    """HTML AI    """
    
    def __init__(self):
        self.bridge = ClaudeCodeBridge()
        self.ai_studio = AIStudioCLI()
        self.imagen3 = Imagen3PhotorealisticEngine()
        self.nano_banana = NanoBananaImageSystem()
        
        self.base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content")
        self.html_path = self.base_path / "html" / "temp_txt"
        self.output_path = self.base_path / "optimized_with_ai_images"
        self.output_path.mkdir(exist_ok=True)
        
        print("    ")
        print(f"  - AI Studio: ")
        print(f"  - Imagen3 Engine: ")
        print(f"  - Nano Banana: ")
    
    def extract_images_from_html(self, html_file):
        """HTML   """
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        #   
        img_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'
        images = re.findall(img_pattern, content)
        
        #   
        title_pattern = r'<title>([^<]+)</title>'
        title_match = re.search(title_pattern, content)
        product_name = title_match.group(1) if title_match else ""
        
        return {
            "file": html_file.name,
            "product_name": product_name,
            "images": images,
            "content": content
        }
    
    def generate_ai_images(self, product_info):
        """   AI  """
        product_name = product_info["product_name"]
        
        print(f"\n AI  : {product_name}")
        
        # 1.    
        main_prompt = self.create_product_prompt(product_name, "main")
        
        # 2. Imagen3   
        imagen3_result = self.imagen3.generate_photorealistic({
            "prompt": main_prompt,
            "style": "product_showcase",
            "resolution": "1920x1080"
        })
        
        # 3. Nano Banana   
        variations = self.nano_banana.generate_variations(
            base_prompt=main_prompt,
            variations=4
        )
        
        # 4. AI Studio  
        thumbnails = []
        for i in range(3):
            thumb_prompt = self.create_product_prompt(product_name, f"thumbnail_{i+1}")
            thumbnail = self.ai_studio.generate_single_image(
                prompt=thumb_prompt,
                size="400x400"
            )
            thumbnails.append(thumbnail)
        
        return {
            "main_image": imagen3_result,
            "variations": variations,
            "thumbnails": thumbnails
        }
    
    def create_product_prompt(self, product_name, image_type="main"):
        """  """
        
        #   
        templates = {
            "main": f"""
                Professional product photography of {product_name},
                clean white background, studio lighting,
                8K resolution, ultra-detailed, photorealistic,
                shot with Canon EOS R5, 85mm lens,
                perfect composition, award-winning quality
            """,
            "thumbnail": f"""
                {product_name} close-up detail shot,
                macro photography, sharp focus,
                product showcase, clean background
            """,
            "lifestyle": f"""
                {product_name} in real-life setting,
                lifestyle photography, natural lighting,
                Korean home kitchen environment,
                warm and inviting atmosphere
            """
        }
        
        #    
        if "thumbnail" in image_type:
            return templates["thumbnail"]
        elif image_type == "lifestyle":
            return templates["lifestyle"]
        else:
            return templates["main"]
    
    def optimize_html_with_ai_images(self, html_info, ai_images):
        """AI   HTML """
        
        content = html_info["content"]
        
        #    AI  
        if ai_images.get("main_image"):
            #     AI  
            content = re.sub(
                r'<img([^>]+)src="[^"]+"([^>]*)>',
                f'<img\\1src="{ai_images["main_image"]}"\\2>',
                content,
                count=1
            )
        
        #    
        styled_content = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html_info["product_name"]} - AI </title>
    <style>
        .ai-optimized-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            font-family: 'Noto Sans KR', sans-serif;
        }}
        
        .ai-image-gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }}
        
        .ai-image {{
            width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}
        
        .ai-image:hover {{
            transform: scale(1.02);
        }}
        
        .product-info {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin: 30px 0;
        }}
        
        .ai-badge {{
            display: inline-block;
            background: #ff6b6b;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <div class="ai-optimized-container">
        <div class="ai-badge">AI  </div>
        <h1>{html_info["product_name"]}</h1>
        
        <div class="ai-image-gallery">
            <!-- AI     -->
            {self.create_image_gallery(ai_images)}
        </div>
        
        <div class="product-info">
            {content}
        </div>
    </div>
</body>
</html>
        """
        
        return styled_content
    
    def create_image_gallery(self, ai_images):
        """AI   HTML """
        gallery_html = ""
        
        #  
        if ai_images.get("main_image"):
            gallery_html += f'<img src="{ai_images["main_image"]}" class="ai-image" alt=" ">\n'
        
        #  
        if ai_images.get("variations"):
            for i, var in enumerate(ai_images["variations"]):
                if var.get("image_path"):
                    gallery_html += f'<img src="{var["image_path"]}" class="ai-image" alt=" {i+1}">\n'
        
        # 
        if ai_images.get("thumbnails"):
            for i, thumb in enumerate(ai_images["thumbnails"]):
                if thumb:
                    gallery_html += f'<img src="{thumb}" class="ai-image" alt=" {i+1}">\n'
        
        return gallery_html
    
    def process_all_html_files(self):
        """ HTML  """
        
        html_files = list(self.html_path.glob("*.txt"))
        total = len(html_files)
        
        print(f"\n{'='*60}")
        print(f" HTML + AI    ")
        print(f"   {total} ")
        print(f"{'='*60}\n")
        
        # Claude Bridge   
        request = {
            "task": "HTML  AI  ",
            "total_files": total,
            "systems": ["AI Studio", "Imagen3", "Nano Banana"]
        }
        
        actions = self.bridge.request_action_plan(
            task="Cafe24 HTML AI  ",
            context=request
        )
        
        #   3  
        for i, html_file in enumerate(html_files[:3], 1):
            print(f"\n[{i}/3]  : {html_file.name}")
            
            # 1. HTML 
            html_info = self.extract_images_from_html(html_file)
            print(f"  - : {html_info['product_name']}")
            print(f"  -  : {len(html_info['images'])}")
            
            # 2. AI  
            ai_images = self.generate_ai_images(html_info)
            
            # 3. HTML 
            optimized_html = self.optimize_html_with_ai_images(html_info, ai_images)
            
            # 4. 
            output_file = self.output_path / f"ai_optimized_{html_file.name.replace('.txt', '.html')}"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(optimized_html)
            
            print(f"    : {output_file.name}")
            
            #  
            self.bridge.send_feedback(
                action_id=f"image_integration_{int(time.time())}",
                result={
                    "file": html_file.name,
                    "success": True,
                    "ai_images_generated": len(ai_images)
                }
            )
        
        print(f"\n{'='*60}")
        print(f"  !")
        print(f"   : {self.output_path}")
        print(f"{'='*60}")
    
    def interactive_menu(self):
        """ """
        
        while True:
            print("\n" + "="*60)
            print(" Cafe24 HTML + AI   ")
            print("="*60)
            print("\n1.  HTML  AI  ")
            print("2.   ")
            print("3. AI  ")
            print("4.   ")
            print("0. ")
            print("-"*60)
            
            choice = input("\n: ").strip()
            
            if choice == "1":
                self.process_all_html_files()
                
            elif choice == "2":
                files = list(self.html_path.glob("*.txt"))
                if files:
                    test_file = files[0]
                    print(f"\n : {test_file.name}")
                    html_info = self.extract_images_from_html(test_file)
                    ai_images = self.generate_ai_images(html_info)
                    optimized = self.optimize_html_with_ai_images(html_info, ai_images)
                    print("  ")
                
            elif choice == "3":
                product_name = input(" : ")
                if product_name:
                    ai_images = self.generate_ai_images({"product_name": product_name})
                    print(f" AI   : {len(ai_images)}")
                
            elif choice == "4":
                print("\n :")
                print(f"  - AI Studio:  ")
                print(f"  - Imagen3:  ")
                print(f"  - Nano Banana:  ")
                print(f"  - HTML : {len(list(self.html_path.glob('*.txt')))}")
                
            elif choice == "0":
                print(".")
                break
            
            else:
                print(" .")


def main():
    """ """
    integration = HtmlImageIntegration()
    
    #   
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "process":
            integration.process_all_html_files()
        elif command == "test":
            #  
            files = list(integration.html_path.glob("*.txt"))
            if files:
                html_info = integration.extract_images_from_html(files[0])
                print(f" : {html_info['product_name']}")
        else:
            print(f"Unknown command: {command}")
    else:
        #  
        integration.interactive_menu()


if __name__ == "__main__":
    main()
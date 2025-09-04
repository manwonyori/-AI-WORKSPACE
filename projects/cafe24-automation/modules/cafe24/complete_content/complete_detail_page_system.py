"""
   
 +    
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# CUA-MASTER  
sys.path.insert(0, r'C:\Users\8899y\CUA-MASTER')

from core.claude_code_bridge import ClaudeCodeBridge

class CompleteDetailPageSystem:
    """    """
    
    def __init__(self):
        self.bridge = ClaudeCodeBridge()
        self.base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content")
        
        #   
        self.page_components = {
            "header": ",  ",
            "images": " ,  ",
            "price_info": ", , ",
            "product_info": ", , ",
            "detail_content": "  ",
            "nutrition": " ",
            "recipe": ", ",
            "certification": "",
            "notice": "",
            "delivery": "",
            "refund": "/ "
        }
        
        print("    ")
    
    def analyze_current_content(self, txt_file):
        """ TXT   """
        
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        analysis = {
            "has_title": bool(re.search(r'<title>', content)),
            "has_price": bool(re.search(r'\d+,?\d*\s*', content)),
            "has_images": bool(re.search(r'<img', content)),
            "has_description": len(content) > 1000,
            "missing_components": []
        }
        
        #   
        if not analysis["has_price"]:
            analysis["missing_components"].append("price_info")
        if len(content) < 2000:
            analysis["missing_components"].extend(["detail_content", "recipe", "nutrition"])
        
        return analysis
    
    def generate_complete_content(self, product_info):
        """   """
        
        print(f"\n   : {product_info['product_name']}")
        
        # Claude Bridge   
        content_request = {
            "task": "   ",
            "product": product_info,
            "requirements": [
                "1. SEO   ",
                "2.   ",
                "3.  ",
                "4.    ",
                "5.  "
            ],
            "tone": "  "
        }
        
        # Claude Bridge 
        actions = self.bridge.request_action_plan(
            task="  ",
            context=content_request
        )
        
        #   (Claude   )
        if actions:
            return self.parse_content_from_claude(actions, product_info)
        else:
            return self.generate_default_content(product_info)
    
    def generate_default_content(self, product_info):
        """   ()"""
        
        content_sections = {}
        
        # 1.  
        content_sections["header"] = f"""
        <h1>{product_info['product_name']}</h1>
        <p class="subtitle">{self.generate_subtitle(product_info)}</p>
        """
        
        # 2.  
        content_sections["description"] = self.generate_description(product_info)
        
        # 3.   
        content_sections["product_info"] = self.generate_info_table(product_info)
        
        # 4. 
        content_sections["nutrition"] = self.generate_nutrition_table(product_info)
        
        # 5. 
        content_sections["recipe"] = self.generate_recipe(product_info)
        
        # 6.  
        content_sections["brand_story"] = self.generate_brand_story(product_info)
        
        # 7.  
        content_sections["purchase_guide"] = self.generate_purchase_guide()
        
        return content_sections
    
    def generate_subtitle(self, product_info):
        """ """
        
        subtitles = {
            "manwon": " ,  ",
            "insaeng": "   ",
            "ccw": "   ",
            "banchan": "  , ",
            "choi": "    "
        }
        
        category = product_info.get('category', 'etc')
        return subtitles.get(category, "   ")
    
    def generate_description(self, product_info):
        """   """
        
        name = product_info['product_name']
        category = product_info.get('category', '')
        
        description = f"""
        <div class="product-description">
            <h2> {name}?</h2>
            
            <h3>   </h3>
            <p>
            {name}()     .
                   .
            HACCP        .
            </p>
            
            <h3>   </h3>
            <ul>
                <li>     </li>
                <li>       </li>
                <li>        </li>
                <li>     </li>
            </ul>
            
            <h3>  </h3>
            <p>
            30     ,
                  .
                  ,
                    .
            </p>
        </div>
        """
        
        return description
    
    def generate_info_table(self, product_info):
        """   """
        
        return f"""
        <table class="product-info-table">
            <tr>
                <th></th>
                <td>{product_info['product_name']}</td>
            </tr>
            <tr>
                <th></th>
                <td>{product_info.get('weight', '1kg ( 20)')}</td>
            </tr>
            <tr>
                <th></th>
                <td>{product_info.get('ingredients', '   ')}</td>
            </tr>
            <tr>
                <th></th>
                <td>{product_info.get('origin', '')}</td>
            </tr>
            <tr>
                <th></th>
                <td>{product_info.get('storage', ' (-18℃ )')}</td>
            </tr>
            <tr>
                <th></th>
                <td>{product_info.get('expiry', ' 12')}</td>
            </tr>
        </table>
        """
    
    def generate_nutrition_table(self, product_info):
        """  """
        
        return """
        <div class="nutrition-info">
            <h3></h3>
            <table>
                <tr>
                    <th></th>
                    <th>100g</th>
                    <th>1 </th>
                </tr>
                <tr>
                    <td></td>
                    <td>230kcal</td>
                    <td>345kcal</td>
                </tr>
                <tr>
                    <td></td>
                    <td>28g</td>
                    <td>42g</td>
                </tr>
                <tr>
                    <td></td>
                    <td>12g</td>
                    <td>18g</td>
                </tr>
                <tr>
                    <td></td>
                    <td>8g</td>
                    <td>12g</td>
                </tr>
                <tr>
                    <td></td>
                    <td>450mg</td>
                    <td>675mg</td>
                </tr>
            </table>
            <p class="nutrition-note">
                * 1 : 150g <br>
                *        
            </p>
        </div>
        """
    
    def generate_recipe(self, product_info):
        """ """
        
        category = product_info.get('category', '')
        
        if '' in product_info['product_name']:
            recipe = """
            <div class="recipe-section">
                <h3>   </h3>
                
                <div class="recipe-method">
                    <h4>  ()</h4>
                    <ol>
                        <li>   </li>
                        <li>    12-15 </li>
                        <li>!    </li>
                    </ol>
                </div>
                
                <div class="recipe-method">
                    <h4> </h4>
                    <ol>
                        <li>    </li>
                        <li>     </li>
                        <li> 1/3    5 </li>
                        <li>   !</li>
                    </ol>
                </div>
                
                <div class="recipe-tip">
                    <h4>  TIP</h4>
                    <ul>
                        <li>   </li>
                        <li>: 180℃ 15</li>
                        <li>:    3-4</li>
                    </ul>
                </div>
            </div>
            """
        else:
            recipe = """
            <div class="recipe-section">
                <h3> </h3>
                <ol>
                    <li>    </li>
                    <li>   </li>
                    <li>    </li>
                </ol>
            </div>
            """
        
        return recipe
    
    def generate_brand_story(self, product_info):
        """  """
        
        stories = {
            "manwon": """
            <div class="brand-story">
                <h3> </h3>
                <p>
                "   "<br><br>
                      
                     .
                      .
                </p>
            </div>
            """,
            "insaeng": """
            <div class="brand-story">
                <h3> </h3>
                <p>
                "   "<br><br>
                3      .
                      
                       .
                </p>
            </div>
            """
        }
        
        category = product_info.get('category', 'etc')
        return stories.get(category, "")
    
    def generate_purchase_guide(self):
        """  """
        
        return """
        <div class="purchase-guide">
            <h3>  </h3>
            <ul>
                <li>: 3,000 (3  )</li>
                <li>:   2-3 ( )</li>
                <li>    </li>
                <li>/:   </li>
            </ul>
            
            <h3> / </h3>
            <ul>
                <li>     </li>
                <li>   100% </li>
                <li>       </li>
                <li>: 1588-1234 ( 9:00-18:00)</li>
            </ul>
        </div>
        """
    
    def create_complete_detail_page(self, txt_file):
        """  """
        
        print(f"\n   : {txt_file.name}")
        
        # 1.   
        analysis = self.analyze_current_content(txt_file)
        print(f"   : {len(analysis['missing_components'])}  ")
        
        # 2.   
        with open(txt_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        product_info = self.extract_product_info(original_content, txt_file)
        
        # 3.   
        content_sections = self.generate_complete_content(product_info)
        
        # 4.   
        image_section = self.prepare_image_section(product_info)
        
        # 5.   
        final_page = self.assemble_final_page(
            content_sections,
            image_section,
            product_info
        )
        
        return final_page
    
    def extract_product_info(self, content, txt_file):
        """  """
        
        title_match = re.search(r'<title>([^<]+)</title>', content)
        product_name = title_match.group(1) if title_match else txt_file.stem
        
        category = self.get_category(product_name)
        
        return {
            "product_id": txt_file.stem,
            "product_name": product_name,
            "category": category,
            "original_content": content
        }
    
    def get_category(self, product_name):
        """ """
        categories = {
            '': 'manwon',
            '': 'insaeng',
            '': 'ccw',
            '': 'banchan',
            '': 'choi'
        }
        
        for brand, code in categories.items():
            if brand in product_name:
                return code
        return 'etc'
    
    def prepare_image_section(self, product_info):
        """  """
        
        # FTP   
        base_url = f"https://manwonyori.cafe24.com/web/product/ai_optimization_{datetime.now().strftime('%Y%m%d')}"
        category = product_info['category']
        product_id = product_info['product_id']
        
        return f"""
        <div class="image-gallery">
            <!--   -->
            <img src="{base_url}/{category}/main_{product_id}.jpg" 
                 alt="{product_info['product_name']}" class="main-image">
            
            <!--   -->
            <img src="{base_url}/{category}/detail1_{product_id}.jpg" class="detail-image">
            <img src="{base_url}/{category}/detail2_{product_id}.jpg" class="detail-image">
            <img src="{base_url}/{category}/detail3_{product_id}.jpg" class="detail-image">
            
            <!--   -->
            <img src="{base_url}/{category}/nutrition_{product_id}.jpg" class="nutrition-image">
        </div>
        """
    
    def assemble_final_page(self, content_sections, image_section, product_info):
        """  """
        
        #    
        final_html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{product_info['product_name']} - </title>
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .product-description {{ margin: 40px 0; }}
        .product-info-table {{ width: 100%; border-collapse: collapse; margin: 30px 0; }}
        .product-info-table th {{ background: #f5f5f5; padding: 15px; text-align: left; width: 30%; }}
        .product-info-table td {{ padding: 15px; border-bottom: 1px solid #eee; }}
        .nutrition-info table {{ width: 100%; margin: 20px 0; }}
        .recipe-section {{ background: #f9f9f9; padding: 30px; border-radius: 10px; margin: 40px 0; }}
        .brand-story {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; border-radius: 10px; margin: 40px 0; }}
        .purchase-guide {{ border: 2px solid #eee; padding: 30px; border-radius: 10px; margin: 40px 0; }}
        .image-gallery img {{ width: 100%; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        {content_sections.get('header', '')}
        
        {image_section}
        
        {content_sections.get('description', '')}
        
        {content_sections.get('product_info', '')}
        
        {content_sections.get('nutrition', '')}
        
        {content_sections.get('recipe', '')}
        
        {content_sections.get('brand_story', '')}
        
        {content_sections.get('purchase_guide', '')}
    </div>
</body>
</html>
        """
        
        return final_html
    
    def parse_content_from_claude(self, actions, product_info):
        """Claude  """
        # Claude   
        return self.generate_default_content(product_info)
    
    def process_all_files(self):
        """  """
        
        txt_files = list(Path(self.base_path / "html" / "temp_txt").glob("*.txt"))
        output_path = self.base_path / "complete_detail_pages"
        output_path.mkdir(exist_ok=True)
        
        print(f"\n{'='*60}")
        print(f"    ")
        print(f"   {len(txt_files)} ")
        print(f"{'='*60}")
        
        #  3 
        for i, txt_file in enumerate(txt_files[:3], 1):
            print(f"\n[{i}/3] {txt_file.name}")
            
            #   
            complete_page = self.create_complete_detail_page(txt_file)
            
            # 
            output_file = output_path / f"complete_{txt_file.stem}.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(complete_page)
            
            print(f"   : {output_file.name}")
            print(f"    - : 5 ")
            print(f"    - : 8 ")
            print(f"    -  : {len(complete_page):,} ")
        
        print(f"\n{'='*60}")
        print(f"   !")
        print(f"  : {output_path}")
        print(f"{'='*60}")


def main():
    system = CompleteDetailPageSystem()
    system.process_all_files()


if __name__ == "__main__":
    main()
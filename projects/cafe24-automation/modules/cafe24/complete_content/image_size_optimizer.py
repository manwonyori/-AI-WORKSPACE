"""
   
/      
"""

import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from PIL import Image
import requests
from io import BytesIO

class ImageSizeOptimizer:
    """     """
    
    def __init__(self):
        self.base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content")
        self.representative_path = self.base_path / "representative_images"
        self.representative_path.mkdir(exist_ok=True)
        
        #   
        self.image_sizes = {
            "representative": {
                "size": (1000, 1000),
                "quality": 95,
                "format": "JPEG",
                "folder": "representative_images",
                "naming": "{product_num}_{product_name}.jpg"
            },
            "desktop_main": {
                "size": (800, 800),
                "quality": 90,
                "format": "JPEG",
                "max_width": "800px"
            },
            "mobile_main": {
                "size": (500, 500),
                "quality": 85,
                "format": "JPEG",
                "max_width": "100%"
            },
            "thumbnail": {
                "size": (300, 300),
                "quality": 80,
                "format": "JPEG"
            },
            "detail": {
                "size": (600, None),  #  ,   
                "quality": 85,
                "format": "JPEG",
                "max_width": "600px"
            }
        }
        
        #  CSS 
        self.responsive_css = """
<style>
/*    */
.product-image-container {
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
}

.product-image {
    width: 100%;
    height: auto;
    display: block;
}

/*  */
@media (min-width: 768px) {
    .product-image-container {
        max-width: 800px;
    }
    
    .product-main-image {
        max-width: 800px;
        height: auto;
    }
    
    .product-detail-image {
        max-width: 600px;
        height: auto;
        margin: 20px auto;
    }
}

/*  */
@media (max-width: 767px) {
    .product-image-container {
        max-width: 100%;
        padding: 0 10px;
    }
    
    .product-main-image {
        width: 100%;
        height: auto;
    }
    
    .product-detail-image {
        width: 100%;
        height: auto;
        margin: 10px 0;
    }
}

/*   */
.representative-image {
    display: none; /*   */
}

/*    */
.lazy-load {
    loading: lazy;
}

/*   */
.image-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
    margin: 20px 0;
}

@media (max-width: 767px) {
    .image-gallery {
        grid-template-columns: 1fr;
    }
}
</style>
"""
    
    def create_representative_image(self, source_image_path: str, product_num: str, product_name: str) -> Path:
        """  (1000x1000)"""
        
        print(f"\n  : {product_num}_{product_name}")
        
        try:
            #  
            if source_image_path.startswith('http'):
                response = requests.get(source_image_path)
                img = Image.open(BytesIO(response.content))
            else:
                img = Image.open(source_image_path)
            
            # RGB  (JPEG  )
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # 1000x1000  
            img_square = self.make_square_image(img, 1000)
            
            #   ( )
            safe_name = "".join(c for c in product_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')[:30]  #  30
            
            filename = f"{product_num}_{safe_name}.jpg"
            output_path = self.representative_path / filename
            
            # 
            img_square.save(output_path, 'JPEG', quality=95, optimize=True)
            
            print(f"    : {output_path}")
            print(f"   : 1000x1000")
            print(f"   : {output_path.stat().st_size / 1024:.1f}KB")
            
            return output_path
            
        except Exception as e:
            print(f"     : {e}")
            return None
    
    def make_square_image(self, img: Image.Image, size: int) -> Image.Image:
        """   (  )"""
        
        #   
        width, height = img.size
        
        if width == height:
            #  
            return img.resize((size, size), Image.Resampling.LANCZOS)
        
        #     
        if width > height:
            #    -  
            new_img = Image.new('RGB', (width, width), (255, 255, 255))
            y_offset = (width - height) // 2
            new_img.paste(img, (0, y_offset))
            return new_img.resize((size, size), Image.Resampling.LANCZOS)
        else:
            #    -  
            new_img = Image.new('RGB', (height, height), (255, 255, 255))
            x_offset = (height - width) // 2
            new_img.paste(img, (x_offset, 0))
            return new_img.resize((size, size), Image.Resampling.LANCZOS)
    
    def optimize_content_images(self, html_content: str) -> str:
        """HTML    """
        
        import re
        
        #   
        img_pattern = r'<img[^>]*src=["\']([^"\']+)["\'][^>]*>'
        
        def replace_img_tag(match):
            img_tag = match.group(0)
            img_url = match.group(1)
            
            #   
            if '' in img_tag or 'main' in img_tag.lower():
                #  
                new_tag = f'''
<div class="product-image-container">
    <img src="{img_url}" 
         class="product-image product-main-image lazy-load" 
         alt=" "
         loading="lazy">
</div>'''
            else:
                #  
                new_tag = f'''
<div class="product-image-container">
    <img src="{img_url}" 
         class="product-image product-detail-image lazy-load" 
         alt=" "
         loading="lazy">
</div>'''
            
            return new_tag
        
        #   
        optimized_content = re.sub(img_pattern, replace_img_tag, html_content)
        
        #  CSS  (  )
        if '<style>' not in optimized_content:
            optimized_content = self.responsive_css + '\n' + optimized_content
        
        return optimized_content
    
    def extract_existing_images(self, txt_file_path: Path) -> List[str]:
        """ TXT   URL """
        
        import re
        
        with open(txt_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        #  URL 
        patterns = [
            r'<img[^>]*src=["\']([^"\']+)["\']',
            r'https?://[^\s<>"]+\.(?:jpg|jpeg|png|gif|webp)',
            r'//[^\s<>"]+\.(?:jpg|jpeg|png|gif|webp)'
        ]
        
        images = []
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            images.extend(matches)
        
        #  
        images = list(set(images))
        
        #  
        normalized_images = []
        for img in images:
            if img.startswith('//'):
                img = 'https:' + img
            if img.startswith('/'):
                img = 'https://manwonyori.cafe24.com' + img
            normalized_images.append(img)
        
        return normalized_images
    
    def process_product_images(self, product_info: Dict) -> Dict:
        """   """
        
        result = {
            "product": product_info,
            "representative": None,
            "optimized_images": [],
            "responsive_html": None,
            "errors": []
        }
        
        try:
            # 1.   
            txt_file = Path(product_info.get('file_path', ''))
            if txt_file.exists():
                existing_images = self.extract_existing_images(txt_file)
                print(f"\n  : {len(existing_images)}")
                
                # 2.  
                if existing_images:
                    #    
                    rep_image = self.create_representative_image(
                        existing_images[0],
                        product_info['product_num'],
                        product_info['product_name']
                    )
                    result["representative"] = str(rep_image) if rep_image else None
                
                # 3. HTML  
                with open(txt_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                optimized_content = self.optimize_content_images(content)
                result["responsive_html"] = optimized_content
                
                # 4.   
                output_path = self.base_path / "optimized" / f"{product_info['product_num']}_optimized.txt"
                output_path.parent.mkdir(exist_ok=True)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(optimized_content)
                
                print(f"    : {output_path}")
            
        except Exception as e:
            result["errors"].append(str(e))
            print(f"    : {e}")
        
        return result
    
    def generate_upload_ready_files(self):
        """   """
        
        print("\n" + "="*60)
        print("    ")
        print("="*60)
        
        #   
        rep_images = list(self.representative_path.glob("*.jpg"))
        
        # CSV   ( )
        csv_path = self.base_path / "representative_images_upload.csv"
        
        with open(csv_path, 'w', encoding='utf-8-sig') as f:
            f.write(",,\n")
            
            for img_path in rep_images:
                #   
                filename = img_path.stem
                product_num = filename.split('_')[0]
                
                f.write(f"{product_num},{img_path.name},{img_path}\n")
        
        print(f"\n    : {csv_path}")
        print(f"   {len(rep_images)} ")
        
        #  
        report = f"""
========================================
  
========================================

  : {self.representative_path}
  : {len(rep_images)}
  : {csv_path}

 :
- : 1000 x 1000 px
- : JPEG
- : 95%

 :
[]_[].jpg

========================================
"""
        
        print(report)
        
        #  
        report_path = self.base_path / "representative_images_report.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
    
    def create_responsive_template(self) -> str:
        """   """
        
        template = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title> </title>
    
    <style>
    /*    */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Noto Sans KR', sans-serif;
        line-height: 1.6;
        color: #333;
    }
    
    /*  */
    .product-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /*   */
    .product-image-container {
        width: 100%;
        margin-bottom: 30px;
    }
    
    .product-image {
        width: 100%;
        height: auto;
        display: block;
    }
    
    /*  (768px ) */
    @media (min-width: 768px) {
        .product-container {
            padding: 40px 20px;
        }
        
        .product-main-image {
            max-width: 800px;
            margin: 0 auto;
            display: block;
        }
        
        .product-detail-image {
            max-width: 600px;
            margin: 20px auto;
            display: block;
        }
        
        .image-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }
    }
    
    /*  (767px ) */
    @media (max-width: 767px) {
        .product-container {
            padding: 15px;
        }
        
        .product-main-image,
        .product-detail-image {
            width: 100%;
            height: auto;
        }
        
        .image-grid {
            display: block;
        }
        
        .image-grid > * {
            margin-bottom: 15px;
        }
    }
    
    /*   */
    .product-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        color: #222;
    }
    
    @media (max-width: 767px) {
        .product-title {
            font-size: 20px;
        }
    }
    
    .product-description {
        font-size: 16px;
        line-height: 1.8;
        margin-bottom: 30px;
    }
    
    @media (max-width: 767px) {
        .product-description {
            font-size: 14px;
        }
    }
    
    /*   */
    .info-table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
    }
    
    .info-table th,
    .info-table td {
        padding: 12px;
        border: 1px solid #e0e0e0;
        text-align: left;
    }
    
    .info-table th {
        background-color: #f8f8f8;
        font-weight: normal;
        width: 30%;
    }
    
    @media (max-width: 767px) {
        .info-table {
            font-size: 14px;
        }
        
        .info-table th,
        .info-table td {
            padding: 8px;
        }
    }
    
    /*   */
    .section {
        margin-bottom: 40px;
        padding-bottom: 40px;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .section:last-child {
        border-bottom: none;
    }
    
    .section-title {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 20px;
        color: #222;
    }
    
    @media (max-width: 767px) {
        .section {
            margin-bottom: 30px;
            padding-bottom: 30px;
        }
        
        .section-title {
            font-size: 18px;
        }
    }
    </style>
</head>
<body>
    <div class="product-container">
        <!--   -->
        <div class="product-image-container">
            <img src="{main_image_url}" 
                 class="product-image product-main-image" 
                 alt="  "
                 loading="lazy">
        </div>
        
        <!--   -->
        <section class="section">
            <h1 class="product-title">{product_name}</h1>
            <div class="product-description">
                {product_description}
            </div>
        </section>
        
        <!--   -->
        <section class="section">
            <h2 class="section-title"> </h2>
            <table class="info-table">
                <tbody>
                    {product_info_rows}
                </tbody>
            </table>
        </section>
        
        <!--   -->
        <section class="section">
            <h2 class="section-title"> </h2>
            {detail_images}
        </section>
        
        <!--   -->
        {additional_content}
    </div>
</body>
</html>"""
        
        return template


def main():
    """ """
    
    optimizer = ImageSizeOptimizer()
    
    print("\n" + "="*60)
    print("    ")
    print("="*60)
    print("\n:")
    print("  •   (1000x1000)")
    print("  •   ")
    print("  • / ")
    print("  •   URL ")
    
    #  
    sample_product = {
        "product_num": "131",
        "product_name": " ",
        "file_path": r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html\temp_txt\131.txt"
    }
    
    print(f"\n : {sample_product['product_name']}")
    
    #  
    result = optimizer.process_product_images(sample_product)
    
    if result["representative"]:
        print(f"\n : {result['representative']}")
    
    #   
    optimizer.generate_upload_ready_files()
    
    #   
    template = optimizer.create_responsive_template()
    template_path = optimizer.base_path / "responsive_template.html"
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"\n   : {template_path}")


if __name__ == "__main__":
    main()
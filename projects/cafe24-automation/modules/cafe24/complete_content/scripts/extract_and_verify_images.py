"""
이미지 추출 및 검증 스크립트
HTML 파일에서 이미지 링크 추출
"""
import re
from pathlib import Path
import json
from datetime import datetime

def extract_images_from_txt():
    """temp_txt 파일에서 이미지 링크 추출"""
    
    txt_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html\temp_txt")
    
    image_links = {}
    
    for txt_file in txt_path.glob("*.txt"):
        product_no = txt_file.stem
        
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 이미지 링크 추출
        img_pattern = r'src="([^"]*\.jpg[^"]*)"'
        images = re.findall(img_pattern, content)
        
        if images:
            image_links[product_no] = images
    
    print(f"총 {len(image_links)}개 상품의 이미지 링크 추출")
    
    # 결과 저장
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = Path(f"C:\\Users\\8899y\\CUA-MASTER\\modules\\cafe24\\complete_content\\reports\\image_links_{timestamp}.json")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(image_links, f, ensure_ascii=False, indent=2)
    
    print(f"결과 저장: {output_path}")
    
    return image_links

if __name__ == "__main__":
    extract_images_from_txt()
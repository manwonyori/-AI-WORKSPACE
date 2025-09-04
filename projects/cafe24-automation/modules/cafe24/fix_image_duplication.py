"""
Cafe24 상세페이지 이미지 중복 문제 해결 스크립트
각 제품별로 올바른 이미지 링크를 매핑하여 수정
"""

import json
import os
from pathlib import Path
from datetime import datetime
import re

class ImageDuplicationFixer:
    def __init__(self):
        self.base_dir = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24")
        self.content_dir = self.base_dir / "complete_content"
        self.output_dir = self.content_dir / "output" / "chuyoungru_fixed"
        self.output_dir.mkdir(exist_ok=True)
        
        # 제품별 올바른 이미지 매핑
        self.image_mapping = {
            "131": {
                "name": "교자만두 360g",
                "images": [
                    "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/common/common_1.jpg",  # 공통
                    "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/kyoja/kyoja-360g.jpg",  # 교자만두 전용
                    "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/kyoja/kyoja-360g-d.jpg"  # 교자만두 상세
                ]
            },
            "132": {
                "name": "고기왕만두 420g",
                "images": [
                    "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/common/common_1.jpg",  # 공통
                    "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/gokiking-420/gokiking-420g.jpg",  # 고기왕만두 전용
                    "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/gokiking-420/gokiking-420g-d.jpg"  # 고기왕만두 상세
                ]
            },
            "133": {
                "name": "김치만두 420g",
                "images": [
                    "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/common/common_1.jpg",
                    "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/kimchi/kimchi-420g.jpg",
                    "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/kimchi/kimchi-420g-d.jpg"
                ]
            },
            "134": {
                "name": "물만두 420g",
                "images": [
                    "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/common/common_1.jpg",
                    "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/mul/mul-420g.jpg",
                    "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/mul/mul-420g-d.jpg"
                ]
            },
            "135": {
                "name": "튀김만두 300g",
                "images": [
                    "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/common/common_1.jpg",
                    "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/fried/fried-300g.jpg",
                    "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/fried/fried-300g-d.jpg"
                ]
            },
            "140": {
                "name": "새우만두 420g",
                "images": [
                    "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/common/common_1.jpg",
                    "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/shrimp/shrimp-420g.jpg",
                    "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/shrimp/shrimp-420g-d.jpg"
                ]
            }
        }
    
    def fix_html_images(self, product_id: str):
        """HTML 파일의 이미지 링크 수정"""
        # 기존 파일 경로들
        improved_file = self.content_dir / "output" / "chuyoungru_improved" / f"{product_id}_improved.html"
        
        if not improved_file.exists():
            print(f"[오류] {product_id}_improved.html 파일이 없습니다.")
            return False
        
        # HTML 읽기
        with open(improved_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 제품별 올바른 이미지 정보
        if product_id not in self.image_mapping:
            print(f"[경고] {product_id} 제품의 이미지 매핑 정보가 없습니다.")
            return False
        
        product_info = self.image_mapping[product_id]
        
        # 이미지 태그 찾기 및 교체
        img_pattern = r'<img\s+src="([^"]+)"([^>]*)>'
        img_tags = re.findall(img_pattern, html_content)
        
        if len(img_tags) >= 3:
            # 첫 번째 이미지 (공통 이미지)
            old_img1 = img_tags[0][0]
            new_img1 = product_info['images'][0]
            html_content = html_content.replace(old_img1, new_img1, 1)
            
            # 두 번째 이미지 (제품별 이미지)
            old_img2 = img_tags[1][0]
            new_img2 = product_info['images'][1]
            html_content = html_content.replace(old_img2, new_img2, 1)
            
            # 세 번째 이미지 (상세 이미지)
            old_img3 = img_tags[2][0]
            new_img3 = product_info['images'][2]
            html_content = html_content.replace(old_img3, new_img3, 1)
            
            print(f"[수정] {product_id} 이미지 링크 교체:")
            print(f"  이미지1: {new_img1.split('/')[-1]}")
            print(f"  이미지2: {new_img2.split('/')[-1]}")
            print(f"  이미지3: {new_img3.split('/')[-1]}")
        
        # alt 텍스트도 제품별로 수정
        product_name = product_info['name']
        html_content = re.sub(
            r'alt="[^"]*고기왕만두[^"]*"',
            f'alt="취영루 {product_name}"',
            html_content
        )
        
        # 수정된 파일 저장
        output_file = self.output_dir / f"{product_id}_fixed.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"[저장] {output_file}")
        return True
    
    def fix_all_products(self):
        """모든 제품 HTML 수정"""
        print("="*60)
        print("Cafe24 상세페이지 이미지 중복 문제 수정")
        print("="*60)
        
        success_count = 0
        for product_id in self.image_mapping.keys():
            print(f"\n처리 중: {product_id} - {self.image_mapping[product_id]['name']}")
            if self.fix_html_images(product_id):
                success_count += 1
        
        print("\n" + "="*60)
        print(f"완료: {success_count}/{len(self.image_mapping)} 제품 수정됨")
        print(f"저장 위치: {self.output_dir}")
        
        # 보고서 생성
        self.create_report(success_count)
    
    def create_report(self, success_count):
        """수정 보고서 생성"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_products": len(self.image_mapping),
            "fixed_products": success_count,
            "output_directory": str(self.output_dir),
            "image_mappings": self.image_mapping
        }
        
        report_file = self.content_dir / "reports" / "image_fix_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n보고서 저장: {report_file}")

def main():
    fixer = ImageDuplicationFixer()
    fixer.fix_all_products()

if __name__ == "__main__":
    main()
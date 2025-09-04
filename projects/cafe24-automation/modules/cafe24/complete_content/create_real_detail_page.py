"""
진짜 상세페이지 생성 시스템
이미지 + 상세 정보 + 콘텐츠가 모두 포함된 완전한 상세페이지
"""

import json
from pathlib import Path
from datetime import datetime

class RealDetailPageCreator:
    def __init__(self):
        self.base_dir = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content")
        self.output_dir = self.base_dir / "output_real_detail"
        self.output_dir.mkdir(exist_ok=True)
        
        # Research 데이터 로드
        self.research_dir = self.base_dir / "research"
        
    def load_research_data(self, product_id: str):
        """제품 리서치 데이터 로드"""
        research_file = self.research_dir / f"{product_id}_research.json"
        if research_file.exists():
            with open(research_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def create_complete_detail_page(self, product_id: str):
        """완전한 상세페이지 생성"""
        
        # 리서치 데이터 로드
        research = self.load_research_data(product_id)
        if not research:
            print(f"[오류] {product_id} 리서치 데이터 없음")
            return None
        
        # 제품별 이미지 매핑
        image_map = {
            "131": {"folder": "kyoja", "file": "kyoja-360g"},
            "132": {"folder": "gokiking-420", "file": "gokiking-420g"},
            "133": {"folder": "kimchi", "file": "kimchi-420g"},
            "134": {"folder": "mul", "file": "mul-420g"},
            "135": {"folder": "fried", "file": "fried-300g"},
            "136": {"folder": "galbi", "file": "galbi-420g"},
            "137": {"folder": "shrimp", "file": "shrimp-420g"},
            "138": {"folder": "potato", "file": "potato-420g"},
            "139": {"folder": "vege", "file": "vege-420g"},
            "140": {"folder": "shrimp", "file": "shrimp-420g"}
        }
        
        img_info = image_map.get(product_id, {"folder": "common", "file": "common_1"})
        
        # HTML 생성
        html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{research['product_name']} - 만원요리</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #fff;
        }}
        
        .detail-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        /* 헤더 섹션 */
        .header-section {{
            text-align: center;
            padding: 40px 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 20px;
            margin-bottom: 40px;
        }}
        
        .product-title {{
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        
        .product-subtitle {{
            font-size: 18px;
            opacity: 0.9;
        }}
        
        /* 메인 콘텐츠 그리드 */
        .content-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            margin-bottom: 40px;
        }}
        
        @media (max-width: 768px) {{
            .content-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        
        /* 이미지 섹션 */
        .image-section {{
            position: relative;
        }}
        
        .main-image {{
            width: 100%;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        .badge {{
            position: absolute;
            top: 20px;
            left: 20px;
            background: #ff6b6b;
            color: white;
            padding: 8px 16px;
            border-radius: 25px;
            font-weight: 600;
            font-size: 14px;
        }}
        
        /* 정보 섹션 */
        .info-section {{
            padding: 20px;
        }}
        
        .feature-list {{
            margin-bottom: 30px;
        }}
        
        .feature-item {{
            display: flex;
            align-items: center;
            margin-bottom: 15px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            transition: transform 0.3s;
        }}
        
        .feature-item:hover {{
            transform: translateX(10px);
            background: #e9ecef;
        }}
        
        .feature-icon {{
            width: 30px;
            height: 30px;
            background: #667eea;
            border-radius: 50%;
            margin-right: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }}
        
        /* 영양정보 테이블 */
        .nutrition-section {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 40px;
        }}
        
        .section-title {{
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 20px;
            color: #495057;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            display: inline-block;
        }}
        
        .nutrition-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .nutrition-item {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        
        .nutrition-value {{
            font-size: 24px;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .nutrition-label {{
            font-size: 14px;
            color: #6c757d;
        }}
        
        /* 재료 섹션 */
        .ingredients-section {{
            margin-bottom: 40px;
        }}
        
        .ingredient-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-top: 20px;
        }}
        
        .ingredient-item {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 24px;
            border-radius: 25px;
            font-weight: 500;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }}
        
        /* 조리방법 섹션 */
        .cooking-section {{
            background: white;
            border: 2px solid #e9ecef;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 40px;
        }}
        
        .cooking-methods {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .cooking-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }}
        
        .cooking-title {{
            font-weight: 600;
            color: #495057;
            margin-bottom: 10px;
            font-size: 18px;
        }}
        
        .cooking-desc {{
            color: #6c757d;
            font-size: 14px;
        }}
        
        /* 하단 이미지 섹션 */
        .bottom-images {{
            margin-top: 50px;
        }}
        
        .detail-image {{
            width: 100%;
            margin-bottom: 20px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        
        /* 푸터 */
        .footer-section {{
            text-align: center;
            padding: 40px 20px;
            background: #f8f9fa;
            border-radius: 15px;
            margin-top: 50px;
        }}
        
        .brand-info {{
            font-size: 16px;
            color: #6c757d;
            margin-bottom: 10px;
        }}
        
        .haccp-badge {{
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            font-weight: 600;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <div class="detail-container">
        <!-- 헤더 -->
        <div class="header-section">
            <h1 class="product-title">{research['product_name']}</h1>
            <p class="product-subtitle">만원요리 X 취영루 프리미엄 만두</p>
        </div>
        
        <!-- 메인 콘텐츠 -->
        <div class="content-grid">
            <!-- 이미지 섹션 -->
            <div class="image-section">
                <span class="badge">BEST</span>
                <img src="https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/{img_info['folder']}/{img_info['file']}.jpg" 
                     alt="{research['product_name']}" 
                     class="main-image">
            </div>
            
            <!-- 정보 섹션 -->
            <div class="info-section">
                <h2 class="section-title">제품 특징</h2>
                <div class="feature-list">
"""
        
        # 특징 추가
        for i, feature in enumerate(research.get('features', []), 1):
            html_content += f"""
                    <div class="feature-item">
                        <div class="feature-icon">{i}</div>
                        <span>{feature}</span>
                    </div>
"""
        
        html_content += f"""
                </div>
                
                <div style="background: #fff3cd; padding: 15px; border-radius: 10px; margin-top: 20px;">
                    <strong style="color: #856404;">차별점:</strong>
                    <p style="color: #856404; margin-top: 5px;">{research.get('differentiators', '')}</p>
                </div>
            </div>
        </div>
        
        <!-- 영양정보 -->
        <div class="nutrition-section">
            <h2 class="section-title">영양정보 (100g당)</h2>
            <div class="nutrition-grid">
"""
        
        # 영양정보 추가
        nutrition = research.get('nutrition', {})
        for key, value in nutrition.items():
            html_content += f"""
                <div class="nutrition-item">
                    <div class="nutrition-value">{value}</div>
                    <div class="nutrition-label">{key}</div>
                </div>
"""
        
        html_content += f"""
            </div>
        </div>
        
        <!-- 주요 재료 -->
        <div class="ingredients-section">
            <h2 class="section-title">주요 재료</h2>
            <div class="ingredient-list">
"""
        
        # 재료 추가
        ingredients = research.get('ingredients', {})
        for ingredient, percentage in ingredients.items():
            html_content += f"""
                <div class="ingredient-item">{ingredient} {percentage}</div>
"""
        
        html_content += f"""
            </div>
        </div>
        
        <!-- 조리방법 -->
        <div class="cooking-section">
            <h2 class="section-title">조리방법</h2>
            <div class="cooking-methods">
"""
        
        # 조리방법 추가
        for method in research.get('cooking_methods', []):
            if ':' in method:
                title, desc = method.split(':', 1)
                html_content += f"""
                <div class="cooking-card">
                    <div class="cooking-title">{title}</div>
                    <div class="cooking-desc">{desc.strip()}</div>
                </div>
"""
        
        html_content += f"""
            </div>
        </div>
        
        <!-- 하단 이미지 -->
        <div class="bottom-images">
            <img src="https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/common/common_1.jpg" 
                 alt="취영루 브랜드 소개" 
                 class="detail-image">
            <img src="https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/chi/{img_info['folder']}/{img_info['file']}-d.jpg" 
                 alt="{research['product_name']} 상세정보" 
                 class="detail-image">
        </div>
        
        <!-- 푸터 -->
        <div class="footer-section">
            <p class="brand-info">70년 전통 취영루</p>
            <p class="brand-info">서울특별시 영등포구 도림로 152</p>
            <span class="haccp-badge">HACCP 인증</span>
        </div>
    </div>
</body>
</html>"""
        
        return html_content
    
    def generate_all_detail_pages(self):
        """모든 취영루 제품 상세페이지 생성"""
        print("\n" + "="*60)
        print("진짜 상세페이지 생성 시작")
        print("="*60)
        
        # 취영루 제품 목록
        chuyoungru_products = ["131", "132", "133", "134", "135", "136", "137", "138", "139", "140"]
        
        success_count = 0
        for product_id in chuyoungru_products:
            print(f"\n[생성 중] {product_id}번 제품")
            
            html_content = self.create_complete_detail_page(product_id)
            
            if html_content:
                # 저장
                output_file = self.output_dir / f"{product_id}_real_detail.html"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                print(f"  [OK] 저장 완료: {output_file.name}")
                success_count += 1
            else:
                print(f"  [X] 실패")
        
        print(f"\n완료: {success_count}/{len(chuyoungru_products)} 상세페이지 생성")
        
        # 샘플 파일 열기
        import os
        sample = self.output_dir / "131_real_detail.html"
        if sample.exists():
            os.system(f'start "" "{sample}"')
            print(f"\n샘플 열기: 131_real_detail.html")

def main():
    creator = RealDetailPageCreator()
    creator.generate_all_detail_pages()

if __name__ == "__main__":
    main()
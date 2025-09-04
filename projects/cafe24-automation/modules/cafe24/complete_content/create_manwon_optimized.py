"""
만원요리 최적화 상세페이지 생성기
- 간결한 2탭 구조 (상품설명, 상세정보)
- 만원요리 브랜드 색상 적용
- 불필요한 긴 콘텐츠 제거
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

class ManwonOptimizedPageGenerator:
    def __init__(self):
        """만원요리 최적화 페이지 생성기 초기화"""
        self.base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content")
        self.input_path = self.base_path / "html" / "temp_txt"
        self.output_path = self.base_path / "output" / "manwon"
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # 만원요리 실제 브랜드 색상 (사이트 분석 기반)
        self.brand_colors = {
            'primary': '#333333',      # 메인 텍스트
            'secondary': '#666666',    # 서브 텍스트  
            'accent': '#ff6b6b',       # 강조색 (빨간계열)
            'gold': '#ffd700',         # 골드 포인트
            'bg_main': '#ffffff',      # 메인 배경
            'bg_sub': '#f8f8f8',       # 서브 배경
            'border': '#e0e0e0',       # 테두리
            'price': '#e74c3c',        # 가격 강조
            'button': '#2c3e50',       # 버튼 색상
            'button_hover': '#34495e'  # 버튼 호버
        }
    
    def extract_product_info(self, file_path):
        """제품 정보 추출"""
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()
            
            # 제품명 추출
            title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            product_name = title_match.group(1) if title_match else "상품명"
            
            # 이미지 추출 
            img_matches = re.findall(r'<img[^>]*src=["\'](.*?)["\']', content, re.IGNORECASE)
            images = img_matches[:5] if img_matches else []  # 최대 5개만
            
            # 가격 추출
            price_match = re.search(r'(\d{1,3}(?:,\d{3})*)\s*원', content)
            price = price_match.group(1) if price_match else "10,000"
            
            # 간단한 설명 추출 (너무 길지 않게)
            desc_match = re.search(r'<p[^>]*>(.*?)</p>', content, re.IGNORECASE | re.DOTALL)
            description = ""
            if desc_match:
                description = re.sub(r'<[^>]+>', '', desc_match.group(1))[:200]  # 200자로 제한
            
            return {
                'product_name': product_name,
                'images': images,
                'price': price,
                'description': description
            }
        except Exception as e:
            print(f"[ERROR] 정보 추출 실패: {e}")
            return None
    
    def generate_optimized_html(self, product_info):
        """최적화된 HTML 생성 - 간결한 2탭 구조"""
        
        # 메인 이미지와 썸네일
        main_image = product_info['images'][0] if product_info['images'] else "https://via.placeholder.com/500"
        thumbnails = product_info['images'][1:5] if len(product_info['images']) > 1 else []
        
        # 썸네일 HTML
        thumbnail_html = ""
        if thumbnails:
            thumbnail_html = '\n'.join([
                f'                        <img src="{img}" alt="상품 이미지" class="thumbnail" onclick="changeMainImage(this.src)">'
                for img in thumbnails
            ])
        
        html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{product_info['product_name']}</title>
    
    <!-- Pretendard 폰트 (만원요리 사용 폰트) -->
    <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css" />
    
    <style>
        /* 만원요리 디자인 시스템 */
        :root {{
            --primary-color: {self.brand_colors['primary']};
            --secondary-color: {self.brand_colors['secondary']};
            --accent-color: {self.brand_colors['accent']};
            --gold-color: {self.brand_colors['gold']};
            --bg-main: {self.brand_colors['bg_main']};
            --bg-sub: {self.brand_colors['bg_sub']};
            --border-color: {self.brand_colors['border']};
            --price-color: {self.brand_colors['price']};
            --button-color: {self.brand_colors['button']};
            --button-hover: {self.brand_colors['button_hover']};
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--primary-color);
            line-height: 1.6;
            background: var(--bg-main);
        }}
        
        /* 컨테이너 */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        /* 상품 헤더 영역 */
        .product-header {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 30px;
            margin-bottom: 50px;
            padding: 30px;
            background: white;
            border: 1px solid var(--border-color);
        }}
        
        @media (min-width: 768px) {{
            .product-header {{
                grid-template-columns: 500px 1fr;
                gap: 40px;
            }}
        }}
        
        /* 이미지 영역 */
        .product-images {{
            position: relative;
        }}
        
        .main-image {{
            width: 100%;
            aspect-ratio: 1/1;
            object-fit: contain;
            background: var(--bg-sub);
            border: 1px solid var(--border-color);
        }}
        
        .thumbnail-list {{
            display: flex;
            gap: 10px;
            margin-top: 15px;
            overflow-x: auto;
        }}
        
        .thumbnail {{
            width: 70px;
            height: 70px;
            object-fit: cover;
            cursor: pointer;
            border: 2px solid var(--border-color);
            transition: border-color 0.3s;
        }}
        
        .thumbnail:hover {{
            border-color: var(--accent-color);
        }}
        
        /* 상품 정보 영역 */
        .product-info {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}
        
        .product-title {{
            font-size: 24px;
            font-weight: 600;
            color: var(--primary-color);
            line-height: 1.4;
        }}
        
        .price-section {{
            padding: 20px;
            background: var(--bg-sub);
            border-left: 3px solid var(--accent-color);
        }}
        
        .original-price {{
            text-decoration: line-through;
            color: var(--secondary-color);
            font-size: 16px;
        }}
        
        .final-price {{
            font-size: 28px;
            font-weight: 700;
            color: var(--price-color);
            margin-top: 5px;
        }}
        
        /* 구매 영역 */
        .purchase-section {{
            display: flex;
            flex-direction: column;
            gap: 15px;
        }}
        
        .quantity-control {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        .quantity-btn {{
            width: 35px;
            height: 35px;
            border: 1px solid var(--border-color);
            background: white;
            cursor: pointer;
            font-size: 18px;
            transition: all 0.3s;
        }}
        
        .quantity-btn:hover {{
            background: var(--bg-sub);
        }}
        
        .quantity-input {{
            width: 60px;
            height: 35px;
            text-align: center;
            border: 1px solid var(--border-color);
            font-size: 16px;
        }}
        
        .btn-purchase {{
            padding: 15px;
            background: var(--button-color);
            color: white;
            border: none;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s;
        }}
        
        .btn-purchase:hover {{
            background: var(--button-hover);
        }}
        
        .btn-cart {{
            padding: 15px;
            background: white;
            color: var(--button-color);
            border: 2px solid var(--button-color);
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }}
        
        .btn-cart:hover {{
            background: var(--bg-sub);
        }}
        
        /* 탭 네비게이션 - 간결한 2탭 */
        .tab-section {{
            margin-top: 50px;
            border-top: 2px solid var(--primary-color);
        }}
        
        .tab-nav {{
            display: flex;
            background: white;
            border-bottom: 1px solid var(--border-color);
        }}
        
        .tab-item {{
            flex: 1;
            padding: 15px;
            text-align: center;
            font-size: 16px;
            font-weight: 500;
            color: var(--secondary-color);
            cursor: pointer;
            border-bottom: 3px solid transparent;
            transition: all 0.3s;
        }}
        
        .tab-item.active {{
            color: var(--primary-color);
            border-bottom-color: var(--accent-color);
            font-weight: 600;
        }}
        
        .tab-item:hover {{
            background: var(--bg-sub);
        }}
        
        /* 탭 콘텐츠 - 간결하게 */
        .tab-content {{
            padding: 40px 20px;
            background: white;
            min-height: 300px;
        }}
        
        .tab-pane {{
            display: none;
        }}
        
        .tab-pane.active {{
            display: block;
        }}
        
        /* 상품설명 스타일 */
        .product-description {{
            max-width: 800px;
            margin: 0 auto;
            line-height: 1.8;
        }}
        
        .desc-title {{
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--accent-color);
        }}
        
        .desc-content {{
            color: var(--secondary-color);
            font-size: 15px;
        }}
        
        .desc-point {{
            background: var(--bg-sub);
            padding: 15px;
            margin: 20px 0;
            border-left: 3px solid var(--accent-color);
        }}
        
        /* 상세정보 테이블 */
        .detail-table {{
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            border-collapse: collapse;
        }}
        
        .detail-table th,
        .detail-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }}
        
        .detail-table th {{
            width: 150px;
            background: var(--bg-sub);
            font-weight: 500;
        }}
        
        /* 모바일 최적화 */
        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}
            
            .product-header {{
                padding: 20px;
            }}
            
            .product-title {{
                font-size: 20px;
            }}
            
            .tab-item {{
                font-size: 14px;
            }}
            
            .detail-table {{
                font-size: 14px;
            }}
            
            .detail-table th {{
                width: 120px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 상품 헤더 -->
        <div class="product-header">
            <div class="product-images">
                <img src="{main_image}" alt="{product_info['product_name']}" class="main-image" id="mainImage">
                <div class="thumbnail-list">
{thumbnail_html}
                </div>
            </div>
            
            <div class="product-info">
                <h1 class="product-title">{product_info['product_name']}</h1>
                
                <div class="price-section">
                    <div class="original-price">12,000원</div>
                    <div class="final-price">{product_info['price']}원</div>
                </div>
                
                <div class="purchase-section">
                    <div class="quantity-control">
                        <span>구매수량</span>
                        <button class="quantity-btn" onclick="changeQuantity(-1)">-</button>
                        <input type="number" class="quantity-input" id="quantity" value="1" min="1" max="99">
                        <button class="quantity-btn" onclick="changeQuantity(1)">+</button>
                    </div>
                    
                    <button class="btn-purchase">바로구매</button>
                    <button class="btn-cart">장바구니</button>
                </div>
            </div>
        </div>
        
        <!-- 탭 섹션 (간결한 2탭 구조) -->
        <div class="tab-section">
            <div class="tab-nav">
                <div class="tab-item active" onclick="showTab('description')">상품설명</div>
                <div class="tab-item" onclick="showTab('detail')">상세정보</div>
            </div>
            
            <div class="tab-content">
                <!-- 상품설명 탭 -->
                <div class="tab-pane active" id="description">
                    <div class="product-description">
                        <h2 class="desc-title">만원요리 프리미엄 간편식</h2>
                        
                        <div class="desc-point">
                            ✓ 엄선된 재료로 만든 프리미엄 제품<br>
                            ✓ 간편한 조리로 완벽한 한 끼 식사<br>
                            ✓ 합리적인 가격의 고품질 간편식
                        </div>
                        
                        <div class="desc-content">
                            <p>{product_info.get('description', '최고의 재료와 정성으로 만든 만원요리 시리즈입니다. 바쁜 일상 속에서도 집밥의 따뜻함을 느낄 수 있습니다.')}</p>
                            
                            <p style="margin-top: 20px;">
                                <strong>조리방법:</strong><br>
                                1. 냉동 상태에서 바로 조리 가능<br>
                                2. 전자레인지 3-5분<br>
                                3. 에어프라이어 5-7분
                            </p>
                        </div>
                    </div>
                </div>
                
                <!-- 상세정보 탭 -->
                <div class="tab-pane" id="detail">
                    <table class="detail-table">
                        <tr>
                            <th>제품명</th>
                            <td>{product_info['product_name']}</td>
                        </tr>
                        <tr>
                            <th>내용량</th>
                            <td>360g</td>
                        </tr>
                        <tr>
                            <th>원재료</th>
                            <td>상품 포장 참조</td>
                        </tr>
                        <tr>
                            <th>보관방법</th>
                            <td>냉동보관 (-18℃ 이하)</td>
                        </tr>
                        <tr>
                            <th>유통기한</th>
                            <td>제조일로부터 12개월</td>
                        </tr>
                        <tr>
                            <th>제조원</th>
                            <td>만원요리</td>
                        </tr>
                        <tr>
                            <th>배송안내</th>
                            <td>냉동배송</td>
                        </tr>
                        <tr>
                            <th>교환/반품</th>
                            <td>수령일로부터 7일 이내</td>
                        </tr>
                    </table>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // 이미지 변경
        function changeMainImage(src) {{
            document.getElementById('mainImage').src = src;
        }}
        
        // 수량 변경
        function changeQuantity(delta) {{
            const input = document.getElementById('quantity');
            let value = parseInt(input.value) + delta;
            if (value < 1) value = 1;
            if (value > 99) value = 99;
            input.value = value;
        }}
        
        // 탭 전환
        function showTab(tabName) {{
            // 모든 탭 비활성화
            document.querySelectorAll('.tab-item').forEach(tab => {{
                tab.classList.remove('active');
            }});
            document.querySelectorAll('.tab-pane').forEach(pane => {{
                pane.classList.remove('active');
            }});
            
            // 선택된 탭 활성화
            event.target.classList.add('active');
            document.getElementById(tabName).classList.add('active');
        }}
    </script>
</body>
</html>"""
        
        return html
    
    def process_product(self, product_number):
        """제품 처리"""
        file_path = self.input_path / f"{product_number}.txt"
        
        if not file_path.exists():
            print(f"[ERROR] 파일을 찾을 수 없습니다: {file_path}")
            return False
        
        # 제품 정보 추출
        product_info = self.extract_product_info(file_path)
        if not product_info:
            return False
        
        # HTML 생성
        html_content = self.generate_optimized_html(product_info)
        
        # 파일 저장
        output_file = self.output_path / f"{product_number}_optimized.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"[완료] {output_file}")
        print(f"  - 2탭 구조: 상품설명, 상세정보")
        print(f"  - 만원요리 브랜드 색상 적용")
        print(f"  - 간결한 콘텐츠 구성")
        
        return True

if __name__ == "__main__":
    import sys
    
    generator = ManwonOptimizedPageGenerator()
    
    # 제품 번호 처리
    product_number = sys.argv[1] if len(sys.argv) > 1 else "131"
    generator.process_product(product_number)
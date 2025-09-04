"""
통합 제품 상세페이지 생성 시스템
- 마켓컬리 스타일 + 우리 브랜드 색상
- 이미지 적용 버전과 링크 버전 동시 생성
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

class UnifiedProductPageGenerator:
    def __init__(self):
        """통합 제품 페이지 생성기 초기화"""
        self.base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content")
        self.input_path = self.base_path / "html" / "temp_txt"
        self.output_path = self.base_path / "output" / "unified"
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # 우리 브랜드 색상 시스템 (만원요리 브랜드)
        self.brand_colors = {
            '--brand-primary': '#E4A853',      # 금색 (Saffron Gold)
            '--brand-secondary': '#C53030',     # 진한 빨강 (Deep Rose)
            '--brand-dark': '#1F2937',          # 진한 차콜
            '--brand-accent': '#5f0080',        # 컬리 보라 (호환성)
            '--brand-success': '#51a351',       # 성공 초록
            '--brand-discount': '#fa622f',      # 할인 주황
            '--text-primary': '#333333',
            '--text-secondary': '#666666',
            '--text-muted': '#999999',
            '--bg-primary': '#ffffff',
            '--bg-secondary': '#f7f7f7',
            '--bg-accent': '#fff5e6',           # 연한 금색 배경
            '--border-light': '#e5e7eb',
            '--border-default': '#d1d5db',
            '--shadow-sm': '0 1px 3px rgba(0,0,0,0.12)',
            '--shadow-md': '0 4px 6px rgba(0,0,0,0.15)',
            '--shadow-lg': '0 10px 15px rgba(0,0,0,0.2)'
        }
    
    def extract_product_info(self, file_path):
        """제품 정보 추출"""
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()
            
            # 제품명 추출
            title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            product_name = title_match.group(1) if title_match else "상품명"
            
            # 이미지 링크 추출
            img_matches = re.findall(r'<img[^>]*src=["\'](.*?)["\']', content, re.IGNORECASE)
            images = img_matches[:10] if img_matches else []  # 최대 10개
            
            # 가격 정보 추출 (다양한 패턴)
            price_patterns = [
                r'(\d{1,3}(?:,\d{3})*)\s*원',
                r'₩\s*(\d{1,3}(?:,\d{3})*)',
                r'price["\']?\s*[:=]\s*["\']*(\d{1,3}(?:,\d{3})*)'
            ]
            
            price = "10,000"  # 기본값
            for pattern in price_patterns:
                price_match = re.search(pattern, content, re.IGNORECASE)
                if price_match:
                    price = price_match.group(1)
                    break
            
            # 제품 설명 추출
            desc_patterns = [
                r'<p[^>]*>(.*?)</p>',
                r'<div[^>]*class=["\']*description["\']*[^>]*>(.*?)</div>'
            ]
            
            description = ""
            for pattern in desc_patterns:
                desc_match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
                if desc_match:
                    description = re.sub(r'<[^>]+>', '', desc_match.group(1))[:500]
                    break
            
            return {
                'product_name': product_name,
                'images': images,
                'price': price,
                'description': description,
                'original_content': content
            }
        except Exception as e:
            print(f"[ERROR] 제품 정보 추출 실패: {e}")
            return None
    
    def generate_unified_html(self, product_info, version='with_images'):
        """통합 HTML 생성"""
        
        # 색상 시스템 CSS
        color_css = '\n'.join([f"    {key}: {value};" for key, value in self.brand_colors.items()])
        
        # 이미지 처리
        if version == 'with_images' and product_info['images']:
            # 실제 이미지 사용
            main_image = product_info['images'][0]
            thumbnails = product_info['images'][1:5] if len(product_info['images']) > 1 else []
        else:
            # 플레이스홀더 또는 링크 이미지
            main_image = product_info['images'][0] if product_info['images'] else "https://via.placeholder.com/500"
            thumbnails = product_info['images'][1:5] if len(product_info['images']) > 1 else []
        
        # 썸네일 HTML 생성
        thumbnail_html = ""
        if thumbnails:
            thumbnail_html = '\n'.join([
                f'                <img src="{img}" alt="제품 이미지 {i+2}" class="thumbnail" onclick="changeMainImage(this.src)">'
                for i, img in enumerate(thumbnails)
            ])
        
        html_template = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>{product_info['product_name']} - 만원요리</title>
    
    <!-- 폰트 -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    
    <style>
        /* 브랜드 색상 시스템 */
        :root {{
{color_css}
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--text-primary);
            line-height: 1.6;
            background: var(--bg-primary);
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        
        /* 메인 컨테이너 */
        .product-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        /* 상품 헤더 영역 */
        .product-header {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 40px;
            margin-bottom: 60px;
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: var(--shadow-md);
        }}
        
        @media (min-width: 768px) {{
            .product-header {{
                grid-template-columns: 500px 1fr;
                gap: 50px;
            }}
        }}
        
        /* 이미지 영역 */
        .product-images {{
            position: relative;
        }}
        
        .main-image-container {{
            position: relative;
            width: 100%;
            aspect-ratio: 1/1;
            border-radius: 8px;
            overflow: hidden;
            background: var(--bg-secondary);
            border: 2px solid var(--border-light);
        }}
        
        .main-image {{
            width: 100%;
            height: 100%;
            object-fit: {('contain' if version == 'link_version' else 'cover')};
        }}
        
        /* 이미지 리사이징 (링크 버전) */
        {'''
        @media (max-width: 768px) {
            .main-image {
                max-height: 400px;
            }
        }
        ''' if version == 'link_version' else ''}
        
        .discount-badge {{
            position: absolute;
            top: 10px;
            left: 10px;
            background: var(--brand-secondary);
            color: white;
            padding: 8px 16px;
            border-radius: 24px;
            font-weight: 700;
            font-size: 14px;
            z-index: 10;
        }}
        
        .thumbnail-list {{
            display: flex;
            gap: 10px;
            margin-top: 16px;
            overflow-x: auto;
            padding: 5px 0;
            -webkit-overflow-scrolling: touch;
        }}
        
        .thumbnail {{
            width: 80px;
            height: 80px;
            border-radius: 4px;
            border: 2px solid var(--border-light);
            cursor: pointer;
            transition: all 0.3s ease;
            flex-shrink: 0;
            object-fit: cover;
        }}
        
        .thumbnail:hover {{
            border-color: var(--brand-primary);
            transform: scale(1.05);
        }}
        
        /* 상품 정보 영역 */
        .product-info {{
            display: flex;
            flex-direction: column;
            gap: 24px;
        }}
        
        .brand-badge {{
            display: inline-block;
            background: var(--bg-accent);
            color: var(--brand-primary);
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 14px;
            font-weight: 700;
            margin-bottom: 8px;
        }}
        
        .product-title {{
            font-size: 28px;
            font-weight: 700;
            color: var(--text-primary);
            line-height: 1.3;
        }}
        
        .product-subtitle {{
            font-size: 16px;
            color: var(--text-secondary);
            margin-top: 8px;
        }}
        
        /* 가격 영역 */
        .price-section {{
            background: var(--bg-secondary);
            padding: 24px;
            border-radius: 8px;
            border-left: 4px solid var(--brand-primary);
        }}
        
        .price-row {{
            display: flex;
            align-items: baseline;
            gap: 16px;
            margin-bottom: 8px;
        }}
        
        .discount-rate {{
            color: var(--brand-secondary);
            font-size: 32px;
            font-weight: 900;
        }}
        
        .original-price {{
            text-decoration: line-through;
            color: var(--text-muted);
            font-size: 18px;
        }}
        
        .final-price {{
            font-size: 32px;
            font-weight: 900;
            color: var(--text-primary);
        }}
        
        .price-unit {{
            font-size: 20px;
            font-weight: 400;
        }}
        
        /* 구매 옵션 */
        .purchase-options {{
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}
        
        .quantity-selector {{
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 16px;
            background: white;
            border: 1px solid var(--border-default);
            border-radius: 8px;
        }}
        
        .quantity-label {{
            font-weight: 500;
            color: var(--text-secondary);
            min-width: 80px;
        }}
        
        .quantity-controls {{
            display: flex;
            align-items: center;
            gap: 0;
            border: 1px solid var(--border-default);
            border-radius: 4px;
            overflow: hidden;
        }}
        
        .quantity-btn {{
            width: 36px;
            height: 36px;
            border: none;
            background: white;
            cursor: pointer;
            font-size: 18px;
            color: var(--text-secondary);
            transition: all 0.2s;
        }}
        
        .quantity-btn:hover {{
            background: var(--bg-secondary);
        }}
        
        .quantity-input {{
            width: 60px;
            height: 36px;
            border: none;
            border-left: 1px solid var(--border-default);
            border-right: 1px solid var(--border-default);
            text-align: center;
            font-size: 16px;
            font-weight: 500;
        }}
        
        /* 액션 버튼 */
        .action-buttons {{
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 12px;
        }}
        
        .btn {{
            padding: 16px 24px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            border: none;
        }}
        
        .btn-wishlist {{
            background: white;
            border: 2px solid var(--brand-primary);
            color: var(--brand-primary);
        }}
        
        .btn-wishlist:hover {{
            background: var(--bg-accent);
        }}
        
        .btn-cart {{
            background: var(--brand-primary);
            color: white;
        }}
        
        .btn-cart:hover {{
            background: var(--brand-secondary);
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }}
        
        /* 상품 메타 정보 */
        .product-meta {{
            padding: 24px;
            background: var(--bg-secondary);
            border-radius: 8px;
        }}
        
        .meta-item {{
            display: flex;
            padding: 12px 0;
            border-bottom: 1px solid var(--border-light);
        }}
        
        .meta-item:last-child {{
            border-bottom: none;
        }}
        
        .meta-label {{
            width: 120px;
            color: var(--text-secondary);
            font-size: 14px;
        }}
        
        .meta-value {{
            flex: 1;
            color: var(--text-primary);
            font-size: 14px;
            font-weight: 500;
        }}
        
        /* 상세 정보 탭 */
        .detail-tabs {{
            margin-top: 60px;
            border-top: 2px solid var(--brand-primary);
        }}
        
        .tab-nav {{
            display: flex;
            background: white;
            border-bottom: 1px solid var(--border-light);
            overflow-x: auto;
        }}
        
        .tab-item {{
            padding: 16px 24px;
            font-size: 16px;
            font-weight: 500;
            color: var(--text-secondary);
            cursor: pointer;
            border-bottom: 3px solid transparent;
            transition: all 0.3s;
            white-space: nowrap;
        }}
        
        .tab-item.active {{
            color: var(--brand-primary);
            border-bottom-color: var(--brand-primary);
        }}
        
        .tab-item:hover {{
            color: var(--text-primary);
            background: var(--bg-secondary);
        }}
        
        .tab-content {{
            padding: 40px 20px;
            background: white;
        }}
        
        .content-section {{
            margin-bottom: 40px;
        }}
        
        .section-title {{
            font-size: 24px;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 24px;
            padding-bottom: 12px;
            border-bottom: 2px solid var(--brand-primary);
        }}
        
        .highlight-box {{
            background: var(--bg-accent);
            border-left: 4px solid var(--brand-primary);
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        
        .highlight-title {{
            font-size: 18px;
            font-weight: 700;
            color: var(--brand-primary);
            margin-bottom: 12px;
        }}
        
        /* 반응형 이미지 그리드 */
        .image-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .grid-image {{
            width: 100%;
            aspect-ratio: 1/1;
            object-fit: cover;
            border-radius: 8px;
            box-shadow: var(--shadow-sm);
        }}
        
        /* 푸터 정보 */
        .product-footer {{
            margin-top: 60px;
            padding: 30px;
            background: var(--bg-secondary);
            border-radius: 12px;
            text-align: center;
        }}
        
        .footer-logo {{
            font-size: 24px;
            font-weight: 900;
            color: var(--brand-primary);
            margin-bottom: 16px;
        }}
        
        .footer-text {{
            color: var(--text-secondary);
            font-size: 14px;
            line-height: 1.8;
        }}
        
        /* 모바일 최적화 */
        @media (max-width: 768px) {{
            .product-container {{
                padding: 10px;
            }}
            
            .product-header {{
                padding: 20px;
            }}
            
            .product-title {{
                font-size: 24px;
            }}
            
            .action-buttons {{
                grid-template-columns: 1fr;
            }}
            
            .tab-nav {{
                -webkit-overflow-scrolling: touch;
            }}
        }}
    </style>
</head>
<body>
    <div class="product-container">
        <!-- 상품 헤더 -->
        <div class="product-header">
            <div class="product-images">
                <div class="main-image-container">
                    <span class="discount-badge">20% 할인</span>
                    <img src="{main_image}" alt="{product_info['product_name']}" class="main-image" id="mainImage">
                </div>
                <div class="thumbnail-list">
{thumbnail_html}
                </div>
            </div>
            
            <div class="product-info">
                <div>
                    <span class="brand-badge">만원요리</span>
                    <h1 class="product-title">{product_info['product_name']}</h1>
                    <p class="product-subtitle">프리미엄 간편식 시리즈</p>
                </div>
                
                <div class="price-section">
                    <div class="price-row">
                        <span class="discount-rate">20%</span>
                        <span class="original-price">12,500원</span>
                    </div>
                    <div class="final-price">
                        {product_info['price']}<span class="price-unit">원</span>
                    </div>
                </div>
                
                <div class="purchase-options">
                    <div class="quantity-selector">
                        <span class="quantity-label">구매수량</span>
                        <div class="quantity-controls">
                            <button class="quantity-btn" onclick="decreaseQuantity()">-</button>
                            <input type="number" class="quantity-input" id="quantity" value="1" min="1" max="99">
                            <button class="quantity-btn" onclick="increaseQuantity()">+</button>
                        </div>
                    </div>
                    
                    <div class="action-buttons">
                        <button class="btn btn-wishlist">♥ 찜하기</button>
                        <button class="btn btn-cart">장바구니 담기</button>
                    </div>
                </div>
                
                <div class="product-meta">
                    <div class="meta-item">
                        <span class="meta-label">배송방법</span>
                        <span class="meta-value">샛별배송 / 일반배송</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">판매단위</span>
                        <span class="meta-value">1팩</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">중량/용량</span>
                        <span class="meta-value">500g</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">원산지</span>
                        <span class="meta-value">상품설명 참조</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">유통기한</span>
                        <span class="meta-value">제조일로부터 12개월</span>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 상세 정보 탭 -->
        <div class="detail-tabs">
            <div class="tab-nav">
                <div class="tab-item active" onclick="showTab('description')">상품설명</div>
                <div class="tab-item" onclick="showTab('detail')">상세정보</div>
                <div class="tab-item" onclick="showTab('review')">후기</div>
                <div class="tab-item" onclick="showTab('inquiry')">문의</div>
            </div>
            
            <div class="tab-content" id="description">
                <div class="content-section">
                    <h2 class="section-title">만원요리가 제안하는 특별한 맛</h2>
                    
                    <div class="highlight-box">
                        <div class="highlight-title">✨ 프리미엄 재료로 만든 정성</div>
                        <p>엄선된 국내산 재료만을 사용하여 만든 프리미엄 간편식입니다.</p>
                    </div>
                    
                    <p style="margin: 20px 0; line-height: 1.8;">
                        {product_info.get('description', '최고급 재료와 전문 셰프의 노하우가 만나 탄생한 만원요리 시리즈. 집에서도 레스토랑 못지않은 맛을 경험해보세요.')}
                    </p>
                    
                    <!-- 이미지 그리드 -->
                    <div class="image-grid">
                        {f'<img src="{product_info["images"][1]}" alt="상품 이미지" class="grid-image">' if len(product_info['images']) > 1 else ''}
                        {f'<img src="{product_info["images"][2]}" alt="상품 이미지" class="grid-image">' if len(product_info['images']) > 2 else ''}
                    </div>
                </div>
                
                <div class="content-section">
                    <h2 class="section-title">이렇게 즐겨보세요</h2>
                    <ol style="padding-left: 20px; line-height: 2;">
                        <li>냉동 상태에서 바로 조리 가능합니다</li>
                        <li>전자레인지 3분, 에어프라이어 5분이면 완성</li>
                        <li>취향에 따라 소스를 추가해보세요</li>
                    </ol>
                </div>
            </div>
        </div>
        
        <!-- 푸터 -->
        <div class="product-footer">
            <div class="footer-logo">만원요리</div>
            <p class="footer-text">
                프리미엄 간편식의 새로운 기준<br>
                만원의 행복을 전해드립니다
            </p>
        </div>
    </div>
    
    <script>
        function changeMainImage(src) {{
            document.getElementById('mainImage').src = src;
        }}
        
        function increaseQuantity() {{
            var input = document.getElementById('quantity');
            var value = parseInt(input.value);
            if (value < 99) {{
                input.value = value + 1;
            }}
        }}
        
        function decreaseQuantity() {{
            var input = document.getElementById('quantity');
            var value = parseInt(input.value);
            if (value > 1) {{
                input.value = value - 1;
            }}
        }}
        
        function showTab(tabName) {{
            // 탭 전환 로직
            var tabs = document.querySelectorAll('.tab-item');
            tabs.forEach(function(tab) {{
                tab.classList.remove('active');
            }});
            event.target.classList.add('active');
            
            // 콘텐츠 전환 (실제 구현시 추가)
            console.log('Showing tab:', tabName);
        }}
    </script>
</body>
</html>"""
        
        return html_template
    
    def process_product(self, file_path, product_number):
        """단일 제품 처리"""
        print(f"\n[처리중] 제품 {product_number}")
        
        # 제품 정보 추출
        product_info = self.extract_product_info(file_path)
        if not product_info:
            print(f"[ERROR] 제품 정보 추출 실패: {product_number}")
            return False
        
        # 두 가지 버전 생성
        versions = [
            ('with_images', '이미지 적용 버전'),
            ('link_version', '링크 리사이징 버전')
        ]
        
        for version_type, version_name in versions:
            html_content = self.generate_unified_html(product_info, version_type)
            
            # 파일 저장
            output_file = self.output_path / f"{product_number}_{version_type}.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"  [OK] {version_name} 생성: {output_file}")
        
        # 리포트 생성
        report = {
            'timestamp': datetime.now().isoformat(),
            'product_number': product_number,
            'product_name': product_info['product_name'],
            'image_count': len(product_info['images']),
            'versions_created': ['with_images', 'link_version'],
            'output_path': str(self.output_path)
        }
        
        report_file = self.output_path / f"{product_number}_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return True
    
    def run(self, product_number=None):
        """실행"""
        if product_number:
            # 단일 제품 처리
            file_path = self.input_path / f"{product_number}.txt"
            if file_path.exists():
                success = self.process_product(file_path, product_number)
                if success:
                    print(f"\n[완료] 제품 {product_number} 처리 완료!")
                    print(f"  - 이미지 버전: {self.output_path}/{product_number}_with_images.html")
                    print(f"  - 링크 버전: {self.output_path}/{product_number}_link_version.html")
            else:
                print(f"[ERROR] 파일을 찾을 수 없습니다: {file_path}")
        else:
            # 전체 처리 (필요시)
            print("[INFO] 제품 번호를 지정하세요")

if __name__ == "__main__":
    import sys
    
    generator = UnifiedProductPageGenerator()
    
    if len(sys.argv) > 1:
        product_number = sys.argv[1]
        generator.run(product_number)
    else:
        # 테스트용 131번 제품 처리
        generator.run("131")
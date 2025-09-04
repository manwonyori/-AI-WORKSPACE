"""
카페24 상품 콘텐츠만 생성하는 시스템
- 상품 헤더는 카페24가 자동 처리
- 우리는 상품설명과 상세정보 HTML만 생성
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

class ContentOnlyGenerator:
    def __init__(self):
        """콘텐츠 전용 생성기 초기화"""
        self.base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content")
        self.input_path = self.base_path / "html" / "temp_txt"
        self.output_path = self.base_path / "output" / "content_only"
        self.output_path.mkdir(parents=True, exist_ok=True)
    
    def extract_product_info(self, file_path):
        """제품 정보 추출"""
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()
            
            # 제품명 추출
            title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            product_name = title_match.group(1) if title_match else "상품명"
            
            # 이미지 추출 (콘텐츠에 삽입할 이미지만)
            img_matches = re.findall(r'<img[^>]*src=["\'](.*?)["\']', content, re.IGNORECASE)
            content_images = img_matches[2:7] if len(img_matches) > 2 else []  # 상세 이미지용
            
            # 간단한 설명 추출
            desc_match = re.search(r'<p[^>]*>(.*?)</p>', content, re.IGNORECASE | re.DOTALL)
            description = ""
            if desc_match:
                description = re.sub(r'<[^>]+>', '', desc_match.group(1))[:200]
            
            return {
                'product_name': product_name,
                'content_images': content_images,
                'description': description
            }
        except Exception as e:
            print(f"[ERROR] 정보 추출 실패: {e}")
            return None
    
    def generate_content_html(self, product_info):
        """콘텐츠 HTML만 생성 (카페24 상세페이지용)"""
        
        # 콘텐츠 이미지 HTML 생성
        content_images_html = ""
        if product_info['content_images']:
            content_images_html = '\n'.join([
                f'    <img src="{img}" alt="상품 상세 이미지" style="width: 100%; max-width: 860px; margin: 20px auto; display: block;">'
                for img in product_info['content_images']
            ])
        
        # 카페24 상세페이지에 들어갈 콘텐츠만 생성
        html = f"""<!-- 상품 상세 콘텐츠 시작 -->
<style>
    .product-content-wrapper {{
        max-width: 860px;
        margin: 0 auto;
        padding: 20px;
        font-family: "Pretendard Variable", Pretendard, -apple-system, sans-serif;
        color: #333;
        line-height: 1.6;
    }}
    
    .content-section {{
        margin-bottom: 50px;
    }}
    
    .section-title {{
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #ff6b6b;
        color: #333;
    }}
    
    .highlight-box {{
        background: #f8f8f8;
        padding: 20px;
        margin: 20px 0;
        border-left: 3px solid #ff6b6b;
    }}
    
    .highlight-box ul {{
        list-style: none;
        padding: 0;
    }}
    
    .highlight-box li {{
        padding: 5px 0;
        color: #333;
    }}
    
    .highlight-box li:before {{
        content: "✓ ";
        color: #ff6b6b;
        font-weight: bold;
        margin-right: 8px;
    }}
    
    .cooking-method {{
        background: #fff;
        padding: 20px;
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        margin: 20px 0;
    }}
    
    .cooking-method h3 {{
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 15px;
        color: #333;
    }}
    
    .cooking-method ol {{
        padding-left: 20px;
        color: #666;
    }}
    
    .cooking-method li {{
        padding: 5px 0;
    }}
    
    .detail-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
    }}
    
    .detail-table th,
    .detail-table td {{
        padding: 12px;
        text-align: left;
        border-bottom: 1px solid #e0e0e0;
    }}
    
    .detail-table th {{
        width: 150px;
        background: #f8f8f8;
        font-weight: 500;
        color: #333;
    }}
    
    .detail-table td {{
        color: #666;
    }}
    
    @media (max-width: 768px) {{
        .product-content-wrapper {{
            padding: 20px;
            font-size: 18px;
        }}
        
        .section-title {{
            font-size: 26px !important;
            margin-bottom: 20px;
            font-weight: 700;
        }}
        
        .highlight-box {{
            padding: 20px;
            font-size: 18px;
        }}
        
        .highlight-box li {{
            font-size: 18px !important;
            padding: 10px 0;
            line-height: 1.6;
        }}
        
        .cooking-method {{
            font-size: 18px;
        }}
        
        .cooking-method h3 {{
            font-size: 22px !important;
            margin-bottom: 15px;
        }}
        
        .cooking-method li {{
            font-size: 18px !important;
            padding: 10px 0;
            line-height: 1.5;
        }}
        
        .cooking-method ol {{
            padding-left: 25px;
        }}
        
        .detail-table {{
            font-size: 18px;
        }}
        
        .detail-table th,
        .detail-table td {{
            padding: 18px 12px;
            font-size: 18px !important;
        }}
        
        .detail-table th {{
            width: 110px;
            font-size: 17px !important;
            font-weight: 600;
        }}
        
        p {{
            font-size: 18px !important;
            line-height: 1.7;
            margin: 15px 0;
        }}
        
        /* 모바일에서 판매자 정보 글자 크기 */
        .content-section h3 {{
            font-size: 20px !important;
            font-weight: 600;
        }}
        
        /* 판매자 정보 모바일 최적화 */
        .seller-info-section {{
            margin-bottom: 25px !important;
            padding: 25px !important;
        }}
        
        .seller-info-section h3 {{
            font-size: 22px !important;
            margin-bottom: 20px !important;
        }}
        
        .seller-info-section .detail-table th {{
            width: 120px !important;
            font-size: 17px !important;
            padding: 20px 15px !important;
        }}
        
        .seller-info-section .detail-table td {{
            font-size: 18px !important;
            padding: 20px 15px !important;
            line-height: 1.5;
        }}
        
        /* 모든 텍스트 강제로 18px 이상 */
        * {{
            font-size: 18px !important;
        }}
        
        /* 제목들은 더 크게 */
        h1, h2, h3 {{
            font-size: 24px !important;
        }}
        
        /* 섹션 제목 특별히 크게 */
        .section-title {{
            font-size: 28px !important;
            margin-bottom: 25px !important;
        }}
    }}
</style>

<div class="product-content-wrapper">
    <!-- 상품설명 섹션 -->
    <div class="content-section">
        <h2 class="section-title">상품설명</h2>
        
        <div class="highlight-box">
            <ul>
                <li>엄선된 재료로 만든 프리미엄 제품</li>
                <li>간편한 조리로 완벽한 한 끼 식사</li>
                <li>합리적인 가격의 고품질 간편식</li>
            </ul>
        </div>
        
        <p style="margin: 20px 0; color: #666;">
            {product_info.get('description', '만원요리 최씨남매 X 취영루 단독 공구')}
        </p>
        
        <div class="cooking-method">
            <h3>조리방법</h3>
            <ol>
                <li>냉동 상태에서 바로 조리 가능</li>
                <li>전자레인지 3-5분</li>
                <li>에어프라이어 5-7분</li>
            </ol>
        </div>
    </div>
    
    <!-- 콘텐츠 이미지들 -->
{content_images_html}
    
    <!-- 상세정보 섹션 -->
    <div class="content-section">
        <h2 class="section-title">상세정보</h2>
        
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
        </table>
    </div>
    
    <!-- 판매자 정보 섹션 -->
    <div class="content-section">
        <h2 class="section-title">판매자 정보</h2>
        
        <!-- 회사 정보 -->
        <div class="seller-info-section" style="background: #f8f8f8; padding: 20px; border-radius: 5px; margin-bottom: 20px;">
            <h3 style="color: #ff6b6b; font-size: 20px; font-weight: 600; margin-bottom: 15px; text-align: center;">회사 정보</h3>
            <table class="detail-table" style="margin: 0;">
                <tr>
                    <th>상호</th>
                    <td>㈜값진한끼</td>
                </tr>
                <tr>
                    <th>대표자</th>
                    <td>고혜숙</td>
                </tr>
                <tr>
                    <th>사업자등록번호</th>
                    <td>434-86-03863</td>
                </tr>
                <tr>
                    <th>통신판매업</th>
                    <td>2025-경기파주-2195호</td>
                </tr>
            </table>
        </div>
        
        <!-- 연락처 정보 -->
        <div class="seller-info-section" style="background: #f8f8f8; padding: 20px; border-radius: 5px;">
            <h3 style="color: #ff6b6b; font-size: 20px; font-weight: 600; margin-bottom: 15px; text-align: center;">연락처</h3>
            <table class="detail-table" style="margin: 0;">
                <tr>
                    <th>주소</th>
                    <td>경기도 파주시 경의로 1246, 11층 1105-19호</td>
                </tr>
                <tr>
                    <th>전화</th>
                    <td>070-8835-2885</td>
                </tr>
                <tr>
                    <th>이메일</th>
                    <td>we@manwonyori.com</td>
                </tr>
                <tr>
                    <th>사이트</th>
                    <td>만원요리 최씨남매</td>
                </tr>
            </table>
        </div>
    </div>
</div>
<!-- 상품 상세 콘텐츠 끝 -->"""
        
        return html
    
    def generate_simple_text(self, product_info):
        """카페24 에디터용 간단한 텍스트 버전"""
        text = f"""상품설명
─────────────────────────

만원요리 프리미엄 간편식

✓ 엄선된 재료로 만든 프리미엄 제품
✓ 간편한 조리로 완벽한 한 끼 식사
✓ 합리적인 가격의 고품질 간편식

{product_info.get('description', '만원요리 최씨남매 X 취영루 단독 공구')}

조리방법:
1. 냉동 상태에서 바로 조리 가능
2. 전자레인지 3-5분
3. 에어프라이어 5-7분


상세정보
─────────────────────────

제품명: {product_info['product_name']}
내용량: 360g
원재료: 상품 포장 참조
보관방법: 냉동보관 (-18℃ 이하)
유통기한: 제조일로부터 12개월
제조원: 만원요리
배송안내: 냉동배송


판매자 정보
─────────────────────────

[회사 정보]
상호: ㈜값진한끼
대표자: 고혜숙  
사업자등록번호: 434-86-03863
통신판매업: 2025-경기파주-2195호

[연락처]
주소: 경기도 파주시 경의로 1246, 11층 1105-19호
전화: 070-8835-2885
이메일: we@manwonyori.com
사이트: 만원요리 최씨남매"""
        
        return text
    
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
        
        # HTML 버전 생성
        html_content = self.generate_content_html(product_info)
        html_file = self.output_path / f"{product_number}_content.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # 텍스트 버전 생성
        text_content = self.generate_simple_text(product_info)
        text_file = self.output_path / f"{product_number}_content.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(text_content)
        
        print(f"[완료] 콘텐츠만 생성 완료")
        print(f"  HTML: {html_file}")
        print(f"  TEXT: {text_file}")
        print(f"  카페24 상세페이지에 바로 붙여넣기 가능")
        
        return True
    
    def process_batch(self, start_num=131, end_num=140):
        """배치 처리"""
        print(f"\n[배치 처리] {start_num}번부터 {end_num}번까지")
        print("-" * 50)
        
        success_count = 0
        for num in range(start_num, end_num + 1):
            product_number = str(num)
            file_path = self.input_path / f"{product_number}.txt"
            
            if file_path.exists():
                print(f"\n[{num}] 처리중...")
                if self.process_product(product_number):
                    success_count += 1
            else:
                print(f"[{num}] 파일 없음 - 건너뜀")
        
        print(f"\n[배치 완료] 총 {success_count}개 제품 처리 완료")
        return success_count

if __name__ == "__main__":
    import sys
    
    generator = ContentOnlyGenerator()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "batch":
            # 배치 처리
            start = int(sys.argv[2]) if len(sys.argv) > 2 else 131
            end = int(sys.argv[3]) if len(sys.argv) > 3 else 140
            generator.process_batch(start, end)
        else:
            # 단일 제품
            product_number = sys.argv[1]
            generator.process_product(product_number)
    else:
        # 기본 테스트
        generator.process_product("131")
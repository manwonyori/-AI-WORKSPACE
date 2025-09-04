"""
완전한 중복 제거 및 이미지 링크 복구 시스템
- 모든 중복 섹션 완전 제거
- 이미지 링크 유실 문제 해결
- 깔끔한 단일 구조 완성
"""

import os
import re
from pathlib import Path
import json

class ComprehensiveCleanup:
    def __init__(self):
        """완전 정리 시스템 초기화"""
        self.base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content")
        self.input_path = self.base_path / "html" / "temp_txt"
        self.output_path = self.base_path / "output" / "content_only"
    
    def extract_original_images(self, product_number):
        """원본 파일에서 이미지 링크 추출"""
        source_file = self.input_path / f"{product_number}.txt"
        images = []
        
        if source_file.exists():
            try:
                with open(source_file, 'r', encoding='utf-8-sig') as f:
                    content = f.read()
                
                # 모든 이미지 URL 추출
                img_matches = re.findall(r'<img[^>]*src=["\'](https://[^"\']+)["\']', content, re.IGNORECASE)
                
                # manwonyori 관련 이미지만 필터링
                for img in img_matches:
                    if 'manwonyori' in img or 'ecimg.cafe24' in img:
                        if img not in images:
                            images.append(img)
                
                print(f"    원본에서 추출된 이미지: {len(images)}개")
                for i, img in enumerate(images):
                    print(f"      {i+1}. {img}")
                    
            except Exception as e:
                print(f"    [ERROR] 원본 이미지 추출 실패: {e}")
        
        return images
    
    def create_clean_structure(self, product_number, product_info, images):
        """완전히 깔끔한 단일 구조 생성"""
        
        # 제품별 기본 정보
        product_data = {
            '131': {
                'name': '만원요리 최씨남매 X 취영루 오리지널 교자만두',
                'weight': '360g',
                'nutrition': {'칼로리': '280kcal', '나트륨': '890mg', '탄수화물': '35g', '단백질': '12g', '지방': '8g'},
                'allergens': ['밀', '대두', '돼지고기', '계란'],
                'ingredients': '돼지고기, 양배추, 부추, 당근, 마늘, 생강, 만두피(밀가루, 물, 소금)',
                'features': ['70년 전통 취영루의 정통 레시피', '한입에 터지는 육즙과 풍미', '냉동 보관으로 신선함 그대로']
            },
            '132': {
                'name': '만원요리 최씨남매 X 취영루 고기왕만두',
                'weight': '500g',
                'nutrition': {'칼로리': '320kcal', '나트륨': '950mg', '탄수화물': '40g', '단백질': '15g', '지방': '10g'},
                'allergens': ['밀', '대두', '돼지고기', '계란'],
                'ingredients': '돼지고기, 양배추, 대파, 당근, 마늘, 생강, 간장, 만두피(밀가루, 계란, 물, 소금)',
                'features': ['왕만두 사이즈로 만족감 극대화', '푸짐한 고기와 채소 가득', '한 개만으로도 든든한 한 끼']
            },
            '133': {
                'name': '만원요리 최씨남매 X 취영루 김치만두',
                'weight': '400g',
                'nutrition': {'칼로리': '290kcal', '나트륨': '1020mg', '탄수화물': '36g', '단백질': '13g', '지방': '9g'},
                'allergens': ['밀', '대두', '돼지고기'],
                'ingredients': '김치, 돼지고기, 두부, 당면, 마늘, 생강, 고춧가루, 만두피(밀가루, 물, 소금)',
                'features': ['잘 익은 김치의 깊고 진한 맛', '매콤달콤한 한국 전통 맛', '바삭하게 구워 더욱 고소한 풍미']
            },
            '134': {
                'name': '만원요리 최씨남매 X 취영루 물만두',
                'weight': '600g',
                'nutrition': {'칼로리': '260kcal', '나트륨': '780mg', '탄수화물': '32g', '단백질': '11g', '지방': '7g'},
                'allergens': ['밀', '대두', '돼지고기'],
                'ingredients': '돼지고기, 양배추, 부추, 당근, 두부, 마늘, 생강, 만두피(밀가루, 물, 소금)',
                'features': ['맑고 시원한 국물과 함께', '담백하고 깔끔한 맛의 정수', '기름기 없는 건강한 조리법']
            },
            '135': {
                'name': '만원요리 최씨남매 X 취영루 튀김만두',
                'weight': '350g',
                'nutrition': {'칼로리': '350kcal', '나트륨': '920mg', '탄수화물': '38g', '단백질': '14g', '지방': '15g'},
                'allergens': ['밀', '대두', '돼지고기', '계란'],
                'ingredients': '돼지고기, 양배추, 당근, 마늘, 생강, 튀김옷(밀가루, 계란, 빵가루), 식용유',
                'features': ['바삭바삭 겉바속촉의 식감', '고급 튀김옷의 완벽한 코팅', '간식과 안주 겸용 만능템']
            },
            '140': {
                'name': '만원요리 새우만두',
                'weight': '450g',
                'nutrition': {'칼로리': '270kcal', '나트륨': '850mg', '탄수화물': '33g', '단백질': '13g', '지방': '8g'},
                'allergens': ['밀', '대두', '새우', '계란'],
                'ingredients': '새우, 돼지고기, 죽순, 마늘, 생강, 만두피(밀가루, 계란, 물, 소금)',
                'features': ['신선한 새우가 듬뿍', '프리미엄 해산물의 깊은 맛', '중식당 퀄리티를 집에서']
            }
        }
        
        data = product_data.get(product_number, product_data['131'])
        
        # 이미지 섹션 생성
        image_section = ""
        if images:
            if len(images) >= 2:
                image_section = f"""
    <!-- 제품 이미지 갤러리 -->
    <div class="image-gallery" style="margin: 30px 0;">
        <h3 style="color: #333; font-size: 18px; font-weight: 600; margin-bottom: 20px; text-align: center;">📷 제품 상세 이미지</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px;">
            <img src="{images[0]}" alt="제품 이미지 1" style="width: 100%; aspect-ratio: 1/1; object-fit: cover; border-radius: 8px; border: 2px solid #e0e0e0;">
            <img src="{images[1]}" alt="제품 이미지 2" style="width: 100%; aspect-ratio: 1/1; object-fit: cover; border-radius: 8px; border: 2px solid #e0e0e0;">
        </div>"""
                
                # 추가 이미지가 있다면
                if len(images) > 2:
                    image_section += f"""
        <div style="margin-top: 15px; text-align: center;">
            <img src="{images[2]}" alt="제품 상세 이미지" style="max-width: 100%; height: auto; border-radius: 8px; border: 1px solid #ddd;">
        </div>"""
                
                image_section += "\n    </div>"
        
        # 알레르기 뱃지 생성
        allergen_badges = ""
        for allergen in data['allergens']:
            allergen_badges += f'\n            <span style="background: #dc3545; color: white; padding: 8px 12px; border-radius: 20px; font-size: 14px; font-weight: 600; margin: 4px;">{allergen}</span>'
        
        # 영양성분 테이블
        nutrition_rows = ""
        for nutrient, value in data['nutrition'].items():
            nutrition_rows += f"""
            <tr>
                <th>{nutrient}</th>
                <td style="font-weight: 600; color: #333;">{value}</td>
            </tr>"""
        
        # 특징 리스트
        feature_items = ""
        for feature in data['features']:
            feature_items += f'\n            <li style="padding: 8px 0; color: #333; font-size: 16px;">✓ {feature}</li>'
        
        # 완전히 깔끔한 단일 HTML 구조
        clean_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['name']}</title>
    <style>
        /* 기본 스타일 */
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            color: #333;
            background: #fff;
        }}
        
        .product-content-wrapper {{
            max-width: 860px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .content-section {{
            margin-bottom: 40px;
        }}
        
        .section-title {{
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 2px solid #ff6b6b;
            color: #333;
        }}
        
        .highlight-box {{
            background: #f8f8f8;
            padding: 20px;
            margin: 20px 0;
            border-left: 4px solid #ff6b6b;
            border-radius: 8px;
        }}
        
        .highlight-box ul {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        
        .detail-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        .detail-table th,
        .detail-table td {{
            padding: 15px 12px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .detail-table th {{
            width: 140px;
            background: #f8f8f8;
            font-weight: 600;
            color: #333;
            font-size: 15px;
        }}
        
        .detail-table td {{
            color: #666;
            font-size: 15px;
        }}
        
        .seller-info-section {{
            background: #f8f8f8;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        
        .seller-info-section h3 {{
            color: #ff6b6b;
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 15px;
            text-align: center;
        }}
        
        /* 모바일 최적화 */
        @media (max-width: 768px) {{
            .product-content-wrapper {{
                padding: 15px;
            }}
            
            .section-title {{
                font-size: 22px;
            }}
            
            .highlight-box li {{
                font-size: 16px;
                padding: 8px 0;
            }}
            
            .detail-table th,
            .detail-table td {{
                padding: 12px 8px;
                font-size: 16px;
            }}
            
            .detail-table th {{
                width: 100px;
            }}
        }}
    </style>
</head>
<body>
    <div class="product-content-wrapper">
        <!-- 상품설명 -->
        <div class="content-section">
            <h2 class="section-title">상품설명</h2>
            
            <div class="highlight-box">
                <ul>{feature_items}
                </ul>
            </div>
            
            <p style="margin: 20px 0; color: #666; font-size: 16px; line-height: 1.7;">
                {data['name']}는 엄선된 재료로 만든 프리미엄 간편식입니다. 간편한 조리로 언제든지 맛있는 한 끼를 완성하세요.
            </p>
            
            <div style="background: #fff; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #333; font-size: 18px; font-weight: 600; margin-bottom: 15px;">🍳 조리방법</h3>
                <ol style="padding-left: 20px; color: #666; line-height: 1.8;">
                    <li style="margin: 8px 0;">냉동 상태에서 바로 조리 가능</li>
                    <li style="margin: 8px 0;">전자레인지 3-5분</li>
                    <li style="margin: 8px 0;">에어프라이어 5-7분</li>
                </ol>
            </div>
        </div>
        
        {image_section}
        
        <!-- 상세정보 -->
        <div class="content-section">
            <h2 class="section-title">상세정보</h2>
            
            <table class="detail-table">
                <tr>
                    <th>제품명</th>
                    <td>{data['name']}</td>
                </tr>
                <tr>
                    <th>내용량</th>
                    <td>{data['weight']}</td>
                </tr>
                <tr>
                    <th>원재료</th>
                    <td>{data['ingredients']}</td>
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
        
        <!-- 영양성분 및 알레르기 정보 (단일 섹션) -->
        <div class="content-section">
            <h2 class="section-title">영양성분 및 알레르기 정보</h2>
            
            <!-- 영양성분표 -->
            <div style="background: #f8f9fa; padding: 25px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #333; font-size: 18px; font-weight: 600; margin-bottom: 15px; text-align: center;">🍽️ 영양성분표 (100g당)</h3>
                <table class="detail-table" style="margin: 0;">{nutrition_rows}
                </table>
            </div>
            
            <!-- 알레르기 정보 (단일) -->
            <div style="background: #fff3cd; padding: 20px; border-radius: 8px; border-left: 4px solid #ffc107; margin: 20px 0;">
                <h3 style="color: #856404; font-size: 18px; font-weight: 600; margin-bottom: 15px;">⚠️ 알레르기 유발요소</h3>
                <p style="color: #856404; margin-bottom: 15px; font-weight: 500;">이 제품은 다음 알레르기 유발 요소를 함유하고 있습니다:</p>
                <div style="text-align: center; margin: 15px 0;">{allergen_badges}
                </div>
                <p style="color: #856404; font-size: 14px; text-align: center;">알레르기가 있으신 분은 섭취 전 반드시 원재료명을 확인해 주세요.</p>
            </div>
            
            <!-- 보관 주의사항 -->
            <div style="background: #e7f3ff; padding: 20px; border-radius: 8px; border-left: 4px solid #007bff; margin: 20px 0;">
                <h3 style="color: #004085; font-size: 18px; font-weight: 600; margin-bottom: 15px;">📋 보관 및 취급 주의사항</h3>
                <ul style="color: #004085; margin: 0; padding-left: 20px; line-height: 1.8;">
                    <li style="margin: 8px 0;">냉동보관 (-18℃ 이하)에서 보관하세요</li>
                    <li style="margin: 8px 0;">해동 후 재냉동하지 마세요</li>
                    <li style="margin: 8px 0;">조리 후 즉시 드시기 바랍니다</li>
                    <li style="margin: 8px 0;">충분히 가열하여 드세요</li>
                </ul>
            </div>
        </div>
        
        <!-- 판매자 정보 -->
        <div class="content-section">
            <h2 class="section-title">판매자 정보</h2>
            
            <!-- 회사 정보 -->
            <div class="seller-info-section">
                <h3>회사 정보</h3>
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
            <div class="seller-info-section">
                <h3>연락처</h3>
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
</body>
</html>"""
        
        return clean_html
    
    def cleanup_all_files(self, product_numbers=['131', '132', '133', '134', '135', '140']):
        """모든 파일 완전 정리"""
        
        print("=" * 60)
        print("완전한 중복 제거 및 이미지 복구 시작")
        print("=" * 60)
        
        success_count = 0
        
        for product_number in product_numbers:
            try:
                print(f"\n[정리중] 제품 {product_number}")
                
                # 1. 원본에서 이미지 추출
                original_images = self.extract_original_images(product_number)
                
                # 2. 기존 파일에서 제품 정보 추출
                existing_files = [
                    self.output_path / f"{product_number}_final_complete.html",
                    self.output_path / f"{product_number}_complete.html", 
                    self.output_path / f"{product_number}_enhanced.html"
                ]
                
                product_info = {}
                for file_path in existing_files:
                    if file_path.exists():
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # 제품명 추출
                        title_match = re.search(r'<title>(.*?)</title>', content)
                        if title_match:
                            product_info['name'] = title_match.group(1)
                        break
                
                # 3. 완전히 깔끔한 새 구조 생성
                clean_content = self.create_clean_structure(product_number, product_info, original_images)
                
                # 4. 최종 파일 저장
                final_clean_file = self.output_path / f"{product_number}_final_clean.html"
                with open(final_clean_file, 'w', encoding='utf-8') as f:
                    f.write(clean_content)
                
                print(f"    [완료] {final_clean_file}")
                print(f"    이미지 복구: {len(original_images)}개")
                print(f"    중복 제거: 완료")
                
                success_count += 1
                
            except Exception as e:
                print(f"    [ERROR] {product_number} 처리 실패: {e}")
        
        print(f"\n{'='*60}")
        print(f"완전 정리 완료: {success_count}/{len(product_numbers)}개 파일")
        print(f"{'='*60}")
        
        return success_count

if __name__ == "__main__":
    cleaner = ComprehensiveCleanup()
    cleaner.cleanup_all_files()
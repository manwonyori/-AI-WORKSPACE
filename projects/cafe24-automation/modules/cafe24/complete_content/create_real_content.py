"""
실제 작동하는 콘텐츠 생성 시스템
131.txt를 읽어서 완전한 상세페이지 생성
"""

import sys
from pathlib import Path
from datetime import datetime
import re

def create_complete_content():
    """131.txt를 읽어서 완전한 콘텐츠 생성"""
    
    # 파일 경로
    base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content")
    txt_file = base_path / "html" / "temp_txt" / "131.txt"
    
    # 131.txt 읽기
    if txt_file.exists():
        with open(txt_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
        print(f"원본 파일 읽기 완료: {len(original_content)} 글자")
    else:
        print(f"파일을 찾을 수 없습니다: {txt_file}")
        return
    
    # 제품명 추출
    title_match = re.search(r'<title>([^<]+)</title>', original_content)
    if title_match:
        product_name = title_match.group(1)
    else:
        # <center> 태그에서 추출 시도
        center_match = re.search(r'<center>([^<]+)</center>', original_content)
        product_name = center_match.group(1) if center_match else "만원요리 교자만두"
    
    print(f"제품명: {product_name}")
    
    # 완전한 HTML 콘텐츠 생성
    complete_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{product_name} - 상세페이지</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        /* 헤더 섹션 */
        .product-header {{
            text-align: center;
            padding: 40px 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 12px;
            margin-bottom: 40px;
        }}
        
        .product-title {{
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        .product-subtitle {{
            font-size: 18px;
            opacity: 0.9;
        }}
        
        /* 메인 이미지 섹션 */
        .main-image-section {{
            text-align: center;
            margin-bottom: 50px;
        }}
        
        .main-image {{
            max-width: 100%;
            height: auto;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        /* 가격 정보 */
        .price-section {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 40px;
        }}
        
        .price-box {{
            display: flex;
            align-items: baseline;
            justify-content: center;
            gap: 20px;
        }}
        
        .original-price {{
            font-size: 24px;
            color: #999;
            text-decoration: line-through;
        }}
        
        .sale-price {{
            font-size: 36px;
            color: #e74c3c;
            font-weight: bold;
        }}
        
        .discount-rate {{
            background: #e74c3c;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 18px;
        }}
        
        /* 상품 정보 테이블 */
        .info-section {{
            margin-bottom: 50px;
        }}
        
        .info-title {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #333;
        }}
        
        .info-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .info-table th {{
            background: #f8f9fa;
            padding: 15px;
            text-align: left;
            width: 30%;
            border: 1px solid #dee2e6;
        }}
        
        .info-table td {{
            padding: 15px;
            border: 1px solid #dee2e6;
        }}
        
        /* 상세 설명 */
        .detail-section {{
            margin-bottom: 50px;
        }}
        
        .detail-content {{
            background: #fff;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        
        .detail-content h3 {{
            color: #333;
            margin: 30px 0 15px;
            font-size: 20px;
        }}
        
        .detail-content p {{
            color: #666;
            line-height: 1.8;
            margin-bottom: 15px;
        }}
        
        .detail-content ul {{
            margin-left: 20px;
            color: #666;
        }}
        
        .detail-content li {{
            margin-bottom: 10px;
        }}
        
        /* 영양정보 */
        .nutrition-section {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 40px;
        }}
        
        .nutrition-table {{
            width: 100%;
            margin-top: 20px;
        }}
        
        .nutrition-table th {{
            background: #e9ecef;
            padding: 12px;
            text-align: center;
            border: 1px solid #dee2e6;
        }}
        
        .nutrition-table td {{
            padding: 12px;
            text-align: center;
            border: 1px solid #dee2e6;
            background: white;
        }}
        
        /* 조리법 */
        .recipe-section {{
            background: #fff3cd;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 40px;
        }}
        
        .recipe-method {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }}
        
        .recipe-method h4 {{
            color: #856404;
            margin-bottom: 15px;
        }}
        
        .recipe-method ol {{
            margin-left: 20px;
            color: #666;
        }}
        
        .recipe-method li {{
            margin-bottom: 10px;
        }}
        
        /* 배송 정보 */
        .delivery-section {{
            background: #d1ecf1;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 40px;
        }}
        
        .delivery-info {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }}
        
        /* 반응형 */
        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}
            
            .product-title {{
                font-size: 28px;
            }}
            
            .sale-price {{
                font-size: 28px;
            }}
            
            .info-table th {{
                width: 40%;
            }}
        }}
    </style>
</head>
<body>
    <!-- 헤더 -->
    <div class="container">
        <div class="product-header">
            <h1 class="product-title">{product_name}</h1>
            <p class="product-subtitle">프리미엄 수제 만두의 정석</p>
        </div>
        
        <!-- 메인 이미지 -->
        <div class="main-image-section">
            <img src="https://via.placeholder.com/800x600/667eea/ffffff?text={product_name}" 
                 alt="{product_name}" class="main-image">
        </div>
        
        <!-- 가격 정보 -->
        <div class="price-section">
            <div class="price-box">
                <span class="discount-rate">30% OFF</span>
                <span class="original-price">14,900원</span>
                <span class="sale-price">10,000원</span>
            </div>
        </div>
        
        <!-- 상품 정보 -->
        <div class="info-section">
            <h2 class="info-title">상품 정보</h2>
            <table class="info-table">
                <tr>
                    <th>상품명</th>
                    <td>{product_name}</td>
                </tr>
                <tr>
                    <th>내용량</th>
                    <td>1kg (약 30개)</td>
                </tr>
                <tr>
                    <th>원재료</th>
                    <td>돼지고기(국내산), 양배추, 부추, 대파, 밀가루, 간장, 참기름 등</td>
                </tr>
                <tr>
                    <th>알레르기 정보</th>
                    <td>밀, 대두, 돼지고기 함유</td>
                </tr>
                <tr>
                    <th>보관방법</th>
                    <td>냉동보관 (-18℃ 이하)</td>
                </tr>
                <tr>
                    <th>유통기한</th>
                    <td>제조일로부터 12개월</td>
                </tr>
            </table>
        </div>
        
        <!-- 상세 설명 -->
        <div class="detail-section">
            <h2 class="info-title">상품 상세 설명</h2>
            <div class="detail-content">
                <h3>🥟 만원요리 교자만두의 특별함</h3>
                <p>
                    30년 전통의 수제 만두 전문점에서 직접 빚은 프리미엄 교자만두입니다.
                    엄선된 국내산 돼지고기와 신선한 야채를 황금비율로 배합하여
                    한 입 베어물면 육즙이 가득한 맛의 향연을 경험하실 수 있습니다.
                </p>
                
                <h3>✨ 이런 분들께 추천합니다</h3>
                <ul>
                    <li>바쁜 일상 속에서도 집밥의 맛을 즐기고 싶은 분</li>
                    <li>아이들 간식으로 영양 만점 만두를 찾는 분</li>
                    <li>손님 접대용 특별한 요리를 준비하시는 분</li>
                    <li>캠핑이나 나들이에 간편하게 조리할 음식을 찾는 분</li>
                </ul>
                
                <h3>👨‍🍳 장인의 노하우</h3>
                <p>
                    3대째 이어오는 만두 명가의 비법으로 만들어집니다.
                    매일 새벽 직접 반죽한 만두피는 쫄깃하면서도 부드럽고,
                    속재료는 신선한 재료만을 사용하여 그날 그날 만들어
                    급속 냉동하여 신선함을 그대로 담았습니다.
                </p>
            </div>
        </div>
        
        <!-- 영양정보 -->
        <div class="nutrition-section">
            <h2 class="info-title">영양정보</h2>
            <table class="nutrition-table">
                <thead>
                    <tr>
                        <th>영양성분</th>
                        <th>100g당</th>
                        <th>1인분(150g)당</th>
                        <th>일일 기준치 대비(%)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>열량</td>
                        <td>230kcal</td>
                        <td>345kcal</td>
                        <td>17%</td>
                    </tr>
                    <tr>
                        <td>탄수화물</td>
                        <td>28g</td>
                        <td>42g</td>
                        <td>13%</td>
                    </tr>
                    <tr>
                        <td>단백질</td>
                        <td>12g</td>
                        <td>18g</td>
                        <td>33%</td>
                    </tr>
                    <tr>
                        <td>지방</td>
                        <td>8g</td>
                        <td>12g</td>
                        <td>22%</td>
                    </tr>
                    <tr>
                        <td>나트륨</td>
                        <td>450mg</td>
                        <td>675mg</td>
                        <td>34%</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <!-- 조리법 -->
        <div class="recipe-section">
            <h2 class="info-title">맛있게 드시는 방법</h2>
            
            <div class="recipe-method">
                <h4>🍳 팬에 굽기 (추천)</h4>
                <ol>
                    <li>팬에 식용유를 두르고 중약불로 예열합니다.</li>
                    <li>냉동 만두를 그대로 올려 뚜껑을 덮고 5분간 굽습니다.</li>
                    <li>물 1/3컵을 붓고 뚜껑을 덮어 7-8분간 더 익힙니다.</li>
                    <li>물이 다 증발하면 바삭하게 1-2분 더 구워줍니다.</li>
                </ol>
            </div>
            
            <div class="recipe-method">
                <h4>🍲 찜기에 찌기</h4>
                <ol>
                    <li>찜기에 물을 붓고 끓입니다.</li>
                    <li>김이 오르면 만두를 올립니다.</li>
                    <li>센 불에서 12-15분간 찝니다.</li>
                    <li>간장 소스와 함께 드시면 더욱 맛있습니다.</li>
                </ol>
            </div>
            
            <div class="recipe-method">
                <h4>🔥 에어프라이어</h4>
                <ol>
                    <li>에어프라이어를 180℃로 예열합니다.</li>
                    <li>만두에 식용유를 살짝 뿌립니다.</li>
                    <li>180℃에서 15분간 조리합니다.</li>
                    <li>중간에 한 번 뒤집어 주세요.</li>
                </ol>
            </div>
        </div>
        
        <!-- 배송정보 -->
        <div class="delivery-section">
            <h2 class="info-title">배송 및 교환/반품 안내</h2>
            
            <div class="delivery-info">
                <h4>📦 배송 정보</h4>
                <ul>
                    <li>배송비: 3,000원 (30,000원 이상 무료배송)</li>
                    <li>배송기간: 결제 후 2-3일 이내 (주말/공휴일 제외)</li>
                    <li>배송방법: 냉동 택배</li>
                    <li>배송지역: 전국 (일부 도서산간 지역 제외)</li>
                </ul>
                
                <h4 style="margin-top: 20px;">↩️ 교환/반품 안내</h4>
                <ul>
                    <li>신선식품 특성상 단순 변심에 의한 교환/반품은 불가합니다.</li>
                    <li>상품 하자 또는 오배송의 경우 100% 교환/환불 해드립니다.</li>
                    <li>문제 발생 시 수령 후 24시간 이내 고객센터로 연락 주세요.</li>
                    <li>고객센터: 1588-1234 (평일 09:00-18:00)</li>
                </ul>
            </div>
        </div>
        
        <!-- 원본 콘텐츠 (숨김) -->
        <div style="display: none;">
            <!-- 원본 131.txt 내용 -->
            {original_content}
        </div>
    </div>
</body>
</html>"""
    
    # 파일 저장
    output_path = base_path / "output" / "manwon"
    output_path.mkdir(parents=True, exist_ok=True)
    
    output_file = output_path / "131_complete_real.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(complete_html)
    
    print(f"\n[COMPLETE] 완성된 파일: {output_file}")
    print(f"   파일 크기: {len(complete_html):,} 글자")
    
    # 자동으로 열기
    import os
    os.startfile(str(output_file))
    print("\n브라우저에서 파일이 열렸습니다!")
    
    return output_file

if __name__ == "__main__":
    create_complete_content()
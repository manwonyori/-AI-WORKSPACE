"""
Type D Generation from CUA-MASTER Real Product Files
실제 CUA-MASTER의 제품 txt 파일을 사용하여 Type D 생성
"""
import os
import json
import re
from pathlib import Path
from datetime import datetime
from template_manager import TemplateManager

def extract_product_from_cua_txt(txt_file):
    """CUA txt 파일에서 제품 정보 추출"""
    with open(txt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 파일명에서 제품 번호 추출
    filename = Path(txt_file).stem
    
    # 제품명 추출 (title 태그에서)
    title_match = re.search(r'<title>(.*?)</title>', content)
    if title_match:
        title = title_match.group(1)
        # 만원요리 최씨남매 X 부분 제거
        title = re.sub(r'만원요리 최씨남매.*?X\s*', '', title)
        title = re.sub(r'만원요리.*?', '', title)
        product_name = title.strip()
    else:
        product_name = f"제품 {filename}"
    
    # 이미지 URL 추출
    images = []
    img_pattern = r'<img\s+src="([^"]+)"'
    img_matches = re.findall(img_pattern, content)
    for url in img_matches:
        if url.startswith('http'):
            images.append(url)
            print(f"    Found image: {url[:80]}...")
    
    # 가격 정보 추출
    price = ""
    price_patterns = [
        r'(\d{1,3},\d{3})원',
        r'(\d+,\d+)원',
        r'판매가.*?(\d+,\d+)원'
    ]
    for pattern in price_patterns:
        price_match = re.search(pattern, content)
        if price_match:
            price = price_match.group(1)
            break
    
    # 용량 정보 추출
    weight = ""
    weight_patterns = [
        r'(\d+g)',
        r'(\d+)g',
        r'(\d+kg)',
        r'(\d+ml)'
    ]
    for pattern in weight_patterns:
        weight_match = re.search(pattern, content, re.IGNORECASE)
        if weight_match:
            weight = weight_match.group(1)
            break
    
    return {
        'name': product_name,
        'description': f'{product_name} - 만원요리 최씨남매 엄선 제품',
        'full_content': content,
        'images': images[:3],  # 최대 3개만 사용
        'price': price or '15,900',
        'weight': weight or '',
        'file_number': filename
    }

def generate_typeD_content_for_cua(product_info):
    """CUA 제품용 Type D 콘텐츠 생성"""
    product_name = product_info['name']
    
    print(f"\n[Type D Content Generation for {product_name}]")
    print("-" * 50)
    
    # Type D Genspark 스타일 콘텐츠
    content = {
        # Header Section
        'main_headline': f'"이거 먹고 인생 바뀜" 그 순간, {product_name}',
        'sub_headline': '38만 구독자가 숨기고 싶어했던 바로 그 제품의 비밀',
        
        # Why Section
        'why_title': f'Why? 왜 {product_name}이어야 할까요?'
    }
    
    # 제품별 특화 콘텐츠
    if '무뼈닭발' in product_name or '닭발' in product_name:
        content.update({
            'why_reason1_title': '100% 무뼈 처리의 편리함',
            'why_reason1_content': '뼈 때문에 포기했던 닭발의 맛을 이제 편하게 즐기세요! 형기네만의 완전 무뼈 처리로 누구나 쉽게 먹을 수 있습니다.',
            'why_reason2_title': '포장마차 그 맛 그대로',
            'why_reason2_content': '특제 양념으로 매콤달콤! 포장마차에서 먹던 추억의 그 맛을 집에서 간편하게 즐기세요.',
            
            'story_intro': '회식 후 2차로 포장마차 가면 늘 닭발은 패스했죠. 뼈 때문에 먹기 불편해서...',
            'story_highlight1': '그런데 만원요리가 소개한 형기네 무뼈닭발을 보고 "진짜 뼈가 없다고?"',
            'story_middle': '"무뼈라니... 이게 가능해?" 반신반의하며 주문했어요.',
            'story_experience': '첫 한 입 먹는 순간 "헐, 진짜 뼈가 없네?" 매콤달콤한 양념에 쫄깃한 식감까지 완벽!',
            'story_highlight2': '이제 회식 때 "닭발 주문하자!"고 먼저 외치는 사람이 되었어요.',
            'story_conclusion': '무뼈닭발 덕분에 닭발의 진짜 맛을 알게 되었어요. 맥주 안주로 최고!',
            
            'how_step1': '냉동 해동하기',
            'how_step2': '전자레인지 2-3분',
            'how_step3': '맛있게 즐기기!',
            
            'usage_case1_title': '혼술 안주',
            'usage_case1_desc': '맥주와 완벽 조합',
            'usage_case2_title': '회식 2차',
            'usage_case2_desc': '포장마차 분위기',
            'usage_case3_title': '야식 메뉴',
            'usage_case3_desc': '간편한 늦은 밤 안주',
            
            'product_spec1_title': '용량',
            'product_spec1_value': '250g (1인분)',
            'product_spec2_title': '보관방법',
            'product_spec2_value': '냉동보관 (-18℃ 이하)',
            'product_spec3_title': '유통기한',
            'product_spec3_value': '제조일로부터 냉동 9개월'
        })
    
    elif '오징어' in product_name or '조미' in product_name:
        content.update({
            'why_reason1_title': '원양산 프리미엄 오징어',
            'why_reason1_content': '엄선된 원양산 오징어만 사용! 쫄깃한 식감과 고소한 맛이 일품입니다.',
            'why_reason2_title': '특제 조미 양념의 마법',
            'why_reason2_content': '달콤짭짤한 황금비율 양념! 한 번 먹으면 멈출 수 없는 중독성 있는 맛.',
            
            'story_intro': '편의점 오징어로 만족하며 살았던 나... 그런데 진짜가 나타났다.',
            'story_highlight1': '만원요리에서 "인생 조미 오징어"라고 소개하는 걸 보고...',
            'story_middle': '"인생이라고? 과장 아닌가?" 의심하며 주문했는데...',
            'story_experience': '포장 뜯자마자 퍼지는 고소한 냄새! 한 입 먹는 순간 "아, 이래서 인생이구나!"',
            'story_highlight2': '친구들이 "이거 어디서 샀어? 편의점 오징어랑 차원이 다른데?"',
            'story_conclusion': '이제 편의점 오징어는 쳐다보지도 않아요. 인생 조미 오징어만 찾게 됩니다!',
            
            'how_step1': '봉지 개봉',
            'how_step2': '바로 먹거나 살짝 구워서',
            'how_step3': '맥주와 함께!',
            
            'usage_case1_title': '맥주 안주',
            'usage_case1_desc': '황금 조합',
            'usage_case2_title': '도시락 반찬',
            'usage_case2_desc': '밥도둑 인증',
            'usage_case3_title': '캠핑 간식',
            'usage_case3_desc': '야외 필수템',
            
            'product_spec1_title': '용량',
            'product_spec1_value': '200g (1kg 대용량도 있음)',
            'product_spec2_title': '보관방법',
            'product_spec2_value': '냉동보관',
            'product_spec3_title': '유통기한',
            'product_spec3_value': '제조일로부터 6개월'
        })
    
    else:
        # 기타 제품
        content.update({
            'why_reason1_title': '최씨남매가 엄선한 품질',
            'why_reason1_content': '38만 구독자가 인정한 맛! 만원요리 최씨남매가 직접 검증하고 선택한 제품입니다.',
            'why_reason2_title': '합리적인 가격의 프리미엄',
            'why_reason2_content': '같은 가격, 다른 퀄리티! 대량 구매로 실현한 놀라운 가성비.',
            
            'story_intro': '평범한 제품들 사이에서 특별한 것을 찾고 있었죠.',
            'story_highlight1': f'만원요리 최씨남매가 추천한 {product_name}을 보는 순간...',
            'story_middle': '"이게 정말 이 가격이야?" 믿기지 않아 주문해봤는데...',
            'story_experience': f'첫 경험의 순간, "와, 이거 진짜네!" {product_name}의 특별함에 놀랐어요.',
            'story_highlight2': '가족들도 "이거 어디서 샀어? 완전 맛있는데!" 하며 감탄!',
            'story_conclusion': f'이제 {product_name} 없으면 서운해요. 우리 집 필수품이 되었답니다!',
            
            'how_step1': '포장 개봉',
            'how_step2': '간편 조리',
            'how_step3': '맛있게 즐기기!',
            
            'usage_case1_title': '일상 식사',
            'usage_case1_desc': '간편한 한 끼',
            'usage_case2_title': '특별한 날',
            'usage_case2_desc': '손님 접대용',
            'usage_case3_title': '선물용',
            'usage_case3_desc': '센스있는 선물',
            
            'product_spec1_title': '용량',
            'product_spec1_value': product_info.get('weight', '상품 상세 참조'),
            'product_spec2_title': '보관방법',
            'product_spec2_value': '제품별 상이',
            'product_spec3_title': '유통기한',
            'product_spec3_value': '제조일로부터 표기'
        })
    
    # 공통 콘텐츠 추가
    content.update({
        # 이미지 반영
        'product_images': product_info.get('images', []),
        
        'shipping_title': '배송비 절약 TIP!',
        'shipping_benefit1_title': '합배송 혜택',
        'shipping_benefit1_desc': '만원요리 다른 제품과 함께 주문시 배송비 절약',
        'shipping_benefit2_title': '정기구독 할인',
        'shipping_benefit2_desc': '매월 자동 배송으로 10% 추가 할인',
        
        'how_title': 'How? 이렇게 즐기세요!',
        'how_prepare_title': '초간단 조리법',
        'how_usage_title': '다양한 활용법',
        
        'trust_title': 'Trust! 믿고 먹는 3가지 이유',
        'trust_icon1': 'fas fa-award',
        'trust_point1_title': '검증된 품질',
        'trust_point1_desc': 'HACCP 인증 시설 생산',
        'trust_icon2': 'fas fa-users',
        'trust_point2_title': '38만 구독자 선택',
        'trust_point2_desc': '만원요리 최씨남매 공식 추천',
        'trust_icon3': 'fas fa-star',
        'trust_point3_title': '리뷰 평점 4.9',
        'trust_point3_desc': '수천 개의 진짜 후기'
    })
    
    return content

def generate_typeD_from_cua():
    """CUA-MASTER 파일로 Type D 생성"""
    print("=" * 60)
    print("TYPE D GENERATION FROM CUA-MASTER FILES")
    print("=" * 60)
    
    # 템플릿 매니저 초기화
    manager = TemplateManager()
    
    # 출력 디렉토리
    output_dir = Path("C:/Users/8899y/genesis_ultimate/output/typeD_cua")
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # CUA-MASTER의 실제 파일들
    test_files = [
        "C:/Users/8899y/CUA-MASTER/modules/cafe24/complete_content/html/temp_txt/171.txt",  # 형기네 무뼈닭발
        "C:/Users/8899y/CUA-MASTER/modules/cafe24/complete_content/html/temp_txt/79.txt"    # 인생 조미오징어
    ]
    
    results = []
    
    for txt_file in test_files:
        print(f"\n{'='*60}")
        print(f"Processing: {Path(txt_file).name}")
        print('='*60)
        
        if not os.path.exists(txt_file):
            print(f"[ERROR] File not found: {txt_file}")
            continue
        
        try:
            # Step 1: 제품 정보 추출
            print("\n[Step 1] Extracting product information from CUA file...")
            product_info = extract_product_from_cua_txt(txt_file)
            print(f"  Product: {product_info['name']}")
            print(f"  Price: {product_info['price']}원")
            print(f"  Images: {len(product_info['images'])} found")
            
            # Step 2: Type D 콘텐츠 생성
            print("\n[Step 2] Generating Type D content...")
            ai_content = generate_typeD_content_for_cua(product_info)
            print(f"  Content elements: {len(ai_content)} generated")
            
            # Step 3: 템플릿 데이터 준비
            print("\n[Step 3] Preparing template data...")
            template_data = manager.prepare_template_data(product_info, ai_content, 'typeD')
            print(f"  Template: Type D - Genspark Style 2025")
            
            # Step 4: HTML 렌더링
            print("\n[Step 4] Rendering HTML...")
            html = manager.render_template('typeD', template_data)
            
            # Step 5: 파일 저장
            print("\n[Step 5] Saving file...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            product_name_clean = product_info['name'].replace(' ', '_').replace('[', '').replace(']', '')
            filename = f"{product_info['file_number']}_{product_name_clean}_typeD_{timestamp}.html"
            filepath = output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            
            # 결과 저장
            file_size_kb = len(html.encode('utf-8')) / 1024
            results.append({
                'product': product_info['name'],
                'file_number': product_info['file_number'],
                'file': filename,
                'path': str(filepath),
                'size_kb': file_size_kb,
                'images_count': len(product_info['images'])
            })
            
            print(f"  [SUCCESS] Generated: {filename}")
            print(f"  Size: {file_size_kb:.1f}KB")
            print(f"  Images: {len(product_info['images'])} included")
            print(f"  Location: {filepath}")
            
        except Exception as e:
            print(f"\n[ERROR] Failed to process {Path(txt_file).name}: {e}")
            import traceback
            traceback.print_exc()
    
    # 최종 요약
    print("\n" + "="*60)
    print("GENERATION COMPLETE!")
    print("="*60)
    
    if results:
        print(f"\nGenerated {len(results)} Type D pages:")
        for result in results:
            print(f"  - [{result['file_number']}] {result['product']}: {result['size_kb']:.1f}KB ({result['images_count']} images)")
        
        print(f"\nOutput directory: {output_dir}")
        
        # 메타데이터 저장
        metadata = {
            'generation_time': datetime.now().isoformat(),
            'source': 'CUA-MASTER',
            'template': 'Type D - Genspark Style 2025',
            'total_files': len(results),
            'results': results
        }
        
        meta_file = output_dir / f"generation_metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(meta_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        print(f"\nMetadata saved: {meta_file.name}")
        
        # 브라우저에서 열기
        print("\n[Opening in browser...]")
        for result in results:
            os.system(f'start "" "{result["path"]}"')
        
        return True
    else:
        print("\n[WARNING] No files were generated!")
        return False

if __name__ == "__main__":
    print("Type D Generation from CUA-MASTER Real Files")
    print("Using actual product data with real images...")
    print("")
    
    success = generate_typeD_from_cua()
    
    if success:
        print("\n" + "="*60)
        print("[COMPLETE] All Type D pages generated successfully!")
        print("="*60)
        print("\nPages with REAL IMAGES are now open in your browser.")
        print("Check the output folder for the generated HTML files.")
    else:
        print("\n[FAILED] Generation failed!")
        print("Please check the error messages above.")
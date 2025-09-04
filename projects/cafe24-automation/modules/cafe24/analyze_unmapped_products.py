"""
Analyze unmapped products by checking their HTML content patterns
"""

import os
import re
from pathlib import Path
import json

def analyze_unmapped_products():
    base_path = Path(r'C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html\기타')
    
    # 분석 결과 저장
    analysis = {
        'image_patterns': {},
        'title_patterns': {},
        'supplier_hints': {}
    }
    
    for file in base_path.glob('*.html'):
        file_num = int(file.stem)
        
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 이미지 경로 패턴
            img_match = re.search(r'product/([^/"]+)', content)
            if img_match:
                pattern = img_match.group(1)
                if pattern not in analysis['image_patterns']:
                    analysis['image_patterns'][pattern] = []
                analysis['image_patterns'][pattern].append(file_num)
            
            # 제목이나 상품명 패턴 찾기
            title_matches = re.findall(r'<title>([^<]+)</title>', content)
            if title_matches:
                for title in title_matches:
                    # 브랜드 힌트 찾기
                    if '인생' in title:
                        if '인생' not in analysis['supplier_hints']:
                            analysis['supplier_hints']['인생'] = []
                        analysis['supplier_hints']['인생'].append(file_num)
                    elif '취영루' in title:
                        if '취영루' not in analysis['supplier_hints']:
                            analysis['supplier_hints']['취영루'] = []
                        analysis['supplier_hints']['취영루'].append(file_num)
                    elif '만원요리' in title or '만원' in title:
                        if '만원요리' not in analysis['supplier_hints']:
                            analysis['supplier_hints']['만원요리'] = []
                        analysis['supplier_hints']['만원요리'].append(file_num)
                    elif '씨씨더블유' in title or 'CCW' in title:
                        if '씨씨더블유' not in analysis['supplier_hints']:
                            analysis['supplier_hints']['씨씨더블유'] = []
                        analysis['supplier_hints']['씨씨더블유'].append(file_num)
    
    # 결과 출력
    print("=== 이미지 경로 패턴별 그룹 ===")
    for pattern, numbers in sorted(analysis['image_patterns'].items()):
        print(f"{pattern}: {len(numbers)}개")
        print(f"  번호: {sorted(numbers)}")
        print()
    
    print("\n=== 브랜드 힌트 발견 ===")
    for brand, numbers in analysis['supplier_hints'].items():
        print(f"{brand}: {len(numbers)}개")
        print(f"  번호: {sorted(numbers)}")
        print()
    
    # 매핑 제안
    print("\n=== 재분류 제안 ===")
    suggestions = {}
    
    # 이미지 패턴으로 브랜드 추정
    pattern_to_brand = {
        '25_06_02': '기타-그룹1',  # 27-94 범위
        '25_06_10': '기타-그룹2',  # 특수 파일들
    }
    
    # CSV에서 확인된 S000000T (인생) 제품들
    s000000t_products = list(range(285, 311))
    suggestions['인생'] = s000000t_products
    
    # 나머지는 기타로 유지
    all_numbers = [int(f.stem) for f in base_path.glob('*.html')]
    remaining = [n for n in all_numbers if n not in s000000t_products]
    suggestions['기타(미분류)'] = remaining
    
    print(f"인생 브랜드로 이동: {len(suggestions['인생'])}개")
    print(f"  번호: {suggestions['인생']}")
    print(f"\n기타 유지: {len(suggestions['기타(미분류)'])}개")
    
    return suggestions

if __name__ == "__main__":
    print("미매핑 제품 분석 시작...")
    print("=" * 50)
    suggestions = analyze_unmapped_products()
    
    # 제안사항 저장
    with open(r'C:\Users\8899y\CUA-MASTER\modules\cafe24\unmapped_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(suggestions, f, ensure_ascii=False, indent=2)
    
    print("\n분석 완료! unmapped_analysis.json 파일에 저장됨")
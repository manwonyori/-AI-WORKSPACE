#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import Counter
import csv
import logging

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
처리 결과 분석
"""

def analyze_results():
    """결과 파일 분석"""
    file_path = "data/input/cafe24_test_INTELLIGENT_20250828_134947.csv"
    
    print("\n" + "="*70)
    print("40개 검색어 시스템 처리 결과 분석")
    print("="*70)
    
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"\n총 {len(rows)}개 상품 처리됨")
    print("-"*70)
    
    # 필수 키워드
    required_keywords = [
        "만원요리", "최씨남매", "집밥각", "술한잔", 
        "반찬고민끝", "국물땡김", "혼밥만세", "시간없어", 
        "힘내자", "모임각"
    ]
    
    for i, row in enumerate(rows[:5], 1):  # 상위 5개만
        print(f"\n[{i}] {row['상품명']}")
        print(f"브랜드: {row['상품명'][:15] if '[' in row['상품명'] else '없음'}")
        
        # 검색어 분석
        keywords = row['검색어설정'].split(',')
        print(f"총 키워드 수: {len(keywords)}개")
        
        # 필수 키워드 확인
        found_required = [k for k in keywords if k in required_keywords]
        print(f"필수 키워드: {len(found_required)}개 -> {', '.join(found_required)}")
        
        # 일반 키워드
        general = [k for k in keywords if k not in required_keywords]
        print(f"일반 키워드: {len(general)}개")
        
        # 상품 설명
        print(f"요약설명({len(row['상품 요약설명'])}자): {row['상품 요약설명']}")
        print(f"간략설명({len(row['상품 간략설명'])}자): {row['상품 간략설명']}")
        
        # 오타 확인
        if '꾸븐' in row['상품명']:
            print("  [경고] 상품명에 '꾸븐' 오타 발견!")
        if '꾸븐' in row['상품 요약설명'] or '꾸븐' in row['상품 간략설명']:
            print("  [경고] 설명에 '꾸븐' 오타 발견!")
        if '구운' in row['상품명'] or '구운' in row['상품 요약설명']:
            print("  [OK] '구운'으로 올바르게 수정됨")
    
    # 전체 통계
    print("\n" + "="*70)
    print("전체 통계")
    print("="*70)
    
    total_keywords = []
    required_counts = []
    
    for row in rows:
        keywords = row['검색어설정'].split(',')
        total_keywords.append(len(keywords))
        found = len([k for k in keywords if k in required_keywords])
        required_counts.append(found)
    
    print(f"평균 총 키워드: {sum(total_keywords)/len(total_keywords):.1f}개")
    print(f"평균 필수 키워드: {sum(required_counts)/len(required_counts):.1f}개")
    print(f"최대 키워드 수: {max(total_keywords)}개")
    print(f"최소 키워드 수: {min(total_keywords)}개")
    
    # 40개 초과 확인
    over_40 = [i for i, k in enumerate(total_keywords, 1) if k > 40]
    if over_40:
        print(f"[경고] 40개 초과 상품: {len(over_40)}개 (행: {over_40[:5]}...)")
    else:
        print("[OK] 모든 상품이 40개 키워드 제한 준수")
    
    # 오타 전체 확인
    typo_count = 0
    for row in rows:
        for field in ['상품명', '상품 요약설명', '상품 간략설명', '검색엔진최적화(SEO) Title', 
                      '검색엔진최적화(SEO) Description', '검색엔진최적화(SEO) Keywords']:
            if '꾸븐' in row.get(field, ''):
                typo_count += 1
                break
    
    if typo_count > 0:
        print(f"[경고] '꾸븐' 오타가 있는 상품: {typo_count}개")
    else:
        print("[OK] 모든 '꾸븐' 오타가 '구운'으로 수정됨")

if __name__ == "__main__":
    analyze_results()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
결과 파일 검증
"""

import csv
from collections import Counter

def verify_file(file_path):
    """결과 파일 검증"""
    print("\n" + "="*70)
    print("처리 결과 검증")
    print("="*70)
    
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"\n파일: {file_path}")
    print(f"총 상품 수: {len(rows)}개")
    print("-"*70)
    
    # 통계
    keyword_counts = []
    typo_count = 0
    samples = []
    
    for i, row in enumerate(rows, 1):
        product_name = row['상품명']
        keywords = row['검색어설정'].split(',')
        keyword_counts.append(len(keywords))
        
        # 오타 확인
        has_typo = False
        for field in ['상품명', '상품 요약설명', '상품 간략설명']:
            if '꾸븐' in row.get(field, ''):
                typo_count += 1
                has_typo = True
                break
        
        # 샘플 저장 (처음 3개)
        if i <= 3:
            samples.append({
                'name': product_name,
                'keywords': keywords,
                'keyword_count': len(keywords),
                'has_typo': has_typo
            })
    
    # 샘플 출력
    print("\n샘플 상품 (처음 3개):")
    for i, sample in enumerate(samples, 1):
        print(f"\n[{i}] {sample['name'][:40]}")
        print(f"  키워드 수: {sample['keyword_count']}개")
        print(f"  오타 상태: {'발견됨' if sample['has_typo'] else '정상'}")
        print(f"  키워드 샘플: {', '.join(sample['keywords'][:10])}...")
    
    # 전체 통계
    print("\n" + "="*70)
    print("전체 통계:")
    print("-"*70)
    
    avg_keywords = sum(keyword_counts) / len(keyword_counts)
    print(f"평균 키워드 수: {avg_keywords:.1f}개")
    print(f"최대 키워드 수: {max(keyword_counts)}개")
    print(f"최소 키워드 수: {min(keyword_counts)}개")
    
    # 키워드 수 분포
    print("\n키워드 수 분포:")
    under_20 = len([k for k in keyword_counts if k < 20])
    between_20_30 = len([k for k in keyword_counts if 20 <= k < 30])
    over_30 = len([k for k in keyword_counts if k >= 30])
    
    print(f"  20개 미만: {under_20}개 상품 ({under_20/len(rows)*100:.1f}%)")
    print(f"  20-29개: {between_20_30}개 상품 ({between_20_30/len(rows)*100:.1f}%)")
    print(f"  30개 이상: {over_30}개 상품 ({over_30/len(rows)*100:.1f}%)")
    
    # 오타 확인
    print(f"\n오타 검사:")
    if typo_count > 0:
        print(f"  [경고] '꾸븐' 오타 발견: {typo_count}개 상품")
    else:
        print(f"  [정상] 모든 '꾸븐' → '구운' 수정 완료")
    
    # 결과 평가
    print("\n" + "="*70)
    print("최종 평가:")
    if avg_keywords >= 30:
        print("  [우수] 평균 30개 이상 키워드 생성")
    elif avg_keywords >= 20:
        print("  [양호] 평균 20개 이상 키워드 생성")
    else:
        print("  [미흡] 평균 20개 미만 키워드")
    
    if typo_count == 0:
        print("  [우수] 오타 완전 수정")
    else:
        print("  [미흡] 오타 수정 필요")
    
    print("="*70)

if __name__ == "__main__":
    import sys
    
    # 가장 최근 파일 확인
    file_path = "data/output/cafe24_QUICK_20250828_142821.csv"
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    
    verify_file(file_path)
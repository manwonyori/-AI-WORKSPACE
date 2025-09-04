#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
검색어 추출 및 검증 스크립트
상품코드와 검색어만 매칭하여 출력
"""

import csv
import os
from datetime import datetime

def extract_keywords(input_file):
    """CSV에서 상품코드와 검색어만 추출"""
    
    # 파일 읽기
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # 결과 저장
    results = []
    missing_keywords = []
    
    for row in rows:
        product_code = row.get('상품코드', '')
        product_name = row.get('상품명', '')
        keywords = row.get('검색어설정', '')
        
        # 키워드 검증
        keyword_list = [k.strip() for k in keywords.split(',') if k.strip()]
        keyword_count = len(keyword_list)
        
        # 필수 키워드 체크
        has_brand = any(k in keyword_list for k in ['만원요리', '최씨남매'])
        has_essential = False
        
        # 상품별 필수 키워드 체크
        if '오돌뼈' in product_name:
            has_essential = any(k in keyword_list for k in ['술한잔', '모임각'])
        elif any(word in product_name for word in ['국', '탕', '찌개']):
            has_essential = any(k in keyword_list for k in ['국물땡김', '집밥각'])
        elif any(word in product_name for word in ['반찬', '김치']):
            has_essential = any(k in keyword_list for k in ['반찬고민끝', '집밥각'])
        else:
            has_essential = True  # 기타 상품은 패스
        
        # 결과 저장
        results.append({
            '상품코드': product_code,
            '상품명': product_name,
            '검색어': keywords,
            '키워드수': keyword_count,
            '브랜드키워드': '포함' if has_brand else '누락',
            '필수키워드': '포함' if has_essential else '누락'
        })
        
        if not has_brand or not has_essential:
            missing_keywords.append({
                '상품코드': product_code,
                '상품명': product_name,
                '누락내용': f"브랜드: {not has_brand}, 필수: {not has_essential}"
            })
    
    # 타임스탬프
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 1. 전체 결과 저장
    output_file = f'data/output/keywords_extracted_{timestamp}.csv'
    with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
        fieldnames = ['상품코드', '상품명', '검색어', '키워드수', '브랜드키워드', '필수키워드']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"[OK] 전체 결과 저장: {output_file}")
    
    # 2. 간단 버전 (코드와 키워드만)
    simple_file = f'data/output/keywords_simple_{timestamp}.csv'
    with open(simple_file, 'w', encoding='utf-8-sig', newline='') as f:
        fieldnames = ['상품코드', '검색어']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow({
                '상품코드': row['상품코드'],
                '검색어': row['검색어']
            })
    
    print(f"[OK] 간단 버전 저장: {simple_file}")
    
    # 3. 누락 키워드 리포트
    if missing_keywords:
        missing_file = f'data/output/keywords_missing_{timestamp}.csv'
        with open(missing_file, 'w', encoding='utf-8-sig', newline='') as f:
            fieldnames = ['상품코드', '상품명', '누락내용']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(missing_keywords)
        
        print(f"⚠ 필수 키워드 누락 상품 {len(missing_keywords)}개: {missing_file}")
    
    # 통계 출력
    print(f"\n=== 검증 결과 ===")
    print(f"총 상품: {len(results)}개")
    print(f"평균 키워드: {sum(r['키워드수'] for r in results) / len(results):.1f}개")
    print(f"브랜드 키워드 포함: {sum(1 for r in results if r['브랜드키워드'] == '포함')}개")
    print(f"필수 키워드 포함: {sum(1 for r in results if r['필수키워드'] == '포함')}개")
    
    return output_file

if __name__ == '__main__':
    # 최신 output 파일 찾기
    output_dir = 'data/output'
    files = [f for f in os.listdir(output_dir) if f.endswith('.csv') and 'AI멀티' in f]
    
    if files:
        latest_file = sorted(files)[-1]
        input_file = os.path.join(output_dir, latest_file)
        print(f"처리 파일: {input_file}")
        extract_keywords(input_file)
    else:
        print("AI 처리된 파일이 없습니다. 먼저 처리를 실행하세요.")
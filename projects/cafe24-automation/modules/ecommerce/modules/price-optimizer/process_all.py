#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
전체 상품 가격 분석 처리
"""

import os
import sys
import csv
from datetime import datetime

# 현재 디렉토리를 sys.path에 추가
sys.path.append(os.path.dirname(__file__))

from price_analyzer import PriceOptimizer

def process_all_products():
    """전체 상품 가격 분석"""
    print("=== 전체 상품 가격 분석 시작 ===")
    
    optimizer = PriceOptimizer()
    
    # 입력 파일 경로
    input_file = "../../data/output/clean_test_AI멀티_20250828_173909.csv"
    
    if not os.path.exists(input_file):
        print(f"입력 파일을 찾을 수 없습니다: {input_file}")
        return
    
    print(f"입력 파일: {input_file}")
    
    # 출력 파일명 생성
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"../../data/output/가격분석_결과_{timestamp}.csv"
    
    # CSV 읽기
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = list(reader.fieldnames) + [
            '마진율(%)', '가격대', '경쟁가격_평균', '최적가격_제안', '가격전략'
        ]
    
    print(f"총 {len(rows)}개 상품 처리 예정")
    
    # 처리
    processed = []
    successful = 0
    
    for i, row in enumerate(rows[:10], 1):  # 처음 10개만 테스트
        try:
            print(f"\n[{i}/10] 처리 중: {row.get('상품명', 'Unknown')[:30]}...")
            
            # 가격 분석
            analysis = optimizer.analyze_price_strategy(row)
            
            # 결과 추가
            row['마진율(%)'] = analysis['마진율']
            row['가격대'] = analysis['가격대']
            row['경쟁가격_평균'] = analysis['경쟁가격_추정'].get('평균가', 0)
            row['최적가격_제안'] = str(analysis['최적가격_제안'])
            row['가격전략'] = analysis['가격전략']
            
            processed.append(row)
            successful += 1
            
        except Exception as e:
            print(f"오류 발생: {e}")
            # 기본값으로 처리
            row['마진율(%)'] = 0
            row['가격대'] = '분석불가'
            row['경쟁가격_평균'] = 0
            row['최적가격_제안'] = '분석불가'
            row['가격전략'] = '분석실패'
            processed.append(row)
    
    # 저장
    with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(processed)
    
    print(f"\n=== 가격 분석 완료 ===")
    print(f"성공: {successful}/10")
    print(f"결과 파일: {output_file}")

if __name__ == "__main__":
    process_all_products()
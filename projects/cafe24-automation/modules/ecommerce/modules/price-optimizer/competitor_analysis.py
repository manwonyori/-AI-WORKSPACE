#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
경쟁업체 가격 비교 분석
"""

import price_analyzer
import os
import csv

def main():
    print('=== 경쟁업체 가격 비교 분석 ===')
    analyzer = price_analyzer.PriceOptimizer()

    print('주요 분석 대상:')
    for name, domain in analyzer.competitors.items():
        print(f'- {name}: {domain}')

    print('\n분석 방법:')
    print('1. AI 기반 가격 추정 (OpenAI GPT-3.5)')
    print('2. 상품명 기반 유사 상품 매칭')
    print('3. 가격대별 경쟁력 평가')

    # 샘플 분석
    output_dir = '../../data/output'
    if os.path.exists(output_dir):
        csv_files = [f for f in os.listdir(output_dir) if '가격분석_결과_' in f and f.endswith('.csv')]
        if csv_files:
            latest_file = sorted(csv_files)[-1]
            file_path = os.path.join(output_dir, latest_file)
            
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            
            print(f'\n샘플 경쟁가격 분석 (상위 3개 상품):')
            for i, row in enumerate(rows[:3]):
                name = row.get('상품명', '')[:25]
                current = row.get('판매가', 0)
                competitor_avg = row.get('경쟁가격_평균', 0)
                print(f'{i+1}. {name}')
                print(f'   현재가: {current}원 | 경쟁평균: {competitor_avg}원')
                
            print('\n경쟁력 평가 완료!')
        else:
            print('\n가격분석 결과 파일이 없습니다.')
            print('먼저 [1] 전체 상품 가격 분석을 실행하세요.')

if __name__ == "__main__":
    main()
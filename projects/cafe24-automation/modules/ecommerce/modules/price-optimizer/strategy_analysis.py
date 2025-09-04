#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
최적 가격 전략 수립
"""

import price_analyzer
import os
import csv

def main():
    print('=== 최적 가격 전략 수립 ===')

    print('4가지 가격 전략 분석:')
    print('1. 공격적 가격: 경쟁업체 최저가 대비 -2% (시장점유율 확대)')
    print('2. 경쟁적 가격: 경쟁업체 평균가 대비 -1% (균형잡힌 접근)')
    print('3. 안전적 가격: 경쟁업체 평균가 대비 +2% (안정성 우선)')
    print('4. 프리미엄 가격: 경쟁업체 평균가 대비 +8% (브랜드 가치)')

    # 실제 데이터 기반 전략 제안
    output_dir = '../../data/output'
    if os.path.exists(output_dir):
        csv_files = [f for f in os.listdir(output_dir) if '가격분석_결과_' in f and f.endswith('.csv')]
        if csv_files:
            latest_file = sorted(csv_files)[-1]
            file_path = os.path.join(output_dir, latest_file)
            
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            
            print(f'\n상품별 맞춤 전략 (상위 3개):')
            for i, row in enumerate(rows[:3]):
                name = row.get('상품명', '')[:25]
                strategy = row.get('가격전략', '')
                tier = row.get('가격대', '')
                margin = row.get('마진율(%)', '0')
                
                print(f'\n{i+1}. {name}')
                print(f'   가격대: {tier} | 마진: {margin}%')
                print(f'   전략: {strategy}')
                
                # 최적가격 제안 파싱 (간단 버전)
                if '최적가격_제안' in row:
                    suggestions = row["최적가격_제안"]
                    if len(suggestions) > 50:
                        suggestions = suggestions[:50] + "..."
                    print(f'   제안: {suggestions}')
                    
            print('\n전략 수립 완료! 상품별 세부 전략은 CSV 파일을 확인하세요.')
        else:
            print('\n전략 수립을 위해 먼저 가격 분석이 필요합니다.')
            print('[1] 전체 상품 가격 분석을 먼저 실행하세요.')
    else:
        print('데이터 폴더를 찾을 수 없습니다.')

if __name__ == "__main__":
    main()
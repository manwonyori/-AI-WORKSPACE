#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
마진율 개선 제안 시스템
"""

import price_analyzer
import os
import csv

def main():
    print('=== 마진율 개선 제안 시스템 ===')
    analyzer = price_analyzer.PriceOptimizer()

    # 최신 가격분석 결과 파일 찾기
    output_dir = '../../data/output'
    if os.path.exists(output_dir):
        csv_files = [f for f in os.listdir(output_dir) if '가격분석_결과_' in f and f.endswith('.csv')]
        if csv_files:
            latest_file = sorted(csv_files)[-1]
            file_path = os.path.join(output_dir, latest_file)
            print(f'분석 파일: {latest_file}')
            
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                low_margin_products = []
                for row in reader:
                    try:
                        margin = float(row.get('마진율(%)', 0))
                        if margin < 15:
                            low_margin_products.append((row.get('상품명', ''), margin))
                    except:
                        continue
            
            print(f'\n마진율 15% 미만 상품: {len(low_margin_products)}개')
            for name, margin in low_margin_products[:5]:
                print(f'- {name[:30]}: {margin:.1f}%')
            
            if len(low_margin_products) > 5:
                print(f'... 외 {len(low_margin_products)-5}개 상품')
            
            print('\n개선 방안:')
            print('1. 공급가 재협상으로 원가 절감')
            print('2. 부가가치 서비스 추가로 가격 정당화')
            print('3. 번들 상품으로 전체 마진율 개선')
            print('4. 프리미엄 포지셔닝으로 가격 상향')
        else:
            print('가격분석 결과 파일을 찾을 수 없습니다.')
            print('먼저 [1] 전체 상품 가격 분석을 실행하세요.')
    else:
        print('output 폴더를 찾을 수 없습니다.')

if __name__ == "__main__":
    main()
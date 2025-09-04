#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
공급사별 마진율 분석 및 관리 시스템
"""

import os
import csv
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SupplierMarginAnalyzer:
    def __init__(self):
        self.margin_levels = {
            1: "위험 (5% 미만)",
            2: "낮음 (5-15%)", 
            3: "보통 (15-25%)",
            4: "양호 (25-35%)",
            5: "우수 (35% 이상)"
        }
    
    def get_margin_level(self, margin):
        """마진율을 5단계로 분류"""
        if margin < 5:
            return 1
        elif margin < 15:
            return 2
        elif margin < 25:
            return 3
        elif margin < 35:
            return 4
        else:
            return 5
    
    def analyze_suppliers(self, input_file: str) -> dict:
        """공급사별 마진율 분석 - 타입 힌팅 추가"""
        print("=== 공급사별 마진율 분석 ===")
        
        if not os.path.exists(input_file):
            logging.error(f"파일을 찾을 수 없음: {input_file}")
            print("가격분석 결과 파일을 찾을 수 없습니다.")
            return {}
        
        supplier_data = defaultdict(list)
        
        with open(input_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                product_name = row.get('상품명', '')
                # 안전한 float 변환
                try:
                    margin = float(str(row.get('마진율(%)', 0)).replace('%', ''))
                except (ValueError, TypeError):
                    margin = 0.0
                price = row.get('판매가', 0)
                
                # 공급사 추출 (상품명에서 [공급사명] 패턴)
                supplier = "기타"
                if '[' in product_name and ']' in product_name:
                    start = product_name.find('[') + 1
                    end = product_name.find(']')
                    if start > 0 and end > start:
                        supplier = product_name[start:end]
                
                supplier_data[supplier].append({
                    'name': product_name,
                    'margin': margin,
                    'price': price,
                    'level': self.get_margin_level(margin)
                })
        
        # 공급사별 통계
        print(f"\n총 {len(supplier_data)}개 공급사 발견:")
        print("-" * 80)
        
        for supplier, products in supplier_data.items():
            avg_margin = sum(p['margin'] for p in products) / len(products)
            level_counts = defaultdict(int)
            for p in products:
                level_counts[p['level']] += 1
            
            print(f"\n[{supplier}] ({len(products)}개 상품)")
            print(f"   평균 마진율: {avg_margin:.1f}%")
            print(f"   마진 분포:")
            for level in range(1, 6):
                count = level_counts[level]
                if count > 0:
                    print(f"     {level}단계 ({self.margin_levels[level]}): {count}개")
        
        return supplier_data
    
    def show_margin_distribution(self, supplier_data):
        """마진율 5단계별 전체 분포"""
        print("\n=== 전체 마진율 분포 ===")
        
        all_products = []
        for products in supplier_data.values():
            all_products.extend(products)
        
        level_products = defaultdict(list)
        for product in all_products:
            level_products[product['level']].append(product)
        
        print(f"총 {len(all_products)}개 상품:")
        for level in range(1, 6):
            products = level_products[level]
            if products:
                avg_margin = sum(p['margin'] for p in products) / len(products)
                print(f"\n{level}단계 ({self.margin_levels[level]}): {len(products)}개 (평균 {avg_margin:.1f}%)")
                
                # 상위 3개만 표시
                for i, product in enumerate(products[:3]):
                    print(f"  - {product['name'][:40]}: {product['margin']:.1f}%")
                if len(products) > 3:
                    print(f"  ... 외 {len(products)-3}개")
        
        return level_products

def main():
    analyzer = SupplierMarginAnalyzer()
    
    # 최신 가격분석 결과 파일 찾기
    output_dir = '../../data/output'
    if os.path.exists(output_dir):
        csv_files = [f for f in os.listdir(output_dir) if '가격분석_결과_' in f and f.endswith('.csv')]
        if csv_files:
            latest_file = os.path.join(output_dir, sorted(csv_files)[-1])
            supplier_data = analyzer.analyze_suppliers(latest_file)
            analyzer.show_margin_distribution(supplier_data)
        else:
            print("가격분석 결과 파일이 없습니다.")
            print("먼저 [1] 전체 상품 가격 분석을 실행하세요.")
    else:
        print("데이터 폴더를 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
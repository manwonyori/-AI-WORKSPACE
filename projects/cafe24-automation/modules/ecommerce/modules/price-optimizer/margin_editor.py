#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
마진율 일괄/개별 수정 시스템
"""

import os
import csv
from datetime import datetime
from collections import defaultdict
from typing import Optional, Dict, List
import logging

# 로깅 설정
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class MarginEditor:
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
    
    def calculate_new_price(self, cost_price: float, target_margin: float) -> Optional[int]:
        """목표 마진율로 새로운 판매가 계산 - 타입 힌팅 추가"""
        # 마진율 = (판매가 - 원가) / 판매가 * 100
        # 판매가 = 원가 / (1 - 마진율/100)
        if target_margin >= 100:
            logger.warning(f"잘못된 마진율: {target_margin}%")
            print("마진율은 100% 미만이어야 합니다.")
            return None
        
        if cost_price <= 0:
            logger.warning(f"잘못된 원가: {cost_price}")
            return None
        
        new_price = cost_price / (1 - target_margin / 100)
        return int(new_price)
    
    def batch_edit_by_level(self, input_file: str, target_level: int, new_margin: float) -> Optional[str]:
        """마진율 단계별 일괄 수정 - 개선된 버전"""
        print(f"=== {target_level}단계 상품 마진율을 {new_margin}%로 일괄 수정 ===")
        
        if not os.path.exists(input_file):
            print("입력 파일을 찾을 수 없습니다.")
            return None
        
        updated_rows = []
        update_count = 0
        
        with open(input_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            
            for row in reader:
                current_margin = float(row.get('마진율(%)', 0))
                current_level = self.get_margin_level(current_margin)
                
                if current_level == target_level:
                    # 공급가(원가) 기반으로 새로운 판매가 계산
                    cost_price = int(str(row.get('공급가', 0)).replace(',', '')) if row.get('공급가') else 0
                    
                    if cost_price > 0:
                        new_price = self.calculate_new_price(cost_price, new_margin)
                        if new_price:
                            row['판매가'] = str(new_price)
                            row['마진율(%)'] = new_margin
                            update_count += 1
                            print(f"수정: {row.get('상품명', '')[:30]} | {current_margin:.1f}% → {new_margin}% | {new_price:,}원")
                
                updated_rows.append(row)
        
        if update_count > 0:
            # 수정된 파일 저장
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"../../data/output/마진수정_{target_level}단계_{timestamp}.csv"
            
            with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(updated_rows)
            
            print(f"\n총 {update_count}개 상품 수정 완료!")
            print(f"결과 파일: {output_file}")
            return output_file
        else:
            print(f"{target_level}단계에 해당하는 상품이 없습니다.")
            return None
    
    def batch_edit_by_supplier(self, input_file, target_supplier, new_margin):
        """공급사별 마진율 일괄 수정"""
        print(f"=== [{target_supplier}] 상품 마진율을 {new_margin}%로 일괄 수정 ===")
        
        if not os.path.exists(input_file):
            print("입력 파일을 찾을 수 없습니다.")
            return None
        
        updated_rows = []
        update_count = 0
        
        with open(input_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            
            for row in reader:
                product_name = row.get('상품명', '')
                
                # 공급사 확인
                supplier = "기타"
                if '[' in product_name and ']' in product_name:
                    start = product_name.find('[') + 1
                    end = product_name.find(']')
                    if start > 0 and end > start:
                        supplier = product_name[start:end]
                
                if supplier == target_supplier:
                    # 공급가(원가) 기반으로 새로운 판매가 계산
                    cost_price = int(str(row.get('공급가', 0)).replace(',', '')) if row.get('공급가') else 0
                    current_margin = float(row.get('마진율(%)', 0))
                    
                    if cost_price > 0:
                        new_price = self.calculate_new_price(cost_price, new_margin)
                        if new_price:
                            row['판매가'] = str(new_price)
                            row['마진율(%)'] = new_margin
                            update_count += 1
                            print(f"수정: {product_name[:40]} | {current_margin:.1f}% → {new_margin}% | {new_price:,}원")
                
                updated_rows.append(row)
        
        if update_count > 0:
            # 수정된 파일 저장
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"../../data/output/마진수정_{target_supplier}_{timestamp}.csv"
            
            with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(updated_rows)
            
            print(f"\n총 {update_count}개 상품 수정 완료!")
            print(f"결과 파일: {output_file}")
            return output_file
        else:
            print(f"[{target_supplier}] 공급사 상품이 없습니다.")
            return None
    
    def interactive_edit(self, input_file):
        """대화형 개별 마진율 수정"""
        print("=== 개별 마진율 수정 ===")
        
        if not os.path.exists(input_file):
            print("입력 파일을 찾을 수 없습니다.")
            return None
        
        # 낮은 마진율 상품 찾기
        low_margin_products = []
        with open(input_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                margin = float(row.get('마진율(%)', 0))
                if margin < 20:  # 20% 미만
                    low_margin_products.append((i, row, margin))
        
        if not low_margin_products:
            print("마진율이 20% 미만인 상품이 없습니다.")
            return None
        
        print(f"\n마진율 20% 미만 상품 {len(low_margin_products)}개 발견:")
        for i, (idx, row, margin) in enumerate(low_margin_products[:10]):
            print(f"{i+1}. {row.get('상품명', '')[:40]} | 현재: {margin:.1f}%")
        
        if len(low_margin_products) > 10:
            print(f"... 외 {len(low_margin_products)-10}개 상품")
        
        print("\n개별 수정을 위해 별도 프로그램을 실행하거나")
        print("일괄 수정 기능을 사용하시기 바랍니다.")

def main():
    editor = MarginEditor()
    
    # 최신 가격분석 결과 파일 찾기
    output_dir = '../../data/output'
    if os.path.exists(output_dir):
        csv_files = [f for f in os.listdir(output_dir) if '가격분석_결과_' in f and f.endswith('.csv')]
        if csv_files:
            latest_file = os.path.join(output_dir, sorted(csv_files)[-1])
            
            print("마진율 수정 옵션을 선택하세요:")
            print("1. 마진율 단계별 일괄 수정")
            print("2. 공급사별 일괄 수정") 
            print("3. 개별 수정 (낮은 마진율 상품 확인)")
            
            choice = input("\n선택 (1-3): ").strip()
            
            if choice == "1":
                print("\n마진율 단계:")
                for level, desc in editor.margin_levels.items():
                    print(f"{level}. {desc}")
                
                level = int(input("수정할 단계 (1-5): "))
                new_margin = float(input("새로운 마진율 (%): "))
                editor.batch_edit_by_level(latest_file, level, new_margin)
                
            elif choice == "2":
                supplier = input("공급사명 입력: ").strip()
                new_margin = float(input("새로운 마진율 (%): "))
                editor.batch_edit_by_supplier(latest_file, supplier, new_margin)
                
            elif choice == "3":
                editor.interactive_edit(latest_file)
                
        else:
            print("가격분석 결과 파일이 없습니다.")
            print("먼저 [1] 전체 상품 가격 분석을 실행하세요.")
    else:
        print("데이터 폴더를 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
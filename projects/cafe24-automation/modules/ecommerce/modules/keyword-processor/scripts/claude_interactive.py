#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Claude 대화형 처리 시스템
사용자가 Claude와 대화하면서 처리
"""

import os
import csv
import pyperclip  # 클립보드 제어
import webbrowser
from datetime import datetime

class ClaudeInteractive:
    def __init__(self):
        self.products = []
        self.results = []
    
    def load_csv(self, file_path):
        """CSV 파일 로드"""
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            self.products = list(reader)
        print(f"[OK] {len(self.products)}개 상품 로드 완료")
    
    def generate_prompt(self, product):
        """Claude용 프롬프트 생성"""
        prompt = f"""
한국 이커머스 상품의 검색 키워드 40개를 생성해주세요.

상품명: {product.get('상품명', '')}
카테고리: {product.get('category', '')}
가격: {product.get('판매가', '')}원

조건:
1. 필수 포함: 만원요리, 최씨남매, 집밥각, 술한잔 중 적절한 것
2. 소비자가 실제 검색할 키워드 30개 이상
3. 쉼표로 구분하여 한 줄로

키워드:"""
        return prompt
    
    def process_single(self, index):
        """단일 상품 처리"""
        if index >= len(self.products):
            return False
        
        product = self.products[index]
        print(f"\n[{index+1}/{len(self.products)}] {product['상품명']}")
        
        # 프롬프트 생성 및 클립보드 복사
        prompt = self.generate_prompt(product)
        pyperclip.copy(prompt)
        
        print("\n프롬프트가 클립보드에 복사되었습니다!")
        print("1. Claude.ai에서 붙여넣기 (Ctrl+V)")
        print("2. 응답 받기")
        print("3. 응답 복사 (Ctrl+C)")
        
        # Claude 열기
        webbrowser.open('https://claude.ai')
        
        # 응답 대기
        input("\nClaude 응답을 복사했으면 Enter...")
        
        # 클립보드에서 응답 가져오기
        response = pyperclip.paste()
        
        # 결과 저장
        product['검색어설정'] = response
        self.results.append(product)
        
        print("[OK] 처리 완료")
        return True
    
    def save_results(self):
        """결과 저장"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'data/output/claude_처리_{timestamp}.csv'
        
        if self.results:
            keys = self.results[0].keys()
            with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(self.results)
            print(f"\n결과 저장: {output_file}")

def main():
    processor = ClaudeInteractive()
    
    # CSV 로드
    input_file = 'data/input/manwonyori_20250828_283_56dd.csv'
    processor.load_csv(input_file)
    
    print("\n" + "="*60)
    print("Claude 대화형 처리 시스템")
    print("="*60)
    
    while True:
        print("\n[1] 다음 상품 처리")
        print("[2] 결과 저장")
        print("[3] 종료")
        
        choice = input("\n선택: ")
        
        if choice == '1':
            index = len(processor.results)
            if not processor.process_single(index):
                print("모든 상품 처리 완료!")
        elif choice == '2':
            processor.save_results()
        elif choice == '3':
            break

if __name__ == '__main__':
    # pyperclip 설치 필요
    try:
        import pyperclip
    except:
        print("pip install pyperclip 실행 필요")
        exit()
    
    main()
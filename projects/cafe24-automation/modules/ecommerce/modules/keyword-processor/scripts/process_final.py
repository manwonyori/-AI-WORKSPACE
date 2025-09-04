#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
최종 처리 실행
개선된 40개 키워드 시스템 적용
"""

import os
import sys
from datetime import datetime

# 상위 디렉토리의 src 폴더를 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.main_system import IntelligentSystem

def main():
    """메인 실행"""
    print("\n" + "="*70)
    print("AI 처리 시스템 실행")
    print("목표: 각 상품당 30-40개 키워드 생성")
    print("="*70)
    
    # 시스템 초기화 시도
    try:
        system = IntelligentSystem()
    except Exception as e:
        print(f"\nAI 초기화 실패: {e}")
        print("\nAPI 키가 설정되지 않았습니다.")
        print("다음 방법 중 하나를 선택하세요:")
        print("1. .env 파일에 API 키 설정")
        print("2. '빠른 처리' 모드 사용 (API 불필요)")
        return None
    
    # input 폴더에서 CSV 파일 자동 탐색
    input_dir = "../../../data/input"
    csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"오류: {input_dir} 폴더에 CSV 파일이 없습니다!")
        return
    
    # 첫 번째 CSV 파일 사용 (또는 가장 최신 파일)
    input_file = os.path.join(input_dir, csv_files[0])
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = os.path.splitext(csv_files[0])[0]
    output_file = f"../../../data/output/{base_name}_AI_{timestamp}.csv"
    
    print(f"\n입력: {input_file}")
    print(f"출력: {output_file}")
    print("\n처리 시작...")
    print("-"*70)
    
    try:
        # CSV 처리
        result_file = system.process_csv(input_file, output_file)
        
        print("\n" + "="*70)
        print("처리 완료!")
        print(f"결과 파일: {result_file}")
        print("="*70)
        
        return result_file
        
    except Exception as e:
        print(f"\n오류 발생: {e}")
        return None

if __name__ == "__main__":
    result = main()
    if result:
        print(f"\n성공적으로 처리되었습니다.")
        print(f"파일 위치: {result}")
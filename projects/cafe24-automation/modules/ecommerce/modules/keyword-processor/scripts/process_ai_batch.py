#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI 일괄 처리 스크립트
각 파일을 개별적으로 AI 처리
"""

import os
import sys
from datetime import datetime

# 상위 디렉토리의 src 폴더를 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.main_system import IntelligentSystem

def main():
    """메인 실행"""
    
    # 명령줄 인수 처리
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        print("오류: 입력 파일을 지정하세요.")
        return None
    
    # 파일 존재 확인
    if not os.path.exists(input_file):
        print(f"오류: 파일이 없습니다: {input_file}")
        return None
    
    print(f"\n파일: {os.path.basename(input_file)}")
    print("-" * 60)
    
    # 시스템 초기화 시도
    try:
        system = IntelligentSystem()
    except Exception as e:
        print(f"AI 초기화 실패: {e}")
        print("\nAPI 키가 설정되지 않았습니다.")
        print(".env 파일에 다음 중 하나를 설정하세요:")
        print("- OPENAI_API_KEY")
        print("- ANTHROPIC_API_KEY")
        print("- GEMINI_API_KEY")
        return None
    
    # 출력 파일명 생성
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = f"data/output/{base_name}_AI처리_{timestamp}.csv"
    
    try:
        # AI 처리 실행
        print("AI 처리 시작...")
        result_file = system.process_csv(input_file, output_file)
        
        print(f"처리 완료: {output_file}")
        return result_file
        
    except Exception as e:
        print(f"처리 중 오류 발생: {e}")
        return None

if __name__ == "__main__":
    result = main()
    if result:
        print(f"성공: {result}")
    else:
        print("처리 실패")
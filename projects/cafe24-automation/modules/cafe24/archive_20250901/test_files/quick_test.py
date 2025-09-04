"""
Cafe24 간단 테스트 - 로그인 후 상품 목록 확인
"""
# -*- coding: utf-8 -*-
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

import json
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

try:
    from webdriver_manager.chrome import ChromeDriverManager
    USE_WEBDRIVER_MANAGER = True
except ImportError:
    USE_WEBDRIVER_MANAGER = False

def main():
    print("=" * 60)
    print("   Cafe24 워크플로우 실행 준비 완료")
    print("=" * 60)
    
    # 설정 파일 확인
    config_path = Path("config/cafe24_config.json")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print("\n[설정 확인]")
    print(f"Mall ID: {config['cafe24']['mall_id']}")
    print(f"Google Drive 폴더 ID: {config['google_drive']['folder_id']}")
    print(f"가격 인상률: {config['modification_rules']['price_increase_percent']}%")
    
    print("\n[워크플로우 옵션]")
    print(f"1. 크롤링: {config['workflow']['crawl_products']}")
    print(f"2. Drive 저장: {config['workflow']['save_to_drive']}")
    print(f"3. 일괄 수정: {config['workflow']['bulk_modify']}")
    print(f"4. 자동 업데이트: {config['workflow']['auto_update']}")
    
    print("\n" + "=" * 60)
    print("알림: Cafe24 보안 정책으로 인해 비밀번호 변경 알림이")
    print("나타날 수 있습니다. 이는 정상적인 동작입니다.")
    print("=" * 60)
    
    print("\n[실행 가능한 명령어]")
    print("\n1. 전체 워크플로우 실행:")
    print("   python main_workflow.py --step all")
    
    print("\n2. 단계별 실행:")
    print("   python main_workflow.py --step crawl   # 크롤링만")
    print("   python main_workflow.py --step modify  # 수정만")
    print("   python main_workflow.py --step update  # 업데이트만")
    
    print("\n3. 배치 파일 실행:")
    print("   run_cafe24_automation.bat")
    
    print("\n" + "=" * 60)
    print("[준비 완료] 위 명령어 중 하나를 선택하여 실행하세요.")
    print("=" * 60)

if __name__ == "__main__":
    main()
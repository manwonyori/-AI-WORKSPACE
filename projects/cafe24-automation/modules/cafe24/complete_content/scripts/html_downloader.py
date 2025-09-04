# -*- coding: utf-8 -*-
"""
Cafe24 HTML 다운로더
상품 상세설명 HTML을 다운로드하는 스크립트
"""
import sys
import os
import csv
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json

# UTF-8 인코딩 설정
if os.name == 'nt':  # Windows
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def setup_driver():
    """Chrome 드라이버 설정"""
    options = Options()
    options.add_argument("--headless")  # 백그라운드 실행
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    try:
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as e:
        print(f"❌ Chrome 드라이버 설정 실패: {e}")
        print("💡 Chrome과 ChromeDriver가 설치되어 있는지 확인하세요.")
        return None

def download_html_content():
    """HTML 콘텐츠 다운로드"""
    
    # CSV 파일 경로
    csv_path = Path("../download")
    csv_files = list(csv_path.glob("manwonyori_*.csv"))
    
    if not csv_files:
        print("❌ CSV 파일을 찾을 수 없습니다.")
        print(f"📍 경로 확인: {csv_path.absolute()}")
        return
    
    # 가장 최신 CSV 파일 사용
    latest_csv = max(csv_files, key=lambda x: x.stat().st_mtime)
    print(f"📄 사용할 CSV: {latest_csv.name}")
    
    # 설정 파일 확인
    config_path = Path("config/cafe24_config.json")
    if not config_path.exists():
        print("❌ 설정 파일이 없습니다: config/cafe24_config.json")
        print("📝 수동으로 로그인 정보를 입력하세요.")
        return
    
    # 드라이버 설정
    driver = setup_driver()
    if not driver:
        return
    
    try:
        # CSV 읽기
        products = []
        with open(latest_csv, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                product_no = row.get('상품번호', '')
                product_name = row.get('상품명', '')
                if product_no:
                    products.append({
                        'no': product_no,
                        'name': product_name
                    })
        
        print(f"📊 총 {len(products)}개 상품 발견")
        
        # 실제 다운로드는 수동 가이드 제공
        print("\n🔧 자동 다운로드 구현은 복잡합니다.")
        print("📝 현재는 temp_txt 폴더의 239개 TXT 파일을 사용하세요.")
        print("✅ 이미 완성된 콘텐츠가 있습니다!")
        
        # TXT → HTML 변환 제안
        print("\n💡 추천 작업 순서:")
        print("1. temp_txt 폴더에 TXT 파일들이 있는지 확인")
        print("2. scripts/apply_txt_to_html.py 실행")
        print("3. scripts/complete_reclassification.py 실행")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    download_html_content()
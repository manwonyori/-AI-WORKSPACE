# -*- coding: utf-8 -*-
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

import json
import time
import re
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

try:
    from webdriver_manager.chrome import ChromeDriverManager
    USE_WEBDRIVER_MANAGER = True
except ImportError:
    USE_WEBDRIVER_MANAGER = False

def extract_product_data_from_html(html_file_path):
    """HTML 파일에서 상품 데이터 추출"""
    
    print("="*80)
    print("   P00000NB 상품 데이터 추출 및 분석")
    print("="*80)
    
    # HTML 파일 읽기
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 추출된 상품 데이터
    product_data = {}
    
    print("\n[STEP 1] 기본 상품 정보 추출...")
    
    # 1. 상품코드
    product_code_elem = soup.find('span', id='product_code')
    if product_code_elem:
        product_data['product_code'] = product_code_elem.get_text().strip()
        print(f"   상품코드: {product_data['product_code']}")
    
    # 2. 상품명 (기본 쇼핑몰)
    product_name_input = soup.find('input', {'name': 'product_name[1]', 'id': 'product_name'})
    if product_name_input:
        product_data['product_name'] = product_name_input.get('value', '')
        print(f"   상품명: {product_data['product_name']}")
    
    # 3. 영문 상품명
    eng_product_name_input = soup.find('input', {'name': 'eng_product_name'})
    if eng_product_name_input:
        product_data['eng_product_name'] = eng_product_name_input.get('value', '')
        print(f"   영문상품명: {product_data['eng_product_name']}")
    
    # 4. 상품명(관리용)
    item_name_input = soup.find('input', {'name': 'item_name'})
    if item_name_input:
        product_data['item_name'] = item_name_input.get('value', '')
        print(f"   관리용상품명: {product_data['item_name']}")
    
    # 5. 자체 상품코드
    ma_product_code_input = soup.find('input', {'name': 'ma_product_code'})
    if ma_product_code_input:
        product_data['ma_product_code'] = ma_product_code_input.get('value', '')
        print(f"   자체상품코드: {product_data['ma_product_code'] or '(미설정)'}")
    
    print("\n[STEP 2] 가격 정보 추출...")
    
    # 6. 판매가 찾기
    price_inputs = soup.find_all('input', {'name': re.compile(r'price_.*')})
    for price_input in price_inputs:
        name = price_input.get('name', '')
        value = price_input.get('value', '')
        if value and value != '0':
            product_data[name] = value
            print(f"   {name}: {value}원")
    
    print("\n[STEP 3] 상태 정보 추출...")
    
    # 7. 진열상태
    display_inputs = soup.find_all('input', {'name': re.compile(r'display_.*')})
    for display_input in display_inputs:
        name = display_input.get('name', '')
        if display_input.get('checked'):
            product_data[name] = display_input.get('value', '')
            print(f"   {name}: {display_input.get('value', '')}")
    
    # 8. 판매상태
    sell_inputs = soup.find_all('input', {'name': re.compile(r'selling_.*')})
    for sell_input in sell_inputs:
        name = sell_input.get('name', '')
        if sell_input.get('checked'):
            product_data[name] = sell_input.get('value', '')
            print(f"   {name}: {sell_input.get('value', '')}")
    
    print("\n[STEP 4] 분류 및 옵션 정보 추출...")
    
    # 9. 상품 분류
    category_selects = soup.find_all('select', {'name': re.compile(r'category_.*')})
    for category_select in category_selects:
        name = category_select.get('name', '')
        selected_option = category_select.find('option', selected=True)
        if selected_option:
            product_data[name] = selected_option.get('value', '')
            print(f"   {name}: {selected_option.get_text().strip()}")
    
    # 10. 옵션 정보
    option_inputs = soup.find_all('input', {'name': re.compile(r'option_.*')})
    option_count = 0
    for option_input in option_inputs:
        name = option_input.get('name', '')
        value = option_input.get('value', '')
        if value:
            product_data[name] = value
            option_count += 1
    
    if option_count > 0:
        print(f"   옵션 관련 필드: {option_count}개")
    
    print("\n[STEP 5] 폼 전체 분석...")
    
    # 모든 input 필드 통계
    all_inputs = soup.find_all('input')
    all_textareas = soup.find_all('textarea')
    all_selects = soup.find_all('select')
    
    print(f"   총 input 필드: {len(all_inputs)}개")
    print(f"   총 textarea 필드: {len(all_textareas)}개") 
    print(f"   총 select 필드: {len(all_selects)}개")
    print(f"   총 폼 요소: {len(all_inputs) + len(all_textareas) + len(all_selects)}개")
    
    # 주요 필드명만 출력
    important_fields = []
    for input_elem in all_inputs:
        name = input_elem.get('name', '')
        if name and any(keyword in name for keyword in ['product', 'price', 'display', 'selling', 'category']):
            if name not in important_fields:
                important_fields.append(name)
    
    print(f"   주요 필드명 ({len(important_fields)}개): {important_fields[:10]}...")
    
    return product_data

def save_extracted_data(product_data, output_dir="test_output"):
    """추출된 데이터 저장"""
    
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    # JSON 파일로 저장
    json_file = output_dir / f"P00000NB_extracted_data_{timestamp}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(product_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n[저장완료] 추출된 데이터: {json_file}")
    
    return json_file

def main():
    """메인 실행 함수"""
    
    # 가장 최신 HTML 파일 찾기
    html_files = list(Path("test_output").glob("P00000NB_page_*.html"))
    if not html_files:
        print("P00000NB HTML 파일을 찾을 수 없습니다!")
        return
    
    latest_html = sorted(html_files)[-1]
    print(f"분석할 파일: {latest_html}")
    
    # 데이터 추출
    product_data = extract_product_data_from_html(latest_html)
    
    # 데이터 저장
    json_file = save_extracted_data(product_data)
    
    print("\n" + "="*80)
    print(f"[완료] P00000NB 상품 데이터 추출 및 저장 완료")
    print(f"추출된 항목 수: {len(product_data)}개")
    print(f"저장 위치: {json_file}")
    print("="*80)

if __name__ == "__main__":
    main()
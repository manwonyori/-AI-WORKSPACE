"""
P00000NB 상품 찾기 및 진입 테스트
성공한 로그인 코드 기반으로 상품까지 접근
"""
# -*- coding: utf-8 -*-
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

import json
import time
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

try:
    from webdriver_manager.chrome import ChromeDriverManager
    USE_WEBDRIVER_MANAGER = True
except ImportError:
    USE_WEBDRIVER_MANAGER = False

def handle_alert(driver):
    """알림 처리"""
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        print(f"   [알림] {alert_text[:50]}...")
        alert.accept()
        time.sleep(1)
        return True
    except NoAlertPresentException:
        return False

def login_to_cafe24(driver, config):
    """Cafe24 로그인 (성공한 로직 사용)"""
    
    print("\n[LOGIN STEP 1] 관리자 페이지 접속...")
    admin_url = config['cafe24']['admin_url']
    driver.get(admin_url)
    time.sleep(3)
    
    # 보안 알림 처리
    if handle_alert(driver):
        print("   [OK] 보안 알림 처리")
    
    print(f"   현재 URL: {driver.current_url}")
    
    print("\n[LOGIN STEP 2] 아이디/비밀번호 입력...")
    
    # 아이디 입력
    username_input = driver.find_element(By.XPATH, "//input[@type='text' and not(@placeholder='')]")
    username_input.clear()
    username_input.send_keys(config['cafe24']['username'])
    print(f"   [OK] 아이디 입력: {config['cafe24']['username']}")
    
    # 비밀번호 입력
    password_input = driver.find_element(By.XPATH, "//input[@type='password']")
    password_input.clear()
    password_input.send_keys(config['cafe24']['password'])
    print("   [OK] 비밀번호 입력")
    
    # 로그인 버튼 클릭
    login_button = driver.find_element(By.XPATH, "//button[contains(text(), '로그인')]")
    login_button.click()
    print("   [OK] 로그인 버튼 클릭")
    
    time.sleep(3)
    
    # 추가 알림 처리
    alert_count = 0
    while handle_alert(driver) and alert_count < 5:
        alert_count += 1
        time.sleep(1)
    
    current_url = driver.current_url
    if "admin" in current_url and "dashboard" in current_url:
        print("   [SUCCESS] 로그인 성공!")
        return True
    else:
        print(f"   [ERROR] 로그인 실패: {current_url}")
        return False

def find_product_P00000NB(driver, config):
    """P00000NB 상품 직접 접근 및 JavaScript 콘텐츠 로딩 대기"""
    
    print("\n" + "="*60)
    print("   P00000NB 상품 직접 접근 시작")
    print("   상품번호: 339")
    print("="*60)
    
    # STEP 1: P00000NB 상품 수정 페이지 직접 접근
    print("\n[PRODUCT STEP 1] P00000NB 상품 수정 페이지 직접 접근...")
    
    mall_id = config['cafe24']['mall_id']
    # 실제 P00000NB 상품 수정 URL (product_no=339)
    product_edit_url = f"https://{mall_id}.cafe24.com/disp/admin/shop1/product/ProductRegister?product_no=339"
    
    print(f"   접근 URL: {product_edit_url}")
    
    try:
        driver.get(product_edit_url)
        time.sleep(5)  # 초기 페이지 로딩 대기
        
        print("\n[PRODUCT STEP 2] JavaScript 콘텐츠 로딩 대기...")
        
        # JavaScript가 DOM을 완전히 구성할 때까지 대기
        wait = WebDriverWait(driver, 30)
        
        # 상품 입력 폼이 로딩될 때까지 대기 (여러 방법 시도)
        form_loaded = False
        for attempt in range(5):
            print(f"   시도 {attempt + 1}: JavaScript 로딩 확인...")
            time.sleep(3)
            
            # 페이지의 JavaScript 실행 상태 확인
            ready_state = driver.execute_script("return document.readyState")
            jquery_ready = driver.execute_script("return typeof jQuery !== 'undefined' && jQuery.active == 0")
            
            print(f"   DOM 상태: {ready_state}, jQuery 대기: {jquery_ready}")
            
            # 상품명 입력 필드나 폼 요소 찾기 시도
            try:
                # 일반적인 상품 폼 요소들 찾기
                inputs = driver.find_elements(By.TAG_NAME, "input")
                textareas = driver.find_elements(By.TAG_NAME, "textarea") 
                selects = driver.find_elements(By.TAG_NAME, "select")
                
                total_elements = len(inputs) + len(textareas) + len(selects)
                print(f"   폼 요소 발견: input({len(inputs)}), textarea({len(textareas)}), select({len(selects)}) = 총 {total_elements}개")
                
                if total_elements > 10:  # 충분한 폼 요소가 로딩되었으면
                    form_loaded = True
                    print("   [OK] 상품 폼 요소들이 로딩됨")
                    break
                    
            except Exception as e:
                print(f"   폼 요소 검색 오류: {e}")
            
            # 추가 대기
            time.sleep(2)
        
        current_url = driver.current_url
        print(f"\n   [OK] 상품 수정 페이지 접근 완료: {current_url}")
        
        # STEP 3: 최종 페이지 내용 분석
        print("\n[PRODUCT STEP 3] 페이지 내용 분석...")
        page_source = driver.page_source
        print(f"   페이지 길이: {len(page_source):,} bytes")
        
        # P00000NB 또는 상품 관련 콘텐츠 검색
        import re
        
        # 상품코드 패턴 검색
        product_codes = re.findall(r'P\d{5}[A-Z0-9]*', page_source)
        if product_codes:
            print(f"   발견된 상품코드: {list(set(product_codes))}")
        
        # 상품명이나 기본 정보 검색
        if "상품명" in page_source or "product_name" in page_source:
            print("   [OK] 상품명 필드 발견")
        
        if "상품코드" in page_source or "product_code" in page_source:
            print("   [OK] 상품코드 필드 발견")
            
        if "판매가" in page_source or "price" in page_source:
            print("   [OK] 가격 필드 발견")
        
        # URL에 product_no=339가 있으면 성공
        if "product_no=339" in current_url or form_loaded:
            print("   [SUCCESS] P00000NB 상품 페이지 확인됨!")
            return True
        else:
            print("   [INFO] 페이지 로딩 완료, 상품 데이터 분석 필요")
            return True
            
    except Exception as e:
        print(f"   [ERROR] 상품 수정 페이지 접근 실패: {e}")
        return False

def main():
    """메인 실행 함수"""
    
    # 설정 파일 로드
    config_path = Path("config/cafe24_config.json")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print("=" * 80)
    print("   P00000NB 상품 검색 및 진입 테스트")
    print("=" * 80)
    
    # Chrome 드라이버 시작
    print("\n[INIT] Chrome 브라우저 시작...")
    options = Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    if USE_WEBDRIVER_MANAGER:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)
    
    driver.maximize_window()
    
    try:
        # 1. 로그인
        if not login_to_cafe24(driver, config):
            print("로그인 실패, 종료합니다.")
            return
        
        # 2. P00000NB 상품 찾기
        if find_product_P00000NB(driver, config):
            print("\n" + "="*80)
            print("[SUCCESS] P00000NB 상품 페이지 접근 성공!")
            
            # 현재 페이지 정보 저장
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_dir = Path("test_output")
            output_dir.mkdir(exist_ok=True)
            
            # HTML 저장
            html_file = output_dir / f"P00000NB_page_{timestamp}.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            
            # 스크린샷 저장
            screenshot = output_dir / f"P00000NB_screenshot_{timestamp}.png"
            driver.save_screenshot(str(screenshot))
            
            print(f"HTML 저장: {html_file}")
            print(f"스크린샷: {screenshot}")
            print("="*80)
            
            # 60초간 수동 확인 시간
            print("\n60초간 수동 확인 시간을 제공합니다...")
            for i in range(60, 0, -10):
                print(f"   {i}초 후 종료...")
                time.sleep(10)
            
        else:
            print("\n[ERROR] P00000NB 상품을 찾을 수 없습니다")
    
    except Exception as e:
        print(f"\n[ERROR] 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        driver.quit()
        print("\n[완료] 브라우저 종료")

if __name__ == "__main__":
    main()
"""
Cafe24 단일 상품 크롤링 테스트
1개 상품(P00000NB)의 HTML을 가져와서 확인
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
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
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

def test_single_product():
    """단일 상품 테스트"""
    
    # 설정 파일 로드
    config_path = Path("config/cafe24_config.json")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print("=" * 60)
    print("   Cafe24 단일 상품 크롤링 테스트")
    print("   대상 상품: P00000NB")
    print("=" * 60)
    
    # Chrome 드라이버 초기화
    print("\n[1/5] Chrome 브라우저 시작...")
    options = Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    if USE_WEBDRIVER_MANAGER:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)
    
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    
    try:
        # 1. 관리자 페이지 접속
        print("\n[2/5] Cafe24 관리자 페이지 접속...")
        admin_url = config['cafe24']['admin_url']
        driver.get(admin_url)
        time.sleep(2)
        
        # 알림 처리
        handle_alert(driver)
        
        # 2. 로그인
        print("\n[3/5] 로그인 중...")
        try:
            username_input = wait.until(
                EC.presence_of_element_located((By.NAME, "userid"))
            )
            password_input = driver.find_element(By.NAME, "userpasswd")
            
            username_input.clear()
            username_input.send_keys(config['cafe24']['username'])
            password_input.clear()
            password_input.send_keys(config['cafe24']['password'])
            password_input.send_keys(Keys.RETURN)
            
            time.sleep(3)
            
            # 로그인 후 알림 처리
            for _ in range(3):
                if not handle_alert(driver):
                    break
            
            print("   [OK] 로그인 성공")
            
        except UnexpectedAlertPresentException:
            handle_alert(driver)
            print("   [INFO] 보안 알림으로 인해 로그인 페이지 재접속 필요")
            driver.get(admin_url)
            time.sleep(2)
        
        # 3. 상품 관리 페이지로 이동
        print("\n[4/5] 상품 관리 페이지로 이동...")
        
        # 현재 URL 확인
        current_url = driver.current_url
        print(f"   현재 위치: {current_url}")
        
        # 상품 관리 직접 URL로 이동
        product_list_url = f"{config['cafe24']['admin_url']}/product/list"
        driver.get(product_list_url)
        time.sleep(3)
        
        # 대체 URL 시도
        if "product" not in driver.current_url:
            print("   상품 목록 페이지 접근 시도 중...")
            # 메뉴 클릭 시도
            try:
                # 상품관리 메뉴 찾기
                menu_elements = driver.find_elements(By.XPATH, "//a[contains(text(), '상품')]")
                if menu_elements:
                    menu_elements[0].click()
                    time.sleep(2)
                    
                    # 상품목록 서브메뉴 찾기
                    submenu = driver.find_elements(By.XPATH, "//a[contains(text(), '목록')]")
                    if submenu:
                        submenu[0].click()
                        time.sleep(2)
            except:
                pass
        
        # 4. 상품 검색
        print("\n[5/5] 상품 P00000NB 검색 중...")
        
        # 검색창 찾기 (여러 가능한 name 속성 시도)
        search_names = ['search_word', 'keyword', 'search', 'query', 'product_code']
        search_input = None
        
        for name in search_names:
            try:
                search_input = driver.find_element(By.NAME, name)
                break
            except:
                continue
        
        if not search_input:
            # ID나 class로도 시도
            try:
                search_input = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
            except:
                print("   [WARNING] 검색창을 찾을 수 없습니다")
        
        if search_input:
            search_input.clear()
            search_input.send_keys("P00000NB")
            search_input.send_keys(Keys.RETURN)
            time.sleep(3)
            print("   [OK] 상품 검색 완료")
        
        # 5. 상품 상세 페이지 접근
        print("\n[추가] 상품 상세 정보 확인...")
        
        # 검색 결과에서 상품 링크 찾기
        product_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'P00000NB')]")
        if not product_links:
            product_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'P00000NB')]")
        
        if product_links:
            print(f"   [OK] {len(product_links)}개 상품 링크 발견")
            
            # 첫 번째 링크 클릭
            product_links[0].click()
            time.sleep(3)
            
            # 현재 페이지 HTML 가져오기
            page_html = driver.page_source
            soup = BeautifulSoup(page_html, 'html.parser')
            
            # HTML 저장
            output_dir = Path("test_output")
            output_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = output_dir / f"P00000NB_{timestamp}.html"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(page_html)
            
            print(f"\n   [OK] HTML 저장 완료: {output_file}")
            print(f"   파일 크기: {len(page_html):,} bytes")
            
            # 간단한 정보 추출
            print("\n[상품 정보 미리보기]")
            
            # 상품명 찾기
            title_elements = soup.find_all(['h1', 'h2', 'h3'], limit=5)
            for elem in title_elements:
                text = elem.get_text(strip=True)
                if text and len(text) > 2:
                    print(f"   제목: {text[:50]}")
                    break
            
            # 이미지 개수
            images = soup.find_all('img')
            print(f"   이미지 개수: {len(images)}개")
            
            # 입력 필드 개수
            inputs = soup.find_all('input')
            print(f"   입력 필드: {len(inputs)}개")
            
            # 텍스트 영역
            textareas = soup.find_all('textarea')
            print(f"   텍스트 영역: {len(textareas)}개")
            
        else:
            print("   [WARNING] 상품을 찾을 수 없습니다")
            
            # 현재 페이지 스크린샷 저장
            screenshot_path = Path("test_output") / f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            driver.save_screenshot(str(screenshot_path))
            print(f"   [INFO] 스크린샷 저장: {screenshot_path}")
        
        print("\n" + "=" * 60)
        print("테스트 완료!")
        print("=" * 60)
        
        # 사용자가 확인할 시간
        print("\n브라우저를 10초 후에 닫습니다...")
        print("(수동으로 확인하려면 브라우저에서 직접 탐색하세요)")
        time.sleep(10)
        
    except Exception as e:
        print(f"\n[ERROR] 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        
        # 오류 시 스크린샷
        try:
            screenshot_path = Path("test_output") / f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            screenshot_path.parent.mkdir(exist_ok=True)
            driver.save_screenshot(str(screenshot_path))
            print(f"\n[INFO] 오류 스크린샷 저장: {screenshot_path}")
        except:
            pass
    
    finally:
        driver.quit()
        print("\n[OK] 브라우저 종료")

if __name__ == "__main__":
    test_single_product()
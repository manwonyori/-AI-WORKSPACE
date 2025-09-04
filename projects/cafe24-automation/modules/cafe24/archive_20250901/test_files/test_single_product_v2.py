"""
Cafe24 단일 상품 크롤링 테스트 v2
새로운 로그인 페이지 형식 대응
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
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException, NoSuchElementException
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

def find_login_inputs(driver):
    """로그인 입력 필드 찾기"""
    username_input = None
    password_input = None
    
    # 다양한 방법으로 입력 필드 찾기
    login_selectors = [
        # 전통적인 방식
        ("name", "userid"),
        ("name", "userpasswd"),
        # placeholder 기반
        ("placeholder", "아이디를 입력해 주세요"),
        ("placeholder", "비밀번호를 입력해 주세요"),
        # type 기반
        ("type", "email"),
        ("type", "password"),
        # ID 기반
        ("id", "userid"),
        ("id", "password"),
        ("id", "username"),
        ("id", "passwd")
    ]
    
    # 아이디 입력 필드
    for method, value in login_selectors[:6]:  # 처음 6개는 아이디용
        try:
            if method == "placeholder":
                username_input = driver.find_element(By.XPATH, f"//input[@placeholder='{value}']")
            else:
                username_input = driver.find_element(By.CSS_SELECTOR, f"input[{method}='{value}']")
            break
        except:
            continue
    
    # 비밀번호 입력 필드
    for method, value in [("type", "password")] + login_selectors:
        try:
            if method == "placeholder":
                password_input = driver.find_element(By.XPATH, f"//input[@placeholder='{value}']")
            elif method == "type" and value == "password":
                password_input = driver.find_element(By.CSS_SELECTOR, f"input[type='password']")
            else:
                password_input = driver.find_element(By.CSS_SELECTOR, f"input[{method}='{value}']")
            break
        except:
            continue
    
    return username_input, password_input

def test_single_product():
    """단일 상품 테스트"""
    
    # 설정 파일 로드
    config_path = Path("config/cafe24_config.json")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print("=" * 60)
    print("   Cafe24 단일 상품 크롤링 테스트 v2")
    print("   대상 상품: P00000NB")
    print("=" * 60)
    
    # Chrome 드라이버 초기화
    print("\n[1/6] Chrome 브라우저 시작...")
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
        print("\n[2/6] Cafe24 관리자 페이지 접속...")
        admin_url = config['cafe24']['admin_url']
        driver.get(admin_url)
        time.sleep(3)
        
        # 알림 처리
        handle_alert(driver)
        
        # 2. 로그인 페이지 확인
        print("\n[3/6] 로그인 페이지 분석...")
        current_url = driver.current_url
        print(f"   현재 URL: {current_url}")
        
        # 페이지 유형 확인
        page_source = driver.page_source
        
        if "대표운영자" in page_source:
            print("   [INFO] 새로운 Cafe24 로그인 페이지 감지")
            
            # 대표운영자 탭 클릭
            try:
                admin_tab = driver.find_element(By.XPATH, "//button[contains(text(), '대표운영자')]")
                admin_tab.click()
                time.sleep(1)
                print("   [OK] 대표운영자 탭 선택")
            except:
                print("   [INFO] 이미 대표운영자 탭이 선택됨")
        
        # 3. 로그인 입력 필드 찾기
        print("\n[4/6] 로그인 정보 입력...")
        
        username_input, password_input = find_login_inputs(driver)
        
        if not username_input or not password_input:
            print("   [ERROR] 로그인 필드를 찾을 수 없습니다")
            
            # 모든 입력 필드 출력 (디버깅)
            all_inputs = driver.find_elements(By.TAG_NAME, "input")
            print(f"   [DEBUG] 총 {len(all_inputs)}개 입력 필드 발견:")
            for i, inp in enumerate(all_inputs):
                name = inp.get_attribute('name') or 'None'
                placeholder = inp.get_attribute('placeholder') or 'None'
                input_type = inp.get_attribute('type') or 'None'
                print(f"     {i+1}. name='{name}' placeholder='{placeholder}' type='{input_type}'")
            
            return False
        
        # 로그인 정보 입력
        try:
            username_input.clear()
            username_input.send_keys(config['cafe24']['username'])
            
            password_input.clear() 
            password_input.send_keys(config['cafe24']['password'])
            
            print("   [OK] 로그인 정보 입력 완료")
        except Exception as e:
            print(f"   [ERROR] 입력 실패: {e}")
            return False
        
        # 4. 로그인 버튼 클릭
        try:
            # 로그인 버튼 찾기
            login_button = None
            login_selectors = [
                "//button[contains(text(), '로그인')]",
                "//input[@type='submit']",
                "//button[@type='submit']",
                "//input[@value='로그인']"
            ]
            
            for selector in login_selectors:
                try:
                    login_button = driver.find_element(By.XPATH, selector)
                    break
                except:
                    continue
            
            if login_button:
                login_button.click()
                print("   [OK] 로그인 버튼 클릭")
            else:
                # Enter 키로 시도
                password_input.send_keys(Keys.RETURN)
                print("   [OK] Enter 키로 로그인")
            
            time.sleep(4)
            
        except Exception as e:
            print(f"   [ERROR] 로그인 실행 실패: {e}")
        
        # 5. 로그인 후 처리
        print("\n[5/6] 로그인 결과 확인...")
        
        # 추가 알림 처리
        for _ in range(3):
            if not handle_alert(driver):
                break
        
        # 현재 상태 확인
        time.sleep(2)
        current_url = driver.current_url
        page_title = driver.title
        
        print(f"   현재 URL: {current_url}")
        print(f"   페이지 제목: {page_title}")
        
        # 관리자 페이지 접근 확인
        admin_indicators = ["admin", "manage", "관리", "dashboard"]
        is_admin = any(indicator in current_url.lower() or indicator in page_title for indicator in admin_indicators)
        
        if is_admin:
            print("   [SUCCESS] 관리자 페이지 로그인 성공!")
            
            # 6. 상품 관리로 이동
            print("\n[6/6] 상품 관리 페이지 접근...")
            
            # 직접 상품 관리 URL로 이동
            mall_id = config['cafe24']['mall_id']
            product_manage_urls = [
                f"https://{mall_id}.cafe24.com/disp/admin/shop1/product",
                f"https://echosting.cafe24.com/disp/admin/shop1/product/Product_list",
                current_url.replace('/admin', '/disp/admin/shop1/product')
            ]
            
            for url in product_manage_urls:
                try:
                    driver.get(url)
                    time.sleep(3)
                    
                    if "product" in driver.current_url.lower():
                        print(f"   [OK] 상품 관리 페이지 접근 성공: {driver.current_url}")
                        break
                        
                except Exception as e:
                    print(f"   [WARNING] URL 시도 실패: {url[:50]}...")
                    continue
            
            # 현재 페이지 HTML 저장
            page_html = driver.page_source
            
            # 결과 저장
            output_dir = Path("test_output")
            output_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = output_dir / f"cafe24_admin_{timestamp}.html"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(page_html)
            
            print(f"\n[결과] HTML 저장: {output_file}")
            print(f"   파일 크기: {len(page_html):,} bytes")
            
            # 페이지 분석
            soup = BeautifulSoup(page_html, 'html.parser')
            
            # 상품 관련 링크 찾기
            product_links = soup.find_all('a', href=lambda x: x and ('product' in x.lower() or '상품' in x))
            if product_links:
                print(f"   [분석] {len(product_links)}개 상품 관련 링크 발견")
                
                for i, link in enumerate(product_links[:5]):  # 처음 5개만
                    text = link.get_text(strip=True)
                    href = link.get('href', '')
                    if text:
                        print(f"     {i+1}. {text[:30]} -> {href[:50]}")
            
            # 입력 필드 분석
            inputs = soup.find_all('input')
            textareas = soup.find_all('textarea')
            
            print(f"   [분석] 입력 필드 {len(inputs)}개, 텍스트 영역 {len(textareas)}개")
            
        else:
            print("   [WARNING] 아직 일반 페이지에 있습니다")
            print("   추가 인증이나 단계가 필요할 수 있습니다")
        
        print("\n" + "=" * 60)
        print("테스트 완료! 브라우저를 15초 후에 닫습니다.")
        print("(수동으로 확인하려면 브라우저를 그대로 두세요)")
        print("=" * 60)
        
        time.sleep(15)
        
    except Exception as e:
        print(f"\n[ERROR] 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        
        # 오류 시 스크린샷
        try:
            screenshot_path = Path("test_output") / f"error_v2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            screenshot_path.parent.mkdir(exist_ok=True)
            driver.save_screenshot(str(screenshot_path))
            print(f"\n[INFO] 오류 스크린샷: {screenshot_path}")
        except:
            pass
    
    finally:
        driver.quit()
        print("\n[OK] 브라우저 종료")

if __name__ == "__main__":
    test_single_product()
"""
Cafe24 단계별 로그인 테스트 - 함께 수정하기
각 단계를 하나씩 확인하며 진행
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
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains

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
        print(f"   [알림 처리] {alert_text[:50]}...")
        alert.accept()
        time.sleep(1)
        return True
    except NoAlertPresentException:
        return False

def step_by_step_login():
    """단계별 로그인"""
    
    # 설정 파일 로드
    config_path = Path("config/cafe24_config.json")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print("=" * 60)
    print("   Cafe24 단계별 로그인 테스트")
    print("   각 단계를 확인하며 진행")
    print("=" * 60)
    
    # STEP 1: Chrome 시작
    print("\n[STEP 1] Chrome 드라이버 시작...")
    options = Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    if USE_WEBDRIVER_MANAGER:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)
    
    driver.maximize_window()
    print("   [OK] Chrome 시작 완료")
    
    try:
        # STEP 2: 페이지 접속
        print("\n[STEP 2] 관리자 페이지 접속...")
        admin_url = config['cafe24']['admin_url']
        print(f"   접속 URL: {admin_url}")
        
        driver.get(admin_url)
        time.sleep(3)
        print("   [OK] 페이지 로드 완료")
        
        # STEP 3: 보안 알림 처리
        print("\n[STEP 3] 보안 알림 확인...")
        if handle_alert(driver):
            print("   [OK] 보안 알림 처리 완료")
        else:
            print("   [OK] 보안 알림 없음")
        
        # STEP 4: 현재 페이지 상태 확인
        print("\n[STEP 4] 현재 페이지 상태...")
        current_url = driver.current_url
        page_title = driver.title
        print(f"   현재 URL: {current_url}")
        print(f"   페이지 제목: {page_title}")
        
        # STEP 5: 로그인 탭 확인 (필요시)
        print("\n[STEP 5] 로그인 탭 확인...")
        page_source = driver.page_source
        
        if "대표운영자" in page_source:
            print("   대표운영자 탭 감지됨")
            try:
                admin_tab = driver.find_element(By.XPATH, "//button[contains(text(), '대표운영자')]")
                if "active" not in admin_tab.get_attribute("class"):
                    admin_tab.click()
                    print("   [OK] 대표운영자 탭 선택")
                else:
                    print("   [OK] 이미 대표운영자 탭 활성화")
                time.sleep(1)
            except:
                print("   [OK] 탭 선택 생략")
        
        # STEP 6: 아이디/비밀번호 입력 단계
        print("\n[STEP 6] 아이디/비밀번호 입력...")
        
        # 아이디 입력 필드 찾기
        print("   아이디 입력 필드 찾는 중...")
        username_input = None
        
        # 여러 방법으로 아이디 필드 찾기 시도
        username_selectors = [
            ("xpath", "//input[@placeholder='아이디를 입력해 주세요']"),
            ("name", "userid"),
            ("xpath", "//input[@type='text' and not(@placeholder='')]"),
            ("css", "input[type='text']")
        ]
        
        for method, selector in username_selectors:
            try:
                if method == "xpath":
                    username_input = driver.find_element(By.XPATH, selector)
                elif method == "name":
                    username_input = driver.find_element(By.NAME, selector)
                elif method == "css":
                    username_input = driver.find_element(By.CSS_SELECTOR, selector)
                
                if username_input and username_input.is_displayed():
                    print(f"   [OK] 아이디 필드 발견: {method}='{selector}'")
                    break
                else:
                    username_input = None
            except:
                continue
        
        # 비밀번호 입력 필드 찾기
        print("   비밀번호 입력 필드 찾는 중...")
        password_input = None
        
        try:
            password_input = driver.find_element(By.XPATH, "//input[@type='password']")
            if password_input.is_displayed():
                print("   [OK] 비밀번호 필드 발견")
        except:
            print("   [ERROR] 비밀번호 필드를 찾을 수 없습니다")
        
        # 입력 필드 확인 후 계속 진행 여부 결정
        if username_input and password_input:
            print("\n   로그인 필드를 성공적으로 찾았습니다!")
            print("   다음 단계로 진행하시겠습니까?")
            
            # STEP 7: 실제 아이디 입력
            print("\n[STEP 7] 아이디 입력 시작...")
            
            try:
                # 아이디 필드 클릭
                ActionChains(driver).click(username_input).perform()
                time.sleep(0.5)
                
                # 기존 내용 지우기
                username_input.clear()
                time.sleep(0.5)
                
                # 아이디 입력
                username = config['cafe24']['username']
                username_input.send_keys(username)
                time.sleep(1)
                
                print(f"   [OK] 아이디 입력 완료: {username}")
                
            except Exception as e:
                print(f"   [ERROR] 아이디 입력 실패: {e}")
            
            # STEP 8: 비밀번호 입력
            print("\n[STEP 8] 비밀번호 입력 시작...")
            
            try:
                # 비밀번호 필드 클릭
                ActionChains(driver).click(password_input).perform()
                time.sleep(0.5)
                
                # 기존 내용 지우기
                password_input.clear()
                time.sleep(0.5)
                
                # 비밀번호 입력
                password = config['cafe24']['password']
                password_input.send_keys(password)
                time.sleep(1)
                
                print("   [OK] 비밀번호 입력 완료")
                
            except Exception as e:
                print(f"   [ERROR] 비밀번호 입력 실패: {e}")
            
            # STEP 9: 로그인 버튼 찾기 및 클릭 준비
            print("\n[STEP 9] 로그인 버튼 찾는 중...")
            
            login_button = None
            login_selectors = [
                ("xpath", "//button[contains(text(), '로그인')]"),
                ("xpath", "//input[@value='로그인']"),
                ("xpath", "//button[@type='submit']"),
                ("css", "button[type='submit']")
            ]
            
            for method, selector in login_selectors:
                try:
                    if method == "xpath":
                        login_button = driver.find_element(By.XPATH, selector)
                    elif method == "css":
                        login_button = driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if login_button and login_button.is_displayed():
                        print(f"   [OK] 로그인 버튼 발견: {method}='{selector}'")
                        break
                    else:
                        login_button = None
                except:
                    continue
            
            if login_button:
                print("\n[확인] 로그인 정보 입력 완료!")
                print("로그인 버튼을 클릭하시겠습니까?")
                
                # STEP 10: 로그인 버튼 클릭
                print("\n[STEP 10] 로그인 버튼 클릭...")
                
                try:
                    login_button.click()
                    print("   [OK] 로그인 버튼 클릭 완료")
                    time.sleep(3)
                    
                except Exception as e:
                    print(f"   [ERROR] 로그인 버튼 클릭 실패: {e}")
                    
                    # Enter 키로 대체 시도
                    try:
                        password_input.send_keys(Keys.RETURN)
                        print("   [OK] Enter 키로 로그인 시도")
                        time.sleep(3)
                    except:
                        print("   [ERROR] Enter 키도 실패")
                
                # STEP 11: 로그인 후 처리
                print("\n[STEP 11] 로그인 후 상태 확인...")
                
                # 추가 알림 처리
                alert_count = 0
                while handle_alert(driver) and alert_count < 5:
                    alert_count += 1
                    time.sleep(1)
                
                if alert_count > 0:
                    print(f"   [OK] {alert_count}개 추가 알림 처리 완료")
                
                # 현재 상태 확인
                time.sleep(2)
                current_url = driver.current_url
                page_title = driver.title
                
                print(f"   현재 URL: {current_url}")
                print(f"   페이지 제목: {page_title}")
                
                # 로그인 성공 여부 판단
                success_indicators = [
                    "admin", "관리", "dashboard", "상품", "product", 
                    "logout", "로그아웃", "main", "home"
                ]
                
                page_source = driver.page_source.lower()
                found_indicators = [indicator for indicator in success_indicators 
                                  if indicator in page_source or indicator in current_url.lower()]
                
                if found_indicators:
                    print("\n[SUCCESS] 로그인 성공!")
                    print(f"   감지된 요소: {', '.join(found_indicators)}")
                    
                    # STEP 12: 관리자 페이지 접근 시도
                    print("\n[STEP 12] 관리자 페이지 접근 시도...")
                    
                    # 상품 관리 URL 시도
                    mall_id = config['cafe24']['mall_id']
                    product_urls = [
                        f"https://{mall_id}.cafe24.com/disp/admin/shop1/product",
                        f"https://echosting.cafe24.com/disp/admin/shop1/product/Product_list",
                        current_url.replace('/Shop/', '/admin/shop1/product/')
                    ]
                    
                    for url in product_urls:
                        try:
                            print(f"   상품 관리 URL 시도: {url[:50]}...")
                            driver.get(url)
                            time.sleep(3)
                            
                            if "product" in driver.current_url.lower() or "상품" in driver.page_source:
                                print("   [SUCCESS] 상품 관리 페이지 접근 성공!")
                                break
                                
                        except Exception as e:
                            print(f"   [WARNING] URL 접근 실패: {str(e)[:50]}...")
                            continue
                    
                else:
                    print("\n[WARNING] 로그인 상태가 명확하지 않습니다")
                    print("   수동으로 확인이 필요할 수 있습니다")
                
                # 최종 결과 저장
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                output_dir = Path("test_output")
                output_dir.mkdir(exist_ok=True)
                
                # HTML 저장
                final_html = output_dir / f"final_result_{timestamp}.html"
                with open(final_html, 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
                
                # 스크린샷 저장
                screenshot = output_dir / f"final_screenshot_{timestamp}.png"
                driver.save_screenshot(str(screenshot))
                
                print(f"\n[결과 저장]")
                print(f"   HTML: {final_html}")
                print(f"   스크린샷: {screenshot}")
                
                # 최종 대기
                print("\n[최종] 30초간 수동 확인 시간...")
                for i in range(30, 0, -5):
                    print(f"   {i}초 후 종료...")
                    time.sleep(5)
            else:
                print("\n[ERROR] 로그인 버튼을 찾을 수 없습니다")
                print("Enter 키로 시도합니다...")
                
                try:
                    password_input.send_keys(Keys.RETURN)
                    print("   [OK] Enter 키로 로그인 시도 완료")
                    time.sleep(3)
                    
                    # 이후 처리는 동일하게 진행
                    print("\n[STEP 11] 로그인 후 상태 확인...")
                    
                    # 추가 알림 처리
                    alert_count = 0
                    while handle_alert(driver) and alert_count < 5:
                        alert_count += 1
                        time.sleep(1)
                    
                    print(f"   현재 URL: {driver.current_url}")
                    print("   Enter 키 로그인 시도 완료")
                    
                except Exception as e:
                    print(f"   [ERROR] Enter 키도 실패: {e}")
                
                # 30초간 수동 확인
                print("\n[수동확인] 30초간 확인 시간...")
                for i in range(30, 0, -5):
                    print(f"   {i}초 후 종료...")
                    time.sleep(5)
        else:
            print("\n[ERROR] 입력 필드를 찾지 못했습니다.")
            print("   수동으로 확인해주세요.")
            
            # 60초간 대기
            for i in range(60, 0, -10):
                print(f"   {i}초 후 종료...")
                time.sleep(10)
        
    except Exception as e:
        print(f"\n[ERROR] 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        driver.quit()
        print("\n[완료] 브라우저 종료")

if __name__ == "__main__":
    step_by_step_login()
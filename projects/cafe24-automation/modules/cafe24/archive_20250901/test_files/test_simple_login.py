"""
Cafe24 단순 로그인 테스트
수동으로 확인할 수 있도록 긴 대기 시간 설정
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
        print(f"   [알림] {alert_text[:100]}...")
        alert.accept()
        time.sleep(1)
        return True
    except NoAlertPresentException:
        return False

def main():
    # 설정 파일 로드
    config_path = Path("config/cafe24_config.json")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print("=" * 70)
    print("   Cafe24 수동 확인 테스트")
    print("   로그인 과정을 천천히 진행하여 수동 확인 가능")
    print("=" * 70)
    
    print(f"\n[설정 정보]")
    print(f"Mall ID: {config['cafe24']['mall_id']}")
    print(f"Username: {config['cafe24']['username']}")
    print(f"Admin URL: {config['cafe24']['admin_url']}")
    
    # Chrome 드라이버 시작
    print(f"\n[1] Chrome 브라우저 시작...")
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
        # 관리자 페이지 접속
        print(f"\n[2] 관리자 페이지 접속 중...")
        admin_url = config['cafe24']['admin_url']
        driver.get(admin_url)
        time.sleep(3)
        
        # 보안 알림 처리
        if handle_alert(driver):
            print("   [OK] 보안 알림 처리됨")
        
        print(f"\n[3] 현재 페이지 상태:")
        print(f"   URL: {driver.current_url}")
        print(f"   Title: {driver.title}")
        
        # 로그인 시도
        print(f"\n[4] 로그인 시도...")
        
        # 아이디 입력 시도
        username_selectors = [
            "//input[@placeholder='아이디를 입력해 주세요']",
            "//input[@name='userid']",
            "//input[@type='text']",
            "//input[@type='email']"
        ]
        
        username_input = None
        for selector in username_selectors:
            try:
                username_input = driver.find_element(By.XPATH, selector)
                print(f"   [OK] 아이디 입력창 발견: {selector}")
                break
            except:
                continue
        
        if username_input:
            try:
                # 클릭으로 포커스
                ActionChains(driver).click(username_input).perform()
                time.sleep(0.5)
                
                # 기존 내용 지우기
                username_input.clear()
                time.sleep(0.5)
                
                # JavaScript로 값 설정
                driver.execute_script(f"arguments[0].value = '{config['cafe24']['username']}';", username_input)
                
                print(f"   [OK] 아이디 입력 성공")
                
            except Exception as e:
                print(f"   [ERROR] 아이디 입력 실패: {e}")
        
        # 비밀번호 입력 시도
        password_selectors = [
            "//input[@placeholder='비밀번호를 입력해 주세요']",
            "//input[@name='userpasswd']",
            "//input[@type='password']"
        ]
        
        password_input = None
        for selector in password_selectors:
            try:
                password_input = driver.find_element(By.XPATH, selector)
                print(f"   [OK] 비밀번호 입력창 발견: {selector}")
                break
            except:
                continue
        
        if password_input:
            try:
                # 클릭으로 포커스
                ActionChains(driver).click(password_input).perform()
                time.sleep(0.5)
                
                # 기존 내용 지우기  
                password_input.clear()
                time.sleep(0.5)
                
                # JavaScript로 값 설정
                driver.execute_script(f"arguments[0].value = '{config['cafe24']['password']}';", password_input)
                
                print(f"   [OK] 비밀번호 입력 성공")
                
            except Exception as e:
                print(f"   [ERROR] 비밀번호 입력 실패: {e}")
        
        # 로그인 버튼 클릭
        print(f"\n[5] 로그인 버튼 클릭...")
        
        login_selectors = [
            "//button[contains(text(), '로그인')]",
            "//input[@value='로그인']",
            "//button[@type='submit']"
        ]
        
        login_clicked = False
        for selector in login_selectors:
            try:
                login_btn = driver.find_element(By.XPATH, selector)
                login_btn.click()
                print(f"   [OK] 로그인 버튼 클릭됨: {selector}")
                login_clicked = True
                break
            except:
                continue
        
        if not login_clicked:
            print("   [INFO] Enter 키로 시도...")
            if password_input:
                password_input.send_keys(Keys.RETURN)
        
        # 로그인 후 대기
        print(f"\n[6] 로그인 처리 대기 중...")
        time.sleep(5)
        
        # 추가 알림 처리
        alert_count = 0
        while handle_alert(driver) and alert_count < 5:
            alert_count += 1
            time.sleep(1)
        
        # 결과 확인
        print(f"\n[7] 로그인 결과:")
        print(f"   현재 URL: {driver.current_url}")
        print(f"   페이지 제목: {driver.title}")
        
        # 페이지 소스에서 성공 지표 찾기
        page_source = driver.page_source
        success_indicators = ["관리자", "admin", "dashboard", "상품", "product", "로그아웃", "logout"]
        
        found_indicators = []
        for indicator in success_indicators:
            if indicator in page_source:
                found_indicators.append(indicator)
        
        if found_indicators:
            print(f"   [SUCCESS] 관리자 페이지 접근 성공!")
            print(f"   발견된 요소: {', '.join(found_indicators)}")
        else:
            print(f"   [WARNING] 아직 로그인이 완전히 되지 않았을 수 있습니다")
        
        # HTML 저장
        output_dir = Path("test_output")
        output_dir.mkdir(exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        html_file = output_dir / f"login_result_{timestamp}.html"
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(page_source)
        
        print(f"\n[8] 결과 저장: {html_file}")
        print(f"   파일 크기: {len(page_source):,} bytes")
        
        # 스크린샷
        screenshot_file = output_dir / f"screenshot_{timestamp}.png"
        driver.save_screenshot(str(screenshot_file))
        print(f"   스크린샷: {screenshot_file}")
        
        print(f"\n" + "=" * 70)
        print("   수동 확인을 위해 브라우저를 30초간 유지합니다.")
        print("   필요시 직접 브라우저에서 작업을 계속하세요.")
        print("=" * 70)
        
        # 30초 대기 (수동 확인용)
        for i in range(30, 0, -5):
            print(f"   {i}초 후 자동 종료...")
            time.sleep(5)
        
    except Exception as e:
        print(f"\n[ERROR] 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print(f"\n[완료] 브라우저 종료")
        driver.quit()

if __name__ == "__main__":
    main()
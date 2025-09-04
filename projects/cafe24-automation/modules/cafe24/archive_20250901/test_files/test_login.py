"""
Cafe24 로그인 테스트 스크립트
설정이 올바른지 확인하는 용도
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

def test_login():
    """Cafe24 로그인 테스트"""
    
    # 설정 파일 로드
    config_path = Path("config/cafe24_config.json")
    if not config_path.exists():
        print("[ERROR] 설정 파일이 없습니다: config/cafe24_config.json")
        return False
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 로그인 정보 확인
    username = config['cafe24']['username']
    password = config['cafe24']['password']
    
    if username == "your_username" or password == "your_password":
        print("[ERROR] 로그인 정보를 입력해주세요!")
        print("   config/cafe24_config.json 파일을 열어서")
        print("   username과 password를 실제 정보로 수정하세요.")
        return False
    
    print("[OK] 설정 파일 확인 완료")
    print(f"   Mall ID: {config['cafe24']['mall_id']}")
    print(f"   Admin URL: {config['cafe24']['admin_url']}")
    print(f"   Username: {username[:3]}***")
    
    # Chrome 드라이버 초기화
    print("\n[INFO] Chrome 브라우저 시작...")
    
    try:
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
        
        print("[OK] Chrome 드라이버 초기화 성공")
        
    except Exception as e:
        print(f"[ERROR] Chrome 드라이버 초기화 실패: {e}")
        print("\n해결방법:")
        print("1. Chrome 브라우저가 설치되어 있는지 확인")
        print("2. ChromeDriver를 다운로드하여 현재 폴더에 복사")
        print("   https://chromedriver.chromium.org/downloads")
        return False
    
    try:
        # Cafe24 관리자 페이지 접속
        print(f"\n[INFO] Cafe24 관리자 페이지 접속 중...")
        admin_url = config['cafe24']['admin_url']
        driver.get(admin_url)
        time.sleep(2)
        
        print("[OK] 페이지 로드 완료")
        
        # 로그인 폼 찾기
        print("\n[INFO] 로그인 시도 중...")
        
        # 기존 알림이 있으면 처리
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except:
            pass
        
        username_input = wait.until(
            EC.presence_of_element_located((By.NAME, "userid"))
        )
        password_input = driver.find_element(By.NAME, "userpasswd")
        
        # 자격증명 입력
        username_input.clear()
        username_input.send_keys(username)
        
        password_input.clear()
        password_input.send_keys(password)
        
        print("   아이디/비밀번호 입력 완료")
        
        # 로그인 버튼 클릭
        password_input.send_keys(Keys.RETURN)
        
        print("   로그인 버튼 클릭")
        time.sleep(3)
        
        # 보안 알림 처리
        try:
            alert = driver.switch_to.alert
            alert_text = alert.text
            print(f"   [INFO] 보안 알림 메시지 감지")
            alert.accept()  # 확인 버튼 클릭
            print("   [OK] 보안 알림 처리 완료")
            time.sleep(2)
        except:
            pass  # 알림이 없으면 계속 진행
        
        # 로그인 성공 확인
        current_url = driver.current_url
        if "admin/php/shop1" in current_url or "admin/product" in current_url:
            print("\n[SUCCESS] 로그인 성공!")
            print(f"   현재 URL: {current_url}")
            
            # 상품 메뉴 확인
            try:
                product_menu = driver.find_element(By.XPATH, "//a[contains(text(), '상품관리')]")
                print("\n[OK] 상품관리 메뉴 확인 완료")
                
                # 상품 개수 확인 시도
                product_menu.click()
                time.sleep(1)
                
                product_list = driver.find_element(By.XPATH, "//a[contains(text(), '상품목록')]")
                product_list.click()
                time.sleep(2)
                
                print("[OK] 상품 목록 페이지 접근 성공")
                
            except:
                print("[WARNING] 상품 메뉴 확인 실패 (권한 문제일 수 있음)")
            
            return True
            
        else:
            print(f"\n[ERROR] 로그인 실패")
            print(f"   현재 URL: {current_url}")
            print("\n가능한 원인:")
            print("1. 아이디/비밀번호가 올바르지 않음")
            print("2. 계정이 잠겨있거나 비활성화됨")
            print("3. IP 제한이 설정되어 있음")
            return False
            
    except Exception as e:
        print(f"\n[ERROR] 오류 발생: {e}")
        return False
        
    finally:
        print("\n[INFO] 5초 후 브라우저를 닫습니다...")
        time.sleep(5)
        driver.quit()
        print("[OK] 테스트 완료")

if __name__ == "__main__":
    print("=" * 50)
    print("   Cafe24 로그인 테스트")
    print("=" * 50)
    
    success = test_login()
    
    if success:
        print("\n" + "=" * 50)
        print("[SUCCESS] 모든 테스트 통과!")
        print("다음 단계로 진행하세요.")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("[ERROR] 테스트 실패")
        print("위의 오류 메시지를 확인하고 문제를 해결하세요.")
        print("=" * 50)
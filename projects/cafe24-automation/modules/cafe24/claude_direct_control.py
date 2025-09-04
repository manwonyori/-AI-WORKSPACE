# -*- coding: utf-8 -*-
"""
Claude 직접 카페24 제어 시스템
Claude가 실시간으로 카페24를 제어할 수 있는 인터페이스
"""
import os
import sys
import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

class ClaudeDirectControl:
    """Claude가 직접 카페24를 제어하는 클래스"""
    
    def __init__(self):
        """초기화"""
        self.driver = None
        self.wait = None
        self.config_file = "C:\\Users\\8899y\\CUA-MASTER\\modules\\cafe24\\config\\cafe24_config.json"
        self.load_config()
        
        print("=" * 50)
        print("🤖 Claude 직접 카페24 제어 시스템 시작")
        print("=" * 50)
        
    def load_config(self):
        """설정 파일 로드"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            print(f"✅ 설정 로드 완료: {self.config['cafe24']['mall_id']}")
        except Exception as e:
            print(f"❌ 설정 로드 실패: {e}")
            sys.exit(1)
    
    def setup_driver(self):
        """브라우저 설정 및 시작"""
        try:
            # Chrome 옵션 설정
            options = Options()
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            
            # 기존 Chrome 창 사용하도록 설정
            options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            
            try:
                # 기존 Chrome에 연결 시도
                self.driver = webdriver.Chrome(options=options)
                print("✅ 기존 Chrome 브라우저에 연결 성공")
            except:
                # 새 Chrome 시작
                options = Options()
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                self.driver = webdriver.Chrome(options=options)
                print("✅ 새 Chrome 브라우저 시작")
                
            self.wait = WebDriverWait(self.driver, 10)
            return True
            
        except Exception as e:
            print(f"❌ 브라우저 설정 실패: {e}")
            return False
    
    def check_login_status(self):
        """로그인 상태 확인"""
        try:
            current_url = self.driver.current_url
            print(f"📍 현재 URL: {current_url}")
            
            if "admin" in current_url and "cafe24.com" in current_url:
                print("✅ 카페24 관리자 페이지에 접속 중")
                return True
            else:
                print("❌ 카페24 관리자 페이지가 아님")
                return False
                
        except Exception as e:
            print(f"❌ 로그인 상태 확인 실패: {e}")
            return False
    
    def login_to_cafe24(self):
        """카페24 로그인"""
        try:
            print("🔐 카페24 로그인 시작...")
            
            # 로그인 페이지로 이동
            login_url = self.config['cafe24']['admin_url']
            self.driver.get(login_url)
            time.sleep(3)
            
            # 로그인 폼 찾기 및 입력
            username = self.config['cafe24']['username']
            password = self.config['cafe24']['password']
            
            # 아이디 입력
            username_field = self.wait.until(EC.presence_of_element_located((By.NAME, "mall_id")))
            username_field.clear()
            username_field.send_keys(username)
            
            # 비밀번호 입력
            password_field = self.driver.find_element(By.NAME, "userpasswd")
            password_field.clear()
            password_field.send_keys(password)
            
            # 로그인 버튼 클릭
            login_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
            login_button.click()
            
            time.sleep(5)
            
            # 로그인 성공 확인
            if self.check_login_status():
                print("✅ 카페24 로그인 성공")
                return True
            else:
                print("❌ 카페24 로그인 실패")
                return False
                
        except Exception as e:
            print(f"❌ 로그인 중 오류: {e}")
            return False
    
    def navigate_to_products(self):
        """상품 관리 페이지로 이동"""
        try:
            print("📦 상품 관리 페이지로 이동...")
            
            # 상품 관리 메뉴 클릭
            product_menu = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '상품관리')]")))
            product_menu.click()
            time.sleep(2)
            
            # 상품 목록 클릭
            product_list = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '상품목록')]")))
            product_list.click()
            time.sleep(3)
            
            print("✅ 상품 목록 페이지 접근 성공")
            return True
            
        except Exception as e:
            print(f"❌ 상품 페이지 이동 실패: {e}")
            return False
    
    def get_product_list(self):
        """상품 목록 정보 수집"""
        try:
            print("📋 상품 목록 정보 수집 중...")
            
            # 상품 테이블 찾기
            product_table = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            rows = product_table.find_elements(By.TAG_NAME, "tr")
            
            products = []
            for i, row in enumerate(rows[1:6]):  # 처음 5개만 수집
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 3:
                    product_info = {
                        'index': i + 1,
                        'name': cells[2].text.strip() if len(cells) > 2 else "N/A",
                        'status': cells[1].text.strip() if len(cells) > 1 else "N/A"
                    }
                    products.append(product_info)
            
            print(f"✅ 상품 {len(products)}개 정보 수집 완료")
            for product in products:
                print(f"  - {product['index']}: {product['name'][:30]}...")
                
            return products
            
        except Exception as e:
            print(f"❌ 상품 목록 수집 실패: {e}")
            return []
    
    def click_first_product(self):
        """첫 번째 상품 편집 페이지로 이동"""
        try:
            print("🎯 첫 번째 상품 편집...")
            
            # 첫 번째 상품의 편집 버튼 찾기
            edit_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '수정')]")))
            edit_button.click()
            time.sleep(5)
            
            print("✅ 상품 편집 페이지 접근 성공")
            return True
            
        except Exception as e:
            print(f"❌ 상품 편집 페이지 접근 실패: {e}")
            return False
    
    def take_screenshot(self, filename=None):
        """스크린샷 촬영"""
        try:
            if not filename:
                filename = f"cafe24_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            screenshot_path = f"C:\\Users\\8899y\\CUA-MASTER\\modules\\cafe24\\logs\\{filename}"
            self.driver.save_screenshot(screenshot_path)
            print(f"📸 스크린샷 저장: {screenshot_path}")
            return screenshot_path
            
        except Exception as e:
            print(f"❌ 스크린샷 실패: {e}")
            return None
    
    def execute_command(self, command):
        """명령어 실행"""
        try:
            print(f"⚡ 명령어 실행: {command}")
            
            if command == "login":
                return self.login_to_cafe24()
            elif command == "products":
                return self.navigate_to_products()
            elif command == "list":
                return self.get_product_list()
            elif command == "edit":
                return self.click_first_product()
            elif command == "screenshot":
                return self.take_screenshot()
            elif command == "status":
                return self.check_login_status()
            else:
                print(f"❌ 알 수 없는 명령어: {command}")
                return False
                
        except Exception as e:
            print(f"❌ 명령어 실행 실패: {e}")
            return False
    
    def close(self):
        """브라우저 종료"""
        if self.driver:
            self.driver.quit()
            print("🔚 브라우저 종료")

def main():
    """메인 실행 함수"""
    controller = ClaudeDirectControl()
    
    try:
        # 1. 브라우저 설정
        if not controller.setup_driver():
            return
        
        # 2. 현재 상태 확인
        controller.execute_command("status")
        
        # 3. 스크린샷 촬영
        controller.execute_command("screenshot")
        
        # 4. 상품 페이지로 이동
        if not controller.execute_command("products"):
            # 로그인이 필요하면 로그인 시도
            controller.execute_command("login")
            controller.execute_command("products")
        
        # 5. 상품 목록 수집
        controller.execute_command("list")
        
        print("\n" + "=" * 50)
        print("✅ Claude 직접 제어 테스트 완료")
        print("=" * 50)
        
    except KeyboardInterrupt:
        print("\n⚠️ 사용자에 의해 중단됨")
    except Exception as e:
        print(f"❌ 실행 중 오류: {e}")
    finally:
        # controller.close()  # 기존 브라우저 유지
        pass

if __name__ == "__main__":
    main()

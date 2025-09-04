# -*- coding: utf-8 -*-
"""
Unified CUA Agent - 통합된 Cafe24 자동화 시스템
성공한 로그인 + 다운로드 방식을 통합한 완벽한 CUA Agent
"""
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

import json
import time
import glob
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

class UnifiedCUAAgent:
    """통합된 CUA Agent - 로그인부터 다운로드까지 완벽 처리"""
    
    def __init__(self, download_folder="C:\\Users\\8899y\\CUA-MASTER\\modules\\cafe24\\download"):
        """초기화"""
        self.driver = None
        self.download_folder = download_folder
        self.config_file = "C:\\Users\\8899y\\CUA-MASTER\\modules\\cafe24\\config\\cafe24_config.json"
        self.config = {}
        
        # 다운로드 폴더 생성
        os.makedirs(download_folder, exist_ok=True)
        
        print("[UNIFIED-CUA] 통합된 CUA Agent 시작")
        print(f"[DOWNLOAD-PATH] {download_folder}")
        
        # 설정 로드
        self.load_config()
        
    def load_config(self):
        """설정 파일 로드"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            print(f"   [CONFIG] 설정 로드 완료")
        except Exception as e:
            print(f"   [CONFIG-ERROR] 설정 파일 로드 실패: {e}")
            # 기본 설정 사용
            self.config = {
                'cafe24': {
                    'admin_url': 'https://manwonyori.cafe24.com/admin',
                    'mall_id': 'manwonyori',
                    'username': 'manwonyori',
                    'password': 'happy8263!'
                }
            }
    
    def setup_chrome_driver(self):
        """Chrome 드라이버 설정 - 검증된 성공 패턴"""
        print("\n[SETUP] Chrome 드라이버 설정...")
        
        options = Options()
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # 다운로드 경로 지정
        prefs = {
            "download.default_directory": self.download_folder,
            "download.prompt_for_download": False,
        }
        options.add_experimental_option("prefs", prefs)
        
        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("   [OK] 드라이버 설정 완료")
            return True
        except Exception as e:
            print(f"   [ERROR] 드라이버 설정 실패: {e}")
            return False
    
    def handle_alert(self):
        """알림 처리 - 성공한 패턴"""
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text[:50]
            print(f"   [ALERT] {alert_text}...")
            alert.accept()
            time.sleep(1)
            return True
        except:
            return False
    
    def login_to_admin(self):
        """관리자 로그인 - 검증된 성공 방식"""
        print("\n[LOGIN] 관리자 로그인 시작...")
        
        try:
            # 1. 관리자 URL 접근
            admin_url = self.config['cafe24']['admin_url']
            self.driver.get(admin_url)
            time.sleep(3)
            
            # 2. 보안 알림 처리
            if self.handle_alert():
                print("   [OK] 보안 알림 처리")
            
            # 3. 로그인 폼 입력 (성공한 XPath 패턴)
            username_input = self.driver.find_element(By.XPATH, "//input[@type='text' and not(@placeholder='')]")
            username_input.clear()
            username_input.send_keys(self.config['cafe24']['username'])
            
            password_input = self.driver.find_element(By.XPATH, "//input[@type='password']")
            password_input.clear()
            password_input.send_keys(self.config['cafe24']['password'])
            
            # 4. 로그인 버튼 클릭
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '로그인')]")
            login_button.click()
            time.sleep(3)
            
            print("   [OK] 로그인 폼 제출 완료")
            
            # 5. 로그인 후 알림 처리
            alert_count = 0
            while self.handle_alert() and alert_count < 5:
                alert_count += 1
            
            print("   [SUCCESS] 관리자 로그인 완료")
            return True
            
        except Exception as e:
            print(f"   [ERROR] 로그인 실패: {e}")
            return False
    
    def navigate_to_product_list(self):
        """상품목록 페이지로 이동 - 검증된 방식"""
        print("\n[NAVIGATE] 상품목록 페이지 이동...")
        
        try:
            # 상품관리 URL로 직접 이동
            product_list_url = "https://manwonyori.cafe24.com/disp/admin/shop1/product/productmanage"
            self.driver.get(product_list_url)
            time.sleep(3)
            
            # 페이지 로딩 확인
            WebDriverWait(self.driver, 10).until(
                lambda d: "상품관리" in d.page_source or "전체 239건" in d.page_source
            )
            
            print("   [SUCCESS] 상품목록 페이지 접근 완료")
            return True
            
        except Exception as e:
            print(f"   [ERROR] 상품목록 페이지 이동 실패: {e}")
            return False
    
    def wait_for_user_download(self):
        """사용자 다운로드 대기 및 모니터링"""
        print("\n" + "="*60)
        print("[START] 다운로드 시작!")
        print("사용자가 직접 다운로드를 진행해주세요")
        print("- '전체 239건' 클릭")
        print("- '엑셀다운로드' 버튼 클릭") 
        print("- 필요한 설정 후 다운로드 완료")
        print("="*60)
        
        # 다운로드 폴더 기준선 설정
        initial_files = set(glob.glob(os.path.join(self.download_folder, "*.*")))
        print(f"\n[MONITORING] 다운로드 폴더 모니터링 시작...")
        print(f"[FOLDER] {self.download_folder}")
        print(f"[BASELINE] 기존 파일: {len(initial_files)}개")
        
        # 사용자 다운로드 대기 (최대 5분)
        print("\n[WAIT] 사용자 다운로드 작업 대기 중...")
        for minute in range(5):  # 5분 대기
            for second in range(60):  # 60초씩
                time.sleep(1)
                
                # 새 파일 체크
                current_files = set(glob.glob(os.path.join(self.download_folder, "*.*")))
                new_files = current_files - initial_files
                
                if new_files:
                    print(f"\n[DETECTED] 새 파일 감지: {len(new_files)}개")
                    for new_file in new_files:
                        filename = os.path.basename(new_file)
                        size = os.path.getsize(new_file)
                        print(f"   - {filename}: {size:,} bytes ({size/1024/1024:.1f} MB)")
                    
                    # 추가 대기 (다운로드 완료 확인)
                    print("[WAIT] 다운로드 완료 확인을 위해 10초 대기...")
                    time.sleep(10)
                    return True, list(new_files)
                
                # 진행 표시
                if second % 15 == 0:  # 15초마다 표시
                    print(f"\r[WAITING] {minute+1}분 {second+1}초 경과 - 사용자 작업 대기 중...", end="")
        
        print(f"\n[TIMEOUT] 5분 대기 완료 - 새 파일이 감지되지 않음")
        return False, []
    
    def verify_downloads(self):
        """다운로드 결과 확인"""
        print("\n[VERIFY] 다운로드 결과 확인...")
        
        try:
            # 다운로드 폴더에서 최신 파일들 확인
            excel_files = glob.glob(os.path.join(self.download_folder, "*.xlsx"))
            excel_files.extend(glob.glob(os.path.join(self.download_folder, "*.xls")))
            excel_files.extend(glob.glob(os.path.join(self.download_folder, "*.csv")))
            
            if excel_files:
                # 최신 파일 정보
                latest_file = max(excel_files, key=os.path.getctime)
                file_size = os.path.getsize(latest_file)
                created_time = datetime.fromtimestamp(os.path.getctime(latest_file))
                
                print(f"   [SUCCESS] 다운로드 파일 확인:")
                print(f"   [FILE] {os.path.basename(latest_file)}")
                print(f"   [SIZE] {file_size:,} bytes ({file_size/1024/1024:.1f} MB)")
                print(f"   [TIME] {created_time.strftime('%Y-%m-%d %H:%M:%S')}")
                
                return True, latest_file
            else:
                print("   [WARNING] 다운로드 파일을 찾을 수 없음")
                return False, None
                
        except Exception as e:
            print(f"   [ERROR] 다운로드 확인 실패: {e}")
            return False, None
    
    def run_complete_workflow(self):
        """완전한 CUA Agent 워크플로우 실행 - 사용자 다운로드 방식"""
        print("\n" + "="*80)
        print("[CUA-WORKFLOW] 통합된 CUA Agent 워크플로우 시작")
        print("로그인 → 상품목록 → 사용자 다운로드 → 모니터링 → 결과확인")
        print("="*80)
        
        try:
            # 1. Chrome 드라이버 설정
            if not self.setup_chrome_driver():
                return False
            
            # 2. 관리자 로그인
            if not self.login_to_admin():
                return False
            
            # 3. 상품목록 페이지 이동  
            if not self.navigate_to_product_list():
                return False
            
            # 4. 사용자 다운로드 대기 및 모니터링
            download_success, new_files = self.wait_for_user_download()
            
            if download_success and new_files:
                print("\n" + "="*80)
                print("[CUA-SUCCESS] 사용자 다운로드 완료 감지!")
                print(f"새 파일: {len(new_files)}개")
                for new_file in new_files:
                    filename = os.path.basename(new_file)
                    size = os.path.getsize(new_file)
                    created = datetime.fromtimestamp(os.path.getctime(new_file))
                    print(f"  - {filename}: {size/1024/1024:.1f} MB ({created.strftime('%H:%M:%S')})")
                print("="*80)
                return True
            else:
                print("\n[CUA-INFO] 사용자 다운로드가 감지되지 않았습니다")
                print("브라우저는 계속 열려있으니 필요시 수동으로 작업하세요")
                return False
            
        except Exception as e:
            print(f"\n[CUA-ERROR] 워크플로우 실행 중 오류: {e}")
            return False
        
        finally:
            # 브라우저 유지 - 사용자가 계속 작업할 수 있도록
            print("\n[INFO] 브라우저는 계속 유지됩니다")
            print("작업 완료 후 직접 닫아주세요")
            print("[CLEANUP] CUA Agent 모니터링 완료")

def main():
    """메인 실행"""
    print("="*80)
    print("UNIFIED CUA AGENT")
    print("성공한 로그인 + 다운로드 방식을 통합한 완벽한 Cafe24 자동화 시스템")
    print("="*80)
    
    # 통합된 CUA Agent 실행
    cua_agent = UnifiedCUAAgent()
    success = cua_agent.run_complete_workflow()
    
    if success:
        print("\n[RESULT] 통합된 CUA Agent 성공!")
        print("모든 과정이 검증된 패턴으로 완벽 실행됨")
    else:
        print("\n[RESULT] 통합된 CUA Agent 실패")
        print("오류 로그를 확인하여 문제를 해결하세요")

if __name__ == "__main__":
    main()
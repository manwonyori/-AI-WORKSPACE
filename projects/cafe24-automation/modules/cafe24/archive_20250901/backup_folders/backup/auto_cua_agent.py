# -*- coding: utf-8 -*-
"""
Auto CUA Agent - 완전 자동 Cafe24 다운로드 시스템
로그인부터 다운로드까지 CUA Agent가 직접 모든 작업 수행
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

class AutoCUAAgent:
    """완전 자동 CUA Agent - 모든 작업을 자동으로 수행"""
    
    def __init__(self, download_folder="C:\\Users\\8899y\\CUA-MASTER\\modules\\cafe24\\download"):
        """초기화"""
        self.driver = None
        self.download_folder = download_folder
        self.config_file = "C:\\Users\\8899y\\CUA-MASTER\\modules\\cafe24\\config\\cafe24_config.json"
        self.config = {}
        
        # 다운로드 폴더 생성
        os.makedirs(download_folder, exist_ok=True)
        
        print("[AUTO-CUA] 완전 자동 CUA Agent 시작")
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
            time.sleep(5)
            
            # 페이지 로딩 확인
            WebDriverWait(self.driver, 10).until(
                lambda d: "상품관리" in d.page_source or "전체 239건" in d.page_source
            )
            
            print("   [SUCCESS] 상품목록 페이지 접근 완료")
            return True
            
        except Exception as e:
            print(f"   [ERROR] 상품목록 페이지 이동 실패: {e}")
            return False
    
    def auto_download_excel(self):
        """자동 엑셀 다운로드 - CUA Agent가 직접 실행"""
        print("\n[AUTO-DOWNLOAD] CUA Agent가 직접 엑셀 다운로드 실행...")
        
        try:
            # 1. 페이지 완전 로딩 대기
            print("   [WAIT] 페이지 완전 로딩 대기...")
            time.sleep(3)
            
            # 2. 엑셀다운로드 버튼 찾기 - 여러 방식 시도
            print("   [SEARCH] 엑셀다운로드 버튼 검색...")
            excel_button = None
            
            # 다양한 선택자 시도
            selectors = [
                "//a[contains(text(), '엑셀다운로드')]",
                "//a[contains(text(), '엑셀')]",
                "//button[contains(text(), '엑셀')]",
                "//*[contains(@onclick, '엑셀')]",
                "//*[contains(text(), '엑셀다운로드')]"
            ]
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            excel_button = element
                            print(f"   [FOUND] 엑셀다운로드 버튼 발견: {selector}")
                            break
                    if excel_button:
                        break
                except:
                    continue
            
            if not excel_button:
                print("   [ERROR] 엑셀다운로드 버튼을 찾을 수 없습니다")
                return False
            
            # 3. 엑셀다운로드 버튼 클릭
            excel_button.click()
            print("   [CLICK] 엑셀다운로드 버튼 클릭 완료")
            
            # 4. 새 창 전환 대기
            print("   [WAIT] 다운로드 팝업 창 대기...")
            for attempt in range(15):  # 15초 대기
                time.sleep(1)
                if len(self.driver.window_handles) > 1:
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    print("   [SWITCH] 다운로드 팝업으로 전환")
                    break
                print(f"   [WAITING] 팝업 대기 중... ({attempt+1}/15)")
            else:
                print("   [ERROR] 다운로드 팝업이 열리지 않았습니다")
                return False
            
            # 5. 다운로드 양식 선택
            print("   [SELECT] 다운로드 양식 선택...")
            try:
                select_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "aManagesList"))
                )
                select = Select(select_element)
                select.select_by_visible_text("카페24상품다운로드양식전체")
                print("   [OK] 양식 선택 완료")
            except Exception as e:
                print(f"   [INFO] 양식 선택 생략: {e}")
            
            # 6. 엑셀파일요청 버튼 클릭
            print("   [REQUEST] 엑셀 파일 생성 요청...")
            request_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@value='엑셀파일요청']"))
            )
            request_button.click()
            print("   [OK] 엑셀 파일 생성 요청 완료")
            
            # 7. 확인 팝업 처리
            try:
                WebDriverWait(self.driver, 3).until(EC.alert_is_present())
                alert = self.driver.switch_to.alert
                alert.accept()
                print("   [POPUP] 확인 팝업 처리 완료")
            except:
                print("   [INFO] 확인 팝업 없음")
            
            # 8. 파일 생성 대기
            print("   [WAIT] 엑셀 파일 생성 대기 (25초)...")
            time.sleep(25)
            
            # 9. 다운로드 링크 찾기 및 클릭
            print("   [DOWNLOAD] 다운로드 링크 검색...")
            download_selectors = [
                "//span[text()='다운로드']",
                "//a[contains(text(), '다운로드')]",
                "//*[contains(@onclick, '다운로드')]",
                "//span[contains(text(), '다운로드')]"
            ]
            
            download_link = None
            for selector in download_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            download_link = element
                            print(f"   [FOUND] 다운로드 링크 발견: {selector}")
                            break
                    if download_link:
                        break
                except:
                    continue
            
            if not download_link:
                print("   [ERROR] 다운로드 링크를 찾을 수 없습니다")
                return False
            
            # 10. 다운로드 실행
            download_link.click()
            print("   [DOWNLOAD] 파일 다운로드 시작!")
            
            # 11. 다운로드 완료 대기
            print("   [WAIT] 다운로드 완료 대기 (15초)...")
            time.sleep(15)
            
            # 12. 원래 창으로 복귀
            self.driver.switch_to.window(self.driver.window_handles[0])
            print("   [SUCCESS] 엑셀 다운로드 완료!")
            
            return True
            
        except Exception as e:
            print(f"   [ERROR] 자동 다운로드 실패: {e}")
            # 안전하게 원래 창으로 복귀
            try:
                self.driver.switch_to.window(self.driver.window_handles[0])
            except:
                pass
            return False
    
    def verify_download(self):
        """다운로드 결과 확인"""
        print("\n[VERIFY] 다운로드 결과 확인...")
        
        try:
            # 다운로드 폴더에서 최신 파일들 확인
            excel_files = glob.glob(os.path.join(self.download_folder, "*.xlsx"))
            excel_files.extend(glob.glob(os.path.join(self.download_folder, "*.xls")))
            excel_files.extend(glob.glob(os.path.join(self.download_folder, "*.csv")))
            
            if excel_files:
                # 최신 파일 정보 (30초 내)
                recent_files = []
                current_time = time.time()
                
                for file_path in excel_files:
                    file_mtime = os.path.getmtime(file_path)
                    if current_time - file_mtime < 300:  # 5분 내 파일
                        recent_files.append({
                            'path': file_path,
                            'name': os.path.basename(file_path),
                            'size': os.path.getsize(file_path),
                            'time': datetime.fromtimestamp(file_mtime)
                        })
                
                if recent_files:
                    print(f"   [SUCCESS] 최근 다운로드 파일: {len(recent_files)}개")
                    for file_info in recent_files:
                        print(f"   [FILE] {file_info['name']}")
                        print(f"   [SIZE] {file_info['size']:,} bytes ({file_info['size']/1024/1024:.1f} MB)")
                        print(f"   [TIME] {file_info['time'].strftime('%H:%M:%S')}")
                    return True, recent_files
                else:
                    print("   [INFO] 최근 5분 내 새 파일 없음")
                    return False, []
            else:
                print("   [WARNING] 다운로드 파일을 찾을 수 없음")
                return False, []
                
        except Exception as e:
            print(f"   [ERROR] 다운로드 확인 실패: {e}")
            return False, []
    
    def run_auto_workflow(self):
        """완전 자동 워크플로우 실행"""
        print("\n" + "="*80)
        print("[AUTO-WORKFLOW] CUA Agent 완전 자동 워크플로우 시작")
        print("로그인 → 상품목록 → 자동 다운로드 → 결과확인")
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
            
            # 4. 자동 엑셀 다운로드
            if not self.auto_download_excel():
                return False
            
            # 5. 다운로드 결과 확인
            success, downloaded_files = self.verify_download()
            
            if success and downloaded_files:
                print("\n" + "="*80)
                print("[AUTO-SUCCESS] CUA Agent 완전 자동 다운로드 성공!")
                print(f"새 파일: {len(downloaded_files)}개")
                for file_info in downloaded_files:
                    print(f"  - {file_info['name']}: {file_info['size']/1024/1024:.1f} MB ({file_info['time'].strftime('%H:%M:%S')})")
                print("="*80)
                return True
            else:
                print("\n[AUTO-INFO] 새로운 다운로드 파일이 감지되지 않음")
                return False
            
        except Exception as e:
            print(f"\n[AUTO-ERROR] 자동 워크플로우 실행 중 오류: {e}")
            return False
        
        finally:
            # 정리
            print("\n[WAIT] 결과 확인을 위해 10초 대기...")
            time.sleep(10)
            
            if self.driver:
                self.driver.quit()
                print("[CLEANUP] CUA Agent 자동 실행 완료")

def main():
    """메인 실행"""
    print("="*80)
    print("AUTO CUA AGENT")
    print("CUA Agent가 직접 모든 작업을 자동으로 수행하는 완벽한 시스템")
    print("="*80)
    
    # 완전 자동 CUA Agent 실행
    auto_agent = AutoCUAAgent()
    success = auto_agent.run_auto_workflow()
    
    if success:
        print("\n[RESULT] CUA Agent 완전 자동 실행 성공!")
        print("모든 과정이 자동으로 완벽 실행됨")
    else:
        print("\n[RESULT] CUA Agent 자동 실행 중 문제 발생")
        print("로그를 확인하여 문제를 해결하세요")

if __name__ == "__main__":
    main()
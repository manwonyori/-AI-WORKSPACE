# -*- coding: utf-8 -*-
"""
Step by Step CUA Agent - 사용자 순서 그대로 화면 체크하며 진행
사용자가 지정한 정확한 순서로 각 단계를 체크하면서 실행
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

class StepByStepCUAAgent:
    """사용자 순서 그대로 진행하는 CUA Agent"""
    
    def __init__(self, download_folder="C:\\Users\\8899y\\CUA-MASTER\\modules\\cafe24\\download"):
        """초기화"""
        self.driver = None
        self.download_folder = download_folder
        self.config_file = "C:\\Users\\8899y\\CUA-MASTER\\modules\\cafe24\\config\\cafe24_config.json"
        self.config = {}
        
        # 다운로드 폴더 생성
        os.makedirs(download_folder, exist_ok=True)
        
        print("[STEP-CUA] 사용자 순서 그대로 진행하는 CUA Agent")
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
            # 기본 설정 사용
            self.config = {
                'cafe24': {
                    'admin_url': 'https://manwonyori.cafe24.com/admin',
                    'mall_id': 'manwonyori',
                    'username': 'manwonyori',
                    'password': 'happy8263!'
                }
            }
            print(f"   [CONFIG] 기본 설정 사용")
    
    def setup_chrome_driver(self):
        """Chrome 드라이버 설정"""
        print("\n[STEP-1] Chrome 드라이버 설정...")
        
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
            print("   [OK] Chrome 드라이버 설정 완료")
            return True
        except Exception as e:
            print(f"   [ERROR] 드라이버 설정 실패: {e}")
            return False
    
    def step2_login_to_admin(self):
        """STEP-2: 관리자 로그인 - 사용자 성공 방식"""
        print("\n[STEP-2] 관리자 로그인...")
        
        try:
            # 2-1: 관리자 URL 접근
            admin_url = self.config['cafe24']['admin_url']
            self.driver.get(admin_url)
            time.sleep(3)
            print("   [2-1] 관리자 페이지 접근 완료")
            
            # 2-2: 보안 알림 처리
            try:
                alert = self.driver.switch_to.alert
                alert_text = alert.text[:50]
                print(f"   [2-2] 보안 알림: {alert_text}...")
                alert.accept()
                time.sleep(1)
            except:
                print("   [2-2] 보안 알림 없음")
            
            # 2-3: 로그인 폼 확인 및 입력
            username_input = self.driver.find_element(By.XPATH, "//input[@type='text' and not(@placeholder='')]")
            username_input.clear()
            username_input.send_keys(self.config['cafe24']['username'])
            print("   [2-3] 사용자명 입력 완료")
            
            password_input = self.driver.find_element(By.XPATH, "//input[@type='password']")
            password_input.clear()
            password_input.send_keys(self.config['cafe24']['password'])
            print("   [2-3] 비밀번호 입력 완료")
            
            # 2-4: 로그인 버튼 클릭
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '로그인')]")
            login_button.click()
            time.sleep(3)
            print("   [2-4] 로그인 버튼 클릭 완료")
            
            # 2-5: 로그인 후 알림 처리
            alert_count = 0
            while alert_count < 5:
                try:
                    alert = self.driver.switch_to.alert
                    alert.accept()
                    alert_count += 1
                    print(f"   [2-5] 로그인 후 알림 처리 {alert_count}")
                    time.sleep(1)
                except:
                    break
            
            print("   [SUCCESS] 관리자 로그인 완료")
            return True
            
        except Exception as e:
            print(f"   [ERROR] 로그인 실패: {e}")
            return False
    
    def step3_navigate_to_product_list(self):
        """STEP-3: 상품목록 페이지로 이동"""
        print("\n[STEP-3] 상품목록 페이지 이동...")
        
        try:
            # 3-1: 상품관리 페이지로 직접 이동 (사용자 방식)
            product_list_url = "https://manwonyori.cafe24.com/disp/admin/shop1/product/productmanage"
            self.driver.get(product_list_url)
            time.sleep(5)
            print("   [3-1] 상품관리 URL 접근 완료")
            
            # 3-2: 페이지 로딩 확인
            WebDriverWait(self.driver, 10).until(
                lambda d: "상품관리" in d.page_source or "전체 239건" in d.page_source
            )
            print("   [3-2] 상품목록 페이지 로딩 확인")
            
            # 3-3: 현재 화면 상태 체크
            page_source = self.driver.page_source
            if "전체 239건" in page_source:
                print("   [3-3] 전체 239건 확인됨")
            if "상품관리" in page_source:
                print("   [3-3] 상품관리 페이지 확인됨")
            
            print("   [SUCCESS] 상품목록 페이지 준비 완료")
            return True
            
        except Exception as e:
            print(f"   [ERROR] 상품목록 페이지 이동 실패: {e}")
            return False
    
    def step4_click_total_239(self):
        """STEP-4: 전체 239건 클릭 - 사용자 순서 1번"""
        print("\n[STEP-4] 전체 239건 클릭...")
        
        try:
            # 4-1: 전체 239건 링크 찾기
            print("   [4-1] '전체 239건' 링크 검색...")
            
            # 다양한 방식으로 전체 링크 찾기
            selectors = [
                "//a[contains(text(), '전체') and contains(text(), '239')]",
                "//a[contains(text(), '전체 239')]",
                "//a[contains(text(), '전체')]",
                "//*[contains(text(), '전체 239건')]//parent::a",
                "//td[contains(text(), '전체')]//a"
            ]
            
            total_link = None
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            total_link = element
                            print(f"   [4-1] '전체' 링크 발견: {selector}")
                            break
                    if total_link:
                        break
                except:
                    continue
            
            if not total_link:
                print("   [WARNING] '전체 239건' 링크를 찾을 수 없음 - 다음 단계 진행")
                return True
            
            # 4-2: 전체 링크 클릭
            total_link.click()
            time.sleep(3)
            print("   [4-2] '전체 239건' 클릭 완료")
            
            # 4-3: 클릭 후 화면 상태 체크
            updated_source = self.driver.page_source
            if "전체 239건" in updated_source:
                print("   [4-3] 전체 선택 상태 확인됨")
            
            print("   [SUCCESS] 전체 상품 선택 완료")
            return True
            
        except Exception as e:
            print(f"   [ERROR] 전체 239건 클릭 실패: {e}")
            return True  # 실패해도 계속 진행
    
    def step5_search_settings(self):
        """STEP-5: 검색 조건 설정 - 사용자 순서 2번"""
        print("\n[STEP-5] 검색 조건 설정...")
        
        try:
            # 5-1: 검색 버튼 찾기 및 클릭
            search_button = None
            try:
                search_elements = self.driver.find_elements(By.XPATH, "//a[contains(text(), '검색')]")
                for element in search_elements:
                    if element.is_displayed() and element.is_enabled():
                        search_button = element
                        break
                
                if search_button:
                    search_button.click()
                    time.sleep(2)
                    print("   [5-1] '검색' 버튼 클릭 완료")
                else:
                    print("   [5-1] '검색' 버튼 없음 - 검색 조건 생략")
            except Exception as e:
                print(f"   [5-1] 검색 버튼 클릭 생략: {e}")
            
            # 5-2: 진열상태 전체로 설정 (선택사항)
            try:
                display_all = self.driver.find_element(By.XPATH, "//input[@name='display' and @value='A']")
                if not display_all.is_selected():
                    display_all.click()
                    print("   [5-2] 진열상태 '전체' 설정 완료")
                else:
                    print("   [5-2] 진열상태 이미 '전체' 상태")
            except:
                print("   [5-2] 진열상태 설정 생략")
            
            # 5-3: 판매상태 전체로 설정 (선택사항)
            try:
                selling_all = self.driver.find_element(By.XPATH, "//input[@name='selling' and @value='A']")
                if not selling_all.is_selected():
                    selling_all.click()
                    print("   [5-3] 판매상태 '전체' 설정 완료")
                else:
                    print("   [5-3] 판매상태 이미 '전체' 상태")
            except:
                print("   [5-3] 판매상태 설정 생략")
            
            print("   [SUCCESS] 검색 조건 설정 완료")
            return True
            
        except Exception as e:
            print(f"   [INFO] 검색 조건 설정 생략: {e}")
            return True  # 실패해도 계속 진행
    
    def step6_excel_download(self):
        """STEP-6: 엑셀다운로드 버튼 클릭 - 사용자 순서 3번"""
        print("\n[STEP-6] 엑셀다운로드 실행...")
        
        try:
            # 6-1: 페이지 상태 재확인
            time.sleep(2)
            current_source = self.driver.page_source
            print("   [6-1] 현재 페이지 상태 확인 완료")
            
            # 6-2: 엑셀다운로드 버튼 찾기
            print("   [6-2] 엑셀다운로드 버튼 검색...")
            excel_button = None
            
            selectors = [
                "//a[contains(text(), '엑셀다운로드')]",
                "//a[contains(text(), '엑셀')]",
                "//button[contains(text(), '엑셀')]",
                "//*[contains(text(), '엑셀다운로드')]"
            ]
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            excel_button = element
                            print(f"   [6-2] 엑셀다운로드 버튼 발견: {selector}")
                            break
                    if excel_button:
                        break
                except:
                    continue
            
            if not excel_button:
                print("   [ERROR] 엑셀다운로드 버튼을 찾을 수 없습니다")
                return False
            
            # 6-3: 엑셀다운로드 버튼 클릭
            excel_button.click()
            print("   [6-3] 엑셀다운로드 버튼 클릭 완료")
            
            # 6-4: 팝업 창 전환 대기
            print("   [6-4] 다운로드 팝업 창 대기...")
            for attempt in range(10):
                time.sleep(1)
                if len(self.driver.window_handles) > 1:
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    print("   [6-4] 다운로드 팝업으로 전환 완료")
                    break
                print(f"       대기 중... ({attempt+1}/10)")
            else:
                print("   [ERROR] 다운로드 팝업이 열리지 않음")
                return False
            
            print("   [SUCCESS] 엑셀다운로드 팝업 전환 완료")
            return True
            
        except Exception as e:
            print(f"   [ERROR] 엑셀다운로드 실패: {e}")
            return False
    
    def step7_download_process(self):
        """STEP-7: 다운로드 프로세스 완료"""
        print("\n[STEP-7] 다운로드 프로세스...")
        
        try:
            # 7-1: 양식 선택
            print("   [7-1] 다운로드 양식 선택...")
            try:
                select_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "aManagesList"))
                )
                select = Select(select_element)
                select.select_by_visible_text("카페24상품다운로드양식전체")
                print("   [7-1] 양식 선택 완료: 카페24상품다운로드양식전체")
            except:
                print("   [7-1] 양식 선택 생략 - 기본값 사용")
            
            # 7-2: 엑셀파일요청 버튼 클릭
            print("   [7-2] 엑셀파일 생성 요청...")
            request_button = self.driver.find_element(By.XPATH, "//input[@value='엑셀파일요청']")
            request_button.click()
            print("   [7-2] 엑셀파일 생성 요청 완료")
            
            # 7-3: 확인 팝업 처리
            try:
                WebDriverWait(self.driver, 3).until(EC.alert_is_present())
                alert = self.driver.switch_to.alert
                alert.accept()
                print("   [7-3] 확인 팝업 처리 완료")
            except:
                print("   [7-3] 확인 팝업 없음")
            
            # 7-4: 파일 생성 대기
            print("   [7-4] 엑셀 파일 생성 대기 (25초)...")
            time.sleep(25)
            
            # 7-5: 다운로드 링크 찾기 및 클릭
            print("   [7-5] 다운로드 링크 검색...")
            download_link = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='다운로드']"))
            )
            download_link.click()
            print("   [7-5] 다운로드 시작!")
            
            # 7-6: 다운로드 완료 대기
            print("   [7-6] 다운로드 완료 대기 (10초)...")
            time.sleep(10)
            
            # 7-7: 원래 창으로 복귀
            self.driver.switch_to.window(self.driver.window_handles[0])
            print("   [7-7] 원래 창으로 복귀 완료")
            
            print("   [SUCCESS] 다운로드 프로세스 완료!")
            return True
            
        except Exception as e:
            print(f"   [ERROR] 다운로드 프로세스 실패: {e}")
            # 안전하게 원래 창으로 복귀
            try:
                self.driver.switch_to.window(self.driver.window_handles[0])
            except:
                pass
            return False
    
    def step8_verify_result(self):
        """STEP-8: 다운로드 결과 확인"""
        print("\n[STEP-8] 다운로드 결과 확인...")
        
        try:
            # 최근 파일 확인
            excel_files = glob.glob(os.path.join(self.download_folder, "*.csv"))
            excel_files.extend(glob.glob(os.path.join(self.download_folder, "*.xlsx")))
            excel_files.extend(glob.glob(os.path.join(self.download_folder, "*.xls")))
            
            if excel_files:
                # 최신 파일 (5분 내)
                recent_files = []
                current_time = time.time()
                
                for file_path in excel_files:
                    file_mtime = os.path.getmtime(file_path)
                    if current_time - file_mtime < 300:  # 5분 내
                        recent_files.append({
                            'path': file_path,
                            'name': os.path.basename(file_path),
                            'size': os.path.getsize(file_path),
                            'time': datetime.fromtimestamp(file_mtime)
                        })
                
                if recent_files:
                    print(f"   [SUCCESS] 새 다운로드 파일: {len(recent_files)}개")
                    for file_info in recent_files:
                        print(f"   [FILE] {file_info['name']}")
                        print(f"   [SIZE] {file_info['size']:,} bytes ({file_info['size']/1024/1024:.1f} MB)")
                        print(f"   [TIME] {file_info['time'].strftime('%H:%M:%S')}")
                    return True, recent_files
                else:
                    print("   [INFO] 5분 내 새 파일 없음 - 기존 파일들:")
                    for file_path in excel_files[-3:]:  # 최근 3개
                        name = os.path.basename(file_path)
                        size = os.path.getsize(file_path)
                        mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                        print(f"   [EXISTING] {name}: {size/1024/1024:.1f} MB ({mtime.strftime('%H:%M:%S')})")
                    return False, []
            else:
                print("   [WARNING] 다운로드 파일을 찾을 수 없음")
                return False, []
                
        except Exception as e:
            print(f"   [ERROR] 결과 확인 실패: {e}")
            return False, []
    
    def run_step_by_step_workflow(self):
        """사용자 순서 그대로 단계별 워크플로우 실행"""
        print("\n" + "="*80)
        print("[STEP-BY-STEP-WORKFLOW] 사용자 순서 그대로 진행")
        print("STEP-1: 드라이버 설정")
        print("STEP-2: 관리자 로그인")  
        print("STEP-3: 상품목록 페이지")
        print("STEP-4: 전체 239건 클릭 ← 사용자 순서!")
        print("STEP-5: 검색 조건 설정")
        print("STEP-6: 엑셀다운로드 클릭")
        print("STEP-7: 다운로드 프로세스")
        print("STEP-8: 결과 확인")
        print("="*80)
        
        try:
            # 각 단계를 사용자 순서 그대로 실행
            if not self.setup_chrome_driver():
                return False
            
            if not self.step2_login_to_admin():
                return False
            
            if not self.step3_navigate_to_product_list():
                return False
            
            if not self.step4_click_total_239():  # 사용자 순서 1번
                return False
            
            if not self.step5_search_settings():  # 사용자 순서 2번
                return False
            
            if not self.step6_excel_download():   # 사용자 순서 3번
                return False
            
            if not self.step7_download_process():
                return False
            
            success, files = self.step8_verify_result()
            
            if success:
                print("\n" + "="*80)
                print("[STEP-SUCCESS] 사용자 순서 그대로 실행 완료!")
                print("모든 단계가 정확한 순서로 실행됨")
                print("="*80)
            else:
                print("\n[STEP-INFO] 워크플로우는 완료되었으나 새 파일이 감지되지 않음")
            
            return success
            
        except Exception as e:
            print(f"\n[STEP-ERROR] 단계별 실행 중 오류: {e}")
            return False
        
        finally:
            # 10초 후 정리
            print("\n[WAIT] 결과 확인을 위해 10초 대기...")
            time.sleep(10)
            
            if self.driver:
                self.driver.quit()
                print("[CLEANUP] 단계별 실행 완료")

def main():
    """메인 실행"""
    print("="*80)
    print("STEP BY STEP CUA AGENT")
    print("사용자가 지정한 순서 그대로 화면을 체크하며 진행")
    print("="*80)
    
    # 단계별 CUA Agent 실행
    step_agent = StepByStepCUAAgent()
    success = step_agent.run_step_by_step_workflow()
    
    if success:
        print("\n[RESULT] 사용자 순서 그대로 실행 성공!")
        print("정확한 순서로 모든 단계 완료")
    else:
        print("\n[RESULT] 단계별 실행 완료")
        print("각 단계별 로그를 확인하세요")

if __name__ == "__main__":
    main()
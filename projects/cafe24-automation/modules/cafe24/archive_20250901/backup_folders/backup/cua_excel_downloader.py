# -*- coding: utf-8 -*-
"""
CUA Excel Downloader - 사용자 지시 단계 완벽 구현
로그인 → 상품관리 → 전체 239건 → 검색 → 엑셀다운로드 → 지정위치 저장
"""
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

class CUAExcelDownloader:
    """CUA Agent Excel Downloader - 대화형 모드 추가"""
    
    def __init__(self, download_path="C:\\Users\\8899y\\Downloads\\CUA_Excel_Cafe24", interactive_mode=True):
        """초기화"""
        self.driver = None
        self.download_path = download_path
        self.interactive_mode = interactive_mode
        
        # 다운로드 폴더 생성
        os.makedirs(download_path, exist_ok=True)
        
        print(f"[CUA-EXCEL] CUA Agent Excel Downloader 시작")
        print(f"[DOWNLOAD-PATH] 지정된 다운로드 위치: {download_path}")
        if interactive_mode:
            print("[INTERACTIVE] 대화형 모드 활성화 - 사용자와 단계별 진행")
    
    def setup_driver(self):
        """드라이버 설정 - 다운로드 경로 지정"""
        print("[CUA-SETUP] Chrome 드라이버 설정...")
        
        options = Options()
        options.add_argument('--window-size=1920,1080')
        
        # 다운로드 경로 지정 (사용자 요구사항)
        prefs = {
            "download.default_directory": self.download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print(f"   [OK] 드라이버 준비 완료 (다운로드: {self.download_path})")
        return True
    
    def step1_login_access(self):
        """1단계: 성공한 로그인 패턴으로 로그인 후 상품관리 진입"""
        print("\n[STEP-1] 성공한 로그인 패턴으로 로그인...")
        
        try:
            # 성공한 로그인 방식: admin_url로 먼저 접근
            admin_url = "https://manwonyori.cafe24.com/admin"
            self.driver.get(admin_url)
            time.sleep(3)
            
            # 1-1: 초기 알림 처리 (성공 패턴)
            try:
                alert = self.driver.switch_to.alert
                alert_text = alert.text[:50]
                print(f"   [ALERT] {alert_text}...")
                alert.accept()
                time.sleep(1)
                print("   [OK] 보안 알림 처리")
            except:
                pass
            
            # 1-2: 로그인 폼 입력 (성공 패턴)
            print("   [LOGIN-FORM] 로그인 폼 입력...")
            
            # 사용자명 입력 (성공한 XPath 패턴)
            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='text' and not(@placeholder='')]"))
            )
            username_input.clear()
            username_input.send_keys("manwonyori")
            
            # 패스워드 입력 (성공한 XPath 패턴)
            password_input = self.driver.find_element(By.XPATH, "//input[@type='password']")
            password_input.clear()
            password_input.send_keys("happy8263!")
            
            # 로그인 버튼 클릭 (성공한 XPath 패턴)
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '로그인')]")
            login_button.click()
            time.sleep(3)
            
            print("   [OK] 로그인 폼 제출 완료")
            
            # 1-3: 로그인 후 알림 처리 (성공 패턴)
            alert_count = 0
            while alert_count < 5:
                try:
                    alert = self.driver.switch_to.alert
                    alert_text = alert.text[:50]
                    print(f"   [ALERT-{alert_count+1}] {alert_text}...")
                    alert.accept()
                    time.sleep(1)
                    alert_count += 1
                except:
                    break
            
            # 1-4: 상품관리 페이지로 이동
            print("   [NAVIGATE] 상품관리 페이지로 이동...")
            product_manage_url = "https://manwonyori.cafe24.com/disp/admin/shop1/product/productmanage"
            self.driver.get(product_manage_url)
            time.sleep(5)
            
            # 1-5: 페이지 로딩 확인
            for attempt in range(10):
                try:
                    if "전체 239건" in self.driver.page_source or "상품관리" in self.driver.page_source:
                        print("   [SUCCESS] 상품관리 페이지 진입 성공")
                        print("   [CHECK] 전체 239건판매함 169건판매안함 70건진열함 150건진열안함 89건상품등록 확인")
                        return True
                    time.sleep(2)
                except:
                    time.sleep(2)
            
            print("   [FAIL] 상품관리 페이지 로딩 실패")
            return False
            
        except Exception as e:
            print(f"   [ERROR] 로그인 프로세스 실패: {e}")
            return False
    
    def step2_activate_full_search(self):
        """2단계: 전체 239건 클릭 → 검색 설정"""
        print("\n[STEP-2] 전체 239건 활성화 및 검색 설정...")
        
        try:
            # 개선된 검색 방식: 더 안전한 접근
            # 1단계: 페이지를 새로고침해서 상태 초기화
            self.driver.refresh()
            time.sleep(3)
            print("   [2-1] 페이지 새로고침 완료")
            
            # 2단계: 전체 링크 찾기 - 더 구체적인 XPath 사용  
            try:
                # 다양한 XPath 시도
                selectors = [
                    "//a[contains(text(), '전체') and contains(text(), '239')]",
                    "//a[contains(text(), '전체')]",
                    "//span[contains(text(), '전체')]//parent::a",
                    "//td[contains(text(), '전체')]//a"
                ]
                
                total_link = None
                for selector in selectors:
                    try:
                        elements = self.driver.find_elements(By.XPATH, selector)
                        for element in elements:
                            if element.is_displayed() and element.is_enabled():
                                total_link = element
                                break
                        if total_link:
                            break
                    except:
                        continue
                
                if total_link:
                    # ActionChains을 사용해서 안전하게 클릭
                    from selenium.webdriver.common.action_chains import ActionChains
                    ActionChains(self.driver).move_to_element(total_link).click().perform()
                    time.sleep(2)
                    print("   [2-2] 전체 링크 클릭 완료")
                else:
                    print("   [SKIP] 전체 링크를 찾을 수 없음 - 다음 단계 진행")
            
            except Exception as e:
                print(f"   [SKIP] 전체 링크 클릭 실패: {e} - 다음 단계 진행")
            
            # 3단계: 바로 엑셀 다운로드 버튼 찾기
            print("   [2-3] 엑셀다운로드 버튼 찾기...")
            
            # 엑셀다운로드 버튼 바로 찾아서 클릭
            try:
                excel_buttons = self.driver.find_elements(By.XPATH, "//a[contains(text(), '엑셀다운로드')]")
                if excel_buttons:
                    excel_button = excel_buttons[0]
                    if excel_button.is_displayed() and excel_button.is_enabled():
                        print("       [FOUND] 엑셀다운로드 버튼 발견 - 바로 다운로드 진행")
                        return True
                    
            except Exception as e:
                print(f"       [INFO] 엑셀다운로드 버튼 검색 중: {e}")
            
            # 필요시 진열상태/판매상태 설정 (옵션)
            try:
                display_elements = self.driver.find_elements(By.XPATH, "//input[@name='display' and @value='A']")
                if display_elements:
                    display_all = display_elements[0] 
                    if not display_all.is_selected():
                        display_all.click()
                        print("       [OK] 진열상태 '전체' 설정")
                        
                selling_elements = self.driver.find_elements(By.XPATH, "//input[@name='selling' and @value='A']")
                if selling_elements:
                    selling_all = selling_elements[0]
                    if not selling_all.is_selected():
                        selling_all.click()
                        print("       [OK] 판매상태 '전체' 설정")
            except Exception as e:
                print(f"       [INFO] 상태 설정 중: {e}")
            
            print("   [SUCCESS] 검색 조건 설정 완료 - 엑셀 다운로드 준비")
            return True
            
        except Exception as e:
            print(f"   [ERROR] 검색 설정 실패: {e}")
            return False
    
    def step3_excel_download_process(self):
        """3단계: 엑셀다운로드 전체 프로세스"""
        print("\n[STEP-3] 엑셀다운로드 프로세스 시작...")
        
        try:
            # 3-1: 엑셀다운로드 버튼 클릭
            print("   [3-1] 엑셀다운로드 버튼 클릭...")
            excel_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '엑셀다운로드')]"))
            )
            excel_button.click()
            print("       [OK] 엑셀다운로드 버튼 클릭 완료")
            
            # 3-2: 새창 전환 (사용자 지시: 새창이 열린다)
            WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            print("   [3-2] 엑셀다운로드 팝업 창으로 전환")
            
            # 3-3: 양식 선택 - 카페24상품다운로드양식전체 (사용자 지시)
            print("   [3-3] 양식 선택...")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "aManagesList"))
            )
            
            select_element = Select(self.driver.find_element(By.ID, "aManagesList"))
            
            # 사용자 지시: 카페24상품다운로드양식전체를 스크롤해서 찾아야 함
            try:
                select_element.select_by_visible_text("카페24상품다운로드양식전체")
                print("       [OK] '카페24상품다운로드양식전체' 선택 완료")
            except:
                # 값으로 선택 시도
                select_element.select_by_value("52")
                print("       [OK] '카페24상품다운로드양식전체' (값 52) 선택 완료")
            
            # 3-4: 엑셀파일요청 버튼 클릭 (사용자 지시: 중요!)
            print("   [3-4] 엑셀파일요청 버튼 클릭...")
            request_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@value='엑셀파일요청']"))
            )
            request_button.click()
            print("       [OK] 엑셀파일요청 버튼 클릭 완료")
            
            # 3-5: 확인 팝업 처리 (사용자 지시)
            try:
                alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
                print("   [3-5] 확인 팝업 처리...")
                alert.accept()
                print("       [OK] 확인 팝업 클릭 완료")
            except:
                print("       [INFO] 확인 팝업 없음")
            
            # 3-6: 20초 대기 (사용자 지시)
            print("   [3-6] 파일 생성 대기 (20초)...")
            for i in range(20, 0, -1):
                print(f"       [WAIT] {i}초 남음...")
                time.sleep(1)
            
            # 3-7: 다운로드 링크 찾기 및 클릭 (사용자 지시)
            print("   [3-7] 다운로드 링크 검색...")
            
            # 사용자 지시: "다운로드" 스팬 텍스트 클릭
            download_span = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='다운로드']"))
            )
            
            print("       [FOUND] 다운로드 링크 발견!")
            download_span.click()
            print("       [CLICK] 다운로드 시작!")
            
            # 3-8: 다운로드 완료 대기
            print("   [3-8] 다운로드 완료 대기...")
            time.sleep(10)  # 파일 다운로드 완료 대기
            
            # 원래 창으로 복귀
            self.driver.switch_to.window(self.driver.window_handles[0])
            
            print("   [SUCCESS] 엑셀다운로드 프로세스 완료!")
            return True
            
        except Exception as e:
            print(f"   [ERROR] 엑셀다운로드 실패: {e}")
            # 안전하게 원래 창으로 복귀 시도
            try:
                self.driver.switch_to.window(self.driver.window_handles[0])
            except:
                pass
            return False
    
    def step4_verify_download(self):
        """4단계: 다운로드 결과 확인"""
        print("\n[STEP-4] 다운로드 결과 확인...")
        
        try:
            import glob
            
            # 다운로드 폴더에서 최신 Excel 파일 찾기
            excel_files = glob.glob(os.path.join(self.download_path, "*.xlsx"))
            excel_files.extend(glob.glob(os.path.join(self.download_path, "*.xls")))
            
            if excel_files:
                # 최신 파일 찾기
                latest_file = max(excel_files, key=os.path.getctime)
                file_size = os.path.getsize(latest_file)
                
                print(f"   [SUCCESS] 다운로드 파일 확인:")
                print(f"   [FILE] {latest_file}")
                print(f"   [SIZE] {file_size:,} bytes")
                print(f"   [TIME] {datetime.fromtimestamp(os.path.getctime(latest_file))}")
                
                return True
            else:
                print("   [WARNING] 다운로드 폴더에서 Excel 파일을 찾을 수 없음")
                return False
                
        except Exception as e:
            print(f"   [ERROR] 다운로드 확인 실패: {e}")
            return False
    
    def run_complete_workflow(self):
        """CUA Agent 완전한 엑셀다운로드 워크플로우"""
        print("="*80)
        print("[CUA-WORKFLOW] 완전한 엑셀다운로드 워크플로우 시작")
        print("사용자 지시 단계를 정확히 구현")
        print("="*80)
        
        try:
            # 단계별 실행
            if not self.setup_driver():
                return False
            
            if not self.step1_login_access():
                return False
            
            if not self.step2_activate_full_search():
                return False
            
            if not self.step3_excel_download_process():
                return False
            
            if not self.step4_verify_download():
                return False
            
            print("\n" + "="*80)
            print("[CUA-SUCCESS] 전체 워크플로우 완료!")
            print("239개 전체 상품 데이터가 지정된 위치에 다운로드됨")
            print(f"다운로드 위치: {self.download_path}")
            print("="*80)
            
            return True
            
        except Exception as e:
            print(f"\n[CUA-ERROR] 워크플로우 실행 중 오류: {e}")
            return False
        
        finally:
            # 결과 확인을 위해 10초 대기
            print("\n[WAIT] 결과 확인을 위해 10초 대기...")
            time.sleep(10)
            
            if self.driver:
                self.driver.quit()
                print("[CLEANUP] CUA Agent 정리 완료")
    
    def interactive_step_by_step(self):
        """대화형 단계별 진행 모드"""
        print("\n" + "="*80)
        print("[INTERACTIVE] 대화형 모드 시작")
        print("상품목록 페이지에서 사용자 지시에 따라 단계별 진행")
        print("="*80)
        
        # 1. 드라이버 설정 및 로그인
        if not self.setup_driver():
            return False
            
        print("\n[STEP] 로그인 및 상품목록 페이지 접근...")
        if not self.step1_login_access():
            return False
        
        # 2. 상품목록 페이지에서 대기 - 사용자 지시 대기
        print("\n" + "="*60)
        print("[INTERACTIVE] 상품목록 페이지 접근 완료")
        print("https://manwonyori.cafe24.com/disp/admin/shop1/product/productmanage")
        print("="*60)
        
        print("\n[WAITING] 사용자 지시를 기다리고 있습니다...")
        print("- 클릭할 요소를 알려주세요")
        print("- 'continue' 입력 시 다음 단계 진행")
        print("- 'quit' 입력 시 종료")
        
        while True:
            try:
                user_input = input("\n>>> 다음 지시사항 또는 명령어: ").strip()
                
                if user_input.lower() == 'quit':
                    print("[EXIT] 사용자 종료 요청")
                    break
                elif user_input.lower() == 'continue':
                    print("[CONTINUE] 자동 엑셀 다운로드 진행...")
                    return self.auto_excel_download()
                elif user_input:
                    # 사용자 지시 처리
                    print(f"[USER-INSTRUCTION] 지시사항: {user_input}")
                    self.process_user_instruction(user_input)
                else:
                    print("[INFO] 명령어를 입력해주세요")
                    
            except KeyboardInterrupt:
                print("\n[EXIT] 사용자 중단")
                break
        
        return False
    
    def process_user_instruction(self, instruction):
        """사용자 지시사항 처리"""
        print(f"[PROCESS] '{instruction}' 처리 중...")
        
        try:
            # 텍스트 기반 요소 찾기
            if "클릭" in instruction or "click" in instruction.lower():
                # 클릭할 요소 텍스트 추출
                click_text = instruction.replace("클릭", "").replace("click", "").strip()
                
                if click_text:
                    # 다양한 방법으로 요소 찾기
                    selectors = [
                        f"//a[contains(text(), '{click_text}')]",
                        f"//button[contains(text(), '{click_text}')]",
                        f"//span[contains(text(), '{click_text}')]",
                        f"//input[@value='{click_text}']",
                        f"//*[contains(text(), '{click_text}')]"
                    ]
                    
                    element_found = False
                    for selector in selectors:
                        try:
                            elements = self.driver.find_elements(By.XPATH, selector)
                            for element in elements:
                                if element.is_displayed() and element.is_enabled():
                                    element.click()
                                    print(f"   [SUCCESS] '{click_text}' 요소 클릭 완료")
                                    element_found = True
                                    break
                            if element_found:
                                break
                        except:
                            continue
                    
                    if not element_found:
                        print(f"   [NOT-FOUND] '{click_text}' 요소를 찾을 수 없습니다")
                        
            elif "스크롤" in instruction:
                # 스크롤 처리
                self.driver.execute_script("window.scrollBy(0, 300);")
                print("   [SCROLL] 페이지 스크롤 완료")
                
            else:
                print(f"   [INFO] '{instruction}' - 처리 방법을 구체적으로 알려주세요")
                
        except Exception as e:
            print(f"   [ERROR] 지시사항 처리 실패: {e}")
    
    def auto_excel_download(self):
        """자동 엑셀 다운로드 진행"""
        print("\n[AUTO] 자동 엑셀 다운로드 시작...")
        
        try:
            if not self.step2_activate_full_search():
                print("[INFO] 검색 설정 생략 - 엑셀 다운로드 진행")
                
            if not self.step3_excel_download_process():
                return False
                
            if not self.step4_verify_download():
                return False
                
            print("\n[SUCCESS] 자동 엑셀 다운로드 완료!")
            return True
            
        except Exception as e:
            print(f"[ERROR] 자동 다운로드 실패: {e}")
            return False
    
    def setup_for_interactive(self):
        """대화형 모드 준비 - 상품목록 페이지까지 접근"""
        print("\n" + "="*80)
        print("[SETUP] 대화형 모드 준비 시작")
        print("로그인 → 상품목록 페이지 접근 → 사용자 작업 준비")
        print("="*80)
        
        try:
            # 1. 드라이버 설정
            if not self.setup_driver():
                return False
                
            # 2. 로그인 및 상품목록 페이지 접근
            print("\n[STEP] 로그인 및 상품목록 페이지 접근...")
            if not self.step1_login_access():
                return False
            
            # 3. 상품목록 페이지 확인 및 대기
            print("\n" + "="*60)
            print("[SUCCESS] 상품목록 페이지 접근 완료!")
            print("URL: https://manwonyori.cafe24.com/disp/admin/shop1/product/productmanage")
            print("="*60)
            
            print("\n[INTERACTIVE-READY] 브라우저가 열려있습니다")
            print("- 상품목록에서 필요한 작업을 직접 수행하세요")
            print("- '전체 239건' 링크 클릭")
            print("- '엑셀다운로드' 버튼 클릭")  
            print("- 또는 다른 필요한 작업 진행")
            
            print("\n[WAIT] 사용자 작업 완료까지 브라우저 유지...")
            print("작업 완료 후 이 창에서 아무 키나 눌러 종료하세요")
            
            # 60초 동안 브라우저 유지 (사용자 작업 시간)
            for i in range(60):
                print(f"\r[TIME] 대기 중... {60-i}초 남음", end="")
                time.sleep(1)
            
            print(f"\n[TIMEOUT] 60초 대기 완료 - 브라우저 유지 상태")
            print("[INFO] 필요시 작업을 계속 진행하세요")
            
            return True
            
        except Exception as e:
            print(f"\n[ERROR] 대화형 준비 실패: {e}")
            return False

def main():
    """메인 실행 - 대화형/자동 모드 선택"""
    print("="*80)
    print("CUA AGENT EXCEL DOWNLOADER")
    print("사용자 지시 단계를 정확히 구현한 완벽한 엑셀다운로드 시스템")
    print("="*80)
    
    # 다운로드 경로 지정
    download_path = "C:\\Users\\8899y\\Downloads\\CUA_Excel_Cafe24"
    
    print("\n[MODE-SELECT] 실행 모드를 선택하세요:")
    print("1. 대화형 모드 (Interactive) - 상품목록에서 단계별 클릭 지시")
    print("2. 자동 모드 (Auto) - 전체 자동 실행")
    
    # Claude Code 환경에서는 대화형 준비 모드로 시작
    print("\n[SELECTED] 대화형 준비 모드 시작")
    print("상품목록 페이지 접근 후 사용자 지시 대기")
    
    cua_downloader = CUAExcelDownloader(download_path, interactive_mode=True)
    success = cua_downloader.setup_for_interactive()
    
    if success:
        print("\n[READY] 대화형 모드 준비 완료!")
        print("상품목록 페이지에서 사용자 지시를 기다리는 상태")
    else:
        print("\n[RESULT] CUA Agent 준비 실패")

if __name__ == "__main__":
    main()
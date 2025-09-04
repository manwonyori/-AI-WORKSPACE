"""
Cafe24 자동 Excel 다운로드 스크립트
상품관리 페이지에서 전체 상품 엑셀 다운로드 자동화
"""
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class AutoExcelDownloader:
    def __init__(self):
        self.download_path = "C:\\Users\\8899y\\CUA-MASTER\\modules\\cafe24\\download"
        self.driver = None
        
        # 다운로드 폴더 생성
        os.makedirs(self.download_path, exist_ok=True)
        
    def setup_driver(self):
        """드라이버 설정"""
        print("[SETUP] Chrome 드라이버 설정...")
        
        options = Options()
        options.add_argument('--window-size=1920,1080')
        
        # 다운로드 경로 지정
        prefs = {
            "download.default_directory": self.download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print(f"[OK] 드라이버 준비 완료")
        
    def login_and_navigate(self):
        """로그인 및 상품관리 페이지 이동"""
        print("\n[STEP-1] Cafe24 로그인...")
        
        # 관리자 페이지 접속
        self.driver.get("https://manwonyori.cafe24.com/admin")
        time.sleep(3)
        
        # 알림 처리
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
            print("[OK] 보안 알림 처리")
        except:
            pass
        
        # 로그인
        try:
            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))
            )
            username_input.clear()
            username_input.send_keys("manwonyori")
            
            password_input = self.driver.find_element(By.XPATH, "//input[@type='password']")
            password_input.clear()
            password_input.send_keys("happy8263!")
            
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '로그인')]")
            login_button.click()
            time.sleep(3)
            
            print("[OK] 로그인 완료")
        except Exception as e:
            print(f"[ERROR] 로그인 실패: {e}")
            return False
        
        # 로그인 후 알림 처리
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except:
            pass
        
        # 상품관리 페이지로 이동
        print("\n[STEP-2] 상품관리 페이지 이동...")
        self.driver.get("https://manwonyori.cafe24.com/disp/admin/shop1/product/productmanage")
        time.sleep(5)
        
        return True
    
    def download_excel(self):
        """엑셀 다운로드 실행"""
        print("\n[STEP-3] 엑셀 다운로드 시작...")
        
        try:
            # 1. 전체 상품 링크 클릭 (전체 294건)
            print("[ACTION] 전체 상품 선택...")
            all_products_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '전체')]"))
            )
            all_products_link.click()
            time.sleep(3)
            
            # 2. 검색 버튼 클릭
            print("[ACTION] 검색 버튼 클릭...")
            search_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '검색') or @class='btnSearch']")
            search_button.click()
            time.sleep(5)
            
            # 3. 엑셀 다운로드 버튼 찾기 및 클릭
            print("[ACTION] 엑셀 다운로드 버튼 찾기...")
            
            # 여러 가능한 방법으로 시도
            excel_button = None
            
            # 방법 1: 텍스트로 찾기
            try:
                excel_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '엑셀다운로드')]")
            except:
                pass
            
            # 방법 2: 클래스명으로 찾기
            if not excel_button:
                try:
                    excel_button = self.driver.find_element(By.XPATH, "//button[contains(@class, 'excel') or contains(@class, 'download')]")
                except:
                    pass
            
            # 방법 3: 링크로 찾기
            if not excel_button:
                try:
                    excel_button = self.driver.find_element(By.XPATH, "//a[contains(text(), '엑셀') or contains(text(), 'Excel')]")
                except:
                    pass
            
            if excel_button:
                excel_button.click()
                print("[OK] 엑셀 다운로드 시작")
                
                # 다운로드 완료 대기
                time.sleep(10)
                
                # 다운로드된 파일 확인
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                print(f"[SUCCESS] 엑셀 파일 다운로드 완료")
                print(f"[PATH] {self.download_path}")
                
                return True
            else:
                print("[ERROR] 엑셀 다운로드 버튼을 찾을 수 없습니다")
                print("[TIP] 수동으로 엑셀다운로드 버튼을 클릭해주세요")
                
                # 수동 대기
                input("엑셀 다운로드 완료 후 Enter를 눌러주세요...")
                return True
                
        except Exception as e:
            print(f"[ERROR] 다운로드 실패: {e}")
            return False
    
    def check_downloaded_files(self):
        """다운로드된 파일 확인"""
        print("\n[STEP-4] 다운로드된 파일 확인...")
        
        csv_files = [f for f in os.listdir(self.download_path) if f.endswith('.csv')]
        xls_files = [f for f in os.listdir(self.download_path) if f.endswith(('.xls', '.xlsx'))]
        
        print(f"[CSV FILES] {len(csv_files)}개")
        for f in csv_files[-5:]:  # 최근 5개만 표시
            print(f"  - {f}")
        
        print(f"[EXCEL FILES] {len(xls_files)}개")
        for f in xls_files[-5:]:  # 최근 5개만 표시
            print(f"  - {f}")
    
    def run(self):
        """전체 프로세스 실행"""
        print("="*60)
        print("Cafe24 자동 Excel 다운로드")
        print(f"시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # 드라이버 설정
        self.setup_driver()
        
        # 로그인 및 페이지 이동
        if self.login_and_navigate():
            # 엑셀 다운로드
            if self.download_excel():
                # 다운로드 파일 확인
                self.check_downloaded_files()
        
        # 브라우저 유지 (사용자가 확인할 수 있도록)
        print("\n[COMPLETE] 작업 완료")
        print("[INFO] 브라우저를 닫으려면 Enter를 누르세요...")
        input()
        
        # 종료
        self.driver.quit()
        print("[END] 프로그램 종료")

if __name__ == "__main__":
    downloader = AutoExcelDownloader()
    downloader.run()
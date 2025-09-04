# -*- coding: utf-8 -*-
"""
Cafe24 상품 수정 검증 시스템
수정 전후 데이터를 엑셀로 다운로드하여 실제 반영 여부 확인
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

class Cafe24VerificationSystem:
    """상품 수정 검증 시스템"""
    
    def __init__(self):
        """초기화"""
        self.driver = None
        print("[VERIFICATION-SYSTEM] 상품 수정 검증 시스템 시작")
    
    def setup_driver(self):
        """드라이버 설정"""
        options = Options()
        options.add_argument('--window-size=1920,1080')
        
        # 다운로드 경로 설정
        prefs = {
            "download.default_directory": "C:\\Users\\8899y\\Downloads",
            "download.prompt_for_download": False,
        }
        options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return True
    
    def login_to_admin(self):
        """관리자 로그인 - 성공한 방식 그대로 사용"""
        print("[LOGIN] 관리자 페이지 로그인...")
        
        # 검증된 성공 방식: 직접 상품관리 URL로 접근
        product_manage_url = "https://manwonyori.cafe24.com/disp/admin/shop1/product/productmanage"
        self.driver.get(product_manage_url)
        
        # 알림 처리 (성공한 패턴)
        for i in range(3):
            try:
                alert = WebDriverWait(self.driver, 3).until(EC.alert_is_present())
                alert_text = alert.text[:50]
                print(f"[ALERT-{i+1}] {alert_text}")
                alert.accept()
                time.sleep(1)
            except:
                break
        
        # 페이지 로딩 완료 대기
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: "상품관리" in d.page_source or "전체 239건" in d.page_source
            )
            print("[LOGIN-SUCCESS] 상품관리 페이지 접근 성공")
            return True
        except:
            print("[LOGIN-FAIL] 상품관리 페이지 접근 실패")
            return False
    
    def navigate_to_product_list(self):
        """상품 목록 페이지로 이동"""
        print("[NAVIGATE] 상품 목록 페이지 이동...")
        
        # 검증된 상품 관리 URL
        product_list_url = "https://manwonyori.cafe24.com/disp/admin/shop1/product/productmanage"
        self.driver.get(product_list_url)
        
        # 페이지 로딩 대기
        WebDriverWait(self.driver, 10).until(
            lambda d: "전체 239건" in d.page_source or "상품관리" in d.page_source
        )
        
        print("[SUCCESS] 상품 목록 페이지 로드 완료")
        return True
    
    def activate_full_search(self):
        """전체 상품 검색 활성화"""
        print("[SEARCH] 전체 239건 상품 검색 활성화...")
        
        try:
            # 1단계: 전체 239건 클릭
            total_link = self.driver.find_element(By.XPATH, "//a[contains(text(), '전체')]")
            total_link.click()
            time.sleep(2)
            
            # 2단계: 검색 버튼 클릭
            search_button = self.driver.find_element(By.XPATH, "//a[contains(text(), '검색')]")
            search_button.click()
            time.sleep(2)
            
            # 3단계: 진열상태 및 판매상태를 '전체'로 설정
            # 진열상태 전체 라디오 버튼 클릭
            display_all = self.driver.find_element(By.XPATH, "//input[@name='display' and @value='A']")
            if not display_all.is_selected():
                display_all.click()
            
            # 판매상태 전체 라디오 버튼 클릭
            selling_all = self.driver.find_element(By.XPATH, "//input[@name='selling' and @value='A']")
            if not selling_all.is_selected():
                selling_all.click()
            
            print("[SUCCESS] 전체 상품 검색 조건 설정 완료")
            return True
            
        except Exception as e:
            print(f"[ERROR] 검색 설정 실패: {e}")
            return False
    
    def download_product_excel(self):
        """전체 상품 엑셀 다운로드"""
        print("[DOWNLOAD] 전체 상품 엑셀 다운로드...")
        
        try:
            # 1단계: 엑셀다운로드 버튼 클릭
            excel_download = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '엑셀다운로드')]"))
            )
            excel_download.click()
            
            # 새 창으로 전환
            self.driver.switch_to.window(self.driver.window_handles[-1])
            print("[INFO] 엑셀 다운로드 팝업 창으로 전환")
            
            # 2단계: 양식 선택 - '카페24상품다운로드양식전체' 선택
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "aManagesList"))
            )
            
            select_element = Select(self.driver.find_element(By.ID, "aManagesList"))
            select_element.select_by_visible_text("카페24상품다운로드양식전체")
            print("[SELECT] '카페24상품다운로드양식전체' 선택 완료")
            
            # 3단계: 엑셀파일요청 버튼 클릭
            request_button = self.driver.find_element(By.XPATH, "//input[@value='엑셀파일요청']")
            request_button.click()
            
            # 4단계: 확인 팝업 처리
            try:
                alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
                alert.accept()
                print("[POPUP] 확인 팝업 처리 완료")
            except:
                print("[INFO] 확인 팝업 없음")
            
            # 5단계: 20초 대기 (파일 생성 시간)
            print("[WAIT] 엑셀 파일 생성 대기 (20초)...")
            time.sleep(20)
            
            # 6단계: 다운로드 링크 찾기 및 클릭
            download_link = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='다운로드']"))
            )
            download_link.click()
            
            print("[SUCCESS] 엑셀 파일 다운로드 시작")
            time.sleep(5)  # 다운로드 완료 대기
            
            # 원래 창으로 복귀
            self.driver.switch_to.window(self.driver.window_handles[0])
            
            return True
            
        except Exception as e:
            print(f"[ERROR] 엑셀 다운로드 실패: {e}")
            # 원래 창으로 복귀 시도
            try:
                self.driver.switch_to.window(self.driver.window_handles[0])
            except:
                pass
            return False
    
    def run_verification_workflow(self):
        """검증 워크플로우 전체 실행"""
        print("\n" + "="*80)
        print("[VERIFICATION-WORKFLOW] 상품 수정 검증 워크플로우 시작")
        print("="*80)
        
        try:
            # 1단계: 드라이버 설정
            if not self.setup_driver():
                return False
            
            # 2단계: 직접 상품관리 페이지 접근 (로그인 포함)
            if not self.login_to_admin():
                return False
            
            # 3단계: 전체 상품 검색 활성화
            if not self.activate_full_search():
                return False
            
            # 4단계: 엑셀 다운로드
            if not self.download_product_excel():
                return False
            
            print("\n" + "="*80)
            print("[VERIFICATION-SUCCESS] 검증 워크플로우 완료!")
            print("다운로드 폴더에서 엑셀 파일을 확인하여 수정 사항 검증")
            print("="*80)
            
            return True
            
        except Exception as e:
            print(f"\n[VERIFICATION-ERROR] 워크플로우 실행 중 오류: {e}")
            return False
        
        finally:
            # 결과 확인을 위해 잠시 대기
            print("[WAIT] 결과 확인을 위해 10초 대기...")
            time.sleep(10)
            
            if self.driver:
                self.driver.quit()
                print("[CLEANUP] 정리 완료")

def main():
    """메인 실행"""
    print("="*80)
    print("CAFE24 상품 수정 검증 시스템")
    print("수정 전후 데이터를 엑셀로 다운로드하여 실제 반영 여부 확인")
    print("="*80)
    
    verification = Cafe24VerificationSystem()
    success = verification.run_verification_workflow()
    
    if success:
        print("\n✅ 검증 시스템 성공!")
        print("📊 다운로드된 엑셀 파일에서 수정된 상품 데이터 확인 가능")
    else:
        print("\n❌ 검증 시스템 실패")

if __name__ == "__main__":
    main()
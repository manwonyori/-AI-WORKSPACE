# -*- coding: utf-8 -*-
"""
239개 상품 대량 처리 시스템
P00000NB 성공 패턴을 기반으로 한 확장 시스템
"""
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

import json
import time
import csv
import re
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from bs4 import BeautifulSoup

try:
    from webdriver_manager.chrome import ChromeDriverManager
    USE_WEBDRIVER_MANAGER = True
except ImportError:
    USE_WEBDRIVER_MANAGER = False

class CafeBulkProcessor:
    """Cafe24 상품 대량 처리 클래스"""
    
    def __init__(self, config_path="config/cafe24_config.json"):
        """초기화"""
        self.config = self.load_config(config_path)
        self.driver = None
        self.processed_count = 0
        self.success_count = 0
        self.error_count = 0
        self.results = []
        
        # 출력 디렉토리 생성
        self.output_dir = Path("bulk_processing_output")
        self.output_dir.mkdir(exist_ok=True)
    
    def load_config(self, config_path):
        """설정 파일 로드"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def setup_driver(self):
        """Chrome 드라이버 설정"""
        print("\n[INIT] Chrome 브라우저 초기화...")
        
        options = Options()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        
        if USE_WEBDRIVER_MANAGER:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
        else:
            self.driver = webdriver.Chrome(options=options)
        
        self.driver.maximize_window()
        print("   [OK] Chrome 브라우저 준비 완료")
    
    def handle_alert(self):
        """알림 처리"""
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text[:50]
            alert.accept()
            time.sleep(1)
            return True
        except NoAlertPresentException:
            return False
    
    def login_to_cafe24(self):
        """Cafe24 로그인 (성공한 패턴 사용)"""
        print("\n[LOGIN] Cafe24 관리자 로그인...")
        
        admin_url = self.config['cafe24']['admin_url']
        self.driver.get(admin_url)
        time.sleep(3)
        
        # 보안 알림 처리
        if self.handle_alert():
            print("   [OK] 보안 알림 처리")
        
        # 로그인 정보 입력
        username_input = self.driver.find_element(By.XPATH, "//input[@type='text' and not(@placeholder='')]")
        username_input.clear()
        username_input.send_keys(self.config['cafe24']['username'])
        
        password_input = self.driver.find_element(By.XPATH, "//input[@type='password']")
        password_input.clear()
        password_input.send_keys(self.config['cafe24']['password'])
        
        login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '로그인')]")
        login_button.click()
        
        time.sleep(3)
        
        # 추가 알림 처리
        alert_count = 0
        while self.handle_alert() and alert_count < 5:
            alert_count += 1
            time.sleep(1)
        
        current_url = self.driver.current_url
        if "admin" in current_url and "dashboard" in current_url:
            print("   [SUCCESS] 로그인 성공!")
            return True
        else:
            print(f"   [ERROR] 로그인 실패: {current_url}")
            return False
    
    def access_product_by_id(self, product_no, product_code=""):
        """상품번호로 직접 상품 수정 페이지 접근"""
        mall_id = self.config['cafe24']['mall_id']
        product_url = f"https://{mall_id}.cafe24.com/disp/admin/shop1/product/ProductRegister?product_no={product_no}"
        
        try:
            self.driver.get(product_url)
            time.sleep(2)
            
            # 알림 처리 (존재하지 않는 상품 등)
            alert_handled = False
            for _ in range(3):
                if self.handle_alert():
                    print(f"   [INFO] 상품 {product_no} 관련 알림 처리됨")
                    alert_handled = True
                    break
                time.sleep(1)
            
            # 알림이 처리되었으면 상품이 존재하지 않는 것으로 판단
            if alert_handled:
                return False
            
            # JavaScript 로딩 대기
            wait = WebDriverWait(self.driver, 15)
            
            # 폼 요소 로딩 확인
            for attempt in range(3):
                try:
                    inputs = self.driver.find_elements(By.TAG_NAME, "input")
                    if len(inputs) > 100:  # 충분한 폼 요소가 로딩되면
                        break
                except:
                    pass
                time.sleep(2)
            
            current_url = self.driver.current_url
            if f"product_no={product_no}" in current_url:
                print(f"   [OK] 상품 {product_no} 접근 성공 ({product_code})")
                return True
            else:
                print(f"   [INFO] 상품 {product_no}는 존재하지 않음")
                return False
                
        except Exception as e:
            print(f"   [ERROR] 상품 {product_no} 접근 오류: {e}")
            return False
    
    def extract_product_data(self):
        """현재 페이지에서 상품 데이터 추출"""
        try:
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # 기본 정보 추출
            product_data = {}
            
            # 상품코드
            product_code_elem = soup.find('span', id='product_code')
            if product_code_elem:
                product_data['product_code'] = product_code_elem.get_text().strip()
            
            # 상품명
            product_name_input = soup.find('input', {'name': 'product_name[1]'})
            if product_name_input:
                product_data['product_name'] = product_name_input.get('value', '')
            
            # 판매가
            price_input = soup.find('input', {'name': 'prd_price_org[1]'})
            if price_input:
                product_data['price'] = price_input.get('value', '0')
            
            # 영문 상품명
            eng_name_input = soup.find('input', {'name': 'eng_product_name'})
            if eng_name_input:
                product_data['eng_product_name'] = eng_name_input.get('value', '')
            
            # 진열상태 확인
            display_inputs = soup.find_all('input', {'name': re.compile(r'is_display.*')})
            for display_input in display_inputs:
                if display_input.get('checked'):
                    product_data['display_status'] = display_input.get('value', '')
                    break
            
            return product_data
            
        except Exception as e:
            print(f"   [ERROR] 데이터 추출 오류: {e}")
            return {}
    
    def save_processing_results(self):
        """처리 결과 저장"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # CSV 파일로 결과 저장
        csv_file = self.output_dir / f"bulk_processing_results_{timestamp}.csv"
        
        if self.results:
            with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                
                # 헤더
                headers = ['product_no', 'status', 'product_code', 'product_name', 'price', 'processing_time', 'error_message']
                writer.writerow(headers)
                
                # 데이터
                for result in self.results:
                    writer.writerow([
                        result.get('product_no', ''),
                        result.get('status', ''),
                        result.get('product_code', ''),
                        result.get('product_name', ''),
                        result.get('price', ''),
                        result.get('processing_time', ''),
                        result.get('error_message', '')
                    ])
        
        # JSON 파일로도 저장
        json_file = self.output_dir / f"bulk_processing_results_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'summary': {
                    'total_processed': self.processed_count,
                    'success_count': self.success_count,
                    'error_count': self.error_count,
                    'processing_time': timestamp
                },
                'details': self.results
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n[저장완료] 처리 결과:")
        print(f"   CSV: {csv_file}")
        print(f"   JSON: {json_file}")
        
        return csv_file, json_file
    
    def process_product_range(self, start_product_no, end_product_no, max_products=10):
        """상품 범위 처리 (테스트용)"""
        print(f"\n[PROCESSING] 상품 번호 {start_product_no}~{end_product_no} 범위 처리 시작")
        print(f"최대 처리 개수: {max_products}개")
        print("="*80)
        
        current_no = start_product_no
        
        while current_no <= end_product_no and self.processed_count < max_products:
            start_time = time.time()
            
            print(f"\n[{self.processed_count + 1}/{max_products}] 상품 번호 {current_no} 처리 중...")
            
            result = {
                'product_no': current_no,
                'status': 'failed',
                'product_code': '',
                'product_name': '',
                'price': '',
                'processing_time': 0,
                'error_message': ''
            }
            
            try:
                # 상품 페이지 접근
                if self.access_product_by_id(current_no):
                    # 데이터 추출
                    product_data = self.extract_product_data()
                    
                    if product_data:
                        result.update({
                            'status': 'success',
                            'product_code': product_data.get('product_code', ''),
                            'product_name': product_data.get('product_name', ''),
                            'price': product_data.get('price', ''),
                        })
                        
                        self.success_count += 1
                        print(f"   [SUCCESS] {product_data.get('product_code', '')} - {product_data.get('product_name', '')}")
                    else:
                        result['error_message'] = '데이터 추출 실패'
                        self.error_count += 1
                else:
                    result['error_message'] = '페이지 접근 실패'
                    self.error_count += 1
                    
            except Exception as e:
                result['error_message'] = str(e)
                self.error_count += 1
                print(f"   [ERROR] 처리 오류: {e}")
            
            # 처리 시간 기록
            processing_time = time.time() - start_time
            result['processing_time'] = round(processing_time, 2)
            
            self.results.append(result)
            self.processed_count += 1
            
            # 다음 상품으로
            current_no += 1
            
            # 간격 조정 (서버 부하 방지)
            time.sleep(1)
        
        print(f"\n[처리완료] {self.processed_count}개 상품 처리")
        print(f"성공: {self.success_count}개, 실패: {self.error_count}개")
    
    def run_bulk_processing_test(self, start_product_no=339, max_products=5):
        """대량 처리 테스트 실행"""
        print("="*80)
        print("   Cafe24 상품 대량 처리 시스템 테스트")
        print("="*80)
        
        try:
            # 1. 드라이버 설정
            self.setup_driver()
            
            # 2. 로그인
            if not self.login_to_cafe24():
                print("로그인 실패로 종료합니다.")
                return
            
            # 3. 상품 범위 처리
            self.process_product_range(start_product_no, start_product_no + 20, max_products)
            
            # 4. 결과 저장
            csv_file, json_file = self.save_processing_results()
            
            print("\n" + "="*80)
            print("[최종 완료] 대량 처리 테스트 완료")
            print(f"처리된 상품: {self.processed_count}개")
            print(f"성공률: {(self.success_count/self.processed_count*100):.1f}%" if self.processed_count > 0 else "0%")
            print("="*80)
            
        except Exception as e:
            print(f"\n[CRITICAL ERROR] 시스템 오류: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            if self.driver:
                self.driver.quit()
                print("\n[완료] 브라우저 종료")

def main():
    """메인 실행 함수"""
    processor = CafeBulkProcessor()
    
    # 테스트 실행: P00000NB(339) 주변 상품들 확인
    # 더 넓은 범위에서 존재하는 상품들 찾기
    processor.run_bulk_processing_test(start_product_no=330, max_products=10)

if __name__ == "__main__":
    main()
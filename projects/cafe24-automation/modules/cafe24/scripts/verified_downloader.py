"""
검증된 다운로더 - 성공한 방식 그대로 사용
"""
import os
import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import random

class VerifiedDownloader:
    def __init__(self):
        self.base_folder = "C:\\Users\\8899y\\CUA-MASTER\\modules\\cafe24\\complete_content"
        self.download_folder = "C:\\Users\\8899y\\CUA-MASTER\\modules\\cafe24\\download"
        self.config_file = "C:\\Users\\8899y\\CUA-MASTER\\modules\\cafe24\\config\\cafe24_config.json"
        self.driver = None
        
        # 설정 로드
        with open(self.config_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # 이미 완료된 상품
        self.completed = self.get_completed_products()
        print(f"[CHECK] 이미 완료: {len(self.completed)}개")
        
        # CSV에서 상품 목록 로드
        self.products = self.load_products_from_csv()
        print(f"[TOTAL] 전체 상품: {len(self.products)}개")
        
    def get_completed_products(self):
        """이미 다운로드된 상품"""
        completed = set()
        html_folder = os.path.join(self.base_folder, "html")
        
        if os.path.exists(html_folder):
            for supplier in os.listdir(html_folder):
                if supplier == "nul":
                    continue
                supplier_path = os.path.join(html_folder, supplier)
                if os.path.isdir(supplier_path):
                    for file in os.listdir(supplier_path):
                        if file.endswith('.html'):
                            product_code = file.replace('.html', '')
                            completed.add(product_code)
        
        return completed
    
    def load_products_from_csv(self):
        """CSV에서 상품 정보 로드"""
        csv_files = [f for f in os.listdir(self.download_folder) if f.endswith('.csv')]
        if not csv_files:
            print("[ERROR] CSV 파일 없음")
            return []
        
        latest_csv = max(csv_files, key=lambda f: os.path.getctime(os.path.join(self.download_folder, f)))
        csv_path = os.path.join(self.download_folder, latest_csv)
        
        try:
            df = pd.read_csv(csv_path, encoding='utf-8-sig')
        except:
            df = pd.read_csv(csv_path, encoding='cp949')
        
        products = []
        for _, row in df.iterrows():
            product_no = str(row.get('상품번호', ''))
            product_name = str(row.get('상품명', ''))
            product_code = str(row.get('상품코드', ''))
            
            if product_no and product_no != 'nan':
                products.append({
                    'no': product_no,
                    'name': product_name,
                    'code': product_code
                })
        
        return products
    
    def setup_driver(self):
        """드라이버 설정"""
        options = Options()
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        print("[DRIVER] Chrome 설정 완료")
    
    def initial_login_and_enter(self):
        """최초 로그인 및 상품 수정 페이지 진입"""
        try:
            # 1. 관리자 페이지 접속
            self.driver.get(self.config['cafe24']['admin_url'])
            time.sleep(3)
            
            # 2. 보안 알림 처리
            try:
                alert = self.driver.switch_to.alert
                alert.accept()
                time.sleep(1)
            except:
                pass
            
            # 3. 로그인
            username = self.driver.find_element(By.XPATH, "//input[@type='text' and not(@placeholder='')]")
            username.send_keys(self.config['cafe24']['username'])
            
            password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            password.send_keys(self.config['cafe24']['password'])
            
            # Enter키로 로그인
            password.send_keys('\n')
            time.sleep(5)
            
            print("[LOGIN] 로그인 성공")
            
            # 4. 첫 번째 상품 수정 페이지로 진입
            if self.products:
                first_product = self.products[0]['no']
                url = f"https://manwonyori.cafe24.com/disp/admin/shop1/product/ProductRegister?product_no={first_product}"
                self.driver.get(url)
                time.sleep(5)
                
                print(f"[ENTER] 상품 수정 페이지 진입 (시작: {first_product})")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] 초기 진입 실패: {e}")
            return False
    
    def download_current_page(self, product_name):
        """현재 페이지의 HTML 다운로드 - 성공한 방식 그대로"""
        try:
            # 현재 URL에서 product_no 추출
            current_url = self.driver.current_url
            product_no = current_url.split('product_no=')[1].split('&')[0]
            
            # 상세설명 탭으로 이동 (#tabCont1_2)
            try:
                # 탭 링크 클릭
                tab_link = self.driver.find_element(By.CSS_SELECTOR, 'a[href="#tabCont1_2"]')
                self.driver.execute_script("arguments[0].click();", tab_link)
                time.sleep(1)
                print(f"    [TAB] 상세설명 탭 이동")
            except:
                # JavaScript로 탭 전환
                try:
                    self.driver.execute_script("location.hash = '#tabCont1_2'")
                    time.sleep(1)
                except:
                    pass
            
            # HTML 소스 버튼 클릭 (</>)
            try:
                # Froala Editor의 HTML 버튼
                html_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'button[data-cmd="html"], button[title="HTML"], .fr-command[data-cmd="html"]')
                for btn in html_buttons:
                    if btn.is_displayed():
                        self.driver.execute_script("arguments[0].click();", btn)
                        time.sleep(1)
                        print(f"    [HTML] 소스 보기 버튼 클릭")
                        break
            except:
                pass
            
            # HTML 추출 - complete_content_manager.py와 동일한 방식
            detail_html = None
            
            # 1차 시도: product_description ID로 찾기
            try:
                detail_element = self.driver.find_element(By.ID, "product_description")
                detail_html = detail_element.get_attribute('value')
                print(f"    [FOUND] product_description element")
            except:
                pass
            
            # 2차 시도: editor를 포함하는 iframe 찾기
            if not detail_html:
                try:
                    # ID에 'editor'가 포함된 iframe 찾기
                    iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                    for iframe in iframes:
                        iframe_id = iframe.get_attribute('id') or ''
                        if 'editor' in iframe_id.lower():
                            self.driver.switch_to.frame(iframe)
                            detail_html = self.driver.find_element(By.TAG_NAME, "body").get_attribute('innerHTML')
                            self.driver.switch_to.default_content()
                            print(f"    [FOUND] editor iframe: {iframe_id}")
                            break
                except Exception as e:
                    print(f"    [ERROR] iframe 찾기 실패: {e}")
            
            # 3차 시도: prd-detail iframe (기존 방식)
            if not detail_html:
                try:
                    iframe = self.driver.find_element(By.ID, "prd-detail")
                    self.driver.switch_to.frame(iframe)
                    detail_html = self.driver.find_element(By.TAG_NAME, "body").get_attribute('innerHTML')
                    self.driver.switch_to.default_content()
                    print(f"    [FOUND] prd-detail iframe")
                except:
                    pass
            
            # HTML 저장
            if detail_html and len(detail_html) > 100:
                # 업체 분류
                supplier = "기타"
                if "인생만두" in product_name:
                    supplier = "인생만두"
                elif "만원요리" in product_name:
                    supplier = "만원요리"
                elif "가마솥" in product_name:
                    supplier = "가마솥"
                elif "인생양념" in product_name:
                    supplier = "인생양념"
                elif "씨씨더블유" in product_name or "CCW" in product_name:
                    supplier = "씨씨더블유"
                elif "에스엘" in product_name:
                    supplier = "에스엘"
                
                # 저장
                supplier_folder = os.path.join(self.base_folder, "html", supplier)
                os.makedirs(supplier_folder, exist_ok=True)
                
                html_file = os.path.join(supplier_folder, f"{product_no}.html")
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(detail_html)
                
                print(f"    [SAVED] {len(detail_html)} bytes -> {supplier}/{product_no}.html")
                return True
            else:
                print(f"    [FAIL] HTML 없음 또는 너무 짧음 ({len(detail_html) if detail_html else 0} bytes)")
                return False
                
        except Exception as e:
            print(f"    [ERROR] 다운로드 실패: {e}")
            return False
    
    def change_product_url(self, product_no):
        """JavaScript로 URL의 product_no만 변경"""
        script = f"""
        window.location.href = 'https://manwonyori.cafe24.com/disp/admin/shop1/product/ProductRegister?product_no={product_no}';
        """
        self.driver.execute_script(script)
        time.sleep(5)  # 페이지 로드 대기
    
    def run(self):
        """실행"""
        print("="*60)
        print("[VERIFIED] 검증된 다운로더 시작")
        print(f"시작: {datetime.now().strftime('%H:%M:%S')}")
        print("="*60)
        
        # 드라이버 설정
        self.setup_driver()
        
        # 최초 로그인 및 상품 수정 페이지 진입
        if not self.initial_login_and_enter():
            print("[ERROR] 초기 진입 실패")
            self.driver.quit()
            return
        
        # 통계
        stats = {
            'processed': 0,
            'success': 0,
            'failed': 0
        }
        start_time = datetime.now()
        
        # 모든 상품 처리
        for product in self.products:
            product_no = product['no']
            product_name = product['name']
            
            # 이미 완료된 상품 건너뛰기
            if product_no in self.completed:
                continue
            
            # URL 변경 (같은 창에서)
            self.change_product_url(product_no)
            
            stats['processed'] += 1
            print(f"\n[{stats['processed']}] 상품 {product_no}: {product_name[:30]}...")
            
            # 다운로드
            success = self.download_current_page(product_name)
            
            if success:
                stats['success'] += 1
                print(f"    [OK] 성공")
            else:
                stats['failed'] += 1
                print(f"    [FAIL] 실패")
            
            # 진행률 (10개마다)
            if stats['processed'] % 10 == 0:
                elapsed = (datetime.now() - start_time).total_seconds()
                rate = stats['processed'] / elapsed if elapsed > 0 else 0
                
                print(f"\n[PROGRESS] {datetime.now().strftime('%H:%M:%S')}")
                print(f"  처리: {stats['processed']}, 성공: {stats['success']}")
                print(f"  속도: {rate*60:.1f}개/분\n")
            
            # 서버 부하 방지 (30-45초 랜덤)
            wait_time = random.randint(30, 45)
            time.sleep(wait_time)
            
            # 30개마다 1분 휴식
            if stats['processed'] % 30 == 0:
                print("\n[PAUSE] 1분 휴식...")
                time.sleep(60)
        
        # 드라이버 종료
        self.driver.quit()
        
        # 최종 보고
        elapsed = datetime.now() - start_time
        print("\n" + "="*60)
        print("[COMPLETE] 다운로드 완료")
        print(f"처리: {stats['processed']}개")
        print(f"성공: {stats['success']}개")
        print(f"실패: {stats['failed']}개")
        print(f"총 완료: {len(self.completed) + stats['success']}개")
        print(f"소요 시간: {str(elapsed).split('.')[0]}")
        print("="*60)

if __name__ == "__main__":
    downloader = VerifiedDownloader()
    downloader.run()
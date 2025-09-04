"""
다운로드 재시작 - 미완료 상품만 처리
"""
import os
import json
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

class RestartDownloader:
    def __init__(self):
        self.base_path = r"C:\Users\8899y\CUA-MASTER\modules\cafe24"
        self.html_folder = os.path.join(self.base_path, "complete_content", "html")
        self.download_folder = os.path.join(self.base_path, "download")
        
        # 이미 다운로드된 파일 목록
        self.downloaded = set()
        for root, dirs, files in os.walk(self.html_folder):
            for file in files:
                if file.endswith('.html'):
                    product_no = file.replace('.html', '')
                    self.downloaded.add(int(product_no) if product_no.isdigit() else product_no)
        
        print(f"[CHECK] 이미 다운로드: {len(self.downloaded)}개")
        
        # retry_list.json 로드
        retry_path = os.path.join(self.base_path, "retry_list.json")
        if os.path.exists(retry_path):
            with open(retry_path, 'r', encoding='utf-8') as f:
                self.retry_list = json.load(f)
            print(f"[LOAD] 재시도 목록: {len(self.retry_list)}개")
        else:
            self.retry_list = []
        
        self.driver = None
        
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
    
    def login(self):
        """로그인"""
        try:
            # 로그인 페이지로 직접 이동
            self.driver.get("https://manwonyori.cafe24.com/admin/")
            time.sleep(3)
            
            # Alert 처리 (여러 번 나올 수 있음)
            alert_count = 0
            while alert_count < 5:
                try:
                    alert = self.driver.switch_to.alert
                    alert_text = alert.text
                    print(f"[ALERT {alert_count+1}] {alert_text}")
                    alert.accept()
                    time.sleep(1)
                    alert_count += 1
                except:
                    break
            
            # 로그인 필요한 경우
            if "login" in self.driver.current_url.lower():
                username = self.driver.find_element(By.XPATH, "//input[@type='text' and not(@placeholder='')]")
                username.send_keys("manwonyori")
                
                password = self.driver.find_element(By.XPATH, "//input[@type='password']")
                password.send_keys("happy8263!")
                password.send_keys('\n')
                
                time.sleep(5)
                print("[LOGIN] 로그인 완료")
            
            # 상품 목록 페이지로 이동
            self.driver.get("https://manwonyori.cafe24.com/disp/admin/shop1/product/ProductRegister")
            time.sleep(2)
            
            return True
            
        except Exception as e:
            print(f"[ERROR] 로그인 실패: {e}")
            return False
    
    def download_product(self, product_no, product_name):
        """상품 다운로드"""
        try:
            # URL 변경 (JavaScript)
            script = f"window.location.href = 'https://manwonyori.cafe24.com/disp/admin/shop1/product/ProductRegister?product_no={product_no}'"
            self.driver.execute_script(script)
            time.sleep(2)
            
            # 상세설명 탭으로 이동
            try:
                tab_link = self.driver.find_element(By.CSS_SELECTOR, 'a[href="#tabCont1_2"]')
                self.driver.execute_script("arguments[0].click();", tab_link)
                time.sleep(1)
            except:
                self.driver.execute_script("location.hash = '#tabCont1_2'")
                time.sleep(1)
            
            # HTML 소스 버튼 클릭
            try:
                html_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'button[data-cmd="html"], button[title="HTML"], .fr-command[data-cmd="html"]')
                for btn in html_buttons:
                    if btn.is_displayed():
                        self.driver.execute_script("arguments[0].click();", btn)
                        time.sleep(1)
                        break
            except:
                pass
            
            # HTML 추출
            detail_html = None
            
            # product_description textarea
            try:
                detail_element = self.driver.find_element(By.ID, "product_description")
                detail_html = detail_element.get_attribute('value')
            except:
                pass
            
            # iframe 확인
            if not detail_html:
                try:
                    iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                    for iframe in iframes:
                        iframe_id = iframe.get_attribute('id') or ''
                        if 'editor' in iframe_id.lower() or 'prd-detail' in iframe_id:
                            self.driver.switch_to.frame(iframe)
                            detail_html = self.driver.find_element(By.TAG_NAME, "body").get_attribute('innerHTML')
                            self.driver.switch_to.default_content()
                            break
                except:
                    self.driver.switch_to.default_content()
            
            # 저장
            if detail_html and len(detail_html) > 10:
                # 업체 분류
                if "[인생]" in product_name and "만두" not in product_name:
                    supplier = "인생"
                elif "[인생만두]" in product_name:
                    supplier = "인생만두"
                elif "[취영루]" in product_name:
                    supplier = "취영루"
                elif "[최시남매]" in product_name:
                    supplier = "최시남매"
                else:
                    supplier = "기타"
                
                # 폴더 생성
                supplier_folder = os.path.join(self.html_folder, supplier)
                os.makedirs(supplier_folder, exist_ok=True)
                
                # 파일 저장
                file_path = os.path.join(supplier_folder, f"{product_no}.html")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(detail_html)
                
                print(f"    [SUCCESS] {supplier}/{product_no}.html ({len(detail_html)} bytes)")
                return True
            else:
                print(f"    [FAIL] 빈 HTML")
                return False
                
        except Exception as e:
            print(f"    [ERROR] {e}")
            return False
    
    def run(self):
        """실행"""
        print("="*80)
        print("다운로드 재시작")
        print("="*80)
        
        # CSV 로드
        csv_files = [f for f in os.listdir(self.download_folder) if f.endswith('.csv')]
        latest_csv = max(csv_files, key=lambda f: os.path.getctime(os.path.join(self.download_folder, f)))
        csv_path = os.path.join(self.download_folder, latest_csv)
        
        try:
            df = pd.read_csv(csv_path, encoding='utf-8-sig')
        except:
            df = pd.read_csv(csv_path, encoding='cp949')
        
        # 미다운로드 상품 찾기
        to_download = []
        for _, row in df.iterrows():
            product_no = int(row['상품번호'])
            if product_no not in self.downloaded:
                to_download.append({
                    'no': product_no,
                    'name': str(row['상품명']),
                    'code': str(row['상품코드'])
                })
        
        print(f"[TARGET] 다운로드 대상: {len(to_download)}개")
        
        if not to_download:
            print("모든 상품이 이미 다운로드되었습니다.")
            return
        
        # 드라이버 시작
        self.setup_driver()
        
        # 로그인
        if not self.login():
            self.driver.quit()
            return
        
        # 다운로드 시작
        success = 0
        fail = 0
        start_time = datetime.now()
        
        print(f"\n[START] {datetime.now().strftime('%H:%M:%S')}")
        print("-"*80)
        
        for idx, product in enumerate(to_download, 1):
            product_no = product['no']
            product_name = product['name']
            
            try:
                print(f"[{idx}/{len(to_download)}] {product_no}: {product_name[:30]}...")
            except UnicodeEncodeError:
                print(f"[{idx}/{len(to_download)}] {product_no}: [특수문자 포함 상품명]")
            
            if self.download_product(product_no, product_name):
                success += 1
            else:
                fail += 1
            
            # 진행 상황
            if idx % 10 == 0:
                elapsed = (datetime.now() - start_time).seconds
                speed = success / (elapsed/60) if elapsed > 0 else 0
                print(f"\n[PROGRESS] 처리: {idx}, 성공: {success}, 실패: {fail}")
                print(f"[SPEED] {speed:.1f}개/분")
                remaining = len(to_download) - idx
                eta = remaining / speed if speed > 0 else 0
                print(f"[ETA] 약 {int(eta)}분 남음\n")
            
            # 30개마다 휴식
            if idx % 30 == 0:
                print("\n[PAUSE] 1분 휴식...")
                time.sleep(60)
            else:
                time.sleep(2)
        
        # 완료
        print("\n" + "="*80)
        print(f"다운로드 완료: 성공 {success}, 실패 {fail}")
        print(f"소요 시간: {(datetime.now() - start_time).seconds//60}분")
        print("="*80)
        
        # 드라이버 종료
        self.driver.quit()

if __name__ == "__main__":
    downloader = RestartDownloader()
    downloader.run()
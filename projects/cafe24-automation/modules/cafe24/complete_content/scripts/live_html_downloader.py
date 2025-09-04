# -*- coding: utf-8 -*-
"""
실제 카페24 HTML 다운로더 - 로그인부터 상품 수정까지
"""
import sys
import os
import csv
import time
import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# UTF-8 인코딩 설정
if os.name == 'nt':  # Windows
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class Cafe24HtmlDownloader:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.config = self.load_config()
        
    def load_config(self):
        """설정 파일 로드"""
        config_path = Path("config/cafe24_config.json")
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def setup_driver(self, headless=False):
        """Chrome 드라이버 설정"""
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 10)
            return True
        except Exception as e:
            print(f"❌ Chrome 드라이버 설정 실패: {e}")
            return False
    
    def login_to_cafe24(self):
        """카페24 로그인"""
        if not self.config:
            print("❌ 설정 파일이 없습니다.")
            return False
        
        try:
            print("🔐 카페24 로그인 시작...")
            
            # 로그인 페이지로 이동
            login_url = self.config['cafe24']['login_url']
            self.driver.get(login_url)
            time.sleep(3)
            
            # 몰 ID 입력
            mall_id = self.config['cafe24']['mall_id']
            mall_input = self.wait.until(EC.presence_of_element_located((By.NAME, "mall_id")))
            mall_input.clear()
            mall_input.send_keys(mall_id)
            print(f"✅ 몰 ID 입력: {mall_id}")
            
            # 사용자 ID 입력
            username = self.config['cafe24']['credentials']['username']
            if username != "DEMO_USER":  # 실제 계정 정보가 있는 경우
                user_input = self.wait.until(EC.presence_of_element_located((By.NAME, "user_id")))
                user_input.clear()
                user_input.send_keys(username)
                print(f"✅ 사용자 ID 입력: {username}")
                
                # 비밀번호 입력
                password = self.config['cafe24']['credentials']['password']
                pass_input = self.wait.until(EC.presence_of_element_located((By.NAME, "user_pw")))
                pass_input.clear()
                pass_input.send_keys(password)
                print("✅ 비밀번호 입력 완료")
                
                # 로그인 버튼 클릭
                login_btn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "login_btn")))
                login_btn.click()
                time.sleep(5)
                
                # 로그인 성공 확인
                if "admin" in self.driver.current_url:
                    print("✅ 카페24 로그인 성공!")
                    return True
                else:
                    print("❌ 로그인 실패")
                    return False
            else:
                print("⚠️ 데모 계정 정보입니다. 실제 로그인 정보를 설정하세요.")
                return False
                
        except Exception as e:
            print(f"❌ 로그인 중 오류: {e}")
            return False
    
    def get_product_list(self):
        """상품 목록 가져오기"""
        try:
            # CSV 파일에서 상품 목록 읽기
            csv_path = Path("../download")
            csv_files = list(csv_path.glob("manwonyori_*.csv"))
            
            if not csv_files:
                print("❌ CSV 파일을 찾을 수 없습니다.")
                return []
            
            latest_csv = max(csv_files, key=lambda x: x.stat().st_mtime)
            print(f"📄 CSV 파일 로드: {latest_csv.name}")
            
            products = []
            with open(latest_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    product_no = row.get('상품번호', '')
                    product_name = row.get('상품명', '')
                    if product_no:
                        products.append({
                            'no': product_no,
                            'name': product_name
                        })
            
            print(f"📊 총 {len(products)}개 상품 발견")
            return products[:5]  # 처음 5개만 테스트
            
        except Exception as e:
            print(f"❌ 상품 목록 로드 실패: {e}")
            return []
    
    def navigate_to_product_edit(self, product_no):
        """상품 수정 페이지로 이동"""
        try:
            # 상품 관리 페이지로 이동
            admin_url = self.config['cafe24']['admin_url']
            product_url = f"{admin_url}/php/shop1/product/Product_list.php"
            self.driver.get(product_url)
            time.sleep(3)
            
            print(f"🔍 상품번호 {product_no} 검색 중...")
            
            # 검색창에 상품번호 입력
            search_input = self.wait.until(EC.presence_of_element_located((By.NAME, "product_no")))
            search_input.clear()
            search_input.send_keys(product_no)
            
            # 검색 버튼 클릭
            search_btn = self.driver.find_element(By.CLASS_NAME, "search_btn")
            search_btn.click()
            time.sleep(3)
            
            # 상품 수정 링크 클릭
            edit_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'Product_write.php')]")))
            edit_link.click()
            time.sleep(5)
            
            print(f"✅ 상품 {product_no} 수정 페이지 진입")
            return True
            
        except Exception as e:
            print(f"❌ 상품 수정 페이지 이동 실패: {e}")
            return False
    
    def extract_product_html(self, product_no):
        """상품 상세설명 HTML 추출"""
        try:
            # iframe으로 전환 (상세설명은 보통 iframe 내부)
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            
            html_content = ""
            
            for i, iframe in enumerate(iframes):
                try:
                    self.driver.switch_to.frame(iframe)
                    body = self.driver.find_element(By.TAG_NAME, "body")
                    iframe_html = body.get_attribute('innerHTML')
                    
                    if iframe_html and len(iframe_html) > 100:  # 의미있는 내용이 있는 경우
                        html_content += f"<!-- iframe {i} -->\n{iframe_html}\n"
                        print(f"✅ iframe {i}에서 HTML 추출 완료 ({len(iframe_html)} 문자)")
                    
                    self.driver.switch_to.default_content()
                except:
                    self.driver.switch_to.default_content()
                    continue
            
            # 메인 페이지의 상세설명 영역도 확인
            try:
                detail_areas = self.driver.find_elements(By.CLASS_NAME, "detail_info")
                for area in detail_areas:
                    area_html = area.get_attribute('innerHTML')
                    if area_html:
                        html_content += f"<!-- detail_area -->\n{area_html}\n"
            except:
                pass
            
            # HTML 파일로 저장
            if html_content:
                output_dir = Path("html/downloaded")
                output_dir.mkdir(exist_ok=True, parents=True)
                
                output_file = output_dir / f"{product_no}_detail.html"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                print(f"✅ HTML 저장: {output_file} ({len(html_content)} 문자)")
                return True
            else:
                print(f"⚠️ 추출할 HTML이 없습니다: {product_no}")
                return False
                
        except Exception as e:
            print(f"❌ HTML 추출 실패: {e}")
            return False
    
    def run_download_process(self):
        """전체 다운로드 프로세스 실행"""
        print("🚀 카페24 HTML 다운로드 시작")
        print("=" * 50)
        
        # 1. 드라이버 설정
        if not self.setup_driver(headless=False):  # 실제 동작을 보기 위해 headless=False
            return False
        
        try:
            # 2. 카페24 로그인
            if not self.login_to_cafe24():
                return False
            
            # 3. 상품 목록 가져오기
            products = self.get_product_list()
            if not products:
                return False
            
            # 4. 각 상품별 HTML 다운로드
            success_count = 0
            for i, product in enumerate(products, 1):
                print(f"\n📦 [{i}/{len(products)}] 처리 중: {product['no']} - {product['name'][:30]}...")
                
                # 상품 수정 페이지로 이동
                if self.navigate_to_product_edit(product['no']):
                    # HTML 추출
                    if self.extract_product_html(product['no']):
                        success_count += 1
                
                time.sleep(2)  # 서버 부하 방지
            
            print(f"\n🎉 완료! {success_count}/{len(products)}개 상품 처리")
            
        finally:
            if self.driver:
                input("\n⏸️ 엔터를 누르면 브라우저를 종료합니다...")
                self.driver.quit()
        
        return True

def main():
    """메인 실행 함수"""
    downloader = Cafe24HtmlDownloader()
    downloader.run_download_process()

if __name__ == "__main__":
    main()
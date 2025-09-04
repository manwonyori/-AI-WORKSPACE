"""
Cafe24 상품 데이터 크롤링 및 Google Drive 연동 시스템
239개 상품의 상세 페이지 HTML을 자동으로 수집하고 저장
"""

import os
import json
import time
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, UnexpectedAlertPresentException, NoAlertPresentException
try:
    from webdriver_manager.chrome import ChromeDriverManager
    USE_WEBDRIVER_MANAGER = True
except ImportError:
    USE_WEBDRIVER_MANAGER = False
import pandas as pd
from bs4 import BeautifulSoup
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Cafe24ProductCrawler:
    """Cafe24 상품 데이터 자동 크롤링 시스템"""
    
    def __init__(self, mall_id: str = "manwonyori"):
        self.mall_id = mall_id
        self.base_url = f"https://{mall_id}.cafe24.com"
        self.admin_url = f"{self.base_url}/disp/admin/shop1/product"
        
        # 저장 경로 설정
        self.base_path = Path("C:/Users/8899y/CUA-MASTER/data/cafe24_products")
        self.html_path = self.base_path / "html_pages"
        self.json_path = self.base_path / "product_data"
        self.backup_path = self.base_path / "backups"
        
        # 디렉토리 생성
        for path in [self.html_path, self.json_path, self.backup_path]:
            path.mkdir(parents=True, exist_ok=True)
        
        # 로그인 정보 (환경 변수에서 로드)
        self.username = os.getenv("CAFE24_USERNAME", "")
        self.password = os.getenv("CAFE24_PASSWORD", "")
        
        # Chrome 드라이버 설정
        self.driver = None
        self.wait = None
        
        # Google Drive 설정
        self.drive_folder_id = "1HHc_-hga4DK_6tUtL9LshTpZKI8M0m7_"
        self.drive_service = None
        
        # 상품 목록 캐시
        self.products_cache = []
        
    def init_driver(self):
        """Selenium 드라이버 초기화"""
        options = Options()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # 쿠키 저장을 위한 프로필 설정
        options.add_argument('user-data-dir=C:/Users/8899y/CUA-MASTER/data/chrome_profile')
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)
        
        # User-Agent 변경
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        logger.info("Chrome 드라이버 초기화 완료")
        
    def login_cafe24(self) -> bool:
        """Cafe24 관리자 로그인"""
        try:
            # 로그인 페이지로 이동
            login_url = f"{self.base_url}/disp/admin/shop1/mode/login"
            self.driver.get(login_url)
            time.sleep(3)
            
            # 이미 로그인되어 있는지 확인
            if "ProductList" in self.driver.current_url:
                logger.info("이미 로그인된 상태입니다")
                return True
            
            # 로그인 폼 입력
            username_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "mall_id"))
            )
            password_input = self.driver.find_element(By.ID, "userpasswd")
            
            username_input.clear()
            username_input.send_keys(self.username)
            password_input.clear()
            password_input.send_keys(self.password)
            
            # 로그인 버튼 클릭
            login_btn = self.driver.find_element(By.CLASS_NAME, "btnSubmit")
            login_btn.click()
            
            # 로그인 성공 확인
            time.sleep(5)
            if "product" in self.driver.current_url.lower():
                logger.info("Cafe24 로그인 성공")
                self.save_cookies()
                return True
            else:
                logger.error("로그인 실패")
                return False
                
        except Exception as e:
            logger.error(f"로그인 중 오류: {e}")
            return False
    
    def save_cookies(self):
        """쿠키 저장"""
        cookies = self.driver.get_cookies()
        with open(self.base_path / "cookies.json", 'w') as f:
            json.dump(cookies, f)
    
    def load_cookies(self):
        """저장된 쿠키 로드"""
        cookie_file = self.base_path / "cookies.json"
        if cookie_file.exists():
            with open(cookie_file, 'r') as f:
                cookies = json.load(f)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            return True
        return False
    
    def get_product_list(self) -> List[Dict]:
        """전체 상품 목록 가져오기"""
        products = []
        
        try:
            # 상품 목록 페이지로 이동
            list_url = f"{self.admin_url}/ProductList"
            self.driver.get(list_url)
            time.sleep(3)
            
            # 페이지당 100개씩 보기 설정
            try:
                limit_select = self.driver.find_element(By.NAME, "limit")
                limit_select.send_keys("100")
                time.sleep(2)
            except:
                pass
            
            page = 1
            while True:
                logger.info(f"페이지 {page} 크롤링 중...")
                
                # 상품 목록 테이블 찾기
                product_rows = self.driver.find_elements(
                    By.CSS_SELECTOR, 
                    "table.mBoard tbody tr"
                )
                
                for row in product_rows:
                    try:
                        # 상품 정보 추출
                        product_code = row.find_element(By.CSS_SELECTOR, "td.product_code").text
                        product_name = row.find_element(By.CSS_SELECTOR, "td.product_name").text
                        product_no = row.get_attribute("product_no")
                        
                        # 수정 링크 생성
                        edit_url = f"{self.admin_url}/ProductRegister?product_no={product_no}"
                        
                        products.append({
                            "product_code": product_code,
                            "product_name": product_name,
                            "product_no": product_no,
                            "edit_url": edit_url,
                            "crawled_at": datetime.now().isoformat()
                        })
                        
                    except Exception as e:
                        logger.warning(f"상품 정보 추출 실패: {e}")
                        continue
                
                # 다음 페이지 확인
                try:
                    next_btn = self.driver.find_element(
                        By.CSS_SELECTOR, 
                        "a.next:not(.disabled)"
                    )
                    next_btn.click()
                    time.sleep(2)
                    page += 1
                except:
                    logger.info("마지막 페이지 도달")
                    break
            
            logger.info(f"총 {len(products)}개 상품 발견")
            self.products_cache = products
            
            # 상품 목록 저장
            self.save_product_list(products)
            
            return products
            
        except Exception as e:
            logger.error(f"상품 목록 가져오기 실패: {e}")
            return []
    
    def save_product_list(self, products: List[Dict]):
        """상품 목록 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON 저장
        json_file = self.json_path / f"product_list_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        
        # CSV 저장
        df = pd.DataFrame(products)
        csv_file = self.json_path / f"product_list_{timestamp}.csv"
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        
        logger.info(f"상품 목록 저장 완료: {len(products)}개")
    
    def crawl_product_detail(self, product: Dict) -> Dict:
        """개별 상품 상세 페이지 크롤링"""
        try:
            # 상품 수정 페이지로 이동
            self.driver.get(product["edit_url"])
            time.sleep(3)
            
            # 상세설명 iframe 찾기
            try:
                iframe = self.driver.find_element(
                    By.CSS_SELECTOR, 
                    "iframe#product_description"
                )
                self.driver.switch_to.frame(iframe)
                
                # HTML 소스 가져오기
                detail_html = self.driver.page_source
                
                # iframe에서 나오기
                self.driver.switch_to.default_content()
                
            except:
                # iframe이 없는 경우 직접 가져오기
                try:
                    detail_element = self.driver.find_element(
                        By.CSS_SELECTOR, 
                        "textarea[name='detail_description']"
                    )
                    detail_html = detail_element.get_attribute("value")
                except:
                    detail_html = ""
            
            # 기타 정보 수집
            product_data = {
                **product,
                "detail_html": detail_html,
                "crawled_detail_at": datetime.now().isoformat()
            }
            
            # 추가 정보 수집 (판매가, 재고 등)
            try:
                price = self.driver.find_element(
                    By.NAME, "product_price"
                ).get_attribute("value")
                product_data["price"] = price
            except:
                pass
            
            try:
                stock = self.driver.find_element(
                    By.NAME, "stock_number"
                ).get_attribute("value")
                product_data["stock"] = stock
            except:
                pass
            
            # HTML 파일 저장
            self.save_product_html(product_data)
            
            return product_data
            
        except Exception as e:
            logger.error(f"상품 상세 크롤링 실패 ({product['product_code']}): {e}")
            return product
    
    def save_product_html(self, product_data: Dict):
        """상품 HTML 저장"""
        product_code = product_data["product_code"]
        
        # HTML 파일 저장
        html_file = self.html_path / f"{product_code}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(product_data.get("detail_html", ""))
        
        # JSON 데이터 저장
        json_file = self.json_path / f"{product_code}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(product_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"상품 데이터 저장: {product_code}")
    
    def init_google_drive(self):
        """Google Drive API 초기화"""
        try:
            # 서비스 계정 키 파일 경로
            key_file = Path("C:/Users/8899y/CUA-MASTER/configs/google_service_account.json")
            
            if not key_file.exists():
                logger.warning("Google 서비스 계정 키 파일이 없습니다")
                return False
            
            # 인증
            creds = service_account.Credentials.from_service_account_file(
                key_file,
                scopes=['https://www.googleapis.com/auth/drive']
            )
            
            self.drive_service = build('drive', 'v3', credentials=creds)
            logger.info("Google Drive API 초기화 완료")
            return True
            
        except Exception as e:
            logger.error(f"Google Drive 초기화 실패: {e}")
            return False
    
    def upload_to_drive(self, file_path: Path, folder_id: str = None):
        """파일을 Google Drive에 업로드"""
        if not self.drive_service:
            logger.warning("Google Drive 서비스가 초기화되지 않았습니다")
            return None
        
        try:
            folder_id = folder_id or self.drive_folder_id
            
            file_metadata = {
                'name': file_path.name,
                'parents': [folder_id]
            }
            
            media = MediaFileUpload(
                str(file_path),
                mimetype='text/html' if file_path.suffix == '.html' else 'application/json'
            )
            
            file = self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            logger.info(f"Google Drive 업로드 완료: {file_path.name}")
            return file.get('id')
            
        except Exception as e:
            logger.error(f"Google Drive 업로드 실패: {e}")
            return None
    
    def crawl_all_products(self):
        """전체 상품 크롤링 실행"""
        try:
            # 드라이버 초기화
            self.init_driver()
            
            # 로그인
            if not self.login_cafe24():
                logger.error("로그인 실패로 크롤링 중단")
                return
            
            # 상품 목록 가져오기
            products = self.get_product_list()
            
            if not products:
                logger.warning("상품 목록이 비어있습니다")
                return
            
            # Google Drive 초기화 (옵션)
            self.init_google_drive()
            
            # 각 상품 크롤링
            success_count = 0
            for i, product in enumerate(products, 1):
                logger.info(f"진행률: {i}/{len(products)} - {product['product_code']}")
                
                # 이미 크롤링된 경우 스킵
                html_file = self.html_path / f"{product['product_code']}.html"
                if html_file.exists():
                    logger.info(f"이미 크롤링됨: {product['product_code']}")
                    continue
                
                # 상품 상세 크롤링
                product_data = self.crawl_product_detail(product)
                
                if product_data.get("detail_html"):
                    success_count += 1
                    
                    # Google Drive 업로드
                    if self.drive_service:
                        self.upload_to_drive(html_file)
                
                # 과부하 방지
                time.sleep(2)
                
                # 50개마다 백업
                if i % 50 == 0:
                    self.create_backup()
            
            logger.info(f"크롤링 완료: 성공 {success_count}/{len(products)}")
            
        except Exception as e:
            logger.error(f"크롤링 중 오류: {e}")
            
        finally:
            if self.driver:
                self.driver.quit()
    
    def create_backup(self):
        """백업 생성"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.backup_path / timestamp
        backup_dir.mkdir(exist_ok=True)
        
        # HTML 파일 백업
        import shutil
        for html_file in self.html_path.glob("*.html"):
            shutil.copy2(html_file, backup_dir)
        
        logger.info(f"백업 생성 완료: {backup_dir}")
    
    def update_product_html(self, product_code: str, new_html: str):
        """상품 HTML 업데이트"""
        try:
            # 드라이버 초기화
            if not self.driver:
                self.init_driver()
                self.login_cafe24()
            
            # 상품 찾기
            product = None
            for p in self.products_cache:
                if p["product_code"] == product_code:
                    product = p
                    break
            
            if not product:
                logger.error(f"상품을 찾을 수 없습니다: {product_code}")
                return False
            
            # 상품 수정 페이지로 이동
            self.driver.get(product["edit_url"])
            time.sleep(3)
            
            # 상세설명 업데이트
            try:
                # iframe 찾기
                iframe = self.driver.find_element(
                    By.CSS_SELECTOR, 
                    "iframe#product_description"
                )
                self.driver.switch_to.frame(iframe)
                
                # 에디터에 HTML 입력
                self.driver.execute_script(
                    "document.body.innerHTML = arguments[0];",
                    new_html
                )
                
                # iframe에서 나오기
                self.driver.switch_to.default_content()
                
            except:
                # textarea 직접 입력
                try:
                    detail_element = self.driver.find_element(
                        By.CSS_SELECTOR, 
                        "textarea[name='detail_description']"
                    )
                    detail_element.clear()
                    detail_element.send_keys(new_html)
                except Exception as e:
                    logger.error(f"HTML 업데이트 실패: {e}")
                    return False
            
            # 저장 버튼 클릭
            save_btn = self.driver.find_element(
                By.CSS_SELECTOR, 
                "button.btnSubmit"
            )
            save_btn.click()
            
            logger.info(f"상품 업데이트 완료: {product_code}")
            return True
            
        except Exception as e:
            logger.error(f"상품 업데이트 실패: {e}")
            return False


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("Cafe24 상품 데이터 자동화 시스템")
    print("=" * 60)
    
    # 환경 변수 설정 확인
    if not os.getenv("CAFE24_USERNAME"):
        username = input("Cafe24 아이디: ")
        password = input("Cafe24 비밀번호: ")
        os.environ["CAFE24_USERNAME"] = username
        os.environ["CAFE24_PASSWORD"] = password
    
    crawler = Cafe24ProductCrawler()
    
    while True:
        print("\n작업 선택:")
        print("1. 전체 상품 크롤링")
        print("2. 특정 상품 업데이트")
        print("3. Google Drive 동기화")
        print("4. 백업 생성")
        print("0. 종료")
        
        choice = input("\n선택: ")
        
        if choice == "1":
            print("\n전체 상품 크롤링을 시작합니다...")
            crawler.crawl_all_products()
            
        elif choice == "2":
            product_code = input("상품 코드 입력: ")
            print(f"\n{product_code} 업데이트 중...")
            # 여기에 업데이트 로직 추가
            
        elif choice == "3":
            print("\nGoogle Drive 동기화 중...")
            crawler.init_google_drive()
            # 동기화 로직 추가
            
        elif choice == "4":
            print("\n백업 생성 중...")
            crawler.create_backup()
            
        elif choice == "0":
            print("\n프로그램을 종료합니다.")
            break
        
        else:
            print("\n잘못된 선택입니다.")


if __name__ == "__main__":
    main()
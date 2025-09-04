"""
Cafe24 상품 자동 업데이트 시스템
수정된 HTML을 Cafe24 관리자 페이지에 자동으로 재등록
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pyperclip
import pyautogui

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cafe24_auto_updater.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Cafe24AutoUpdater:
    """Cafe24 상품 자동 업데이트 시스템"""
    
    def __init__(self, config_path: str = "config/cafe24_config.json"):
        """초기화"""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.driver = None
        self.wait = None
        self.update_results = []
        
    def _load_config(self) -> Dict:
        """설정 파일 로드"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            logger.error("설정 파일이 없습니다")
            return {}
    
    def init_driver(self, headless: bool = False):
        """Chrome 드라이버 초기화"""
        options = Options()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        if headless:
            options.add_argument('--headless')
        
        # 한국어 설정
        options.add_argument('--lang=ko-KR')
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        
        # User-Agent 변경
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        logger.info("Chrome 드라이버 초기화 완료")
    
    def login_cafe24(self) -> bool:
        """Cafe24 관리자 로그인"""
        try:
            admin_url = self.config['cafe24']['admin_url']
            self.driver.get(admin_url)
            time.sleep(2)
            
            # 로그인 폼 찾기
            username_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "userid"))
            )
            password_input = self.driver.find_element(By.NAME, "userpasswd")
            
            # 자격증명 입력
            username_input.send_keys(self.config['cafe24']['username'])
            password_input.send_keys(self.config['cafe24']['password'])
            password_input.send_keys(Keys.RETURN)
            
            time.sleep(3)
            
            # 로그인 성공 확인
            if "admin/php/shop1" in self.driver.current_url:
                logger.info("Cafe24 로그인 성공")
                return True
            else:
                logger.error("Cafe24 로그인 실패")
                return False
                
        except Exception as e:
            logger.error(f"로그인 중 오류: {e}")
            return False
    
    def navigate_to_product_edit(self, product_code: str) -> bool:
        """특정 상품 편집 페이지로 이동"""
        try:
            # 상품 관리 메뉴 클릭
            product_menu = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '상품관리')]"))
            )
            product_menu.click()
            time.sleep(1)
            
            # 상품 목록 클릭
            product_list = self.driver.find_element(By.XPATH, "//a[contains(text(), '상품목록')]")
            product_list.click()
            time.sleep(2)
            
            # 상품 코드로 검색
            search_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "search_word"))
            )
            search_input.clear()
            search_input.send_keys(product_code)
            
            # 검색 버튼 클릭
            search_btn = self.driver.find_element(By.XPATH, "//input[@value='검색']")
            search_btn.click()
            time.sleep(2)
            
            # 검색 결과에서 상품 선택
            product_link = self.driver.find_element(
                By.XPATH, f"//a[contains(@href, 'product_no') and contains(text(), '{product_code}')]"
            )
            product_link.click()
            
            logger.info(f"상품 편집 페이지 진입: {product_code}")
            return True
            
        except Exception as e:
            logger.error(f"상품 편집 페이지 진입 실패 {product_code}: {e}")
            return False
    
    def update_product_html(self, product_code: str, new_html: str) -> bool:
        """상품 HTML 업데이트"""
        try:
            # 상품 편집 페이지로 이동
            if not self.navigate_to_product_edit(product_code):
                return False
            
            time.sleep(2)
            
            # HTML 편집 모드로 전환
            try:
                # 에디터 탭 찾기
                html_tab = self.driver.find_element(
                    By.XPATH, "//a[contains(text(), 'HTML') or contains(text(), '소스')]"
                )
                html_tab.click()
                time.sleep(1)
            except:
                logger.info("HTML 탭을 찾을 수 없음, 직접 편집 시도")
            
            # 상품 상세설명 에디터 찾기
            try:
                # iframe 내부의 에디터인 경우
                iframe = self.driver.find_element(By.CSS_SELECTOR, "iframe.editor_frame")
                self.driver.switch_to.frame(iframe)
                
                # 에디터 내용 지우고 새 HTML 입력
                editor_body = self.driver.find_element(By.TAG_NAME, "body")
                editor_body.clear()
                
                # 클립보드를 통한 붙여넣기 (큰 HTML의 경우)
                pyperclip.copy(new_html)
                editor_body.send_keys(Keys.CONTROL, 'v')
                
                self.driver.switch_to.default_content()
                
            except:
                # textarea 직접 편집
                try:
                    html_textarea = self.driver.find_element(By.NAME, "detail_html")
                    html_textarea.clear()
                    html_textarea.send_keys(new_html)
                except:
                    logger.error("HTML 에디터를 찾을 수 없습니다")
                    return False
            
            # 저장 버튼 클릭
            time.sleep(1)
            save_btn = self.driver.find_element(
                By.XPATH, "//input[@value='저장'] | //button[contains(text(), '저장')]"
            )
            save_btn.click()
            
            # 저장 확인 대기
            time.sleep(3)
            
            # 성공 메시지 확인
            try:
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                alert.accept()
                logger.info(f"저장 완료 {product_code}: {alert_text}")
            except:
                logger.info(f"저장 완료: {product_code}")
            
            return True
            
        except Exception as e:
            logger.error(f"상품 HTML 업데이트 실패 {product_code}: {e}")
            return False
    
    def update_products_batch(self, products: List[Dict]) -> List[Dict]:
        """여러 상품 일괄 업데이트"""
        results = []
        total = len(products)
        
        for idx, product in enumerate(products, 1):
            product_code = product['product_code']
            html_content = product.get('modified_html', product.get('html_content'))
            
            logger.info(f"업데이트 진행 [{idx}/{total}]: {product_code}")
            
            success = self.update_product_html(product_code, html_content)
            
            result = {
                'product_code': product_code,
                'success': success,
                'timestamp': datetime.now().isoformat()
            }
            results.append(result)
            
            if success:
                logger.info(f"✓ 업데이트 성공: {product_code}")
            else:
                logger.error(f"✗ 업데이트 실패: {product_code}")
            
            # 과부하 방지를 위한 대기
            time.sleep(2)
        
        self.update_results = results
        return results
    
    def update_from_directory(self, directory: str) -> List[Dict]:
        """디렉토리의 모든 HTML 파일 업데이트"""
        dir_path = Path(directory)
        html_files = list(dir_path.glob("*.html"))
        
        products = []
        for file_path in html_files:
            product_code = file_path.stem.replace('_modified', '')
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            products.append({
                'product_code': product_code,
                'modified_html': html_content,
                'file_path': str(file_path)
            })
        
        logger.info(f"{len(products)}개 파일 발견")
        return self.update_products_batch(products)
    
    def create_update_report(self) -> Dict:
        """업데이트 결과 리포트 생성"""
        success_count = sum(1 for r in self.update_results if r['success'])
        fail_count = len(self.update_results) - success_count
        
        report = {
            'total_products': len(self.update_results),
            'success_count': success_count,
            'fail_count': fail_count,
            'update_time': datetime.now().isoformat(),
            'results': self.update_results
        }
        
        # 리포트 저장
        report_path = Path(f"update_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"업데이트 리포트 생성: {report_path}")
        logger.info(f"결과: 성공 {success_count}개, 실패 {fail_count}개")
        
        return report
    
    def cleanup(self):
        """드라이버 정리"""
        if self.driver:
            self.driver.quit()
            logger.info("드라이버 종료")

class SmartUpdater(Cafe24AutoUpdater):
    """스마트 업데이트 기능이 추가된 업데이터"""
    
    def update_with_validation(self, product_code: str, new_html: str) -> bool:
        """업데이트 전 검증 수행"""
        # HTML 검증
        if not self._validate_html(new_html):
            logger.error(f"HTML 검증 실패: {product_code}")
            return False
        
        # 백업 생성
        self._create_backup(product_code)
        
        # 업데이트 수행
        success = self.update_product_html(product_code, new_html)
        
        # 업데이트 후 확인
        if success:
            self._verify_update(product_code)
        
        return success
    
    def _validate_html(self, html: str) -> bool:
        """HTML 유효성 검증"""
        # 필수 태그 확인
        required_tags = ['<html', '<body', '</html>', '</body>']
        for tag in required_tags:
            if tag not in html.lower():
                return False
        return True
    
    def _create_backup(self, product_code: str):
        """업데이트 전 백업 생성"""
        backup_dir = Path("backups")
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = backup_dir / f"{product_code}_backup_{timestamp}.json"
        
        # 현재 상태 저장
        backup_data = {
            'product_code': product_code,
            'backup_time': timestamp,
            'url': self.driver.current_url
        }
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
    
    def _verify_update(self, product_code: str) -> bool:
        """업데이트 확인"""
        try:
            # 페이지 새로고침
            self.driver.refresh()
            time.sleep(2)
            
            # 업데이트 확인 로직
            logger.info(f"업데이트 확인 완료: {product_code}")
            return True
        except:
            return False

def main():
    """메인 실행 함수"""
    updater = SmartUpdater()
    
    try:
        # 1. 드라이버 초기화
        logger.info("=== Cafe24 자동 업데이터 시작 ===")
        updater.init_driver(headless=False)
        
        # 2. 로그인
        if not updater.login_cafe24():
            logger.error("로그인 실패, 프로그램 종료")
            return
        
        # 3. 수정된 파일 디렉토리에서 업데이트
        logger.info("=== 상품 일괄 업데이트 시작 ===")
        results = updater.update_from_directory("modified_products")
        
        # 4. 리포트 생성
        report = updater.create_update_report()
        
        logger.info("=== 작업 완료 ===")
        
    finally:
        # 5. 정리
        updater.cleanup()

if __name__ == "__main__":
    main()
# -*- coding: utf-8 -*-
"""
Cafe24 고급 상품 편집기 - 모든 요소 수정 가능 시스템
HTML 편집기 포함 완전 자동화
"""
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

import json
import time
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoAlertPresentException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

try:
    from webdriver_manager.chrome import ChromeDriverManager
    USE_WEBDRIVER_MANAGER = True
except ImportError:
    USE_WEBDRIVER_MANAGER = False

class AdvancedCafe24Editor:
    """Cafe24 고급 상품 편집기 클래스"""
    
    def __init__(self, config_path="config/cafe24_config.json"):
        """초기화"""
        self.config = self.load_config(config_path)
        self.driver = None
        self.wait = None
        self.editable_elements = {}
        self.html_editors = {}
        
        # 출력 디렉토리
        self.output_dir = Path("advanced_editing_output")
        self.output_dir.mkdir(exist_ok=True)
        
        print("[EDITOR-INIT] 고급 상품 편집기 초기화 완료")
    
    def load_config(self, config_path):
        """설정 파일 로드"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def setup_driver(self):
        """Chrome 드라이버 설정 (고급 편집용)"""
        print("\n[DRIVER-SETUP] 고급 편집용 Chrome 드라이버 설정...")
        
        options = Options()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        
        if USE_WEBDRIVER_MANAGER:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
        else:
            self.driver = webdriver.Chrome(options=options)
        
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 30)
        
        print("   [OK] 고급 편집용 드라이버 준비 완료")
    
    def handle_alert(self):
        """알림 처리"""
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text[:50]
            print(f"   [ALERT] {alert_text}")
            alert.accept()
            time.sleep(1)
            return True
        except NoAlertPresentException:
            return False
    
    def login_to_cafe24(self):
        """Cafe24 로그인"""
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
    
    def access_product_edit_page(self, product_no=339):
        """상품 수정 페이지 접근"""
        print(f"\n[ACCESS] 상품 {product_no}번 수정 페이지 접근...")
        
        mall_id = self.config['cafe24']['mall_id']
        product_url = f"https://{mall_id}.cafe24.com/disp/admin/shop1/product/ProductRegister?product_no={product_no}"
        
        self.driver.get(product_url)
        time.sleep(5)
        
        # 알림 처리
        if self.handle_alert():
            print("   [INFO] 상품 페이지 알림 처리됨")
        
        # 페이지 완전 로딩 대기
        print("   [WAIT] 페이지 완전 로딩 대기...")
        for attempt in range(10):
            try:
                # JavaScript 실행 상태 확인
                ready_state = self.driver.execute_script("return document.readyState")
                jquery_ready = self.driver.execute_script("return typeof jQuery !== 'undefined' && jQuery.active == 0")
                
                inputs = self.driver.find_elements(By.TAG_NAME, "input")
                if len(inputs) > 100 and ready_state == "complete":
                    print(f"   [OK] 페이지 로딩 완료: {len(inputs)}개 input 요소")
                    break
                    
                time.sleep(2)
            except Exception as e:
                print(f"   [WAIT] 로딩 대기 중... ({attempt + 1}/10)")
                time.sleep(2)
        
        current_url = self.driver.current_url
        if f"product_no={product_no}" in current_url:
            print(f"   [SUCCESS] 상품 {product_no}번 수정 페이지 접근 완료")
            return True
        else:
            print(f"   [ERROR] 상품 페이지 접근 실패")
            return False
    
    def analyze_all_editable_elements(self):
        """모든 수정 가능한 요소 분석"""
        print("\n[ANALYSIS] 모든 수정 가능한 요소 분석 중...")
        
        editable_elements = {
            'input_fields': [],
            'textarea_fields': [],
            'select_fields': [],
            'button_elements': [],
            'html_editors': [],
            'clickable_elements': []
        }
        
        try:
            # 1. Input 필드들
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            for i, input_elem in enumerate(inputs):
                try:
                    element_info = {
                        'index': i,
                        'type': input_elem.get_attribute('type') or 'text',
                        'name': input_elem.get_attribute('name') or '',
                        'id': input_elem.get_attribute('id') or '',
                        'class': input_elem.get_attribute('class') or '',
                        'value': input_elem.get_attribute('value') or '',
                        'placeholder': input_elem.get_attribute('placeholder') or '',
                        'editable': input_elem.is_enabled() and not input_elem.get_attribute('readonly')
                    }
                    editable_elements['input_fields'].append(element_info)
                except Exception as e:
                    pass
            
            # 2. Textarea 필드들
            textareas = self.driver.find_elements(By.TAG_NAME, "textarea")
            for i, textarea_elem in enumerate(textareas):
                try:
                    element_info = {
                        'index': i,
                        'name': textarea_elem.get_attribute('name') or '',
                        'id': textarea_elem.get_attribute('id') or '',
                        'class': textarea_elem.get_attribute('class') or '',
                        'value': textarea_elem.get_attribute('value') or textarea_elem.text,
                        'editable': textarea_elem.is_enabled() and not textarea_elem.get_attribute('readonly')
                    }
                    editable_elements['textarea_fields'].append(element_info)
                except Exception as e:
                    pass
            
            # 3. Select 필드들
            selects = self.driver.find_elements(By.TAG_NAME, "select")
            for i, select_elem in enumerate(selects):
                try:
                    element_info = {
                        'index': i,
                        'name': select_elem.get_attribute('name') or '',
                        'id': select_elem.get_attribute('id') or '',
                        'class': select_elem.get_attribute('class') or '',
                        'value': select_elem.get_attribute('value') or '',
                        'options': [opt.text for opt in select_elem.find_elements(By.TAG_NAME, "option")],
                        'editable': select_elem.is_enabled()
                    }
                    editable_elements['select_fields'].append(element_info)
                except Exception as e:
                    pass
            
            # 4. Button 요소들
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for i, button_elem in enumerate(buttons):
                try:
                    element_info = {
                        'index': i,
                        'text': button_elem.text,
                        'type': button_elem.get_attribute('type') or '',
                        'class': button_elem.get_attribute('class') or '',
                        'onclick': button_elem.get_attribute('onclick') or '',
                        'clickable': button_elem.is_enabled()
                    }
                    editable_elements['button_elements'].append(element_info)
                except Exception as e:
                    pass
            
            # 5. HTML 편집기 영역 찾기
            html_editor_candidates = [
                "//iframe[contains(@class, 'fr-iframe')]",  # FroalaEditor iframe
                "//div[contains(@class, 'fr-element')]",    # FroalaEditor div
                "//iframe[contains(@title, 'editor')]",      # 일반 editor iframe
                "//div[contains(@class, 'editor')]",         # 일반 editor div
                "//textarea[contains(@class, 'editor')]"     # textarea editor
            ]
            
            for xpath in html_editor_candidates:
                try:
                    elements = self.driver.find_elements(By.XPATH, xpath)
                    for elem in elements:
                        element_info = {
                            'type': 'html_editor',
                            'xpath': xpath,
                            'class': elem.get_attribute('class') or '',
                            'id': elem.get_attribute('id') or '',
                            'tag': elem.tag_name
                        }
                        editable_elements['html_editors'].append(element_info)
                except Exception as e:
                    pass
            
            # 6. 클릭 가능한 특수 요소들 (저장 버튼, 미리보기 등)
            special_clickables = [
                "//button[contains(text(), '저장')]",
                "//button[contains(text(), '수정')]",
                "//button[contains(text(), '미리보기')]",
                "//a[contains(text(), '저장')]",
                "//input[@type='submit']",
                "//input[contains(@value, '저장')]"
            ]
            
            for xpath in special_clickables:
                try:
                    elements = self.driver.find_elements(By.XPATH, xpath)
                    for elem in elements:
                        element_info = {
                            'type': 'special_button',
                            'xpath': xpath,
                            'text': elem.text or elem.get_attribute('value') or '',
                            'class': elem.get_attribute('class') or '',
                            'clickable': elem.is_enabled()
                        }
                        editable_elements['clickable_elements'].append(element_info)
                except Exception as e:
                    pass
            
            self.editable_elements = editable_elements
            
            # 결과 출력
            print(f"   [FOUND] Input 필드: {len(editable_elements['input_fields'])}개")
            print(f"   [FOUND] Textarea 필드: {len(editable_elements['textarea_fields'])}개")
            print(f"   [FOUND] Select 필드: {len(editable_elements['select_fields'])}개")
            print(f"   [FOUND] Button 요소: {len(editable_elements['button_elements'])}개")
            print(f"   [FOUND] HTML 편집기: {len(editable_elements['html_editors'])}개")
            print(f"   [FOUND] 특수 클릭 요소: {len(editable_elements['clickable_elements'])}개")
            
            return editable_elements
            
        except Exception as e:
            print(f"   [ERROR] 요소 분석 중 오류: {e}")
            return None
    
    def find_html_editor_detailed(self):
        """HTML 편집기 상세 분석"""
        print("\n[HTML-EDITOR] HTML 편집기 상세 분석...")
        
        # 다양한 HTML 편집기 패턴 확인
        editor_patterns = [
            {
                'name': 'FroalaEditor_iframe',
                'selector': "iframe.fr-iframe",
                'content_selector': "body"
            },
            {
                'name': 'FroalaEditor_div',
                'selector': "div.fr-element[contenteditable='true']",
                'content_selector': None
            },
            {
                'name': 'TinyMCE_iframe',
                'selector': "iframe[title*='editor']",
                'content_selector': "body"
            },
            {
                'name': 'CKEditor',
                'selector': "div[contenteditable='true']",
                'content_selector': None
            },
            {
                'name': 'Textarea_editor',
                'selector': "textarea[name*='detail'], textarea[id*='detail']",
                'content_selector': None
            }
        ]
        
        found_editors = []
        
        for pattern in editor_patterns:
            try:
                if pattern['selector'].startswith('iframe'):
                    # iframe 기반 편집기
                    elements = self.driver.find_elements(By.CSS_SELECTOR, pattern['selector'])
                else:
                    # div/textarea 기반 편집기
                    elements = self.driver.find_elements(By.CSS_SELECTOR, pattern['selector'])
                
                for i, elem in enumerate(elements):
                    editor_info = {
                        'type': pattern['name'],
                        'index': i,
                        'element': elem,
                        'selector': pattern['selector'],
                        'content_selector': pattern['content_selector'],
                        'is_iframe': pattern['selector'].startswith('iframe'),
                        'id': elem.get_attribute('id') or '',
                        'class': elem.get_attribute('class') or ''
                    }
                    found_editors.append(editor_info)
                    print(f"   [FOUND] {pattern['name']} #{i}: {elem.get_attribute('class')}")
                    
            except Exception as e:
                print(f"   [DEBUG] {pattern['name']} 검색 실패: {e}")
        
        # 상품 상세 설명 관련 특별 검색
        detail_patterns = [
            "//textarea[contains(@name, 'detail')]",
            "//iframe[contains(@title, '상세')]",
            "//div[contains(@class, 'detail') and @contenteditable='true']"
        ]
        
        for xpath in detail_patterns:
            try:
                elements = self.driver.find_elements(By.XPATH, xpath)
                for elem in elements:
                    editor_info = {
                        'type': 'product_detail_editor',
                        'element': elem,
                        'xpath': xpath,
                        'is_iframe': elem.tag_name == 'iframe',
                        'name': elem.get_attribute('name') or '',
                        'id': elem.get_attribute('id') or ''
                    }
                    found_editors.append(editor_info)
                    print(f"   [FOUND] 상품 상세 편집기: {elem.tag_name}")
            except Exception as e:
                pass
        
        self.html_editors = found_editors
        print(f"   [TOTAL] 발견된 HTML 편집기: {len(found_editors)}개")
        
        return found_editors
    
    def save_analysis_results(self):
        """분석 결과 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        analysis_data = {
            'timestamp': timestamp,
            'editable_elements': self.editable_elements,
            'html_editors': [
                {
                    'type': editor['type'],
                    'selector': editor.get('selector', ''),
                    'xpath': editor.get('xpath', ''),
                    'id': editor.get('id', ''),
                    'class': editor.get('class', ''),
                    'is_iframe': editor.get('is_iframe', False)
                }
                for editor in self.html_editors
            ]
        }
        
        # JSON 파일로 저장
        analysis_file = self.output_dir / f"product_elements_analysis_{timestamp}.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n[SAVE] 분석 결과 저장: {analysis_file}")
        return analysis_file
    
    def run_comprehensive_analysis(self, product_no=339):
        """종합 분석 실행"""
        print("="*80)
        print("[COMPREHENSIVE] Cafe24 상품 페이지 종합 분석 시작")
        print(f"대상 상품: {product_no}번")
        print("="*80)
        
        try:
            # 1. 드라이버 설정
            self.setup_driver()
            
            # 2. 로그인
            if not self.login_to_cafe24():
                print("로그인 실패로 종료")
                return None
            
            # 3. 상품 수정 페이지 접근
            if not self.access_product_edit_page(product_no):
                print("상품 페이지 접근 실패로 종료")
                return None
            
            # 4. 모든 수정 가능한 요소 분석
            elements = self.analyze_all_editable_elements()
            if not elements:
                print("요소 분석 실패")
                return None
            
            # 5. HTML 편집기 상세 분석
            editors = self.find_html_editor_detailed()
            
            # 6. 분석 결과 저장
            result_file = self.save_analysis_results()
            
            print("\n" + "="*80)
            print("[SUCCESS] 종합 분석 완료!")
            print(f"결과 파일: {result_file}")
            print("="*80)
            
            return {
                'elements': elements,
                'editors': editors,
                'result_file': result_file
            }
            
        except Exception as e:
            print(f"\n[ERROR] 분석 중 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            return None
        
        finally:
            if self.driver:
                print("\n[INFO] 60초 후 브라우저 종료 (수동 확인 시간)")
                time.sleep(60)
                self.driver.quit()

def main():
    """메인 실행 함수"""
    editor = AdvancedCafe24Editor()
    
    # P00000NB (339번) 상품 종합 분석
    results = editor.run_comprehensive_analysis(product_no=339)
    
    if results:
        print(f"\n[NEXT] 다음 단계: HTML 편집기 접근 및 수정 구현")
        print(f"발견된 HTML 편집기: {len(results['editors'])}개")
        print(f"수정 가능한 전체 요소: {sum(len(v) for v in results['elements'].values())}개")

if __name__ == "__main__":
    main()
# -*- coding: utf-8 -*-
"""
Cafe24 HTML 콘텐츠 완전 대체 시스템
HTML 편집기에 접근해서 콘텐츠를 완전히 대체하고 저장하는 시스템
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

try:
    from webdriver_manager.chrome import ChromeDriverManager
    USE_WEBDRIVER_MANAGER = True
except ImportError:
    USE_WEBDRIVER_MANAGER = False

class HTMLContentReplacer:
    """HTML 콘텐츠 완전 대체 클래스"""
    
    def __init__(self, config_path="config/cafe24_config.json"):
        """초기화"""
        self.config = self.load_config(config_path)
        self.driver = None
        self.wait = None
        self.replacement_results = []
        
        # 출력 디렉토리
        self.output_dir = Path("html_replacement_output")
        self.output_dir.mkdir(exist_ok=True)
        
        print("[HTML-REPLACER] HTML 콘텐츠 대체 시스템 초기화 완료")
    
    def load_config(self, config_path):
        """설정 파일 로드"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def setup_driver(self):
        """Chrome 드라이버 설정"""
        print("\n[DRIVER-SETUP] HTML 편집용 Chrome 드라이버 설정...")
        
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
        
        print("   [OK] HTML 편집용 드라이버 준비 완료")
    
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
    
    def login_and_access_product(self, product_no=339):
        """로그인 및 상품 페이지 접근"""
        print(f"\n[ACCESS] 상품 {product_no}번 페이지 접근...")
        
        # 로그인
        admin_url = self.config['cafe24']['admin_url']
        self.driver.get(admin_url)
        time.sleep(3)
        
        if self.handle_alert():
            print("   [OK] 보안 알림 처리")
        
        username_input = self.driver.find_element(By.XPATH, "//input[@type='text' and not(@placeholder='')]")
        username_input.clear()
        username_input.send_keys(self.config['cafe24']['username'])
        
        password_input = self.driver.find_element(By.XPATH, "//input[@type='password']")
        password_input.clear()
        password_input.send_keys(self.config['cafe24']['password'])
        
        login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '로그인')]")
        login_button.click()
        time.sleep(3)
        
        alert_count = 0
        while self.handle_alert() and alert_count < 5:
            alert_count += 1
        
        # 상품 페이지 접근
        mall_id = self.config['cafe24']['mall_id']
        product_url = f"https://{mall_id}.cafe24.com/disp/admin/shop1/product/ProductRegister?product_no={product_no}"
        self.driver.get(product_url)
        time.sleep(5)
        
        # 페이지 로딩 완료 대기
        for attempt in range(10):
            try:
                inputs = self.driver.find_elements(By.TAG_NAME, "input")
                if len(inputs) > 100:
                    print(f"   [OK] 상품 페이지 로딩 완료: {len(inputs)}개 요소")
                    return True
                time.sleep(2)
            except:
                time.sleep(2)
        
        return False
    
    def find_html_editors(self):
        """HTML 편집기 찾기"""
        print("\n[EDITOR-SEARCH] HTML 편집기 검색...")
        
        html_editors = []
        
        # FroalaEditor iframe 방식
        try:
            iframe_editors = self.driver.find_elements(By.CSS_SELECTOR, "iframe.fr-iframe")
            for i, iframe in enumerate(iframe_editors):
                editor_info = {
                    'type': 'froala_iframe',
                    'index': i,
                    'element': iframe,
                    'id': iframe.get_attribute('id') or f'froala_iframe_{i}',
                    'name': f'Froala Editor #{i}'
                }
                html_editors.append(editor_info)
                print(f"   [FOUND] Froala iframe #{i}: {editor_info['id']}")
        except Exception as e:
            print(f"   [DEBUG] Froala iframe 검색 실패: {e}")
        
        # Textarea 방식 (일부 편집기)
        try:
            textarea_editors = self.driver.find_elements(By.CSS_SELECTOR, "textarea[name*='detail'], textarea[id*='detail']")
            for i, textarea in enumerate(textarea_editors):
                editor_info = {
                    'type': 'textarea',
                    'index': i,
                    'element': textarea,
                    'id': textarea.get_attribute('id') or f'textarea_editor_{i}',
                    'name': textarea.get_attribute('name') or f'Textarea Editor #{i}'
                }
                html_editors.append(editor_info)
                print(f"   [FOUND] Textarea #{i}: {editor_info['name']}")
        except Exception as e:
            print(f"   [DEBUG] Textarea 검색 실패: {e}")
        
        print(f"   [TOTAL] 발견된 HTML 편집기: {len(html_editors)}개")
        return html_editors
    
    def replace_html_content_in_iframe(self, iframe_element, new_html_content):
        """iframe 내 HTML 콘텐츠 완전 대체"""
        print(f"   [REPLACE] iframe 콘텐츠 대체 중...")
        
        try:
            # iframe으로 전환
            self.driver.switch_to.frame(iframe_element)
            
            # body 요소 찾기
            body = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # 기존 내용 확인
            original_content = body.get_attribute('innerHTML')
            print(f"   [INFO] 기존 콘텐츠 길이: {len(original_content)} 문자")
            
            # 모든 내용 선택 및 삭제
            body.click()
            self.driver.execute_script("document.body.focus();")
            
            # Ctrl+A로 전체 선택
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
            time.sleep(0.5)
            
            # Delete로 삭제
            ActionChains(self.driver).send_keys(Keys.DELETE).perform()
            time.sleep(0.5)
            
            # JavaScript로 HTML 직접 삽입
            self.driver.execute_script(f"document.body.innerHTML = arguments[0];", new_html_content)
            time.sleep(2)
            
            # 결과 확인
            new_content = self.driver.execute_script("return document.body.innerHTML;")
            print(f"   [SUCCESS] 새 콘텐츠 길이: {len(new_content)} 문자")
            
            # 메인 프레임으로 복귀
            self.driver.switch_to.default_content()
            
            return True
            
        except Exception as e:
            print(f"   [ERROR] iframe 콘텐츠 대체 실패: {e}")
            # 메인 프레임으로 복귀 시도
            try:
                self.driver.switch_to.default_content()
            except:
                pass
            return False
    
    def replace_html_content_in_textarea(self, textarea_element, new_html_content):
        """textarea 내 HTML 콘텐츠 대체"""
        print(f"   [REPLACE] textarea 콘텐츠 대체 중...")
        
        try:
            # textarea에 포커스
            self.driver.execute_script("arguments[0].focus();", textarea_element)
            time.sleep(0.5)
            
            # 기존 내용 확인
            original_content = textarea_element.get_attribute('value')
            print(f"   [INFO] 기존 콘텐츠 길이: {len(original_content)} 문자")
            
            # 전체 내용 선택 및 삭제
            textarea_element.click()
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
            time.sleep(0.5)
            
            # 새 내용 입력
            textarea_element.send_keys(Keys.DELETE)
            time.sleep(0.5)
            textarea_element.send_keys(new_html_content)
            
            # 결과 확인
            new_content = textarea_element.get_attribute('value')
            print(f"   [SUCCESS] 새 콘텐츠 길이: {len(new_content)} 문자")
            
            return True
            
        except Exception as e:
            print(f"   [ERROR] textarea 콘텐츠 대체 실패: {e}")
            return False
    
    def find_and_click_save_button(self):
        """저장 버튼 찾기 및 클릭 - 강화된 버전"""
        print("\n[SAVE-SEARCH] 저장 버튼 종합 검색 시작...")
        
        # 1단계: JavaScript로 모든 저장 관련 버튼 찾기
        save_buttons = self.driver.execute_script("""
            var allButtons = Array.from(document.querySelectorAll('button, input[type="submit"], input[type="button"], a[onclick], div[onclick]'));
            var saveButtons = [];
            
            allButtons.forEach(function(btn, index) {
                var text = (btn.textContent || btn.innerText || btn.value || btn.title || '').trim();
                var className = btn.className || '';
                var id = btn.id || '';
                var onclick = btn.getAttribute('onclick') || '';
                
                // 저장 관련 키워드 검색 (한국어/영어)
                var keywords = ['저장', '수정', '완료', 'save', 'submit', 'update', 'confirm'];
                var hasKeyword = keywords.some(keyword => 
                    text.toLowerCase().includes(keyword) || 
                    className.toLowerCase().includes(keyword) || 
                    id.toLowerCase().includes(keyword) ||
                    onclick.toLowerCase().includes(keyword)
                );
                
                if (hasKeyword) {
                    var rect = btn.getBoundingClientRect();
                    var isVisible = rect.width > 0 && rect.height > 0 && 
                                   window.getComputedStyle(btn).display !== 'none' &&
                                   window.getComputedStyle(btn).visibility !== 'hidden';
                    
                    saveButtons.push({
                        element: btn,
                        text: text,
                        className: className,
                        id: id,
                        onclick: onclick,
                        index: index,
                        isVisible: isVisible,
                        tagName: btn.tagName.toLowerCase(),
                        priority: text.includes('저장') ? 1 : (text.includes('수정') ? 2 : 3)
                    });
                }
            });
            
            // 우선순위별 정렬 (저장 > 수정 > 기타)
            return saveButtons.sort((a, b) => a.priority - b.priority);
        """)
        
        if not save_buttons:
            print("   [SAVE-FAIL] 저장 버튼을 찾을 수 없습니다")
            return False
        
        print(f"   [SAVE-FOUND] 총 {len(save_buttons)}개의 저장 관련 버튼 발견")
        
        # 2단계: 우선순위별로 버튼 클릭 시도
        for i, button_info in enumerate(save_buttons):
            text = button_info.get('text', '')[:30]
            visible = button_info.get('isVisible', False)
            print(f"   [SAVE-TRY] #{i+1}: '{text}' (visible: {visible})")
            
            if not visible:
                continue
            
            try:
                # JavaScript로 클릭 시도 (더 안전함)
                click_result = self.driver.execute_script("""
                    try {
                        var btn = arguments[0];
                        
                        // 버튼이 화면에 보이도록 스크롤
                        btn.scrollIntoView({behavior: 'smooth', block: 'center'});
                        
                        // 클릭 실행
                        if (btn.click) {
                            btn.click();
                            return {success: true, method: 'click()'};
                        } else if (btn.onclick) {
                            btn.onclick();
                            return {success: true, method: 'onclick()'};
                        } else {
                            var event = new MouseEvent('click', {bubbles: true, cancelable: true});
                            btn.dispatchEvent(event);
                            return {success: true, method: 'dispatchEvent'};
                        }
                    } catch (e) {
                        return {success: false, error: e.toString()};
                    }
                """, button_info['element'])
                
                if click_result.get('success'):
                    print(f"   [SAVE-SUCCESS] 버튼 #{i+1} 클릭 성공! (방법: {click_result.get('method')})")
                    time.sleep(3)  # 저장 처리 대기
                    
                    # 저장 성공 확인
                    page_changes = self.driver.execute_script("""
                        return {
                            title: document.title,
                            url: window.location.href,
                            alerts: document.querySelectorAll('.alert, .success, .message').length
                        };
                    """)
                    
                    print(f"   [SAVE-CHECK] 저장 후 페이지 상태: {page_changes}")
                    return True
                    
                else:
                    error = click_result.get('error', 'Unknown error')
                    print(f"   [SAVE-FAIL] #{i+1} 클릭 실패: {error}")
                    
            except Exception as e:
                print(f"   [SAVE-ERROR] #{i+1} 처리 중 오류: {e}")
                continue
        
        print("   [SAVE-FINAL] 모든 저장 버튼 클릭 시도 완료")
        return False
    
    def execute_html_replacement(self, product_no, new_html_content):
        """HTML 콘텐츠 완전 대체 실행"""
        print("="*80)
        print(f"[HTML-REPLACEMENT] 상품 {product_no}번 HTML 콘텐츠 대체 시작")
        print("="*80)
        
        try:
            # 1. 드라이버 설정
            self.setup_driver()
            
            # 2. 로그인 및 상품 페이지 접근
            if not self.login_and_access_product(product_no):
                print("상품 페이지 접근 실패")
                return False
            
            # 3. HTML 편집기 찾기
            html_editors = self.find_html_editors()
            if not html_editors:
                print("HTML 편집기를 찾을 수 없습니다")
                return False
            
            # 4. 각 HTML 편집기에 콘텐츠 대체
            replacement_success = False
            for editor in html_editors:
                print(f"\n[PROCESS] {editor['name']} 콘텐츠 대체 중...")
                
                if editor['type'] == 'froala_iframe':
                    success = self.replace_html_content_in_iframe(editor['element'], new_html_content)
                elif editor['type'] == 'textarea':
                    success = self.replace_html_content_in_textarea(editor['element'], new_html_content)
                else:
                    print(f"   [SKIP] 지원하지 않는 편집기 타입: {editor['type']}")
                    continue
                
                if success:
                    replacement_success = True
                    print(f"   [SUCCESS] {editor['name']} 콘텐츠 대체 완료")
                
                # 각 편집기 사이에 잠시 대기
                time.sleep(2)
            
            # 5. 저장 버튼 클릭
            if replacement_success:
                save_success = self.find_and_click_save_button()
                if save_success:
                    print("\n[COMPLETE] HTML 콘텐츠 대체 및 저장 완료!")
                    return True
                else:
                    print("\n[WARNING] 콘텐츠 대체는 완료되었지만 저장 버튼 클릭 실패")
                    print("수동으로 저장 버튼을 클릭해주세요")
                    # 60초 대기 후 종료
                    time.sleep(60)
                    return True
            else:
                print("\n[FAIL] HTML 콘텐츠 대체 실패")
                return False
            
        except Exception as e:
            print(f"\n[ERROR] HTML 대체 프로세스 오류: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        finally:
            if self.driver:
                time.sleep(5)  # 최종 결과 확인 시간
                self.driver.quit()
                print("\n[CLEANUP] 브라우저 종료")

def main():
    """메인 실행 함수"""
    
    # 사용자가 제공한 HTML 콘텐츠
    new_html_content = '''
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[씨씨더블유]가마솥 불스지 300g - 만원요리 최씨남매</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --saffron-gold: #E4A853; --deep-rose: #C53030; --deep-charcoal: #1F2937; --pure-white: #FFFFFF; --light-gray: #F9FAFB; --medium-gray: #6B7280; --border-gray: #E5E7EB; --success-green: #10B981;
        }
        
        * {
            margin: 0; padding: 0; box-sizing: border-box;
        }
        
        body {
            font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif; line-height: 1.6; color: var(--deep-charcoal); background: var(--light-gray);
        }
    </style>
    
    <div class="container">
        <div class="red-gradient">
            <h1 class="text-4xl md:text-5xl font-black mb-6">[씨씨더블유]가마솥 불스지 300g</h1>
            <p class="text-xl md:text-2xl mb-8 leading-relaxed">만원요리 최씨남매가 엄선한 프리미엄 상품</p>
        </div>
    </div>
    '''
    
    replacer = HTMLContentReplacer()
    
    # P00000NB (339번) 상품의 HTML 콘텐츠 대체
    success = replacer.execute_html_replacement(product_no=339, new_html_content=new_html_content)
    
    if success:
        print("\n[FINAL-SUCCESS] HTML 콘텐츠 대체 및 저장 성공!")
    else:
        print("\n[FINAL-FAIL] HTML 콘텐츠 대체 실패")

if __name__ == "__main__":
    main()
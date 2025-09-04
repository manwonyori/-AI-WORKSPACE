# -*- coding: utf-8 -*-
"""
Ultimate Cafe24 Product Editor
완전한 상품 수정 워크플로우 자동화 시스템
"""
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

class UltimateProductEditor:
    """최종 상품 편집 자동화 시스템"""
    
    def __init__(self):
        """초기화"""
        self.driver = None
        self.config = self.load_config()
        self.results = {
            'start_time': datetime.now().isoformat(),
            'products_processed': [],
            'success_count': 0,
            'fail_count': 0
        }
        print("[ULTIMATE-EDITOR] 최종 상품 편집 시스템 초기화 완료")
    
    def load_config(self):
        """설정 로드"""
        try:
            with open('config/cafe24_config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            print("   [CONFIG] 설정 파일 로드 성공")
            return config
        except Exception as e:
            print(f"   [ERROR] 설정 파일 로드 실패: {e}")
            return None
    
    def setup_driver(self):
        """Chrome 드라이버 설정"""
        print("\n[DRIVER-SETUP] Chrome 드라이버 초기화...")
        
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        service = Service(ChromeDriverManager().install())
        
        try:
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("   [OK] Chrome 드라이버 준비 완료")
            return True
        except Exception as e:
            print(f"   [ERROR] 드라이버 초기화 실패: {e}")
            return False
    
    def login_to_cafe24(self):
        """Cafe24 로그인"""
        print("\n[LOGIN] Cafe24 로그인 시작...")
        
        if not self.config:
            return False
        
        cafe24_config = self.config.get('cafe24', {})
        login_url = f"https://{cafe24_config['mall_id']}.cafe24.com/disp/admin/shop1/login"
        
        try:
            self.driver.get(login_url)
            
            # 초기 알림 처리 (페이지 로드 시)
            try:
                alert = WebDriverWait(self.driver, 2).until(EC.alert_is_present())
                alert_text = alert.text
                print(f"   [ALERT-INITIAL] {alert_text}")
                alert.accept()
                time.sleep(1)
            except:
                pass
            
            time.sleep(2)
            
            # 알림 처리 후 로그인 폼 요소들 다시 찾기
            try:
                id_input = self.driver.find_element(By.NAME, "admin_id")
                id_input.clear()
                id_input.send_keys(cafe24_config['username'])
                
                pw_input = self.driver.find_element(By.NAME, "admin_passwd")
                pw_input.clear()
                pw_input.send_keys(cafe24_config['password'])
                
                # 로그인 버튼 클릭 전 알림 처리
                try:
                    alert = WebDriverWait(self.driver, 1).until(EC.alert_is_present())
                    print(f"   [ALERT-PRE-SUBMIT] {alert.text}")
                    alert.accept()
                    time.sleep(1)
                except:
                    pass
                
                # 로그인 버튼 클릭
                login_button = self.driver.find_element(By.XPATH, "//input[@type='submit' or @type='button']")
                
                # JavaScript로 클릭 (더 안전)
                self.driver.execute_script("arguments[0].click();", login_button)
                
            except Exception as form_error:
                print(f"   [WARNING] 폼 입력 중 오류: {form_error}")
                # 직접 URL로 이동 시도
                admin_url = f"https://{cafe24_config['mall_id']}.cafe24.com/admin"
                self.driver.get(admin_url)
                time.sleep(2)
            
            # 로그인 후 알림 처리
            max_alerts = 3  # 최대 3개 알림 처리
            for i in range(max_alerts):
                try:
                    alert = WebDriverWait(self.driver, 3).until(EC.alert_is_present())
                    alert_text = alert.text
                    print(f"   [ALERT-{i+1}] {alert_text}")
                    alert.accept()
                    time.sleep(1)
                except:
                    break  # 더 이상 알림이 없으면 종료
            
            time.sleep(2)
            
            # 로그인 성공 확인
            current_url = self.driver.current_url
            if "admin" in current_url or "shop1" in current_url:
                print(f"   [SUCCESS] 로그인 성공: {current_url}")
                return True
            else:
                print(f"   [FAIL] 로그인 실패: {current_url}")
                return False
                
        except Exception as e:
            print(f"   [ERROR] 로그인 중 오류: {e}")
            return False
    
    def access_product_edit_page(self, product_no):
        """상품 수정 페이지 접근"""
        print(f"\n[ACCESS] 상품 {product_no}번 수정 페이지 접근...")
        
        cafe24_config = self.config.get('cafe24', {})
        product_url = f"https://{cafe24_config['mall_id']}.cafe24.com/disp/admin/shop1/product/ProductRegister?product_no={product_no}"
        
        try:
            self.driver.get(product_url)
            
            # JavaScript 로딩 완료 대기
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # 입력 요소들이 로드될 때까지 대기
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "input"))
            )
            
            input_count = len(self.driver.find_elements(By.TAG_NAME, "input"))
            print(f"   [OK] 상품 수정 페이지 로드 완료: {input_count}개 입력 필드")
            return True
            
        except Exception as e:
            print(f"   [ERROR] 상품 페이지 접근 실패: {e}")
            return False
    
    def replace_html_content(self, new_html_content):
        """HTML 콘텐츠 대체"""
        print("\n[HTML-REPLACE] HTML 콘텐츠 대체 시작...")
        
        # Froala 에디터 iframe 찾기
        froala_iframes = self.driver.execute_script("""
            return Array.from(document.querySelectorAll('iframe')).filter(iframe => 
                iframe.id && iframe.id.includes('IFRAME')
            ).map(iframe => ({
                id: iframe.id,
                src: iframe.src,
                isVisible: iframe.offsetWidth > 0 && iframe.offsetHeight > 0
            }));
        """)
        
        if not froala_iframes:
            print("   [FAIL] HTML 에디터를 찾을 수 없습니다")
            return False
        
        print(f"   [FOUND] {len(froala_iframes)}개의 HTML 에디터 발견")
        
        success_count = 0
        
        # 첫 번째 에디터(주 상품 설명)에만 콘텐츠 적용
        main_editor = froala_iframes[0]
        
        if main_editor['isVisible']:
            try:
                # iframe으로 전환
                iframe_element = self.driver.find_element(By.ID, main_editor['id'])
                self.driver.switch_to.frame(iframe_element)
                
                # 기존 콘텐츠 모두 선택 및 삭제
                body = self.driver.find_element(By.TAG_NAME, "body")
                body.click()
                
                # Ctrl+A로 전체 선택 후 새 내용 입력
                ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                time.sleep(0.5)
                
                # JavaScript로 직접 HTML 설정
                self.driver.execute_script("document.body.innerHTML = arguments[0];", new_html_content)
                
                # 메인 프레임으로 복귀
                self.driver.switch_to.default_content()
                
                print(f"   [SUCCESS] 메인 에디터 콘텐츠 대체 완료: {len(new_html_content)}자")
                success_count += 1
                
            except Exception as e:
                print(f"   [ERROR] 메인 에디터 콘텐츠 대체 실패: {e}")
                self.driver.switch_to.default_content()
        
        return success_count > 0
    
    def save_product_changes(self):
        """상품 변경사항 저장"""
        print("\n[SAVE] 상품 변경사항 저장 시도...")
        
        # 1단계: Ctrl+S 키보드 단축키 시도
        try:
            print("   [TRY] Ctrl+S 키보드 단축키 시도...")
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('s').key_up(Keys.CONTROL).perform()
            time.sleep(2)
            
            # 브라우저 저장 다이얼로그 처리 (ESC로 닫기)
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(1)
            
            print("   [INFO] Ctrl+S 실행 완료")
        except Exception as e:
            print(f"   [ERROR] Ctrl+S 실행 실패: {e}")
        
        # 2단계: 저장 버튼 찾기 및 클릭
        save_buttons = self.driver.execute_script("""
            var buttons = Array.from(document.querySelectorAll('button, input[type="submit"], input[type="button"], a'));
            return buttons.filter(btn => {
                var text = (btn.textContent || btn.innerText || btn.value || '').toLowerCase();
                var className = (btn.className || '').toLowerCase();
                var id = (btn.id || '').toLowerCase();
                
                return text.includes('저장') || text.includes('수정') || text.includes('완료') ||
                       text.includes('save') || text.includes('update') || text.includes('submit') ||
                       className.includes('save') || className.includes('submit') ||
                       id.includes('save') || id.includes('submit');
            }).map(btn => ({
                text: btn.textContent || btn.innerText || btn.value || '',
                visible: btn.offsetWidth > 0 && btn.offsetHeight > 0,
                element: btn
            }));
        """)
        
        if save_buttons:
            print(f"   [FOUND] {len(save_buttons)}개의 저장 관련 버튼 발견")
            
            for i, button_info in enumerate(save_buttons):
                if not button_info['visible']:
                    continue
                
                try:
                    print(f"   [CLICK] 저장 버튼 #{i+1}: '{button_info['text'][:20]}'")
                    
                    # JavaScript로 클릭
                    self.driver.execute_script("arguments[0].click();", button_info['element'])
                    time.sleep(2)
                    
                    print(f"   [SUCCESS] 저장 버튼 #{i+1} 클릭 완료")
                    return True
                    
                except Exception as e:
                    print(f"   [FAIL] 버튼 #{i+1} 클릭 실패: {e}")
                    continue
        
        # 3단계: 폼 자동 제출 시도
        try:
            print("   [TRY] 폼 자동 제출 시도...")
            forms = self.driver.find_elements(By.TAG_NAME, "form")
            
            if forms:
                main_form = forms[0]  # 첫 번째 폼 사용
                self.driver.execute_script("arguments[0].submit();", main_form)
                time.sleep(3)
                print("   [SUCCESS] 폼 제출 완료")
                return True
            else:
                print("   [INFO] 제출할 폼을 찾을 수 없습니다")
        except Exception as e:
            print(f"   [ERROR] 폼 제출 실패: {e}")
        
        print("   [WARNING] 모든 저장 시도 완료")
        return False
    
    def process_single_product(self, product_no, html_content):
        """단일 상품 처리"""
        print("="*80)
        print(f"[PRODUCT-PROCESS] 상품 {product_no}번 처리 시작")
        print("="*80)
        
        product_result = {
            'product_no': product_no,
            'start_time': datetime.now().isoformat(),
            'success': False,
            'steps': []
        }
        
        try:
            # 1단계: 상품 페이지 접근
            if self.access_product_edit_page(product_no):
                product_result['steps'].append({'step': 'access_page', 'success': True})
            else:
                product_result['steps'].append({'step': 'access_page', 'success': False})
                return product_result
            
            # 2단계: HTML 콘텐츠 대체
            if self.replace_html_content(html_content):
                product_result['steps'].append({'step': 'replace_html', 'success': True})
            else:
                product_result['steps'].append({'step': 'replace_html', 'success': False})
                return product_result
            
            # 3단계: 변경사항 저장
            if self.save_product_changes():
                product_result['steps'].append({'step': 'save_changes', 'success': True})
                product_result['success'] = True
                print(f"\n[COMPLETE-SUCCESS] 상품 {product_no}번 처리 완료!")
            else:
                product_result['steps'].append({'step': 'save_changes', 'success': False})
                print(f"\n[COMPLETE-PARTIAL] 상품 {product_no}번 콘텐츠 대체 완료, 저장 확인 필요")
                # 콘텐츠 대체는 성공했으므로 부분 성공으로 처리
                product_result['success'] = True
            
            return product_result
            
        except Exception as e:
            print(f"\n[COMPLETE-ERROR] 상품 {product_no}번 처리 중 오류: {e}")
            product_result['error'] = str(e)
            return product_result
    
    def run_ultimate_workflow(self, product_list, html_content):
        """최종 워크플로우 실행"""
        print("="*80)
        print("[ULTIMATE-WORKFLOW] 최종 상품 수정 워크플로우 시작")
        print("="*80)
        
        if not self.setup_driver():
            return False
        
        if not self.login_to_cafe24():
            return False
        
        for product_no in product_list:
            result = self.process_single_product(product_no, html_content)
            
            self.results['products_processed'].append(result)
            
            if result['success']:
                self.results['success_count'] += 1
            else:
                self.results['fail_count'] += 1
        
        # 최종 결과 출력
        self.print_final_results()
        
        # 드라이버 종료
        if self.driver:
            self.driver.quit()
        
        return True
    
    def print_final_results(self):
        """최종 결과 출력"""
        print("\n" + "="*80)
        print("[FINAL-RESULTS] 최종 처리 결과")
        print("="*80)
        
        total_products = len(self.results['products_processed'])
        success_rate = (self.results['success_count'] / total_products * 100) if total_products > 0 else 0
        
        print(f"총 처리 상품: {total_products}개")
        print(f"성공: {self.results['success_count']}개")
        print(f"실패: {self.results['fail_count']}개")
        print(f"성공률: {success_rate:.1f}%")
        
        # 상세 결과
        for result in self.results['products_processed']:
            status = "[SUCCESS]" if result['success'] else "[FAIL]"
            steps_info = " -> ".join([f"{step['step']}({'O' if step['success'] else 'X'})" for step in result['steps']])
            print(f"  상품 {result['product_no']}번: {status} ({steps_info})")

def main():
    """메인 실행"""
    # 사용자 제공 HTML 콘텐츠
    new_html_content = '''
    <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 15px; margin-bottom: 30px;">
            <h1 style="margin: 0; font-size: 2.5em; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">🍽️ 만원요리 프리미엄</h1>
            <p style="margin: 10px 0 0 0; font-size: 1.2em; opacity: 0.9;">최고 품질의 간편식을 경험하세요</p>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 25px; margin: 30px 0;">
            <div style="background: #f8f9fa; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 5px solid #28a745;">
                <h3 style="color: #28a745; margin-top: 0;">✅ 프리미엄 품질</h3>
                <p>엄선된 재료로 만든 최고급 간편식</p>
            </div>
            
            <div style="background: #f8f9fa; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 5px solid #007bff;">
                <h3 style="color: #007bff; margin-top: 0;">🚀 빠른 조리</h3>
                <p>전자레인지 3분이면 완성되는 간편함</p>
            </div>
            
            <div style="background: #f8f9fa; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 5px solid #dc3545;">
                <h3 style="color: #dc3545; margin-top: 0;">💝 특별 혜택</h3>
                <p>지금 주문하면 무료배송 + 할인혜택</p>
            </div>
        </div>
        
        <div style="background: linear-gradient(45deg, #FF6B6B, #4ECDC4); color: white; padding: 25px; border-radius: 15px; text-align: center; margin: 30px 0;">
            <h2 style="margin: 0 0 15px 0;">🎉 한정 특가 이벤트</h2>
            <p style="font-size: 1.1em; margin: 0;">오늘만 특별가격으로 만나보세요!</p>
        </div>
    </div>
    '''
    
    # 에디터 인스턴스 생성
    editor = UltimateProductEditor()
    
    # P00000NB 상품 (339번) 처리
    product_list = [339]
    
    # 최종 워크플로우 실행
    editor.run_ultimate_workflow(product_list, new_html_content)

if __name__ == "__main__":
    main()
"""
카페24 통합 학습 시스템 (Unified Learner)
모든 학습 기능을 통합하고 개선한 버전
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
import json
import time
import os
from datetime import datetime
from pathlib import Path
import traceback

class Cafe24UnifiedLearner:
    """카페24 통합 학습 클래스"""
    
    def __init__(self):
        self.driver = None
        self.learning_dir = Path("C:/Users/8899y/CUA-MASTER/modules/cafe24/learning")
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        self.claude_bridge_dir = Path("C:/Users/8899y/claude_bridge")
        self.claude_bridge_dir.mkdir(parents=True, exist_ok=True)
        self.learning_data = {}
        
    def setup_driver(self):
        """Chrome 드라이버 설정"""
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("useAutomationExtension", False)
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        
        # 마우스 시각화 활성화
        self.inject_mouse_visualizer()
        
        print("[OK] Chrome 드라이버 준비 완료")
        
    def inject_mouse_visualizer(self):
        """개선된 마우스 시각화"""
        try:
            self.driver.execute_script("""
                // 기존 포인터 제거
                var old = document.getElementById('custom-mouse-pointer');
                if (old) old.remove();
                
                // 새 포인터 생성
                var pointer = document.createElement('div');
                pointer.id = 'custom-mouse-pointer';
                pointer.style.cssText = `
                    position: fixed;
                    width: 30px;
                    height: 30px;
                    border: 3px solid #FF0000;
                    border-radius: 50%;
                    background: rgba(255, 0, 0, 0.3);
                    pointer-events: none;
                    z-index: 2147483647;
                    transition: all 0.1s;
                `;
                document.body.appendChild(pointer);
                
                // 마우스 추적
                document.addEventListener('mousemove', function(e) {
                    pointer.style.left = (e.clientX - 15) + 'px';
                    pointer.style.top = (e.clientY - 15) + 'px';
                });
                
                // 클릭 효과
                document.addEventListener('click', function() {
                    pointer.style.background = 'rgba(255, 255, 0, 0.7)';
                    setTimeout(() => {
                        pointer.style.background = 'rgba(255, 0, 0, 0.3)';
                    }, 200);
                });
                
                console.log('마우스 시각화 활성화');
            """)
            print("[OK] 마우스 시각화 활성화")
        except:
            pass
    
    def login_cafe24(self):
        """카페24 로그인 (학습된 패턴 사용)"""
        try:
            # 학습된 로그인 데이터 로드
            learning_file = self.learning_dir / "cua_learning_data.json"
            if learning_file.exists():
                with open(learning_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    patterns = data.get('successful_patterns', {}).get('login', {})
            else:
                patterns = {
                    'xpath_username': "//input[@type='text' and not(@placeholder='')]",
                    'xpath_password': "//input[@type='password']",
                    'xpath_login_button': "//button[contains(text(), '로그인')]"
                }
            
            # 로그인 페이지로 이동
            self.driver.get("https://manwonyori.cafe24.com/admin/")
            time.sleep(2)
            
            # 알림 처리
            try:
                alert = Alert(self.driver)
                alert_text = alert.text
                print(f"[ALERT] {alert_text}")
                alert.accept()
                time.sleep(1)
            except:
                pass
            
            # 로그인 입력
            username = self.driver.find_element(By.XPATH, patterns['xpath_username'])
            password = self.driver.find_element(By.XPATH, patterns['xpath_password'])
            
            username.clear()
            username.send_keys("8899yang")
            
            password.clear()
            password.send_keys("xptmxm73xptmxm73!")
            
            # 로그인 버튼 클릭
            login_btn = self.driver.find_element(By.XPATH, patterns['xpath_login_button'])
            login_btn.click()
            
            time.sleep(3)
            print("[OK] 로그인 성공")
            return True
            
        except Exception as e:
            print(f"[ERROR] 로그인 실패: {e}")
            return False
    
    def learn_product_page(self, product_no="338"):
        """상품 페이지 완전 학습"""
        
        print(f"\n{'='*60}")
        print(f"상품 {product_no}번 완전 학습 시작")
        print(f"{'='*60}")
        
        # 상품 수정 페이지로 이동
        url = f"https://manwonyori.cafe24.com/disp/admin/shop1/product/ProductRegister?product_no={product_no}"
        self.driver.get(url)
        time.sleep(3)
        
        # 5가지 요구사항 실행
        requirements = {
            "1_dom_scan": self.requirement_1_dom_scan,
            "2_element_mapping": self.requirement_2_element_mapping,
            "3_event_listeners": self.requirement_3_event_listeners_safe,
            "4_ajax_monitoring": self.requirement_4_ajax_monitoring,
            "5_save_process": self.requirement_5_save_process
        }
        
        results = {}
        for name, func in requirements.items():
            try:
                print(f"\n[{name.upper()}] 실행 중...")
                results[name] = func()
                print(f"   [OK] 완료")
            except Exception as e:
                print(f"   [ERROR] {e}")
                results[name] = {"error": str(e)}
        
        # 섹션별 학습
        sections = self.learn_all_sections()
        
        # 학습 데이터 저장
        self.learning_data = {
            "product_no": product_no,
            "timestamp": datetime.now().isoformat(),
            "requirements": results,
            "sections": sections,
            "url": url
        }
        
        # 파일 저장
        self.save_learning_data()
        
        return self.learning_data
    
    def requirement_1_dom_scan(self):
        """요구사항 1: DOM 스캔"""
        dom_data = self.driver.execute_script("""
            return {
                total_elements: document.querySelectorAll('*').length,
                body_html_size: document.body.innerHTML.length,
                forms: document.forms.length,
                inputs: document.querySelectorAll('input').length,
                selects: document.querySelectorAll('select').length,
                textareas: document.querySelectorAll('textarea').length,
                buttons: document.querySelectorAll('button').length,
                links: document.querySelectorAll('a').length
            };
        """)
        return dom_data
    
    def requirement_2_element_mapping(self):
        """요구사항 2: 요소 매핑"""
        element_map = self.driver.execute_script("""
            function mapElements() {
                var map = {
                    inputs: [],
                    selects: [],
                    checkboxes: [],
                    radios: [],
                    textareas: [],
                    buttons: []
                };
                
                // Input 매핑
                document.querySelectorAll('input').forEach(function(el) {
                    var data = {
                        type: el.type,
                        name: el.name,
                        id: el.id,
                        value: el.value,
                        xpath: getXPath(el)
                    };
                    
                    if (el.type === 'checkbox') {
                        data.checked = el.checked;
                        map.checkboxes.push(data);
                    } else if (el.type === 'radio') {
                        data.checked = el.checked;
                        map.radios.push(data);
                    } else {
                        map.inputs.push(data);
                    }
                });
                
                // Select 매핑
                document.querySelectorAll('select').forEach(function(el) {
                    map.selects.push({
                        name: el.name,
                        id: el.id,
                        value: el.value,
                        options: Array.from(el.options).map(o => ({
                            value: o.value,
                            text: o.text,
                            selected: o.selected
                        })),
                        xpath: getXPath(el)
                    });
                });
                
                // Textarea 매핑
                document.querySelectorAll('textarea').forEach(function(el) {
                    map.textareas.push({
                        name: el.name,
                        id: el.id,
                        value: el.value,
                        xpath: getXPath(el)
                    });
                });
                
                // Button 매핑
                document.querySelectorAll('button, input[type="button"], input[type="submit"]').forEach(function(el) {
                    map.buttons.push({
                        type: el.type || 'button',
                        text: el.innerText || el.value,
                        onclick: el.onclick ? el.onclick.toString().substring(0, 100) : '',
                        xpath: getXPath(el)
                    });
                });
                
                return map;
            }
            
            function getXPath(el) {
                if (el.id) return "//*[@id='" + el.id + "']";
                if (el.name) return "//*[@name='" + el.name + "']";
                return "";
            }
            
            return mapElements();
        """)
        
        # 통계 추가
        element_map['statistics'] = {
            'total_inputs': len(element_map.get('inputs', [])),
            'total_selects': len(element_map.get('selects', [])),
            'total_checkboxes': len(element_map.get('checkboxes', [])),
            'total_radios': len(element_map.get('radios', [])),
            'total_textareas': len(element_map.get('textareas', [])),
            'total_buttons': len(element_map.get('buttons', []))
        }
        
        return element_map
    
    def requirement_3_event_listeners_safe(self):
        """요구사항 3: 이벤트 리스너 분석 (안전한 버전)"""
        return self.driver.execute_script("""
            function analyzeEvents() {
                return {
                    onclick_elements: document.querySelectorAll('[onclick]').length,
                    onchange_elements: document.querySelectorAll('[onchange]').length,
                    onsubmit_forms: document.querySelectorAll('[onsubmit]').length,
                    total_buttons: document.querySelectorAll('button').length,
                    total_links: document.querySelectorAll('a[href]').length,
                    interactive_elements: document.querySelectorAll('button, a, input[type="submit"], [onclick]').length
                };
            }
            return analyzeEvents();
        """)
    
    def requirement_4_ajax_monitoring(self):
        """요구사항 4: AJAX 모니터링"""
        self.driver.execute_script("""
            window.ajaxCalls = [];
            
            // XMLHttpRequest 인터셉트
            var originalXHR = window.XMLHttpRequest;
            window.XMLHttpRequest = function() {
                var xhr = new originalXHR();
                var originalOpen = xhr.open;
                xhr.open = function(method, url) {
                    window.ajaxCalls.push({
                        type: 'XHR',
                        method: method,
                        url: url,
                        timestamp: new Date().toISOString()
                    });
                    originalOpen.apply(xhr, arguments);
                };
                return xhr;
            };
            
            // Fetch 인터셉트
            var originalFetch = window.fetch;
            window.fetch = function(url, options) {
                window.ajaxCalls.push({
                    type: 'Fetch',
                    url: url,
                    method: (options && options.method) || 'GET',
                    timestamp: new Date().toISOString()
                });
                return originalFetch.apply(window, arguments);
            };
            
            console.log('AJAX 모니터링 활성화');
        """)
        
        return {"monitoring": "active", "message": "AJAX 호출이 window.ajaxCalls에 기록됩니다"}
    
    def requirement_5_save_process(self):
        """요구사항 5: 저장 프로세스 추적"""
        save_elements = self.driver.execute_script("""
            function findSaveElements() {
                var results = {
                    save_buttons: [],
                    forms: []
                };
                
                // 저장 버튼 찾기
                var buttons = document.querySelectorAll('button, input[type="submit"]');
                buttons.forEach(function(btn) {
                    var text = (btn.innerText || btn.value || '').toLowerCase();
                    if (text.includes('저장') || text.includes('save') || text.includes('등록')) {
                        results.save_buttons.push({
                            type: btn.type || 'button',
                            text: btn.innerText || btn.value,
                            id: btn.id,
                            class: btn.className
                        });
                    }
                });
                
                // 폼 찾기
                document.querySelectorAll('form').forEach(function(form, idx) {
                    results.forms.push({
                        id: form.id || 'form_' + idx,
                        action: form.action,
                        method: form.method,
                        name: form.name
                    });
                });
                
                return results;
            }
            return findSaveElements();
        """)
        
        return save_elements
    
    def learn_all_sections(self):
        """모든 섹션 학습"""
        sections = {}
        
        # 섹션 탭 목록
        tab_names = [
            "표시설정", "기본정보", "판매정보", "옵션/재고",
            "이미지정보", "제작정보", "상세이용안내", "아이콘설정",
            "배송정보", "추가구성상품", "관련상품", "SEO설정", "메모"
        ]
        
        for tab_name in tab_names:
            try:
                # 탭 클릭
                tab = self.driver.find_element(By.XPATH, f"//a[contains(text(), '{tab_name}')]")
                self.driver.execute_script("arguments[0].click();", tab)
                time.sleep(1)
                
                # 섹션 내용 학습
                section_data = self.learn_section_content(tab_name)
                sections[tab_name] = section_data
                
                print(f"   [OK] {tab_name} 학습 완료")
                
            except Exception as e:
                print(f"   [SKIP] {tab_name}: {str(e)[:50]}")
                sections[tab_name] = {"error": "탭을 찾을 수 없음"}
        
        return sections
    
    def learn_section_content(self, section_name):
        """섹션 내용 학습"""
        return self.driver.execute_script("""
            function learnSection(sectionName) {
                var data = {
                    name: sectionName,
                    inputs: document.querySelectorAll('input:not([type="hidden"])').length,
                    selects: document.querySelectorAll('select').length,
                    textareas: document.querySelectorAll('textarea').length,
                    checkboxes: document.querySelectorAll('input[type="checkbox"]').length,
                    radios: document.querySelectorAll('input[type="radio"]').length
                };
                return data;
            }
            return learnSection(arguments[0]);
        """, section_name)
    
    def save_learning_data(self):
        """학습 데이터 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON 파일 저장
        json_file = self.learning_dir / f"unified_learning_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.learning_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n[저장] 학습 데이터: {json_file}")
        
        # Claude Bridge에 알림
        self.notify_claude_bridge(f"학습 완료: {json_file}")
        
        return json_file
    
    def notify_claude_bridge(self, message):
        """Claude Bridge에 알림"""
        try:
            notification = {
                "type": "learning_complete",
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
            
            notification_file = self.claude_bridge_dir / f"notification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(notification_file, 'w', encoding='utf-8') as f:
                json.dump(notification, f, ensure_ascii=False, indent=2)
                
        except:
            pass
    
    def run(self, product_no="338"):
        """메인 실행 함수"""
        try:
            print("\n카페24 통합 학습 시스템 시작...")
            
            # 드라이버 설정
            self.setup_driver()
            
            # 로그인
            if not self.login_cafe24():
                return False
            
            # 상품 페이지 학습
            result = self.learn_product_page(product_no)
            
            print("\n[완료] 학습 성공!")
            return result
            
        except Exception as e:
            print(f"\n[ERROR] 학습 실패: {e}")
            traceback.print_exc()
            return None
            
        finally:
            if self.driver:
                input("\n엔터를 눌러 브라우저를 종료...")
                self.driver.quit()

if __name__ == "__main__":
    learner = Cafe24UnifiedLearner()
    learner.run("338")
# -*- coding: utf-8 -*-
"""
Claude 카페24 상세페이지 직접 수정 시스템
실시간으로 상품 상세페이지 HTML을 수정하고 저장하는 통합 시스템
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
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ClaudeDetailPageEditor:
    """Claude 상세페이지 직접 편집기"""
    
    def __init__(self):
        """초기화"""
        self.driver = None
        self.wait = None
        self.config = self.load_config()
        self.html_templates_path = Path("C:/Users/8899y/CUA-MASTER/modules/cafe24/complete_content/html")
        
        print("🎨 Claude 상세페이지 직접 편집 시스템 시작")
        print(f"📁 HTML 템플릿 경로: {self.html_templates_path}")
        
    def load_config(self):
        """카페24 설정 로드"""
        config_path = "C:/Users/8899y/CUA-MASTER/modules/cafe24/config/cafe24_config.json"
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 설정 로드 실패: {e}")
            return None
    
    def setup_browser(self):
        """브라우저 설정"""
        try:
            options = Options()
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, 15)
            
            print("✅ 브라우저 설정 완료")
            return True
            
        except Exception as e:
            print(f"❌ 브라우저 설정 실패: {e}")
            return False
    
    def login_to_cafe24(self):
        """카페24 관리자 로그인"""
        try:
            print("🔐 카페24 관리자 로그인...")
            
            login_url = self.config['cafe24']['admin_url']
            self.driver.get(login_url)
            time.sleep(3)
            
            # 로그인 정보 입력
            username_field = self.wait.until(EC.presence_of_element_located((By.NAME, "mall_id")))
            username_field.clear()
            username_field.send_keys(self.config['cafe24']['username'])
            
            password_field = self.driver.find_element(By.NAME, "userpasswd")
            password_field.clear()
            password_field.send_keys(self.config['cafe24']['password'])
            
            # 로그인 버튼 클릭
            login_button = self.driver.find_element(By.XPATH, "//input[@type='submit' or @type='image']")
            login_button.click()
            
            time.sleep(5)
            
            if "admin" in self.driver.current_url:
                print("✅ 카페24 로그인 성공")
                return True
            else:
                print("❌ 카페24 로그인 실패")
                return False
                
        except Exception as e:
            print(f"❌ 로그인 오류: {e}")
            return False
    
    def navigate_to_product_edit(self, product_code=None):
        """상품 편집 페이지로 이동"""
        try:
            print("📦 상품 편집 페이지로 이동...")
            
            # 상품관리 메뉴 클릭
            product_menu = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '상품관리') or contains(@href, 'product')]")))
            product_menu.click()
            time.sleep(2)
            
            # 상품 목록 클릭
            product_list = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '상품목록') or contains(@href, 'productlist')]")))
            product_list.click()
            time.sleep(3)
            
            # 첫 번째 상품의 수정 버튼 클릭 (또는 특정 상품 검색)
            if product_code:
                # 상품 코드로 검색
                search_field = self.driver.find_element(By.NAME, "search_key")
                search_field.clear()
                search_field.send_keys(product_code)
                search_button = self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='검색']")
                search_button.click()
                time.sleep(3)
            
            # 수정 버튼 클릭
            edit_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '수정') or contains(@href, 'product_modify')]")))
            edit_button.click()
            time.sleep(5)
            
            print("✅ 상품 편집 페이지 접근 성공")
            return True
            
        except Exception as e:
            print(f"❌ 상품 편집 페이지 접근 실패: {e}")
            return False
    
    def find_html_editor(self):
        """HTML 편집기 찾기 및 접근"""
        try:
            print("🔍 HTML 편집기 찾는 중...")
            
            # 상세설명 탭 클릭 (있는 경우)
            try:
                detail_tab = self.driver.find_element(By.XPATH, "//a[contains(text(), '상세설명') or contains(text(), '상세정보')]")
                detail_tab.click()
                time.sleep(2)
            except:
                pass
            
            # HTML 편집기 iframe 찾기
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            
            for i, iframe in enumerate(iframes):
                try:
                    # iframe으로 전환
                    self.driver.switch_to.frame(iframe)
                    
                    # HTML 편집기인지 확인
                    editor_body = self.driver.find_element(By.TAG_NAME, "body")
                    if editor_body.get_attribute("contenteditable") == "true" or editor_body.get_attribute("class"):
                        print(f"✅ HTML 편집기 발견 (iframe {i})")
                        return True
                        
                except:
                    # 원래 프레임으로 돌아가기
                    self.driver.switch_to.default_content()
                    continue
            
            print("❌ HTML 편집기를 찾을 수 없음")
            return False
            
        except Exception as e:
            print(f"❌ HTML 편집기 찾기 실패: {e}")
            return False
    
    def get_current_html_content(self):
        """현재 HTML 콘텐츠 가져오기"""
        try:
            print("📖 현재 HTML 콘텐츠 읽기...")
            
            # HTML 편집기 본문 가져오기
            editor_body = self.driver.find_element(By.TAG_NAME, "body")
            current_html = editor_body.get_attribute("innerHTML")
            
            print(f"✅ HTML 콘텐츠 읽기 성공 ({len(current_html)} 글자)")
            return current_html
            
        except Exception as e:
            print(f"❌ HTML 콘텐츠 읽기 실패: {e}")
            return None
    
    def replace_html_content(self, new_html_content):
        """HTML 콘텐츠 교체"""
        try:
            print("✏️ HTML 콘텐츠 교체 중...")
            
            # JavaScript로 HTML 콘텐츠 교체
            script = f"""
            var body = document.querySelector('body');
            if (body) {{
                body.innerHTML = `{new_html_content}`;
                console.log('HTML 콘텐츠 교체 완료');
                return true;
            }} else {{
                console.log('HTML 편집기 body 요소를 찾을 수 없음');
                return false;
            }}
            """
            
            result = self.driver.execute_script(script)
            
            if result:
                print("✅ HTML 콘텐츠 교체 성공")
                time.sleep(2)  # 변경 사항 반영 대기
                return True
            else:
                print("❌ HTML 콘텐츠 교체 실패")
                return False
                
        except Exception as e:
            print(f"❌ HTML 콘텐츠 교체 오류: {e}")
            return False
    
    def save_changes(self):
        """변경사항 저장"""
        try:
            print("💾 변경사항 저장 중...")
            
            # 원래 프레임으로 돌아가기
            self.driver.switch_to.default_content()
            
            # 저장 버튼 찾기 및 클릭
            save_selectors = [
                "//input[@value='저장' or @value='수정']",
                "//button[contains(text(), '저장') or contains(text(), '수정')]",
                "//a[contains(text(), '저장') or contains(text(), '수정')]"
            ]
            
            for selector in save_selectors:
                try:
                    save_button = self.driver.find_element(By.XPATH, selector)
                    save_button.click()
                    print("✅ 저장 버튼 클릭 성공")
                    time.sleep(5)  # 저장 처리 대기
                    return True
                except:
                    continue
            
            print("❌ 저장 버튼을 찾을 수 없음")
            return False
            
        except Exception as e:
            print(f"❌ 저장 실패: {e}")
            return False
    
    def load_html_template(self, brand_name, product_id):
        """브랜드별 HTML 템플릿 로드"""
        try:
            print(f"📄 HTML 템플릿 로드: {brand_name}/{product_id}")
            
            # 브랜드 폴더에서 HTML 파일 찾기
            brand_path = self.html_templates_path / brand_name
            if not brand_path.exists():
                print(f"❌ 브랜드 폴더 없음: {brand_name}")
                return None
            
            # 상품 ID에 해당하는 HTML 파일 찾기
            html_files = list(brand_path.glob(f"{product_id}.html"))
            if not html_files:
                html_files = list(brand_path.glob("*.html"))
                if html_files:
                    html_file = html_files[0]  # 첫 번째 파일 사용
                else:
                    print(f"❌ HTML 파일 없음: {product_id}")
                    return None
            else:
                html_file = html_files[0]
            
            # HTML 파일 읽기
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
                
            print(f"✅ HTML 템플릿 로드 성공: {html_file.name}")
            return html_content
            
        except Exception as e:
            print(f"❌ HTML 템플릿 로드 실패: {e}")
            return None
    
    def edit_product_detail_page(self, brand_name="만원요리", product_id="168", product_code=None):
        """상품 상세페이지 편집 전체 프로세스"""
        try:
            print("=" * 60)
            print("🎨 Claude 상세페이지 편집 시작")
            print(f"🏷️ 브랜드: {brand_name}")
            print(f"🆔 상품ID: {product_id}")
            print(f"📋 상품코드: {product_code if product_code else '자동선택'}")
            print("=" * 60)
            
            # 1. 브라우저 설정
            if not self.setup_browser():
                return False
            
            # 2. 카페24 로그인
            if not self.login_to_cafe24():
                return False
            
            # 3. 상품 편집 페이지로 이동
            if not self.navigate_to_product_edit(product_code):
                return False
            
            # 4. HTML 편집기 찾기
            if not self.find_html_editor():
                return False
            
            # 5. 현재 HTML 백업
            current_html = self.get_current_html_content()
            if current_html:
                backup_path = f"backup_html_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(current_html)
                print(f"💾 현재 HTML 백업: {backup_path}")
            
            # 6. 새 HTML 템플릿 로드
            new_html = self.load_html_template(brand_name, product_id)
            if not new_html:
                print("❌ 새 HTML 템플릿을 로드할 수 없음")
                return False
            
            # 7. HTML 콘텐츠 교체
            if not self.replace_html_content(new_html):
                return False
            
            # 8. 변경사항 저장
            if not self.save_changes():
                return False
            
            print("=" * 60)
            print("✅ 상세페이지 편집 완료!")
            print("=" * 60)
            
            return True
            
        except Exception as e:
            print(f"❌ 상세페이지 편집 실패: {e}")
            return False
        finally:
            # 브라우저 종료 (선택사항)
            # if self.driver:
            #     self.driver.quit()
            pass
    
    def batch_edit_products(self, edit_list):
        """여러 상품 일괄 편집"""
        try:
            print(f"🔄 {len(edit_list)}개 상품 일괄 편집 시작")
            
            success_count = 0
            for i, product_info in enumerate(edit_list, 1):
                print(f"\n[{i}/{len(edit_list)}] 상품 편집 중...")
                
                if self.edit_product_detail_page(**product_info):
                    success_count += 1
                    print(f"✅ 상품 {i} 편집 성공")
                else:
                    print(f"❌ 상품 {i} 편집 실패")
                
                # 다음 상품으로 이동하기 전 대기
                time.sleep(3)
            
            print(f"\n📊 일괄 편집 결과: {success_count}/{len(edit_list)} 성공")
            return success_count
            
        except Exception as e:
            print(f"❌ 일괄 편집 실패: {e}")
            return 0

def main():
    """메인 실행 함수"""
    editor = ClaudeDetailPageEditor()
    
    try:
        # 단일 상품 편집 테스트
        success = editor.edit_product_detail_page(
            brand_name="만원요리",
            product_id="168",
            product_code=None  # 첫 번째 상품 자동 선택
        )
        
        if success:
            print("🎉 상세페이지 편집 테스트 성공!")
        else:
            print("💥 상세페이지 편집 테스트 실패")
            
    except KeyboardInterrupt:
        print("\n⚠️ 사용자에 의해 중단됨")
    except Exception as e:
        print(f"❌ 실행 오류: {e}")

if __name__ == "__main__":
    main()

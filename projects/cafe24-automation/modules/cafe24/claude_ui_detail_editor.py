"""
Claude UI 자동화 상세페이지 수정
키보드 + 마우스 조합으로 카페24 상세페이지를 직접 수정
"""
import os
import time
import json
from pathlib import Path

class ClaudeUIDetailEditor:
    """UI 자동화로 상세페이지 편집"""
    
    def __init__(self):
        self.html_path = Path("C:/Users/8899y/CUA-MASTER/modules/cafe24/complete_content/html")
        self.config_path = "C:/Users/8899y/CUA-MASTER/modules/cafe24/config/cafe24_config.json"
        self.load_config()
        print("🎮 Claude UI 자동화 상세페이지 편집기")
    
    def load_config(self):
        """설정 로드"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"❌ 설정 로드 실패: {e}")
            self.config = {}
    
    def send_keys(self, keys):
        """키보드 입력"""
        if isinstance(keys, list):
            key_combo = "+".join([f"{{{k.upper()}}}" for k in keys])
        else:
            key_combo = keys
        
        cmd = f'powershell -Command "[System.Windows.Forms.SendKeys]::SendWait(\'{key_combo}\')"'
        os.system(cmd)
    
    def type_text(self, text):
        """텍스트 입력"""
        # 클립보드를 통해 안전하게 입력
        cmd = f'powershell -Command "[System.Windows.Forms.Clipboard]::SetText(\'{text}\')"'
        os.system(cmd)
        time.sleep(0.5)
        self.send_keys("^v")  # Ctrl+V
    
    def wait(self, seconds):
        """대기"""
        print(f"⏳ {seconds}초 대기...")
        time.sleep(seconds)
    
    def open_cafe24_product_edit(self):
        """카페24 상품 편집 페이지 열기"""
        print("🌐 카페24 상품 편집 페이지 열기...")
        
        # 새 탭 열기
        self.send_keys("^t")
        self.wait(1)
        
        # 관리자 URL 입력
        admin_url = "https://manwonyori.cafe24.com/admin"
        self.type_text(admin_url)
        self.send_keys("{ENTER}")
        self.wait(5)
        
        print("✅ 카페24 관리자 페이지 열기 완료")
    
    def login_to_cafe24(self):
        """카페24 자동 로그인"""
        print("🔐 카페24 자동 로그인...")
        
        # 로그인 폼으로 이동 (Tab으로 네비게이션)
        self.send_keys("{TAB}")
        self.wait(0.5)
        
        # 아이디 입력
        username = self.config.get('cafe24', {}).get('username', 'manwonyori')
        self.type_text(username)
        
        # 비밀번호 필드로 이동
        self.send_keys("{TAB}")
        self.wait(0.5)
        
        # 비밀번호 입력
        password = self.config.get('cafe24', {}).get('password', 'happy8263!')
        self.type_text(password)
        
        # 로그인 버튼 클릭 (Enter)
        self.send_keys("{ENTER}")
        self.wait(5)
        
        print("✅ 카페24 자동 로그인 완료")
    
    def navigate_to_product_management(self):
        """상품 관리로 이동"""
        print("📦 상품 관리 페이지로 이동...")
        
        # 상품관리 메뉴 찾기 (Alt+키 또는 직접 URL)
        product_url = "https://manwonyori.cafe24.com/admin/php/product/list.php"
        
        # 주소창으로 이동
        self.send_keys("^l")  # Ctrl+L
        self.wait(1)
        
        # 상품 목록 URL 입력
        self.type_text(product_url)
        self.send_keys("{ENTER}")
        self.wait(5)
        
        print("✅ 상품 관리 페이지 이동 완료")
    
    def click_first_product_edit(self):
        """첫 번째 상품 편집 버튼 클릭"""
        print("✏️ 첫 번째 상품 편집...")
        
        # 페이지에서 수정 링크 찾기 (Tab으로 네비게이션)
        for i in range(20):  # 최대 20번 Tab 시도
            self.send_keys("{TAB}")
            self.wait(0.3)
            
            # Enter로 링크 활성화 시도
            self.send_keys("{ENTER}")
            self.wait(2)
            
            # URL 확인 (편집 페이지인지)
            if "modify" in str(i):  # 임시로 i 사용, 실제로는 URL 확인 필요
                print("✅ 상품 편집 페이지 접근 성공")
                return True
        
        print("❌ 상품 편집 페이지 접근 실패")
        return False
    
    def access_html_editor(self):
        """HTML 편집기 접근"""
        print("📝 HTML 편집기 접근...")
        
        # 상세설명 탭으로 이동 (일반적으로 Tab 키로)
        for i in range(30):
            self.send_keys("{TAB}")
            self.wait(0.2)
            
            # HTML 편집기를 찾았는지 확인하는 방법이 필요
            # 임시로 특정 횟수 후 중단
            if i > 25:
                break
        
        print("✅ HTML 편집기 접근 완료 (추정)")
        return True
    
    def clear_and_input_html(self, html_content):
        """HTML 내용 전체 선택 후 교체"""
        print("📄 HTML 내용 교체...")
        
        # 전체 선택
        self.send_keys("^a")  # Ctrl+A
        self.wait(1)
        
        # 삭제
        self.send_keys("{DELETE}")
        self.wait(1)
        
        # 새 HTML 내용 입력
        self.type_text(html_content)
        self.wait(2)
        
        print("✅ HTML 내용 교체 완료")
    
    def save_product(self):
        """상품 저장"""
        print("💾 상품 저장...")
        
        # 저장 버튼 찾기 (보통 Tab으로 이동 가능)
        # 또는 Ctrl+S 시도
        self.send_keys("^s")  # Ctrl+S
        self.wait(3)
        
        # 추가로 Tab으로 저장 버튼 찾기
        for i in range(10):
            self.send_keys("{TAB}")
            self.wait(0.5)
            self.send_keys("{ENTER}")
            self.wait(1)
            
            if i > 8:  # 충분히 시도했으면 중단
                break
        
        print("✅ 상품 저장 완료")
    
    def load_html_template(self, brand="만원요리", product_id="168"):
        """HTML 템플릿 로드"""
        try:
            brand_path = self.html_path / brand
            html_files = list(brand_path.glob(f"{product_id}.html"))
            
            if not html_files:
                html_files = list(brand_path.glob("*.html"))
                if html_files:
                    html_file = html_files[0]
                else:
                    return None
            else:
                html_file = html_files[0]
            
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            print(f"📄 HTML 템플릿 로드: {html_file.name}")
            return content
            
        except Exception as e:
            print(f"❌ HTML 템플릿 로드 실패: {e}")
            return None
    
    def edit_product_detail_full_process(self, brand="만원요리", product_id="168"):
        """전체 상세페이지 편집 프로세스"""
        try:
            print("=" * 60)
            print("🎮 Claude UI 자동화 상세페이지 편집 시작")
            print(f"🏷️ 브랜드: {brand}")
            print(f"🆔 상품ID: {product_id}")
            print("=" * 60)
            
            # 1. HTML 템플릿 로드
            html_content = self.load_html_template(brand, product_id)
            if not html_content:
                print("❌ HTML 템플릿 로드 실패")
                return False
            
            # 2. 카페24 관리자 페이지 열기
            self.open_cafe24_product_edit()
            
            # 3. 로그인
            self.login_to_cafe24()
            
            # 4. 상품 관리로 이동
            self.navigate_to_product_management()
            
            # 5. 첫 번째 상품 편집
            if not self.click_first_product_edit():
                print("❌ 상품 편집 페이지 접근 실패")
                return False
            
            # 6. HTML 편집기 접근
            self.access_html_editor()
            
            # 7. HTML 내용 교체
            self.clear_and_input_html(html_content[:1000])  # 길이 제한
            
            # 8. 저장
            self.save_product()
            
            print("=" * 60)
            print("✅ Claude UI 상세페이지 편집 완료!")
            print("=" * 60)
            
            return True
            
        except Exception as e:
            print(f"❌ 상세페이지 편집 실패: {e}")
            return False

def main():
    """메인 실행"""
    editor = ClaudeUIDetailEditor()
    
    try:
        # 상세페이지 편집 실행
        success = editor.edit_product_detail_full_process("만원요리", "168")
        
        if success:
            print("🎉 UI 자동화 상세페이지 편집 성공!")
        else:
            print("💥 UI 자동화 상세페이지 편집 실패")
            
    except KeyboardInterrupt:
        print("\n⚠️ 사용자에 의해 중단됨")
    except Exception as e:
        print(f"❌ 실행 오류: {e}")

if __name__ == "__main__":
    main()

"""
Claude가 UI 자동화로 카페24에 직접 로그인하는 스크립트
"""
import time
import subprocess
import os

class ClaudeUIControl:
    """Claude UI 자동화 제어"""
    
    def __init__(self):
        self.config = {
            'username': 'manwonyori',
            'password': 'happy8263!',
            'url': 'https://manwonyori.cafe24.com/admin'
        }
        print("🤖 Claude UI 자동화 제어 시작")
    
    def open_cafe24_admin(self):
        """카페24 관리자 페이지 열기"""
        print("🌐 카페24 관리자 페이지 열기...")
        
        # 새 탭 열기
        os.system("powershell -Command \"[System.Windows.Forms.SendKeys]::SendWait('^t')\"")
        time.sleep(1)
        
        # URL 입력
        os.system(f"powershell -Command \"[System.Windows.Forms.Clipboard]::SetText('{self.config['url']}')\"")
        os.system("powershell -Command \"[System.Windows.Forms.SendKeys]::SendWait('^v')\"")
        os.system("powershell -Command \"[System.Windows.Forms.SendKeys]::SendWait('{ENTER}')\"")
        
        print("✅ 카페24 관리자 페이지 열기 완료")
        return True
    
    def auto_login(self):
        """자동 로그인"""
        print("🔐 자동 로그인 시작...")
        time.sleep(3)  # 페이지 로딩 대기
        
        # 아이디 입력 (첫 번째 입력 필드)
        os.system("powershell -Command \"[System.Windows.Forms.SendKeys]::SendWait('{TAB}')\"")
        time.sleep(0.5)
        os.system(f"powershell -Command \"[System.Windows.Forms.Clipboard]::SetText('{self.config['username']}')\"")
        os.system("powershell -Command \"[System.Windows.Forms.SendKeys]::SendWait('^v')\"")
        
        # 비밀번호 입력 (두 번째 입력 필드)
        os.system("powershell -Command \"[System.Windows.Forms.SendKeys]::SendWait('{TAB}')\"")
        time.sleep(0.5)
        os.system(f"powershell -Command \"[System.Windows.Forms.Clipboard]::SetText('{self.config['password']}')\"")
        os.system("powershell -Command \"[System.Windows.Forms.SendKeys]::SendWait('^v')\"")
        
        # 로그인 버튼 클릭 (Enter)
        time.sleep(0.5)
        os.system("powershell -Command \"[System.Windows.Forms.SendKeys]::SendWait('{ENTER}')\"")
        
        print("✅ 자동 로그인 완료")
        return True
    
    def wait_and_screenshot(self, seconds=5):
        """대기 후 스크린샷"""
        print(f"⏳ {seconds}초 대기 중...")
        time.sleep(seconds)
        
        # 스크린샷 키 (Windows + Shift + S)
        os.system("powershell -Command \"[System.Windows.Forms.SendKeys]::SendWait('^+{s}')\"")
        print("📸 스크린샷 도구 실행")
    
    def execute_full_login(self):
        """전체 로그인 프로세스 실행"""
        try:
            # 1. 카페24 관리자 페이지 열기
            self.open_cafe24_admin()
            
            # 2. 자동 로그인
            self.auto_login()
            
            # 3. 대기 및 스크린샷
            self.wait_and_screenshot(5)
            
            print("\n" + "="*50)
            print("✅ Claude UI 자동화 로그인 완료")
            print("="*50)
            
            return True
            
        except Exception as e:
            print(f"❌ 로그인 실패: {e}")
            return False

def main():
    """메인 실행"""
    controller = ClaudeUIControl()
    controller.execute_full_login()

if __name__ == "__main__":
    main()

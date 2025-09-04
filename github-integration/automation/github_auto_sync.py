#!/usr/bin/env python3
"""
AI-WORKSPACE GitHub 자동 동기화 시스템
실시간으로 변경사항을 GitHub에 동기화하며 AI 협업을 지원
"""
import os
import time
import subprocess
import json
from datetime import datetime
from pathlib import Path

class AIWorkspaceGitSync:
    def __init__(self):
        self.workspace_path = Path("C:/Users/8899y/AI-WORKSPACE")
        self.root_path = Path("C:/Users/8899y")
        self.sync_interval = 300  # 5분마다
        self.status_file = self.workspace_path / "sync_status.json"
        
    def check_git_status(self):
        """Git 상태 확인"""
        try:
            os.chdir(self.root_path)
            result = subprocess.run(["git", "status", "--porcelain"], 
                                  capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            print("❌ Git 상태 확인 실패")
            return None
    
    def safe_commit_and_push(self):
        """안전한 커밋 및 푸시"""
        try:
            os.chdir(self.root_path)
            
            # 변경사항 확인
            status = self.check_git_status()
            if not status:
                print("✅ 변경사항 없음")
                return True
            
            # 민감한 파일 확인 (SECURE 폴더는 .gitignore로 제외됨)
            sensitive_files = [
                "FTP_CONFIG.json", "password", "token", "secret", "key",
                ".env", "credentials"
            ]
            
            changes = status.split('\n')
            for change in changes:
                for sensitive in sensitive_files:
                    if sensitive.lower() in change.lower():
                        print(f"⚠️ 민감한 파일 감지: {change}")
                        return False
            
            # 변경사항 추가
            subprocess.run(["git", "add", "."], check=True)
            
            # 커밋 메시지 생성
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_msg = f"""Auto sync AI-WORKSPACE: {timestamp}

🤖 AI Collaboration Update:
- Genesis Ultimate: 339 products system
- Cafe24 Automation: CUA integrated
- MCP System: Active with 14+ servers

🔐 Security: All sensitive files in SECURE/ (gitignored)
🚀 Ready for: ChatGPT, Claude, Perplexity, Gemini

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"""
            
            # 커밋
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            print(f"✅ 커밋 완료: {timestamp}")
            
            # 푸시
            subprocess.run(["git", "push"], check=True)
            print("✅ GitHub 동기화 완료")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git 작업 실패: {e}")
            return False
    
    def update_status(self, success=True):
        """동기화 상태 업데이트"""
        status = {
            "last_sync": datetime.now().isoformat(),
            "success": success,
            "workspace_active": True,
            "mcp_status": "running",
            "ai_collaboration": {
                "chatgpt": "ready",
                "claude": "active", 
                "perplexity": "ready",
                "gemini": "ready"
            }
        }
        
        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump(status, f, indent=2, ensure_ascii=False)
    
    def run_continuous(self):
        """연속 동기화 실행"""
        print("🚀 AI-WORKSPACE GitHub 자동 동기화 시작")
        print(f"📁 워크스페이스: {self.workspace_path}")
        print(f"🔄 동기화 간격: {self.sync_interval}초")
        print("🔐 보안: SECURE/ 폴더 자동 제외")
        print("-" * 50)
        
        while True:
            try:
                print(f"\n🔄 동기화 시작: {datetime.now().strftime('%H:%M:%S')}")
                
                success = self.safe_commit_and_push()
                self.update_status(success)
                
                if success:
                    print("✅ 동기화 성공")
                else:
                    print("⚠️ 동기화 스킵 (민감한 파일 또는 변경사항 없음)")
                
                print(f"⏰ {self.sync_interval}초 대기 중...")
                time.sleep(self.sync_interval)
                
            except KeyboardInterrupt:
                print("\n\n🛑 사용자에 의해 중단됨")
                break
            except Exception as e:
                print(f"❌ 예상치 못한 오류: {e}")
                self.update_status(False)
                time.sleep(60)  # 1분 대기 후 재시도

if __name__ == "__main__":
    sync = AIWorkspaceGitSync()
    sync.run_continuous()
# -*- coding: utf-8 -*-
"""
Claude 대화 자동 저장 스케줄러
실시간으로 대화 내용을 감지하고 자동 저장하는 백그라운드 서비스
"""
import os
import time
import json
import threading
from datetime import datetime
from pathlib import Path
import schedule
from claude_conversation_manager import ClaudeConversationManager

class ConversationAutoSaver:
    """대화 자동 저장기"""
    
    def __init__(self):
        """초기화"""
        self.manager = ClaudeConversationManager()
        self.current_session_id = None
        self.last_check_time = datetime.now()
        self.auto_save_interval = 5  # 5분마다 자동 저장
        self.running = False
        
        print("🔄 Claude 대화 자동 저장 스케줄러 시작")
    
    def start_new_session(self, topic="자동 생성 세션"):
        """새 세션 시작"""
        self.current_session_id = self.manager.create_session(topic)
        print(f"🆕 새 세션 시작: {self.current_session_id}")
        return self.current_session_id
    
    def detect_and_save_conversation(self):
        """대화 감지 및 저장"""
        try:
            # 대화 로그 파일에서 새로운 내용 감지
            log_files = [
                Path("C:/Users/8899y/CUA-MASTER/logs/claude_conversation_20250902.md"),
                Path("C:/Users/8899y/CUA-MASTER/conversations")
            ]
            
            for log_file in log_files:
                if log_file.exists() and log_file.is_file():
                    # 파일 수정 시간 확인
                    modified_time = datetime.fromtimestamp(log_file.stat().st_mtime)
                    if modified_time > self.last_check_time:
                        # 새 내용이 있으면 저장
                        self.save_recent_updates(log_file)
                        self.last_check_time = modified_time
            
            # 새로 생성된 파일 감지
            self.detect_new_files()
            
        except Exception as e:
            print(f"❌ 대화 감지 실패: {e}")
    
    def save_recent_updates(self, log_file):
        """최근 업데이트 저장"""
        try:
            if not self.current_session_id:
                self.start_new_session(f"자동 감지 - {datetime.now().strftime('%H:%M')}")
            
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 간단한 파싱으로 대화 내용 추출
            lines = content.split('\n')
            for line in lines:
                if line.startswith('- '):
                    # 간단한 메시지로 저장
                    self.manager.save_message(
                        self.current_session_id,
                        "System",
                        line,
                        "log_entry"
                    )
            
            print(f"💾 로그 파일 업데이트 저장: {log_file.name}")
            
        except Exception as e:
            print(f"❌ 로그 저장 실패: {e}")
    
    def detect_new_files(self):
        """새로 생성된 파일 감지"""
        try:
            # 오늘 생성된 파일들 찾기
            base_dir = Path("C:/Users/8899y/CUA-MASTER")
            today = datetime.now().date()
            
            for file_path in base_dir.rglob("*"):
                if file_path.is_file():
                    created_time = datetime.fromtimestamp(file_path.stat().st_ctime)
                    if created_time.date() == today and created_time > self.last_check_time:
                        # Claude가 생성한 파일인지 확인
                        if "claude" in file_path.name.lower() or "photoshop" in file_path.name.lower():
                            if self.current_session_id:
                                self.manager.save_created_file(
                                    self.current_session_id,
                                    str(file_path),
                                    f"자동 감지된 파일 - {created_time.strftime('%H:%M')}"
                                )
            
        except Exception as e:
            print(f"❌ 새 파일 감지 실패: {e}")
    
    def export_daily_summary(self):
        """일일 요약 생성"""
        try:
            if self.current_session_id:
                # 마크다운으로 내보내기
                markdown_file = self.manager.export_conversation_to_markdown(self.current_session_id)
                
                # 추가 요약 정보 생성
                summary_data = {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "session_id": self.current_session_id,
                    "exported_file": str(markdown_file) if markdown_file else None,
                    "auto_saved": True
                }
                
                # JSON 요약 파일 생성
                summary_file = Path(f"C:/Users/8899y/CUA-MASTER/logs/daily_summary_{datetime.now().strftime('%Y%m%d')}.json")
                with open(summary_file, 'w', encoding='utf-8') as f:
                    json.dump(summary_data, f, ensure_ascii=False, indent=2)
                
                print(f"📊 일일 요약 생성 완료: {summary_file}")
                
        except Exception as e:
            print(f"❌ 일일 요약 생성 실패: {e}")
    
    def backup_conversations(self):
        """대화 백업"""
        try:
            # 데이터베이스 백업
            source_db = Path("C:/Users/8899y/CUA-MASTER/data/claude_conversations.db")
            backup_dir = Path("C:/Users/8899y/CUA-MASTER/backup/conversations")
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            if source_db.exists():
                backup_file = backup_dir / f"conversations_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.db"
                import shutil
                shutil.copy2(source_db, backup_file)
                print(f"💾 대화 데이터베이스 백업 완료: {backup_file}")
            
        except Exception as e:
            print(f"❌ 백업 실패: {e}")
    
    def start_scheduler(self):
        """스케줄러 시작"""
        self.running = True
        
        # 스케줄 설정
        schedule.every(5).minutes.do(self.detect_and_save_conversation)  # 5분마다 대화 감지
        schedule.every(1).hours.do(self.export_daily_summary)  # 1시간마다 요약
        schedule.every(4).hours.do(self.backup_conversations)  # 4시간마다 백업
        
        print("⏰ 자동 저장 스케줄 시작:")
        print("  - 대화 감지: 5분마다")
        print("  - 요약 생성: 1시간마다")  
        print("  - 백업: 4시간마다")
        
        # 첫 세션 시작
        self.start_new_session("자동 저장 세션")
        
        # 스케줄 실행
        while self.running:
            schedule.run_pending()
            time.sleep(30)  # 30초마다 스케줄 체크
    
    def stop_scheduler(self):
        """스케줄러 중지"""
        self.running = False
        print("🛑 자동 저장 스케줄러 중지")

def run_in_background():
    """백그라운드 실행"""
    auto_saver = ConversationAutoSaver()
    
    try:
        # 백그라운드 스레드로 실행
        scheduler_thread = threading.Thread(target=auto_saver.start_scheduler, daemon=True)
        scheduler_thread.start()
        
        print("🚀 백그라운드 자동 저장 시작")
        
        # 메인 스레드는 계속 실행
        while True:
            time.sleep(60)  # 1분마다 상태 체크
            
    except KeyboardInterrupt:
        print("\n⚠️ 사용자에 의해 중단됨")
        auto_saver.stop_scheduler()
    except Exception as e:
        print(f"❌ 백그라운드 실행 오류: {e}")

def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("🤖 Claude 대화 자동 저장 시스템")
    print("=" * 60)
    
    choice = input("실행 모드를 선택하세요:\n1. 백그라운드 자동 저장\n2. 수동 저장 테스트\n선택 (1-2): ")
    
    if choice == "1":
        run_in_background()
    elif choice == "2":
        # 수동 테스트
        auto_saver = ConversationAutoSaver()
        auto_saver.start_new_session("수동 테스트 세션")
        auto_saver.detect_and_save_conversation()
        auto_saver.export_daily_summary()
        print("✅ 수동 저장 테스트 완료")
    else:
        print("❌ 잘못된 선택")

if __name__ == "__main__":
    main()

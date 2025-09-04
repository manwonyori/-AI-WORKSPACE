# -*- coding: utf-8 -*-
"""
Claude 대화 지속 저장 및 컨텍스트 관리 시스템
실시간으로 대화 내용을 저장하고 이후 세션에서 활용하는 통합 시스템
"""
import os
import json
import sqlite3
from datetime import datetime
from pathlib import Path
import hashlib

class ClaudeConversationManager:
    """Claude 대화 지속 저장 관리자"""
    
    def __init__(self, base_dir="C:/Users/8899y/CUA-MASTER"):
        """초기화"""
        self.base_dir = Path(base_dir)
        self.conversation_dir = self.base_dir / "conversations"
        self.db_path = self.base_dir / "data" / "claude_conversations.db"
        
        # 디렉토리 생성
        self.conversation_dir.mkdir(exist_ok=True)
        (self.base_dir / "data").mkdir(exist_ok=True)
        
        # 데이터베이스 초기화
        self.init_database()
        
        print("💾 Claude 대화 지속 저장 시스템 시작")
        print(f"📁 대화 저장 경로: {self.conversation_dir}")
        print(f"🗄️ 데이터베이스: {self.db_path}")
    
    def init_database(self):
        """데이터베이스 초기화"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 대화 세션 테이블
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversation_sessions (
                    session_id TEXT PRIMARY KEY,
                    start_time DATETIME,
                    end_time DATETIME,
                    topic TEXT,
                    summary TEXT,
                    file_path TEXT,
                    message_count INTEGER DEFAULT 0,
                    created_files INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'active'
                )
                """)
                
                # 개별 메시지 테이블
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    timestamp DATETIME,
                    speaker TEXT,
                    content TEXT,
                    content_hash TEXT,
                    message_type TEXT,
                    metadata TEXT,
                    FOREIGN KEY (session_id) REFERENCES conversation_sessions (session_id)
                )
                """)
                
                # 생성된 파일 추적 테이블
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS created_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    file_path TEXT,
                    file_type TEXT,
                    file_size INTEGER,
                    description TEXT,
                    created_time DATETIME,
                    FOREIGN KEY (session_id) REFERENCES conversation_sessions (session_id)
                )
                """)
                
                # 프로젝트 컨텍스트 테이블
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS project_contexts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_name TEXT,
                    last_session_id TEXT,
                    context_data TEXT,
                    updated_time DATETIME,
                    UNIQUE(project_name)
                )
                """)
                
                conn.commit()
                print("✅ 데이터베이스 초기화 완료")
                
        except Exception as e:
            print(f"❌ 데이터베이스 초기화 실패: {e}")
    
    def create_session(self, topic="일반 대화"):
        """새 대화 세션 생성"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        start_time = datetime.now()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                INSERT INTO conversation_sessions 
                (session_id, start_time, topic, status)
                VALUES (?, ?, ?, 'active')
                """, (session_id, start_time, topic))
                conn.commit()
            
            print(f"📝 새 대화 세션 생성: {session_id}")
            return session_id
            
        except Exception as e:
            print(f"❌ 세션 생성 실패: {e}")
            return None
    
    def save_message(self, session_id, speaker, content, message_type="text", metadata=None):
        """메시지 저장"""
        try:
            timestamp = datetime.now()
            content_hash = hashlib.md5(content.encode()).hexdigest()
            metadata_json = json.dumps(metadata) if metadata else None
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                INSERT INTO messages 
                (session_id, timestamp, speaker, content, content_hash, message_type, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (session_id, timestamp, speaker, content, content_hash, message_type, metadata_json))
                
                # 메시지 카운트 업데이트
                cursor.execute("""
                UPDATE conversation_sessions 
                SET message_count = message_count + 1, end_time = ?
                WHERE session_id = ?
                """, (timestamp, session_id))
                
                conn.commit()
            
            return True
            
        except Exception as e:
            print(f"❌ 메시지 저장 실패: {e}")
            return False
    
    def save_created_file(self, session_id, file_path, description=""):
        """생성된 파일 정보 저장"""
        try:
            file_path_obj = Path(file_path)
            file_type = file_path_obj.suffix.lower()
            file_size = file_path_obj.stat().st_size if file_path_obj.exists() else 0
            created_time = datetime.now()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                INSERT INTO created_files 
                (session_id, file_path, file_type, file_size, description, created_time)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (session_id, str(file_path), file_type, file_size, description, created_time))
                
                # 생성 파일 카운트 업데이트
                cursor.execute("""
                UPDATE conversation_sessions 
                SET created_files = created_files + 1
                WHERE session_id = ?
                """, (session_id,))
                
                conn.commit()
            
            print(f"📄 파일 추가 기록: {file_path_obj.name}")
            return True
            
        except Exception as e:
            print(f"❌ 파일 정보 저장 실패: {e}")
            return False
    
    def export_conversation_to_markdown(self, session_id):
        """대화를 마크다운으로 내보내기"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 세션 정보 가져오기
                cursor.execute("""
                SELECT * FROM conversation_sessions WHERE session_id = ?
                """, (session_id,))
                session = cursor.fetchone()
                
                if not session:
                    print(f"❌ 세션을 찾을 수 없음: {session_id}")
                    return None
                
                # 메시지 가져오기
                cursor.execute("""
                SELECT timestamp, speaker, content, message_type
                FROM messages 
                WHERE session_id = ? 
                ORDER BY timestamp
                """, (session_id,))
                messages = cursor.fetchall()
                
                # 생성된 파일 가져오기
                cursor.execute("""
                SELECT file_path, description, created_time
                FROM created_files 
                WHERE session_id = ?
                ORDER BY created_time
                """, (session_id,))
                files = cursor.fetchall()
            
            # 마크다운 생성
            markdown_content = f"""# Claude 대화 기록
**세션 ID**: {session_id}
**주제**: {session[3] if len(session) > 3 else '일반 대화'}
**시작 시간**: {session[1]}
**종료 시간**: {session[2] if session[2] else '진행 중'}
**메시지 수**: {session[6] if len(session) > 6 else 0}
**생성 파일 수**: {session[7] if len(session) > 7 else 0}

---

## 💬 대화 내용

"""
            
            for msg in messages:
                timestamp, speaker, content, msg_type = msg
                speaker_emoji = "🧑" if speaker == "Human" else "🤖"
                markdown_content += f"### {speaker_emoji} {speaker} ({timestamp})\n\n"
                markdown_content += f"{content}\n\n---\n\n"
            
            # 생성된 파일 목록 추가
            if files:
                markdown_content += "## 📁 생성된 파일들\n\n"
                for file_path, description, created_time in files:
                    markdown_content += f"- **{Path(file_path).name}** ({created_time})\n"
                    markdown_content += f"  - 경로: `{file_path}`\n"
                    markdown_content += f"  - 설명: {description}\n\n"
            
            # 파일 저장
            output_file = self.conversation_dir / f"{session_id}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"📄 대화 마크다운 내보내기 완료: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"❌ 마크다운 내보내기 실패: {e}")
            return None
    
    def search_conversations(self, keyword, limit=10):
        """대화 내용 검색"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                SELECT DISTINCT m.session_id, cs.topic, cs.start_time, 
                       COUNT(m.id) as message_count,
                       GROUP_CONCAT(SUBSTR(m.content, 1, 100), ' | ') as preview
                FROM messages m
                JOIN conversation_sessions cs ON m.session_id = cs.session_id
                WHERE m.content LIKE ?
                GROUP BY m.session_id
                ORDER BY cs.start_time DESC
                LIMIT ?
                """, (f"%{keyword}%", limit))
                
                results = cursor.fetchall()
                
                print(f"🔍 '{keyword}' 검색 결과: {len(results)}개")
                for result in results:
                    session_id, topic, start_time, msg_count, preview = result
                    print(f"  📝 {session_id} - {topic} ({start_time})")
                    print(f"    메시지 {msg_count}개 | {preview[:100]}...")
                
                return results
                
        except Exception as e:
            print(f"❌ 검색 실패: {e}")
            return []
    
    def get_project_context(self, project_name):
        """프로젝트 컨텍스트 가져오기"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                SELECT context_data, last_session_id, updated_time
                FROM project_contexts 
                WHERE project_name = ?
                """, (project_name,))
                
                result = cursor.fetchone()
                if result:
                    context_data, last_session, updated_time = result
                    return {
                        'context': json.loads(context_data) if context_data else {},
                        'last_session': last_session,
                        'updated_time': updated_time
                    }
                else:
                    return None
                    
        except Exception as e:
            print(f"❌ 프로젝트 컨텍스트 가져오기 실패: {e}")
            return None
    
    def update_project_context(self, project_name, context_data, session_id):
        """프로젝트 컨텍스트 업데이트"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                INSERT OR REPLACE INTO project_contexts 
                (project_name, last_session_id, context_data, updated_time)
                VALUES (?, ?, ?, ?)
                """, (project_name, session_id, json.dumps(context_data), datetime.now()))
                conn.commit()
                
            print(f"💾 프로젝트 컨텍스트 업데이트: {project_name}")
            return True
            
        except Exception as e:
            print(f"❌ 프로젝트 컨텍스트 업데이트 실패: {e}")
            return False

def main():
    """메인 실행 함수"""
    manager = ClaudeConversationManager()
    
    # 현재 세션 생성
    session_id = manager.create_session("포토샵 + 카페24 자동화 개발")
    
    # 오늘 대화 내용 저장
    manager.save_message(session_id, "Human", "내 컴퓨터 C:\\Users\\8899y\\CUA-MASTER 접속 확인할 것이 있다.")
    manager.save_message(session_id, "Claude", "CUA-MASTER 프로젝트 구조를 분석하고 포토샵 자동화, 카페24 제어 시스템을 구축했습니다.")
    
    # 생성된 파일들 기록
    created_files = [
        ("C:/Users/8899y/CUA-MASTER/scripts/photoshop_automation.jsx", "포토샵 기본 자동화"),
        ("C:/Users/8899y/CUA-MASTER/scripts/batch_image_process.jsx", "이미지 일괄 처리"),
        ("C:/Users/8899y/CUA-MASTER/scripts/photoshop_controller.py", "Python 포토샵 컨트롤러"),
        ("C:/Users/8899y/CUA-MASTER/modules/cafe24/claude_direct_control.py", "카페24 직접 제어"),
        ("C:/Users/8899y/CUA-MASTER/modules/cafe24/claude_ui_control.py", "UI 자동화 제어"),
        ("C:/Users/8899y/CUA-MASTER/modules/cafe24/claude_detail_page_editor.py", "상세페이지 편집기"),
        ("C:/Users/8899y/CUA-MASTER/modules/cafe24/claude_ui_detail_editor.py", "UI 상세페이지 편집"),
        ("C:/Users/8899y/CUA-MASTER/modules/cafe24/START_DETAIL_PAGE_EDIT.bat", "원클릭 실행")
    ]
    
    for file_path, description in created_files:
        manager.save_created_file(session_id, file_path, description)
    
    # 프로젝트 컨텍스트 저장
    context_data = {
        "current_projects": ["포토샵 자동화", "카페24 제어"],
        "completed_tasks": [
            "CUA-MASTER 구조 분석",
            "포토샵 JSX 스크립트 생성",
            "카페24 제어 시스템 구축",
            "상세페이지 편집기 개발"
        ],
        "next_steps": [
            "대화 지속 저장 시스템 구현",
            "자동화 스크립트 실행 테스트",
            "프로젝트 컨텍스트 관리"
        ],
        "key_files": created_files
    }
    
    manager.update_project_context("CUA-MASTER", context_data, session_id)
    
    # 대화 마크다운으로 내보내기
    markdown_file = manager.export_conversation_to_markdown(session_id)
    
    print("\n" + "=" * 60)
    print("✅ Claude 대화 지속 저장 시스템 구축 완료")
    print("=" * 60)
    
    return manager

if __name__ == "__main__":
    main()

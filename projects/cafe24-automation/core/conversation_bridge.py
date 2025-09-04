"""
Claude 대화 연결 브릿지
새로운 Claude 세션에서 이전 대화 컨텍스트를 자동으로 로드하는 시스템
"""
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

class ConversationBridge:
    """대화 연결 브릿지"""
    
    def __init__(self):
        """초기화"""
        self.db_path = Path("C:/Users/8899y/CUA-MASTER/data/claude_conversations.db")
        self.context_file = Path("C:/Users/8899y/CUA-MASTER/data/current_context.json")
        
        print("🌉 Claude 대화 연결 브릿지 시작")
    
    def get_recent_context(self, days=7):
        """최근 대화 컨텍스트 가져오기"""
        try:
            if not self.db_path.exists():
                return None
            
            cutoff_date = datetime.now() - timedelta(days=days)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 최근 세션들 가져오기
                cursor.execute("""
                SELECT session_id, topic, start_time, summary, message_count, created_files
                FROM conversation_sessions 
                WHERE start_time > ?
                ORDER BY start_time DESC
                LIMIT 5
                """, (cutoff_date,))
                
                sessions = cursor.fetchall()
                
                if not sessions:
                    return None
                
                # 최근 메시지들 가져오기
                cursor.execute("""
                SELECT cs.topic, m.speaker, m.content, m.timestamp
                FROM messages m
                JOIN conversation_sessions cs ON m.session_id = cs.session_id
                WHERE m.timestamp > ?
                ORDER BY m.timestamp DESC
                LIMIT 20
                """, (cutoff_date,))
                
                recent_messages = cursor.fetchall()
                
                # 최근 생성된 파일들
                cursor.execute("""
                SELECT cf.file_path, cf.description, cf.created_time, cs.topic
                FROM created_files cf
                JOIN conversation_sessions cs ON cf.session_id = cs.session_id
                WHERE cf.created_time > ?
                ORDER BY cf.created_time DESC
                LIMIT 10
                """, (cutoff_date,))
                
                recent_files = cursor.fetchall()
            
            context = {
                "updated_time": datetime.now().isoformat(),
                "recent_sessions": [
                    {
                        "session_id": s[0],
                        "topic": s[1],
                        "start_time": s[2],
                        "summary": s[3],
                        "message_count": s[4],
                        "created_files": s[5]
                    } for s in sessions
                ],
                "recent_messages": [
                    {
                        "topic": m[0],
                        "speaker": m[1],
                        "content": m[2][:200] + "..." if len(m[2]) > 200 else m[2],
                        "timestamp": m[3]
                    } for m in recent_messages
                ],
                "recent_files": [
                    {
                        "file_path": f[0],
                        "description": f[1],
                        "created_time": f[2],
                        "topic": f[3]
                    } for f in recent_files
                ]
            }
            
            return context
            
        except Exception as e:
            print(f"❌ 컨텍스트 가져오기 실패: {e}")
            return None
    
    def save_current_context(self):
        """현재 컨텍스트 저장"""
        try:
            context = self.get_recent_context()
            if context:
                with open(self.context_file, 'w', encoding='utf-8') as f:
                    json.dump(context, f, ensure_ascii=False, indent=2)
                print(f"💾 현재 컨텍스트 저장 완료: {self.context_file}")
                return True
            return False
            
        except Exception as e:
            print(f"❌ 컨텍스트 저장 실패: {e}")
            return False
    
    def load_context_summary(self):
        """컨텍스트 요약 로드"""
        try:
            if not self.context_file.exists():
                return None
                
            with open(self.context_file, 'r', encoding='utf-8') as f:
                context = json.load(f)
            
            # 사용자 친화적인 요약 생성
            summary = self.generate_context_summary(context)
            return summary
            
        except Exception as e:
            print(f"❌ 컨텍스트 로드 실패: {e}")
            return None
    
    def generate_context_summary(self, context):
        """컨텍스트 요약 생성"""
        try:
            summary = "📋 **이전 대화 컨텍스트**\n\n"
            
            # 최근 세션 요약
            if context.get("recent_sessions"):
                summary += "## 🗂️ 최근 세션들\n"
                for session in context["recent_sessions"][:3]:
                    summary += f"- **{session['topic']}** ({session['start_time'][:10]})\n"
                    summary += f"  메시지 {session['message_count']}개, 파일 {session['created_files']}개 생성\n"
                summary += "\n"
            
            # 최근 생성 파일들
            if context.get("recent_files"):
                summary += "## 📁 최근 생성 파일들\n"
                for file_info in context["recent_files"][:5]:
                    file_name = Path(file_info["file_path"]).name
                    summary += f"- **{file_name}** - {file_info['description']}\n"
                summary += "\n"
            
            # 주요 키워드 추출
            keywords = self.extract_keywords(context)
            if keywords:
                summary += "## 🔑 주요 키워드\n"
                summary += f"{', '.join(keywords[:10])}\n\n"
            
            # 진행 중인 프로젝트
            projects = self.extract_projects(context)
            if projects:
                summary += "## 🚀 진행 중인 프로젝트\n"
                for project in projects[:3]:
                    summary += f"- {project}\n"
                summary += "\n"
            
            summary += "---\n"
            summary += "*대화를 계속 이어가세요. 이전 컨텍스트를 참고하여 답변드립니다.*"
            
            return summary
            
        except Exception as e:
            print(f"❌ 요약 생성 실패: {e}")
            return "이전 컨텍스트 로드 중 오류 발생"
    
    def extract_keywords(self, context):
        """키워드 추출"""
        try:
            keywords = set()
            
            # 세션 토픽에서 추출
            for session in context.get("recent_sessions", []):
                if session["topic"]:
                    keywords.update(session["topic"].split())
            
            # 파일 설명에서 추출
            for file_info in context.get("recent_files", []):
                if file_info["description"]:
                    keywords.update(file_info["description"].split())
            
            # 공통 단어 제거
            stop_words = {"및", "시스템", "파일", "스크립트", "자동화", "완료", "생성", "실행"}
            keywords = keywords - stop_words
            
            return list(keywords)
            
        except Exception as e:
            return []
    
    def extract_projects(self, context):
        """프로젝트 추출"""
        try:
            projects = set()
            
            for session in context.get("recent_sessions", []):
                topic = session.get("topic", "")
                if any(word in topic for word in ["포토샵", "카페24", "자동화", "시스템"]):
                    projects.add(topic)
            
            return list(projects)
            
        except Exception as e:
            return []
    
    def create_welcome_message(self):
        """환영 메시지 생성"""
        context_summary = self.load_context_summary()
        
        if context_summary:
            message = f"""안녕하세요! 👋 

{context_summary}

무엇을 도와드릴까요?"""
        else:
            message = """안녕하세요! 👋

새로운 대화를 시작합니다. 무엇을 도와드릴까요?"""
        
        return message

def main():
    """메인 실행"""
    bridge = ConversationBridge()
    
    print("🔄 컨텍스트 업데이트 중...")
    bridge.save_current_context()
    
    print("\n" + "=" * 60)
    welcome_message = bridge.create_welcome_message()
    print(welcome_message)
    print("=" * 60)

if __name__ == "__main__":
    main()

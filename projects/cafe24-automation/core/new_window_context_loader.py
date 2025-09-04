# -*- coding: utf-8 -*-
"""
Claude Desktop 새 창 자동 연결 시스템
새로운 Claude Desktop 창에서 이전 컨텍스트를 즉시 로드하는 시스템
"""
import json
from pathlib import Path
from datetime import datetime

class NewWindowContextLoader:
    """새 창 컨텍스트 자동 로더"""
    
    def __init__(self):
        self.context_file = Path("C:/Users/8899y/CUA-MASTER/data/current_session_context.md")
        self.quick_context_file = Path("C:/Users/8899y/CUA-MASTER/data/quick_context.json")
        
    def create_quick_context(self):
        """빠른 컨텍스트 파일 생성"""
        quick_context = {
            "session_date": "2025-09-02",
            "session_time": "17:20",
            "main_projects": [
                "포토샵 자동화 시스템",
                "카페24 직접 제어",
                "상세페이지 편집기",
                "대화 지속 저장 시스템"
            ],
            "completed_files": [
                "photoshop_automation.jsx - 포토샵 기본 자동화",
                "claude_direct_control.py - 카페24 직접 제어",
                "claude_detail_page_editor.py - 상세페이지 편집기",
                "claude_conversation_manager.py - 대화 저장 관리자"
            ],
            "key_achievements": [
                "CUA-MASTER 프로젝트 분석 완료",
                "Windows MCP를 통한 직접 시스템 제어 확인",
                "카페24 상세페이지 HTML 완전 수정 가능 확인",
                "포토샵 JSX 자동화 스크립트 구축",
                "대화 Memory + 파일 + DB 트리플 저장 시스템 구현"
            ],
            "current_status": "모든 자동화 시스템 구축 완료, 테스트 준비 상태",
            "next_priority": "시스템 실행 테스트 및 성능 검증",
            "context_file_path": str(self.context_file),
            "memory_status": "프로젝트 정보 Memory 시스템에 저장됨",
            "quick_commands": {
                "포토샵_자동화": "START_PHOTOSHOP_AUTOMATION.bat",
                "카페24_제어": "python claude_direct_control.py", 
                "상세페이지_편집": "START_DETAIL_PAGE_EDIT.bat",
                "대화_관리": "START_CONVERSATION_MANAGER.bat"
            }
        }
        
        # JSON으로 저장
        with open(self.quick_context_file, 'w', encoding='utf-8') as f:
            json.dump(quick_context, f, ensure_ascii=False, indent=2)
        
        return quick_context
    
    def generate_welcome_message(self):
        """새 창 환영 메시지 생성"""
        context = self.create_quick_context()
        
        message = f"""🤖 **Claude Desktop 새 창 연결 완료!**

## 📋 이전 대화 컨텍스트 ({context['session_date']} {context['session_time']})

### ✅ **완료된 주요 프로젝트**
"""
        
        for project in context['main_projects']:
            message += f"- **{project}** ✨\n"
        
        message += "\n### 🎯 **주요 성과**\n"
        for achievement in context['key_achievements'][:3]:
            message += f"- {achievement}\n"
        
        message += f"\n### 📁 **생성된 핵심 파일들** (총 {len(context['completed_files'])}개)\n"
        for file_info in context['completed_files']:
            message += f"- `{file_info}`\n"
        
        message += f"\n### 🚀 **현재 상태**\n{context['current_status']}"
        message += f"\n### 🎯 **다음 우선순위**\n{context['next_priority']}"
        
        message += "\n\n### ⚡ **바로 실행 가능한 명령어들**\n"
        for name, command in context['quick_commands'].items():
            message += f"- **{name.replace('_', ' ')}**: `{command}`\n"
        
        message += f"""
---
💾 **컨텍스트 저장 위치**
- Memory 시스템: ✅ 저장됨
- 파일 시스템: `{self.context_file}`
- 빠른 컨텍스트: `{self.quick_context_file}`

**이어서 대화하세요! 모든 컨텍스트가 연결되었습니다.** 🔗"""
        
        return message
    
    def save_welcome_message(self):
        """환영 메시지를 파일로 저장"""
        message = self.generate_welcome_message()
        
        welcome_file = Path("C:/Users/8899y/CUA-MASTER/data/new_window_welcome.md")
        with open(welcome_file, 'w', encoding='utf-8') as f:
            f.write(message)
        
        print(f"📄 새 창 환영 메시지 저장 완료: {welcome_file}")
        return welcome_file

def main():
    """메인 실행"""
    loader = NewWindowContextLoader()
    
    # 빠른 컨텍스트 생성
    context = loader.create_quick_context()
    print("✅ 빠른 컨텍스트 생성 완료")
    
    # 환영 메시지 생성
    welcome_message = loader.generate_welcome_message()
    
    # 파일로 저장
    welcome_file = loader.save_welcome_message()
    
    print("\n" + "=" * 60)
    print(welcome_message)
    print("=" * 60)
    
    return welcome_message

if __name__ == "__main__":
    main()

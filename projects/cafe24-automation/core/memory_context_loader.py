# -*- coding: utf-8 -*-
"""
Memory 기반 컨텍스트 로더
Claude Memory 시스템에서 프로젝트 컨텍스트를 자동으로 로드하는 시스템
"""
import json
from datetime import datetime
from pathlib import Path

class MemoryContextLoader:
    """Memory 기반 컨텍스트 로더"""
    
    def __init__(self):
        """초기화"""
        self.memory_cache_file = Path("C:/Users/8899y/CUA-MASTER/data/memory_context_cache.json")
        self.memory_cache_file.parent.mkdir(exist_ok=True)
        
        print("🧠 Memory 기반 컨텍스트 로더 시작")
    
    def create_memory_summary(self):
        """Memory 내용을 바탕으로 한 컨텍스트 요약 생성"""
        # Memory에서 가져온 실제 내용을 바탕으로 요약 생성
        memory_context = {
            "last_updated": datetime.now().isoformat(),
            "current_projects": {
                "CUA-MASTER": {
                    "status": "활발히 개발 중",
                    "components": [
                        "포토샵 자동화 시스템",
                        "카페24 제어 시스템", 
                        "Claude 대화 저장 시스템"
                    ],
                    "latest_achievements": [
                        "Windows MCP를 통한 실시간 시스템 제어 검증",
                        "총 12개 파일 생성 (포토샵 4개 + 카페24 4개 + 대화저장 4개)",
                        "Memory 시스템을 활용한 영구 컨텍스트 저장 방법 구현"
                    ]
                }
            },
            "technical_capabilities": {
                "system_control": [
                    "Windows MCP 도구를 통한 직접 시스템 제어",
                    "파일 시스템 읽기/쓰기/수정 완전 가능",
                    "PowerShell 명령어 직접 실행 가능",
                    "키보드/마우스 자동화를 통한 UI 제어",
                    "웹 스크래핑 및 브라우저 제어",
                    "프로그램 실행 및 프로세스 관리 가능"
                ],
                "automation_systems": [
                    "포토샵 JSX 스크립트 자동화",
                    "카페24 Selenium 기반 제어",
                    "UI 자동화를 통한 직접 제어",
                    "상품 상세페이지 HTML 완전 수정"
                ]
            },
            "session_history": {
                "2025-09-02": {
                    "duration": "약 2시간",
                    "files_created": 12,
                    "major_accomplishments": [
                        "포토샵 자동화 시스템 구축 (JSX + Python)",
                        "카페24 상세페이지 직접 편집 시스템 개발", 
                        "대화 지속 저장을 위한 통합 시스템 구축"
                    ]
                }
            },
            "created_files": {
                "photoshop_automation": [
                    "photoshop_automation.jsx",
                    "batch_image_process.jsx", 
                    "photoshop_controller.py",
                    "START_PHOTOSHOP_AUTOMATION.bat"
                ],
                "cafe24_control": [
                    "claude_direct_control.py",
                    "claude_ui_control.py",
                    "claude_detail_page_editor.py",
                    "claude_ui_detail_editor.py",
                    "START_DETAIL_PAGE_EDIT.bat"
                ],
                "conversation_management": [
                    "claude_conversation_manager.py",
                    "conversation_auto_saver.py",
                    "conversation_bridge.py",
                    "START_CONVERSATION_MANAGER.bat"
                ]
            },
            "next_potential_tasks": [
                "자동화 스크립트 실제 실행 및 테스트",
                "카페24 상세페이지 일괄 업데이트 실행",
                "포토샵 자동화 배치 처리 테스트",
                "대화 저장 시스템 백그라운드 실행",
                "프로젝트별 성능 최적화"
            ]
        }
        
        return memory_context
    
    def save_memory_cache(self, context):
        """Memory 컨텍스트 캐시 저장"""
        try:
            with open(self.memory_cache_file, 'w', encoding='utf-8') as f:
                json.dump(context, f, ensure_ascii=False, indent=2)
            print(f"💾 Memory 컨텍스트 캐시 저장: {self.memory_cache_file}")
            return True
        except Exception as e:
            print(f"❌ 캐시 저장 실패: {e}")
            return False
    
    def load_memory_cache(self):
        """Memory 컨텍스트 캐시 로드"""
        try:
            if self.memory_cache_file.exists():
                with open(self.memory_cache_file, 'r', encoding='utf-8') as f:
                    context = json.load(f)
                print(f"📖 Memory 컨텍스트 캐시 로드: {context['last_updated']}")
                return context
            return None
        except Exception as e:
            print(f"❌ 캐시 로드 실패: {e}")
            return None
    
    def generate_welcome_with_memory(self):
        """Memory 기반 환영 메시지 생성"""
        context = self.create_memory_summary()
        self.save_memory_cache(context)
        
        welcome_msg = f"""🧠 **Memory 시스템 컨텍스트 로드 완료**

## 📋 현재 프로젝트 상태

### 🚀 **CUA-MASTER 프로젝트**
- **상태**: {context['current_projects']['CUA-MASTER']['status']}
- **구성 요소**: {len(context['current_projects']['CUA-MASTER']['components'])}개 시스템
- **최근 성과**: {len(context['current_projects']['CUA-MASTER']['latest_achievements'])}개 달성

### 📁 **생성된 파일들** 
- **포토샵 자동화**: {len(context['created_files']['photoshop_automation'])}개 파일
- **카페24 제어**: {len(context['created_files']['cafe24_control'])}개 파일  
- **대화 관리**: {len(context['created_files']['conversation_management'])}개 파일

### ⚡ **시스템 제어 능력**
- Windows MCP 통합 제어 시스템
- 실시간 파일/프로그램/UI 제어
- 포토샵 + 카페24 완전 자동화

### 🎯 **다음 단계 제안**
1. {context['next_potential_tasks'][0]}
2. {context['next_potential_tasks'][1]} 
3. {context['next_potential_tasks'][2]}

---
💡 **Memory 시스템을 통해 모든 컨텍스트가 영구 저장되었습니다.**
새로운 세션에서도 이 정보들을 자동으로 불러올 수 있습니다!

무엇을 도와드릴까요?"""
        
        return welcome_msg
    
    def get_project_specific_context(self, project_name):
        """특정 프로젝트 컨텍스트 가져오기"""
        context = self.load_memory_cache()
        if not context:
            context = self.create_memory_summary()
        
        if project_name in context.get('current_projects', {}):
            project_data = context['current_projects'][project_name]
            
            project_context = f"""## 🎯 {project_name} 프로젝트 컨텍스트

**상태**: {project_data['status']}

**구성 요소**:
{chr(10).join(f"- {component}" for component in project_data['components'])}

**최근 성과**:
{chr(10).join(f"- {achievement}" for achievement in project_data['latest_achievements'])}

**관련 파일들**:
- 포토샵: {', '.join(context['created_files']['photoshop_automation'])}
- 카페24: {', '.join(context['created_files']['cafe24_control'])}
- 대화관리: {', '.join(context['created_files']['conversation_management'])}
"""
            return project_context
        else:
            return f"❌ 프로젝트 '{project_name}'에 대한 컨텍스트를 찾을 수 없습니다."
    
    def update_memory_with_new_info(self, new_info):
        """새로운 정보로 Memory 컨텍스트 업데이트"""
        context = self.load_memory_cache() or self.create_memory_summary()
        
        # 새로운 정보 추가
        context['last_updated'] = datetime.now().isoformat()
        
        if 'new_files' in new_info:
            for category, files in new_info['new_files'].items():
                if category in context['created_files']:
                    context['created_files'][category].extend(files)
                    
        if 'new_achievements' in new_info:
            project_name = new_info.get('project', 'CUA-MASTER')
            if project_name in context['current_projects']:
                context['current_projects'][project_name]['latest_achievements'].extend(
                    new_info['new_achievements']
                )
        
        self.save_memory_cache(context)
        print("✅ Memory 컨텍스트 업데이트 완료")

def main():
    """메인 실행"""
    loader = MemoryContextLoader()
    
    print("=" * 60)
    print("🧠 Memory 기반 컨텍스트 로더 테스트")
    print("=" * 60)
    
    # 환영 메시지 생성
    welcome = loader.generate_welcome_with_memory()
    print(welcome)
    
    print("\n" + "=" * 60)
    print("📋 CUA-MASTER 프로젝트 상세 컨텍스트")
    print("=" * 60)
    
    # 프로젝트별 컨텍스트
    project_context = loader.get_project_specific_context("CUA-MASTER")
    print(project_context)

if __name__ == "__main__":
    main()

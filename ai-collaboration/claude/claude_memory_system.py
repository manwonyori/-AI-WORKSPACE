"""
Claude Memory System - GitHub 기반 지속적 메모리 관리
대화 기억, 파일 관리, 명령어 최적화 통합 시스템
"""

import json
import os
import git
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import hashlib

class ClaudeMemorySystem:
    """Claude의 3대 문제 해결 시스템"""
    
    def __init__(self):
        self.base_dir = Path(r"C:\Users\8899y")
        self.memory_dir = self.base_dir / ".claude_memory"
        self.memory_dir.mkdir(exist_ok=True)
        
        # 메모리 파일들
        self.context_file = self.memory_dir / "CONTEXT.json"
        self.files_db = self.memory_dir / "FILES_DB.json"
        self.commands_db = self.memory_dir / "COMMANDS_DB.json"
        
        # Git 초기화 (있으면 사용, 없으면 생성)
        try:
            self.repo = git.Repo(self.base_dir)
        except:
            self.repo = None
            print("[경고] Git 저장소가 없습니다. 로컬 파일로만 작동합니다.")
        
        self.load_memory()
    
    def load_memory(self):
        """기존 메모리 로드"""
        self.context = self._load_json(self.context_file, {})
        self.files = self._load_json(self.files_db, {})
        self.commands = self._load_json(self.commands_db, {})
    
    def _load_json(self, file_path: Path, default=None):
        """JSON 파일 안전하게 로드"""
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return default if default is not None else {}
        return default if default is not None else {}
    
    def _save_json(self, file_path: Path, data):
        """JSON 파일 저장"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 1. 대화 기억 관리
    def remember_conversation(self, topic: str, content: str, decision: str = None):
        """대화 내용을 기억"""
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if topic not in self.context:
            self.context[topic] = []
        
        self.context[topic].append({
            "session": session_id,
            "timestamp": datetime.now().isoformat(),
            "content": content,
            "decision": decision
        })
        
        self._save_json(self.context_file, self.context)
        print(f"[기억됨] {topic}: {content[:50]}...")
        
        # Git에 커밋
        if self.repo:
            self._git_commit(f"Memory: {topic}")
    
    def recall_conversation(self, topic: str = None) -> List[Dict]:
        """과거 대화 불러오기"""
        if topic:
            return self.context.get(topic, [])
        return self.context
    
    # 2. 파일 관리 체계
    def check_before_create(self, filename: str, purpose: str) -> Dict:
        """파일 생성 전 체크"""
        file_hash = hashlib.md5(purpose.encode()).hexdigest()[:8]
        
        # 비슷한 목적의 파일이 있는지 확인
        for existing_file, info in self.files.items():
            if info.get('purpose') == purpose:
                return {
                    "should_create": False,
                    "existing_file": existing_file,
                    "message": f"이미 같은 목적의 파일이 있습니다: {existing_file}"
                }
            
            # 파일명이 너무 비슷한지 체크
            if self._similarity(filename, existing_file) > 0.8:
                return {
                    "should_create": False,
                    "existing_file": existing_file,
                    "message": f"비슷한 파일이 이미 있습니다: {existing_file}"
                }
        
        # 새 파일 생성 가능
        suggested_name = f"{Path(filename).stem}_{file_hash}{Path(filename).suffix}"
        
        return {
            "should_create": True,
            "suggested_name": suggested_name,
            "message": f"새 파일 생성 가능: {suggested_name}"
        }
    
    def register_file(self, filepath: str, purpose: str, category: str = "general"):
        """생성된 파일 등록"""
        self.files[filepath] = {
            "created": datetime.now().isoformat(),
            "purpose": purpose,
            "category": category,
            "last_modified": datetime.now().isoformat()
        }
        
        self._save_json(self.files_db, self.files)
        print(f"[파일 등록] {filepath} - {purpose}")
    
    def find_final_file(self, category: str) -> Optional[str]:
        """최종 파일 찾기"""
        candidates = []
        for filepath, info in self.files.items():
            if info.get('category') == category:
                candidates.append((filepath, info['last_modified']))
        
        if candidates:
            # 가장 최근 파일 반환
            candidates.sort(key=lambda x: x[1], reverse=True)
            return candidates[0][0]
        return None
    
    # 3. 명령어 최적화
    def suggest_command(self, task: str) -> Optional[str]:
        """작업에 최적화된 명령어 제안"""
        # 비슷한 작업 찾기
        best_match = None
        best_score = 0
        
        for past_task, info in self.commands.items():
            score = self._similarity(task, past_task)
            if score > best_score and info.get('success'):
                best_score = score
                best_match = info['command']
        
        if best_match and best_score > 0.7:
            print(f"[제안] 유사 작업 발견 (유사도: {best_score:.1%})")
            return best_match
        
        return None
    
    def record_command(self, task: str, command: str, success: bool, result: str = None):
        """실행한 명령어 기록"""
        self.commands[task] = {
            "command": command,
            "success": success,
            "result": result,
            "timestamp": datetime.now().isoformat(),
            "execution_count": self.commands.get(task, {}).get('execution_count', 0) + 1
        }
        
        self._save_json(self.commands_db, self.commands)
        status = "성공" if success else "실패"
        print(f"[명령어 기록] {task}: {status}")
    
    def get_best_practices(self) -> List[Dict]:
        """성공한 명령어들 반환"""
        successful = []
        for task, info in self.commands.items():
            if info.get('success'):
                successful.append({
                    "task": task,
                    "command": info['command'],
                    "count": info.get('execution_count', 1)
                })
        
        # 실행 횟수로 정렬
        successful.sort(key=lambda x: x['count'], reverse=True)
        return successful[:10]  # Top 10
    
    # 유틸리티 함수들
    def _similarity(self, str1: str, str2: str) -> float:
        """두 문자열의 유사도 계산 (0~1)"""
        if not str1 or not str2:
            return 0.0
        
        # 간단한 유사도 계산
        set1 = set(str1.lower().split())
        set2 = set(str2.lower().split())
        
        if not set1 or not set2:
            return 0.0
            
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _git_commit(self, message: str):
        """Git 자동 커밋"""
        if self.repo:
            try:
                self.repo.git.add(str(self.memory_dir))
                self.repo.index.commit(f"Claude: {message}")
                print(f"[Git] 커밋됨: {message}")
            except:
                pass  # Git 오류는 무시
    
    def status(self):
        """현재 상태 출력"""
        print("\n" + "="*60)
        print("Claude Memory System Status")
        print("="*60)
        print(f"대화 토픽: {len(self.context)}개")
        print(f"관리 파일: {len(self.files)}개")
        print(f"학습 명령어: {len(self.commands)}개")
        
        # 최근 대화
        if self.context:
            recent_topic = list(self.context.keys())[-1]
            recent_conv = self.context[recent_topic][-1]
            print(f"\n최근 대화: {recent_topic}")
            print(f"  시간: {recent_conv['timestamp']}")
            print(f"  내용: {recent_conv['content'][:50]}...")
        
        # 최종 파일
        for category in ['final', 'output', 'report']:
            final = self.find_final_file(category)
            if final:
                print(f"\n{category} 최종 파일: {final}")
        
        # 베스트 명령어
        best = self.get_best_practices()
        if best:
            print("\n자주 사용하는 명령어:")
            for item in best[:3]:
                print(f"  - {item['task']}: {item['command'][:50]}... ({item['count']}회)")
        
        print("="*60)

# 전역 인스턴스 생성
memory_system = ClaudeMemorySystem()

def demo():
    """시스템 데모"""
    print("Claude Memory System 시작...")
    
    # 1. 대화 기억 테스트
    memory_system.remember_conversation(
        topic="claude_bridge",
        content="Claude Bridge 시스템 분석 및 개선 작업",
        decision="GitHub 기반 메모리 시스템 구축"
    )
    
    # 2. 파일 생성 체크
    check = memory_system.check_before_create(
        "test_system.py",
        "시스템 테스트 스크립트"
    )
    print(f"\n파일 생성 체크: {check['message']}")
    
    # 3. 명령어 기록
    memory_system.record_command(
        task="Python 스크립트 실행",
        command="python test_system.py",
        success=True,
        result="정상 실행됨"
    )
    
    # 4. 상태 출력
    memory_system.status()

if __name__ == "__main__":
    demo()
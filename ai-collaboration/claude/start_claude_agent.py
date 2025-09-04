"""
Claude Code Agent 실행 스크립트
CUA 시스템과 Claude Code Bridge를 통합 실행
"""

import sys
import os
import time
import json
from pathlib import Path
from datetime import datetime

# CUA-MASTER 경로 추가
sys.path.insert(0, r'C:\Users\8899y\CUA-MASTER')

from core.claude_code_bridge import ClaudeCodeBridge
from core.agent_enhanced import EnhancedComputerUseAgent

def main():
    print("="*60)
    print("Claude Code Agent 시스템 시작")
    print("="*60)
    
    # Claude Code Bridge 초기화
    bridge = ClaudeCodeBridge()
    print(f"[OK] Claude Code Bridge 초기화 완료")
    print(f"  작업 디렉토리: {bridge.workspace}")
    
    # CUA Agent 초기화
    agent = EnhancedComputerUseAgent()
    print(f"[OK] CUA Agent 초기화 완료")
    
    # 모니터링 시작
    print("\n모니터링 시작...")
    print("Claude Code Bridge가 요청을 대기 중입니다.")
    print("-"*60)
    
    # 테스트 요청 생성
    test_task = {
        "task": "시스템 상태 확인",
        "description": "현재 CUA 시스템의 상태를 확인하고 보고합니다.",
        "priority": "high"
    }
    
    request_id = f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    request_file = bridge.requests_dir / f"{request_id}.json"
    
    request_data = {
        "id": request_id,
        "timestamp": datetime.now().isoformat(),
        "type": "system_check",
        "task": test_task["task"],
        "context": {
            "description": test_task["description"],
            "priority": test_task["priority"],
            "agent": "CUA Agent Enhanced",
            "bridge": "Claude Code Bridge v1.0"
        }
    }
    
    # 요청 파일 생성
    with open(request_file, 'w', encoding='utf-8') as f:
        json.dump(request_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] 테스트 요청 생성: {request_id}")
    print(f"  요청 파일: {request_file}")
    
    # 대시보드 정보 표시
    print("\n" + "="*60)
    print("Claude Code Agent 대시보드")
    print("="*60)
    print(f"요청 디렉토리: {bridge.requests_dir}")
    print(f"응답 디렉토리: {bridge.responses_dir}")
    print(f"대기 중인 요청: {bridge.workspace / 'pending_request.txt'}")
    
    print("\n사용 가능한 명령:")
    print("1. 새 요청 생성")
    print("2. 응답 확인")
    print("3. 시스템 상태")
    print("4. 모니터링 시작")
    print("0. 종료")
    
    while True:
        try:
            # 요청 파일 모니터링
            pending_file = bridge.workspace / "pending_request.txt"
            if pending_file.exists():
                with open(pending_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        print(f"\n[대기 중] {content}")
            
            # 피드백 파일 체크
            feedback_dir = bridge.workspace / "feedback"
            if feedback_dir.exists():
                for feedback_file in feedback_dir.glob("*.json"):
                    print(f"\n[피드백] {feedback_file.name}")
                    with open(feedback_file, 'r', encoding='utf-8') as f:
                        feedback = json.load(f)
                        print(f"  상태: {feedback.get('status', 'unknown')}")
                        print(f"  메시지: {feedback.get('message', '')}")
            
            time.sleep(2)  # 2초마다 체크
            
        except KeyboardInterrupt:
            print("\n\n모니터링 중지...")
            break
        except Exception as e:
            print(f"\n오류 발생: {e}")
            time.sleep(5)
    
    print("\nClaude Code Agent 종료")

if __name__ == "__main__":
    main()
"""
Claude Code Bridge - Claude Code를 백그라운드에서 활용하는 브릿지
API 키 없이 Claude Code(정액제)를 통해 AI 기능 활용
"""
import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import subprocess

logger = logging.getLogger(__name__)


class ClaudeCodeBridge:
    """
    Claude Code와 CUA Agent를 연결하는 브릿지
    파일 시스템을 통해 통신하며 Claude Code의 응답을 활용
    """
    
    def __init__(self, workspace_dir: str = None):
        """브릿지 초기화"""
        if workspace_dir:
            self.workspace = Path(workspace_dir)
        else:
            self.workspace = Path(r"C:\Users\8899y\CUA-MASTER\data\claude_bridge")
        
        # 작업 디렉토리 생성
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.requests_dir = self.workspace / "requests"
        self.responses_dir = self.workspace / "responses"
        self.requests_dir.mkdir(exist_ok=True)
        self.responses_dir.mkdir(exist_ok=True)
        
        logger.info(f"Claude Code Bridge initialized at {self.workspace}")
    
    def request_action_plan(self, task: str, context: Dict = None) -> Optional[List[Dict]]:
        """
        Claude Code에 액션 계획을 요청
        
        Args:
            task: 수행할 작업 설명
            context: 추가 컨텍스트 정보
        
        Returns:
            계획된 액션 리스트
        """
        request_id = f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        request_file = self.requests_dir / f"{request_id}.json"
        response_file = self.responses_dir / f"{request_id}.json"
        
        # 요청 생성
        request_data = {
            "id": request_id,
            "timestamp": datetime.now().isoformat(),
            "type": "action_plan",
            "task": task,
            "context": context or {},
            "instructions": """
아래 작업을 수행하기 위한 구체적인 액션 계획을 JSON 형식으로 작성해주세요.
각 액션은 다음 형식을 따라야 합니다:
{
    "type": "screenshot|click|type|key|scroll|drag|wait|find|read|execute",
    "parameters": {...},
    "description": "액션 설명"
}

사용 가능한 액션 타입:
- screenshot: 화면 캡처
- click: 마우스 클릭 (x, y 좌표 또는 element)
- type: 텍스트 입력
- key: 키보드 키 입력 (Enter, Tab, Ctrl+C 등)
- scroll: 스크롤 (direction, amount)
- drag: 드래그 (from_x, from_y, to_x, to_y)
- wait: 대기 (seconds)
- find: 화면에서 요소 찾기 (query)
- read: 화면 텍스트 읽기
- execute: 명령 실행 (command)
            """
        }
        
        # 요청 파일 작성
        with open(request_file, 'w', encoding='utf-8') as f:
            json.dump(request_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Request created: {request_file}")
        
        # Claude Code가 처리할 수 있도록 알림 파일 생성
        notification_file = self.workspace / "pending_request.txt"
        with open(notification_file, 'w', encoding='utf-8') as f:
            f.write(f"{request_id}\n{task}")
        
        # 응답 대기 (최대 30초)
        max_wait = 30
        check_interval = 0.5
        waited = 0
        
        while waited < max_wait:
            if response_file.exists():
                try:
                    with open(response_file, 'r', encoding='utf-8') as f:
                        response = json.load(f)
                    
                    # 응답 파일 정리
                    response_file.unlink()
                    if notification_file.exists():
                        notification_file.unlink()
                    
                    return response.get('actions', [])
                    
                except Exception as e:
                    logger.error(f"Error reading response: {e}")
                    return None
            
            time.sleep(check_interval)
            waited += check_interval
        
        logger.warning(f"Timeout waiting for response from Claude Code")
        return None
    
    def analyze_screen(self, screenshot_path: str, instruction: str) -> Optional[Dict]:
        """
        Claude Code를 통해 스크린샷 분석
        
        Args:
            screenshot_path: 스크린샷 파일 경로
            instruction: 분석 지시사항
        
        Returns:
            분석 결과
        """
        request_id = f"analyze_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        request_file = self.requests_dir / f"{request_id}.json"
        response_file = self.responses_dir / f"{request_id}.json"
        
        request_data = {
            "id": request_id,
            "timestamp": datetime.now().isoformat(),
            "type": "screen_analysis",
            "screenshot": screenshot_path,
            "instruction": instruction
        }
        
        with open(request_file, 'w', encoding='utf-8') as f:
            json.dump(request_data, f, ensure_ascii=False, indent=2)
        
        # 알림 생성
        notification_file = self.workspace / "pending_analysis.txt"
        with open(notification_file, 'w', encoding='utf-8') as f:
            f.write(f"{request_id}\n{screenshot_path}\n{instruction}")
        
        # 응답 대기
        max_wait = 20
        check_interval = 0.5
        waited = 0
        
        while waited < max_wait:
            if response_file.exists():
                try:
                    with open(response_file, 'r', encoding='utf-8') as f:
                        response = json.load(f)
                    
                    response_file.unlink()
                    if notification_file.exists():
                        notification_file.unlink()
                    
                    return response.get('analysis', {})
                    
                except Exception as e:
                    logger.error(f"Error reading analysis response: {e}")
                    return None
            
            time.sleep(check_interval)
            waited += check_interval
        
        return None
    
    def send_feedback(self, action_id: str, result: Dict) -> None:
        """
        실행 결과를 Claude Code에 피드백
        
        Args:
            action_id: 액션 ID
            result: 실행 결과
        """
        feedback_file = self.workspace / "feedback" / f"{action_id}.json"
        feedback_file.parent.mkdir(exist_ok=True)
        
        feedback_data = {
            "action_id": action_id,
            "timestamp": datetime.now().isoformat(),
            "result": result
        }
        
        with open(feedback_file, 'w', encoding='utf-8') as f:
            json.dump(feedback_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Feedback sent for action {action_id}")


class ClaudeCodeProcessor:
    """
    Claude Code 측에서 요청을 처리하는 프로세서
    별도 스크립트나 Claude Code 내에서 실행
    """
    
    def __init__(self, workspace_dir: str = None):
        """프로세서 초기화"""
        if workspace_dir:
            self.workspace = Path(workspace_dir)
        else:
            self.workspace = Path(r"C:\Users\8899y\CUA-MASTER\data\claude_bridge")
        
        self.requests_dir = self.workspace / "requests"
        self.responses_dir = self.workspace / "responses"
        
    def process_pending_requests(self):
        """
        대기 중인 요청 처리
        Claude Code에서 이 메서드를 주기적으로 호출
        """
        # pending_request.txt 확인
        notification_file = self.workspace / "pending_request.txt"
        if notification_file.exists():
            with open(notification_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if lines:
                request_id = lines[0].strip()
                task = lines[1].strip() if len(lines) > 1 else ""
                
                # 요청 파일 읽기
                request_file = self.requests_dir / f"{request_id}.json"
                if request_file.exists():
                    with open(request_file, 'r', encoding='utf-8') as f:
                        request_data = json.load(f)
                    
                    # Claude Code가 처리할 내용
                    print(f"\n[Claude Code Bridge Request]")
                    print(f"Task: {task}")
                    print(f"Request ID: {request_id}")
                    print("\n이 작업을 위한 액션 계획을 작성해주세요.")
                    
                    # 여기서 Claude Code가 응답을 생성하도록 유도
                    # 실제로는 Claude Code가 직접 응답 파일을 작성
                    
                    return request_data
        
        # pending_analysis.txt 확인
        analysis_notification = self.workspace / "pending_analysis.txt"
        if analysis_notification.exists():
            with open(analysis_notification, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if lines:
                request_id = lines[0].strip()
                screenshot = lines[1].strip() if len(lines) > 1 else ""
                instruction = lines[2].strip() if len(lines) > 2 else ""
                
                print(f"\n[Claude Code Bridge Analysis Request]")
                print(f"Screenshot: {screenshot}")
                print(f"Instruction: {instruction}")
                print(f"Request ID: {request_id}")
                
                return {
                    "type": "analysis",
                    "id": request_id,
                    "screenshot": screenshot,
                    "instruction": instruction
                }
        
        return None
    
    def save_response(self, request_id: str, response_data: Dict):
        """
        Claude Code의 응답 저장
        
        Args:
            request_id: 요청 ID
            response_data: 응답 데이터
        """
        response_file = self.responses_dir / f"{request_id}.json"
        
        with open(response_file, 'w', encoding='utf-8') as f:
            json.dump(response_data, f, ensure_ascii=False, indent=2)
        
        print(f"Response saved: {response_file}")


# 통합 헬퍼 함수
def setup_claude_code_integration():
    """Claude Code 통합 설정"""
    bridge = ClaudeCodeBridge()
    
    # 모니터링 스크립트 생성
    monitor_script = Path(r"C:\Users\8899y\CUA-MASTER\monitor_claude_bridge.py")
    
    script_content = '''"""
Claude Code Bridge 모니터 - Claude Code에서 실행
"""
import sys
import time
sys.path.insert(0, r'C:\\Users\\8899y\\CUA-MASTER')

from core.claude_code_bridge import ClaudeCodeProcessor

processor = ClaudeCodeProcessor()

print("Claude Code Bridge Monitor Started")
print("Waiting for requests...")

while True:
    request = processor.process_pending_requests()
    if request:
        print(f"\\nNew request received: {request.get('id', 'unknown')}")
        print("Please process this request and save the response.")
    
    time.sleep(1)  # 1초마다 체크
'''
    
    with open(monitor_script, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"Claude Code Bridge 설정 완료!")
    print(f"작업 디렉토리: {bridge.workspace}")
    print(f"모니터 스크립트: {monitor_script}")
    print("\n사용 방법:")
    print("1. CUA Agent에서 bridge.request_action_plan() 호출")
    print("2. Claude Code에서 monitor_claude_bridge.py 실행")
    print("3. Claude Code가 요청을 처리하고 응답 생성")
    print("4. CUA Agent가 응답을 받아 실행")
    
    return bridge


if __name__ == "__main__":
    # 설정 실행
    bridge = setup_claude_code_integration()
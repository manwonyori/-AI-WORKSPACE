"""
Claude Bridge 모니터링 시스템
Claude Code Bridge와 CUA 시스템 간의 통신을 모니터링하고 관리
"""

import json
import time
import os
from pathlib import Path
from datetime import datetime
import threading
from typing import Dict, Any, Optional

class ClaudeBridgeMonitor:
    def __init__(self):
        self.bridge_dir = Path(r"C:\Users\8899y\claude_bridge")
        self.cua_bridge_dir = Path(r"C:\Users\8899y\CUA-MASTER\data\claude_bridge")
        self.monitoring = False
        
        # 디렉토리 생성
        self.bridge_dir.mkdir(exist_ok=True)
        (self.bridge_dir / "requests").mkdir(exist_ok=True)
        (self.bridge_dir / "responses").mkdir(exist_ok=True)
        (self.bridge_dir / "notifications").mkdir(exist_ok=True)
        
        print(f"[초기화] Claude Bridge Monitor")
        print(f"  메인 디렉토리: {self.bridge_dir}")
        print(f"  CUA 브릿지: {self.cua_bridge_dir}")
    
    def check_requests(self):
        """새로운 요청 확인"""
        requests = []
        
        # claude_bridge 요청 확인
        req_dir = self.bridge_dir / "requests"
        if req_dir.exists():
            for req_file in req_dir.glob("*.json"):
                try:
                    with open(req_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        requests.append({
                            'source': 'claude_bridge',
                            'file': req_file.name,
                            'data': data
                        })
                except Exception as e:
                    print(f"[오류] 요청 파일 읽기 실패: {req_file} - {e}")
        
        # CUA bridge 요청 확인
        if self.cua_bridge_dir.exists():
            cua_req_dir = self.cua_bridge_dir / "requests"
            if cua_req_dir.exists():
                for req_file in cua_req_dir.glob("*.json"):
                    try:
                        with open(req_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            requests.append({
                                'source': 'cua_bridge',
                                'file': req_file.name,
                                'data': data
                            })
                    except Exception as e:
                        print(f"[오류] CUA 요청 파일 읽기 실패: {req_file} - {e}")
        
        return requests
    
    def check_notifications(self):
        """알림 확인"""
        notifications = []
        
        notif_dir = self.bridge_dir / "notifications"
        if notif_dir.exists():
            for notif_file in notif_dir.glob("*.json"):
                try:
                    with open(notif_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        notifications.append({
                            'file': notif_file.name,
                            'data': data
                        })
                except Exception as e:
                    print(f"[오류] 알림 파일 읽기 실패: {notif_file} - {e}")
        
        # 루트 디렉토리의 notification 파일도 확인
        for notif_file in self.bridge_dir.glob("notification_*.json"):
            try:
                with open(notif_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    notifications.append({
                        'file': notif_file.name,
                        'data': data
                    })
            except Exception as e:
                print(f"[오류] 알림 파일 읽기 실패: {notif_file} - {e}")
        
        return notifications
    
    def display_status(self):
        """현재 상태 표시"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 70)
        print("Claude Bridge Monitor - 실시간 모니터링")
        print("=" * 70)
        print(f"현재 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 70)
        
        # 요청 확인
        requests = self.check_requests()
        print(f"\n[요청] 대기 중인 요청: {len(requests)}개")
        for req in requests[:5]:  # 최근 5개만 표시
            print(f"  [{req['source']}] {req['file']}")
            if 'task' in req['data']:
                print(f"    작업: {req['data']['task']}")
            if 'type' in req['data']:
                print(f"    타입: {req['data']['type']}")
        
        # 알림 확인
        notifications = self.check_notifications()
        print(f"\n[알림] 알림: {len(notifications)}개")
        for notif in notifications[:3]:  # 최근 3개만 표시
            print(f"  {notif['file']}")
            if 'message' in notif['data']:
                print(f"    메시지: {notif['data']['message']}")
        
        # 디렉토리 상태
        print(f"\n[디렉토리] 상태:")
        dirs_to_check = [
            (self.bridge_dir, "메인 브릿지"),
            (self.bridge_dir / "requests", "요청"),
            (self.bridge_dir / "responses", "응답"),
            (self.cua_bridge_dir, "CUA 브릿지")
        ]
        
        for dir_path, name in dirs_to_check:
            if dir_path.exists():
                file_count = len(list(dir_path.glob("*.json")))
                print(f"  [OK] {name}: {file_count}개 파일")
            else:
                print(f"  [X] {name}: 존재하지 않음")
        
        print("\n" + "-" * 70)
        print("모니터링 중... (Ctrl+C로 종료)")
    
    def create_test_request(self):
        """테스트 요청 생성"""
        request_id = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        request_data = {
            "id": request_id,
            "timestamp": datetime.now().isoformat(),
            "type": "test",
            "task": "시스템 상태 확인",
            "context": {
                "description": "Claude Bridge 연결 테스트",
                "priority": "low"
            }
        }
        
        request_file = self.bridge_dir / "requests" / f"{request_id}.json"
        with open(request_file, 'w', encoding='utf-8') as f:
            json.dump(request_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n[OK] 테스트 요청 생성: {request_id}")
        return request_id
    
    def start_monitoring(self):
        """모니터링 시작"""
        self.monitoring = True
        
        while self.monitoring:
            try:
                self.display_status()
                time.sleep(2)  # 2초마다 업데이트
            except KeyboardInterrupt:
                print("\n\n모니터링 중지...")
                self.monitoring = False
                break
            except Exception as e:
                print(f"\n오류 발생: {e}")
                time.sleep(5)
    
    def interactive_menu(self):
        """대화형 메뉴"""
        while True:
            print("\n" + "=" * 50)
            print("Claude Bridge Monitor - 메뉴")
            print("=" * 50)
            print("1. 실시간 모니터링 시작")
            print("2. 현재 상태 확인")
            print("3. 테스트 요청 생성")
            print("4. 요청 목록 보기")
            print("5. 알림 목록 보기")
            print("0. 종료")
            print("-" * 50)
            
            choice = input("선택: ").strip()
            
            if choice == "1":
                self.start_monitoring()
            elif choice == "2":
                self.display_status()
            elif choice == "3":
                self.create_test_request()
            elif choice == "4":
                requests = self.check_requests()
                print(f"\n요청 목록 ({len(requests)}개):")
                for req in requests:
                    print(f"  - [{req['source']}] {req['file']}")
            elif choice == "5":
                notifications = self.check_notifications()
                print(f"\n알림 목록 ({len(notifications)}개):")
                for notif in notifications:
                    print(f"  - {notif['file']}")
            elif choice == "0":
                print("종료합니다.")
                break
            else:
                print("잘못된 선택입니다.")

def main():
    monitor = ClaudeBridgeMonitor()
    
    # 시작 옵션
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "--monitor":
            monitor.start_monitoring()
        elif sys.argv[1] == "--test":
            monitor.create_test_request()
        elif sys.argv[1] == "--status":
            monitor.display_status()
    else:
        # 기본: 대화형 메뉴
        monitor.interactive_menu()

if __name__ == "__main__":
    main()
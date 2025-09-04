"""
CUA Agent 백그라운드 자동화 스케줄러
주기적으로 카페24 작업을 자동 실행
"""

import time
import json
import schedule
import threading
from datetime import datetime
from pathlib import Path
import subprocess
import sys

class CUABackgroundScheduler:
    """백그라운드 자동화 스케줄러"""
    
    def __init__(self):
        self.base_dir = Path("C:/Users/8899y/CUA-MASTER")
        self.log_dir = self.base_dir / "logs"
        self.log_dir.mkdir(exist_ok=True)
        self.config_file = self.base_dir / "scheduler_config.json"
        self.load_config()
        self.running = True
        
    def load_config(self):
        """설정 로드"""
        default_config = {
            "tasks": [
                {
                    "name": "cafe24_learning",
                    "script": "modules/cafe24/cafe24_unified_learner.py",
                    "schedule": "daily",
                    "time": "10:00",
                    "enabled": True
                },
                {
                    "name": "cafe24_price_update",
                    "script": "modules/cafe24/price_updater.py",
                    "schedule": "hourly",
                    "enabled": False
                },
                {
                    "name": "system_cleanup",
                    "script": "scripts/cleanup.py",
                    "schedule": "weekly",
                    "day": "sunday",
                    "time": "03:00",
                    "enabled": True
                }
            ],
            "monitoring": {
                "cpu_limit": 50,
                "memory_limit": 70,
                "check_interval": 60
            }
        }
        
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.save_config()
            
    def save_config(self):
        """설정 저장"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def log(self, message, level="INFO"):
        """로그 기록"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"
        print(log_message)
        
        # 파일에도 기록
        log_file = self.log_dir / f"scheduler_{datetime.now().strftime('%Y%m%d')}.log"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
    
    def check_system_resources(self):
        """시스템 리소스 체크"""
        try:
            import psutil
            
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            
            if cpu_percent > self.config['monitoring']['cpu_limit']:
                self.log(f"CPU 사용률 높음: {cpu_percent}%", "WARNING")
                return False
                
            if memory_percent > self.config['monitoring']['memory_limit']:
                self.log(f"메모리 사용률 높음: {memory_percent}%", "WARNING")
                return False
                
            return True
            
        except ImportError:
            # psutil이 없으면 체크 건너뛰기
            return True
    
    def run_task(self, task):
        """작업 실행"""
        if not task.get('enabled', False):
            return
            
        self.log(f"작업 시작: {task['name']}")
        
        # 시스템 리소스 체크
        if not self.check_system_resources():
            self.log(f"시스템 리소스 부족으로 작업 연기: {task['name']}", "WARNING")
            return
        
        script_path = self.base_dir / task['script']
        
        if not script_path.exists():
            self.log(f"스크립트 없음: {script_path}", "ERROR")
            return
        
        try:
            # Python 스크립트 실행
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=3600  # 1시간 타임아웃
            )
            
            if result.returncode == 0:
                self.log(f"작업 완료: {task['name']}")
            else:
                self.log(f"작업 실패: {task['name']} - {result.stderr}", "ERROR")
                
        except subprocess.TimeoutExpired:
            self.log(f"작업 타임아웃: {task['name']}", "ERROR")
        except Exception as e:
            self.log(f"작업 실행 오류: {task['name']} - {e}", "ERROR")
    
    def setup_schedules(self):
        """스케줄 설정"""
        for task in self.config['tasks']:
            if not task.get('enabled', False):
                continue
                
            if task['schedule'] == 'hourly':
                schedule.every().hour.do(lambda t=task: self.run_task(t))
                self.log(f"시간별 작업 등록: {task['name']}")
                
            elif task['schedule'] == 'daily':
                schedule.every().day.at(task['time']).do(lambda t=task: self.run_task(t))
                self.log(f"일별 작업 등록: {task['name']} @ {task['time']}")
                
            elif task['schedule'] == 'weekly':
                getattr(schedule.every(), task['day']).at(task['time']).do(
                    lambda t=task: self.run_task(t)
                )
                self.log(f"주별 작업 등록: {task['name']} @ {task['day']} {task['time']}")
    
    def monitor_claude_bridge(self):
        """Claude Bridge 모니터링"""
        bridge_dir = Path("C:/Users/8899y/claude_bridge")
        
        if not bridge_dir.exists():
            return
            
        # 새 요청 확인
        for req_file in bridge_dir.glob("request_*.json"):
            try:
                with open(req_file, 'r', encoding='utf-8') as f:
                    request = json.load(f)
                
                self.log(f"Claude 요청 감지: {request.get('action', 'unknown')}")
                
                # 요청 처리
                self.process_claude_request(request)
                
                # 처리된 파일 이동
                processed_dir = bridge_dir / "processed"
                processed_dir.mkdir(exist_ok=True)
                req_file.rename(processed_dir / req_file.name)
                
            except Exception as e:
                self.log(f"요청 처리 오류: {e}", "ERROR")
    
    def process_claude_request(self, request):
        """Claude 요청 처리"""
        action = request.get('action')
        
        if action == 'learn_product':
            product_no = request.get('product_no', '338')
            self.log(f"상품 학습 요청: {product_no}")
            
            # 학습 스크립트 실행
            task = {
                'name': f'learn_product_{product_no}',
                'script': 'modules/cafe24/cafe24_unified_learner.py'
            }
            self.run_task(task)
            
        elif action == 'update_price':
            self.log("가격 업데이트 요청")
            # 가격 업데이트 로직
            
        elif action == 'status':
            self.write_status_report()
    
    def write_status_report(self):
        """상태 리포트 작성"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "scheduler": "running",
            "next_runs": [],
            "recent_tasks": []
        }
        
        # 다음 실행 예정 작업
        for job in schedule.jobs:
            status["next_runs"].append({
                "job": str(job),
                "next_run": str(job.next_run) if job.next_run else "N/A"
            })
        
        # 상태 파일 저장
        status_file = self.base_dir / "scheduler_status.json"
        with open(status_file, 'w', encoding='utf-8') as f:
            json.dump(status, f, ensure_ascii=False, indent=2)
        
        self.log("상태 리포트 작성 완료")
    
    def run(self):
        """메인 실행 루프"""
        self.log("CUA 백그라운드 스케줄러 시작")
        
        # 스케줄 설정
        self.setup_schedules()
        
        # 상태 리포트 스케줄
        schedule.every(5).minutes.do(self.write_status_report)
        
        # Claude Bridge 모니터링 스케줄
        schedule.every(30).seconds.do(self.monitor_claude_bridge)
        
        # 메인 루프
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(1)
                
            except KeyboardInterrupt:
                self.log("스케줄러 종료 요청")
                self.running = False
                
            except Exception as e:
                self.log(f"스케줄러 오류: {e}", "ERROR")
                time.sleep(10)
        
        self.log("CUA 백그라운드 스케줄러 종료")
    
    def stop(self):
        """스케줄러 중지"""
        self.running = False

def run_in_background():
    """백그라운드에서 실행"""
    scheduler = CUABackgroundScheduler()
    
    # 별도 스레드에서 실행
    thread = threading.Thread(target=scheduler.run, daemon=True)
    thread.start()
    
    return scheduler

if __name__ == "__main__":
    print("""
    ============================================================
    CUA Agent 백그라운드 자동화 스케줄러
    ============================================================
    
    주요 기능:
    1. 주기적 카페24 학습 자동화
    2. 시스템 리소스 모니터링
    3. Claude Bridge 연동
    4. 작업 스케줄 관리
    
    [INFO] Ctrl+C로 종료
    ============================================================
    """)
    
    scheduler = CUABackgroundScheduler()
    
    try:
        scheduler.run()
    except KeyboardInterrupt:
        print("\n스케줄러 종료...")
        scheduler.stop()
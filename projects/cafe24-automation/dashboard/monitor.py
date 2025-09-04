#!/usr/bin/env python
"""
CUA-MASTER 실시간 모니터링 시스템
"""

import sys
import time
import json
import logging
from datetime import datetime
from pathlib import Path
import psutil
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('CUA-Monitor')

class CUAMonitor:
    def __init__(self):
        self.api_url = "http://localhost:8000"
        self.status_file = Path("C:/Users/8899y/CUA-MASTER/data/monitoring_status.json")
        self.log_file = Path("C:/Users/8899y/CUA-MASTER/logs/cua_background.log")
        self.stats = {
            "start_time": datetime.now().isoformat(),
            "api_calls": 0,
            "errors": 0,
            "uptime": 0,
            "background_tasks": 0
        }
        
    def check_api_status(self):
        """API 서버 상태 체크"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "online",
                    "agent_ready": data.get("agent_ready"),
                    "providers": data.get("providers_available", [])
                }
        except:
            return {"status": "offline"}
            
    def get_system_metrics(self):
        """시스템 메트릭 수집"""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "network": {
                "sent": psutil.net_io_counters().bytes_sent,
                "recv": psutil.net_io_counters().bytes_recv
            }
        }
        
    def get_background_tasks(self):
        """백그라운드 작업 상태 조회"""
        if self.status_file.exists():
            try:
                with open(self.status_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data
            except:
                pass
        return {
            "active_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "tasks": {}
        }
    
    def get_recent_logs(self, lines=10):
        """최근 로그 조회"""
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    all_lines = f.readlines()
                    return all_lines[-lines:] if len(all_lines) > lines else all_lines
            except:
                pass
        return []
    
    def check_modules_status(self):
        """모듈 상태 체크"""
        modules = {
            "ecommerce": Path("CUA-MASTER/modules/ecommerce").exists(),
            "invoice": Path("CUA-MASTER/modules/invoice").exists(),
            "orders": Path("CUA-MASTER/modules/orders").exists(),
            "ai_council": Path("CUA-MASTER/modules/ai_council").exists(),
            "cafe24": Path("CUA-MASTER/modules/cafe24").exists()
        }
        return modules
        
    def generate_dashboard_data(self):
        """대시보드 데이터 생성"""
        return {
            "timestamp": datetime.now().isoformat(),
            "api_status": self.check_api_status(),
            "system_metrics": self.get_system_metrics(),
            "modules": self.check_modules_status(),
            "background_tasks": self.get_background_tasks(),
            "recent_logs": self.get_recent_logs(5),
            "stats": self.stats
        }
        
    def save_metrics(self, data):
        """메트릭 저장"""
        log_dir = Path("CUA-MASTER/data/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"monitor_{datetime.now().strftime('%Y%m%d')}.json"
        
        # 기존 로그 읽기
        logs = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                try:
                    logs = json.load(f)
                except:
                    logs = []
                    
        # 새 로그 추가
        logs.append(data)
        
        # 저장
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
            
    def display_status(self, data):
        """상태 표시"""
        print("\n" + "="*50)
        print("[Monitor] CUA-MASTER Real-time Monitoring")
        print("="*50)
        print(f"Time: {data['timestamp']}")
        print(f"API: {data['api_status']['status']}")
        
        metrics = data['system_metrics']
        print(f"CPU: {metrics['cpu_percent']}%")
        print(f"Memory: {metrics['memory_percent']}%")
        print(f"Disk: {metrics['disk_usage']}%")
        
        # 백그라운드 작업 상태
        bg_tasks = data.get('background_tasks', {})
        print(f"\n백그라운드 작업:")
        print(f"  실행 중: {bg_tasks.get('active_tasks', 0)}")
        print(f"  완료됨: {bg_tasks.get('completed_tasks', 0)}")
        print(f"  실패함: {bg_tasks.get('failed_tasks', 0)}")
        
        print("\nModule Status:")
        for module, status in data['modules'].items():
            icon = "[OK]" if status else "[X]"
            print(f"  {icon} {module}")
        
        # 최근 로그
        recent_logs = data.get('recent_logs', [])
        if recent_logs:
            print("\n최근 로그:")
            for log in recent_logs[-3:]:
                print(f"  {log.strip()}")
            
        print("="*50)
        
    def run(self):
        """모니터링 실행"""
        logger.info("[START] CUA Monitoring System Starting")
        
        while True:
            try:
                # 데이터 수집
                data = self.generate_dashboard_data()
                
                # 화면 표시
                self.display_status(data)
                
                # 메트릭 저장
                self.save_metrics(data)
                
                # 통계 업데이트
                self.stats["api_calls"] += 1
                self.stats["uptime"] = (datetime.now() - datetime.fromisoformat(self.stats["start_time"])).total_seconds()
                
                # 30초 대기
                time.sleep(30)
                
            except KeyboardInterrupt:
                logger.info("모니터링 종료")
                break
            except Exception as e:
                logger.error(f"모니터링 오류: {e}")
                self.stats["errors"] += 1
                time.sleep(5)

if __name__ == "__main__":
    monitor = CUAMonitor()
    monitor.run()
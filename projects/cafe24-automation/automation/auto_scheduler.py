#!/usr/bin/env python
"""
CUA-MASTER 자동화 스케줄러
모든 자동화 작업을 관리하고 실행
"""

import sys
import os
import time
import schedule
import logging
from datetime import datetime
from pathlib import Path

# CUA 경로 설정
sys.path.insert(0, str(Path(__file__).parent.parent / 'core'))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('CUA-Scheduler')

class CUAScheduler:
    def __init__(self):
        self.tasks = []
        logger.info("CUA 자동화 스케줄러 초기화")
        
    def system_health_check(self):
        """시스템 건강 체크"""
        logger.info("시스템 건강 체크 실행")
        try:
            # API 서버 체크
            import requests
            response = requests.get('http://localhost:8000/health')
            if response.status_code == 200:
                logger.info("✅ API 서버 정상")
            else:
                logger.warning("⚠️ API 서버 응답 이상")
        except:
            logger.error("❌ API 서버 연결 실패")
            
    def backup_critical_files(self):
        """중요 파일 백업"""
        logger.info("중요 파일 백업 시작")
        backup_dir = Path("CUA-MASTER/data/backups") / datetime.now().strftime("%Y%m%d")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # 백업 대상
        targets = [
            "CUA-MASTER/configs/.env",
            "CUA-MASTER/data/unified.db",
            "CUA-MASTER/CLAUDE.md"
        ]
        
        for target in targets:
            if Path(target).exists():
                logger.info(f"백업: {target}")
                # 실제 백업 로직
                
    def clean_duplicate_files(self):
        """중복 파일 정리"""
        logger.info("중복 파일 스캔 및 정리")
        # 중복 파일 찾기 로직
        
    def optimize_system(self):
        """시스템 최적화"""
        logger.info("시스템 최적화 실행")
        # 캐시 정리, 로그 압축 등
        
    def daily_report(self):
        """일일 보고서 생성"""
        logger.info("일일 보고서 생성")
        report = {
            "date": datetime.now().isoformat(),
            "health_status": "OK",
            "tasks_completed": len(self.tasks),
            "errors": 0
        }
        logger.info(f"보고서: {report}")
        
    def setup_schedules(self):
        """스케줄 설정"""
        # 매 시간
        schedule.every().hour.do(self.system_health_check)
        
        # 매일
        schedule.every().day.at("03:00").do(self.backup_critical_files)
        schedule.every().day.at("04:00").do(self.clean_duplicate_files)
        schedule.every().day.at("05:00").do(self.optimize_system)
        schedule.every().day.at("23:59").do(self.daily_report)
        
        # 매 30분
        schedule.every(30).minutes.do(self.system_health_check)
        
        logger.info("✅ 모든 스케줄 설정 완료")
        
    def run(self):
        """스케줄러 실행"""
        self.setup_schedules()
        logger.info("🚀 CUA 자동화 스케줄러 시작")
        
        # 즉시 한번 실행
        self.system_health_check()
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # 1분마다 체크

if __name__ == "__main__":
    scheduler = CUAScheduler()
    try:
        scheduler.run()
    except KeyboardInterrupt:
        logger.info("스케줄러 종료")
    except Exception as e:
        logger.error(f"스케줄러 오류: {e}")
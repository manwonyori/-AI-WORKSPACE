"""
AI Image Studio - Scheduler
Cron job management and automation scheduler
"""

import schedule
import time
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Callable
import logging
import threading
import sqlite3

class TaskScheduler:
    """Advanced task scheduler for automated image generation workflows"""
    
    def __init__(self, db_path: str = None):
        self.base_path = Path(__file__).parent
        self.db_path = db_path or self.base_path / "config" / "scheduler.db"
        self.jobs = {}
        self.running = False
        self.scheduler_thread = None
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.base_path / "logs" / "scheduler.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("AIStudioScheduler")
        
        # Create directories
        (self.base_path / "logs").mkdir(exist_ok=True)
        (self.base_path / "config").mkdir(exist_ok=True)
        
        self._initialize_database()
        self._load_saved_jobs()
    
    def _initialize_database(self):
        """Initialize SQLite database for job persistence"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_jobs (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                job_type TEXT NOT NULL,
                schedule_type TEXT NOT NULL,
                schedule_value TEXT NOT NULL,
                config TEXT NOT NULL,
                enabled BOOLEAN DEFAULT 1,
                created_at TEXT NOT NULL,
                last_run TEXT,
                next_run TEXT,
                run_count INTEGER DEFAULT 0,
                error_count INTEGER DEFAULT 0,
                last_error TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT NOT NULL,
                started_at TEXT NOT NULL,
                completed_at TEXT,
                status TEXT NOT NULL,
                result TEXT,
                error TEXT,
                FOREIGN KEY (job_id) REFERENCES scheduled_jobs (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _load_saved_jobs(self):
        """Load previously saved jobs from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM scheduled_jobs WHERE enabled = 1")
        rows = cursor.fetchall()
        
        for row in rows:
            job_id, name, job_type, schedule_type, schedule_value, config, enabled, created_at, last_run, next_run, run_count, error_count, last_error = row
            
            job_config = json.loads(config)
            
            # Recreate the job
            if schedule_type == "interval":
                self.schedule_interval_job(
                    job_id=job_id,
                    name=name,
                    job_type=job_type,
                    interval_minutes=int(schedule_value),
                    config=job_config,
                    save_to_db=False  # Already in DB
                )
            elif schedule_type == "daily":
                self.schedule_daily_job(
                    job_id=job_id,
                    name=name,
                    job_type=job_type,
                    time_str=schedule_value,
                    config=job_config,
                    save_to_db=False
                )
            elif schedule_type == "weekly":
                day, time_str = schedule_value.split("_")
                self.schedule_weekly_job(
                    job_id=job_id,
                    name=name,
                    job_type=job_type,
                    day=day,
                    time_str=time_str,
                    config=job_config,
                    save_to_db=False
                )
        
        conn.close()
        self.logger.info(f"Loaded {len(rows)} scheduled jobs from database")
    
    def schedule_batch_generation(self, 
                                 name: str,
                                 products_file: str,
                                 schedule_type: str = "daily",
                                 schedule_value: str = "09:00",
                                 config: Dict = None) -> str:
        """Schedule automated batch image generation"""
        
        job_config = {
            "products_file": products_file,
            "category": config.get("category", "food"),
            "styles": config.get("styles", ["product_showcase"]),
            "platforms": config.get("platforms", ["midjourney"]),
            "output_report": config.get("output_report", "auto")
        }
        
        if schedule_type == "daily":
            return self.schedule_daily_job(
                name=name,
                job_type="batch_generation",
                time_str=schedule_value,
                config=job_config
            )
        elif schedule_type == "weekly":
            day, time_str = schedule_value.split("_") if "_" in schedule_value else ("monday", schedule_value)
            return self.schedule_weekly_job(
                name=name,
                job_type="batch_generation",
                day=day,
                time_str=time_str,
                config=job_config
            )
        elif schedule_type == "interval":
            return self.schedule_interval_job(
                name=name,
                job_type="batch_generation",
                interval_minutes=int(schedule_value),
                config=job_config
            )
    
    def schedule_quality_monitoring(self,
                                  name: str = "Quality Monitor",
                                  interval_minutes: int = 60,
                                  quality_threshold: float = 70) -> str:
        """Schedule automated quality monitoring"""
        
        job_config = {
            "quality_threshold": quality_threshold,
            "check_recent_hours": 24,
            "send_alerts": True,
            "alert_email": None  # Configure as needed
        }
        
        return self.schedule_interval_job(
            name=name,
            job_type="quality_monitoring",
            interval_minutes=interval_minutes,
            config=job_config
        )
    
    def schedule_library_export(self,
                               name: str = "Library Export",
                               schedule_type: str = "weekly",
                               schedule_value: str = "sunday_23:00",
                               min_quality: float = 80) -> str:
        """Schedule automated prompt library exports"""
        
        job_config = {
            "min_quality": min_quality,
            "output_directory": "exports",
            "include_analytics": True
        }
        
        if schedule_type == "weekly":
            day, time_str = schedule_value.split("_")
            return self.schedule_weekly_job(
                name=name,
                job_type="library_export",
                day=day,
                time_str=time_str,
                config=job_config
            )
        elif schedule_type == "daily":
            return self.schedule_daily_job(
                name=name,
                job_type="library_export",
                time_str=schedule_value,
                config=job_config
            )
    
    def schedule_daily_job(self, name: str, job_type: str, time_str: str, 
                          config: Dict, job_id: str = None, save_to_db: bool = True) -> str:
        """Schedule a daily recurring job"""
        
        if not job_id:
            job_id = f"{job_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create the scheduled job
        job = schedule.every().day.at(time_str).do(
            self._execute_job, job_id, job_type, config
        )
        
        self.jobs[job_id] = {
            "name": name,
            "job_type": job_type,
            "schedule_type": "daily",
            "schedule_value": time_str,
            "config": config,
            "job_object": job,
            "created_at": datetime.now().isoformat(),
            "enabled": True
        }
        
        if save_to_db:
            self._save_job_to_db(job_id)
        
        self.logger.info(f"Scheduled daily job '{name}' at {time_str}")
        return job_id
    
    def schedule_weekly_job(self, name: str, job_type: str, day: str, time_str: str,
                           config: Dict, job_id: str = None, save_to_db: bool = True) -> str:
        """Schedule a weekly recurring job"""
        
        if not job_id:
            job_id = f"{job_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Map day names to schedule methods
        day_methods = {
            "monday": schedule.every().monday,
            "tuesday": schedule.every().tuesday,
            "wednesday": schedule.every().wednesday,
            "thursday": schedule.every().thursday,
            "friday": schedule.every().friday,
            "saturday": schedule.every().saturday,
            "sunday": schedule.every().sunday
        }
        
        if day.lower() not in day_methods:
            raise ValueError(f"Invalid day: {day}")
        
        # Create the scheduled job
        job = day_methods[day.lower()].at(time_str).do(
            self._execute_job, job_id, job_type, config
        )
        
        self.jobs[job_id] = {
            "name": name,
            "job_type": job_type,
            "schedule_type": "weekly",
            "schedule_value": f"{day}_{time_str}",
            "config": config,
            "job_object": job,
            "created_at": datetime.now().isoformat(),
            "enabled": True
        }
        
        if save_to_db:
            self._save_job_to_db(job_id)
        
        self.logger.info(f"Scheduled weekly job '{name}' on {day} at {time_str}")
        return job_id
    
    def schedule_interval_job(self, name: str, job_type: str, interval_minutes: int,
                             config: Dict, job_id: str = None, save_to_db: bool = True) -> str:
        """Schedule an interval-based recurring job"""
        
        if not job_id:
            job_id = f"{job_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create the scheduled job
        job = schedule.every(interval_minutes).minutes.do(
            self._execute_job, job_id, job_type, config
        )
        
        self.jobs[job_id] = {
            "name": name,
            "job_type": job_type,
            "schedule_type": "interval",
            "schedule_value": str(interval_minutes),
            "config": config,
            "job_object": job,
            "created_at": datetime.now().isoformat(),
            "enabled": True
        }
        
        if save_to_db:
            self._save_job_to_db(job_id)
        
        self.logger.info(f"Scheduled interval job '{name}' every {interval_minutes} minutes")
        return job_id
    
    def _execute_job(self, job_id: str, job_type: str, config: Dict):
        """Execute a scheduled job"""
        
        start_time = datetime.now()
        self.logger.info(f"Starting job {job_id} ({job_type})")
        
        # Record job start in history
        self._record_job_start(job_id, start_time)
        
        try:
            if job_type == "batch_generation":
                result = self._execute_batch_generation(config)
            elif job_type == "quality_monitoring":
                result = self._execute_quality_monitoring(config)
            elif job_type == "library_export":
                result = self._execute_library_export(config)
            else:
                raise ValueError(f"Unknown job type: {job_type}")
            
            # Record successful completion
            end_time = datetime.now()
            self._record_job_completion(job_id, start_time, end_time, "success", result)
            self._update_job_stats(job_id, success=True)
            
            self.logger.info(f"Job {job_id} completed successfully in {(end_time - start_time).total_seconds():.1f} seconds")
            
        except Exception as e:
            # Record failure
            end_time = datetime.now()
            error_msg = str(e)
            self._record_job_completion(job_id, start_time, end_time, "error", None, error_msg)
            self._update_job_stats(job_id, success=False, error_msg=error_msg)
            
            self.logger.error(f"Job {job_id} failed: {error_msg}")
    
    def _execute_batch_generation(self, config: Dict) -> Dict:
        """Execute batch generation job"""
        from ai_studio_cli import AIStudioCLI
        
        cli = AIStudioCLI()
        
        # Generate timestamped report path if auto
        if config.get("output_report") == "auto":
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            config["output_report"] = f"batch_report_{timestamp}.json"
        
        result = cli.generate_batch(
            products_file=config["products_file"],
            category=config["category"],
            styles=config["styles"],
            platforms=config["platforms"],
            output_report=config.get("output_report")
        )
        
        return result
    
    def _execute_quality_monitoring(self, config: Dict) -> Dict:
        """Execute quality monitoring job"""
        from image_analyzer import ImageQualityAnalyzer
        
        analyzer = ImageQualityAnalyzer()
        
        # Check recent analyses for quality issues
        conn = sqlite3.connect(analyzer.db_path)
        cursor = conn.cursor()
        
        # Get recent analyses
        since_time = (datetime.now() - timedelta(hours=config["check_recent_hours"])).isoformat()
        cursor.execute(
            "SELECT * FROM image_analysis WHERE timestamp > ? ORDER BY timestamp DESC",
            (since_time,)
        )
        
        recent_analyses = cursor.fetchall()
        conn.close()
        
        if not recent_analyses:
            return {"status": "no_recent_analyses", "message": "No recent analyses found"}
        
        # Calculate quality statistics
        quality_scores = [row[6] for row in recent_analyses]  # overall_score column
        avg_quality = sum(quality_scores) / len(quality_scores)
        below_threshold = sum(1 for score in quality_scores if score < config["quality_threshold"])
        
        result = {
            "status": "completed",
            "total_analyses": len(recent_analyses),
            "average_quality": avg_quality,
            "below_threshold_count": below_threshold,
            "below_threshold_percentage": below_threshold / len(recent_analyses) * 100,
            "quality_threshold": config["quality_threshold"]
        }
        
        # Send alert if quality is concerning
        if avg_quality < config["quality_threshold"] or below_threshold / len(recent_analyses) > 0.3:
            result["alert_sent"] = True
            self.logger.warning(f"Quality alert: Average quality {avg_quality:.1f}, {below_threshold_percentage:.1f}% below threshold")
            
            if config.get("send_alerts") and config.get("alert_email"):
                # Send email alert (implement email sending logic)
                pass
        
        return result
    
    def _execute_library_export(self, config: Dict) -> Dict:
        """Execute library export job"""
        from prompt_engine import PromptEngine
        
        engine = PromptEngine()
        
        # Generate timestamped output path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = self.base_path / config["output_directory"]
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"prompt_library_{timestamp}.json"
        
        # Export high-quality prompts
        library_path = engine.export_prompt_library(str(output_path))
        
        # Generate analytics if requested
        analytics = {}
        if config.get("include_analytics"):
            best_prompts = engine.get_best_performing_templates(min_score=config["min_quality"])
            analytics = {
                "export_timestamp": timestamp,
                "total_high_quality_prompts": len(best_prompts),
                "min_quality_threshold": config["min_quality"],
                "total_prompts_in_history": len(engine.generation_history),
                "platform_distribution": engine._get_platform_distribution()
            }
        
        result = {
            "status": "completed",
            "library_path": library_path,
            "analytics": analytics
        }
        
        return result
    
    def start(self):
        """Start the scheduler in a background thread"""
        if self.running:
            self.logger.warning("Scheduler is already running")
            return
        
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        self.logger.info("Scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
        self.logger.info("Scheduler stopped")
    
    def _run_scheduler(self):
        """Main scheduler loop"""
        while self.running:
            schedule.run_pending()
            time.sleep(30)  # Check every 30 seconds
    
    def get_job_status(self, job_id: str = None) -> Dict:
        """Get status of jobs"""
        if job_id:
            job = self.jobs.get(job_id)
            if not job:
                return {"error": f"Job {job_id} not found"}
            
            # Get next run time
            next_run = job["job_object"].next_run
            next_run_str = next_run.isoformat() if next_run else "Not scheduled"
            
            return {
                "job_id": job_id,
                "name": job["name"],
                "type": job["job_type"],
                "schedule": f"{job['schedule_type']}: {job['schedule_value']}",
                "next_run": next_run_str,
                "enabled": job["enabled"]
            }
        else:
            # Return all jobs
            job_statuses = []
            for jid, job in self.jobs.items():
                next_run = job["job_object"].next_run
                next_run_str = next_run.isoformat() if next_run else "Not scheduled"
                
                job_statuses.append({
                    "job_id": jid,
                    "name": job["name"],
                    "type": job["job_type"],
                    "schedule": f"{job['schedule_type']}: {job['schedule_value']}",
                    "next_run": next_run_str,
                    "enabled": job["enabled"]
                })
            
            return {
                "total_jobs": len(job_statuses),
                "running": self.running,
                "jobs": job_statuses
            }
    
    def enable_job(self, job_id: str):
        """Enable a job"""
        if job_id in self.jobs:
            self.jobs[job_id]["enabled"] = True
            self._update_job_enabled_status(job_id, True)
            self.logger.info(f"Enabled job {job_id}")
        else:
            raise ValueError(f"Job {job_id} not found")
    
    def disable_job(self, job_id: str):
        """Disable a job"""
        if job_id in self.jobs:
            self.jobs[job_id]["enabled"] = False
            schedule.cancel_job(self.jobs[job_id]["job_object"])
            self._update_job_enabled_status(job_id, False)
            self.logger.info(f"Disabled job {job_id}")
        else:
            raise ValueError(f"Job {job_id} not found")
    
    def delete_job(self, job_id: str):
        """Delete a job"""
        if job_id in self.jobs:
            schedule.cancel_job(self.jobs[job_id]["job_object"])
            del self.jobs[job_id]
            self._delete_job_from_db(job_id)
            self.logger.info(f"Deleted job {job_id}")
        else:
            raise ValueError(f"Job {job_id} not found")
    
    def get_job_history(self, job_id: str, limit: int = 10) -> List[Dict]:
        """Get execution history for a job"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM job_history WHERE job_id = ? ORDER BY started_at DESC LIMIT ?",
            (job_id, limit)
        )
        
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            history.append({
                "id": row[0],
                "started_at": row[2],
                "completed_at": row[3],
                "status": row[4],
                "duration": self._calculate_duration(row[2], row[3]) if row[3] else None,
                "result_summary": json.loads(row[5])["summary"] if row[5] else None,
                "error": row[6]
            })
        
        return history
    
    # Database helper methods
    def _save_job_to_db(self, job_id: str):
        """Save job configuration to database"""
        job = self.jobs[job_id]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO scheduled_jobs 
            (id, name, job_type, schedule_type, schedule_value, config, enabled, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            job_id,
            job["name"],
            job["job_type"],
            job["schedule_type"],
            job["schedule_value"],
            json.dumps(job["config"]),
            job["enabled"],
            job["created_at"]
        ))
        
        conn.commit()
        conn.close()
    
    def _record_job_start(self, job_id: str, start_time: datetime):
        """Record job start in history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO job_history (job_id, started_at, status)
            VALUES (?, ?, ?)
        ''', (job_id, start_time.isoformat(), "running"))
        
        conn.commit()
        conn.close()
    
    def _record_job_completion(self, job_id: str, start_time: datetime, 
                              end_time: datetime, status: str, result: Dict = None, error: str = None):
        """Record job completion in history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE job_history 
            SET completed_at = ?, status = ?, result = ?, error = ?
            WHERE job_id = ? AND started_at = ?
        ''', (
            end_time.isoformat(),
            status,
            json.dumps(result) if result else None,
            error,
            job_id,
            start_time.isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def _update_job_stats(self, job_id: str, success: bool, error_msg: str = None):
        """Update job statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if success:
            cursor.execute('''
                UPDATE scheduled_jobs 
                SET last_run = ?, run_count = run_count + 1
                WHERE id = ?
            ''', (datetime.now().isoformat(), job_id))
        else:
            cursor.execute('''
                UPDATE scheduled_jobs 
                SET last_run = ?, run_count = run_count + 1, 
                    error_count = error_count + 1, last_error = ?
                WHERE id = ?
            ''', (datetime.now().isoformat(), error_msg, job_id))
        
        conn.commit()
        conn.close()
    
    def _update_job_enabled_status(self, job_id: str, enabled: bool):
        """Update job enabled status in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE scheduled_jobs SET enabled = ? WHERE id = ?",
            (enabled, job_id)
        )
        
        conn.commit()
        conn.close()
    
    def _delete_job_from_db(self, job_id: str):
        """Delete job from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM scheduled_jobs WHERE id = ?", (job_id,))
        cursor.execute("DELETE FROM job_history WHERE job_id = ?", (job_id,))
        
        conn.commit()
        conn.close()
    
    def _calculate_duration(self, start_str: str, end_str: str) -> float:
        """Calculate duration between two datetime strings"""
        start = datetime.fromisoformat(start_str)
        end = datetime.fromisoformat(end_str)
        return (end - start).total_seconds()


if __name__ == "__main__":
    # Example usage
    scheduler = TaskScheduler()
    
    # Schedule a daily batch generation
    job_id = scheduler.schedule_batch_generation(
        name="Daily Product Generation",
        products_file="products.csv",
        schedule_type="daily",
        schedule_value="09:00",
        config={
            "category": "food",
            "styles": ["product_showcase", "lifestyle"],
            "platforms": ["midjourney"]
        }
    )
    
    print(f"Scheduled job: {job_id}")
    
    # Schedule quality monitoring every hour
    monitor_id = scheduler.schedule_quality_monitoring(
        name="Hourly Quality Check",
        interval_minutes=60,
        quality_threshold=75
    )
    
    print(f"Scheduled monitoring: {monitor_id}")
    
    # Start the scheduler
    scheduler.start()
    
    print("Scheduler started. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(10)
            status = scheduler.get_job_status()
            print(f"Active jobs: {status['total_jobs']}, Running: {status['running']}")
    except KeyboardInterrupt:
        scheduler.stop()
        print("Scheduler stopped.")
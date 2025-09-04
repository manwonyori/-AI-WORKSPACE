"""
AI Image Studio - Real-time Monitoring System
Advanced monitoring and alerting for AI image generation workflows
"""

import psutil
import time
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
try:
    import smtplib
    from email.mime.text import MimeText
    from email.mime.multipart import MimeMultipart
    EMAIL_AVAILABLE = True
except ImportError:
    EMAIL_AVAILABLE = False
    print("Warning: Email functionality not available")
import threading
import logging
import requests
from collections import deque
import numpy as np

class SystemMonitor:
    """Real-time system monitoring for AI image generation"""
    
    def __init__(self, config_path: str = None):
        self.base_path = Path(__file__).parent
        self.config_path = config_path or self.base_path / "config" / "monitoring_config.json"
        self.db_path = self.base_path / "analysis" / "monitoring.db"
        
        # Monitoring state
        self.running = False
        self.monitor_thread = None
        self.metrics_history = deque(maxlen=1000)  # Keep last 1000 metrics
        self.alerts_sent = {}  # Track sent alerts to avoid spam
        
        # Configuration
        self.config = self._load_config()
        
        # Setup logging
        self.logger = self._setup_logging()
        
        # Initialize database
        self._initialize_database()
    
    def _load_config(self) -> Dict:
        """Load monitoring configuration"""
        default_config = {
            "monitoring": {
                "interval_seconds": 30,
                "metrics_retention_hours": 24,
                "alert_cooldown_minutes": 30
            },
            "thresholds": {
                "cpu_usage_percent": 80,
                "memory_usage_percent": 85,
                "disk_usage_percent": 90,
                "generation_success_rate": 70,
                "avg_quality_score": 60,
                "generation_time_seconds": 300
            },
            "alerts": {
                "enabled": True,
                "email": {
                    "smtp_server": "smtp.gmail.com",
                    "smtp_port": 587,
                    "username": "",
                    "password": "",
                    "to_addresses": []
                },
                "webhook": {
                    "enabled": False,
                    "url": "",
                    "headers": {}
                }
            },
            "services": {
                "monitor_generation_queue": True,
                "monitor_system_resources": True,
                "monitor_image_quality": True,
                "monitor_api_endpoints": True
            }
        }
        
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    return {**default_config, **loaded_config}
            else:
                self.config_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=2)
                return default_config
        except Exception as e:
            print(f"Error loading monitoring config: {e}")
            return default_config
    
    def _setup_logging(self) -> logging.Logger:
        """Setup monitoring logger"""
        log_dir = self.base_path / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "monitoring.log"),
                logging.StreamHandler()
            ]
        )
        
        return logging.getLogger("AIStudioMonitor")
    
    def _initialize_database(self):
        """Initialize monitoring database"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # System metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                cpu_usage REAL,
                memory_usage REAL,
                disk_usage REAL,
                network_io TEXT,
                active_processes INTEGER,
                generation_queue_size INTEGER
            )
        ''')
        
        # Generation metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS generation_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                total_generations INTEGER,
                successful_generations INTEGER,
                failed_generations INTEGER,
                avg_generation_time REAL,
                avg_quality_score REAL,
                platform_stats TEXT
            )
        ''')
        
        # Alert history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alert_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                message TEXT NOT NULL,
                metrics_snapshot TEXT,
                resolved_at TEXT,
                resolution_notes TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def start_monitoring(self):
        """Start real-time monitoring"""
        if self.running:
            self.logger.warning("Monitoring is already running")
            return
        
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.info("Real-time monitoring started")
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join()
        self.logger.info("Monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                # Collect system metrics
                system_metrics = self._collect_system_metrics()
                
                # Collect generation metrics
                generation_metrics = self._collect_generation_metrics()
                
                # Combine metrics
                combined_metrics = {
                    "timestamp": datetime.now().isoformat(),
                    "system": system_metrics,
                    "generation": generation_metrics
                }
                
                # Store metrics
                self._store_metrics(combined_metrics)
                
                # Add to history
                self.metrics_history.append(combined_metrics)
                
                # Check for alerts
                self._check_alerts(combined_metrics)
                
                # Clean old data
                self._cleanup_old_data()
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
            
            time.sleep(self.config["monitoring"]["interval_seconds"])
    
    def _collect_system_metrics(self) -> Dict:
        """Collect system resource metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # Network I/O
            network = psutil.net_io_counters()
            network_io = {
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv
            }
            
            # Process count
            active_processes = len(psutil.pids())
            
            return {
                "cpu_usage": cpu_percent,
                "memory_usage": memory_percent,
                "disk_usage": disk_percent,
                "network_io": network_io,
                "active_processes": active_processes,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error collecting system metrics: {e}")
            return {}
    
    def _collect_generation_metrics(self) -> Dict:
        """Collect image generation performance metrics"""
        try:
            # Query recent generation data from image analyzer database
            analyzer_db_path = self.base_path / "analysis" / "image_analysis.db"
            
            if not analyzer_db_path.exists():
                return {"error": "Image analysis database not found"}
            
            conn = sqlite3.connect(analyzer_db_path)
            cursor = conn.cursor()
            
            # Get recent generations (last hour)
            since_time = (datetime.now() - timedelta(hours=1)).isoformat()
            
            cursor.execute('''
                SELECT overall_score, timestamp 
                FROM image_analysis 
                WHERE timestamp > ?
            ''', (since_time,))
            
            recent_analyses = cursor.fetchall()
            
            # Calculate metrics
            total_generations = len(recent_analyses)
            successful_generations = sum(1 for score, _ in recent_analyses if score >= 50)
            failed_generations = total_generations - successful_generations
            
            avg_quality_score = 0
            if recent_analyses:
                avg_quality_score = sum(score for score, _ in recent_analyses) / len(recent_analyses)
            
            # Get platform distribution (simplified)
            platform_stats = {"midjourney": 0, "dalle": 0, "stable_diffusion": 0}
            
            conn.close()
            
            return {
                "total_generations": total_generations,
                "successful_generations": successful_generations,
                "failed_generations": failed_generations,
                "success_rate": (successful_generations / total_generations * 100) if total_generations > 0 else 100,
                "avg_quality_score": avg_quality_score,
                "platform_stats": platform_stats,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error collecting generation metrics: {e}")
            return {"error": str(e)}
    
    def _store_metrics(self, metrics: Dict):
        """Store metrics in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Store system metrics
            system = metrics.get("system", {})
            cursor.execute('''
                INSERT INTO system_metrics 
                (timestamp, cpu_usage, memory_usage, disk_usage, network_io, active_processes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                metrics["timestamp"],
                system.get("cpu_usage"),
                system.get("memory_usage"),
                system.get("disk_usage"),
                json.dumps(system.get("network_io", {})),
                system.get("active_processes")
            ))
            
            # Store generation metrics
            generation = metrics.get("generation", {})
            cursor.execute('''
                INSERT INTO generation_metrics 
                (timestamp, total_generations, successful_generations, failed_generations, 
                 avg_generation_time, avg_quality_score, platform_stats)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                metrics["timestamp"],
                generation.get("total_generations"),
                generation.get("successful_generations"),
                generation.get("failed_generations"),
                generation.get("avg_generation_time"),
                generation.get("avg_quality_score"),
                json.dumps(generation.get("platform_stats", {}))
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Error storing metrics: {e}")
    
    def _check_alerts(self, metrics: Dict):
        """Check metrics against thresholds and send alerts"""
        if not self.config["alerts"]["enabled"]:
            return
        
        alerts = []
        system = metrics.get("system", {})
        generation = metrics.get("generation", {})
        thresholds = self.config["thresholds"]
        
        # System resource alerts
        if system.get("cpu_usage", 0) > thresholds["cpu_usage_percent"]:
            alerts.append({
                "type": "high_cpu_usage",
                "severity": "warning",
                "message": f"High CPU usage: {system['cpu_usage']:.1f}% (threshold: {thresholds['cpu_usage_percent']}%)",
                "value": system["cpu_usage"],
                "threshold": thresholds["cpu_usage_percent"]
            })
        
        if system.get("memory_usage", 0) > thresholds["memory_usage_percent"]:
            alerts.append({
                "type": "high_memory_usage",
                "severity": "warning",
                "message": f"High memory usage: {system['memory_usage']:.1f}% (threshold: {thresholds['memory_usage_percent']}%)",
                "value": system["memory_usage"],
                "threshold": thresholds["memory_usage_percent"]
            })
        
        if system.get("disk_usage", 0) > thresholds["disk_usage_percent"]:
            alerts.append({
                "type": "high_disk_usage",
                "severity": "critical",
                "message": f"High disk usage: {system['disk_usage']:.1f}% (threshold: {thresholds['disk_usage_percent']}%)",
                "value": system["disk_usage"],
                "threshold": thresholds["disk_usage_percent"]
            })
        
        # Generation performance alerts
        success_rate = generation.get("success_rate", 100)
        if success_rate < thresholds["generation_success_rate"]:
            alerts.append({
                "type": "low_success_rate",
                "severity": "warning",
                "message": f"Low generation success rate: {success_rate:.1f}% (threshold: {thresholds['generation_success_rate']}%)",
                "value": success_rate,
                "threshold": thresholds["generation_success_rate"]
            })
        
        avg_quality = generation.get("avg_quality_score", 100)
        if avg_quality < thresholds["avg_quality_score"]:
            alerts.append({
                "type": "low_quality_score",
                "severity": "warning",
                "message": f"Low average quality score: {avg_quality:.1f} (threshold: {thresholds['avg_quality_score']})",
                "value": avg_quality,
                "threshold": thresholds["avg_quality_score"]
            })
        
        # Send alerts
        for alert in alerts:
            self._send_alert(alert, metrics)
    
    def _send_alert(self, alert: Dict, metrics: Dict):
        """Send alert via configured channels"""
        alert_key = f"{alert['type']}_{datetime.now().strftime('%Y%m%d_%H')}"
        
        # Check cooldown period
        cooldown_minutes = self.config["monitoring"]["alert_cooldown_minutes"]
        if alert_key in self.alerts_sent:
            last_sent = self.alerts_sent[alert_key]
            if (datetime.now() - last_sent).total_seconds() < cooldown_minutes * 60:
                return  # Still in cooldown period
        
        # Record alert
        self._record_alert(alert, metrics)
        
        # Send email alert
        if self.config["alerts"]["email"]["username"]:
            self._send_email_alert(alert, metrics)
        
        # Send webhook alert
        if self.config["alerts"]["webhook"]["enabled"]:
            self._send_webhook_alert(alert, metrics)
        
        # Update cooldown tracking
        self.alerts_sent[alert_key] = datetime.now()
        
        self.logger.warning(f"Alert sent: {alert['message']}")
    
    def _send_email_alert(self, alert: Dict, metrics: Dict):
        """Send alert via email"""
        if not EMAIL_AVAILABLE:
            self.logger.warning("Email functionality not available - skipping email alert")
            return
            
        try:
            email_config = self.config["alerts"]["email"]
            
            msg = MimeMultipart()
            msg['From'] = email_config["username"]
            msg['To'] = ", ".join(email_config["to_addresses"])
            msg['Subject'] = f"AI Studio Alert: {alert['type']}"
            
            # Create email body
            body = f"""
AI Image Studio Monitoring Alert

Alert Type: {alert['type']}
Severity: {alert['severity']}
Message: {alert['message']}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

System Status:
- CPU Usage: {metrics.get('system', {}).get('cpu_usage', 'N/A')}%
- Memory Usage: {metrics.get('system', {}).get('memory_usage', 'N/A')}%
- Disk Usage: {metrics.get('system', {}).get('disk_usage', 'N/A')}%

Generation Status:
- Success Rate: {metrics.get('generation', {}).get('success_rate', 'N/A')}%
- Avg Quality: {metrics.get('generation', {}).get('avg_quality_score', 'N/A')}
- Recent Generations: {metrics.get('generation', {}).get('total_generations', 'N/A')}

Please check the AI Studio monitoring dashboard for more details.
            """
            
            msg.attach(MimeText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(email_config["smtp_server"], email_config["smtp_port"])
            server.starttls()
            server.login(email_config["username"], email_config["password"])
            
            for to_address in email_config["to_addresses"]:
                server.sendmail(email_config["username"], to_address, msg.as_string())
            
            server.quit()
            self.logger.info("Email alert sent successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to send email alert: {e}")
    
    def _send_webhook_alert(self, alert: Dict, metrics: Dict):
        """Send alert via webhook"""
        try:
            webhook_config = self.config["alerts"]["webhook"]
            
            payload = {
                "alert_type": alert["type"],
                "severity": alert["severity"],
                "message": alert["message"],
                "timestamp": datetime.now().isoformat(),
                "metrics": metrics,
                "source": "ai_image_studio"
            }
            
            headers = {"Content-Type": "application/json"}
            headers.update(webhook_config.get("headers", {}))
            
            response = requests.post(
                webhook_config["url"],
                json=payload,
                headers=headers,
                timeout=10
            )
            
            response.raise_for_status()
            self.logger.info("Webhook alert sent successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to send webhook alert: {e}")
    
    def _record_alert(self, alert: Dict, metrics: Dict):
        """Record alert in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO alert_history 
                (timestamp, alert_type, severity, message, metrics_snapshot)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                alert["type"],
                alert["severity"],
                alert["message"],
                json.dumps(metrics)
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Error recording alert: {e}")
    
    def _cleanup_old_data(self):
        """Clean up old monitoring data"""
        try:
            retention_hours = self.config["monitoring"]["metrics_retention_hours"]
            cutoff_time = (datetime.now() - timedelta(hours=retention_hours)).isoformat()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Clean old system metrics
            cursor.execute("DELETE FROM system_metrics WHERE timestamp < ?", (cutoff_time,))
            
            # Clean old generation metrics
            cursor.execute("DELETE FROM generation_metrics WHERE timestamp < ?", (cutoff_time,))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Error cleaning old data: {e}")
    
    def get_current_status(self) -> Dict:
        """Get current system status"""
        if not self.metrics_history:
            return {"status": "no_data", "message": "No monitoring data available"}
        
        latest_metrics = self.metrics_history[-1]
        
        # Calculate trends from recent data
        recent_metrics = list(self.metrics_history)[-10:]  # Last 10 measurements
        
        trends = {}
        if len(recent_metrics) >= 2:
            # CPU trend
            cpu_values = [m["system"].get("cpu_usage", 0) for m in recent_metrics if m["system"].get("cpu_usage")]
            if cpu_values:
                trends["cpu_trend"] = "increasing" if cpu_values[-1] > cpu_values[0] else "decreasing"
            
            # Quality trend
            quality_values = [m["generation"].get("avg_quality_score", 0) for m in recent_metrics if m["generation"].get("avg_quality_score")]
            if quality_values:
                trends["quality_trend"] = "improving" if quality_values[-1] > quality_values[0] else "declining"
        
        return {
            "status": "monitoring_active",
            "timestamp": latest_metrics["timestamp"],
            "system_metrics": latest_metrics["system"],
            "generation_metrics": latest_metrics["generation"],
            "trends": trends,
            "monitoring_duration": len(self.metrics_history),
            "alerts_in_last_hour": self._count_recent_alerts(hours=1)
        }
    
    def get_metrics_history(self, hours: int = 24) -> List[Dict]:
        """Get metrics history for specified time period"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        filtered_metrics = []
        for metric in self.metrics_history:
            metric_time = datetime.fromisoformat(metric["timestamp"])
            if metric_time >= cutoff_time:
                filtered_metrics.append(metric)
        
        return filtered_metrics
    
    def _count_recent_alerts(self, hours: int = 1) -> int:
        """Count alerts in recent time period"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            since_time = (datetime.now() - timedelta(hours=hours)).isoformat()
            cursor.execute(
                "SELECT COUNT(*) FROM alert_history WHERE timestamp > ?",
                (since_time,)
            )
            
            count = cursor.fetchone()[0]
            conn.close()
            
            return count
            
        except Exception as e:
            self.logger.error(f"Error counting recent alerts: {e}")
            return 0
    
    def generate_health_report(self) -> Dict:
        """Generate comprehensive health report"""
        try:
            current_status = self.get_current_status()
            recent_metrics = self.get_metrics_history(hours=24)
            
            if not recent_metrics:
                return {"error": "No metrics data available"}
            
            # Calculate averages
            system_metrics = [m["system"] for m in recent_metrics if m.get("system")]
            generation_metrics = [m["generation"] for m in recent_metrics if m.get("generation")]
            
            avg_cpu = np.mean([s.get("cpu_usage", 0) for s in system_metrics]) if system_metrics else 0
            avg_memory = np.mean([s.get("memory_usage", 0) for s in system_metrics]) if system_metrics else 0
            avg_quality = np.mean([g.get("avg_quality_score", 0) for g in generation_metrics if g.get("avg_quality_score")]) if generation_metrics else 0
            
            # Health score calculation
            health_score = 100
            if avg_cpu > 80:
                health_score -= 20
            if avg_memory > 85:
                health_score -= 20
            if avg_quality < 60:
                health_score -= 30
            
            recent_alerts = self._count_recent_alerts(24)
            if recent_alerts > 10:
                health_score -= 20
            
            health_score = max(0, health_score)
            
            report = {
                "timestamp": datetime.now().isoformat(),
                "health_score": health_score,
                "health_status": "excellent" if health_score > 90 else 
                               "good" if health_score > 70 else
                               "warning" if health_score > 50 else "critical",
                "system_performance": {
                    "avg_cpu_usage": avg_cpu,
                    "avg_memory_usage": avg_memory,
                    "current_disk_usage": current_status.get("system_metrics", {}).get("disk_usage", 0)
                },
                "generation_performance": {
                    "avg_quality_score": avg_quality,
                    "total_generations_24h": sum(g.get("total_generations", 0) for g in generation_metrics),
                    "avg_success_rate": np.mean([g.get("success_rate", 0) for g in generation_metrics if g.get("success_rate")]) if generation_metrics else 0
                },
                "alerts_summary": {
                    "alerts_last_24h": recent_alerts,
                    "critical_alerts": self._count_alerts_by_severity("critical", 24),
                    "warning_alerts": self._count_alerts_by_severity("warning", 24)
                },
                "recommendations": self._generate_health_recommendations(health_score, avg_cpu, avg_memory, avg_quality, recent_alerts)
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating health report: {e}")
            return {"error": str(e)}
    
    def _count_alerts_by_severity(self, severity: str, hours: int) -> int:
        """Count alerts by severity in time period"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            since_time = (datetime.now() - timedelta(hours=hours)).isoformat()
            cursor.execute(
                "SELECT COUNT(*) FROM alert_history WHERE severity = ? AND timestamp > ?",
                (severity, since_time)
            )
            
            count = cursor.fetchone()[0]
            conn.close()
            
            return count
            
        except Exception as e:
            self.logger.error(f"Error counting alerts by severity: {e}")
            return 0
    
    def _generate_health_recommendations(self, health_score: float, avg_cpu: float, 
                                       avg_memory: float, avg_quality: float, alert_count: int) -> List[str]:
        """Generate health improvement recommendations"""
        recommendations = []
        
        if health_score < 70:
            recommendations.append("System health is below optimal - immediate attention required")
        
        if avg_cpu > 80:
            recommendations.append("High CPU usage detected - consider scaling resources or optimizing generation processes")
        
        if avg_memory > 85:
            recommendations.append("High memory usage - check for memory leaks and consider increasing available RAM")
        
        if avg_quality < 60:
            recommendations.append("Image quality scores are below threshold - review prompt engineering and generation parameters")
        
        if alert_count > 10:
            recommendations.append("High number of alerts - investigate recurring issues and adjust thresholds if needed")
        
        if not recommendations:
            recommendations.append("System is performing well - continue monitoring for optimal performance")
        
        return recommendations


if __name__ == "__main__":
    # Example usage
    monitor = SystemMonitor()
    
    print("Starting AI Studio monitoring...")
    monitor.start_monitoring()
    
    try:
        while True:
            time.sleep(60)  # Check status every minute
            status = monitor.get_current_status()
            
            if status.get("status") == "monitoring_active":
                print(f"System Status - CPU: {status['system_metrics'].get('cpu_usage', 0):.1f}%, "
                     f"Memory: {status['system_metrics'].get('memory_usage', 0):.1f}%, "
                     f"Quality: {status['generation_metrics'].get('avg_quality_score', 0):.1f}")
    
    except KeyboardInterrupt:
        print("Stopping monitoring...")
        monitor.stop_monitoring()
    
    # Generate final health report
    health_report = monitor.generate_health_report()
    print(f"\nFinal Health Report:")
    print(f"Health Score: {health_report.get('health_score', 0)}/100")
    print(f"Status: {health_report.get('health_status', 'unknown')}")
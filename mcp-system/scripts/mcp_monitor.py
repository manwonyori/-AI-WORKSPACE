#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import time
import psutil
import requests
from datetime import datetime
import os
import sys
import json

class MCPServerMonitor:
    def __init__(self):
        self.server_url = "http://localhost:3006"
        self.config_path = r"C:\Users\8899y\AI-WORKSPACE\mcp-system\configs\mcp_superassistant_config.json"
        self.log_file = r"C:\Users\8899y\AI-WORKSPACE\mcp-system\logs\mcp_server.log"
        self.restart_count = 0
        self.max_restarts = 10
        
        # 로그 디렉토리 생성
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
    def log_message(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    
    def check_server_health(self):
        """서버 상태 확인"""
        try:
            response = requests.get(f"{self.server_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def find_node_processes(self):
        """Node.js 프로세스 찾기"""
        node_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'node' in proc.info['name'].lower():
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    if 'mcp' in cmdline.lower() or 'superassistant' in cmdline.lower():
                        node_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return node_processes
    
    def kill_existing_servers(self):
        """기존 서버 프로세스 종료"""
        processes = self.find_node_processes()
        for proc in processes:
            try:
                self.log_message(f"기존 프로세스 종료: PID {proc.pid}")
                proc.terminate()
                proc.wait(timeout=5)
            except:
                try:
                    proc.kill()
                except:
                    pass
    
    def start_server(self):
        """MCP 서버 시작"""
        self.kill_existing_servers()
        time.sleep(2)
        
        cmd = [
            "npx",
            "@srbhptl39/mcp-superassistant-proxy@latest",
            "--config", self.config_path,
            "--outputTransport", "sse",
            "--port", "3006"
        ]
        
        self.log_message(f"서버 시작 중... (재시작 횟수: {self.restart_count})")
        
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                text=True,
                encoding='utf-8'
            )
            return process
        except Exception as e:
            self.log_message(f"서버 시작 실패: {e}", "ERROR")
            return None
    
    def monitor_loop(self):
        """메인 모니터링 루프"""
        self.log_message("MCP 서버 모니터 시작")
        server_process = None
        
        while self.restart_count < self.max_restarts:
            try:
                # 서버 상태 확인
                if not self.check_server_health():
                    self.log_message("서버가 응답하지 않음", "WARNING")
                    
                    if server_process and server_process.poll() is None:
                        self.log_message("프로세스는 실행 중이지만 응답 없음", "WARNING")
                        server_process.terminate()
                        time.sleep(2)
                    
                    # 서버 재시작
                    server_process = self.start_server()
                    if server_process:
                        self.restart_count += 1
                        time.sleep(5)  # 서버 시작 대기
                        
                        # 재시작 후 상태 확인
                        if self.check_server_health():
                            self.log_message("서버가 정상적으로 시작됨", "SUCCESS")
                        else:
                            self.log_message("서버 시작 후에도 응답 없음", "ERROR")
                else:
                    # 서버 정상 작동 중
                    if self.restart_count > 0:
                        self.log_message(f"서버 정상 작동 중 (총 재시작: {self.restart_count}회)")
                        self.restart_count = 0  # 연속 재시작 카운트 리셋
                
                # CPU/메모리 사용량 체크
                if server_process and server_process.poll() is None:
                    try:
                        proc = psutil.Process(server_process.pid)
                        cpu_percent = proc.cpu_percent(interval=1)
                        memory_mb = proc.memory_info().rss / 1024 / 1024
                        
                        if cpu_percent > 80:
                            self.log_message(f"높은 CPU 사용률: {cpu_percent:.1f}%", "WARNING")
                        if memory_mb > 500:
                            self.log_message(f"높은 메모리 사용: {memory_mb:.1f}MB", "WARNING")
                    except:
                        pass
                
                time.sleep(30)  # 30초마다 체크
                
            except KeyboardInterrupt:
                self.log_message("사용자에 의해 중단됨")
                if server_process:
                    server_process.terminate()
                break
            except Exception as e:
                self.log_message(f"모니터링 오류: {e}", "ERROR")
                time.sleep(5)
        
        if self.restart_count >= self.max_restarts:
            self.log_message(f"최대 재시작 횟수({self.max_restarts})에 도달. 모니터링 종료", "CRITICAL")

if __name__ == "__main__":
    monitor = MCPServerMonitor()
    monitor.monitor_loop()
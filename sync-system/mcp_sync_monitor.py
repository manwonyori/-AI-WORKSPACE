#!/usr/bin/env python3
"""
MCP 실시간 동기화 모니터
ChatGPT가 MCP를 통해 수정한 내용을 실시간으로 추적하고 Git에 자동 커밋
"""

import asyncio
import aiohttp
import json
import subprocess
import os
from datetime import datetime
from pathlib import Path
import hashlib

class MCPSyncMonitor:
    def __init__(self):
        self.base_dir = Path(r"C:\Users\8899y\AI-WORKSPACE")
        self.sse_url = "http://localhost:3006/sse"
        self.file_hashes = {}
        self.modified_files = set()
        
    async def connect_sse(self):
        """SSE 서버에 연결하여 이벤트 모니터링"""
        print(f"[{datetime.now()}] MCP SSE 서버 연결 중...")
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.sse_url) as response:
                    print(f"[{datetime.now()}] SSE 연결 성공!")
                    
                    async for data in response.content:
                        if data:
                            await self.process_event(data.decode('utf-8'))
                            
            except Exception as e:
                print(f"[{datetime.now()}] SSE 연결 오류: {e}")
                await asyncio.sleep(5)
                await self.connect_sse()  # 재연결
    
    async def process_event(self, data):
        """SSE 이벤트 처리"""
        try:
            # SSE 데이터 파싱
            if data.startswith("data: "):
                event_data = data[6:].strip()
                
                if event_data and event_data != "[DONE]":
                    event = json.loads(event_data)
                    
                    # filesystem.write_file 메소드 감지
                    if "method" in event and "filesystem" in str(event.get("method", "")):
                        await self.handle_filesystem_event(event)
                        
        except json.JSONDecodeError:
            pass  # 파싱 불가능한 데이터 무시
        except Exception as e:
            print(f"이벤트 처리 오류: {e}")
    
    async def handle_filesystem_event(self, event):
        """파일시스템 이벤트 처리"""
        method = event.get("method", "")
        params = event.get("params", {})
        
        if "write_file" in method or "edit_file" in method:
            # 파일 경로 추출
            file_path = None
            if "arguments" in params:
                args = params["arguments"]
                file_path = args.get("path") or args.get("file_path")
            
            if file_path:
                print(f"[{datetime.now()}] ChatGPT가 파일 수정: {file_path}")
                self.modified_files.add(file_path)
                
                # 10초 후 자동 커밋 (여러 파일 수정 대기)
                await asyncio.sleep(10)
                if self.modified_files:
                    await self.auto_commit()
    
    async def auto_commit(self):
        """수정된 파일 자동 Git 커밋"""
        if not self.modified_files:
            return
            
        try:
            os.chdir(self.base_dir)
            
            # Git 상태 확인
            result = subprocess.run(["git", "status", "--porcelain"], 
                                 capture_output=True, text=True)
            
            if result.stdout.strip():
                # 변경사항 스테이징
                for file_path in self.modified_files:
                    subprocess.run(["git", "add", file_path])
                
                # 커밋 메시지 생성
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file_count = len(self.modified_files)
                commit_msg = f"[MCP Sync] ChatGPT가 {file_count}개 파일 수정 - {timestamp}"
                
                # 커밋 실행
                result = subprocess.run(["git", "commit", "-m", commit_msg],
                                     capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"[{datetime.now()}] Git 커밋 성공: {commit_msg}")
                    
                    # 수정된 파일 목록 출력
                    for file in self.modified_files:
                        print(f"  - {file}")
                    
                    # 로그 파일에 기록
                    await self.log_sync(list(self.modified_files))
                    
                    # 리셋
                    self.modified_files.clear()
                    
        except Exception as e:
            print(f"Git 커밋 실패: {e}")
    
    async def log_sync(self, files):
        """동기화 로그 기록"""
        log_dir = self.base_dir / "sync-system" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"sync_{datetime.now().strftime('%Y%m%d')}.log"
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "source": "ChatGPT via MCP",
            "files": files,
            "status": "synced"
        }
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    
    async def watch_local_changes(self):
        """로컬 파일 변경 감시 (양방향 동기화)"""
        import watchdog.events
        import watchdog.observers
        
        class FileHandler(watchdog.events.FileSystemEventHandler):
            def __init__(self, monitor):
                self.monitor = monitor
                
            def on_modified(self, event):
                if not event.is_directory:
                    file_path = Path(event.src_path)
                    # Git 폴더와 sync-system 폴더 제외
                    if ".git" not in str(file_path) and "sync-system" not in str(file_path):
                        print(f"[{datetime.now()}] 로컬 파일 변경 감지: {file_path}")
                        # ChatGPT에 알림 (웹소켓으로 전송 가능)
        
        handler = FileHandler(self)
        observer = watchdog.observers.Observer()
        observer.schedule(handler, str(self.base_dir), recursive=True)
        observer.start()
        
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
    
    async def run(self):
        """메인 실행 루프"""
        print("=" * 60)
        print("MCP 실시간 동기화 모니터 시작")
        print(f"기준 디렉토리: {self.base_dir}")
        print(f"SSE 서버: {self.sse_url}")
        print("=" * 60)
        
        # SSE 연결과 로컬 감시 동시 실행
        await asyncio.gather(
            self.connect_sse(),
            self.watch_local_changes()
        )

if __name__ == "__main__":
    monitor = MCPSyncMonitor()
    asyncio.run(monitor.run())
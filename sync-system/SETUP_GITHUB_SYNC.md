# GitHub 동기화 설정 가이드

## 현재 상황
- GPT와 Claude가 로컬 파일만 공유
- GitHub 동기화가 안 되어 있음
- AI-WORKSPACE가 git에 추적되지 않음

## 설정 방법

### 1. 새 GitHub 저장소 생성
```bash
# AI-WORKSPACE를 위한 별도 저장소 생성
cd C:\Users\8899y\AI-WORKSPACE
git init
git remote add origin https://github.com/manwonyori/AI-WORKSPACE.git
```

### 2. 자동 동기화 스크립트
```python
# auto_git_sync.py
import subprocess
import time
import os

def git_sync():
    os.chdir(r'C:\Users\8899y\AI-WORKSPACE')
    
    # Pull latest changes
    subprocess.run(['git', 'pull'])
    
    # Add all changes
    subprocess.run(['git', 'add', '.'])
    
    # Commit if there are changes
    result = subprocess.run(['git', 'diff', '--cached', '--quiet'], capture_output=True)
    if result.returncode != 0:
        subprocess.run(['git', 'commit', '-m', 'Auto-sync: AI collaboration update'])
        subprocess.run(['git', 'push'])

# Run every 30 seconds
while True:
    try:
        git_sync()
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(30)
```

### 3. 실시간 파일 감시
```python
# file_watcher.py
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class GitAutoCommit(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and 'chrome-extension' in event.src_path:
            subprocess.run(['git', 'add', event.src_path])
            subprocess.run(['git', 'commit', '-m', f'Auto-update: {event.src_path}'])
            subprocess.run(['git', 'push'])

observer = Observer()
observer.schedule(GitAutoCommit(), r'C:\Users\8899y\AI-WORKSPACE', recursive=True)
observer.start()
```

## 장점
1. **실시간 동기화**: 모든 AI가 최신 코드 보유
2. **버전 관리**: 모든 변경사항 추적
3. **협업 강화**: 충돌 자동 감지 및 해결
4. **백업**: GitHub에 자동 백업

## 현재 가능한 방법
- GPT가 파일 수정 → Claude가 읽음 (로컬)
- Claude가 파일 수정 → GPT가 읽음 (로컬)
- 단점: 동시 수정 시 충돌 가능성
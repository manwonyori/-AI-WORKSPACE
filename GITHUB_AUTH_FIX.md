# GitHub 인증 오류 해결 가이드

## 🚨 현재 오류 상황
- GPT가 GitHub에 push할 때 401 Unauthorized 오류 발생
- manwonyori/-AI-WORKSPACE 저장소 접근 불가

## ✅ 즉시 해결 방법

### 방법 1: Public 저장소로 변경 (가장 빠름)
```bash
# GitHub에서 저장소 설정 변경
# Settings → General → Danger Zone → Change visibility → Public
```

### 방법 2: 새 PAT 토큰 발급 및 설정

#### 1. GitHub에서 새 토큰 생성
```
1. https://github.com/settings/tokens/new
2. 다음 권한 선택:
   ✅ repo (전체)
   ✅ workflow
   ✅ write:packages
   ✅ admin:repo_hook
3. Expiration: 90 days 이상
4. Generate token → 복사
```

#### 2. Windows 환경변수 설정
```batch
# 관리자 권한 CMD에서 실행
setx GITHUB_TOKEN "ghp_새로운토큰여기에" /M
setx GH_TOKEN "ghp_새로운토큰여기에" /M
```

#### 3. Git 자격 증명 업데이트
```bash
# Git Bash에서
git config --global credential.helper manager
git config --global user.name "manwonyori"
git config --global user.email "your-email@example.com"

# 기존 자격 증명 삭제
git config --global --unset credential.helper
git config --global credential.helper store

# 새 토큰으로 인증
echo "https://manwonyori:ghp_새토큰@github.com" > ~/.git-credentials
```

### 방법 3: GPT용 전용 설정 파일

#### .env.local 생성
```env
# C:\Users\8899y\AI-WORKSPACE\.env.local
GITHUB_TOKEN=ghp_새로운토큰
GITHUB_OWNER=manwonyori
GITHUB_REPO=AI-WORKSPACE
GITHUB_BRANCH=main
```

#### MCP 설정 업데이트
```json
// C:\Users\8899y\AI-WORKSPACE\mcp-config.json
{
  "mcpServers": {
    "github": {
      "command": "node",
      "args": ["mcp-server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_새토큰여기에"
      }
    }
  }
}
```

## 🔧 GPT와 Claude 협업용 자동 동기화

### sync-config.json
```json
{
  "github": {
    "owner": "manwonyori",
    "repo": "AI-WORKSPACE",
    "branch": "main",
    "autoCommit": true,
    "commitMessage": "Auto-sync: {agent} update at {timestamp}",
    "syncInterval": 30000
  },
  "auth": {
    "method": "token",
    "tokenEnvVar": "GITHUB_TOKEN"
  },
  "permissions": {
    "allowPush": true,
    "allowForceUpdate": false,
    "protectedPaths": [
      ".git",
      ".github",
      "node_modules"
    ]
  }
}
```

### 자동 권한 복구 스크립트
```python
# auto_auth_fix.py
import os
import subprocess
import json

def fix_github_auth():
    """GitHub 인증 자동 복구"""
    
    # 1. 환경변수 확인
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("❌ GITHUB_TOKEN not found")
        return False
    
    # 2. 토큰 유효성 검사
    result = subprocess.run(
        ['gh', 'auth', 'status'],
        capture_output=True,
        text=True
    )
    
    if 'Logged in' not in result.stdout:
        # 3. 재인증 시도
        subprocess.run(['gh', 'auth', 'login', '--with-token'], 
                      input=token, text=True)
    
    # 4. Git 자격 증명 갱신
    subprocess.run([
        'git', 'config', '--global',
        'credential.helper', 'store'
    ])
    
    # 5. 권한 확인
    test_push = subprocess.run(
        ['git', 'ls-remote', 'https://github.com/manwonyori/AI-WORKSPACE.git'],
        capture_output=True
    )
    
    return test_push.returncode == 0

if __name__ == "__main__":
    if fix_github_auth():
        print("✅ GitHub auth fixed!")
    else:
        print("❌ Manual intervention required")
```

## 📝 GPT에게 전달할 설정

GPT에게 다음 내용을 전달하세요:

```
GitHub 인증 설정:
1. 환경변수 GITHUB_TOKEN 확인: echo $GITHUB_TOKEN
2. 없으면 설정: export GITHUB_TOKEN="ghp_새토큰"
3. Git 인증: git remote set-url origin https://manwonyori:${GITHUB_TOKEN}@github.com/manwonyori/AI-WORKSPACE.git
4. 테스트: git push --dry-run
```

## 🚀 즉시 사용 가능한 임시 해결책

### 로컬 전용 모드
```javascript
// background.js에 추가
const USE_LOCAL_ONLY = true; // GitHub 오류 시 true로 변경

async function saveToGitHub(data) {
  if (USE_LOCAL_ONLY) {
    // 로컬 파일만 사용
    return saveToLocalFile(data);
  }
  // GitHub 시도...
}
```

## ⚡ 빠른 해결 명령어
```bash
# Windows PowerShell (관리자)
$env:GITHUB_TOKEN = "ghp_새토큰"
[System.Environment]::SetEnvironmentVariable("GITHUB_TOKEN", "ghp_새토큰", "Machine")

# 즉시 테스트
git -c http.extraheader="AUTHORIZATION: token $env:GITHUB_TOKEN" push
```

## 🔍 디버깅 체크리스트
- [ ] Token 만료일 확인
- [ ] Repository 권한 확인  
- [ ] Branch 보호 규칙 확인
- [ ] 2FA 설정 확인
- [ ] IP 제한 확인
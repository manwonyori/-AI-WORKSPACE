# GitHub 토큰 즉시 설정 가이드

## 🚨 현재 문제
- MCP error -32603: Authentication Failed: Bad credentials
- 기존 GITHUB_TOKEN이 무효화됨

## ✅ 즉시 해결 방법

### 1단계: 새 토큰 생성 (1분)
1. 이 링크 열기: https://github.com/settings/tokens/new
2. 설정:
   - **Note**: AI-WORKSPACE-2025
   - **Expiration**: 90 days
   - **Scopes**: ☑️ repo (전체 선택)
3. "Generate token" 클릭
4. 토큰 복사 (ghp_로 시작하는 문자열)

### 2단계: 시스템 환경변수 설정 (30초)
Windows PowerShell (관리자 권한):
```powershell
# 기존 토큰 제거
[System.Environment]::SetEnvironmentVariable("GITHUB_TOKEN", $null, "User")
[System.Environment]::SetEnvironmentVariable("GITHUB_TOKEN", $null, "Machine")

# 새 토큰 설정 (ghp_여기에_새토큰_붙여넣기)
$newToken = "ghp_YOUR_NEW_TOKEN_HERE"
[System.Environment]::SetEnvironmentVariable("GITHUB_TOKEN", $newToken, "User")
[System.Environment]::SetEnvironmentVariable("GH_TOKEN", $newToken, "User")
```

### 3단계: Git 설정 (30초)
Git Bash에서:
```bash
# AI-WORKSPACE로 이동
cd /c/Users/8899y/AI-WORKSPACE

# Remote 재설정 (토큰 포함)
git remote set-url origin https://manwonyori:ghp_YOUR_NEW_TOKEN@github.com/manwonyori/AI-WORKSPACE.git

# 테스트
git ls-remote origin HEAD
```

## 🔥 가장 빠른 대안: Public 저장소

토큰 설정이 복잡하면:
1. https://github.com/manwonyori/AI-WORKSPACE/settings
2. 맨 아래 "Danger Zone"
3. "Change repository visibility" → "Make public"
4. 완료! (토큰 불필요)

## 📝 MCP 서버 재시작
```bash
# MCP 서버 재시작
cd AI-WORKSPACE
npx @srbhptl39/mcp-superassistant-proxy@latest --config ./mcp-system/configs/mcp_superassistant_config.json --outputTransport sse
```
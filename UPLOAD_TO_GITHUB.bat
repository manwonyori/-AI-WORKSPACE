@echo off
setlocal enableextensions
chcp 65001 >nul
title AI-WORKSPACE → GitHub 자동 업로드 (Hardened)
color 0A
cls

echo ================================================================
echo          🚀 AI-WORKSPACE GitHub 자동 업로드 (Hardened)
echo ================================================================
echo.

REM --- 기본 설정 ---------------------------------------------------
set "REPO_URL=https://github.com/manwonyori/-AI-WORKSPACE.git"
set "BRANCH=main"

cd /d "C:\Users\8899y\AI-WORKSPACE"
echo 📁 현재 위치: %CD%
echo.

REM --- Git 저장소 초기화 / 원격 설정 ------------------------------
echo [1/7] Git 저장소/원격 설정 점검...
echo ----------------------------------------------------------------
if not exist ".git" (
  echo ▶ Git 저장소 초기화 중...
  git init
)
for /f "delims=" %%r in ('git remote') do set HAS_REMOTE=1
if not defined HAS_REMOTE (
  echo ▶ 원격 저장소(origin) 추가: %REPO_URL%
  git remote add origin %REPO_URL%
) else (
  echo ▶ 원격 저장소 상태:
  git remote -v
)
echo ✅ 완료
echo.

REM --- 브랜치 준비 -------------------------------------------------
echo [2/7] 브랜치 준비...
echo ----------------------------------------------------------------
REM 현재 브랜치 확인
for /f "tokens=2" %%b in ('git symbolic-ref --short -q HEAD 2^>nul') do set CUR_BRANCH=%%b
if not defined CUR_BRANCH (
  echo ▶ 현재 브랜치가 없습니다. %BRANCH% 브랜치로 생성/전환합니다.
  git checkout -B %BRANCH%
) else (
  echo ▶ 현재 브랜치: %CUR_BRANCH%
  if /i not "%CUR_BRANCH%"=="%BRANCH%" (
    echo ▶ %BRANCH% 브랜치로 전환합니다.
    git checkout -B %BRANCH%
  )
)
echo ✅ 완료
echo.

REM --- 인증/권한 사전 점검 (오프라인/자격 문제 조기 탐지) ----------
echo [3/7] 원격 접근/인증 사전 점검...
echo ----------------------------------------------------------------
git ls-remote --heads origin %BRANCH% >nul 2>&1
if %errorlevel% neq 0 (
  echo ❌ 원격 저장소 접근에 실패했습니다.
  echo 💡 점검:
  echo   1) GitHub 로그인/자격 증명 관리자(Windows Credential Manager) 캐시 확인
  echo   2) 2FA 계정은 PAT(토큰) 필요 - HTTPS push 시 자격 프롬프트에 PAT 사용
  echo   3) REPO_URL 권한/URL 확인: %REPO_URL%
  echo   4) 네트워크/프록시 점검
  echo   5) 최초 push 전에는 원격 브랜치가 없을 수 있으니 무시 가능
  echo.
) else (
  echo ✅ 원격 저장소 접근 OK
)
echo.

REM --- 변경 스테이징/커밋 -----------------------------------------
echo [4/7] 변경 스테이징/커밋...
echo ----------------------------------------------------------------
git add -A
for /f "delims=" %%c in ('git status --porcelain') do set HAS_CHANGES=1
if not defined HAS_CHANGES (
  echo ▶ 커밋할 변경 사항이 없습니다.
) else (
  git commit -m "🔁 Auto-deploy: workspace sync (%date% %time%)"
)
echo ✅ 완료
echo.

REM --- 안전한 pull(rebase) ----------------------------------------
echo [5/7] 원격과 동기화(pull --rebase)...
echo ----------------------------------------------------------------
git fetch origin %BRANCH% >nul 2>&1
if %errorlevel% equ 0 (
  git pull --rebase origin %BRANCH%
  if %errorlevel% neq 0 (
    echo ⚠ rebase 충돌 발생. 수동 해결 후 다시 실행하세요.
    goto :end
  )
) else (
  echo ▶ 원격 브랜치가 아직 없거나 접근 불가. pull 생략.
)
echo ✅ 완료
echo.

REM --- push --------------------------------------------------------
echo [6/7] GitHub 업로드(push)...
echo ----------------------------------------------------------------
git push -u origin %BRANCH%
if %errorlevel% neq 0 (
  echo.
  echo ❌ 업로드 실패
  echo └─ 흔한 원인: 인증 실패(자격/토큰), 권한 부족, 저장소/브랜치 미존재
  echo 💡 해결:
  echo    - Windows 자격 증명 관리자: github.com 항목 제거 후 재시도(프롬프트에 PAT 입력)
  echo    - PAT 생성(Scopes: repo) 후 push 시 비밀번호 대신 PAT 사용
  echo    - 브라우저에서 리포지토리 권한/URL 확인: %REPO_URL%
  echo.
  goto :end
)
echo ✅ push 성공
echo.

REM --- 완료 안내 ---------------------------------------------------
echo [7/7] 배포 완료 및 정보
echo ----------------------------------------------------------------
echo 🔗 저장소: %REPO_URL%
echo 📅 완료 시각: %date% %time%
echo ================================================================
echo ✅ AI-WORKSPACE가 성공적으로 GitHub에 업로드되었습니다!
echo ================================================================
echo.

:end
pause
endlocal
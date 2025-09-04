@echo off
chcp 65001 >nul
title AI-WORKSPACE → GitHub 자동 업로드
color 0A
cls

echo ================================================================
echo          🚀 AI-WORKSPACE GitHub 자동 업로드 시작
echo ================================================================
echo.

cd /d "C:\Users\8899y\AI-WORKSPACE"
echo 📁 현재 위치: %CD%

echo.
echo [1/6] Git 초기화 확인...
echo ----------------------------------------------------------------
if not exist ".git" (
    echo Git 저장소 초기화 중...
    git init
    git remote add origin https://github.com/manwonyori/-AI-WORKSPACE.git
    echo ✅ Git 저장소 초기화 완료
) else (
    echo ✅ Git 저장소가 이미 존재합니다
)

echo.
echo [2/6] 원격 저장소 연결 확인...
echo ----------------------------------------------------------------
git remote -v
if %errorlevel% neq 0 (
    echo 원격 저장소 추가 중...
    git remote add origin https://github.com/manwonyori/-AI-WORKSPACE.git
)

echo.
echo [3/6] Git 상태 확인...
echo ----------------------------------------------------------------
git status

echo.
echo [4/6] 모든 변경사항 추가...
echo ----------------------------------------------------------------
git add .
echo ✅ 모든 파일이 스테이징 되었습니다

echo.
echo [5/6] 커밋 생성...
echo ----------------------------------------------------------------
git commit -m "🤖 AI-WORKSPACE Complete Upload: Genesis Ultimate (339 products) + Cafe24 Automation + MCP Integration - %date% %time%"

echo.
echo [6/6] GitHub 업로드...
echo ----------------------------------------------------------------
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ================================================================
    echo ✅ AI-WORKSPACE가 성공적으로 GitHub에 업로드되었습니다!
    echo ================================================================
    echo.
    echo 🎯 업로드된 내용:
    echo ----------------------------------------------------------------
    echo ✅ Genesis Ultimate: 339개 제품 상세페이지 시스템
    echo ✅ Cafe24 Automation: CUA 통합 자동화 시스템
    echo ✅ MCP SuperAssistant: 통합 AI 도구
    echo ✅ 모든 설정 파일 및 스크립트
    echo.
    echo 🔗 저장소 확인: https://github.com/manwonyori/-AI-WORKSPACE
    echo.
) else (
    echo.
    echo ❌ 업로드 중 오류가 발생했습니다.
    echo 💡 해결 방법:
    echo 1. GitHub 로그인 상태 확인
    echo 2. 네트워크 연결 확인
    echo 3. 저장소 권한 확인
    echo.
)

echo 📊 업로드 완료 시간: %date% %time%
echo ================================================================
pause
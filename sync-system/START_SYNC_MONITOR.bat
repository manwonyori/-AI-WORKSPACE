@echo off
title MCP Sync Monitor - ChatGPT 실시간 동기화
cd /d C:\Users\8899y\AI-WORKSPACE\sync-system

echo ========================================
echo   MCP 실시간 동기화 모니터 시작
echo ========================================
echo.
echo ChatGPT가 수정한 파일을 자동으로 감지하고
echo Git에 자동 커밋합니다.
echo.

REM watchdog 설치 확인
pip show watchdog >nul 2>&1
if %errorlevel% neq 0 (
    echo watchdog 설치 중...
    pip install watchdog aiohttp
)

REM 동기화 모니터 실행
python mcp_sync_monitor.py

pause
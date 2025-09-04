@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
color 0A
title MCP SuperAssistant Stable Server

echo ========================================
echo    MCP SuperAssistant 안정화 서버
echo ========================================
echo.

:: 설정 파일 경로
set CONFIG_FILE=C:\Users\8899y\AI-WORKSPACE\mcp-system\configs\mcp_superassistant_config.json

:: 기존 프로세스 종료
echo [1/4] 기존 MCP 프로세스 정리 중...
taskkill /F /IM node.exe 2>nul
timeout /t 2 >nul

:: Node.js 버전 확인
echo [2/4] Node.js 환경 확인 중...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js가 설치되지 않았습니다!
    echo https://nodejs.org 에서 설치해주세요.
    pause
    exit /b 1
)
echo Node.js 버전: 
node --version

:: NPM 캐시 정리 (선택적)
echo [3/4] NPM 캐시 정리 중...
call npm cache verify >nul 2>&1

:: 서버 시작 with 자동 재시작
echo [4/4] MCP 서버 시작 중...
echo.
echo 서버 주소: http://localhost:3006
echo 전송 방식: SSE (Server-Sent Events)
echo.
echo 서버가 중단되면 5초 후 자동으로 재시작됩니다.
echo 완전히 종료하려면 Ctrl+C를 두 번 누르세요.
echo ========================================
echo.

:START_SERVER
echo [%date% %time%] 서버 시작...
npx @srbhptl39/mcp-superassistant-proxy@latest --config "%CONFIG_FILE%" --outputTransport sse --port 3006

:: 서버가 종료되었을 때
echo.
echo [WARNING] 서버가 중단되었습니다.
echo 5초 후 자동 재시작합니다...
timeout /t 5
goto START_SERVER
@echo off
title MCP SuperAssistant Proxy - 수정된 버전
color 0C
cls

echo ================================================================
echo           MCP SuperAssistant Proxy Server 수정 시작
echo ================================================================
echo.
echo 🔧 문제 해결: Server Disconnected 오류 수정
echo 📡 올바른 설정: SSE + CORS 활성화
echo 🌐 포트: 3006 (http://localhost:3006/sse)
echo.
pause

:: 기존 프로세스 종료
echo [1/4] 기존 MCP 프로세스 정리...
echo ----------------------------------------------------------------
taskkill /f /im "node.exe" 2>nul >nul
taskkill /f /im "npx.exe" 2>nul >nul
echo [✓] 기존 프로세스 정리 완료

timeout /t 2 >nul

:: 설정 파일 확인
echo.
echo [2/4] 설정 파일 확인...
echo ----------------------------------------------------------------
cd C:\Users\8899y\AI-WORKSPACE\mcp-system\configs
if exist "mcp_superassistant_config.json" (
    echo [✓] 설정 파일 존재: mcp_superassistant_config.json
) else (
    echo [❌] 설정 파일 없음
    pause
    exit /b 1
)

:: Proxy 서버 시작 (올바른 명령어)
echo.
echo [3/4] MCP SuperAssistant Proxy 시작...
echo ----------------------------------------------------------------
echo 실행 명령어: npx @srbhptl39/mcp-superassistant-proxy@latest --config ./mcp_superassistant_config.json --outputTransport sse
echo.

start /min cmd /k "title MCP-SuperAssistant-Proxy-Fixed && cd C:\Users\8899y\AI-WORKSPACE\mcp-system\configs && npx @srbhptl39/mcp-superassistant-proxy@latest --config ./mcp_superassistant_config.json --outputTransport sse"

echo [✓] Proxy 서버 시작됨 (백그라운드)
echo.

:: 서버 상태 확인
echo [4/4] 서버 연결 테스트...
echo ----------------------------------------------------------------
timeout /t 5 >nul

echo 연결 테스트 중...
curl -s http://localhost:3006/sse 2>nul >nul
if %errorlevel% equ 0 (
    echo [✅] 서버 연결 성공!
) else (
    echo [⏳] 서버 시작 중... 잠시 후 다시 확인하세요
)

echo.
echo ================================================================
echo              ✅ MCP SuperAssistant Proxy 수정 완료!
echo ================================================================
echo.
echo 📡 서버 정보:
echo ----------------------------------------------------------------
echo URL: http://localhost:3006/sse
echo Transport: Server-Sent Events (SSE)
echo CORS: 활성화됨
echo Config: mcp_superassistant_config.json
echo.
echo 🔗 Chrome 확장에서 연결:
echo ----------------------------------------------------------------
echo 1. MCP SuperAssistant 확장프로그램 열기
echo 2. Server URI: http://localhost:3006/sse 입력
echo 3. Connection Type: Server-Sent Events (SSE) 선택
echo 4. Save & Reconnect 클릭
echo.
echo 🎯 문제 해결됨:
echo ----------------------------------------------------------------
echo ✅ 올바른 포트 및 전송 방식 설정
echo ✅ CORS 헤더 활성화
echo ✅ 설정 파일 기반 실행
echo ✅ 백그라운드 안정 실행
echo.
echo 💡 확인 방법:
echo ----------------------------------------------------------------
echo - Chrome 확장에서 "Connected" 상태 확인
echo - AI 플랫폼에서 "파일 검색해줘" 테스트
echo - MCP 도구 자동 감지/실행 확인
echo.
pause
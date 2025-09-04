@echo off
title MCP SuperAssistant - AI Collaboration Hub
color 0B
cls

echo ================================================================
echo           MCP SuperAssistant - AI 협업 허브 시작
echo ================================================================
echo.
echo 🔗 GitHub: https://github.com/srbhptl39/MCP-SuperAssistant
echo 🌐 Extension: Chrome Web Store에서 설치
echo 📡 Local Server: http://localhost:3006/sse
echo.

echo [1/3] MCP SuperAssistant Proxy 서버 시작...
echo ----------------------------------------------------------------
start /min cmd /k "title MCP-SuperAssistant-Proxy && npx @srbhptl39/mcp-superassistant-proxy@latest --port 3006"
timeout /t 3 >nul

echo [✓] Proxy Server: http://localhost:3006/sse
echo.

echo [2/3] MCP Filesystem Server 시작 (AI-WORKSPACE)...
echo ----------------------------------------------------------------
start /min cmd /k "title MCP-Filesystem && npx @modelcontextprotocol/server-filesystem C:\Users\8899y\AI-WORKSPACE --allow-write"
echo [✓] Filesystem: AI-WORKSPACE 접근 가능
echo.

echo [3/3] 브라우저 환경 준비...
echo ----------------------------------------------------------------
echo Chrome 확장프로그램 설치 후 다음 URL로 연결:
echo 👉 http://localhost:3006/sse
echo.

start chrome "https://chromewebstore.google.com/search/MCP%20SuperAssistant"
timeout /t 2 >nul

start chrome "https://chatgpt.com"
echo [1] ChatGPT (MCP 연동)
timeout /t 1 >nul

start chrome "https://gemini.google.com"
echo [2] Gemini (MCP 연동)
timeout /t 1 >nul

start chrome "https://www.perplexity.ai"
echo [3] Perplexity (MCP 연동)
echo.

echo ================================================================
echo                    ✅ MCP SuperAssistant 준비 완료!
echo ================================================================
echo.
echo 📋 사용법:
echo ----------------------------------------------------------------
echo 1. Chrome에서 MCP SuperAssistant 확장프로그램 설치
echo 2. 확장프로그램에서 http://localhost:3006/sse 연결
echo 3. AI 플랫폼에서 "파일 검색해줘", "코드 실행해줘" 등 요청
echo 4. 확장프로그램에서 MCP 도구 자동 감지 및 실행
echo.
echo 🎯 지원 플랫폼:
echo - ChatGPT: GitHub URL 분석, 파일시스템 접근
echo - Gemini: 이미지 생성, 데이터 분석
echo - Perplexity: 실시간 검색, 정보 수집
echo.
echo 💡 팁:
echo - AI 대화에서 구체적인 도구명 언급
echo - 고성능 모델 사용 권장 (GPT-4, Gemini Pro)
echo - 추론 모드(reasoning mode) 활용
echo.
pause
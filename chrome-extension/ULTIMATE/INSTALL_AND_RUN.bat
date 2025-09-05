@echo off
echo ========================================================
echo   AI ULTIMATE AUTO-RELAY SYSTEM v3.0
echo   완벽한 자동 설치 및 실행 시스템
echo ========================================================
echo.

:: 색상 설정
color 0A

:: 현재 디렉토리 확인
echo [1/6] 현재 위치 확인...
echo 경로: %CD%
echo.

:: Chrome 프로세스 확인
echo [2/6] Chrome 브라우저 확인...
tasklist | find "chrome.exe" >nul
if %errorlevel% neq 0 (
    echo Chrome이 실행되지 않았습니다. Chrome을 시작합니다...
    start chrome
    timeout /t 5 /nobreak >nul
) else (
    echo Chrome이 이미 실행 중입니다.
)
echo.

:: Extension 페이지 열기
echo [3/6] Chrome Extensions 페이지 열기...
start chrome "chrome://extensions"
timeout /t 3 /nobreak >nul
echo.

:: 설치 안내
echo [4/6] Extension 설치 안내
echo ========================================================
echo.
echo 다음 단계를 따라주세요:
echo.
echo 1. Chrome Extensions 페이지가 열렸습니다
echo 2. 우측 상단의 "개발자 모드" 토글을 켜주세요
echo 3. "압축해제된 확장 프로그램을 로드합니다" 클릭
echo 4. 이 폴더를 선택하세요:
echo    %CD%
echo 5. "폴더 선택" 클릭
echo.
echo ========================================================
echo.
echo 설치를 완료하셨으면 아무 키나 누르세요...
pause >nul
echo.

:: AI 플랫폼 열기
echo [5/6] AI 플랫폼 열기...
echo.
echo ChatGPT 열기...
start chrome "https://chatgpt.com"
timeout /t 3 /nobreak >nul

echo Claude 열기...
start chrome "https://claude.ai"
timeout /t 3 /nobreak >nul

echo Gemini 열기...
start chrome "https://gemini.google.com"
timeout /t 3 /nobreak >nul

echo Perplexity 열기...
start chrome "https://perplexity.ai"
timeout /t 3 /nobreak >nul
echo.

:: 모니터 대시보드 열기
echo [6/6] 모니터 대시보드 준비...
echo.
echo ========================================================
echo.
echo 모든 설정이 완료되었습니다!
echo.
echo Extension 아이콘을 클릭하여 사용을 시작하세요.
echo.
echo 주요 기능:
echo - 모든 탭 열기: 모든 AI 플랫폼 자동 열기
echo - 상태 확인: 각 플랫폼 연결 상태 확인
echo - 전체 테스트: 모든 기능 자동 테스트
echo - 메시지 전송: 모든 AI에 동시 메시지 전송
echo - 자동 릴레이: AI 간 자동 대화 릴레이
echo - 모니터: 실시간 모니터링 대시보드
echo.
echo ========================================================
echo.
echo 아무 키나 누르면 종료됩니다...
pause >nul
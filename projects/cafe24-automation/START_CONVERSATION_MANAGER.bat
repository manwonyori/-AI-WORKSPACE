@echo off
chcp 65001 > nul
cls
echo =======================================
echo   Claude 대화 지속 저장 시스템
echo =======================================
echo.

cd /d "C:\Users\8899y\CUA-MASTER\core"

echo [1] 대화 저장 시스템 초기화
echo [2] 자동 저장 스케줄러 시작
echo [3] 이전 대화 컨텍스트 로드
echo [4] 대화 검색
echo [5] 마크다운 내보내기
echo [6] 백업 생성
echo [0] 종료
echo.

set /p choice="원하는 작업을 선택하세요: "

if "%choice%"=="1" (
    echo.
    echo 대화 저장 시스템 초기화 중...
    echo =======================================
    python claude_conversation_manager.py
) else if "%choice%"=="2" (
    echo.
    echo 자동 저장 스케줄러 시작 중...
    echo =======================================
    python conversation_auto_saver.py
) else if "%choice%"=="3" (
    echo.
    echo 이전 대화 컨텍스트 로드 중...
    echo =======================================
    python conversation_bridge.py
) else if "%choice%"=="4" (
    echo.
    set /p keyword="검색할 키워드를 입력하세요: "
    echo 대화 검색 중...
    python -c "from claude_conversation_manager import ClaudeConversationManager; m=ClaudeConversationManager(); m.search_conversations('%keyword%')"
) else if "%choice%"=="5" (
    echo.
    set /p session="세션 ID를 입력하세요: "
    echo 마크다운 내보내기 중...
    python -c "from claude_conversation_manager import ClaudeConversationManager; m=ClaudeConversationManager(); m.export_conversation_to_markdown('%session%')"
) else if "%choice%"=="6" (
    echo.
    echo 백업 생성 중...
    echo =======================================
    mkdir "..\backup\conversations" 2>nul
    copy "..\data\claude_conversations.db" "..\backup\conversations\backup_%date:~0,4%%date:~5,2%%date:~8,2%.db"
    echo 백업 완료!
) else if "%choice%"=="0" (
    echo.
    echo 프로그램을 종료합니다.
    exit /b
) else (
    echo.
    echo 잘못된 선택입니다.
)

echo.
echo =======================================
echo 작업 완료
echo.
pause

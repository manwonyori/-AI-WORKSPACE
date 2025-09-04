@echo off
chcp 65001 > nul
title 🎨 궁극의 AI 이미지 생성 자동화 시스템 MVP 🎨

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║        🎨 궁극의 AI 이미지 생성 자동화 시스템 MVP 🎨          ║
echo ║                                                              ║
echo ║  통합 시스템:                                                ║
echo ║  • CUA-MASTER (140+ AI 에이전트)                            ║
echo ║  • AI Council (다중 AI 협업)                                ║
echo ║  • Cafe24 자동 연동                                         ║
echo ║  • SuperClaude 시스템                                       ║
echo ║                                                              ║
echo ║  API 지원:                                                   ║
echo ║  • OpenAI (GPT-4, DALL-E 3) ✅                             ║
echo ║  • Anthropic (Claude 3) ✅                                  ║
echo ║  • Google (Gemini 2.0 Flash) ✅                             ║
echo ║  • Perplexity AI ✅                                         ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Python 환경 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되지 않았거나 PATH에 추가되지 않았습니다.
    echo 📥 Python을 설치한 후 다시 실행해주세요.
    pause
    exit /b 1
)

echo 🔍 Python 환경 확인 완료
echo.

:: 필수 패키지 설치 확인
echo 📦 필수 패키지 설치 중...
pip install requests pathlib asyncio threading queue logging hashlib base64 concurrent.futures >nul 2>&1

echo ✅ 패키지 설치 완료
echo.

:: 시스템 초기화
echo 🚀 시스템 초기화 중...
echo.

:: 출력 디렉터리 생성
if not exist "C:\Users\8899y\CUA-MASTER\output\images" (
    mkdir "C:\Users\8899y\CUA-MASTER\output\images"
    echo 📁 출력 디렉터리 생성 완료
)

if not exist "C:\Users\8899y\CUA-MASTER\logs" (
    mkdir "C:\Users\8899y\CUA-MASTER\logs"
    echo 📁 로그 디렉터리 생성 완료
)

echo.
echo 🎯 시스템 시작 중...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

:: 메인 시스템 실행
cd /d "C:\Users\8899y\CUA-MASTER\modules\nano_banana"
python ultimate_image_automation_system.py

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 🏁 시스템이 종료되었습니다.
echo.

:: 결과 요약
echo 📊 실행 결과 요약:
echo   • 생성된 이미지: C:\Users\8899y\CUA-MASTER\output\images\
echo   • 로그 파일: C:\Users\8899y\CUA-MASTER\logs\image_automation.log
echo   • 메타데이터: *_metadata.json 파일들
echo.

:: 추가 실행 옵션
echo.
echo 🔧 추가 실행 옵션:
echo.
echo 1️⃣  다시 실행하려면 'R' + Enter
echo 2️⃣  로그 확인하려면 'L' + Enter  
echo 3️⃣  출력 폴더 열려면 'O' + Enter
echo 4️⃣  종료하려면 'Q' + Enter
echo.

:choice_loop
set /p choice=선택하세요 (R/L/O/Q): 

if /i "%choice%"=="R" goto restart
if /i "%choice%"=="L" goto show_logs
if /i "%choice%"=="O" goto open_output
if /i "%choice%"=="Q" goto exit

echo ❌ 잘못된 선택입니다. 다시 입력해주세요.
goto choice_loop

:restart
echo.
echo 🔄 시스템을 다시 시작합니다...
echo.
goto :main_loop

:show_logs
echo.
echo 📋 최근 로그 내용:
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if exist "C:\Users\8899y\CUA-MASTER\logs\image_automation.log" (
    type "C:\Users\8899y\CUA-MASTER\logs\image_automation.log"
) else (
    echo 📄 아직 로그 파일이 생성되지 않았습니다.
)
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
pause
goto choice_loop

:open_output
echo.
echo 📂 출력 폴더를 엽니다...
if exist "C:\Users\8899y\CUA-MASTER\output\images" (
    start "" "C:\Users\8899y\CUA-MASTER\output\images"
) else (
    echo ❌ 출력 폴더가 존재하지 않습니다.
)
goto choice_loop

:exit
echo.
echo 👋 이용해 주셔서 감사합니다!
echo 📧 문의사항: CUA-MASTER System
echo.
timeout /t 3 /nobreak >nul
exit

:main_loop
goto :eof
@echo off
chcp 65001 > nul
color 0E
title 초기 설치 프로그램

echo ============================================================
echo              한국 이커머스 시스템 초기 설치
echo ============================================================
echo.
echo 이 프로그램은 시스템을 처음 설치할 때 실행합니다.
echo.

REM Python 확인
echo [1/5] Python 확인...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo 오류: Python이 설치되지 않았습니다!
    echo https://www.python.org 에서 Python 3.8 이상을 설치해주세요.
    pause
    exit /b
)
python --version
echo Python 확인 완료!
echo.

REM 폴더 생성
echo [2/5] 필수 폴더 생성...
if not exist "data\input" mkdir "data\input"
if not exist "data\output" mkdir "data\output"
if not exist "logs" mkdir "logs"
if not exist "backup" mkdir "backup"
echo 폴더 생성 완료!
echo.

REM 패키지 설치
echo [3/5] 필수 패키지 설치...
pip install python-dotenv
echo.
echo 선택 패키지를 설치하시겠습니까? (AI 기능용)
echo OpenAI, Anthropic, Google Gemini API 패키지
set /p install_optional=(Y/N): 
if /i "%install_optional%"=="Y" (
    pip install openai anthropic google-generativeai
)
echo 패키지 설치 완료!
echo.

REM .env 파일 생성
echo [4/5] 환경 설정 파일 생성...
if not exist .env (
    echo # API 키 설정 (선택사항) > .env
    echo # 아래에 실제 API 키를 입력하세요 >> .env
    echo. >> .env
    echo # OpenAI API >> .env
    echo OPENAI_API_KEY= >> .env
    echo. >> .env
    echo # Anthropic Claude API >> .env
    echo ANTHROPIC_API_KEY= >> .env
    echo. >> .env
    echo # Google Gemini API >> .env
    echo GEMINI_API_KEY= >> .env
    echo .env 파일이 생성되었습니다.
) else (
    echo .env 파일이 이미 존재합니다.
)
echo.

REM 테스트 데이터 확인
echo [5/5] 테스트 데이터 확인...
if exist "data\input\cafe24_test.csv" (
    echo 테스트 데이터가 있습니다.
) else (
    echo 테스트 데이터가 없습니다.
    echo data\input\ 폴더에 CSV 파일을 넣어주세요.
)
echo.

echo ============================================================
echo                    설치 완료!
echo ============================================================
echo.
echo 이제 '시작.bat'을 실행하여 시스템을 사용할 수 있습니다.
echo.
echo API 키를 사용하려면:
echo 1. .env 파일을 메모장으로 열기
echo 2. API 키 입력
echo 3. 저장
echo.
pause
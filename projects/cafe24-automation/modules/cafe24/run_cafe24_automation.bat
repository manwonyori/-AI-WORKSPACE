@echo off
chcp 65001 > nul
cls
echo ========================================
echo   Cafe24 상품 관리 자동화 시스템
echo   239개 상품 일괄 처리
echo ========================================
echo.

REM Python 경로 설정
set PYTHON_PATH=python

REM 작업 디렉토리 이동
cd /d "C:\Users\8899y\CUA-MASTER\modules\cafe24"

echo [1] 전체 워크플로우 실행 (크롤링 → 수정 → 업데이트)
echo [2] 크롤링만 실행
echo [3] 일괄 수정만 실행
echo [4] Cafe24 업데이트만 실행
echo [5] 설정 파일 확인
echo [0] 종료
echo.

set /p choice="실행할 작업을 선택하세요: "

if "%choice%"=="1" (
    echo.
    echo 전체 워크플로우를 시작합니다...
    echo ========================================
    %PYTHON_PATH% main_workflow.py --step all
) else if "%choice%"=="2" (
    echo.
    echo 상품 크롤링을 시작합니다...
    echo ========================================
    %PYTHON_PATH% main_workflow.py --step crawl
) else if "%choice%"=="3" (
    echo.
    echo HTML 일괄 수정을 시작합니다...
    echo ========================================
    %PYTHON_PATH% main_workflow.py --step modify
) else if "%choice%"=="4" (
    echo.
    echo Cafe24 업데이트를 시작합니다...
    echo ========================================
    %PYTHON_PATH% main_workflow.py --step update
) else if "%choice%"=="5" (
    echo.
    echo 설정 파일을 확인합니다...
    echo ========================================
    if exist "config\cafe24_config.json" (
        type "config\cafe24_config.json"
    ) else (
        echo 설정 파일이 없습니다. 먼저 실행하여 생성하세요.
    )
) else if "%choice%"=="0" (
    echo.
    echo 프로그램을 종료합니다.
    exit /b
) else (
    echo.
    echo 잘못된 선택입니다.
)

echo.
echo ========================================
echo 작업이 완료되었습니다.
echo.
pause
@echo off
chcp 65001 > nul
cls
echo =======================================
echo   Claude 카페24 상세페이지 직접 수정
echo =======================================
echo.

cd /d "C:\Users\8899y\CUA-MASTER\modules\cafe24"

echo [1] Selenium 자동화 (권장)
echo [2] UI 키보드 자동화 
echo [3] 기존 HTML 교체 시스템
echo [4] 템플릿 목록 확인
echo [0] 종료
echo.

set /p choice="수정 방법을 선택하세요: "

if "%choice%"=="1" (
    echo.
    echo Selenium 자동화로 상세페이지 수정 중...
    echo =======================================
    python claude_detail_page_editor.py
) else if "%choice%"=="2" (
    echo.
    echo UI 키보드 자동화로 상세페이지 수정 중...
    echo =======================================
    python claude_ui_detail_editor.py
) else if "%choice%"=="3" (
    echo.
    echo 기존 HTML 교체 시스템 실행 중...
    echo =======================================
    python core/html_content_replacer.py
) else if "%choice%"=="4" (
    echo.
    echo 사용 가능한 HTML 템플릿 목록:
    echo =======================================
    dir complete_content\html /s /b
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
echo 상세페이지 수정 완료
echo.
pause

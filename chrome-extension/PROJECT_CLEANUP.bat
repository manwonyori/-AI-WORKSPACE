@echo off
chcp 65001 >nul
echo.
echo ===============================================
echo 🧹 AI Workspace Extension 프로젝트 정리
echo ===============================================
echo.

cd /d "C:\Users\8899y\AI-WORKSPACE\chrome-extension"

echo 📋 현재 디렉토리: %CD%
echo.

echo 📂 현재 파일 목록:
echo -----------------------------------------------
dir /b *.js *.json *.html *.md *.bat
echo.

echo 🗂️ 파일 분류 및 정리 시작...
echo -----------------------------------------------

REM 성공한 핵심 파일들을 final 폴더로 이동
if not exist "final" mkdir final
if not exist "archive" mkdir archive
if not exist "development" mkdir development

echo.
echo ✅ 핵심 성공 파일들 (final 폴더):
echo -----------------------------------------------

REM 핵심 성공 파일들
if exist "chatgpt_unlock_input.js" (
    copy "chatgpt_unlock_input.js" "final\" >nul
    echo   ✅ chatgpt_unlock_input.js - ChatGPT 입력창 복구
)

if exist "gemini_complete_fix.js" (
    copy "gemini_complete_fix.js" "final\" >nul
    echo   ✅ gemini_complete_fix.js - Google AI Studio 완전 복구
)

if exist "complete_mock_extension.js" (
    copy "complete_mock_extension.js" "final\" >nul
    echo   ✅ complete_mock_extension.js - Extension 없이 완전 기능
)

if exist "chrome_runtime_mock.js" (
    copy "chrome_runtime_mock.js" "final\" >nul
    echo   ✅ chrome_runtime_mock.js - Chrome Runtime 시뮬레이션
)

REM Extension 기본 파일들
if exist "manifest.json" (
    copy "manifest.json" "final\" >nul
    echo   ✅ manifest.json - Extension 설정
)

if exist "background.js" (
    copy "background.js" "final\" >nul
    echo   ✅ background.js - Extension 백그라운드
)

if exist "content.js" (
    copy "content.js" "final\" >nul
    echo   ✅ content.js - Content Script
)

echo.
echo 🔧 개발/테스트 파일들 (development 폴더):
echo -----------------------------------------------

REM 개발 과정 파일들
for %%f in (
    chatgpt_direct_test.js
    gemini_direct_test.js
    real_working_fix.js
    gemini_send_button_fix.js
    chatgpt_input_diagnosis.js
    basic_reality_check.js
    minimal_working_test.js
    immediate_fix.js
    extension_loading_fix.js
) do (
    if exist "%%f" (
        move "%%f" "development\" >nul
        echo   🔧 %%f
    )
)

echo.
echo 📜 문서/유틸리티 파일들 (archive 폴더):
echo -----------------------------------------------

REM 문서 및 유틸리티
for %%f in (
    CHECK_EXTENSION_STATUS.bat
    comprehensive_diagnostic.js
    chatgpt_specialized.js
    gemini_specialized.js
    content_v*.js
) do (
    if exist "%%f" (
        move "%%f" "archive\" >nul
        echo   📜 %%f
    )
)

echo.
echo 📊 정리 결과:
echo -----------------------------------------------
echo 📂 final 폴더:
dir /b final 2>nul | find /c /v "" > temp_count.txt
set /p final_count=<temp_count.txt
echo   핵심 파일 %final_count%개

echo 📂 development 폴더:
dir /b development 2>nul | find /c /v "" > temp_count.txt
set /p dev_count=<temp_count.txt
echo   개발 파일 %dev_count%개

echo 📂 archive 폴더:
dir /b archive 2>nul | find /c /v "" > temp_count.txt
set /p archive_count=<temp_count.txt
echo   문서 파일 %archive_count%개

del temp_count.txt >nul 2>&1

echo.
echo 🎯 사용법 가이드:
echo -----------------------------------------------
echo 1. final 폴더: 실제 사용할 완성된 파일들
echo 2. development 폴더: 개발 과정에서 만든 테스트 파일들
echo 3. archive 폴더: 참고용 문서 및 유틸리티 파일들
echo.

echo ===============================================
echo ✅ 프로젝트 정리 완료!
echo ===============================================
echo.
pause
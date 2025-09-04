@echo off
chcp 65001 >nul
echo.
echo ===============================================
echo 🔧 Chrome Extension 상태 확인 도구
echo ===============================================
echo.

echo 📋 1단계: 확장 프로그램 디렉토리 확인
echo -----------------------------------------------
cd /d "C:\Users\8899y\AI-WORKSPACE\chrome-extension"
echo 현재 디렉토리: %CD%
echo.

echo 📁 필수 파일 확인:
if exist "manifest.json" (
    echo ✅ manifest.json 존재
) else (
    echo ❌ manifest.json 없음
)

if exist "background.js" (
    echo ✅ background.js 존재
) else (
    echo ❌ background.js 없음
)

if exist "content.js" (
    echo ✅ content.js 존재
) else (
    echo ❌ content.js 없음
)

if exist "popup.html" (
    echo ✅ popup.html 존재
) else (
    echo ❌ popup.html 없음
)
echo.

echo 📋 2단계: manifest.json 버전 확인
echo -----------------------------------------------
if exist "manifest.json" (
    findstr "version" manifest.json
    echo.
)

echo 📋 3단계: Chrome Extensions 페이지 열기
echo -----------------------------------------------
echo Chrome Extensions 페이지를 열고 있습니다...
start chrome://extensions
echo.
timeout /t 3 /nobreak >nul

echo 📋 4단계: 확인할 사항들
echo -----------------------------------------------
echo □ 개발자 모드가 켜져 있는지 확인
echo □ "AI Workspace Controller" 확장이 설치되어 있는지 확인
echo □ 확장이 활성화(enabled)되어 있는지 확인
echo □ 오류가 표시되지 않았는지 확인
echo.

echo 📋 5단계: ChatGPT 페이지에서 테스트
echo -----------------------------------------------
echo ChatGPT 페이지를 열고 있습니다...
start https://chatgpt.com
echo.
timeout /t 3 /nobreak >nul

echo 💡 테스트 방법:
echo 1. ChatGPT 페이지에서 F12 (개발자 도구) 열기
echo 2. Console 탭으로 이동
echo 3. 다음 코드 붙여넣기 및 실행:
echo.
echo    fetch('file:///%CD%/extension_loading_fix.js')
echo      .then(r =^> r.text())
echo      .then(code =^> eval(code));
echo.
echo    또는 직접:
echo    typeof chrome !== 'undefined' ^&^& typeof chrome.runtime !== 'undefined'
echo.

echo 📋 6단계: 문제 해결
echo -----------------------------------------------
echo 만약 chrome.runtime이 없다면:
echo 1. chrome://extensions에서 확장 프로그램 '새로고침' 클릭
echo 2. 개발자 모드 끄고 다시 켜기
echo 3. Chrome 브라우저 재시작
echo 4. 확장 프로그램 삭제 후 다시 설치
echo.

echo ===============================================
echo 🎯 확인 완료 후 아무 키나 누르세요
echo ===============================================
pause >nul
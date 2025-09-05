@echo off
echo.
echo ==========================================
echo Chrome Extension 설치 가이드
echo ==========================================
echo.
echo 1. Chrome을 열고 주소창에 입력:
echo    chrome://extensions/
echo.
echo 2. 우측 상단의 "개발자 모드" 스위치를 켜기
echo.
echo 3. "압축해제된 확장 프로그램 로드" 버튼 클릭
echo.
echo 4. 다음 폴더 선택:
echo    %~dp0
echo.
echo 5. "폴더 선택" 버튼 클릭
echo.
echo ==========================================
echo Extension 경로: %~dp0
echo ==========================================
echo.
echo 설치 후 확인사항:
echo - Extension 이름: AI Workspace Controller
echo - 버전: 1.4.1
echo - 권한: activeTab, scripting, storage 등
echo.
pause

REM Chrome Extensions 페이지 자동 열기
start chrome "chrome://extensions/"

echo.
echo Chrome Extensions 페이지가 열렸습니다.
echo 위의 4단계를 따라 설치해주세요.
echo.
pause
@echo off
echo =======================================
echo      포토샵 자동화 시스템 시작
echo =======================================

cd /d "C:\Users\8899y\CUA-MASTER\scripts"

echo [1] 기본 자동화 실행 중...
start "" "photoshop_automation.jsx"
timeout /t 3 /nobreak > nul

echo [2] Python 컨트롤러 실행 중...
python photoshop_controller.py

echo.
echo =======================================
echo      자동화 작업 완료
echo =======================================
echo 결과 파일 위치: C:\Users\8899y\CUA-MASTER\output\
echo.
pause

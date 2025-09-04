@echo off
title Quick GitHub Sync
echo Syncing to GitHub...
echo.

cd C:\Users\8899y\genesis_ultimate

:: 현재 상태 확인
git status

echo.
echo 커밋 메시지 입력 (엔터 = 자동 메시지):
set /p msg=
if "%msg%"=="" set msg=Auto sync: %date% %time%

:: 모든 변경사항 추가 및 커밋
git add .
git commit -m "%msg%"

:: GitHub에 푸시
git push origin main || git push origin master

echo.
echo ✅ GitHub 동기화 완료!
echo.
echo URL 확인:
gh repo view --web --no-browser 2>nul || echo https://github.com/YOUR_USERNAME/genesis_ultimate
echo.
pause
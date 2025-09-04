@echo off
chcp 65001 > nul
color 0C
title 메뉴 테스트

:메뉴
cls
echo 메뉴 테스트
echo [1] 옵션 1
echo [2] 옵션 2
echo [3] 종료
echo.
set /p choice=선택: 

if "%choice%"=="1" echo 옵션 1 선택됨 && pause && goto 메뉴
if "%choice%"=="2" echo 옵션 2 선택됨 && pause && goto 메뉴
if "%choice%"=="3" goto 종료

goto 메뉴

:종료
echo 시스템을 종료합니다...
pause
exit
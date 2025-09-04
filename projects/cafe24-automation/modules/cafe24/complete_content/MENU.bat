@echo off
chcp 65001 > nul
title 📋 Cafe24 Complete Content - 메인 메뉴

:menu
cls
echo.
echo ================================================
echo     CAFE24 COMPLETE CONTENT SYSTEM
echo              메인 메뉴 v1.0
echo ================================================
echo.
echo  [1] 🚀 전체 자동 실행 (ALL)
echo  [2] 🖼️  대표이미지만 생성 (1000x1000)
echo  [3] 📝 텍스트 콘텐츠만 생성
echo  [4] 🎨 이미지 워크플로우 실행
echo  [5] 📤 FTP 업로드 실행
echo  [6] 🔄 HTML 최적화 실행
echo  [7] 🧪 단일 제품 테스트
echo  [8] 📊 시스템 상태 확인
echo  [9] 🤖 Claude Bridge 테스트
echo  [0] 종료
echo.
echo ------------------------------------------------
set /p choice="선택하세요 (0-9): "

if "%choice%"=="1" goto run_all
if "%choice%"=="2" goto representative
if "%choice%"=="3" goto content
if "%choice%"=="4" goto image
if "%choice%"=="5" goto ftp
if "%choice%"=="6" goto optimize
if "%choice%"=="7" goto test
if "%choice%"=="8" goto status
if "%choice%"=="9" goto bridge
if "%choice%"=="0" goto exit

echo.
echo ❌ 잘못된 선택입니다!
pause
goto menu

:run_all
echo.
echo 🚀 전체 자동 실행을 시작합니다...
echo.
python MASTER_INTEGRATION_SYSTEM.py run
pause
goto menu

:representative
echo.
echo 🖼️ 대표이미지 생성을 시작합니다...
echo.
python image_size_optimizer.py
pause
goto menu

:content
echo.
echo 📝 텍스트 콘텐츠 생성을 시작합니다...
echo.
python complete_detail_page_system.py
pause
goto menu

:image
echo.
echo 🎨 이미지 워크플로우를 시작합니다...
echo.
python ultimate_image_workflow.py
pause
goto menu

:ftp
echo.
echo 📤 FTP 업로드를 시작합니다...
echo.
python ftp_image_upload_system.py
pause
goto menu

:optimize
echo.
echo 🔄 HTML 최적화를 시작합니다...
echo.
python html_design_optimizer.py
pause
goto menu

:test
echo.
echo 🧪 단일 제품 테스트를 시작합니다...
echo.
python MASTER_INTEGRATION_SYSTEM.py test
pause
goto menu

:status
echo.
echo 📊 시스템 상태를 확인합니다...
echo.
python MASTER_INTEGRATION_SYSTEM.py status
pause
goto menu

:bridge
echo.
echo 🤖 Claude Bridge 테스트를 시작합니다...
echo.
python cafe24_bridge_integration.py
pause
goto menu

:exit
echo.
echo 프로그램을 종료합니다.
echo.
exit
@echo off
chcp 65001 > nul
title ⚡ Cafe24 Quick Start

echo.
echo ================================================
echo     CAFE24 QUICK START
echo     빠른 실행 메뉴
echo ================================================
echo.
echo  [R] 대표이미지 생성 (Representative)
echo  [O] HTML 최적화 (Optimize)
echo  [F] FTP 업로드 (FTP)
echo  [A] 전체 실행 (All)
echo  [M] 메인 메뉴 (Menu)
echo.
echo ------------------------------------------------
set /p quick="빠른 선택 (R/O/F/A/M): "

if /i "%quick%"=="R" (
    echo.
    echo 🖼️ 대표이미지 생성 중...
    python image_size_optimizer.py
) else if /i "%quick%"=="O" (
    echo.
    echo 🔄 HTML 최적화 중...
    python html_design_optimizer.py
) else if /i "%quick%"=="F" (
    echo.
    echo 📤 FTP 업로드 중...
    python ftp_image_upload_system.py
) else if /i "%quick%"=="A" (
    echo.
    echo 🚀 전체 실행 중...
    python MASTER_INTEGRATION_SYSTEM.py run
) else if /i "%quick%"=="M" (
    call MENU.bat
) else (
    echo.
    echo ❌ 잘못된 선택입니다!
)

echo.
pause
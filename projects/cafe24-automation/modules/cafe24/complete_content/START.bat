@echo off
chcp 65001 > nul
title Cafe24 Complete Content System

echo.
echo ================================================
echo     CAFE24 COMPLETE CONTENT SYSTEM
echo ================================================
echo.
echo Select operation mode:
echo.
echo [1] Interactive Menu
echo [2] Generate Representative Images (1000x1000)
echo [3] Full Auto Run
echo [4] System Test
echo [5] Exit
echo.
echo ------------------------------------------------
set /p mode="Enter choice (1-5): "

if "%mode%"=="1" (
    call MENU_FIXED.bat
) else if "%mode%"=="2" (
    echo.
    echo Generating representative images...
    python image_size_optimizer.py
    pause
) else if "%mode%"=="3" (
    echo.
    echo Starting full auto run...
    python MASTER_INTEGRATION_SYSTEM.py run
    pause
) else if "%mode%"=="4" (
    echo.
    echo Running system test...
    python test_system.py
    pause
) else if "%mode%"=="5" (
    exit
) else (
    echo.
    echo Invalid selection!
    pause
    goto :eof
)
@echo off
chcp 65001 > nul
title Cafe24 Complete Content - Main Menu

:menu
cls
echo.
echo ================================================
echo     CAFE24 COMPLETE CONTENT SYSTEM
echo              Main Menu v1.0
echo ================================================
echo.
echo  [1] Full Auto Run (ALL)
echo  [2] Representative Images Only (1000x1000)
echo  [3] Text Content Only
echo  [4] Image Workflow Run
echo  [5] FTP Upload Run
echo  [6] HTML Optimization Run
echo  [7] Single Product Test
echo  [8] System Status Check
echo  [9] Claude Bridge Test
echo  [0] Exit
echo.
echo ------------------------------------------------
set /p choice="Select (0-9): "

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
echo Invalid selection!
pause
goto menu

:run_all
echo.
echo Starting full auto run...
echo.
python MASTER_INTEGRATION_SYSTEM.py run
pause
goto menu

:representative
echo.
echo Starting representative image generation...
echo.
python image_size_optimizer.py
pause
goto menu

:content
echo.
echo Starting text content generation...
echo.
python complete_detail_page_system.py
pause
goto menu

:image
echo.
echo Starting image workflow...
echo.
python ultimate_image_workflow.py
pause
goto menu

:ftp
echo.
echo Starting FTP upload...
echo.
python ftp_image_upload_system.py
pause
goto menu

:optimize
echo.
echo Starting HTML optimization...
echo.
python html_design_optimizer.py
pause
goto menu

:test
echo.
echo Starting single product test...
echo.
python MASTER_INTEGRATION_SYSTEM.py test
pause
goto menu

:status
echo.
echo Checking system status...
echo.
python test_system.py
pause
goto menu

:bridge
echo.
echo Starting Claude Bridge test...
echo.
python cafe24_bridge_integration.py
pause
goto menu

:exit
echo.
echo Exiting program.
echo.
exit
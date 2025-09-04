@echo off
chcp 65001 > nul
title Quick Run - Cafe24 Complete Content

if "%1"=="" goto menu
if /i "%1"=="test" goto test
if /i "%1"=="rep" goto representative
if /i "%1"=="all" goto all
if /i "%1"=="menu" goto menu
goto invalid

:menu
echo.
echo ========================================
echo     QUICK RUN COMMANDS
echo ========================================
echo.
echo Usage: RUN.bat [command]
echo.
echo Commands:
echo   test  - Run system test
echo   rep   - Generate representative images
echo   all   - Run full workflow
echo   menu  - Show interactive menu
echo.
echo Examples:
echo   RUN.bat test
echo   RUN.bat rep
echo   RUN.bat all
echo.
pause
exit

:test
echo Running system test...
python test_system.py
pause
exit

:representative
echo Generating representative images...
python image_size_optimizer.py
pause
exit

:all
echo Running full workflow...
python MASTER_INTEGRATION_SYSTEM.py run
pause
exit

:invalid
echo Invalid command: %1
echo.
echo Valid commands: test, rep, all, menu
pause
exit
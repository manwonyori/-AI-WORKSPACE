@echo off
setlocal enableextensions enabledelayedexpansion
chcp 65001 >nul

REM ============================================================================
REM  AI-WORKSPACE - Integrated Work Environment (Robust Menu Version)
REM  - ASCII-only (no emojis)
REM  - Safe pathing via %~dp0
REM  - CHOICE-based menu + loop + error handling
REM ============================================================================

title AI-WORKSPACE - Integrated Work Environment
color 0A

REM Base directory = this script's folder
set "BASE=%~dp0"
pushd "%BASE%" >nul 2>&1

:menu
cls
echo ================================================================
echo                    AI-WORKSPACE Main Menu
echo ================================================================
echo.
echo  Projects:
echo   [1] Genesis Ultimate (339 Product Detail Pages)
echo   [2] Cafe24 Automation (CUA System)
echo   [3] Business Automation
echo.
echo  Tools:
echo   [4] MCP Integrated System
echo   [5] AI Collaboration Tools
echo   [6] GitHub Integration
echo.
echo  [X] Exit
echo ---------------------------------------------------------------
choice /C 123456X /N /M "Choose (1-6 or X): "
set "ERR=%ERRORLEVEL%"
echo.

REM ERRORLEVEL mapping: 1->"1", 2->"2", ..., 7->"X"
if %ERR%==1 goto opt1
if %ERR%==2 goto opt2
if %ERR%==3 goto opt3
if %ERR%==4 goto opt4
if %ERR%==5 goto opt5
if %ERR%==6 goto opt6
if %ERR%==7 goto done

echo [WARN] Invalid selection. Press any key to continue...
pause >nul
goto menu

:opt1
call :OpenDir "projects\genesis-ultimate"
goto menu

:opt2
call :OpenDir "projects\cafe24-automation"
goto menu

:opt3
REM Business Automation path fallback:
if exist "projects\business-automation" (
  call :OpenDir "projects\business-automation"
) else if exist "business-automation" (
  call :OpenDir "business-automation"
) else (
  echo [ERROR] Business Automation directory not found.
  echo        Please create "projects\business-automation" or adjust this script.
  pause
)
goto menu

:opt4
call :OpenDir "mcp-system\scripts"
goto menu

:opt5
call :OpenDir "ai-collaboration\shared"
goto menu

:opt6
call :OpenDir "github-integration\automation"
goto menu

REM ------------------------- helpers ------------------------------
:OpenDir
set "TARGET=%~1"
if not defined TARGET (
  echo [ERROR] No target directory specified.
  pause
  goto :eof
)
if not exist "%BASE%%TARGET%" (
  echo [ERROR] Directory not found: "%TARGET%"
  echo         Base: "%BASE%"
  pause
  goto :eof
)

pushd "%BASE%%TARGET%" >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Failed to enter directory: "%TARGET%"
  pause
  goto :eof
)

echo [INFO] Opened: "%CD%"
REM Choose how to open the workspace:
REM 1) File Explorer:
start "" explorer .
REM 2) VS Code (uncomment if installed):
REM start "" code .

popd >nul 2>&1
goto :eof
REM ---------------------------------------------------------------

:done
popd >nul 2>&1
echo Bye.
endlocal
exit /b 0
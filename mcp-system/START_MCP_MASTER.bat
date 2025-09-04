@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
title MCP SuperAssistant Master Control
color 0E

echo ================================================================
echo          MCP SuperAssistant Master Control Panel
echo                    Stable Version v2.0
echo ================================================================
echo.
echo 실행 옵션을 선택하세요:
echo.
echo [1] 기본 서버 실행 (단순 실행)
echo [2] 자동 재시작 서버 (배치 스크립트)
echo [3] 고급 모니터링 서버 (Python)
echo [4] PowerShell 자동화 서버
echo [5] 로그 파일 보기
echo [6] 모든 MCP 프로세스 종료
echo [Q] 종료
echo.
choice /c 123456Q /n /m "선택: "

if errorlevel 7 goto END
if errorlevel 6 goto KILL_ALL
if errorlevel 5 goto VIEW_LOGS
if errorlevel 4 goto POWERSHELL_MODE
if errorlevel 3 goto PYTHON_MODE
if errorlevel 2 goto BATCH_MODE
if errorlevel 1 goto SIMPLE_MODE

:SIMPLE_MODE
echo.
echo [단순 실행 모드] MCP 서버를 시작합니다...
cd /d "C:\Users\8899y\AI-WORKSPACE"
npx @srbhptl39/mcp-superassistant-proxy@latest --config "C:\Users\8899y\AI-WORKSPACE\mcp-system\configs\mcp_superassistant_config.json" --outputTransport sse --port 3006
goto END

:BATCH_MODE
echo.
echo [자동 재시작 모드] 배치 스크립트를 실행합니다...
call "C:\Users\8899y\AI-WORKSPACE\mcp-system\scripts\START_MCP_STABLE.bat"
goto END

:PYTHON_MODE
echo.
echo [고급 모니터링 모드] Python 모니터를 실행합니다...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python이 설치되지 않았습니다!
    pause
    goto END
)
echo psutil 패키지 설치 확인 중...
pip show psutil >nul 2>&1 || pip install psutil requests
echo.
python "C:\Users\8899y\AI-WORKSPACE\mcp-system\scripts\mcp_monitor.py"
goto END

:POWERSHELL_MODE
echo.
echo [PowerShell 자동화 모드] PowerShell 스크립트를 실행합니다...
powershell -ExecutionPolicy Bypass -File "C:\Users\8899y\AI-WORKSPACE\mcp-system\scripts\MCP_AUTO_RESTART.ps1"
goto END

:VIEW_LOGS
echo.
echo === 최근 로그 파일 목록 ===
echo.
if exist "C:\Users\8899y\AI-WORKSPACE\mcp-system\logs" (
    dir "C:\Users\8899y\AI-WORKSPACE\mcp-system\logs\*.log" /b /o-d 2>nul
    echo.
    echo 로그 파일을 메모장으로 열려면 파일명을 입력하세요 (취소: Enter):
    set /p logfile=
    if not "!logfile!"=="" (
        if exist "C:\Users\8899y\AI-WORKSPACE\mcp-system\logs\!logfile!" (
            notepad "C:\Users\8899y\AI-WORKSPACE\mcp-system\logs\!logfile!"
        ) else (
            echo 파일을 찾을 수 없습니다.
        )
    )
) else (
    echo 로그 디렉토리가 없습니다.
)
pause
goto END

:KILL_ALL
echo.
echo [프로세스 정리] 모든 MCP 관련 프로세스를 종료합니다...
echo.
taskkill /F /IM node.exe 2>nul && echo Node.js 프로세스가 종료되었습니다. || echo 실행 중인 Node.js 프로세스가 없습니다.
taskkill /F /IM npx.exe 2>nul && echo NPX 프로세스가 종료되었습니다. || echo 실행 중인 NPX 프로세스가 없습니다.
echo.
echo 정리가 완료되었습니다.
pause
goto END

:END
echo.
echo 프로그램을 종료합니다.
timeout /t 2 >nul
exit /b
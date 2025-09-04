@echo off
chcp 65001 >nul
title MART 공급업체 관리 시스템

echo ================================================================================
echo                        MART 공급업체 관리 시스템
echo                      사업자등록증 OCR 자동 처리
echo ================================================================================
echo.

REM Python 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo Python이 설치되지 않았습니다. Python 3.8 이상을 설치해주세요.
    pause
    exit /b 1
)

REM 메인 프로그램 실행
python process_business_license.py

pause
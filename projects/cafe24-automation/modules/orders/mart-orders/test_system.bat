@echo off
chcp 65001 >nul
title OCR 시스템 테스트

echo ================================================================================
echo                           OCR 시스템 테스트
echo                    라이브러리 설치 확인 및 기능 테스트
echo ================================================================================
echo.

REM Python 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo Python이 설치되지 않았습니다. Python 3.8 이상을 설치해주세요.
    pause
    exit /b 1
)

REM 테스트 프로그램 실행
python test_ocr_system.py

pause
@echo off
chcp 65001 > nul
title 🚀 Cafe24 Complete Content - 전체 실행

echo.
echo ========================================
echo    CAFE24 COMPLETE CONTENT SYSTEM
echo         전체 자동 실행 모드
echo ========================================
echo.

:: Python 경로 설정
set PYTHON_PATH=python

:: 작업 디렉토리 이동
cd /d "C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content"

echo [1/3] 이미지 최적화 및 대표이미지 생성...
echo ----------------------------------------
%PYTHON_PATH% image_size_optimizer.py
if errorlevel 1 goto error

echo.
echo [2/3] 메인 통합 시스템 실행...
echo ----------------------------------------
%PYTHON_PATH% MASTER_INTEGRATION_SYSTEM.py run
if errorlevel 1 goto error

echo.
echo [3/3] 최종 검증...
echo ----------------------------------------
%PYTHON_PATH% complete_verification.py
if errorlevel 1 goto error

echo.
echo ========================================
echo ✅ 모든 작업이 완료되었습니다!
echo ========================================
echo.
echo 📁 대표이미지: representative_images\
echo 📁 최적화 파일: optimized\
echo 📁 최종 출력: output\
echo.
pause
exit

:error
echo.
echo ❌ 오류가 발생했습니다!
echo.
pause
exit /b 1
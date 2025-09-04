@echo off
echo ========================================
echo     CUA-MASTER SYSTEM LAUNCHER
echo ========================================
echo.

echo [1/4] CUA API 서버 시작...
start /B cmd /c "cd core && python api.py"
timeout /t 3 >nul

echo [2/4] 자동화 스케줄러 시작...
start /B cmd /c "cd automation && python auto_scheduler.py"
timeout /t 2 >nul

echo [3/4] 실시간 모니터링 시작...
start /B cmd /c "cd dashboard && python monitor.py"
timeout /t 2 >nul

echo [4/4] 시스템 체크...
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% == 0 (
    echo.
    echo ✅ CUA-MASTER 시스템 정상 가동!
    echo.
    echo 접속 정보:
    echo   - API: http://localhost:8000
    echo   - API 문서: http://localhost:8000/docs
    echo.
    echo 주요 명령:
    echo   - 송장 처리: curl -X POST http://localhost:8000/task -d "{\"description\":\"송장 자동 처리\"}"
    echo   - 상품 관리: curl -X POST http://localhost:8000/task -d "{\"description\":\"Cafe24 상품 업데이트\"}"
    echo   - AI 협업: curl -X POST http://localhost:8000/task -d "{\"description\":\"AI Council 실행\"}"
) else (
    echo.
    echo ⚠️ API 서버 시작 중... 잠시 후 다시 확인하세요.
)

echo.
echo 종료하려면 Ctrl+C를 누르세요.
pause >nul
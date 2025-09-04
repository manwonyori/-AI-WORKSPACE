@echo off
chcp 65001 > nul
title System Test - Cafe24 Complete Content

echo.
echo ========================================
echo    SYSTEM TEST
echo ========================================
echo.

cd /d "C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content"

echo [1] Running system test...
python test_system.py

echo.
echo [2] Testing image size optimizer...
python -c "from image_size_optimizer import ImageSizeOptimizer; print('[OK] ImageSizeOptimizer ready')"

echo.
echo ========================================
echo Test complete. Check results above.
echo ========================================
echo.
pause
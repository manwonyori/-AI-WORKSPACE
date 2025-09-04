@echo off
echo ========================================
echo AI Platform Browser Automation Tester
echo Using Puppeteer for Real DOM Inspection
echo ========================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if Puppeteer is installed
if not exist node_modules\puppeteer (
    echo Installing Puppeteer...
    npm install puppeteer
)

echo.
echo Starting browser automation tests...
echo.

python test_with_puppeteer.py

echo.
echo ========================================
echo Test completed!
echo Check the screenshots and results file.
echo ========================================
pause
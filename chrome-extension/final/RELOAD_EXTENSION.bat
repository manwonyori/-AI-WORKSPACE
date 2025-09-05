@echo off
echo ========================================
echo   Chrome Extension Reload Helper
echo ========================================
echo.
echo 1. Opening Chrome Extensions page...
start chrome "chrome://extensions/"
echo.
echo 2. Please do the following:
echo    - Click "Reload" button on the extension
echo    - OR Remove and re-add the extension
echo.
echo 3. Test the extension:
echo    - Click the extension icon
echo    - Check if "Start" button is enabled
echo    - Try entering text in relay objective field
echo.
echo 4. For debugging, open:
start chrome "%~dp0test_popup.html"
echo.
echo 5. Check console for errors:
echo    - Right-click extension icon
echo    - Select "Inspect popup"
echo    - Check Console tab
echo.
pause
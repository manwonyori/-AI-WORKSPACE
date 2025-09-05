@echo off
title MCP SuperAssistant - Full Filesystem Access
color 0A
cls

echo ================================================================
echo         MCP SuperAssistant - Full Filesystem Access
echo             Restarting with Extended Permissions
echo ================================================================
echo.

echo [1/4] Stopping existing MCP processes...
taskkill /F /IM "node.exe" /T 2>nul >nul
timeout /t 2 >nul
echo [✓] Previous processes stopped
echo.

echo [2/4] Starting MCP Proxy with updated config...
start /min cmd /k "title MCP-Proxy-FullAccess && npx @srbhptl39/mcp-superassistant-proxy@latest --port 3006 --config C:\Users\8899y\AI-WORKSPACE\mcp-system\configs\mcp_60_servers_config.json"
timeout /t 3 >nul
echo [✓] Proxy started with new configuration
echo.

echo [3/4] Filesystem Access Points:
echo ================================================================
echo 📁 Main Filesystem (filesystem):
echo    Path: C:\Users\8899y (전체 사용자 폴더)
echo    Access: Full Read/Write
echo.
echo 📁 AI Workspace (filesystem-workspace):
echo    Path: C:\Users\8899y\AI-WORKSPACE
echo    Access: Full Read/Write
echo.
echo 📁 Order System (filesystem-orders):
echo    Path: D:\주문취합
echo    Access: Full Read/Write
echo ================================================================
echo.

echo [4/4] Testing filesystem access...
echo.

REM Open Chrome with extension
start chrome "chrome://extensions/"
timeout /t 1 >nul

REM Re-open AI platforms
start chrome "https://chatgpt.com"
start chrome "https://gemini.google.com"
start chrome "https://claude.ai"

echo ================================================================
echo              ✅ Full Access Configuration Active!
echo ================================================================
echo.
echo 🎯 Test Commands:
echo ----------------------------------------------------------------
echo "List all files in my user folder"
echo "Show Desktop folder contents"
echo "Access Documents folder"
echo "Read files from D:\주문취합"
echo "Create a file on Desktop"
echo.
echo 📍 Available Paths:
echo ----------------------------------------------------------------
echo • C:\Users\8899y\Desktop
echo • C:\Users\8899y\Documents
echo • C:\Users\8899y\Downloads
echo • C:\Users\8899y\AI-WORKSPACE
echo • D:\주문취합\주문_배송
echo • Any subfolder in C:\Users\8899y
echo.
echo ⚠️ Security Note:
echo ----------------------------------------------------------------
echo Full filesystem access is enabled. Be careful with:
echo - System files modification
echo - Sensitive data exposure
echo - Large file operations
echo.
echo 💡 Tips:
echo ----------------------------------------------------------------
echo 1. Use specific paths for better performance
echo 2. AI can now access your entire user folder
echo 3. Multiple filesystem servers for different areas
echo.
pause
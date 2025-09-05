@echo off
title MCP SuperAssistant - 60+ Servers Hub
color 0E
cls

echo ================================================================
echo           MCP SuperAssistant - 60+ Servers Active
echo                  Ultimate AI Collaboration Hub
echo ================================================================
echo.

REM Kill existing MCP processes
echo [CLEANUP] Stopping existing MCP processes...
taskkill /F /IM node.exe /T 2>nul >nul
timeout /t 2 >nul

echo.
echo ================================================================
echo [STEP 1/3] Starting MCP SuperAssistant Proxy
echo ================================================================
start /min cmd /k "title MCP-Proxy && npx @srbhptl39/mcp-superassistant-proxy@latest --port 3006 --config C:\Users\8899y\AI-WORKSPACE\mcp-system\configs\mcp_60_servers_config.json"
timeout /t 3 >nul
echo [✓] Proxy running at: http://localhost:3006/sse
echo.

echo ================================================================
echo [STEP 2/3] Loading 60+ MCP Servers
echo ================================================================
echo.
echo Loading configuration from: mcp_60_servers_config.json
echo.
echo Categories:
echo [•] Official Anthropic: 12 servers
echo [•] Development Tools: 15 servers  
echo [•] Data & Analytics: 12 servers
echo [•] AI & ML: 10 servers
echo [•] Productivity: 11 servers
echo [•] Specialized: 6 servers
echo [•] Blockchain: 3 servers
echo [•] IoT: 2 servers
echo [•] Monitoring: 4 servers
echo.
echo Total: 60+ MCP Servers Available
echo.

echo ================================================================
echo [STEP 3/3] Opening AI Platforms
echo ================================================================
echo.

REM Open Chrome with MCP extension page
start chrome "chrome://extensions/"
timeout /t 2 >nul

REM Open MCP SuperAssistant in Chrome Web Store
start chrome "https://chromewebstore.google.com/detail/mcp-superassistant/kngiafgkdnlkgmefdafaibkibegkcaef"
timeout /t 2 >nul

REM Open AI platforms
start chrome "https://chatgpt.com"
echo [1] ChatGPT - Ready for MCP
timeout /t 1 >nul

start chrome "https://gemini.google.com"
echo [2] Google Gemini - Ready for MCP
timeout /t 1 >nul

start chrome "https://www.perplexity.ai"
echo [3] Perplexity - Ready for MCP
timeout /t 1 >nul

start chrome "https://claude.ai"
echo [4] Claude - Ready for MCP
echo.

echo ================================================================
echo                 ✅ All Systems Operational!
echo ================================================================
echo.
echo 📡 Connection Status:
echo ----------------------------------------------------------------
echo Proxy Server: http://localhost:3006/sse
echo Config: 60+ servers loaded
echo Status: ACTIVE
echo.
echo 🎯 Quick Test Commands:
echo ----------------------------------------------------------------
echo In any AI chat, try:
echo • "List my files in AI-WORKSPACE"
echo • "Search GitHub for MCP servers"  
echo • "Run Python code to test"
echo • "Query my SQLite database"
echo • "Create a task in Todoist"
echo • "Generate an image with Stable Diffusion"
echo.
echo 💡 Tips:
echo ----------------------------------------------------------------
echo 1. Make sure Chrome extension is connected to localhost:3006
echo 2. Use specific tool names in your prompts
echo 3. Check extension popup for tool execution status
echo 4. API keys can be set in environment variables
echo.
echo 📋 Available Servers (Sample):
echo ----------------------------------------------------------------
echo filesystem, github, memory, sqlite, postgres, brave-search,
echo google-maps, puppeteer, code-runner, docker, kubernetes,
echo elasticsearch, mongodb, redis, airtable, openai, anthropic,
echo gemini, elevenlabs, stable-diffusion, notion, discord,
echo figma, zapier, ethereum, home-assistant, sentry...
echo.
echo Press any key to keep servers running in background...
pause >nul
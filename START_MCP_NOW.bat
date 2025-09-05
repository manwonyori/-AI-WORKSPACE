@echo off
echo Starting MCP SuperAssistant Server...
echo.
echo Server URL: http://localhost:3006
echo Transport: SSE (Server-Sent Events)
echo.
echo Press Ctrl+C to stop the server
echo ================================
echo.

cd /d "C:\Users\8899y\AI-WORKSPACE"
npx @srbhptl39/mcp-superassistant-proxy@latest --config "C:\Users\8899y\AI-WORKSPACE\mcp-system\configs\mcp_superassistant_config.json" --outputTransport sse --port 3006

pause
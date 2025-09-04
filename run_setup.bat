@echo off
echo ================================================
echo    AI-WORKSPACE Chrome Extension Setup
echo ================================================
echo.

cd /d "C:\Users\8899y\AI-WORKSPACE"

echo [1/6] Creating chrome-extension directory...
if not exist "chrome-extension" mkdir "chrome-extension"

echo [2/6] Creating manifest.json...
call :CreateManifest

echo [3/6] Creating background.js...
call :CreateBackground

echo [4/6] Creating content.js...
call :CreateContent

echo [5/6] Creating popup files...
call :CreatePopup

echo [6/6] Creating icon placeholders...
echo AI > chrome-extension\icon-16.png
echo AI > chrome-extension\icon-48.png
echo AI > chrome-extension\icon-128.png

echo.
echo ================================================
echo    Setup Complete!
echo ================================================
echo.
echo Chrome Extension created at:
echo   %CD%\chrome-extension
echo.
echo Next steps:
echo   1. Open Chrome and go to: chrome://extensions
echo   2. Enable 'Developer mode' (top right)
echo   3. Click 'Load unpacked'
echo   4. Select folder: %CD%\chrome-extension
echo.
pause
goto :eof

:CreateManifest
(
echo {
echo   "manifest_version": 3,
echo   "name": "AI Workspace Sync",
echo   "version": "1.0.0",
echo   "description": "Sync AI platforms with AI-WORKSPACE configuration",
echo   "permissions": [
echo     "activeTab",
echo     "storage"
echo   ],
echo   "host_permissions": [
echo     "https://chatgpt.com/*",
echo     "https://claude.ai/*",
echo     "https://gemini.google.com/*",
echo     "https://www.perplexity.ai/*",
echo     "https://manwonyori.github.io/*"
echo   ],
echo   "background": {
echo     "service_worker": "background.js"
echo   },
echo   "content_scripts": [
echo     {
echo       "matches": [
echo         "https://chatgpt.com/*",
echo         "https://claude.ai/*",
echo         "https://gemini.google.com/*",
echo         "https://www.perplexity.ai/*"
echo       ],
echo       "js": ["content.js"],
echo       "css": ["styles.css"],
echo       "run_at": "document_end"
echo     }
echo   ],
echo   "action": {
echo     "default_popup": "popup.html"
echo   }
echo }
) > chrome-extension\manifest.json
goto :eof

:CreateBackground
(
echo // Background service worker
echo const CONFIG_URL = "https://manwonyori.github.io/-AI-WORKSPACE/ai-config/agents.json";
echo.
echo let currentConfig = null;
echo.
echo async function loadConfig^(^) {
echo   try {
echo     const response = await fetch^(CONFIG_URL^);
echo     currentConfig = await response.json^(^);
echo     chrome.storage.local.set^({ aiConfig: currentConfig }^);
echo     return currentConfig;
echo   } catch ^(error^) {
echo     console.error^("Error loading config:", error^);
echo     return null;
echo   }
echo }
echo.
echo chrome.runtime.onInstalled.addListener^(^(^) =^> {
echo   loadConfig^(^);
echo }^);
echo.
echo chrome.runtime.onMessage.addListener^(^(request, sender, sendResponse^) =^> {
echo   if ^(request.action === "getConfig"^) {
echo     if ^(currentConfig^) {
echo       sendResponse^({ success: true, config: currentConfig }^);
echo     } else {
echo       loadConfig^(^).then^(config =^> {
echo         sendResponse^({ success: !!config, config: config }^);
echo       }^);
echo       return true;
echo     }
echo   }
echo }^);
) > chrome-extension\background.js
goto :eof

:CreateContent
(
echo // Content script
echo ^(function^(^) {
echo   const platform = detectPlatform^(^);
echo.
echo   function detectPlatform^(^) {
echo     const hostname = window.location.hostname;
echo     if ^(hostname.includes^("chatgpt.com"^)^) return "chatgpt";
echo     if ^(hostname.includes^("claude.ai"^)^) return "claude";
echo     if ^(hostname.includes^("gemini.google.com"^)^) return "gemini";
echo     if ^(hostname.includes^("perplexity.ai"^)^) return "perplexity";
echo     return null;
echo   }
echo.
echo   chrome.runtime.sendMessage^({ action: "getConfig" }, ^(response^) =^> {
echo     if ^(response ^&^& response.success^) {
echo       console.log^(`Initialized ${platform}`^);
echo       addStatusIndicator^(^);
echo     }
echo   }^);
echo.
echo   function addStatusIndicator^(^) {
echo     const indicator = document.createElement^("div"^);
echo     indicator.innerHTML = `AI ${platform} Ready`;
echo     indicator.style.cssText = `
echo       position: fixed; bottom: 20px; right: 20px;
echo       background: #4CAF50; color: white; padding: 10px 20px;
echo       border-radius: 20px; z-index: 10000;
echo     `;
echo     document.body.appendChild^(indicator^);
echo     setTimeout^(^(^) =^> { indicator.style.opacity = "0.5"; }, 3000^);
echo   }
echo }^)^(^);
) > chrome-extension\content.js
goto :eof

:CreatePopup
(
echo ^<!DOCTYPE html^>
echo ^<html^>
echo ^<head^>
echo   ^<meta charset="UTF-8"^>
echo   ^<title^>AI Workspace Sync^</title^>
echo   ^<style^>
echo     body { width: 350px; padding: 20px; font-family: system-ui; }
echo     h2 { text-align: center; }
echo     button { padding: 10px; margin: 5px; cursor: pointer; }
echo     #status { padding: 10px; background: #f0f0f0; border-radius: 5px; }
echo   ^</style^>
echo ^</head^>
echo ^<body^>
echo   ^<h2^>AI Workspace Sync^</h2^>
echo   ^<div id="status"^>Ready^</div^>
echo   ^<button id="sync-btn"^>Sync Config^</button^>
echo   ^<button id="status-btn"^>Check Status^</button^>
echo   ^<script src="popup.js"^>^</script^>
echo ^</body^>
echo ^</html^>
) > chrome-extension\popup.html

(
echo document.addEventListener^("DOMContentLoaded", function^(^) {
echo   const statusDiv = document.getElementById^("status"^);
echo   const syncBtn = document.getElementById^("sync-btn"^);
echo   const statusBtn = document.getElementById^("status-btn"^);
echo.
echo   syncBtn.addEventListener^("click", function^(^) {
echo     chrome.runtime.sendMessage^({ action: "reloadConfig" }, function^(response^) {
echo       statusDiv.textContent = response ^&^& response.success ? "Synced!" : "Failed";
echo     }^);
echo   }^);
echo.
echo   statusBtn.addEventListener^("click", function^(^) {
echo     chrome.tabs.query^({ active: true, currentWindow: true }, function^(tabs^) {
echo       const url = new URL^(tabs[0].url^);
echo       let platform = "Unknown";
echo       if ^(url.hostname.includes^("chatgpt"^)^) platform = "ChatGPT";
echo       else if ^(url.hostname.includes^("claude"^)^) platform = "Claude";
echo       statusDiv.textContent = `Platform: ${platform}`;
echo     }^);
echo   }^);
echo }^);
) > chrome-extension\popup.js

echo /* Content styles */ > chrome-extension\styles.css
goto :eof
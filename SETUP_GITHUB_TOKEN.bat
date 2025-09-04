@echo off
echo ======================================
echo GitHub Token Setup for AI-WORKSPACE
echo ======================================
echo.

:: Check if token exists
if "%GITHUB_TOKEN%"=="" (
    echo [ERROR] No GITHUB_TOKEN found!
    echo.
    echo Please follow these steps:
    echo 1. Go to: https://github.com/settings/tokens/new
    echo 2. Create token with 'repo' scope
    echo 3. Run: setx GITHUB_TOKEN "ghp_your_token_here"
    echo.
    pause
    exit /b 1
)

echo Current token: %GITHUB_TOKEN:~0,10%...
echo.

:: Set Git credentials
echo Setting Git credentials...
git config --global user.name "manwonyori"
git config --global user.email "manwonyori@users.noreply.github.com"
git config --global credential.helper store

:: Create credentials file
echo https://manwonyori:%GITHUB_TOKEN%@github.com > %USERPROFILE%\.git-credentials

:: Test connection
echo.
echo Testing GitHub connection...
git ls-remote https://github.com/manwonyori/AI-WORKSPACE.git >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] GitHub connection verified!
) else (
    echo [ERROR] Cannot connect to GitHub repository
    echo Please check:
    echo - Token permissions
    echo - Repository exists
    echo - Internet connection
)

:: Set environment variables for MCP
echo.
echo Setting MCP environment variables...
setx GH_TOKEN "%GITHUB_TOKEN%" >nul 2>&1
setx GITHUB_OWNER "manwonyori" >nul 2>&1  
setx GITHUB_REPO "AI-WORKSPACE" >nul 2>&1

:: Create local config
echo.
echo Creating local config file...
(
echo {
echo   "github": {
echo     "token": "%GITHUB_TOKEN%",
echo     "owner": "manwonyori",
echo     "repo": "AI-WORKSPACE"
echo   }
echo }
) > github-config.json

echo.
echo ======================================
echo Setup Complete!
echo ======================================
echo.
echo Next steps:
echo 1. Restart your terminal/IDE
echo 2. Test with: git push --dry-run
echo 3. If still failing, try: gh auth login
echo.
pause
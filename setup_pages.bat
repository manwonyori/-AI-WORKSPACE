@echo off
echo ================================================
echo    GitHub Pages Setup for AI-WORKSPACE
echo ================================================
echo.

cd /d "C:\Users\8899y\AI-WORKSPACE"

echo [1/4] Checking if docs folder exists...
if not exist "docs" (
    echo Creating docs folder...
    mkdir docs
) else (
    echo docs folder already exists
)

echo.
echo [2/4] Checking if ai-config exists...
if not exist "docs\ai-config" (
    echo ai-config folder already exists in docs
) else (
    echo ai-config folder found
)

echo.
echo [3/4] Adding changes to git...
git add .
if %errorlevel% neq 0 (
    echo Error: Git add failed. Make sure you're in a git repository.
    pause
    exit /b 1
)

echo.
echo [4/4] Committing and pushing to GitHub...
git commit -m "Update Chrome extension with GitHub Pages integration and Gemini support"
if %errorlevel% neq 0 (
    echo Warning: Nothing to commit or git commit failed
)

git push origin clean-integration
if %errorlevel% neq 0 (
    echo Error: Git push failed. Check your GitHub credentials and network.
    pause
    exit /b 1
)

echo.
echo ================================================
echo    Setup Complete!
echo ================================================
echo.
echo Next steps:
echo 1. Go to: https://github.com/manwonyori/-AI-WORKSPACE/settings/pages
echo 2. Set Source to: Deploy from a branch
echo 3. Set Branch to: clean-integration
echo 4. Set Folder to: /docs
echo 5. Click Save
echo.
echo The following URLs will be available after GitHub Pages is enabled:
echo   - Config: https://manwonyori.github.io/-AI-WORKSPACE/ai-config/agents.json
echo   - Dashboard: https://manwonyori.github.io/-AI-WORKSPACE/
echo.
echo Chrome Extension is ready at: chrome-extension folder
echo Load it in Chrome Extensions (Developer mode ^> Load unpacked)
echo.
pause
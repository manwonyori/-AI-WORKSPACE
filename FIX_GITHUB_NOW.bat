@echo off
echo ======================================
echo IMMEDIATE GITHUB FIX
echo ======================================
echo.

echo Step 1: Remove wrong remote
cd AI-WORKSPACE
git remote remove origin

echo.
echo Step 2: Add correct remote without token
git remote add origin https://github.com/manwonyori/AI-WORKSPACE.git

echo.
echo Step 3: Current status
git remote -v

echo.
echo ======================================
echo NOW YOU NEED TO:
echo ======================================
echo.
echo Option 1 - Make repository PUBLIC:
echo   Go to: https://github.com/manwonyori/AI-WORKSPACE/settings
echo   Scroll to "Danger Zone" 
echo   Click "Change visibility" → Make PUBLIC
echo.
echo Option 2 - Use GitHub CLI:
echo   Run: gh auth login
echo   Choose: GitHub.com → HTTPS → Login with web browser
echo.
echo Option 3 - Create new token:
echo   1. Go to: https://github.com/settings/tokens/new
echo   2. Name: AI-WORKSPACE-Token
echo   3. Expiration: 90 days
echo   4. Select scopes: [x] repo (all)
echo   5. Generate token and copy it
echo   6. Run: git remote set-url origin https://manwonyori:YOUR_TOKEN@github.com/manwonyori/AI-WORKSPACE.git
echo.
pause
@echo off
chcp 65001 >nul
title AI-WORKSPACE - Integrated Work Environment
color 0A
cls

echo ================================================================
echo                   AI-WORKSPACE Integrated Environment
echo ================================================================
echo.
echo 📁 Available Projects:
echo ----------------------------------------------------------------
echo [1] Genesis Ultimate (339 Product Detail Pages)
echo [2] Cafe24 Automation (CUA System)
echo [3] Business Automation
echo.
echo 🤖 AI Tools:
echo ----------------------------------------------------------------  
echo [4] MCP Integrated System
echo [5] AI Collaboration Tools
echo [6] GitHub Integration
echo.
echo Choose (1-6):
set /p choice=
echo.
if "%choice%"=="1" (
    cd projects\genesis-ultimate
    start .
    echo Genesis Ultimate Project Opened
)
if "%choice%"=="2" (
    cd projects\cafe24-automation  
    start .
    echo Cafe24 Automation Project Opened
)
if "%choice%"=="4" (
    cd mcp-system\scripts
    echo MCP Integrated System Starting
)
if "%choice%"=="5" (
    cd ai-collaboration\shared
    echo AI Collaboration Tools Starting
)
if "%choice%"=="6" (
    cd github-integration\automation
    echo GitHub Integration Starting
)
pause
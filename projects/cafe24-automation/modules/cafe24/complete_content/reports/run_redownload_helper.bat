@echo off
chcp 65001 > nul
powershell -ExecutionPolicy Bypass -File "%~dp0redownload_helper.ps1"
pause

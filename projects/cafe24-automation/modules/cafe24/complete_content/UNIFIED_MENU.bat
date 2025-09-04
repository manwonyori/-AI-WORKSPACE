@echo off
chcp 65001 > nul
title CUA-MASTER Unified Control System

:menu
cls
echo.
echo ================================================
echo     CUA-MASTER UNIFIED CONTROL SYSTEM
echo           Main Menu v2.0 (2025-09-01)
echo ================================================
echo.
echo  [1] Claude Bridge Auto Generation (CSV Based)
echo  [2] Brand Analysis System (237 Products)
echo  [3] Template Structure Unification
echo  [4] Product Verification System
echo  [5] Batch HTML Generation (By Brand)
echo  [6] FTP Upload System
echo  [7] Quality Control Dashboard
echo  [8] Single Product Test (Custom)
echo  [9] System Status & Monitoring
echo  [C] CSV Data Analysis
echo  [T] Template Preview (Browser)
echo  [0] Exit
echo.
echo ------------------------------------------------
echo  Current Data: 237 products (CSV verified)
echo  Brands: 취영루(14), 인생(95), 씨씨더블유(37), 반찬단지(48), 태공식품(26)
echo ------------------------------------------------
set /p choice="Select (0-9, C, T): "

if "%choice%"=="1" goto claude_bridge
if "%choice%"=="2" goto brand_analysis
if "%choice%"=="3" goto template_unify
if "%choice%"=="4" goto verification
if "%choice%"=="5" goto batch_generate
if "%choice%"=="6" goto ftp_upload
if "%choice%"=="7" goto quality_control
if "%choice%"=="8" goto single_test
if "%choice%"=="9" goto status_monitor
if /i "%choice%"=="C" goto csv_analysis
if /i "%choice%"=="T" goto template_preview
if "%choice%"=="0" goto exit

echo.
echo Invalid selection!
pause
goto menu

:claude_bridge
cls
echo.
echo ================================================
echo       CLAUDE BRIDGE AUTO GENERATION
echo ================================================
echo.
echo  [1] 취영루 만두 14개 (우선 처리 추천)
echo  [2] 인생 해산물 95개 (대량 처리)
echo  [3] 씨씨더블유 육류 37개 (프리미엄)
echo  [4] 전체 237개 (Full Auto)
echo  [5] Custom Brand Selection
echo  [0] Back to Main Menu
echo.
echo ------------------------------------------------
set /p bridge_choice="Select (0-5): "

if "%bridge_choice%"=="1" goto bridge_chuyoungru
if "%bridge_choice%"=="2" goto bridge_insaeng
if "%bridge_choice%"=="3" goto bridge_ccw
if "%bridge_choice%"=="4" goto bridge_all
if "%bridge_choice%"=="5" goto bridge_custom
if "%bridge_choice%"=="0" goto menu

echo Invalid selection!
pause
goto claude_bridge

:bridge_chuyoungru
echo.
echo Starting Claude Bridge for 취영루 14 products...
echo Using verified template structure from 132_research_applied.html
echo.
python scripts/claude_bridge_chuyoungru.py
pause
goto claude_bridge

:bridge_insaeng
echo.
echo Starting Claude Bridge for 인생 95 products...
echo Processing seafood/dried goods category...
echo.
python scripts/claude_bridge_insaeng.py
pause
goto claude_bridge

:bridge_ccw
echo.
echo Starting Claude Bridge for 씨씨더블유 37 products...
echo Processing premium meat category...
echo.
python scripts/claude_bridge_ccw.py
pause
goto claude_bridge

:bridge_all
echo.
echo Starting Claude Bridge for ALL 237 products...
echo This may take 20-30 minutes. Continue? (Y/N)
set /p confirm=
if /i "%confirm%"=="Y" python scripts/claude_bridge_full_auto.py
pause
goto claude_bridge

:bridge_custom
echo.
echo Enter brand name (e.g., 취영루, 인생, 씨씨더블유):
set /p custom_brand=
python scripts/claude_bridge_custom.py "%custom_brand%"
pause
goto claude_bridge

:brand_analysis
cls
echo.
echo Starting brand analysis system...
echo Analyzing 237 products from CSV data...
echo.
python scripts/csv_product_analyzer.py
python scripts/brand_analysis_system.py
pause
goto menu

:template_unify
echo.
echo Starting template structure unification...
echo Applying unified design to all templates...
echo.
python scripts/unify_seller_structure.py
pause
goto menu

:verification
echo.
echo Starting product verification system...
echo Checking data accuracy and completeness...
echo.
python scripts/product_verification_system.py
pause
goto menu

:batch_generate
cls
echo.
echo ================================================
echo         BATCH HTML GENERATION
echo ================================================
echo.
echo  [1] Generate by Brand (Recommended)
echo  [2] Generate by Product Range (e.g., 100-150)
echo  [3] Generate Failed Products Only
echo  [4] Regenerate All Templates
echo  [0] Back to Main Menu
echo.
set /p batch_choice="Select (0-4): "

if "%batch_choice%"=="1" goto batch_by_brand
if "%batch_choice%"=="2" goto batch_by_range
if "%batch_choice%"=="3" goto batch_failed
if "%batch_choice%"=="4" goto batch_all
if "%batch_choice%"=="0" goto menu

echo Invalid selection!
pause
goto batch_generate

:batch_by_brand
echo Enter brand name:
set /p brand_name=
python scripts/batch_html_generator.py --brand "%brand_name%"
pause
goto batch_generate

:batch_by_range
echo Enter range (e.g., 100-150):
set /p range=
python scripts/batch_html_generator.py --range "%range%"
pause
goto batch_generate

:batch_failed
python scripts/batch_html_generator.py --failed-only
pause
goto batch_generate

:batch_all
echo This will regenerate ALL templates. Continue? (Y/N)
set /p confirm=
if /i "%confirm%"=="Y" python scripts/batch_html_generator.py --all
pause
goto batch_generate

:ftp_upload
echo.
echo Starting FTP upload system...
echo.
python ftp_image_upload_system.py
pause
goto menu

:quality_control
echo.
echo Opening quality control dashboard...
echo.
python scripts/quality_control_dashboard.py
start "" "quality_control_dashboard.html"
pause
goto menu

:single_test
echo.
echo Enter product number for single test:
set /p product_num=
python scripts/claude_bridge_single_test.py "%product_num%"
pause
goto menu

:status_monitor
echo.
echo ================================================
echo           SYSTEM STATUS MONITORING
echo ================================================
echo.
python test_system.py
echo.
echo Files Status:
dir "output\content_only\*_final_clean.html" /B 2>nul | find /C ".html"
echo Templates generated.
echo.
dir "html\analysis\*.json" /B 2>nul | find /C ".json"
echo Analysis files created.
echo.
pause
goto menu

:csv_analysis
echo.
echo Starting CSV data analysis...
echo Analyzing manwonyori_20250901_301_e68d.csv
echo.
python scripts/csv_product_analyzer.py
start "" "html\analysis\csv_product_analysis.json"
pause
goto menu

:template_preview
cls
echo.
echo ================================================
echo           TEMPLATE PREVIEW
echo ================================================
echo.
echo  [1] 132 - 취영루 고기왕만두 (Research Applied)
echo  [2] 133 - 취영루 김치만두 (Final Clean)
echo  [3] 134 - 취영루 물만두 (Final Clean)
echo  [4] 135 - 취영루 튀김만두 (Final Clean)
echo  [5] 140 - 새우만두 (Final Clean)
echo  [6] All Templates (Browser Grid)
echo  [0] Back to Main Menu
echo.
set /p preview_choice="Select (0-6): "

if "%preview_choice%"=="1" start "" "output\content_only\132_research_applied.html"
if "%preview_choice%"=="2" start "" "output\content_only\133_final_clean.html"
if "%preview_choice%"=="3" start "" "output\content_only\134_final_clean.html"
if "%preview_choice%"=="4" start "" "output\content_only\135_final_clean.html"
if "%preview_choice%"=="5" start "" "output\content_only\140_final_clean.html"
if "%preview_choice%"=="6" goto preview_all
if "%preview_choice%"=="0" goto menu

pause
goto template_preview

:preview_all
start "" "output\content_only\132_research_applied.html"
start "" "output\content_only\133_final_clean.html"
start "" "output\content_only\134_final_clean.html"
start "" "output\content_only\135_final_clean.html"
start "" "output\content_only\140_final_clean.html"
pause
goto template_preview

:exit
echo.
echo ================================================
echo     CUA-MASTER System Shutdown
echo ================================================
echo.
echo System Status:
echo - CSV Data: 237 products analyzed
echo - Templates: Ready for generation
echo - Claude Bridge: Configured
echo.
echo Thank you for using CUA-MASTER!
echo.
pause
exit
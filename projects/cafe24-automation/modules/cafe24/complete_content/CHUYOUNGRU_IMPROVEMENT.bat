@echo off
chcp 65001 > nul
title 취영루 품질 개선 시스템 - Claude Bridge Integration

:menu
cls
echo.
echo ================================================
echo      취영루 품질 개선 시스템
echo        Claude Bridge Integration
echo ================================================
echo.
echo  현재 상태:
echo  - 기존 HTML: 14개 (html\취영루\*.html)
echo  - 개선 템플릿: 132_research_applied.html (완성)
echo  - 저장 위치: output\chuyoungru_improved\*.html
echo.
echo ------------------------------------------------
echo.
echo  [1] 취영루 14개 품질 개선 실행
echo  [2] 개선된 템플릿 미리보기 (브라우저)
echo  [3] 개선 전후 비교 보고서
echo  [4] 개별 제품 선택 개선
echo  [5] 백업 및 복원 관리
echo  [6] 품질 검증 시스템
echo  [T] 템플릿 테스트 (132번 기준)
echo  [S] 시스템 상태 확인
echo  [0] 메인 메뉴로 돌아가기
echo.
echo ------------------------------------------------
set /p choice="Select (0-6, T, S): "

if "%choice%"=="1" goto improve_all
if "%choice%"=="2" goto preview_improved
if "%choice%"=="3" goto comparison_report
if "%choice%"=="4" goto improve_single
if "%choice%"=="5" goto backup_management
if "%choice%"=="6" goto quality_verification
if /i "%choice%"=="T" goto template_test
if /i "%choice%"=="S" goto system_status
if "%choice%"=="0" goto main_menu

echo.
echo Invalid selection!
pause
goto menu

:improve_all
cls
echo.
echo ================================================
echo        취영루 14개 제품 품질 개선
echo ================================================
echo.
echo  처리 과정:
echo  1. 기존 HTML 백업 (html\취영루\backup\)
echo  2. 132번 템플릿 기반 품질 개선
echo  3. 개선된 HTML 저장 (output\chuyoungru_improved\)
echo  4. 품질 검증 및 보고서 생성
echo.
echo  예상 소요시간: 5-10분
echo.
echo  Continue? (Y/N)
set /p confirm=
if /i "%confirm%" NEQ "Y" goto menu

echo.
echo [1/4] 백업 생성 중...
python scripts/chuyoungru_backup_system.py

echo.
echo [2/4] Claude Bridge 품질 개선 실행...
python scripts/chuyoungru_quality_improvement.py --all

echo.
echo [3/4] 품질 검증 실행...
python scripts/chuyoungru_quality_verification.py

echo.
echo [4/4] 보고서 생성...
python scripts/generate_improvement_report.py

echo.
echo ================================================
echo  ✓ 취영루 14개 제품 품질 개선 완료!
echo ================================================
echo.
echo  결과 확인:
echo  - 개선된 HTML: output\chuyoungru_improved\
echo  - 품질 보고서: reports\chuyoungru_improvement_report.html
echo  - 백업 파일: html\취영루\backup\
echo.
pause
goto menu

:preview_improved
cls
echo.
echo ================================================
echo         개선된 템플릿 미리보기
echo ================================================
echo.
echo  [1] 132번 고기왕만두 (기준 템플릿)
echo  [2] 133번 김치왕만두
echo  [3] 134번 물만두
echo  [4] 135번 튀김만두
echo  [5] 140번 새우만두
echo  [6] 전체 템플릿 (5개 창)
echo  [7] 랜덤 3개 샘플
echo  [0] 돌아가기
echo.
set /p preview_choice="Select (0-7): "

if "%preview_choice%"=="1" start "" "output\chuyoungru_improved\132_improved.html"
if "%preview_choice%"=="2" start "" "output\chuyoungru_improved\133_improved.html"
if "%preview_choice%"=="3" start "" "output\chuyoungru_improved\134_improved.html"
if "%preview_choice%"=="4" start "" "output\chuyoungru_improved\135_improved.html"
if "%preview_choice%"=="5" start "" "output\chuyoungru_improved\140_improved.html"
if "%preview_choice%"=="6" goto preview_all
if "%preview_choice%"=="7" goto preview_random
if "%preview_choice%"=="0" goto menu

pause
goto preview_improved

:preview_all
start "" "output\chuyoungru_improved\132_improved.html"
start "" "output\chuyoungru_improved\133_improved.html"
start "" "output\chuyoungru_improved\134_improved.html"
start "" "output\chuyoungru_improved\135_improved.html"
start "" "output\chuyoungru_improved\140_improved.html"
echo.
echo 5개 템플릿을 브라우저에서 열었습니다.
pause
goto preview_improved

:preview_random
python scripts/preview_random_templates.py --count 3
pause
goto preview_improved

:comparison_report
echo.
echo 개선 전후 비교 보고서 생성 중...
python scripts/generate_comparison_report.py
start "" "reports\chuyoungru_before_after_comparison.html"
echo.
echo 비교 보고서를 브라우저에서 열었습니다.
pause
goto menu

:improve_single
cls
echo.
echo ================================================
echo         개별 제품 선택 개선
echo ================================================
echo.
echo  취영루 제품 목록:
echo  131 - 교자만두 360g
echo  132 - 고기왕만두 420g (★ 기준 템플릿)
echo  133 - 김치왕만두 490g
echo  134 - 물만두 1.4kg
echo  135 - 튀김만두 2800g
echo  136-141 - 기타 만두류
echo.
echo  개선할 제품번호를 입력하세요 (131-141):
set /p product_num=

if "%product_num%"=="" goto improve_single
if %product_num% LSS 131 goto improve_single
if %product_num% GTR 141 goto improve_single

echo.
echo [처리] %product_num%번 제품 개선 중...
python scripts/chuyoungru_quality_improvement.py --single %product_num%

echo.
echo [완료] %product_num%번 제품 개선 완료!
echo 결과: output\chuyoungru_improved\%product_num%_improved.html
echo.
echo 미리보기하시겠습니까? (Y/N)
set /p preview_confirm=
if /i "%preview_confirm%"=="Y" start "" "output\chuyoungru_improved\%product_num%_improved.html"

pause
goto menu

:backup_management
cls
echo.
echo ================================================
echo         백업 및 복원 관리
echo ================================================
echo.
echo  [1] 전체 백업 생성
echo  [2] 백업 상태 확인
echo  [3] 백업에서 복원
echo  [4] 백업 파일 정리
echo  [0] 돌아가기
echo.
set /p backup_choice="Select (0-4): "

if "%backup_choice%"=="1" python scripts/create_chuyoungru_backup.py
if "%backup_choice%"=="2" python scripts/check_backup_status.py
if "%backup_choice%"=="3" goto restore_menu
if "%backup_choice%"=="4" python scripts/cleanup_old_backups.py
if "%backup_choice%"=="0" goto menu

pause
goto backup_management

:restore_menu
echo.
echo 복원할 백업을 선택하세요:
python scripts/list_available_backups.py
echo.
echo 백업 ID를 입력하세요:
set /p backup_id=
python scripts/restore_from_backup.py --id %backup_id%
pause
goto backup_management

:quality_verification
echo.
echo ================================================
echo         품질 검증 시스템 실행
echo ================================================
echo.
echo [검증] 개선된 HTML 파일들 품질 검증 중...
python scripts/chuyoungru_quality_verification.py --detailed

echo.
echo [보고서] 품질 검증 보고서 생성...
start "" "reports\chuyoungru_quality_report.html"

echo.
echo 품질 검증 완료!
pause
goto menu

:template_test
echo.
echo 132번 기준 템플릿 테스트 실행...
python scripts/test_base_template.py --product 132
start "" "output\chuyoungru_improved\132_research_applied.html"
echo.
echo 기준 템플릿을 브라우저에서 열었습니다.
pause
goto menu

:system_status
cls
echo.
echo ================================================
echo           시스템 상태 확인
echo ================================================
echo.

echo [파일 상태]
echo 기존 HTML 파일:
dir "html\취영루\*.html" /B 2>nul | find /C ".html"
echo 개 파일 존재

echo.
echo 개선된 HTML 파일:
dir "output\chuyoungru_improved\*.html" /B 2>nul | find /C ".html" 
echo 개 파일 존재

echo.
echo 백업 파일:
dir "html\취영루\backup\*.html" /B 2>nul | find /C ".html"
echo 개 백업 파일 존재

echo.
echo [디렉토리 구조]
echo ├── html\취영루\ (원본 파일)
echo ├── output\chuyoungru_improved\ (개선된 파일)
echo ├── html\취영루\backup\ (백업 파일)
echo ├── reports\ (보고서)
echo └── scripts\ (처리 스크립트)

echo.
echo [시스템 준비 상태]
python scripts/check_system_readiness.py

echo.
pause
goto menu

:main_menu
echo.
echo 메인 메뉴로 돌아갑니다...
call UNIFIED_MENU.bat
exit

:exit
echo.
echo 취영루 품질 개선 시스템을 종료합니다.
echo.
exit
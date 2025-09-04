@echo off
chcp 65001 > nul
color 0C
title 가격 최적화 분석 시스템 v2.0 (간단버전)

:메인메뉴
cls
echo.
echo    ============================================================
echo          가격 최적화 분석 시스템 v2.0 (간단버전)
echo                 (올바른 마진율 계산 적용)
echo    ============================================================
echo.
echo    1. 전체 상품 가격 분석
echo    2. 마진율 개선 제안
echo    3. 경쟁업체 가격 비교
echo    4. 최적 가격 전략 수립
echo.
echo    5. 공급사별 마진율 분석
echo    6. 마진율 일괄/개별 수정
echo.
echo    7. 키워드 시스템으로 돌아가기
echo    8. 종료
echo.
echo    ============================================================
echo    * 마진율 = (판매가-공급가)/판매가*100
echo    ============================================================
echo.

:입력받기
set /p choice=번호를 입력하세요: 

rem 1-8 사이인지 확인
if "%choice%"=="1" goto 기능1
if "%choice%"=="2" goto 기능2  
if "%choice%"=="3" goto 기능3
if "%choice%"=="4" goto 기능4
if "%choice%"=="5" goto 기능5
if "%choice%"=="6" goto 기능6
if "%choice%"=="7" goto 키워드시스템
if "%choice%"=="8" goto 프로그램종료

echo.
echo 잘못된 입력입니다. 1-8 사이의 번호를 입력하세요.
echo.
pause
goto 메인메뉴

:기능1
echo 전체 상품 가격 분석 실행 중...
cd "modules\price-optimizer"
python process_all.py
cd ..\..
pause
goto 메인메뉴

:기능2
echo 마진율 개선 제안 실행 중...
cd "modules\price-optimizer"  
python margin_analysis.py
cd ..\..
pause
goto 메인메뉴

:기능3
echo 경쟁업체 가격 비교 실행 중...
cd "modules\price-optimizer"
python competitor_analysis.py
cd ..\..
pause
goto 메인메뉴

:기능4
echo 최적 가격 전략 수립 실행 중...
cd "modules\price-optimizer"
python strategy_analysis.py
cd ..\..
pause
goto 메인메뉴

:기능5
echo 공급사별 마진율 분석 실행 중...
cd "modules\price-optimizer"
python supplier_margin_analysis.py
cd ..\..
pause
goto 메인메뉴

:기능6
echo 마진율 수정 실행 중...
cd "modules\price-optimizer"
python margin_editor.py
cd ..\..
pause
goto 메인메뉴

:키워드시스템
echo 키워드 시스템으로 돌아갑니다...
pause
exit

:프로그램종료
cls
echo.
echo 가격 최적화 시스템을 종료합니다.
echo 이용해 주셔서 감사합니다!
echo.
pause
exit
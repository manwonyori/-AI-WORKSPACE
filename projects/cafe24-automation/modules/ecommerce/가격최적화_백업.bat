@echo off
chcp 65001 > nul
color 0C
title 가격 최적화 분석 시스템

:메인메뉴
cls
echo.
echo    ============================================================
echo              가격 최적화 분석 시스템
echo    ============================================================
echo.
echo    [1] 전체 상품 가격 분석
echo    [2] 마진율 개선 제안
echo    [3] 경쟁업체 가격 비교
echo    [4] 최적 가격 전략 수립
echo.
echo    [5] 공급사별 마진율 분석
echo    [6] 마진율 일괄/개별 수정
echo.
echo    [7] 키워드 시스템으로 돌아가기
echo    [8] 종료
echo.
echo    ============================================================
echo.
set /p choice=선택 (1-8): 

rem 입력값 정제 (대괄호, 공백 제거)
set choice=%choice:[=%
set choice=%choice:]=%
set choice=%choice: =%

rem 디버그용 (필요시 주석 해제)
rem echo 입력값: "%choice%"

if "%choice%"=="1" goto 전체분석
if "%choice%"=="2" goto 마진개선
if "%choice%"=="3" goto 경쟁분석
if "%choice%"=="4" goto 전략수립
if "%choice%"=="5" goto 공급사분석
if "%choice%"=="6" goto 마진수정
if "%choice%"=="7" goto 키워드시스템
if "%choice%"=="8" goto 종료

echo 잘못된 선택입니다. 1-8 중에서 선택하세요.
pause
goto 메인메뉴

:전체분석
cls
echo ============================================================
echo                    전체 상품 가격 분석
echo ============================================================
echo.
echo 최신 처리 결과를 기반으로 가격을 분석합니다...
echo.
cd "modules\price-optimizer"
python process_all.py
cd ..\..
echo.
echo 분석 완료!
pause
goto 메인메뉴

:마진개선
cls
echo ============================================================
echo                    마진율 개선 제안
echo ============================================================
echo.
echo 마진율이 낮은 상품들의 개선 방안을 제시합니다.
echo.
cd "modules\price-optimizer"
python margin_analysis.py
cd ..\..
echo.
pause
goto 메인메뉴

:경쟁분석
cls
echo ============================================================
echo                  경쟁업체 가격 비교 분석
echo ============================================================
echo.
echo 주요 온라인 쇼핑몰 가격을 AI로 분석합니다.
echo - 쿠팡, 11번가, 지마켓, 옥션, 인터파크
echo.
cd "modules\price-optimizer"
python competitor_analysis.py
cd ..\..
echo.
pause
goto 메인메뉴

:전략수립
cls
echo ============================================================
echo                  최적 가격 전략 수립
echo ============================================================
echo.
echo 상품별 맞춤 가격 전략을 AI가 제안합니다.
echo.
cd "modules\price-optimizer"
python strategy_analysis.py
cd ..\..
echo.
pause
goto 메인메뉴

:공급사분석
cls
echo ============================================================
echo               공급사별 마진율 분석
echo ============================================================
echo.
echo 공급사별 마진율 분석 및 5단계 분류를 실행합니다...
echo - 공급사별 평균 마진율 계산
echo - 마진율 5단계 분류 (위험~우수)
echo - 상품별 세부 분석
echo.
cd "modules\price-optimizer"
python supplier_margin_analysis.py
cd ..\..
echo.
pause
goto 메인메뉴

:마진수정
cls
echo ============================================================
echo              마진율 일괄/개별 수정
echo ============================================================
echo.
echo 마진율 수정 기능을 실행합니다...
echo - 마진율 5단계별 일괄 수정
echo - 공급사별 일괄 수정
echo - 개별 상품 수정
echo.
cd "modules\price-optimizer"
python margin_editor.py
cd ..\..
echo.
pause
goto 메인메뉴

:키워드시스템
cls
echo ============================================================
echo                키워드 처리 시스템으로 이동
echo ============================================================
echo.
echo 메인 처리시스템으로 돌아갑니다...
pause
exit

:종료
cls
echo ============================================================
echo                  가격 최적화 시스템 종료
echo ============================================================
echo.
echo 가격 최적화 시스템을 종료합니다...
echo 감사합니다!
echo.
pause
exit
@echo off
chcp 65001 > nul
color 0C
title 가격 최적화 분석 시스템 v2.0

:메인메뉴
cls
echo.
echo    ============================================================
echo            가격 최적화 분석 시스템 v2.0
echo                  (올바른 마진율 계산 적용)
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
echo    * 마진율 공식: (판매가-공급가)/판매가*100
echo    * 공급가 = 실제 원가, 상품가 = 중간가격  
echo    ============================================================
echo.

:입력받기
set /p choice=메뉴 번호를 선택하세요 (1-8): 

rem 입력값 정제 (대괄호, 공백, 특수문자 제거)
set choice=%choice:[=%
set choice=%choice:]=%
set choice=%choice: =%
set choice=%choice:(=%
set choice=%choice:)=%

rem 유효성 검사
if "%choice%"=="1" goto 전체분석
if "%choice%"=="2" goto 마진개선
if "%choice%"=="3" goto 경쟁분석  
if "%choice%"=="4" goto 전략수립
if "%choice%"=="5" goto 공급사분석
if "%choice%"=="6" goto 마진수정
if "%choice%"=="7" goto 키워드시스템
if "%choice%"=="8" goto 시스템종료

echo.
echo ❌ 잘못된 입력입니다. 1-8 사이의 번호를 입력하세요.
echo.
pause
goto 메인메뉴

:전체분석
cls
echo ============================================================
echo                  전체 상품 가격 분석
echo ============================================================
echo.
echo 📊 최신 데이터를 기반으로 가격을 분석합니다...
echo    - 마진율 계산 (공급가 기준)
echo    - 가격대별 분류 
echo    - 경쟁가격 추정
echo    - 최적가격 제안
echo.
cd "modules\price-optimizer"
python process_all.py
cd ..\..
echo.
echo ✅ 분석 완료!
pause
goto 메인메뉴

:마진개선
cls  
echo ============================================================
echo                   마진율 개선 제안
echo ============================================================
echo.
echo 📈 마진율이 낮은 상품들의 개선 방안을 제시합니다...
echo    - 15% 미만 마진 상품 식별
echo    - 원가 절감 방안
echo    - 가격 인상 전략
echo    - 부가가치 서비스 제안
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
echo                 경쟁업체 가격 비교 분석  
echo ============================================================
echo.
echo 🏪 주요 온라인 쇼핑몰 가격을 AI로 분석합니다...
echo    - 쿠팡, 11번가, 지마켓, 옥션, 인터파크
echo    - AI 기반 가격 추정
echo    - 경쟁력 평가
echo    - 가격 포지셔닝 분석
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
echo                 최적 가격 전략 수립
echo ============================================================  
echo.
echo 🎯 상품별 맞춤 가격 전략을 AI가 제안합니다...
echo    - 공격적 가격: 시장점유율 확대
echo    - 경쟁적 가격: 균형잡힌 접근
echo    - 안전적 가격: 안정성 우선
echo    - 프리미엄 가격: 브랜드 가치 강화
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
echo 🏢 공급사별 마진율 분석 및 5단계 분류를 실행합니다...
echo    - 공급사별 평균 마진율 계산  
echo    - 5단계 분류: 위험(5%미만) ~ 우수(35%이상)
echo    - 마진 분포 현황
echo    - 상품별 세부 분석
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
echo ✏️ 마진율 수정 기능을 실행합니다...
echo    - 마진율 5단계별 일괄 수정
echo    - 공급사별 일괄 수정  
echo    - 개별 상품 수정
echo    - 실시간 가격 재계산
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
echo               키워드 처리 시스템으로 이동
echo ============================================================
echo.
echo 🔄 메인 처리시스템으로 돌아갑니다...
echo    가격 최적화 작업이 완료되었습니다.
echo.
pause
exit

:시스템종료
cls
echo.  
echo    ============================================================
echo              가격 최적화 시스템 v2.0 종료
echo    ============================================================
echo.
echo    ✅ 가격 최적화 시스템을 종료합니다.
echo    
echo    📊 주요 기능:
echo       - 올바른 마진율 계산 (공급가 기준)
echo       - 공급사별 마진 분석
echo       - AI 기반 경쟁가격 분석  
echo       - 5단계 마진율 분류
echo       - 일괄/개별 가격 수정
echo.
echo    🙏 이용해 주셔서 감사합니다!
echo.
pause
exit
@echo off
chcp 65001 > nul
title Claude 대화형 처리 시스템
color 0B

:메인
cls
echo ============================================================
echo           Claude 대화형 상품 처리 시스템
echo ============================================================
echo.
echo 이 시스템은 Claude와 대화하면서 처리합니다.
echo.
echo [1] 상품 1개씩 처리 (Claude 창 열림)
echo [2] 일괄 처리 준비 (프롬프트 생성)
echo [3] 결과 붙여넣기
echo [4] 종료
echo.
set /p choice=선택: 

if "%choice%"=="1" goto 단일처리
if "%choice%"=="2" goto 일괄준비
if "%choice%"=="3" goto 결과처리
if "%choice%"=="4" exit
goto 메인

:단일처리
cls
echo 처리할 CSV 파일 선택...
echo.
python -c "import pandas as pd; df=pd.read_csv('data/input/manwonyori_20250828_283_56dd.csv', encoding='utf-8-sig'); print('첫 번째 상품:', df.iloc[0]['상품명'])" 2>nul
echo.
echo ========================================
echo Claude에 다음 질문을 복사하세요:
echo ========================================
echo.
echo 다음 상품의 검색 키워드 40개를 생성해주세요:
python -c "import pandas as pd; df=pd.read_csv('data/input/manwonyori_20250828_283_56dd.csv', encoding='utf-8-sig'); print(df.iloc[0]['상품명'])" 2>nul
echo.
echo 조건:
echo - 만원요리, 최씨남매, 집밥각, 술한잔 중 적절한 것 포함
echo - 소비자가 실제 검색할 키워드
echo - 쉼표로 구분
echo.
echo ========================================
echo.
echo Claude.ai 열기 (Y/N)?
set /p open=
if /i "%open%"=="Y" start https://claude.ai
echo.
pause
goto 메인

:일괄준비
cls
echo CSV 파일 읽는 중...
echo.
dir data\input\*.csv /b 2>nul
if errorlevel 1 (
    echo 오류: data\input 폴더에 CSV 파일이 없습니다!
    pause
    goto 메인
)
echo.
echo 첫 5개 상품 미리보기:
echo ----------------------------------------
python -c "import pandas as pd; df=pd.read_csv('data/input/manwonyori_20250828_283_56dd.csv', encoding='utf-8-sig', nrows=5); print(df[['상품명']].to_string())" 2>nul
echo ----------------------------------------
echo.
echo 다음 프롬프트를 Claude에 복사하세요:
echo.
echo ========================================
echo 다음 상품들의 검색 키워드를 각각 40개씩 생성해주세요.
echo 조건: 만원요리, 최씨남매, 집밥각, 술한잔 중 적절한 것 포함
echo 형식: 상품명: 키워드1,키워드2,...(40개)
echo ========================================
echo.
echo Claude.ai 열기 (Y/N)?
set /p open=
if /i "%open%"=="Y" start https://claude.ai
echo.
pause
goto 메인

:결과처리
cls
echo Claude 응답을 메모장에 붙여넣으세요.
notepad temp_claude_response.txt
echo.
echo 저장 후 Enter를 누르세요...
pause
echo.
echo 결과 처리 중...
python scripts\process_claude_response.py
echo.
echo 완료! 결과는 data/output/에 저장되었습니다.
pause
goto 메인
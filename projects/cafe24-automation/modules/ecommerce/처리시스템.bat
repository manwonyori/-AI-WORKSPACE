@echo off
chcp 65001 > nul
color 0A
title 한국 이커머스 통합 처리 시스템 v2.0

:메인메뉴
cls
echo.
echo    ============================================================
echo            한국 이커머스 통합 처리 시스템 v2.0
echo                    (키워드 + 가격 최적화)
echo    ============================================================
echo.
echo    [1] 빠른 처리 (API 불필요, 40개 키워드)
echo    [2] 단일 AI 처리 (OpenAI만 사용)
echo    [3] 멀티 AI 처리 (Claude 지휘 + OpenAI + Gemini)
echo.
echo    [4] 가격 최적화 분석
echo    [5] 환경 설정 (API 키, 패키지)
echo    [6] 종료
echo.
echo    ============================================================
echo.
set /p choice=선택 [1-6]: 

if "%choice%"=="1" goto 빠른처리
if "%choice%"=="2" goto 단일AI
if "%choice%"=="3" goto 멀티AI
if "%choice%"=="4" goto 가격최적화
if "%choice%"=="5" goto 설정
if "%choice%"=="6" exit

goto 메인메뉴

:빠른처리
cls
echo ============================================================
echo                    빠른 처리 모드
echo ============================================================
echo.
echo 필요한 폴더를 생성합니다...
if not exist data\output mkdir data\output
echo.
python modules\keyword-processor\src\quick_processor.py
echo.
echo 처리 완료!
pause
goto 메인메뉴

:단일AI
cls
echo ============================================================
echo                 단일 AI 처리 (OpenAI)
echo ============================================================
echo.
echo 필요한 폴더를 생성합니다...
if not exist data\output mkdir data\output
echo.
if not exist shared\config\.env (
    echo 경고: API 키가 없습니다!
    echo 먼저 설정에서 API 키를 등록하세요.
    echo.
    pause
    goto 메인메뉴
)
python modules\keyword-processor\scripts\process_final.py
echo.
pause
goto 메인메뉴

:멀티AI
cls
echo ============================================================
echo     멀티 AI 처리 (Claude 지휘 + OpenAI + Gemini)
echo ============================================================
echo.
echo Claude가 지휘하고 여러 AI가 협업합니다.
echo.
echo 필요한 폴더를 생성합니다...
if not exist data\output mkdir data\output
echo.
if not exist shared\config\.env (
    echo 경고: API 키가 없습니다!
    echo.
    pause
    goto 메인메뉴
)
python modules\keyword-processor\src\ai_orchestrator.py
echo.
pause
goto 메인메뉴

:설정
cls
echo ============================================================
echo                     환경 설정
echo ============================================================
echo.
echo [1] API 키 설정
echo [2] 패키지 설치
echo [3] 돌아가기
echo.
set /p setup=선택: 

if "%setup%"=="1" (
    if not exist shared\config\.env (
        mkdir shared\config 2>nul
        echo # API 키 설정 > shared\config\.env
        echo OPENAI_API_KEY=여기에_키_입력 >> shared\config\.env
        echo ANTHROPIC_API_KEY=여기에_키_입력 >> shared\config\.env
        echo GOOGLE_API_KEY=여기에_키_입력 >> shared\config\.env
    )
    notepad shared\config\.env
)
if "%setup%"=="2" (
    pip install -r requirements.txt
    pause
)
if "%setup%"=="3" goto 메인메뉴
goto 설정

:가격최적화
cls
echo ============================================================
echo                    가격 최적화 분석
echo ============================================================
echo.
echo 처리된 상품 데이터를 기반으로 가격을 분석합니다...
echo - 마진율 분석
echo - 경쟁가격 추정
echo - 최적가격 제안
echo - 가격전략 수립
echo.
echo 가격최적화.bat를 실행합니다...
echo.
start "" "가격최적화.bat"
echo.
echo 가격 최적화 시스템이 별도 창에서 실행됩니다.
pause
goto 메인메뉴
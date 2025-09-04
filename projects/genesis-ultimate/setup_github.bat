@echo off
title Genesis Ultimate - GitHub Setup
cls
echo ================================================
echo    Genesis Ultimate GitHub 설정
echo ================================================
echo.

:: Git 확인
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Git이 설치되지 않았습니다!
    echo https://git-scm.com 에서 다운로드하세요.
    pause
    exit /b 1
)

:: GitHub CLI 확인
gh --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] GitHub CLI 설치 중...
    winget install GitHub.cli
)

cd C:\Users\8899y\genesis_ultimate

:: Git 초기화 확인
if not exist ".git" (
    echo [1/5] Git 저장소 초기화...
    git init
    git config user.name "Genesis Ultimate User"
    git config user.email "genesis@example.com"
) else (
    echo [✓] Git 저장소 이미 초기화됨
)

:: .gitignore 생성
echo [2/5] .gitignore 파일 생성...
(
echo # Python
echo venv/
echo __pycache__/
echo *.pyc
echo *.pyo
echo *.pyd
echo .Python
echo 
echo # Cache
echo cache/
echo *.log
echo 
echo # Output (선택적)
echo # output/
echo 
echo # Config with sensitive data
echo config/api_keys.json
echo *.env
echo 
echo # IDE
echo .vscode/
echo .idea/
echo *.swp
echo *.swo
echo 
echo # OS
echo Thumbs.db
echo .DS_Store
) > .gitignore

:: README.md 생성
echo [3/5] README.md 생성...
(
echo # Genesis Ultimate - Product Detail Page Generator
echo.
echo ## 📦 프로젝트 소개
echo 만원요리 최씨남매 제품 상세페이지 자동 생성 시스템
echo.
echo ## 🚀 주요 기능
echo - 339개 제품 HTML 자동 생성
echo - TypeD 템플릿 시스템
echo - 브랜드별 분류 ^(12개 브랜드^)
echo - CUA 시스템 통합
echo.
echo ## 📁 폴더 구조
echo ```
echo genesis_ultimate/
echo ├── data/          # 제품 데이터
echo ├── output/        # 생성된 HTML
echo ├── templates/     # HTML 템플릿
echo └── config/        # 설정 파일
echo ```
echo.
echo ## 🔧 사용법
echo ```bash
echo # 가상환경 활성화
echo venv\Scripts\activate
echo.
echo # 의존성 설치
echo pip install -r requirements.txt
echo.
echo # TypeD 생성
echo python generate_typeD_from_CUA.py
echo ```
echo.
echo ## 📊 제품 통계
echo - 총 제품: 339개
echo - 브랜드: 12개
echo - 인생: 120개+
echo - 씨씨더블유: 84개
echo - 반찬단지: 50개
echo.
echo ## 🤝 협업
echo - ChatGPT: 코드 리뷰 및 개선 제안
echo - Claude: 실시간 수정 및 구현
echo.
echo ---
echo Generated: %date%
) > README.md

:: 첫 커밋
echo [4/5] 첫 커밋 생성...
git add .
git commit -m "Initial commit: Genesis Ultimate project setup" 2>nul || echo [✓] 이미 커밋됨

:: GitHub 레포지토리 생성
echo [5/5] GitHub 레포지토리 생성...
echo.
echo GitHub 로그인이 필요합니다...
gh auth status >nul 2>&1
if %errorlevel% neq 0 (
    echo GitHub 로그인 중...
    gh auth login
)

echo.
echo 레포지토리 이름 (기본: genesis_ultimate):
set /p repo_name=
if "%repo_name%"=="" set repo_name=genesis_ultimate

echo.
echo 공개(public) 또는 비공개(private)? [public/private]:
set /p visibility=
if "%visibility%"=="" set visibility=public

:: 레포 생성 및 푸시
gh repo create %repo_name% --%visibility% --source=. --remote=origin --push

echo.
echo ================================================
echo    ✅ GitHub 설정 완료!
echo ================================================
echo.
echo 레포지토리 URL:
gh repo view --web --no-browser
echo.
echo ChatGPT에서 사용:
echo - 위 URL을 복사해서 ChatGPT에 전달
echo - "Analyze this repository: [URL]"
echo.
echo Claude에서 사용:
echo - GitHub MCP 서버 사용
echo - 또는 웹 링크 직접 분석
echo.
echo 동기화 명령:
echo - git add . ^&^& git commit -m "Update" ^&^& git push
echo.
pause
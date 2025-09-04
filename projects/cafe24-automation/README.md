# CUA-MASTER

## Computer Use Agent Master System v3.0

### 개요
카페24 쇼핑몰 자동화를 위한 통합 CUA(Computer Use Agent) 시스템

### 🚀 빠른 시작
```bash
# 메인 메뉴 실행
CUA.bat

# 빠른 명령어
CUA.bat learn     # 통합 학습기 실행
CUA.bat deep      # 심층 섹션 학습
CUA.bat scheduler # 백그라운드 스케줄러
CUA.bat claude    # Claude Agent 시작
CUA.bat ai        # AI Council 실행
CUA.bat monitor   # 대시보드 열기
CUA.bat status    # 시스템 상태 확인
CUA.bat help      # 도움말
```

### 📋 주요 모듈

#### 1. Cafe24 학습 시스템 (`modules/cafe24/`)
- **통합 학습기** (`cafe24_unified_learner.py`)
  - 5가지 요구사항 완전 구현
  - DOM 스캔, 요소 매핑, 이벤트 분석
  - AJAX 모니터링, 저장 프로세스 추적
  
- **심층 섹션 학습** (`cafe24_deep_section_learner.py`)
  - 13개 섹션 완전 학습
  - 하위 카테고리 자동 탐색
  - 모든 입력 요소 매핑

- **학습 데이터** (`learning/`)
  - JSON 형식 저장
  - 패턴 인식 및 재사용
  - 실행 히스토리 관리

#### 2. 백그라운드 자동화 (`cua_background_scheduler.py`)
- 주기적 작업 스케줄링
- 시스템 리소스 모니터링
- Claude Bridge 연동
- 자동 작업 실행

#### 3. Claude Code Bridge (`claude_bridge/`)
- Claude Code Agent와 실시간 통신
- 요청/응답 처리
- 백그라운드 모니터링

#### 4. AI Council 시스템 (`ai-council/`)
- 다중 AI 협업 시스템
- 실시간 대화 모니터링
- 디자인 시스템 통합

### 📁 시스템 구조
```
CUA-MASTER/
├── modules/
│   └── cafe24/                    # Cafe24 자동화 모듈
│       ├── cafe24_unified_learner.py      # 통합 학습기
│       ├── cafe24_deep_section_learner.py # 심층 학습기
│       ├── section_structure_viewer.py    # 구조 뷰어
│       ├── mouse_tracker_logger.py        # 마우스 추적
│       └── learning/              # 학습 데이터
│           ├── *.json             # 학습 결과
│           └── *.html             # 페이지 소스
│
├── cua_background_scheduler.py    # 백그라운드 스케줄러
├── scheduler_config.json          # 스케줄러 설정
│
├── dashboard/                     # 대시보드
│   └── dashboard.html            # 메인 대시보드
│
├── claude_bridge/                # Claude 연동
│   ├── requests/                 # 요청
│   └── responses/                # 응답
│
├── ai-council/                   # AI Council
│   ├── ai_council.py            # 메인 실행
│   └── agents/                  # AI 에이전트들
│
├── logs/                         # 로그 파일
├── docs/                         # 문서
├── CUA.bat                       # 메인 실행 파일
└── README.md                     # 이 파일
```

### ⚙️ 주요 기능

#### Cafe24 상품 페이지 학습
1. **표시설정** - 진열/판매 상태
2. **기본정보** - 상품명, 코드, 설명
3. **판매정보** - 가격, 할인, 적립금
4. **옵션/재고** - 옵션 설정, 재고 관리
5. **이미지정보** - 대표/추가 이미지
6. **제작정보** - 소재, 제작자, KC인증
7. **상세이용안내** - 결제/배송/교환 안내
8. **아이콘설정** - 아이콘 표시 설정
9. **배송정보** - 배송방법, 배송비
10. **추가구성상품** - 추가 상품 설정
11. **관련상품** - 연관 상품 설정
12. **SEO설정** - 검색엔진 최적화
13. **메모** - 관리자 메모

### 🔧 환경 요구사항
- Windows 10/11
- Python 3.7+
- Chrome 브라우저
- Selenium WebDriver

### 📦 설치
```bash
# 1. 저장소 이동
cd C:\Users\8899y\CUA-MASTER

# 2. 의존성 설치
pip install selenium schedule psutil

# 3. Chrome WebDriver 설치
# ChromeDriver를 PATH에 추가 또는 시스템에 설치
```

### 🎯 사용 방법

#### 1. 통합 학습 실행
```bash
CUA.bat learn
# 또는
python modules/cafe24/cafe24_unified_learner.py
```

#### 2. 백그라운드 스케줄러 실행
```bash
CUA.bat scheduler
# 또는
python cua_background_scheduler.py
```

#### 3. Claude Agent 모니터링
```bash
CUA.bat claude
# 또는
python start_claude_agent.py
```

#### 4. 시스템 상태 확인
```bash
CUA.bat status
```

### 📊 최근 업데이트
- **2025-09-01**: CUA.bat v3.0 업데이트
- **2025-09-01**: 통합 학습 시스템 구현
- **2025-09-01**: 심층 섹션 학습기 추가
- **2025-09-01**: 백그라운드 스케줄러 구현
- **2025-09-01**: 마우스 추적 로거 추가
- **2025-08-31**: Claude Code Bridge 연동
- **2025-08-31**: AI Council 시스템 통합

### 🐛 문제 해결
- **세션 만료**: 카페24 재로그인 필요
- **탭 찾기 실패**: 페이지 로드 대기 시간 증가
- **마우스 시각화 안 보임**: 카페24 보안 정책으로 제한됨
- **학습 실패**: Chrome 브라우저 재시작 후 재시도

### 📈 성능 메트릭
- 학습 속도: 상품 1개당 2-3분
- 요소 인식률: 95% 이상
- 메모리 사용: 200-300MB
- CPU 사용: 평균 10-20%

### 🔒 보안 참고사항
- 자격 증명은 환경 변수 또는 설정 파일에 저장
- 민감한 정보는 코드에 하드코딩하지 않음
- 로그 파일에 비밀번호 기록 방지

### 📝 라이선스
Private Use Only - 내부 사용 전용

### 📞 문의
내부 시스템 관리자에게 문의

---
*CUA-MASTER v3.0 - Computer Use Agent for Cafe24*
*최종 업데이트: 2025-09-01*
# 통합 시스템 구축 계획

## 현재 상태 분석

### 1. 핵심 프로젝트 (4개)
```
C:\Users\8899y\
├── ai-council/              # AI 협의회 시스템
├── SuperClaude/             # 자율 학습 AI
├── korean-ecommerce-specialist/  # 한국 이커머스
└── mart-project/            # 마트 공급망
```

### 2. 문제점
- **중복 파일**: 1,500+ 중복 파일
- **잘못된 경로**: CUsers8899y* 폴더들
- **보안 위험**: API 키 노출
- **분산된 기능**: 같은 기능이 여러 곳에

### 3. 데이터베이스 현황
- 학습 DB: 15개 이상 분산
- 카테고리 DB: 3개 중복
- 추적 DB: 5개 분산

## 통합 아키텍처

### Phase 1: 즉시 정리 (오늘)
```python
# 1. 위험 파일 제거
- system_backups/ 삭제
- Desktop/key.md 삭제
- CUsers8899y* 폴더들 삭제

# 2. 보안 설정
- .env 파일로 모든 키 이동
- .gitignore 업데이트
```

### Phase 2: 구조 통합 (내일)
```
C:\Users\8899y\
├── .env                     # 모든 API 키
├── .gitignore              # 보안 설정
├── CLAUDE.md               # 통합 지침
│
├── ai-council/             # [유지] AI 협의회
│   ├── agents/            # 각 AI 에이전트
│   ├── core/              # 핵심 시스템
│   └── integration/       # 프로젝트 연결
│
├── SuperClaude/            # [정리] 자율 학습
│   ├── core/              # 핵심만 유지
│   ├── data/              # DB 통합
│   └── modules/           # 필수 모듈만
│
├── korean-ecommerce/       # [유지] 이커머스
│   ├── modules/           # 키워드, 가격
│   └── data/              # 상품 데이터
│
└── mart-project/           # [유지] 공급망
    ├── src/               # 핵심 로직
    └── docs/              # 발주서 등
```

### Phase 3: AI Council 중심 통합

```python
class UnifiedSystem:
    """
    모든 프로젝트 통합 관리
    """
    def __init__(self):
        self.council = AICouncil()
        self.projects = {
            'superclaude': SuperClaude(),
            'ecommerce': KoreanEcommerce(),
            'mart': MartProject()
        }
    
    async def process_task(self, task):
        # 1. AI Council이 작업 분석
        decision = await self.council.analyze(task)
        
        # 2. 적절한 프로젝트로 분배
        if decision.type == 'learning':
            return await self.projects['superclaude'].evolve()
        elif decision.type == 'product':
            return await self.projects['ecommerce'].process()
        elif decision.type == 'supply':
            return await self.projects['mart'].manage()
        
        # 3. 결과 통합
        return await self.council.integrate_results()
```

## 즉시 실행 계획

### 1. 보안 조치 (긴급)
```bash
# 위험 파일 삭제
del /q system_backups\*
del Desktop\key.md

# 잘못된 폴더 제거
rmdir /s /q CUsers8899y*
```

### 2. 데이터베이스 통합
```python
# 분산된 DB를 하나로
- learning_system.db (통합 학습)
- category_master.db (카테고리)
- tracking_unified.db (추적)
```

### 3. 중복 제거
- 백업 폴더 정리
- 중복 스크립트 통합
- 불필요한 bat 파일 제거

## 기대 효과

### Before
- 디스크 사용: 8.5GB
- 파일 수: 5,000+
- 중복률: 40%
- 보안 위험: 높음

### After
- 디스크 사용: 3GB (-65%)
- 파일 수: 1,500 (-70%)
- 중복률: 0%
- 보안: 안전

## 실행 명령

### 1단계: 정리
```bash
python cleanup_system.py
```

### 2단계: 통합
```bash
python integrate_projects.py
```

### 3단계: 검증
```bash
python verify_integration.py
```

## 작업 우선순위

1. **긴급**: API 키 보안 처리
2. **높음**: 중복 폴더 제거
3. **중간**: DB 통합
4. **낮음**: 문서 정리

## 일관된 작업 방식

- **한국어 우선**: 모든 설명과 주석
- **Edit 우선**: 새 파일 생성 최소화
- **이모지 금지**: 깔끔한 코드
- **보안 최우선**: 환경 변수 사용

## 다음 단계

1. 이 계획 승인 요청
2. 백업 생성
3. 단계별 실행
4. 결과 검증

---
작성일: 2025-08-29
작성자: AI Council System
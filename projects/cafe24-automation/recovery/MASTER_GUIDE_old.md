# 마스터 가이드 - 통합 AI 시스템

## 단 하나의 진입점
```
C:\Users\8899y\RUN.bat
```

## 시작하기
1. **RUN.bat 실행**
   - 모든 Agent 자동 활성화
   - API 키 자동 로드
   - 문서 자동 업데이트 모드

2. **Claude와 대화**
   - "오늘 주문 처리해줘"
   - "키워드 최적화 실행"
   - "발주 리스트 만들어줘"
   - "시스템 상태 확인"

## 활성화되는 Agent들

### 1. ai-council
- AI 협의회 의사결정
- 품질 90% 이상까지 반복 개선
- 중요 결정시 자동 소집

### 2. superclaude  
- 자율학습 시스템
- 패턴 인식 및 진화
- 성능 자동 최적화

### 3. korean-ecommerce-specialist
- 상품 키워드 최적화
- 가격 분석 및 조정
- Cafe24 자동 연동

### 4. mart-project
- 발주 관리
- 공급망 최적화
- OCR 문서 처리

## 자동 업데이트되는 문서

### README.md
- 최근 작업 기록
- 시스템 상태
- 실행 이력

### TODO.md  
- 진행 상황 추적
- 완료/대기 작업
- 자동 시간 기록

### 일일 보고서
- 위치: `D:\주문취합\주문_배송\YYYYMMDD\`
- HTML 보고서
- JSON 데이터

## 명령어 (RUN.bat 실행 후)

### 일일 작업
```bash
RUN daily     # 모든 일일 작업 실행
RUN order     # 주문 처리
RUN keyword   # 키워드 최적화  
RUN price     # 가격 분석
RUN purchase  # 발주 리스트
RUN report    # 보고서 생성
```

### 시스템 관리
```bash
RUN status    # 상태 확인
RUN cleanup   # 시스템 정리
RUN help      # 도움말
```

## 파일 구조

### 핵심 실행 파일
```
RUN.bat           # 메인 진입점
RUN.py            # 통합 실행기
```

### 시스템 파일
```
MASTER_CONTROL.py     # 중앙 제어
UNIFIED_CONFIG.py     # 환경 설정
DAILY_AUTOMATION.py   # 일일 자동화
SYSTEM_CONFIG.py      # 인코딩/안전 설정
```

### 설정 파일
```
.env              # API 키 (자동 로드)
CODING_RULES.md   # 코딩 규칙
```

## 작동 원리

1. **RUN.bat 실행**
   - 환경 변수 설정
   - UTF-8 인코딩 설정
   - 모든 Agent 초기화

2. **자동 로드**
   - .env에서 API 키 읽기
   - 캐싱으로 빠른 응답
   - 모든 프로젝트 연결

3. **작업 실행**
   - Claude 대화로 명령
   - 또는 직접 명령 실행
   - 결과 자동 문서화

4. **문서 업데이트**
   - 작업 완료시 자동
   - README.md 갱신
   - TODO.md 추적

## 보안

### API 키 관리
- 루트 .env 파일에만 저장
- 환경 변수로 자동 로드
- 하드코딩 절대 금지

### 파일 보안
- key.md 파일 제거됨
- system_backups 정리됨
- .gitignore 설정됨

## 최적화

### 성능
- 환경 변수 캐싱
- 10분마다 자동 정리
- .claude 폴더 관리

### 인코딩
- UTF-8 강제 설정
- 이모지 사용 금지
- 안전한 문자만 사용

## 문제 해결

### 인코딩 오류
- SYSTEM_CONFIG.py가 자동 처리
- chcp 65001 설정됨
- PYTHONIOENCODING=utf-8

### 멈춤 현상
- .claude/shell-snapshots 자동 정리
- 메모리 관리 활성
- 백그라운드 정리

## 업그레이드

### 새 기능 추가시
1. RUN.py에 명령 추가
2. DAILY_AUTOMATION.py에 작업 추가
3. 문서 자동 업데이트됨

### Agent 추가시
1. MASTER_CONTROL.py의 project_map 수정
2. RUN.bat의 Agent 목록 갱신
3. 자동으로 연결됨

## 결론

**RUN.bat 하나로 모든 것이 작동합니다.**

- 진입점 단일화
- Agent 자동 활성화
- 문서 자동 관리
- API 키 자동 로드
- 인코딩 문제 해결

이제 Claude와 대화하면서 모든 작업을 수행할 수 있습니다.
# 시스템 시작 가이드

## 🚀 올바른 실행 순서

### 1. 첫 실행 (아침에 한 번)
```bash
RUN.bat
# 또는
python RUN.py status
```
**이 때 일어나는 일:**
- ✅ 모든 API 키 자동 로드
- ✅ 4개 프로젝트 자동 연결
- ✅ MASTER_CONFIG.json 생성/로드
- ✅ 공유 데이터 구조 초기화
- ✅ 모든 시스템 간 연결 확립

### 2. 작업 실행 (필요할 때마다)
```bash
# 송장 처리
python RUN.py invoice

# 일일 작업
python RUN.py daily

# AI 협의회
python RUN.py council

# 아침 회의
python RUN.py morning

# 저녁 보고
python RUN.py evening
```

## 📊 데이터 공유 구조

```
RUN.py (중앙 통제)
    ↓
MASTER_CONFIG.json (공유 저장소)
    ├── AI Council 설정
    ├── SuperClaude 설정  
    ├── 송장 시스템 설정
    └── 마트 프로젝트 설정
```

## 🔄 자동 동기화

### 송장 시스템에서 수정시:
1. `SuperClaude/송장/vendor_classifier.py` 수정
2. → `sync_config.py`가 자동 감지
3. → `MASTER_CONFIG.json` 업데이트
4. → AI Council이 다음 실행시 자동 반영

### AI Council에서 결정시:
1. AI 협의회 의사결정
2. → `MASTER_CONFIG.json` 업데이트
3. → 송장 시스템이 다음 실행시 자동 반영

## ⚠️ 주의사항

1. **항상 RUN.py로 시작**
   - 직접 개별 스크립트 실행 X
   - RUN.py가 모든 초기화 담당

2. **MASTER_CONFIG.json 건드리지 않기**
   - 시스템이 자동 관리
   - 수동 편집 금지

3. **한글 인코딩**
   - 모든 파일 UTF-8
   - 환경변수 자동 설정됨

## 🎯 권장 일일 루틴

### 오전 9:00
```bash
RUN.bat morning     # AI 아침 회의
RUN.bat order       # 주문 처리
RUN.bat invoice     # 송장 작업
```

### 오후 3:00
```bash
RUN.bat status      # 상태 확인
RUN.bat purchase    # 발주 처리
```

### 오후 6:00
```bash
RUN.bat evening     # AI 저녁 보고
RUN.bat report      # 일일 보고서
```

## 🔧 문제 해결

### 한글 깨짐
```bash
chcp 65001
set PYTHONIOENCODING=utf-8
```

### 초기화 문제
```bash
# MASTER_CONFIG.json 삭제 후 재시작
del MASTER_CONFIG.json
python RUN.py status
```

### 포트 충돌
```bash
netstat -ano | findstr :5556
taskkill /PID [번호] /F
```

---
*모든 작업은 RUN.py를 통해!*
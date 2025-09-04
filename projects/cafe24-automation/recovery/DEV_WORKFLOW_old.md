# 개발 작업 흐름 가이드

## 🎯 핵심 원칙
**"수정은 직접, 실행은 RUN.py로"**

## 📝 대화하면서 수정하기

### 1. 송장 시스템 수정
```
나: "송장에서 최씨남매 처리 로직 개선해줘"
Claude: [SuperClaude/송장/vendor_classifier.py 직접 수정]
나: "테스트"
실행: python RUN.py invoice
```

### 2. AI Council 수정
```
나: "AI 협의회 의사결정 로직 개선"
Claude: [ai-council/core/ai_council.py 직접 수정]
나: "테스트"
실행: python RUN.py council
```

### 3. 키워드 최적화 수정
```
나: "키워드 추출 알고리즘 개선"
Claude: [korean-ecommerce-specialist/... 직접 수정]
나: "테스트"
실행: python RUN.py keyword
```

## 🔄 자동 동기화 흐름

```
수정 위치           →  동기화 방법        →  테스트 명령
─────────────────────────────────────────────────────────
송장 파일 수정      →  sync_config.py    →  RUN.py invoice
AI Council 수정     →  MASTER_CONFIG     →  RUN.py council  
키워드 시스템       →  MASTER_CONFIG     →  RUN.py keyword
마트 프로젝트       →  MASTER_CONFIG     →  RUN.py purchase
```

## 🚫 하지 말아야 할 것

1. **RUN.py를 통하지 않고 직접 실행**
   ```bash
   # 나쁜 예
   cd SuperClaude/송장
   python vendor_classifier.py  # ❌ 초기화 안됨
   
   # 좋은 예
   python RUN.py invoice  # ✅ 모든 초기화 완료
   ```

2. **여러 진입점 만들기**
   ```bash
   # 나쁜 예
   python SuperClaude/main.py  # ❌
   python ai-council/main.py   # ❌
   
   # 좋은 예
   python RUN.py [명령]  # ✅ 단일 진입점
   ```

## ✅ 권장 작업 패턴

### 패턴 1: 단일 기능 개선
```
1. "송장 처리 개선해줘"
2. Claude가 vendor_classifier.py 수정
3. python RUN.py invoice 테스트
4. 문제 있으면 다시 수정 요청
```

### 패턴 2: 통합 기능 개발
```
1. "송장과 AI Council 연동 강화"
2. Claude가 여러 파일 수정
   - ai_council_invoice_integration.py
   - sync_config.py
3. python RUN.py invoice 테스트
4. python RUN.py council 테스트
```

### 패턴 3: 새 기능 추가
```
1. "재고 관리 기능 추가"
2. Claude가 새 파일 생성
   - inventory_manager.py
3. RUN.py에 명령 추가
4. python RUN.py inventory 테스트
```

## 🎨 실제 대화 예시

```
사용자: "송장에서 BS 업체 처리가 잘못되고 있어"

Claude: 
[1] vendor_classifier.py 확인
[2] BS 패턴 수정
[3] sync_config.py로 자동 동기화

사용자: "테스트해봐"

Claude:
python RUN.py invoice 실행
결과 확인

사용자: "AI Council도 이 변경사항 알게 해줘"

Claude:
이미 sync_config.py가 자동 동기화했습니다!
python RUN.py council로 확인 가능
```

## 📊 파일별 수정 위치

| 작업 내용 | 수정할 파일 위치 | 테스트 명령 |
|---------|--------------|------------|
| 송장 처리 | SuperClaude/송장/*.py | RUN.py invoice |
| AI 협의회 | ai-council/*.py | RUN.py council |
| 키워드 | korean-ecommerce-specialist/*.py | RUN.py keyword |
| 발주 | mart-project/*.py | RUN.py purchase |
| 일일작업 | DAILY_AUTOMATION.py | RUN.py daily |
| 전체설정 | MASTER_CONFIG.json | RUN.py status |

## 🔧 디버깅 팁

```bash
# 수정 후 문제 발생시
python RUN.py status  # 전체 상태 확인
python RUN.py cleanup # 임시 파일 정리
python RUN.py status  # 다시 확인
```

---
**핵심: 수정은 어디서든, 실행은 RUN.py로!**
# 통합 발주 시스템 전략

## 현황 분석

### 1. CCW B2B 발주 형식
- **특징**: 
  - 복잡한 컬럼 구조 (원가, 마진율, 소비자가 등 포함)
  - 여러 시트로 구성 (B2B, 서울, 패키지, 돼지고기 등)
  - 형식이 자주 변경될 가능성

### 2. 만원요리 온라인 발주 형식  
- **특징**:
  - 날짜별 폴더 구조 (D:\주문취합\주문_배송\YYYYMMDD\)
  - 표준화된 형식
  - 온라인 주문 데이터

## 제안하는 해결 방안

### 1. 적응형 템플릿 시스템 (Adaptive Template System)

```python
class OrderTemplateAdapter:
    """다양한 발주서 형식을 자동으로 인식하고 처리"""
    
    def __init__(self):
        self.templates = {
            'ccw_b2b': CCWTemplate(),
            'manwon_online': ManwonTemplate(),
            'custom': CustomTemplate()
        }
    
    def auto_detect_format(self, file_path):
        """파일 형식 자동 감지"""
        # 컬럼명, 시트명 등으로 형식 판단
        pass
    
    def extract_core_data(self, df):
        """핵심 데이터만 추출"""
        # 형식과 관계없이 필수 정보만 추출
        return {
            'product_name': ...,
            'quantity': ...,
            'price': ...,
            'delivery_date': ...
        }
```

### 2. 유연한 매핑 규칙 (Flexible Mapping Rules)

**컬럼 매핑 설정 파일** (`config/column_mappings.json`):
```json
{
  "ccw_b2b": {
    "product_name": ["상품명", "품명", "제품명"],
    "quantity": ["수량", "주문수량", "발주수량"],
    "price": ["원가", "납품가", "단가"],
    "total": ["금액계", "합계", "총액"]
  },
  "manwon_online": {
    "product_name": ["상품명"],
    "quantity": ["수량"],
    "price": ["단가"],
    "customer": ["주문자"]
  }
}
```

### 3. 변화 추적 시스템 (Change Tracking System)

```python
class FormatChangeTracker:
    """발주서 형식 변경 자동 감지 및 대응"""
    
    def detect_changes(self, new_file, template_history):
        """새로운 형식 변경사항 감지"""
        changes = []
        # 컬럼 추가/삭제/변경 감지
        # 시트 구조 변경 감지
        return changes
    
    def adapt_to_changes(self, changes):
        """변경사항에 자동 적응"""
        # 매핑 규칙 업데이트
        # 사용자에게 확인 요청
        pass
```

### 4. 통합 데이터 모델 (Unified Data Model)

**핵심 발주 데이터 구조**:
```python
@dataclass
class UnifiedOrder:
    # 필수 필드
    order_date: datetime
    supplier: str
    items: List[OrderItem]
    delivery_date: datetime
    
    # 선택 필드 (있으면 좋고, 없어도 처리 가능)
    order_number: Optional[str]
    payment_terms: Optional[str]
    notes: Optional[str]
    
    # 확장 필드 (특정 업체만 사용)
    margin_rate: Optional[float]  # CCW용
    consumer_price: Optional[float]  # CCW용
    customer_info: Optional[dict]  # 만원요리용
```

### 5. 실시간 동기화 아키텍처

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────┐
│   CCW B2B       │────▶│   통합 엔진   │────▶│  통합 DB     │
│   Excel 파일    │     │              │     │              │
└─────────────────┘     │  - 형식 감지  │     │  표준화된    │
                        │  - 데이터 추출 │     │  발주 데이터  │
┌─────────────────┐     │  - 검증       │     │              │
│  만원요리 온라인  │────▶│  - 변환       │     └──────────────┘
│   주문 데이터    │     │              │              │
└─────────────────┘     └──────────────┘              ▼
                                              ┌──────────────┐
                                              │   보고서     │
                                              │   API 연동   │
                                              │   분석       │
                                              └──────────────┘
```

## 구현 우선순위

### Phase 1: 기초 구축 (1주)
1. ✅ 통합 데이터 모델 정의
2. ✅ CCW B2B 형식 파서 구현
3. ✅ 만원요리 온라인 형식 파서 구현

### Phase 2: 자동화 (2주)
1. 형식 자동 감지 기능
2. 컬럼 매핑 자동화
3. 에러 처리 및 복구

### Phase 3: 고급 기능 (3주)
1. 형식 변경 감지 및 알림
2. 실시간 동기화
3. API 연동 (온라인 시스템)

## 핵심 권장사항

### 1. **형식 독립적 설계**
- 특정 형식에 의존하지 않는 코어 로직
- 플러그인 방식으로 새 형식 추가 가능

### 2. **버전 관리**
- 각 발주서 형식의 버전 추적
- 변경 이력 관리

### 3. **검증 시스템**
```python
class OrderValidator:
    def validate_required_fields(self, data):
        """필수 필드 검증"""
        pass
    
    def validate_data_integrity(self, data):
        """데이터 무결성 검증 (수량*단가=합계 등)"""
        pass
    
    def validate_business_rules(self, data):
        """비즈니스 규칙 검증 (최소주문금액 등)"""
        pass
```

### 4. **사용자 피드백 루프**
- 형식 변경 시 사용자 확인
- 매핑 실패 시 수동 매핑 옵션
- 학습을 통한 자동화 개선

## 예상 효과

1. **형식 변경에 강건한 시스템**
   - 컬럼명이 바뀌어도 자동 적응
   - 새로운 형식도 쉽게 추가

2. **운영 효율성**
   - 수동 작업 90% 감소
   - 오류율 최소화

3. **확장성**
   - 새로운 거래처 추가 용이
   - API 연동으로 실시간 처리

4. **데이터 일관성**
   - 모든 발주 데이터 표준화
   - 통합 분석 및 보고 가능
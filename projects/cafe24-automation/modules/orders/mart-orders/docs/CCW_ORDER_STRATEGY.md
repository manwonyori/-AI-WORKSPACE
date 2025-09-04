# CCW 발주서 처리 전략

## 현재 상황 분석

### CCW 엑셀 구조의 특징
1. **복잡한 구조**: 좌측에 기본 정보, 우측에 실제 주문
2. **실제 발주**: U열(20번 컬럼)에만 실제 주문 수량 
3. **대부분 미사용**: 48개 품목 중 실제 발주는 2개뿐
4. **형식 변경 가능성**: 시트 구조가 자주 바뀔 수 있음

## 제안하는 발주서 처리 방안

### 방안 1: 스마트 필터링 시스템 (권장)

```python
class SmartOrderFilter:
    """실제 주문만 추출하는 스마트 시스템"""
    
    def extract_actual_orders(self, excel_file):
        # U열(주문수)이 0보다 큰 행만 추출
        actual_orders = []
        for row in data:
            if row['주문수'] > 0:
                actual_orders.append({
                    '상품명': row['B열'],
                    '수량': row['U열'],
                    '단가': row['E열'],
                    '금액': row['U열'] * row['E열']
                })
        return actual_orders
```

**장점:**
- 불필요한 데이터 제거
- 실제 발주만 정확히 처리
- 처리 속도 향상

### 방안 2: 이중 확인 시스템

```python
class DualVerificationSystem:
    """발주 전 이중 확인"""
    
    def process_order(self, file):
        # 1차: 자동 추출
        orders = extract_orders(file)
        
        # 2차: 사용자 확인
        print("다음 품목이 발주됩니다:")
        for item in orders:
            print(f"- {item['name']}: {item['qty']}개")
        
        confirm = input("확인하셨습니까? (y/n): ")
        
        if confirm == 'y':
            # 3차: 웰빙신선식품에 발주서 전송
            send_to_supplier(orders)
```

### 방안 3: 템플릿 매칭 시스템

**CCW 전용 템플릿 생성:**

```yaml
ccw_template:
  header_row: 2
  columns:
    product_name: 
      - B (index: 1)  # 기본 상품명
      - N (index: 13) # 확인용 상품명
    order_quantity: U (index: 20)
    unit_price: E (index: 4)
    original_price: C (index: 2)
  filter_rules:
    - only_if: order_quantity > 0
    - skip_if: product_name contains "상품명"
```

## 구체적 구현 방안

### 1단계: 즉시 구현 가능한 간단한 솔루션

```python
def process_ccw_order_simple(file_path):
    """CCW 발주서 간단 처리"""
    
    df = pd.read_excel(file_path, sheet_name='CCW B2B수급', header=None)
    
    orders = []
    for i, row in df.iterrows():
        # U열(20)에 주문수량이 있는 경우만
        if len(row) > 20 and row.iloc[20] > 0:
            orders.append({
                '상품명': row.iloc[1],  # B열
                '수량': row.iloc[20],    # U열
                '단가': row.iloc[4]      # E열
            })
    
    # 발주서 생성
    create_purchase_order(orders, '웰빙신선식품')
    return orders
```

### 2단계: 자동화 및 검증 추가

```python
class CCWOrderProcessor:
    def __init__(self):
        self.supplier = "웰빙신선식품"
        self.column_map = {
            'product': 1,   # B열
            'quantity': 20, # U열
            'price': 4      # E열
        }
    
    def validate_order(self, orders):
        """발주 검증"""
        issues = []
        
        for order in orders:
            # 수량 체크
            if order['quantity'] <= 0:
                issues.append(f"{order['product']}: 수량 오류")
            
            # 가격 체크
            if order['price'] <= 0:
                issues.append(f"{order['product']}: 가격 오류")
        
        return issues
    
    def generate_report(self, orders):
        """발주 보고서 생성"""
        total = sum(o['quantity'] * o['price'] for o in orders)
        
        report = f"""
        발주일: {datetime.now()}
        공급업체: {self.supplier}
        
        발주 품목:
        """
        for o in orders:
            report += f"- {o['product']}: {o['quantity']}개\n"
        
        report += f"\n총액: {total:,}원"
        return report
```

### 3단계: 실시간 모니터링

```python
class OrderMonitor:
    """발주 실시간 모니터링"""
    
    def watch_folder(self, folder_path):
        """폴더 감시 - 새 파일 자동 처리"""
        for file in new_files:
            if 'ccw' in file.lower():
                orders = process_ccw_order(file)
                
                if orders:
                    # 알림 전송
                    notify_manager(orders)
                    
                    # 자동 발주 (설정된 경우)
                    if auto_order_enabled:
                        send_order_to_supplier(orders)
```

## 권장 구현 순서

### Phase 1 (즉시) - 기본 기능
1. ✅ U열 주문수량 추출
2. ✅ 웰빙신선식품 발주서 생성
3. ✅ Excel/PDF 출력

### Phase 2 (1주) - 검증 추가
1. 이중 확인 시스템
2. 오류 검출 (수량/가격)
3. 발주 이력 저장

### Phase 3 (2주) - 자동화
1. 폴더 모니터링
2. 자동 발주서 전송
3. 이메일/카톡 알림

## 실제 사용 시나리오

```python
# 1. CCW 파일 업로드
processor = CCWOrderProcessor()

# 2. 주문 추출
orders = processor.extract_orders('ccw 발주.xlsx')
# 결과: 이태원 햄폭탄 3개, 힘찬 장어탕 15개

# 3. 검증
issues = processor.validate_order(orders)
if not issues:
    # 4. 발주서 생성
    po = processor.create_purchase_order(orders)
    
    # 5. 전송
    processor.send_to_supplier(po)
    
    # 6. 기록
    processor.save_history(orders)
```

## 핵심 포인트

1. **단순함 우선**: 복잡한 엑셀에서 필요한 2개 컬럼만 추출
2. **검증 필수**: 발주 전 반드시 확인
3. **이력 관리**: 모든 발주 기록 저장
4. **확장 가능**: 나중에 기능 추가 용이

## 예상 효과

- **시간 절약**: 수동 작업 5분 → 자동 처리 5초
- **오류 감소**: 실수 방지
- **이력 추적**: 모든 발주 기록
- **즉시 대응**: 실시간 처리
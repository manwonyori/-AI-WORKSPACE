#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import json
import logging
import pandas as pd
import re

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
적응형 발주 시스템 - 다양한 형식 자동 처리
"""

@dataclass
class OrderItem:
    """발주 품목 표준 모델"""
    product_name: str
    quantity: float
    unit: str = "개"
    unit_price: float = 0.0
    total_price: float = 0.0
    # 확장 필드
    margin_rate: Optional[float] = None
    consumer_price: Optional[float] = None
    notes: Optional[str] = None

@dataclass 
class UnifiedOrder:
    """통합 발주 데이터 모델"""
    order_date: datetime
    supplier: str
    items: List[OrderItem]
    delivery_date: Optional[datetime] = None
    order_number: Optional[str] = None
    payment_terms: Optional[str] = None
    customer_info: Optional[Dict] = None
    source_file: Optional[str] = None
    format_type: Optional[str] = None

class AdaptiveOrderSystem:
    """다양한 발주서 형식을 자동으로 처리하는 시스템"""
    
    def __init__(self):
        self.config_dir = Path("config")
        self.config_dir.mkdir(exist_ok=True)
        
        # 컬럼 매핑 규칙 로드
        self.column_mappings = self.load_column_mappings()
        
        # 형식별 파서
        self.parsers = {
            'ccw_b2b': self.parse_ccw_b2b,
            'manwon_online': self.parse_manwon_online,
            'wellbeing': self.parse_wellbeing
        }
    
    def load_column_mappings(self) -> Dict:
        """컬럼 매핑 규칙 로드"""
        mapping_file = self.config_dir / "column_mappings.json"
        
        if mapping_file.exists():
            with open(mapping_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 기본 매핑
        default_mappings = {
            "ccw_b2b": {
                "product_name": ["상품명", "품명", "제품명", "상품"],
                "quantity": ["수량", "주문수량", "발주수량", "갯수"],
                "price": ["원가", "납품가", "단가", "원가(납품가)"],
                "total": ["금액계", "합계", "총액", "금액"],
                "consumer_price": ["소비자가", "판매가"]
            },
            "manwon_online": {
                "product_name": ["상품명", "품명", "메뉴명"],
                "quantity": ["수량", "주문수량"],
                "price": ["단가", "가격"],
                "customer": ["주문자", "고객명", "수령인"]
            },
            "general": {
                "product_name": ["상품명", "품명", "제품명", "품목", "상품", "메뉴"],
                "quantity": ["수량", "주문수량", "발주수량", "갯수", "개수"],
                "price": ["단가", "가격", "원가", "납품가"],
                "total": ["금액", "합계", "총액", "금액계"]
            }
        }
        
        # 저장
        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump(default_mappings, f, ensure_ascii=False, indent=2)
        
        return default_mappings
    
    def detect_format(self, file_path: str) -> str:
        """파일 형식 자동 감지"""
        file_path = Path(file_path)
        
        # 파일명으로 판단
        if "ccw" in file_path.name.lower():
            return "ccw_b2b"
        elif "만원요리" in file_path.name or "반찬단지" in file_path.name:
            return "manwon_online"
        elif "웰빙" in file_path.name.lower():
            return "wellbeing"
        
        # Excel 파일인 경우 시트명으로 판단
        if file_path.suffix.lower() in ['.xlsx', '.xls']:
            try:
                excel_file = pd.ExcelFile(file_path)
                sheet_names = excel_file.sheet_names
                
                if any("B2B" in name for name in sheet_names):
                    return "ccw_b2b"
                elif any("주문" in name for name in sheet_names):
                    return "manwon_online"
            except:
                pass
        
        return "general"
    
    def find_column(self, df: pd.DataFrame, possible_names: List[str]) -> Optional[str]:
        """데이터프레임에서 가능한 컬럼명 찾기"""
        df_columns = [str(col).strip() for col in df.columns]
        
        for name in possible_names:
            # 정확한 매칭
            if name in df_columns:
                return name
            
            # 부분 매칭
            for col in df_columns:
                if name in col or col in name:
                    return col
        
        return None
    
    def parse_ccw_b2b(self, file_path: str) -> UnifiedOrder:
        """CCW B2B 발주서 파싱"""
        try:
            # CCW B2B수급 시트 읽기
            df = pd.read_excel(file_path, sheet_name='CCW B2B수급', header=1)
            
            items = []
            for idx, row in df.iterrows():
                # CCW 형식: 1열=상품명, 3열=수량, 4열=단가
                if len(row) > 4:
                    product_name = str(row.iloc[1])
                    
                    # 빈 행이나 헤더 스킵
                    if not product_name or product_name == 'nan' or '상품명' in product_name:
                        continue
                    
                    try:
                        item = OrderItem(
                            product_name=product_name.strip(),
                            quantity=float(row.iloc[3]) if pd.notna(row.iloc[3]) else 0,
                            unit="개",
                            unit_price=float(row.iloc[4]) if pd.notna(row.iloc[4]) else 0,
                            total_price=float(row.iloc[5]) if len(row) > 5 and pd.notna(row.iloc[5]) else 0
                        )
                        items.append(item)
                    except (ValueError, TypeError):
                        continue
            
            # 통합 발주 객체 생성
            order = UnifiedOrder(
                order_date=datetime.now(),
                supplier="CCW",
                items=items,
                source_file=str(file_path),
                format_type="ccw_b2b"
            )
            
            return order
            
        except Exception as e:
            print(f"CCW B2B 파싱 오류: {str(e)}")
            return None
    
    def parse_manwon_online(self, file_path: str) -> UnifiedOrder:
        """만원요리 온라인 발주서 파싱"""
        try:
            df = pd.read_excel(file_path)
            
            # 날짜 추출 (파일명에서)
            date_match = re.search(r'\d{8}', str(file_path))
            order_date = datetime.strptime(date_match.group(), '%Y%m%d') if date_match else datetime.now()
            
            mappings = self.column_mappings.get('manwon_online', {})
            
            items = []
            for _, row in df.iterrows():
                product_col = self.find_column(df, mappings.get('product_name', []))
                qty_col = self.find_column(df, mappings.get('quantity', []))
                
                if product_col and qty_col:
                    product_name = str(row.get(product_col, '')).strip()
                    if not product_name or product_name == 'nan':
                        continue
                    
                    items.append(OrderItem(
                        product_name=product_name,
                        quantity=float(row.get(qty_col, 0)),
                        unit="개"
                    ))
            
            return UnifiedOrder(
                order_date=order_date,
                supplier="만원요리",
                items=items,
                source_file=str(file_path),
                format_type="manwon_online"
            )
            
        except Exception as e:
            print(f"만원요리 파싱 오류: {str(e)}")
            return None
    
    def parse_wellbeing(self, file_path: str) -> UnifiedOrder:
        """웰빙 발주서 파싱"""
        # 웰빙신선식품용 파서
        return self.parse_general(file_path)
    
    def parse_general(self, file_path: str) -> UnifiedOrder:
        """범용 발주서 파싱"""
        try:
            # Excel 파일 읽기
            if Path(file_path).suffix.lower() in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            else:
                df = pd.read_csv(file_path, encoding='utf-8-sig')
            
            mappings = self.column_mappings.get('general', {})
            
            items = []
            for _, row in df.iterrows():
                product_col = self.find_column(df, mappings.get('product_name', []))
                qty_col = self.find_column(df, mappings.get('quantity', []))
                
                if product_col:
                    product_name = str(row.get(product_col, '')).strip()
                    if not product_name or product_name == 'nan':
                        continue
                    
                    items.append(OrderItem(
                        product_name=product_name,
                        quantity=float(row.get(qty_col, 1)) if qty_col else 1,
                        unit="개"
                    ))
            
            return UnifiedOrder(
                order_date=datetime.now(),
                supplier="General",
                items=items,
                source_file=str(file_path),
                format_type="general"
            )
            
        except Exception as e:
            print(f"일반 파싱 오류: {str(e)}")
            return None
    
    def process_order_file(self, file_path: str) -> UnifiedOrder:
        """발주 파일 처리 메인 함수"""
        print(f"\n파일 처리 중: {file_path}")
        
        # 1. 형식 감지
        format_type = self.detect_format(file_path)
        print(f"감지된 형식: {format_type}")
        
        # 2. 적절한 파서 선택
        parser = self.parsers.get(format_type, self.parse_general)
        
        # 3. 파싱 실행
        order = parser(file_path)
        
        if order:
            print(f"성공적으로 파싱됨: {len(order.items)}개 품목")
            return order
        else:
            print("파싱 실패")
            return None
    
    def save_unified_order(self, order: UnifiedOrder, output_dir: str = "data/unified_orders"):
        """통합 발주 데이터 저장"""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # JSON으로 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = output_dir / f"order_{order.supplier}_{timestamp}.json"
        
        # dataclass를 dict로 변환
        order_dict = {
            "order_date": order.order_date.isoformat() if order.order_date else None,
            "delivery_date": order.delivery_date.isoformat() if order.delivery_date else None,
            "supplier": order.supplier,
            "order_number": order.order_number,
            "payment_terms": order.payment_terms,
            "source_file": order.source_file,
            "format_type": order.format_type,
            "items": [
                {
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "unit": item.unit,
                    "unit_price": item.unit_price,
                    "total_price": item.total_price,
                    "margin_rate": item.margin_rate,
                    "consumer_price": item.consumer_price,
                    "notes": item.notes
                }
                for item in order.items
            ],
            "summary": {
                "total_items": len(order.items),
                "total_quantity": sum(item.quantity for item in order.items),
                "total_amount": sum(item.total_price for item in order.items)
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(order_dict, f, ensure_ascii=False, indent=2)
        
        print(f"저장됨: {filename}")
        return filename

# 실행 예제
if __name__ == "__main__":
    system = AdaptiveOrderSystem()
    
    # 테스트할 파일 경로들
    test_files = [
        r"C:\Users\8899y\mart-project\tests\ccw 발주.xlsx",
        # r"D:\주문취합\주문_배송\20250821\만원요리_반찬단지_20250821.xlsx"
    ]
    
    for file_path in test_files:
        if Path(file_path).exists():
            order = system.process_order_file(file_path)
            if order:
                system.save_unified_order(order)
                
                # 간단한 요약 출력
                print(f"\n[발주 요약]")
                print(f"공급업체: {order.supplier}")
                print(f"품목 수: {len(order.items)}")
                print(f"주요 품목:")
                for item in order.items[:5]:  # 처음 5개만
                    print(f"  - {item.product_name}: {item.quantity}{item.unit}")
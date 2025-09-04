"""
재고 추적 및 관리 모듈
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class InventoryTracker:
    """재고 관리 클래스"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.inventory_file = self.data_dir / "inventory.json"
        self.transactions_file = self.data_dir / "inventory_transactions.json"
        self.inventory = self.load_inventory()
        self.transactions = self.load_transactions()
    
    def load_inventory(self) -> Dict:
        """재고 데이터 로드"""
        if self.inventory_file.exists():
            with open(self.inventory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def load_transactions(self) -> List:
        """거래 내역 로드"""
        if self.transactions_file.exists():
            with open(self.transactions_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_inventory(self):
        """재고 데이터 저장"""
        with open(self.inventory_file, 'w', encoding='utf-8') as f:
            json.dump(self.inventory, f, ensure_ascii=False, indent=2)
    
    def save_transactions(self):
        """거래 내역 저장"""
        with open(self.transactions_file, 'w', encoding='utf-8') as f:
            json.dump(self.transactions, f, ensure_ascii=False, indent=2)
    
    def show_current_inventory(self):
        """현재 재고 조회"""
        print("\n[현재 재고 현황]")
        
        if not self.inventory:
            print("재고가 없습니다.")
            return
        
        # 카테고리별 정리
        categories = {}
        for item_code, item in self.inventory.items():
            category = item.get('category', '기타')
            if category not in categories:
                categories[category] = []
            categories[category].append(item)
        
        print(f"총 {len(self.inventory)}개 품목")
        print("=" * 80)
        
        for category, items in sorted(categories.items()):
            print(f"\n[{category}]")
            for item in sorted(items, key=lambda x: x['name']):
                stock_status = self._get_stock_status(item)
                print(f"  {item['name']:<20} | 재고: {item['quantity']:>6}{item['unit']} | {stock_status}")
                
                # 재고 부족 경고
                if item['quantity'] <= item.get('min_stock', 10):
                    print(f"    ⚠ 재고 부족! 최소 재고: {item.get('min_stock', 10)}{item['unit']}")
    
    def _get_stock_status(self, item: Dict) -> str:
        """재고 상태 확인"""
        quantity = item['quantity']
        min_stock = item.get('min_stock', 10)
        
        if quantity <= 0:
            return "품절"
        elif quantity <= min_stock:
            return "재고 부족"
        elif quantity <= min_stock * 2:
            return "재고 주의"
        else:
            return "정상"
    
    def register_incoming(self):
        """재고 입고 등록"""
        print("\n[재고 입고 등록]")
        
        # 품목 정보 입력
        item_code = input("품목 코드: ").strip()
        
        if item_code in self.inventory:
            item = self.inventory[item_code]
            print(f"기존 품목: {item['name']}")
        else:
            # 신규 품목 등록
            print("신규 품목입니다.")
            name = input("품목명: ").strip()
            category = input("카테고리: ").strip()
            unit = input("단위 (kg, 개, 박스 등): ").strip()
            min_stock = int(input("최소 재고량: ").strip() or "10")
            
            item = {
                "code": item_code,
                "name": name,
                "category": category,
                "unit": unit,
                "quantity": 0,
                "min_stock": min_stock,
                "avg_price": 0,
                "last_updated": datetime.now().isoformat()
            }
            self.inventory[item_code] = item
        
        # 입고 수량 및 정보
        quantity = float(input(f"입고 수량 ({item['unit']}): ").strip())
        price = float(input("단가: ").strip())
        supplier = input("공급업체명: ").strip()
        
        # 재고 업데이트
        old_quantity = item['quantity']
        item['quantity'] += quantity
        
        # 평균 단가 계산
        if old_quantity > 0:
            item['avg_price'] = ((item['avg_price'] * old_quantity) + (price * quantity)) / item['quantity']
        else:
            item['avg_price'] = price
        
        item['last_updated'] = datetime.now().isoformat()
        
        # 거래 내역 기록
        transaction = {
            "type": "incoming",
            "date": datetime.now().isoformat(),
            "item_code": item_code,
            "item_name": item['name'],
            "quantity": quantity,
            "unit": item['unit'],
            "price": price,
            "total_amount": price * quantity,
            "supplier": supplier,
            "balance_after": item['quantity']
        }
        
        self.transactions.append(transaction)
        
        # 저장
        self.save_inventory()
        self.save_transactions()
        
        logger.info(f"입고 등록: {item['name']} {quantity}{item['unit']} from {supplier}")
        print(f"\n입고가 완료되었습니다.")
        print(f"품목: {item['name']}")
        print(f"수량: {quantity}{item['unit']}")
        print(f"현재 재고: {item['quantity']}{item['unit']}")
    
    def register_outgoing(self):
        """재고 출고 등록"""
        print("\n[재고 출고 등록]")
        
        if not self.inventory:
            print("재고가 없습니다.")
            return
        
        # 품목 선택
        print("\n출고할 품목 코드를 입력하세요:")
        for code, item in self.inventory.items():
            print(f"  {code}: {item['name']} (재고: {item['quantity']}{item['unit']})")
        
        item_code = input("\n품목 코드: ").strip()
        
        if item_code not in self.inventory:
            print("존재하지 않는 품목입니다.")
            return
        
        item = self.inventory[item_code]
        
        # 출고 수량
        max_quantity = item['quantity']
        quantity = float(input(f"출고 수량 (최대 {max_quantity}{item['unit']}): ").strip())
        
        if quantity > max_quantity:
            print("재고가 부족합니다.")
            return
        
        purpose = input("출고 목적: ").strip()
        
        # 재고 업데이트
        item['quantity'] -= quantity
        item['last_updated'] = datetime.now().isoformat()
        
        # 거래 내역 기록
        transaction = {
            "type": "outgoing",
            "date": datetime.now().isoformat(),
            "item_code": item_code,
            "item_name": item['name'],
            "quantity": quantity,
            "unit": item['unit'],
            "purpose": purpose,
            "balance_after": item['quantity']
        }
        
        self.transactions.append(transaction)
        
        # 저장
        self.save_inventory()
        self.save_transactions()
        
        logger.info(f"출고 등록: {item['name']} {quantity}{item['unit']}")
        print(f"\n출고가 완료되었습니다.")
        print(f"품목: {item['name']}")
        print(f"수량: {quantity}{item['unit']}")
        print(f"남은 재고: {item['quantity']}{item['unit']}")
        
        # 재고 부족 경고
        if item['quantity'] <= item.get('min_stock', 10):
            print(f"\n⚠ 주의: 재고가 최소 수량({item.get('min_stock', 10)}{item['unit']}) 이하입니다!")
    
    def setup_auto_order(self):
        """자동 발주 설정"""
        print("\n[자동 발주 설정]")
        
        if not self.inventory:
            print("재고가 없습니다.")
            return
        
        print("\n자동 발주를 설정할 품목:")
        for code, item in self.inventory.items():
            print(f"  {code}: {item['name']}")
        
        item_code = input("\n품목 코드: ").strip()
        
        if item_code not in self.inventory:
            print("존재하지 않는 품목입니다.")
            return
        
        item = self.inventory[item_code]
        
        print(f"\n현재 설정:")
        print(f"  최소 재고: {item.get('min_stock', 10)}{item['unit']}")
        print(f"  자동 발주: {item.get('auto_order', False)}")
        
        min_stock = int(input("최소 재고량: ").strip())
        order_quantity = int(input("발주 수량: ").strip())
        
        item['min_stock'] = min_stock
        item['auto_order'] = True
        item['auto_order_quantity'] = order_quantity
        
        self.save_inventory()
        
        print(f"\n자동 발주가 설정되었습니다.")
        print(f"재고가 {min_stock}{item['unit']} 이하가 되면")
        print(f"자동으로 {order_quantity}{item['unit']}을(를) 발주합니다.")
    
    def get_item_count(self) -> int:
        """재고 품목 수 반환"""
        return len(self.inventory)
    
    def get_low_stock_items(self) -> List[Dict]:
        """재고 부족 품목 조회"""
        low_stock = []
        for item in self.inventory.values():
            if item['quantity'] <= item.get('min_stock', 10):
                low_stock.append(item)
        return low_stock
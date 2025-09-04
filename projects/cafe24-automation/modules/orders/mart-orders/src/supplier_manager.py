"""
공급업체 관리 모듈
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class SupplierManager:
    """공급업체 관리 클래스"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.suppliers_file = self.data_dir / "suppliers.json"
        self.suppliers = self.load_suppliers()
    
    def load_suppliers(self) -> Dict:
        """공급업체 데이터 로드"""
        if self.suppliers_file.exists():
            with open(self.suppliers_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_suppliers(self):
        """공급업체 데이터 저장"""
        with open(self.suppliers_file, 'w', encoding='utf-8') as f:
            json.dump(self.suppliers, f, ensure_ascii=False, indent=2)
    
    def register_new_supplier(self):
        """신규 공급업체 등록"""
        print("\n[신규 공급업체 등록]")
        
        # 기본 정보 입력
        business_number = input("사업자등록번호: ").strip()
        
        if business_number in self.suppliers:
            print("이미 등록된 사업자입니다.")
            return
        
        name = input("업체명: ").strip()
        representative = input("대표자명: ").strip()
        contact = input("연락처: ").strip()
        address = input("주소: ").strip()
        
        # 취급 품목 입력
        print("\n취급 품목을 입력하세요 (쉼표로 구분):")
        items = [item.strip() for item in input().split(',')]
        
        # 공급업체 정보 저장
        supplier_info = {
            "business_number": business_number,
            "name": name,
            "representative": representative,
            "contact": contact,
            "address": address,
            "items": items,
            "registered_date": datetime.now().isoformat(),
            "transactions": [],
            "rating": 5.0,
            "status": "active"
        }
        
        self.suppliers[business_number] = supplier_info
        self.save_suppliers()
        
        logger.info(f"신규 공급업체 등록: {name} ({business_number})")
        print(f"\n공급업체 '{name}'이(가) 성공적으로 등록되었습니다.")
    
    def list_suppliers(self):
        """공급업체 목록 조회"""
        print("\n[공급업체 목록]")
        
        if not self.suppliers:
            print("등록된 공급업체가 없습니다.")
            return
        
        print(f"\n총 {len(self.suppliers)}개 업체")
        print("-" * 80)
        
        for idx, (biz_num, info) in enumerate(self.suppliers.items(), 1):
            status_mark = "[OK]" if info['status'] == 'active' else "[FAIL]"
            print(f"{idx}. [{status_mark}] {info['name']}")
            print(f"   사업자번호: {biz_num}")
            print(f"   대표자: {info['representative']}")
            print(f"   연락처: {info['contact']}")
            print(f"   취급품목: {', '.join(info['items'][:3])}")
            if len(info['items']) > 3:
                print(f"            외 {len(info['items'])-3}개")
            print(f"   평점: {'★' * int(info.get('rating', 5))}")
            print()
    
    def update_supplier(self):
        """공급업체 정보 수정"""
        print("\n[공급업체 정보 수정]")
        
        business_number = input("수정할 사업자등록번호: ").strip()
        
        if business_number not in self.suppliers:
            print("등록되지 않은 사업자입니다.")
            return
        
        supplier = self.suppliers[business_number]
        print(f"\n현재 정보: {supplier['name']}")
        
        print("\n수정할 항목을 선택하세요:")
        print("1. 연락처")
        print("2. 주소")
        print("3. 취급 품목")
        print("4. 상태 (활성/비활성)")
        
        choice = input("선택: ").strip()
        
        if choice == "1":
            new_contact = input("새 연락처: ").strip()
            supplier['contact'] = new_contact
        elif choice == "2":
            new_address = input("새 주소: ").strip()
            supplier['address'] = new_address
        elif choice == "3":
            print("새 취급 품목 (쉼표로 구분):")
            new_items = [item.strip() for item in input().split(',')]
            supplier['items'] = new_items
        elif choice == "4":
            new_status = input("상태 (active/inactive): ").strip()
            supplier['status'] = new_status
        
        supplier['updated_date'] = datetime.now().isoformat()
        self.save_suppliers()
        
        print("정보가 성공적으로 수정되었습니다.")
    
    def scan_business_license(self):
        """사업자등록증 스캔 (시뮬레이션)"""
        print("\n[사업자등록증 스캔]")
        print("이미지 파일 경로를 입력하세요:")
        image_path = input().strip()
        
        # 실제로는 OCR 처리를 하겠지만, 여기서는 시뮬레이션
        print("\n이미지 처리 중...")
        print("OCR 인식 중...")
        
        # 예시 데이터
        print("\n인식된 정보:")
        print("사업자등록번호: 123-45-67890")
        print("상호: 신선식품유통")
        print("대표자: 홍길동")
        print("사업장소재지: 서울특별시 강남구")
        
        confirm = input("\n이 정보로 등록하시겠습니까? (y/n): ").strip()
        
        if confirm.lower() == 'y':
            print("공급업체가 등록되었습니다.")
    
    def get_supplier_count(self) -> int:
        """등록된 공급업체 수 반환"""
        return len(self.suppliers)
    
    def get_supplier_info(self, business_number: str) -> Optional[Dict]:
        """특정 공급업체 정보 조회"""
        return self.suppliers.get(business_number)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from pathlib import Path
import json
import logging

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
대화형 공급업체 등록 시스템
"""

def register_supplier_interactive():
    """대화형 공급업체 등록"""
    
    print("\n=== 신규 공급업체 등록 ===\n")
    
    # 데이터 디렉토리 확인
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    suppliers_file = data_dir / "suppliers.json"
    
    # 기존 데이터 로드
    if suppliers_file.exists():
        with open(suppliers_file, 'r', encoding='utf-8') as f:
            suppliers = json.load(f)
    else:
        suppliers = {}
    
    print("공급업체 정보를 입력해주세요.\n")
    
    # 사업자등록번호
    while True:
        business_number = input("사업자등록번호 (123-45-67890 형식): ").strip()
        if business_number in suppliers:
            print("❌ 이미 등록된 사업자번호입니다. 다시 입력해주세요.")
        elif len(business_number) == 12 and business_number[3] == '-' and business_number[6] == '-':
            break
        else:
            print("❌ 올바른 형식이 아닙니다. (예: 123-45-67890)")
    
    # 업체명
    name = input("업체명: ").strip()
    while not name:
        print("❌ 업체명은 필수입니다.")
        name = input("업체명: ").strip()
    
    # 대표자명
    representative = input("대표자명: ").strip()
    while not representative:
        print("❌ 대표자명은 필수입니다.")
        representative = input("대표자명: ").strip()
    
    # 연락처
    contact = input("연락처 (예: 02-1234-5678 또는 010-1234-5678): ").strip()
    
    # 주소
    address = input("주소: ").strip()
    
    # 이메일
    email = input("이메일 (선택사항): ").strip()
    
    # 취급 품목
    print("\n취급 품목을 입력하세요.")
    print("(쉼표로 구분, 예: 양파, 당근, 감자)")
    items_input = input("취급 품목: ").strip()
    items = [item.strip() for item in items_input.split(',') if item.strip()]
    
    # 공급 조건
    print("\n공급 조건을 설정하세요.")
    min_order = input("최소 주문 금액 (원, 선택사항): ").strip()
    delivery_days = input("배송 소요일 (일, 선택사항): ").strip()
    payment_terms = input("결제 조건 (예: 월말정산, 현금결제): ").strip() or "월말정산"
    
    # 데이터 구성
    supplier_info = {
        "business_number": business_number,
        "name": name,
        "representative": representative,
        "contact": contact,
        "address": address,
        "email": email,
        "items": items,
        "min_order": int(min_order) if min_order.isdigit() else None,
        "delivery_days": int(delivery_days) if delivery_days.isdigit() else None,
        "payment_terms": payment_terms,
        "registered_date": datetime.now().isoformat(),
        "status": "active",
        "rating": 5.0,
        "transaction_count": 0,
        "total_amount": 0
    }
    
    # 확인
    print("\n=== 입력 정보 확인 ===")
    print(f"업체명: {name}")
    print(f"사업자번호: {business_number}")
    print(f"대표자: {representative}")
    print(f"연락처: {contact}")
    print(f"주소: {address}")
    print(f"이메일: {email if email else '미입력'}")
    print(f"취급 품목: {', '.join(items) if items else '미입력'}")
    print(f"최소 주문: {f'{min_order:,}원' if min_order else '제한 없음'}")
    print(f"배송일: {f'{delivery_days}일' if delivery_days else '미정'}")
    print(f"결제 조건: {payment_terms}")
    
    confirm = input("\n이 정보로 등록하시겠습니까? (y/n): ").strip().lower()
    
    if confirm == 'y':
        # 저장
        suppliers[business_number] = supplier_info
        with open(suppliers_file, 'w', encoding='utf-8') as f:
            json.dump(suppliers, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ '{name}' 공급업체가 성공적으로 등록되었습니다!")
        print(f"등록번호: {business_number}")
        
        # 요약 파일 생성
        summary_file = data_dir / f"supplier_{business_number.replace('-', '')}_summary.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"공급업체 등록 요약\n")
            f.write(f"="*50 + "\n")
            f.write(f"등록일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"업체명: {name}\n")
            f.write(f"사업자번호: {business_number}\n")
            f.write(f"대표자: {representative}\n")
            f.write(f"연락처: {contact}\n")
            f.write(f"주소: {address}\n")
            f.write(f"취급품목: {', '.join(items)}\n")
        
        return supplier_info
    else:
        print("\n등록이 취소되었습니다.")
        return None

if __name__ == "__main__":
    supplier = register_supplier_interactive()
    
    if supplier:
        print("\n다음 작업을 선택하세요:")
        print("1. 추가 공급업체 등록")
        print("2. 등록된 공급업체 목록 보기")
        print("3. 종료")
        
        choice = input("\n선택: ").strip()
        
        if choice == "1":
            register_supplier_interactive()
        elif choice == "2":
            suppliers_file = Path("data/suppliers.json")
            if suppliers_file.exists():
                with open(suppliers_file, 'r', encoding='utf-8') as f:
                    suppliers = json.load(f)
                print(f"\n총 {len(suppliers)}개 공급업체 등록됨:")
                for biz_num, info in suppliers.items():
                    print(f"  - {info['name']} ({biz_num})")
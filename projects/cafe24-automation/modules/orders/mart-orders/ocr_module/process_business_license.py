#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import traceback
from datetime import datetime
from image_processor import SupplierRegistrationSystem, BusinessLicenseProcessor
from pathlib import Path
import json
import logging
import os
import sys

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
사업자등록증 이미지 처리 및 공급업체 등록 시스템
MART 공급망 관리 자동화
"""

# src 디렉토리를 path에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def display_welcome():
    """환영 메시지 표시"""
    print("=" * 70)
    print(" " * 20 + "MART 공급업체 관리 시스템")
    print(" " * 15 + "사업자등록증 OCR 자동 처리")
    print("=" * 70)
    print("\n담당자 정보:")
    print("  배송지: 경기 시흥시 장현능곡로 155 시흥 플랑드르 지하 1층 웰빙 푸드마켓")
    print("  담당자: 윤철 대리")
    print("  연락처: 010-7727-8009")
    print("-" * 70)

def get_image_path():
    """이미지 파일 경로 입력받기"""
    print("\n사업자등록증 이미지 파일 처리")
    print("1. 파일 경로를 직접 입력")
    print("2. 드래그 앤 드롭 (파일을 여기로 끌어다 놓으세요)")
    
    image_path = input("\n이미지 파일 경로: ").strip()
    
    # 따옴표 제거 (드래그 앤 드롭 시 자동으로 따옴표가 추가되는 경우)
    if image_path.startswith('"') and image_path.endswith('"'):
        image_path = image_path[1:-1]
    if image_path.startswith("'") and image_path.endswith("'"):
        image_path = image_path[1:-1]
    
    # 경로 정규화
    image_path = os.path.normpath(image_path)
    
    # 파일 존재 확인
    if not os.path.exists(image_path):
        print(f"오류: 파일을 찾을 수 없습니다 - {image_path}")
        return None
    
    # 이미지 파일 확인
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif'}
    if Path(image_path).suffix.lower() not in valid_extensions:
        print(f"오류: 지원하지 않는 파일 형식입니다. 지원 형식: {', '.join(valid_extensions)}")
        return None
    
    return image_path

def process_single_image():
    """단일 이미지 처리"""
    system = SupplierRegistrationSystem()
    
    # 기본 배송 담당자 정보
    delivery_info = {
        "address": "경기 시흥시 장현능곡로 155 시흥 플랑드르 지하 1층 웰빙 푸드마켓",
        "contact_person": {
            "name": "윤철",
            "position": "대리",
            "phone": "010-7727-8009"
        }
    }
    
    # 이미지 경로 입력
    image_path = get_image_path()
    if not image_path:
        return
    
    # 공급업체 등록
    result = system.register_with_image(image_path, delivery_info)
    
    if result.get("status") != "failed":
        print("\n공급업체 정보가 성공적으로 등록되었습니다!")
        
        # 등록 정보를 별도 파일로 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"data/registration_report_{timestamp}.json"
        
        os.makedirs("data", exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"상세 보고서 저장: {report_file}")

def view_suppliers():
    """등록된 공급업체 목록 보기"""
    system = SupplierRegistrationSystem()
    
    if not system.suppliers:
        print("\n등록된 공급업체가 없습니다.")
        return
    
    print("\n" + "=" * 70)
    print("등록된 공급업체 목록")
    print("=" * 70)
    
    for idx, (business_number, supplier) in enumerate(system.suppliers.items(), 1):
        print(f"\n[{idx}] {supplier['company_name']}")
        print(f"    사업자번호: {business_number}")
        print(f"    대표자: {supplier['representative']}")
        print(f"    주소: {supplier['business_address']}")
        if supplier.get('items'):
            print(f"    취급품목: {', '.join(supplier['items'])}")
        print(f"    등록일: {supplier['registered_date'][:10]}")
        print(f"    상태: {supplier['status']}")

def export_supplier_data():
    """공급업체 데이터 내보내기"""
    system = SupplierRegistrationSystem()
    
    if not system.suppliers:
        print("\n등록된 공급업체가 없습니다.")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_file = f"data/suppliers_export_{timestamp}.json"
    
    # Excel 형식으로도 저장 가능
    try:
        
        # DataFrame 생성
        suppliers_list = []
        for business_number, supplier in system.suppliers.items():
            flat_supplier = {
                "사업자번호": business_number,
                "업체명": supplier['company_name'],
                "대표자": supplier['representative'],
                "주소": supplier['business_address'],
                "업태": supplier.get('business_type', ''),
                "종목": supplier.get('business_item', ''),
                "취급품목": ', '.join(supplier.get('items', [])),
                "담당자이메일": supplier.get('contact_email', ''),
                "등록일": supplier['registered_date'][:10],
                "상태": supplier['status']
            }
            suppliers_list.append(flat_supplier)
        
        df = pd.DataFrame(suppliers_list)
        excel_file = f"data/suppliers_export_{timestamp}.xlsx"
        df.to_excel(excel_file, index=False)
        print(f"\n데이터가 Excel 파일로 저장되었습니다: {excel_file}")
    except ImportError:
        print("\nExcel 내보내기를 위해 pandas가 필요합니다.")
    
    # JSON으로도 저장
    with open(export_file, 'w', encoding='utf-8') as f:
        json.dump(system.suppliers, f, ensure_ascii=False, indent=2)
    print(f"데이터가 JSON 파일로 저장되었습니다: {export_file}")

def main():
    """메인 실행 함수"""
    display_welcome()
    
    while True:
        print("\n" + "=" * 70)
        print("메뉴 선택")
        print("-" * 70)
        print("1. 사업자등록증 이미지 처리 및 공급업체 등록")
        print("2. 등록된 공급업체 목록 보기")
        print("3. 공급업체 데이터 내보내기")
        print("4. 종료")
        print("-" * 70)
        
        choice = input("\n선택 (1-4): ").strip()
        
        if choice == '1':
            process_single_image()
        elif choice == '2':
            view_suppliers()
        elif choice == '3':
            export_supplier_data()
        elif choice == '4':
            print("\n프로그램을 종료합니다.")
            break
        else:
            print("\n잘못된 선택입니다. 다시 시도해주세요.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n프로그램이 사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n오류 발생: {str(e)}")
        traceback.print_exc()
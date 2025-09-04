"""
사업자등록증 이미지 처리 및 OCR 모듈
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Tuple, List
import logging
import sys
import os

# OCR 라이브러리
try:
    from PIL import Image
    import pytesseract
    import cv2
    import numpy as np
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("OCR 라이브러리가 설치되지 않았습니다. 기본 모드로 실행됩니다.")

logger = logging.getLogger(__name__)


class BusinessLicenseProcessor:
    """사업자등록증 처리 클래스"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # 이미지 저장 디렉토리
        self.images_dir = self.data_dir / "business_licenses"
        self.images_dir.mkdir(exist_ok=True)
        
        # 처리된 데이터 저장
        self.processed_dir = self.data_dir / "processed_licenses"
        self.processed_dir.mkdir(exist_ok=True)
    
    def preprocess_image(self, image_path: str):
        """
        이미지 전처리 - OCR 정확도 향상
        """
        # 이미지 읽기
        img = cv2.imread(image_path)
        
        # 그레이스케일 변환
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 노이즈 제거
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # 대비 향상
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        # 이진화
        _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return binary
    
    def extract_business_info(self, image_path: str) -> Dict:
        """
        사업자등록증 이미지에서 정보 추출
        """
        print(f"\n이미지 처리 중: {image_path}")
        
        extracted_info = {
            "extraction_date": datetime.now().isoformat(),
            "image_path": image_path,
            "ocr_status": "pending",
            "raw_text": "",
            "business_info": {}
        }
        
        if not OCR_AVAILABLE:
            extracted_info["ocr_status"] = "ocr_not_available"
            extracted_info["message"] = "OCR 라이브러리가 설치되지 않았습니다"
            return extracted_info
        
        try:
            # 이미지 전처리
            preprocessed = self.preprocess_image(image_path)
            
            # Tesseract 설정 (한국어)
            custom_config = r'--oem 3 --psm 6 -l kor+eng'
            
            # OCR 실행
            text = pytesseract.image_to_string(preprocessed, config=custom_config)
            
            extracted_info["raw_text"] = text
            extracted_info["ocr_status"] = "success"
            
            # 정보 추출
            business_info = self.parse_all_info(text)
            extracted_info["business_info"] = business_info
            
            print(f"✅ OCR 처리 완료")
            
        except Exception as e:
            extracted_info["ocr_status"] = "failed"
            extracted_info["error"] = str(e)
            print(f"❌ OCR 처리 실패: {str(e)}")
        
        return extracted_info
    
    def parse_business_number(self, text: str) -> Optional[str]:
        """사업자등록번호 추출"""
        # 여러 패턴 시도
        patterns = [
            r'\d{3}-\d{2}-\d{5}',  # XXX-XX-XXXXX
            r'\d{10}',  # XXXXXXXXXX (하이픈 없는 경우)
            r'등록번호[\s:]*([^\d]*)([\d-]+)',  # "등록번호" 키워드 포함
            r'사업자[\s]*등록[\s]*번호[\s:]*([^\d]*)([\d-]+)'  # 전체 키워드
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                # 튜플인 경우 마지막 요소 사용
                if isinstance(matches[0], tuple):
                    number = matches[0][-1]
                else:
                    number = matches[0]
                # 하이픈 정규화
                number = re.sub(r'[^\d]', '', number)
                if len(number) == 10:
                    return f"{number[:3]}-{number[3:5]}-{number[5:]}"
        return None
    
    def parse_company_name(self, text: str) -> Optional[str]:
        """상호명 추출"""
        patterns = [
            r'상[\s]*호[\s:]+([^\n]+)',
            r'법인명[\s:]+([^\n]+)',
            r'회사명[\s:]+([^\n]+)',
            r'업체명[\s:]+([^\n]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.MULTILINE)
            if match:
                name = match.group(1).strip()
                # 불필요한 문자 제거
                name = re.sub(r'[\(\)]', '', name).strip()
                if name and len(name) < 50:  # 너무 긴 텍스트 제외
                    return name
        return None
    
    def parse_representative(self, text: str) -> Optional[str]:
        """대표자명 추출"""
        patterns = [
            r'대[\s]*표[\s]*자?[\s:]+([가-힣]{2,4})',
            r'성[\s]*명[\s:]+([가-힣]{2,4})',
            r'대표[\s:]+([가-힣]{2,4})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                name = match.group(1).strip()
                if 2 <= len(name) <= 4:  # 한국 이름 길이 체크
                    return name
        return None
    
    def parse_address(self, text: str) -> Optional[str]:
        """주소 추출"""
        patterns = [
            r'(?:사업장[\s]*)?(?:주소|소재지)[\s:]+([^\n]+)',
            r'(?:서울|부산|대구|인천|광주|대전|울산|세종|경기|강원|충북|충남|전북|전남|경북|경남|제주)[^\n]+',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.MULTILINE)
            if matches:
                # 가장 긴 주소 선택 (보통 더 완전한 주소)
                address = max(matches, key=len) if isinstance(matches[0], str) else matches[0]
                address = address.strip()
                # 불필요한 문자 제거
                address = re.sub(r'[\(\)\[\]]', '', address).strip()
                if address and len(address) > 10:  # 최소 길이 체크
                    return address
        return None
    
    def parse_business_type(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """업태 및 종목 추출"""
        # 업태
        business_pattern = r'업[\s]*태[\s:]+([^\n종]+)'
        business_match = re.search(business_pattern, text)
        business_type = business_match.group(1).strip() if business_match else None
        
        # 종목
        item_pattern = r'종[\s]*목[\s:]+([^\n]+)'
        item_match = re.search(item_pattern, text)
        business_item = item_match.group(1).strip() if item_match else None
        
        return business_type, business_item
    
    def parse_all_info(self, text: str) -> Dict:
        """모든 정보 추출"""
        business_type, business_item = self.parse_business_type(text)
        
        return {
            "business_number": self.parse_business_number(text),
            "company_name": self.parse_company_name(text),
            "representative": self.parse_representative(text),
            "address": self.parse_address(text),
            "business_type": business_type,
            "business_item": business_item
        }
    
    def save_extracted_data(self, data: Dict, business_number: str):
        """추출된 데이터 저장"""
        filename = self.processed_dir / f"license_{business_number.replace('-', '')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return filename
    
    def validate_extracted_info(self, info: Dict) -> Dict:
        """추출된 정보 검증"""
        validation_result = {
            "is_valid": True,
            "missing_fields": [],
            "confidence_scores": {}
        }
        
        required_fields = ["business_number", "company_name", "representative", "address"]
        
        for field in required_fields:
            if not info.get(field):
                validation_result["missing_fields"].append(field)
                validation_result["is_valid"] = False
            else:
                # 간단한 신뢰도 점수 (실제 값이 있으면 높은 점수)
                validation_result["confidence_scores"][field] = 0.9 if info[field] else 0.0
        
        return validation_result
    
    def process_image(self, image_path: str) -> Tuple[bool, Dict]:
        """
        이미지 처리 메인 함수
        Returns: (성공여부, 추출된 데이터)
        """
        try:
            # 파일 존재 확인
            if not Path(image_path).exists():
                return False, {"error": f"이미지 파일을 찾을 수 없습니다: {image_path}"}
            
            # OCR 수행
            extracted = self.extract_business_info(image_path)
            
            if extracted['ocr_status'] == 'success':
                # 추출된 정보 검증
                validation = self.validate_extracted_info(extracted['business_info'])
                extracted['validation'] = validation
                
                # 전체 신뢰도 계산
                if validation['confidence_scores']:
                    avg_confidence = sum(validation['confidence_scores'].values()) / len(validation['confidence_scores'])
                    extracted['confidence'] = avg_confidence
                else:
                    extracted['confidence'] = 0.0
            
            logger.info(f"이미지 처리 완료: {image_path}")
            return extracted['ocr_status'] == 'success', extracted
            
        except Exception as e:
            logger.error(f"이미지 처리 실패: {str(e)}")
            return False, {"error": str(e), "ocr_status": "failed"}


class SupplierRegistrationSystem:
    """통합 공급업체 등록 시스템"""
    
    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
        self.suppliers_file = self.data_dir / "suppliers.json"
        self.contacts_file = self.data_dir / "delivery_contacts.json"
        
        self.image_processor = BusinessLicenseProcessor()
        
        # 기존 데이터 로드
        self.suppliers = self.load_suppliers()
        self.contacts = self.load_contacts()
    
    def load_suppliers(self) -> Dict:
        """공급업체 데이터 로드"""
        if self.suppliers_file.exists():
            with open(self.suppliers_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def load_contacts(self) -> Dict:
        """담당자 정보 로드"""
        if self.contacts_file.exists():
            with open(self.contacts_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_data(self):
        """데이터 저장"""
        with open(self.suppliers_file, 'w', encoding='utf-8') as f:
            json.dump(self.suppliers, f, ensure_ascii=False, indent=2)
        
        with open(self.contacts_file, 'w', encoding='utf-8') as f:
            json.dump(self.contacts, f, ensure_ascii=False, indent=2)
    
    def register_with_image(self, image_path: str, additional_info: Dict) -> Dict:
        """
        이미지와 추가 정보로 공급업체 등록
        
        Args:
            image_path: 사업자등록증 이미지 경로
            additional_info: 담당자 정보 등 추가 정보
        """
        print("\n=== 사업자등록증 기반 공급업체 등록 ===")
        print("\n1. 이미지 분석 중...")
        
        # 이미지 처리
        success, extracted_data = self.image_processor.process_image(image_path)
        
        if not success:
            print(f"\n❌ 이미지 처리 실패: {extracted_data.get('error', '알 수 없는 오류')}")
            manual_input = input("\n수동으로 입력하시겠습니까? (y/n): ").strip().lower()
            if manual_input != 'y':
                return {"status": "failed", "error": extracted_data.get("error")}
            extracted_info = {}
        else:
            extracted_info = extracted_data.get('business_info', {})
            
            # OCR 결과 표시
            print("\n2. OCR 추출 결과:")
            print("-" * 50)
            for key, value in extracted_info.items():
                if value:
                    display_key = {
                        "business_number": "사업자등록번호",
                        "company_name": "상호명",
                        "representative": "대표자명",
                        "address": "사업장 주소",
                        "business_type": "업태",
                        "business_item": "종목"
                    }.get(key, key)
                    print(f"  {display_key}: {value}")
            
            # 검증 결과 표시
            validation = extracted_data.get('validation', {})
            if validation.get('missing_fields'):
                print(f"\n⚠️  누락된 필드: {', '.join(validation['missing_fields'])}")
            
            confidence = extracted_data.get('confidence', 0)
            print(f"\n신뢰도: {confidence:.1%}")
        
        # 수동 입력/확인
        print("\n3. 정보 확인 및 수정")
        print("   (OCR 결과가 있는 경우 Enter를 누르면 그대로 사용합니다)")
        print("-" * 50)
        
        # 각 필드 확인/입력
        business_number = input(f"사업자등록번호 [{extracted_info.get('business_number', '')}]: ").strip()
        if not business_number and extracted_info.get('business_number'):
            business_number = extracted_info['business_number']
        
        company_name = input(f"상호명 [{extracted_info.get('company_name', '')}]: ").strip()
        if not company_name and extracted_info.get('company_name'):
            company_name = extracted_info['company_name']
        
        representative = input(f"대표자명 [{extracted_info.get('representative', '')}]: ").strip()
        if not representative and extracted_info.get('representative'):
            representative = extracted_info['representative']
        
        business_address = input(f"사업장 주소 [{extracted_info.get('address', '')}]: ").strip()
        if not business_address and extracted_info.get('address'):
            business_address = extracted_info['address']
        
        # 업태/종목
        business_type = input(f"업태 [{extracted_info.get('business_type', '')}]: ").strip()
        if not business_type and extracted_info.get('business_type'):
            business_type = extracted_info['business_type']
        
        business_item = input(f"종목 [{extracted_info.get('business_item', '')}]: ").strip()
        if not business_item and extracted_info.get('business_item'):
            business_item = extracted_info['business_item']
        
        # 추가 정보 입력
        print("\n4. 추가 정보 입력")
        items_input = input("취급 품목 (쉼표로 구분): ").strip()
        items = [item.strip() for item in items_input.split(',')] if items_input else []
        
        contact_email = input("담당자 이메일: ").strip()
        notes = input("비고: ").strip()
        
        # 공급업체 정보 구성
        supplier_info = {
            "business_number": business_number,
            "company_name": company_name,
            "representative": representative,
            "business_address": business_address,
            "business_type": business_type,
            "business_item": business_item,
            "items": items,
            "contact_email": contact_email,
            "notes": notes,
            "delivery_info": additional_info,
            "registered_date": datetime.now().isoformat(),
            "status": "active",
            "image_processed": success,
            "image_path": image_path,
            "ocr_data": extracted_data if success else None
        }
        
        # 저장
        self.suppliers[business_number] = supplier_info
        self.save_data()
        
        # 결과 출력
        print("\n" + "=" * 60)
        print("✅ 공급업체 등록 완료!")
        print("=" * 60)
        print(f"\n[등록 정보]")
        print(f"  업체명: {company_name}")
        print(f"  사업자번호: {business_number}")
        print(f"  대표자: {representative}")
        print(f"  주소: {business_address}")
        if business_type:
            print(f"  업태: {business_type}")
        if business_item:
            print(f"  종목: {business_item}")
        if items:
            print(f"  취급품목: {', '.join(items)}")
        
        print(f"\n[배송 정보]")
        print(f"  배송지: {additional_info.get('address')}")
        contact = additional_info.get('contact_person', {})
        print(f"  담당자: {contact.get('name')} {contact.get('position')}")
        print(f"  연락처: {contact.get('phone')}")
        
        return supplier_info
    
    def get_supplier_summary(self, business_number: str) -> Optional[Dict]:
        """공급업체 요약 정보 조회"""
        supplier = self.suppliers.get(business_number)
        if not supplier:
            return None
        
        return {
            "company_name": supplier.get("company_name"),
            "business_number": business_number,
            "representative": supplier.get("representative"),
            "items": supplier.get("items", []),
            "delivery_contact": supplier.get("delivery_info", {}).get("contact_person"),
            "status": supplier.get("status")
        }


# 실행용 헬퍼 함수
def register_supplier_with_manager_info():
    """담당자 정보와 함께 공급업체 등록"""
    
    system = SupplierRegistrationSystem()
    
    # 이미 저장된 담당자 정보 사용
    delivery_info = {
        "address": "경기 시흥시 장현능곡로 155 시흥 플랑드르 지하 1층 웰빙 푸드마켓",
        "contact_person": {
            "name": "윤철",
            "position": "대리",
            "phone": "010-7727-8009"
        }
    }
    
    print("\n담당자 정보:")
    print(f"  배송지: {delivery_info['address']}")
    print(f"  담당자: {delivery_info['contact_person']['name']} {delivery_info['contact_person']['position']}")
    print(f"  연락처: {delivery_info['contact_person']['phone']}")
    
    print("\n사업자등록증 이미지를 준비해주세요.")
    print("이미지 파일 경로를 입력하거나, 직접 정보를 입력할 수 있습니다.")
    
    return system, delivery_info


if __name__ == "__main__":
    system, delivery_info = register_supplier_with_manager_info()
    
    # 테스트용 - 실제로는 이미지 경로를 받음
    choice = input("\n1. 이미지로 등록\n2. 직접 입력\n선택: ").strip()
    
    if choice == "1":
        image_path = input("이미지 경로: ").strip()
        result = system.register_with_image(image_path, delivery_info)
    else:
        # 직접 입력 모드
        print("\n수동으로 정보를 입력합니다.")
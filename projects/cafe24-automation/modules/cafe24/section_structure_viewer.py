"""
카페24 섹션 구조 뷰어
학습된 데이터를 기반으로 섹션 구조 시각화
"""

import json
from pathlib import Path
from datetime import datetime

def display_section_structure():
    """섹션 구조 표시"""
    
    print("\n" + "="*80)
    print("카페24 상품 등록 페이지 - 전체 섹션 구조")
    print("="*80)
    
    sections = {
        "1. 표시설정": {
            "설명": "상품의 진열 및 판매 상태 설정",
            "하위항목": [
                "• 진열상태 (진열함/진열안함)",
                "• 판매상태 (판매함/판매안함)",
                "• 멀티쇼핑몰별 개별 설정",
                "• 진열 우선순위",
                "• 메인 진열 설정"
            ]
        },
        "2. 기본정보": {
            "설명": "상품의 기본 정보 입력",
            "하위항목": [
                "• 상품명 (한글/영문)",
                "• 상품코드 / 자체상품코드",
                "• 모델명",
                "• 상품 요약설명",
                "• 상품 간략설명",
                "• 상품 상세설명 (PC/모바일)",
                "• 제조사 / 브랜드",
                "• 트렌드 / 제조일자"
            ]
        },
        "3. 판매정보": {
            "설명": "가격 및 판매 조건 설정",
            "하위항목": [
                "• 상품가 / 판매가",
                "• 소비자가 / 공급가",
                "• 과세구분 (과세/면세/영세)",
                "• 상품할인 설정",
                "• 할인기간 설정",
                "• 적립금 설정",
                "• 최소/최대 구매수량"
            ]
        },
        "4. 옵션/재고": {
            "설명": "상품 옵션 및 재고 관리",
            "하위항목": [
                "• 옵션 사용 여부",
                "• 옵션 구성 방식 (조합형/독립형)",
                "• 옵션명 / 옵션값",
                "• 옵션별 추가금액",
                "• 재고수량 관리",
                "• 품절시 표시 설정"
            ]
        },
        "5. 이미지정보": {
            "설명": "상품 이미지 등록",
            "하위항목": [
                "• 대표이미지 (목록/상세)",
                "• 추가이미지 (최대 20개)",
                "• 상세이미지",
                "• 이미지 확대 기능",
                "• URL 직접 입력"
            ]
        },
        "6. 제작정보": {
            "설명": "제품 제작 관련 정보",
            "하위항목": [
                "• 제품 소재",
                "• 색상 / 치수",
                "• 제작자 / 수입자",
                "• 제작국",
                "• 세탁방법 및 취급시 주의사항",
                "• KC 인증 정보"
            ]
        },
        "7. 상세이용안내": {
            "설명": "구매 관련 상세 안내",
            "하위항목": [
                "• 상품 결제 정보",
                "• 상품 배송 정보",
                "• 교환/반품 정보",
                "• 서비스 문의"
            ]
        },
        "8. 아이콘설정": {
            "설명": "상품 아이콘 표시",
            "하위항목": [
                "• 아이콘 사용 여부",
                "• 아이콘 선택",
                "• 표시 기간 설정",
                "• 아이콘 위치"
            ]
        },
        "9. 배송정보": {
            "설명": "배송 관련 설정",
            "하위항목": [
                "• 국내/해외 배송 설정",
                "• 배송방법 선택",
                "• 배송비 설정",
                "• 배송지역 제한",
                "• 배송 안내 문구"
            ]
        },
        "10. 추가구성상품": {
            "설명": "함께 판매할 추가 상품",
            "하위항목": [
                "• 추가구성상품 사용 여부",
                "• 상품 선택",
                "• 추가 금액 설정"
            ]
        },
        "11. 관련상품": {
            "설명": "연관 상품 설정",
            "하위항목": [
                "• 관련상품 사용 여부",
                "• 자동/수동 선택",
                "• 관련상품 개수"
            ]
        },
        "12. SEO설정": {
            "설명": "검색엔진 최적화",
            "하위항목": [
                "• 메타 태그",
                "• 검색 키워드",
                "• 대체 텍스트",
                "• Open Graph 설정"
            ]
        },
        "13. 메모": {
            "설명": "관리자용 메모",
            "하위항목": [
                "• 메모 내용",
                "• 공개 여부 설정"
            ]
        }
    }
    
    for section_name, section_info in sections.items():
        print(f"\n{section_name}")
        print(f"  설명: {section_info['설명']}")
        print(f"  하위 항목:")
        for item in section_info['하위항목']:
            print(f"    {item}")
    
    print("\n" + "="*80)
    print("각 섹션을 클릭하면 해당 섹션의 모든 입력 필드가 표시됩니다.")
    print("모든 체크박스, 드롭다운, 텍스트 입력란이 학습 대상입니다.")
    print("="*80)

def analyze_learning_file(filename=None):
    """학습 파일 분석"""
    
    learning_dir = Path("C:/Users/8899y/CUA-MASTER/modules/cafe24/learning")
    
    if not filename:
        # 최신 파일 찾기
        json_files = list(learning_dir.glob("*.json"))
        if not json_files:
            print("학습 파일이 없습니다.")
            return
        
        filename = max(json_files, key=lambda x: x.stat().st_mtime)
    
    print(f"\n학습 파일 분석: {filename.name}")
    print("-" * 60)
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if 'sections' in data:
        for section_name, section_data in data['sections'].items():
            print(f"\n[{section_name}]")
            
            # 요소 개수
            inputs = len(section_data.get('all_inputs', []))
            selects = len(section_data.get('all_selects', []))
            checkboxes = len(section_data.get('all_checkboxes', []))
            radios = len(section_data.get('all_radios', []))
            textareas = len(section_data.get('all_textareas', []))
            
            total = inputs + selects + checkboxes + radios + textareas
            
            if total > 0:
                print(f"  총 {total}개 요소")
                if inputs: print(f"    - Input: {inputs}개")
                if selects: print(f"    - Select: {selects}개")
                if checkboxes: print(f"    - Checkbox: {checkboxes}개")
                if radios: print(f"    - Radio: {radios}개")
                if textareas: print(f"    - Textarea: {textareas}개")
            
            # 하위 섹션
            subsections = section_data.get('subsections', {})
            if subsections:
                print(f"  하위 섹션: {len(subsections)}개")
                for sub_name in subsections.keys():
                    print(f"    • {sub_name}")
    
    # 통계
    if 'statistics' in data:
        stats = data['statistics']
        print(f"\n" + "="*60)
        print("전체 통계:")
        print(f"  총 요소: {stats.get('total_elements', 0)}개")
        print(f"  총 섹션: {stats.get('total_sections', 0)}개")
        print(f"  총 하위섹션: {stats.get('total_subsections', 0)}개")

if __name__ == "__main__":
    print("""
    카페24 섹션 구조 뷰어
    ===================
    
    1. 전체 섹션 구조 보기
    2. 학습 데이터 분석
    """)
    
    # 섹션 구조 표시
    display_section_structure()
    
    # 학습 데이터 분석
    print("\n" + "="*80)
    print("학습 데이터 분석")
    print("="*80)
    analyze_learning_file()
    
    print("\n✅ 분석 완료")
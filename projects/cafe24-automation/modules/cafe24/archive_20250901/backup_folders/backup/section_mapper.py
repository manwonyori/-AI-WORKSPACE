# -*- coding: utf-8 -*-
"""
Section Mapper - Cafe24 상품 수정 13개 섹션 완전 매핑
각 섹션의 위치, 요소, 수정 방법을 체계적으로 분석
"""
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

class SectionMapper:
    """13개 섹션 완전 매핑 시스템"""
    
    def __init__(self):
        """초기화"""
        self.driver = None
        self.sections_data = {}
        print("[SECTION-MAPPER] 13개 섹션 완전 매핑 시스템 시작")
    
    def setup_driver(self):
        """드라이버 설정"""
        options = Options()
        options.add_argument('--window-size=1920,1080')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return True
    
    def access_product_page(self, product_no=339):
        """상품 수정 페이지 접근"""
        print(f"[ACCESS] 상품 {product_no}번 페이지 접근...")
        
        # 검증된 직접 접근 방식
        product_url = f"https://manwonyori.cafe24.com/disp/admin/shop1/product/ProductRegister?product_no={product_no}"
        self.driver.get(product_url)
        
        # 알림 처리
        for i in range(3):
            try:
                alert = WebDriverWait(self.driver, 3).until(EC.alert_is_present())
                print(f"[ALERT-{i+1}] 알림 처리")
                alert.accept()
                time.sleep(1)
            except:
                break
        
        # 페이지 로딩 대기
        WebDriverWait(self.driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        print("[OK] 페이지 로드 완료")
        return True
    
    def map_section_by_scroll(self, section_name, target_keywords):
        """스크롤하며 특정 섹션 찾기 및 매핑"""
        print(f"[MAP-SECTION] {section_name} 섹션 매핑...")
        
        section_data = {
            "name": section_name,
            "found": False,
            "scroll_position": 0,
            "elements": [],
            "inputs": 0,
            "selects": 0,
            "textareas": 0,
            "buttons": 0,
            "checkboxes": 0,
            "radio_buttons": 0
        }
        
        # 페이지 전체 높이 확인
        total_height = self.driver.execute_script("return document.body.scrollHeight")
        current_position = 0
        scroll_step = 300
        
        while current_position < total_height:
            # 스크롤
            self.driver.execute_script(f"window.scrollTo(0, {current_position});")
            time.sleep(0.5)
            
            # 현재 화면에서 섹션 키워드 찾기
            page_text = self.driver.execute_script("return document.body.innerText;").lower()
            
            section_found = any(keyword.lower() in page_text for keyword in target_keywords)
            
            if section_found:
                print(f"   [FOUND] {section_name} 섹션 발견! (스크롤 위치: {current_position})")
                section_data["found"] = True
                section_data["scroll_position"] = current_position
                
                # 현재 화면의 모든 요소 분석
                section_elements = self.analyze_current_view_elements()
                section_data.update(section_elements)
                break
            
            current_position += scroll_step
        
        if not section_data["found"]:
            print(f"   [NOT-FOUND] {section_name} 섹션을 찾을 수 없습니다")
        
        return section_data
    
    def analyze_current_view_elements(self):
        """현재 화면의 모든 요소 분석"""
        # 화면에 보이는 요소들만 분석
        elements_info = self.driver.execute_script("""
            var rect = {top: window.pageYOffset, bottom: window.pageYOffset + window.innerHeight};
            var elements = {
                inputs: [],
                selects: [],
                textareas: [],
                buttons: [],
                checkboxes: [],
                radio_buttons: []
            };
            
            // 모든 입력 요소 검사
            document.querySelectorAll('input, select, textarea, button').forEach(function(el) {
                var elRect = el.getBoundingClientRect();
                var elTop = elRect.top + window.pageYOffset;
                
                // 현재 화면에 보이는 요소만 포함
                if (elTop >= rect.top && elTop <= rect.bottom) {
                    var info = {
                        tag: el.tagName.toLowerCase(),
                        type: el.type || '',
                        name: el.name || '',
                        id: el.id || '',
                        className: el.className || '',
                        placeholder: el.placeholder || '',
                        value: el.value || ''
                    };
                    
                    if (el.tagName === 'INPUT') {
                        if (el.type === 'checkbox') {
                            elements.checkboxes.push(info);
                        } else if (el.type === 'radio') {
                            elements.radio_buttons.push(info);
                        } else {
                            elements.inputs.push(info);
                        }
                    } else if (el.tagName === 'SELECT') {
                        elements.selects.push(info);
                    } else if (el.tagName === 'TEXTAREA') {
                        elements.textareas.push(info);
                    } else if (el.tagName === 'BUTTON') {
                        elements.buttons.push(info);
                    }
                }
            });
            
            return {
                elements: elements,
                inputs: elements.inputs.length,
                selects: elements.selects.length,
                textareas: elements.textareas.length,
                buttons: elements.buttons.length,
                checkboxes: elements.checkboxes.length,
                radio_buttons: elements.radio_buttons.length
            };
        """)
        
        return elements_info
    
    def map_all_13_sections(self):
        """13개 섹션 모두 매핑"""
        print("\n[MAP-ALL] 13개 섹션 전체 매핑 시작...")
        
        # 13개 섹션과 각각의 키워드 정의
        sections_config = {
            "표시설정": ["표시설정", "진열상태", "판매상태", "성인인증"],
            "기본정보": ["기본정보", "상품명", "브랜드", "모델명", "제조사"],
            "판매정보": ["판매정보", "판매가", "할인", "적립금", "소비자가"],
            "옵션재고": ["옵션", "재고", "옵션관리", "재고관리", "옵션설정"],
            "이미지정보": ["이미지정보", "상품이미지", "이미지업로드", "대표이미지"],
            "제작정보": ["제작정보", "원산지", "제조일자", "유효기간"],
            "상세이용안내": ["상세이용안내", "상품상세", "상세설명", "상품설명"],
            "아이콘설정": ["아이콘설정", "상품아이콘", "아이콘선택"],
            "배송정보": ["배송정보", "배송비", "배송방법", "배송조건"],
            "추가구성상품": ["추가구성상품", "구성상품", "세트상품"],
            "관련상품": ["관련상품", "연관상품", "추천상품"],
            "SEO설정": ["SEO", "검색최적화", "메타태그", "검색키워드"],
            "메모": ["메모", "관리자메모", "상품메모"]
        }
        
        # 각 섹션별 매핑 실행
        for section_name, keywords in sections_config.items():
            section_data = self.map_section_by_scroll(section_name, keywords)
            self.sections_data[section_name] = section_data
            
            # 각 섹션 매핑 후 잠시 대기
            time.sleep(1)
        
        # 결과 저장
        self.save_mapping_results()
        self.print_mapping_summary()
    
    def save_mapping_results(self):
        """매핑 결과 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cafe24_13sections_mapping_{timestamp}.json"
        
        # 전체 요약 정보 추가
        summary = {
            "mapping_time": datetime.now().isoformat(),
            "total_sections": 13,
            "found_sections": len([s for s in self.sections_data.values() if s["found"]]),
            "sections": self.sections_data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"[SAVE] 매핑 결과 저장: {filename}")
    
    def print_mapping_summary(self):
        """매핑 요약 출력"""
        print("\n" + "="*80)
        print("[MAPPING-SUMMARY] 13개 섹션 매핑 결과")
        print("="*80)
        
        found_count = 0
        total_elements = 0
        
        for section_name, data in self.sections_data.items():
            if data["found"]:
                found_count += 1
                section_elements = data["inputs"] + data["selects"] + data["textareas"] + data["buttons"] + data["checkboxes"] + data["radio_buttons"]
                total_elements += section_elements
                
                print(f"✅ {section_name}: {section_elements}개 요소 (스크롤: {data['scroll_position']})")
                print(f"   입력: {data['inputs']}, 선택: {data['selects']}, 텍스트: {data['textareas']}")
                print(f"   버튼: {data['buttons']}, 체크박스: {data['checkboxes']}, 라디오: {data['radio_buttons']}")
            else:
                print(f"❌ {section_name}: 찾을 수 없음")
        
        print("\n" + "-"*80)
        print(f"📊 발견된 섹션: {found_count}/13개")
        print(f"📊 총 요소 수: {total_elements}개")
        print(f"📊 매핑 완료율: {found_count/13*100:.1f}%")

def main():
    """메인 실행"""
    print("="*80)
    print("CAFE24 13개 섹션 완전 매핑 시스템")
    print("상품 수정의 모든 영역을 체계적으로 분석")
    print("="*80)
    
    mapper = SectionMapper()
    
    try:
        # 1. 드라이버 설정
        mapper.setup_driver()
        
        # 2. 상품 페이지 접근
        if mapper.access_product_page(339):
            # 3. 13개 섹션 모두 매핑
            mapper.map_all_13_sections()
        
    finally:
        if mapper.driver:
            print("[WAIT] 결과 확인을 위해 10초 대기...")
            time.sleep(10)
            mapper.driver.quit()
            print("[CLEANUP] 정리 완료")

if __name__ == "__main__":
    main()
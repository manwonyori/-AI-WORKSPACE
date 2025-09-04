"""
카페24 섹션별 하위 카테고리 심층 학습 시스템
모든 탭과 하위 요소를 완전히 매핑
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import json
import time
from datetime import datetime
from pathlib import Path

class Cafe24DeepSectionLearner:
    """카페24 섹션 심층 학습"""
    
    def __init__(self):
        self.driver = None
        self.learning_dir = Path("C:/Users/8899y/CUA-MASTER/modules/cafe24/learning")
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        
        # 섹션별 상세 구조 정의
        self.section_structure = {
            "표시설정": {
                "subsections": ["진열상태", "판매상태", "진열우선순위"],
                "elements": ["멀티쇼핑몰별 진열", "카테고리별 진열", "메인진열"]
            },
            "기본정보": {
                "subsections": ["상품명", "상품코드", "자체상품코드", "모델명", "상품요약설명", "상품간략설명", "상품상세설명"],
                "elements": ["PC 상품상세설명", "모바일 상품상세설명", "상품분류", "제조사", "브랜드", "트렌드", "제조일자", "출시일자"]
            },
            "판매정보": {
                "subsections": ["상품가", "판매가", "소비자가", "공급가", "과세구분", "과세율"],
                "elements": ["판매가 대체문구", "판매가 대체문구 색상", "소비자가 대체문구", "상품할인", "할인기간", "적립금", "수량"]
            },
            "옵션/재고": {
                "subsections": ["옵션사용", "옵션구성방식", "옵션표시방식", "필수여부"],
                "elements": ["옵션명", "옵션값", "재고수량", "재고관리", "품절표시문구", "재고품절시 주문"]
            },
            "이미지정보": {
                "subsections": ["대표이미지", "추가이미지", "상세이미지"],
                "elements": ["이미지등록", "URL직접입력", "이미지크기", "이미지확대기능"]
            },
            "제작정보": {
                "subsections": ["제작정보사용", "제품소재", "색상", "치수", "제작자/수입자", "제작국", "세탁방법", "품질보증기준"],
                "elements": ["A/S 책임자", "KC인증", "구매안전서비스"]
            },
            "상세이용안내": {
                "subsections": ["상품결제정보", "상품배송정보", "교환/반품정보"],
                "elements": ["서비스문의", "이용안내"]
            },
            "아이콘설정": {
                "subsections": ["아이콘사용", "아이콘기간"],
                "elements": ["아이콘선택", "아이콘위치"]
            },
            "배송정보": {
                "subsections": ["국내배송", "해외배송"],
                "elements": ["배송방법", "배송비", "배송지역", "배송기간", "배송안내문구"]
            },
            "추가구성상품": {
                "subsections": ["추가구성상품사용", "상품선택"],
                "elements": ["추가상품명", "추가상품가격"]
            },
            "관련상품": {
                "subsections": ["관련상품사용", "관련상품선택"],
                "elements": ["자동선택", "수동선택", "관련상품수"]
            },
            "SEO설정": {
                "subsections": ["검색엔진최적화"],
                "elements": ["메타태그", "검색키워드", "상품설명태그", "대체텍스트"]
            },
            "메모": {
                "subsections": ["관리자메모"],
                "elements": ["메모내용", "메모공개여부"]
            }
        }
        
    def setup_driver(self):
        """Chrome 드라이버 설정"""
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        print("[OK] Chrome 드라이버 준비 완료")
        
    def handle_alert(self):
        """알림 처리"""
        try:
            alert = Alert(self.driver)
            alert_text = alert.text
            print(f"[ALERT] {alert_text}")
            alert.accept()
            time.sleep(0.5)
            return True
        except:
            return False
    
    def login_cafe24(self):
        """카페24 로그인"""
        try:
            self.driver.get("https://manwonyori.cafe24.com/admin/")
            time.sleep(2)
            
            # 알림 처리
            self.handle_alert()
            
            # 로그인
            username = self.driver.find_element(By.XPATH, "//input[@type='text']")
            password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            
            username.send_keys("8899yang")
            password.send_keys("xptmxm73xptmxm73!")
            
            login_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), '로그인')]")
            login_btn.click()
            
            time.sleep(3)
            print("[OK] 로그인 성공")
            return True
            
        except Exception as e:
            print(f"[ERROR] 로그인 실패: {e}")
            return False
    
    def navigate_to_product(self, product_no="338"):
        """상품 수정 페이지로 이동"""
        url = f"https://manwonyori.cafe24.com/disp/admin/shop1/product/ProductRegister?product_no={product_no}"
        self.driver.get(url)
        time.sleep(3)
        self.handle_alert()
        print(f"[OK] 상품 {product_no}번 페이지 로드")
    
    def learn_section_deep(self, section_name):
        """섹션 심층 학습"""
        print(f"\n[섹션 학습] {section_name}")
        
        section_data = {
            "name": section_name,
            "timestamp": datetime.now().isoformat(),
            "subsections": {},
            "elements": {},
            "all_inputs": [],
            "all_selects": [],
            "all_checkboxes": [],
            "all_radios": [],
            "all_textareas": []
        }
        
        try:
            # 섹션 탭 클릭
            tab = self.driver.find_element(By.XPATH, f"//a[contains(text(), '{section_name}')]")
            self.driver.execute_script("arguments[0].click();", tab)
            time.sleep(1)
            
            # 섹션 내 모든 요소 수집
            section_data = self.collect_all_elements_in_section(section_data)
            
            # 하위 섹션 구조 분석
            if section_name in self.section_structure:
                structure = self.section_structure[section_name]
                
                # 하위 섹션 찾기
                for subsection in structure.get("subsections", []):
                    subsection_data = self.find_subsection_elements(subsection)
                    if subsection_data:
                        section_data["subsections"][subsection] = subsection_data
                        print(f"   [하위] {subsection}: {len(subsection_data)} 요소")
                
                # 특정 요소 찾기
                for element_name in structure.get("elements", []):
                    element_data = self.find_specific_element(element_name)
                    if element_data:
                        section_data["elements"][element_name] = element_data
                        print(f"   [요소] {element_name}: 찾음")
            
            print(f"   [완료] 총 {self.count_elements(section_data)} 요소 학습")
            
        except Exception as e:
            print(f"   [ERROR] {section_name}: {str(e)[:50]}")
            section_data["error"] = str(e)
        
        return section_data
    
    def collect_all_elements_in_section(self, section_data):
        """섹션 내 모든 요소 수집"""
        
        # Input 요소
        inputs = self.driver.find_elements(By.CSS_SELECTOR, "input:not([type='hidden'])")
        for inp in inputs:
            try:
                element_info = {
                    "type": inp.get_attribute("type"),
                    "name": inp.get_attribute("name"),
                    "id": inp.get_attribute("id"),
                    "value": inp.get_attribute("value"),
                    "placeholder": inp.get_attribute("placeholder"),
                    "class": inp.get_attribute("class")
                }
                
                if inp.get_attribute("type") == "checkbox":
                    element_info["checked"] = inp.is_selected()
                    section_data["all_checkboxes"].append(element_info)
                elif inp.get_attribute("type") == "radio":
                    element_info["checked"] = inp.is_selected()
                    section_data["all_radios"].append(element_info)
                else:
                    section_data["all_inputs"].append(element_info)
            except:
                pass
        
        # Select 요소
        selects = self.driver.find_elements(By.TAG_NAME, "select")
        for sel in selects:
            try:
                options = sel.find_elements(By.TAG_NAME, "option")
                section_data["all_selects"].append({
                    "name": sel.get_attribute("name"),
                    "id": sel.get_attribute("id"),
                    "value": sel.get_attribute("value"),
                    "options": [{"value": opt.get_attribute("value"), 
                                "text": opt.text,
                                "selected": opt.is_selected()} for opt in options],
                    "class": sel.get_attribute("class")
                })
            except:
                pass
        
        # Textarea 요소
        textareas = self.driver.find_elements(By.TAG_NAME, "textarea")
        for txt in textareas:
            try:
                section_data["all_textareas"].append({
                    "name": txt.get_attribute("name"),
                    "id": txt.get_attribute("id"),
                    "value": txt.get_attribute("value"),
                    "rows": txt.get_attribute("rows"),
                    "cols": txt.get_attribute("cols"),
                    "class": txt.get_attribute("class")
                })
            except:
                pass
        
        return section_data
    
    def find_subsection_elements(self, subsection_name):
        """하위 섹션 요소 찾기"""
        elements = []
        
        try:
            # 라벨로 찾기
            labels = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{subsection_name}')]")
            
            for label in labels:
                # 라벨 근처의 입력 요소 찾기
                parent = label.find_element(By.XPATH, "..")
                inputs = parent.find_elements(By.TAG_NAME, "input")
                selects = parent.find_elements(By.TAG_NAME, "select")
                textareas = parent.find_elements(By.TAG_NAME, "textarea")
                
                for elem in inputs + selects + textareas:
                    elements.append({
                        "tag": elem.tag_name,
                        "type": elem.get_attribute("type"),
                        "name": elem.get_attribute("name"),
                        "id": elem.get_attribute("id")
                    })
        except:
            pass
        
        return elements
    
    def find_specific_element(self, element_name):
        """특정 요소 찾기"""
        try:
            # ID로 찾기
            elem = self.driver.find_element(By.XPATH, f"//*[@*[contains(., '{element_name}')]]")
            return {
                "found": True,
                "tag": elem.tag_name,
                "id": elem.get_attribute("id"),
                "name": elem.get_attribute("name"),
                "class": elem.get_attribute("class")
            }
        except:
            return None
    
    def count_elements(self, section_data):
        """요소 개수 계산"""
        total = 0
        total += len(section_data.get("all_inputs", []))
        total += len(section_data.get("all_selects", []))
        total += len(section_data.get("all_checkboxes", []))
        total += len(section_data.get("all_radios", []))
        total += len(section_data.get("all_textareas", []))
        return total
    
    def run_deep_learning(self, product_no="338"):
        """심층 학습 실행"""
        
        print("\n" + "="*60)
        print("카페24 심층 학습 시스템")
        print("모든 섹션 및 하위 카테고리 학습")
        print("="*60)
        
        # 드라이버 설정
        self.setup_driver()
        
        # 로그인
        if not self.login_cafe24():
            return None
        
        # 상품 페이지로 이동
        self.navigate_to_product(product_no)
        
        # 모든 섹션 학습
        all_sections = {}
        section_names = list(self.section_structure.keys())
        
        for section_name in section_names:
            section_data = self.learn_section_deep(section_name)
            all_sections[section_name] = section_data
            time.sleep(1)  # 부하 방지
        
        # 학습 결과 저장
        learning_result = {
            "product_no": product_no,
            "timestamp": datetime.now().isoformat(),
            "sections": all_sections,
            "statistics": self.calculate_statistics(all_sections)
        }
        
        # 파일 저장
        filename = self.save_learning_data(learning_result)
        
        # 요약 출력
        self.print_learning_summary(learning_result)
        
        return learning_result
    
    def calculate_statistics(self, all_sections):
        """통계 계산"""
        stats = {
            "total_sections": len(all_sections),
            "total_subsections": 0,
            "total_inputs": 0,
            "total_selects": 0,
            "total_checkboxes": 0,
            "total_radios": 0,
            "total_textareas": 0,
            "sections_with_errors": 0
        }
        
        for section_name, section_data in all_sections.items():
            if "error" in section_data:
                stats["sections_with_errors"] += 1
            
            stats["total_subsections"] += len(section_data.get("subsections", {}))
            stats["total_inputs"] += len(section_data.get("all_inputs", []))
            stats["total_selects"] += len(section_data.get("all_selects", []))
            stats["total_checkboxes"] += len(section_data.get("all_checkboxes", []))
            stats["total_radios"] += len(section_data.get("all_radios", []))
            stats["total_textareas"] += len(section_data.get("all_textareas", []))
        
        stats["total_elements"] = (
            stats["total_inputs"] + 
            stats["total_selects"] + 
            stats["total_checkboxes"] + 
            stats["total_radios"] + 
            stats["total_textareas"]
        )
        
        return stats
    
    def save_learning_data(self, data):
        """학습 데이터 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.learning_dir / f"deep_learning_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n[저장] {filename}")
        return filename
    
    def print_learning_summary(self, result):
        """학습 요약 출력"""
        print("\n" + "="*60)
        print("심층 학습 완료")
        print("="*60)
        
        stats = result["statistics"]
        print(f"총 섹션: {stats['total_sections']}개")
        print(f"총 하위 섹션: {stats['total_subsections']}개")
        print(f"총 요소: {stats['total_elements']}개")
        print(f"  - Input: {stats['total_inputs']}개")
        print(f"  - Select: {stats['total_selects']}개")
        print(f"  - Checkbox: {stats['total_checkboxes']}개")
        print(f"  - Radio: {stats['total_radios']}개")
        print(f"  - Textarea: {stats['total_textareas']}개")
        
        if stats['sections_with_errors'] > 0:
            print(f"\n주의: {stats['sections_with_errors']}개 섹션에서 오류 발생")
        
        print("\n각 섹션별 요소 수:")
        for section_name, section_data in result["sections"].items():
            element_count = self.count_elements(section_data)
            subsection_count = len(section_data.get("subsections", {}))
            print(f"  {section_name}: {element_count}개 요소, {subsection_count}개 하위섹션")
    
    def cleanup(self):
        """정리"""
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    learner = Cafe24DeepSectionLearner()
    
    try:
        result = learner.run_deep_learning("338")
        
        if result:
            print("\n✅ 심층 학습 성공!")
            print("모든 섹션과 하위 카테고리가 학습되었습니다.")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        
    finally:
        input("\n엔터를 눌러 종료...")
        learner.cleanup()
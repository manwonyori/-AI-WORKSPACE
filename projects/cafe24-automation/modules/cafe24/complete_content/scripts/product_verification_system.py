import requests
import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class VerificationStatus(Enum):
    VERIFIED = "verified"
    UNCERTAIN = "uncertain" 
    NOT_FOUND = "not_found"
    CONFLICTED = "conflicted"

@dataclass
class NutritionFact:
    name: str
    value: str
    unit: str
    daily_value: Optional[str] = None
    source: str = ""
    status: VerificationStatus = VerificationStatus.NOT_FOUND

@dataclass
class ProductData:
    product_name: str
    brand: str
    weight: str
    nutrition_facts: Dict[str, NutritionFact]
    ingredients: List[str]
    allergens: List[str]
    manufacturer: str
    manufacturing_location: str
    verification_sources: List[str]
    confidence_score: float

class ProductVerificationSystem:
    def __init__(self):
        self.verification_sources = [
            "식품의약품안전처",
            "제조사 공식 사이트", 
            "주요 쇼핑몰",
            "영양성분 데이터베이스"
        ]
        self.required_fields = [
            "열량", "나트륨", "탄수화물", "단백질", "지방"
        ]
    
    def verify_product(self, product_id: str, temp_txt_path: str) -> ProductData:
        """개별 제품 검증 실행"""
        print(f"🔍 제품 검증 시작: {product_id}")
        
        # 1단계: 원본 데이터 추출
        original_data = self.extract_original_data(temp_txt_path)
        
        # 2단계: 웹 소스별 데이터 수집
        web_data = self.collect_web_data(original_data['product_name'])
        
        # 3단계: 교차 검증
        verified_data = self.cross_verify(original_data, web_data)
        
        # 4단계: 신뢰도 점수 계산
        confidence_score = self.calculate_confidence(verified_data)
        
        return verified_data
    
    def extract_original_data(self, temp_txt_path: str) -> Dict:
        """temp_txt 파일에서 원본 데이터 추출"""
        try:
            with open(temp_txt_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # HTML에서 제품명 추출
            title_match = re.search(r'<title>(.*?)</title>', content)
            product_name = title_match.group(1) if title_match else "제품명 미확인"
            
            return {
                'product_name': product_name,
                'source': 'temp_txt',
                'content': content
            }
        except Exception as e:
            print(f"❌ 원본 데이터 추출 실패: {e}")
            return {}
    
    def collect_web_data(self, product_name: str) -> Dict:
        """웹에서 제품 데이터 수집"""
        search_results = {}
        
        # 검색 키워드 생성
        search_keywords = self.generate_search_keywords(product_name)
        
        for keyword in search_keywords:
            print(f"🔎 검색 중: {keyword}")
            
            # 실제 웹 검색 (여기서는 시뮬레이션)
            results = self.web_search_simulation(keyword)
            search_results[keyword] = results
        
        return search_results
    
    def generate_search_keywords(self, product_name: str) -> List[str]:
        """검색 키워드 생성"""
        base_keywords = [product_name]
        
        # 브랜드명 추출
        if "취영루" in product_name:
            base_keywords.extend([
                "취영루 영양성분",
                "취영루 원재료",
                "취영루 만두 칼로리"
            ])
        
        if "고기왕만두" in product_name:
            base_keywords.extend([
                "고기왕만두 420g 영양성분",
                "왕만두 칼로리",
                "취영루 고기만두 원재료"
            ])
        
        return base_keywords
    
    def web_search_simulation(self, keyword: str) -> Dict:
        """웹 검색 시뮬레이션 (실제로는 WebSearch 도구 사용)"""
        # 실제 구현에서는 WebSearch나 WebFetch 도구 사용
        return {
            'keyword': keyword,
            'sources_found': [],
            'nutrition_data': {},
            'ingredients_data': [],
            'confidence': 0.0
        }
    
    def cross_verify(self, original: Dict, web_data: Dict) -> ProductData:
        """교차 검증 실행"""
        print("🔄 교차 검증 중...")
        
        # 영양성분 검증
        nutrition_facts = {}
        for field in self.required_fields:
            verified_fact = self.verify_nutrition_field(field, original, web_data)
            nutrition_facts[field] = verified_fact
        
        # 기본 ProductData 생성
        product_data = ProductData(
            product_name=original.get('product_name', ''),
            brand=self.extract_brand(original.get('product_name', '')),
            weight=self.extract_weight(original.get('product_name', '')),
            nutrition_facts=nutrition_facts,
            ingredients=[],
            allergens=[],
            manufacturer="",
            manufacturing_location="",
            verification_sources=[],
            confidence_score=0.0
        )
        
        return product_data
    
    def verify_nutrition_field(self, field_name: str, original: Dict, web_data: Dict) -> NutritionFact:
        """개별 영양성분 필드 검증"""
        
        # 여러 소스에서 데이터 수집
        sources_data = []
        
        # 웹 데이터에서 검색
        for keyword, results in web_data.items():
            if field_name in results.get('nutrition_data', {}):
                sources_data.append({
                    'value': results['nutrition_data'][field_name],
                    'source': f'웹검색: {keyword}',
                    'confidence': results.get('confidence', 0.0)
                })
        
        # 검증 결과 결정
        if not sources_data:
            return NutritionFact(
                name=field_name,
                value="정보 없음",
                unit="",
                status=VerificationStatus.NOT_FOUND,
                source="검증 불가"
            )
        
        # 가장 신뢰도 높은 데이터 선택
        best_source = max(sources_data, key=lambda x: x['confidence'])
        
        return NutritionFact(
            name=field_name,
            value=best_source['value'],
            unit=self.get_nutrition_unit(field_name),
            status=VerificationStatus.VERIFIED if best_source['confidence'] > 0.8 else VerificationStatus.UNCERTAIN,
            source=best_source['source']
        )
    
    def get_nutrition_unit(self, field_name: str) -> str:
        """영양성분별 단위 반환"""
        units = {
            "열량": "kcal",
            "나트륨": "mg",
            "탄수화물": "g", 
            "당류": "g",
            "지방": "g",
            "포화지방": "g",
            "트랜스지방": "g",
            "콜레스테롤": "mg",
            "단백질": "g"
        }
        return units.get(field_name, "")
    
    def extract_brand(self, product_name: str) -> str:
        """제품명에서 브랜드 추출"""
        if "취영루" in product_name:
            return "취영루"
        elif "최씨남매" in product_name:
            return "만원요리 최씨남매"
        return "브랜드 미확인"
    
    def extract_weight(self, product_name: str) -> str:
        """제품명에서 중량 추출"""
        weight_pattern = r'(\d+g|\d+kg)'
        match = re.search(weight_pattern, product_name)
        return match.group(1) if match else "중량 미확인"
    
    def calculate_confidence(self, product_data: ProductData) -> float:
        """전체 신뢰도 점수 계산"""
        total_fields = len(self.required_fields)
        verified_count = sum(1 for field, fact in product_data.nutrition_facts.items() 
                           if fact.status == VerificationStatus.VERIFIED)
        
        return verified_count / total_fields if total_fields > 0 else 0.0
    
    def generate_verification_report(self, product_data: ProductData) -> str:
        """검증 보고서 생성"""
        report = f"""
🔍 제품 검증 보고서
===================
제품명: {product_data.product_name}
브랜드: {product_data.brand}
전체 신뢰도: {product_data.confidence_score:.1%}

📊 영양성분 검증 결과:
"""
        for field_name, fact in product_data.nutrition_facts.items():
            status_emoji = {
                VerificationStatus.VERIFIED: "✅",
                VerificationStatus.UNCERTAIN: "⚠️", 
                VerificationStatus.NOT_FOUND: "❌",
                VerificationStatus.CONFLICTED: "🔄"
            }
            
            report += f"{status_emoji[fact.status]} {field_name}: {fact.value}{fact.unit} ({fact.source})\n"
        
        return report

# 사용 예시
def verify_product_132():
    """132번 제품 검증 예시"""
    verifier = ProductVerificationSystem()
    
    temp_txt_path = "C:/Users/8899y/CUA-MASTER/modules/cafe24/complete_content/html/temp_txt/132.txt"
    
    try:
        verified_data = verifier.verify_product("132", temp_txt_path)
        report = verifier.generate_verification_report(verified_data)
        print(report)
        return verified_data
    except Exception as e:
        print(f"❌ 검증 실패: {e}")
        return None

if __name__ == "__main__":
    verify_product_132()
import os
import re
from typing import Dict, List, Set
from collections import defaultdict, Counter
import json

class BrandAnalysisSystem:
    def __init__(self, temp_txt_directory: str):
        self.temp_txt_dir = temp_txt_directory
        self.products_data = {}
        self.brand_taxonomy = defaultdict(list)
        self.brand_patterns = {
            "취영루": ["취영루", "CYR"],
            "최씨남매": ["최씨남매", "만원요리"],
            "청정원": ["청정원", "CHUNGJUNGONE"], 
            "오뚜기": ["오뚜기", "OTTOGI"],
            "동원": ["동원", "DONGWON"],
            "풀무원": ["풀무원", "PULMUONE"]
        }
        
    def analyze_all_products(self) -> Dict:
        """230개 모든 제품 분석"""
        print("[분석] 230개 제품 브랜드 분석 시작...")
        
        # 1단계: 모든 temp_txt 파일 로드
        all_files = self.load_all_temp_files()
        print(f"[파일] 총 {len(all_files)}개 파일 발견")
        
        # 2단계: 각 파일에서 브랜드 정보 추출
        for file_path in all_files:
            product_id = self.extract_product_id(file_path)
            product_data = self.extract_product_data(file_path)
            self.products_data[product_id] = product_data
        
        # 3단계: 브랜드별 분류
        self.classify_by_brands()
        
        # 4단계: 브랜드 데이터베이스 생성
        brands_database = self.generate_brands_database()
        
        # 5단계: 결과 저장
        self.save_analysis_results(brands_database)
        
        return brands_database
    
    def load_all_temp_files(self) -> List[str]:
        """모든 temp_txt 파일 경로 수집"""
        temp_files = []
        for filename in os.listdir(self.temp_txt_dir):
            if filename.endswith('.txt'):
                file_path = os.path.join(self.temp_txt_dir, filename)
                temp_files.append(file_path)
        return sorted(temp_files)
    
    def extract_product_id(self, file_path: str) -> str:
        """파일 경로에서 제품 ID 추출"""
        filename = os.path.basename(file_path)
        return filename.replace('.txt', '')
    
    def extract_product_data(self, file_path: str) -> Dict:
        """개별 제품 데이터 추출"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # 제품명 추출
            product_name = self.extract_product_name(content)
            
            # 브랜드 식별
            detected_brand = self.detect_brand(product_name, content)
            
            # 제품 카테고리 추정
            category = self.estimate_category(product_name, content)
            
            # 중량/용량 추출
            weight = self.extract_weight(product_name)
            
            return {
                'product_name': product_name,
                'detected_brand': detected_brand,
                'category': category,
                'weight': weight,
                'file_path': file_path,
                'content_sample': content[:200] + "..." if len(content) > 200 else content
            }
            
        except Exception as e:
            print(f"[오류] 파일 처리 실패: {file_path} - {e}")
            return {
                'product_name': f'파일 오류: {os.path.basename(file_path)}',
                'detected_brand': '미확인',
                'category': '미확인',
                'weight': '미확인',
                'file_path': file_path,
                'content_sample': ''
            }
    
    def extract_product_name(self, content: str) -> str:
        """HTML 콘텐츠에서 제품명 추출"""
        # <title> 태그에서 추출
        title_pattern = r'<title>(.*?)</title>'
        title_match = re.search(title_pattern, content, re.IGNORECASE)
        if title_match:
            return title_match.group(1).strip()
        
        # h1, h2 태그에서 추출 시도
        h_pattern = r'<h[12][^>]*>(.*?)</h[12]>'
        h_match = re.search(h_pattern, content, re.IGNORECASE)
        if h_match:
            return re.sub(r'<[^>]+>', '', h_match.group(1)).strip()
        
        # meta description에서 추출 시도
        meta_pattern = r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']'
        meta_match = re.search(meta_pattern, content, re.IGNORECASE)
        if meta_match:
            return meta_match.group(1)[:50] + "..."
        
        return "제품명 추출 실패"
    
    def detect_brand(self, product_name: str, content: str) -> str:
        """제품명과 콘텐츠에서 브랜드 감지"""
        search_text = f"{product_name} {content}".lower()
        
        for brand_name, patterns in self.brand_patterns.items():
            for pattern in patterns:
                if pattern.lower() in search_text:
                    return brand_name
        
        # 추가 패턴 매칭
        if "만원요리" in search_text or "최씨남매" in search_text:
            return "만원요리_최씨남매"
        elif "취영루" in search_text:
            return "취영루"
        elif any(word in search_text for word in ["청정원", "chungjung"]):
            return "청정원"
        elif any(word in search_text for word in ["오뚜기", "ottogi"]):
            return "오뚜기"
        
        return "미분류"
    
    def estimate_category(self, product_name: str, content: str) -> str:
        """제품 카테고리 추정"""
        text = f"{product_name} {content}".lower()
        
        categories = {
            "만두류": ["만두", "교자", "왕만두", "군만두", "물만두", "김치만두"],
            "면류": ["라면", "국수", "냉면", "파스타", "우동"],
            "반찬류": ["반찬", "나물", "김치", "젓갈"],
            "육류": ["고기", "소고기", "돼지고기", "닭고기", "육류"],
            "해산물": ["생선", "새우", "오징어", "해산물", "수산"],
            "간편식": ["간편식", "즉석", "레토르트"],
            "조미료": ["간장", "된장", "고추장", "조미료", "양념"],
            "음료": ["음료", "주스", "차", "커피"],
            "유제품": ["우유", "치즈", "요구르트", "유제품"]
        }
        
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return "기타"
    
    def extract_weight(self, product_name: str) -> str:
        """제품명에서 중량/용량 추출"""
        weight_patterns = [
            r'(\d+(?:\.\d+)?kg)',
            r'(\d+(?:\.\d+)?g)',
            r'(\d+(?:\.\d+)?ml)',
            r'(\d+(?:\.\d+)?l)',
            r'(\d+개입)',
            r'(\d+인분)'
        ]
        
        for pattern in weight_patterns:
            match = re.search(pattern, product_name, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return "중량 미표기"
    
    def classify_by_brands(self):
        """브랜드별 제품 분류"""
        for product_id, data in self.products_data.items():
            brand = data['detected_brand']
            self.brand_taxonomy[brand].append(product_id)
    
    def generate_brands_database(self) -> Dict:
        """브랜드 데이터베이스 생성"""
        brands_db = {}
        
        for brand, product_ids in self.brand_taxonomy.items():
            if brand == "미분류":
                continue
                
            # 브랜드별 통계
            categories = [self.products_data[pid]['category'] for pid in product_ids]
            category_stats = Counter(categories)
            
            # 브랜드 스토리 생성
            brand_story = self.generate_brand_story(brand, len(product_ids), category_stats)
            
            brands_db[brand] = {
                "product_count": len(product_ids),
                "product_ids": product_ids,
                "main_categories": dict(category_stats.most_common(3)),
                "brand_story": brand_story,
                "sample_products": [
                    {
                        "id": pid,
                        "name": self.products_data[pid]['product_name'],
                        "category": self.products_data[pid]['category']
                    }
                    for pid in product_ids[:3]  # 샘플 3개
                ]
            }
        
        return brands_db
    
    def generate_brand_story(self, brand: str, product_count: int, category_stats: Counter) -> str:
        """브랜드별 스토리 생성"""
        stories = {
            "취영루": f"1945년부터 3대에 걸쳐 만두 하나에 집중해온 대한민국 대표 만두 전문기업입니다. "
                     f"70년간 변하지 않는 정통 제조법으로 현재 {product_count}개 제품을 선보이고 있습니다.",
            
            "만원요리_최씨남매": f"유튜브 커머스를 통해 고객과 소통하는 신세대 식품 브랜드입니다. "
                                f"AI 자동화 시스템으로 {product_count}개 엄선된 제품을 합리적인 가격에 제공합니다.",
            
            "청정원": f"1954년 창업 이래 한국 전통 장류의 맛을 지켜온 종합 식품기업입니다. "
                     f"현재 {product_count}개 프리미엄 제품으로 건강한 식문화를 선도합니다.",
            
            "오뚜기": f"1969년 창업한 대한민국 대표 종합식품기업입니다. "
                     f"{product_count}개 혁신적인 제품으로 간편하고 맛있는 식사를 제안합니다."
        }
        
        return stories.get(brand, f"{brand} 브랜드의 {product_count}개 엄선된 제품을 만나보세요.")
    
    def save_analysis_results(self, brands_database: Dict):
        """분석 결과 저장"""
        # 브랜드 데이터베이스 저장
        db_path = os.path.join(self.temp_txt_dir, "..", "analysis", "brands_database.json")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(brands_database, f, ensure_ascii=False, indent=2)
        
        # 상세 분석 보고서 저장
        report = self.generate_analysis_report(brands_database)
        report_path = os.path.join(self.temp_txt_dir, "..", "analysis", "brand_analysis_report.md")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"[완료] 분석 결과 저장 완료:")
        print(f"   [DB] 브랜드 DB: {db_path}")
        print(f"   [보고서] 분석 보고서: {report_path}")
    
    def generate_analysis_report(self, brands_database: Dict) -> str:
        """분석 보고서 생성"""
        report = """# 🔍 230개 제품 브랜드 분석 보고서

## 📊 브랜드별 제품 현황

"""
        
        total_products = sum(data['product_count'] for data in brands_database.values())
        
        for brand, data in sorted(brands_database.items(), key=lambda x: x[1]['product_count'], reverse=True):
            percentage = (data['product_count'] / total_products) * 100
            report += f"""### {brand}
- **제품 수**: {data['product_count']}개 ({percentage:.1f}%)
- **주요 카테고리**: {', '.join(data['main_categories'].keys())}
- **브랜드 스토리**: {data['brand_story']}

**샘플 제품들**:
"""
            for sample in data['sample_products']:
                report += f"- `{sample['id']}`: {sample['name']} ({sample['category']})\n"
            
            report += "\n---\n\n"
        
        # 미분류 제품들
        if "미분류" in self.brand_taxonomy:
            unclassified = self.brand_taxonomy["미분류"]
            report += f"""## ⚠️ 미분류 제품들 ({len(unclassified)}개)

추가 조사가 필요한 제품들:
"""
            for pid in unclassified[:10]:  # 처음 10개만 표시
                product_name = self.products_data[pid]['product_name']
                report += f"- `{pid}`: {product_name}\n"
            
            if len(unclassified) > 10:
                report += f"- ... 외 {len(unclassified) - 10}개\n"
        
        return report

# 실행 함수
def run_brand_analysis():
    """브랜드 분석 실행"""
    temp_txt_dir = "C:/Users/8899y/CUA-MASTER/modules/cafe24/complete_content/html/temp_txt"
    
    analyzer = BrandAnalysisSystem(temp_txt_dir)
    results = analyzer.analyze_all_products()
    
    print("\n[성공] 브랜드 분석 완료!")
    print("다음 단계: Claude Bridge 활용 자동화 시스템 구축")
    
    return results

if __name__ == "__main__":
    run_brand_analysis()
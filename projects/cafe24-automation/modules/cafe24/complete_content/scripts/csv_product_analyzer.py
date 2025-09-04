import pandas as pd
import json
from typing import Dict, List

class CSVProductAnalyzer:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.products_df = None
        self.brand_mapping = {}
        
    def load_and_analyze(self):
        """CSV 로드 및 분석"""
        print("[CSV] 상품 데이터 로드 중...")
        
        # CSV 로드
        self.products_df = pd.read_csv(self.csv_path, encoding='utf-8-sig')
        print(f"[CSV] 총 {len(self.products_df)}개 상품 데이터 로드 완료")
        
        # 브랜드 패턴 분석
        self.analyze_brand_patterns()
        
        # 상품번호-이름 매핑 생성
        product_mapping = self.create_product_mapping()
        
        return product_mapping
    
    def analyze_brand_patterns(self):
        """브랜드 패턴 분석"""
        print("[분석] 브랜드 패턴 추출 중...")
        
        brand_counts = {}
        
        for _, row in self.products_df.iterrows():
            product_name = row['상품명']
            
            # [브랜드명] 패턴 추출
            import re
            brand_match = re.search(r'\[([^\]]+)\]', product_name)
            
            if brand_match:
                brand_name = brand_match.group(1)
                
                if brand_name not in brand_counts:
                    brand_counts[brand_name] = {
                        'count': 0,
                        'products': [],
                        'categories': set()
                    }
                
                brand_counts[brand_name]['count'] += 1
                brand_counts[brand_name]['products'].append({
                    'code': row['상품코드'],
                    'number': row['상품번호'],
                    'name': product_name
                })
                
                # 카테고리 추정
                category = self.estimate_category(product_name)
                brand_counts[brand_name]['categories'].add(category)
                
                # 디버깅: 진귀한선물 브랜드 확인
                if brand_name == "진귀한선물":
                    print(f"[디버그] 진귀한선물 발견: {product_name}")
        
        # 결과 정리
        for brand, data in brand_counts.items():
            data['categories'] = list(data['categories'])
            print(f"[브랜드] {brand}: {data['count']}개 상품")
        
        self.brand_mapping = brand_counts
        return brand_counts
    
    def estimate_category(self, product_name: str) -> str:
        """상품명으로 카테고리 추정"""
        name_lower = product_name.lower()
        
        if any(keyword in name_lower for keyword in ['갈비', '불고기', '소', '돼지', '한우', '한돈']):
            return '육류'
        elif any(keyword in name_lower for keyword in ['오징어', '새우', '조개', '어포', '해산물']):
            return '해산물'
        elif any(keyword in name_lower for keyword in ['김치', '나물', '반찬']):
            return '반찬류'
        elif any(keyword in name_lower for keyword in ['라면', '국수', '면']):
            return '면류'
        else:
            return '기타'
    
    def create_product_mapping(self) -> Dict:
        """상품번호-상품명 매핑 생성"""
        mapping = {}
        
        for _, row in self.products_df.iterrows():
            product_number = str(row['상품번호'])
            product_name = row['상품명']
            product_code = row['상품코드']
            
            # 브랜드 추출
            import re
            brand_match = re.search(r'\[([^\]]+)\]', product_name)
            brand = brand_match.group(1) if brand_match else '미분류'
            
            # 실제 상품명 (브랜드 제외)
            clean_name = re.sub(r'\[[^\]]+\]', '', product_name).strip()
            
            mapping[product_number] = {
                'product_code': product_code,
                'full_name': product_name,
                'clean_name': clean_name,
                'brand': brand,
                'category': self.estimate_category(product_name)
            }
        
        return mapping
    
    def save_results(self, output_path: str):
        """결과 저장"""
        results = {
            'total_products': len(self.products_df),
            'brand_analysis': self.brand_mapping,
            'product_mapping': self.create_product_mapping()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"[저장] 분석 결과 저장: {output_path}")
        return results

def analyze_csv_products():
    """CSV 상품 분석 실행"""
    csv_path = "C:/Users/8899y/CUA-MASTER/modules/cafe24/download/manwonyori_20250901_301_e68d.csv"
    output_path = "C:/Users/8899y/CUA-MASTER/modules/cafe24/complete_content/html/analysis/csv_product_analysis.json"
    
    analyzer = CSVProductAnalyzer(csv_path)
    results = analyzer.load_and_analyze()
    analyzer.save_results(output_path)
    
    print(f"\n[완료] CSV 분석 완료!")
    print(f"총 {len(results)}개 상품 매핑 생성")
    
    return results

if __name__ == "__main__":
    analyze_csv_products()
"""
브랜드명 기반 분류 스크립트
상품명의 [브랜드명] 패턴을 이용한 분류
"""
import csv
import shutil
from pathlib import Path
import re
from datetime import datetime
from collections import defaultdict

def classify_by_brand():
    """브랜드명으로 HTML 파일 분류"""
    
    csv_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\download\manwonyori_20250901_301_e68d.csv")
    html_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html")
    
    brand_mapping = {}
    
    # CSV에서 브랜드 정보 추출
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            product_no = row.get('상품번호', '')
            product_name = row.get('상품명', '')
            
            if not product_no:
                continue
            
            # 브랜드 추출
            brand = '기타'
            match = re.search(r'\[(.*?)\]', product_name)
            if match:
                brand_raw = match.group(1)
                
                if '씨씨더블유' in brand_raw:
                    brand = '씨씨더블유'
                elif '인생' in brand_raw:
                    brand = '인생'
                elif '반찬단지' in brand_raw:
                    brand = '반찬단지'
                elif '태공식품' in brand_raw:
                    brand = '태공식품'
                elif '취영루' in brand_raw:
                    brand = '취영루'
                elif '최씨남매' in brand_raw:
                    brand = '최씨남매'
                elif '모비딕' in brand_raw:
                    brand = '모비딕'
                elif 'BS' in brand_raw or '비에스' in brand_raw:
                    brand = '비에스'
                else:
                    brand = brand_raw
            elif '만원요리' in product_name:
                brand = '만원요리'
            
            brand_mapping[product_no] = brand
    
    print(f"브랜드 매핑: {len(brand_mapping)}개 상품")
    
    # 브랜드별 통계
    brand_counts = defaultdict(int)
    for brand in brand_mapping.values():
        brand_counts[brand] += 1
    
    for brand, count in sorted(brand_counts.items()):
        print(f"  {brand}: {count}개")
    
    return brand_mapping

if __name__ == "__main__":
    classify_by_brand()
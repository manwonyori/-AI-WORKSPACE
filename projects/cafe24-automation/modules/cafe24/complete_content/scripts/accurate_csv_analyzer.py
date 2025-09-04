import pandas as pd
import re
from collections import Counter

def analyze_csv_accurately():
    """정확한 CSV 브랜드 분석"""
    csv_path = "C:/Users/8899y/CUA-MASTER/modules/cafe24/download/manwonyori_20250901_301_e68d.csv"
    
    print("[정확한 분석] CSV 브랜드 분석 시작...")
    
    # CSV 로드
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    print(f"총 {len(df)}개 상품 로드")
    
    brand_counter = Counter()
    detailed_brands = {}
    
    for index, row in df.iterrows():
        product_name = row['상품명']
        product_number = row['상품번호']
        
        # [브랜드명] 패턴 정확히 추출
        brand_match = re.search(r'\[([^\]]+)\]', product_name)
        
        if brand_match:
            brand = brand_match.group(1)
            brand_counter[brand] += 1
            
            if brand not in detailed_brands:
                detailed_brands[brand] = []
            
            detailed_brands[brand].append({
                'number': product_number,
                'name': product_name
            })
        else:
            # 브랜드 없는 제품
            brand_counter['브랜드없음'] += 1
            print(f"브랜드 없음: {product_number} - {product_name}")
    
    # 결과 출력
    print("\n=== 정확한 브랜드 현황 ===")
    for brand, count in brand_counter.most_common():
        percentage = (count / len(df)) * 100
        print(f"{brand}: {count}개 ({percentage:.1f}%)")
        
        # 샘플 3개 표시
        if brand in detailed_brands:
            print("  샘플:")
            for sample in detailed_brands[brand][:3]:
                print(f"    {sample['number']}: {sample['name']}")
        print()
    
    return brand_counter, detailed_brands

if __name__ == "__main__":
    analyze_csv_accurately()
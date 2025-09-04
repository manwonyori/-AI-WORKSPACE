"""
새 CSV 데이터를 기준으로 HTML 파일 업체 분류 업데이트
"""
import csv
import shutil
from pathlib import Path

def update_classification():
    """새 CSV 기준으로 HTML 파일 재분류"""
    
    # CSV에서 공급사 매핑 로드
    csv_path = r'C:\Users\8899y\CUA-MASTER\modules\cafe24\download\manwonyori_20250901_299_6bef.csv'
    supplier_mapping = {}
    
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            product_no = row.get('상품번호', '')
            supplier = row.get('공급사', '')
            if product_no and supplier:
                supplier_mapping[product_no] = supplier
    
    # 공급사 코드 - 브랜드명 매핑
    supplier_brands = {
        'S000000T': '인생',        # 95개 - 가장 많은 메인 브랜드
        'S000000K': '기타',        # 48개 - 초기 제품들
        'S000000Y': '씨씨더블유',   # 37개
        'S000000V': '취영루',       # 26개 
        'S000000L': '인생만두',     # 14개 - 진짜 인생만두 (62, 65, 131-145)
        'S000000I': '만원요리',     # 6개 - 진짜 만원요리
        'S000000S': '해선',        # 5개 - 새 발견 브랜드
        'S000000Q': '비에스',      # 2개 - 새 발견 브랜드 
        'S000000C': '기타2',       # 2개
        'S0000000': '기타3',       # 2개
        'S000000O': '기타4',       # 1개
        'S000000N': '기타5'        # 1개
    }
    
    base_path = Path(r'C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html')
    
    # 새 브랜드 폴더 생성
    new_brands = ['해선', '비에스', '기타2', '기타3', '기타4', '기타5']
    for brand in new_brands:
        (base_path / brand).mkdir(exist_ok=True)
        print(f"[OK] {brand} 폴더 생성")
    
    # 재분류 통계
    stats = {'moved': 0, 'total': 0}
    
    # 모든 HTML 파일 확인 및 이동
    for folder in base_path.iterdir():
        if folder.is_dir() and folder.name != 'nul':
            html_files = list(folder.glob('*.html'))
            
            for html_file in html_files:
                product_no = html_file.stem
                stats['total'] += 1
                
                # CSV에서 올바른 브랜드 찾기
                if product_no in supplier_mapping:
                    supplier_code = supplier_mapping[product_no]
                    correct_brand = supplier_brands.get(supplier_code, '미분류')
                    
                    # 현재 폴더와 다른 경우 이동
                    if folder.name != correct_brand:
                        dest_folder = base_path / correct_brand
                        dest_folder.mkdir(exist_ok=True)
                        dest_file = dest_folder / html_file.name
                        
                        try:
                            shutil.move(str(html_file), str(dest_file))
                            stats['moved'] += 1
                            print(f"  → {product_no}.html: {folder.name} → {correct_brand}")
                        except Exception as e:
                            print(f"  ✗ Error moving {product_no}.html: {e}")
    
    print(f"\n=== 재분류 완료 ===")
    print(f"총 파일: {stats['total']}개")
    print(f"이동된 파일: {stats['moved']}개")
    
    # 최종 통계
    print("\n=== 최종 브랜드별 통계 ===")
    final_stats = {}
    for folder in base_path.iterdir():
        if folder.is_dir() and folder.name != 'nul':
            html_count = len(list(folder.glob('*.html')))
            if html_count > 0:
                final_stats[folder.name] = html_count
    
    for brand, count in sorted(final_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"{brand}: {count}개")
    
    return final_stats

if __name__ == "__main__":
    print("=== CSV 기준 HTML 파일 재분류 시작 ===")
    update_classification()
    print("\n✓ 재분류 완료!")
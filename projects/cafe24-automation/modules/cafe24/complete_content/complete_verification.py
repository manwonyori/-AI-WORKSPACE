"""
HTML 파일 구조와 CSV 데이터 완벽 매칭 검증
모든 파일을 조사하고 정확한 매칭 확인
"""
import csv
import json
from pathlib import Path
from collections import defaultdict
import re

def analyze_html_structure():
    """HTML 폴더 구조 완전 분석"""
    
    base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html")
    
    print("=" * 80)
    print("HTML 폴더 구조 완전 분석")
    print("=" * 80)
    
    # 모든 HTML 파일 수집
    all_files = {}
    folder_stats = {}
    
    for folder in base_path.iterdir():
        if folder.is_dir() and folder.name not in ['temp_txt', 'nul']:
            html_files = list(folder.glob("*.html"))
            if html_files:
                folder_stats[folder.name] = len(html_files)
                file_numbers = [int(f.stem) for f in html_files]
                all_files[folder.name] = sorted(file_numbers)
                print(f"{folder.name}: {len(html_files)}개")
                print(f"  파일 번호: {sorted(file_numbers)}")
    
    print(f"\n총 폴더: {len(folder_stats)}개")
    print(f"총 파일: {sum(folder_stats.values())}개")
    
    return all_files, folder_stats

def analyze_csv_data():
    """CSV 데이터 완전 분석"""
    
    csv_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\download\manwonyori_20250901_301_e68d.csv")
    
    print("\n" + "=" * 80)
    print("CSV 데이터 완전 분석")
    print("=" * 80)
    
    csv_data = {}
    brand_mapping = defaultdict(list)
    
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
                
                if '씨씨더블유' in brand_raw or 'CCW' in brand_raw:
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
                elif '피자코리아' in brand_raw:
                    brand = '피자코리아'
                elif '단지식품' in brand_raw:
                    brand = '단지식품유통'
                else:
                    brand = brand_raw
            elif '만원요리' in product_name:
                brand = '만원요리'
            
            csv_data[product_no] = {
                'brand': brand,
                'name': product_name
            }
            brand_mapping[brand].append(int(product_no))
    
    print(f"CSV 상품 수: {len(csv_data)}개")
    print("\nCSV 브랜드별 상품 수:")
    for brand, products in brand_mapping.items():
        print(f"  {brand}: {len(products)}개 - {sorted(products)}")
    
    return csv_data, brand_mapping

def cross_verify_matching(html_files, csv_data, csv_brands):
    """HTML과 CSV 완벽 매칭 검증"""
    
    print("\n" + "=" * 80)
    print("HTML ↔ CSV 완벽 매칭 검증")
    print("=" * 80)
    
    errors = []
    
    # 1. HTML에는 있지만 CSV에 없는 파일
    print("\n[1] HTML에는 있지만 CSV에 없는 파일:")
    html_only = []
    for folder, files in html_files.items():
        for file_no in files:
            if str(file_no) not in csv_data:
                html_only.append((folder, file_no))
                print(f"  {file_no}.html (현재: {folder})")
    
    if not html_only:
        print("  ✅ 없음")
    
    # 2. CSV에는 있지만 HTML에 없는 파일
    print("\n[2] CSV에는 있지만 HTML에 없는 파일:")
    csv_only = []
    all_html_numbers = set()
    for files in html_files.values():
        all_html_numbers.update(files)
    
    for product_no in csv_data.keys():
        if int(product_no) not in all_html_numbers:
            csv_only.append(product_no)
            print(f"  {product_no} - {csv_data[product_no]['brand']}: {csv_data[product_no]['name'][:50]}...")
    
    if not csv_only:
        print("  ✅ 없음")
    
    # 3. 브랜드 폴더가 잘못된 파일
    print("\n[3] 브랜드 폴더가 잘못된 파일:")
    misplaced = []
    for folder, files in html_files.items():
        for file_no in files:
            if str(file_no) in csv_data:
                correct_brand = csv_data[str(file_no)]['brand']
                if folder != correct_brand:
                    misplaced.append({
                        'file': file_no,
                        'current': folder,
                        'correct': correct_brand,
                        'name': csv_data[str(file_no)]['name']
                    })
                    print(f"  {file_no}.html: {folder} → {correct_brand}")
                    print(f"    상품명: {csv_data[str(file_no)]['name']}")
    
    if not misplaced:
        print("  ✅ 없음")
    
    # 4. 브랜드별 매칭 확인
    print("\n[4] 브랜드별 매칭 상세 확인:")
    for brand, csv_files in csv_brands.items():
        html_files_in_brand = html_files.get(brand, [])
        
        missing_in_html = set(csv_files) - set(html_files_in_brand)
        extra_in_html = set(html_files_in_brand) - set(csv_files)
        
        print(f"\n  {brand}:")
        print(f"    CSV: {len(csv_files)}개 - {sorted(csv_files)}")
        print(f"    HTML: {len(html_files_in_brand)}개 - {sorted(html_files_in_brand)}")
        
        if missing_in_html:
            print(f"    ❌ HTML에 없음: {sorted(missing_in_html)}")
        if extra_in_html:
            print(f"    ❌ HTML에 추가: {sorted(extra_in_html)}")
        if not missing_in_html and not extra_in_html:
            print(f"    ✅ 완벽 매칭")
    
    return {
        'html_only': html_only,
        'csv_only': csv_only,
        'misplaced': misplaced,
        'total_errors': len(html_only) + len(csv_only) + len(misplaced)
    }

def generate_verification_report(html_files, csv_data, verification_results):
    """검증 리포트 생성"""
    
    from datetime import datetime
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_path = Path(f"C:\\Users\\8899y\\CUA-MASTER\\modules\\cafe24\\complete_content\\verification_report_{timestamp}.json")
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'html_structure': {folder: len(files) for folder, files in html_files.items()},
        'csv_products': len(csv_data),
        'verification_results': verification_results,
        'detailed_html_files': html_files
    }
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n[REPORT] {report_path}")
    
    # 텍스트 리포트
    txt_path = report_path.with_suffix('.txt')
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("HTML-CSV 완벽 매칭 검증 리포트\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"검증 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"총 오류: {verification_results['total_errors']}개\n\n")
        
        if verification_results['html_only']:
            f.write("HTML에만 있는 파일:\n")
            for folder, file_no in verification_results['html_only']:
                f.write(f"  {file_no}.html ({folder})\n")
            f.write("\n")
        
        if verification_results['csv_only']:
            f.write("CSV에만 있는 파일:\n")
            for file_no in verification_results['csv_only']:
                f.write(f"  {file_no}\n")
            f.write("\n")
        
        if verification_results['misplaced']:
            f.write("잘못 배치된 파일:\n")
            for item in verification_results['misplaced']:
                f.write(f"  {item['file']}.html: {item['current']} → {item['correct']}\n")
    
    print(f"[REPORT] {txt_path}")

if __name__ == "__main__":
    print("HTML 파일 구조와 CSV 완벽 매칭 검증 시작")
    
    # 1. HTML 구조 분석
    html_files, html_stats = analyze_html_structure()
    
    # 2. CSV 데이터 분석  
    csv_data, csv_brands = analyze_csv_data()
    
    # 3. 매칭 검증
    verification_results = cross_verify_matching(html_files, csv_data, csv_brands)
    
    # 4. 리포트 생성
    generate_verification_report(html_files, csv_data, verification_results)
    
    # 5. 결과 요약
    print("\n" + "=" * 80)
    print("최종 검증 결과")
    print("=" * 80)
    
    if verification_results['total_errors'] == 0:
        print("✅ 완벽한 매칭! 모든 파일이 올바르게 배치되었습니다.")
    else:
        print(f"❌ {verification_results['total_errors']}개의 매칭 오류 발견")
        print("상세 내용은 리포트를 확인하세요.")
    
    print(f"\nHTML 파일: {sum(html_stats.values())}개")
    print(f"CSV 상품: {len(csv_data)}개")
    
    print("\n[COMPLETE] 검증 완료!")
"""
CSV 파일 기반 완전한 재분류
모든 HTML 파일을 CSV의 정확한 브랜드로 재배치
"""
import csv
import shutil
from pathlib import Path
import re
import json
from datetime import datetime
from collections import defaultdict

def parse_csv_complete():
    """CSV 파일 완전 파싱 - 상품번호별 브랜드 정확히 추출"""
    
    csv_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\download\manwonyori_20250901_301_e68d.csv")
    
    if not csv_path.exists():
        print(f"[ERROR] CSV 파일을 찾을 수 없음: {csv_path}")
        return None
    
    product_brands = {}
    brand_counts = defaultdict(int)
    
    print("=" * 60)
    print("CSV 파일 완전 분석")
    print("=" * 60)
    
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            product_no = row.get('상품번호', '')
            product_name = row.get('상품명', '')
            
            if not product_no:
                continue
            
            # 상품명에서 브랜드 추출
            brand = '기타'  # 기본값
            
            # [브랜드명] 패턴으로 브랜드 추출
            match = re.search(r'\[(.*?)\]', product_name)
            if match:
                brand_raw = match.group(1)
                
                # 브랜드 정규화
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
                    brand = brand_raw  # 그대로 사용
            elif '만원요리' in product_name:
                brand = '만원요리'
            
            product_brands[product_no] = brand
            brand_counts[brand] += 1
            
            # 디버그 출력 (주요 상품만)
            if product_no in ['172', '143', '144', '151', '168', '77', '92', '93', '94']:
                print(f"  {product_no}: {product_name} → {brand}")
    
    print(f"\n[FOUND] {len(product_brands)}개 상품의 브랜드 정보 추출")
    print("\n[브랜드별 상품 수]")
    for brand, count in sorted(brand_counts.items()):
        print(f"  {brand}: {count}개")
    
    return product_brands

def clean_and_reorganize_html(product_brands):
    """모든 HTML 파일 재분류"""
    
    base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html")
    
    # 통계
    stats = {
        'total_files': 0,
        'moved_files': 0,
        'already_correct': 0,
        'not_in_csv': 0,
        'errors': 0,
        'movements': defaultdict(lambda: defaultdict(int))
    }
    
    print("\n" + "=" * 60)
    print("HTML 파일 완전 재분류")
    print("=" * 60)
    
    # 1. 먼저 모든 HTML 파일을 수집
    all_html_files = []
    for folder in base_path.iterdir():
        if folder.is_dir() and folder.name != 'temp_txt':
            for html_file in folder.glob("*.html"):
                all_html_files.append((folder.name, html_file))
    
    print(f"[SCAN] {len(all_html_files)}개 HTML 파일 발견")
    
    # 2. 각 파일을 올바른 브랜드 폴더로 이동
    for current_folder, html_file in all_html_files:
        stats['total_files'] += 1
        product_no = html_file.stem  # 파일명에서 상품번호 추출
        
        if product_no in product_brands:
            correct_brand = product_brands[product_no]
            
            # 대상 폴더 생성
            target_folder = base_path / correct_brand
            target_folder.mkdir(exist_ok=True)
            
            if current_folder != correct_brand:
                # 파일 이동 필요
                try:
                    target_path = target_folder / html_file.name
                    if target_path.exists():
                        target_path.unlink()  # 기존 파일 삭제
                    shutil.move(str(html_file), str(target_path))
                    stats['moved_files'] += 1
                    stats['movements'][current_folder][correct_brand] += 1
                    print(f"  [MOVE] {product_no}.html: {current_folder} → {correct_brand}")
                except Exception as e:
                    print(f"  [ERROR] {product_no}.html 이동 실패: {e}")
                    stats['errors'] += 1
            else:
                stats['already_correct'] += 1
        else:
            print(f"  [WARNING] {product_no}: CSV에 없음 (현재 위치: {current_folder})")
            stats['not_in_csv'] += 1
    
    return stats

def remove_empty_folders():
    """빈 폴더 삭제"""
    
    base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html")
    
    print("\n" + "=" * 60)
    print("빈 폴더 정리")
    print("=" * 60)
    
    deleted_folders = []
    
    for folder in base_path.iterdir():
        if folder.is_dir() and folder.name not in ['temp_txt', 'nul']:
            html_files = list(folder.glob("*.html"))
            if len(html_files) == 0:
                try:
                    shutil.rmtree(folder)
                    deleted_folders.append(folder.name)
                    print(f"  [DELETE] {folder.name} 폴더 삭제")
                except Exception as e:
                    print(f"  [ERROR] {folder.name} 삭제 실패: {e}")
    
    return deleted_folders

def verify_final_structure():
    """최종 구조 검증"""
    
    base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html")
    
    print("\n" + "=" * 60)
    print("최종 폴더 구조")
    print("=" * 60)
    
    folder_stats = {}
    total_files = 0
    
    for folder in sorted(base_path.iterdir()):
        if folder.is_dir() and folder.name not in ['temp_txt', 'nul']:
            html_files = list(folder.glob("*.html"))
            if html_files:
                folder_stats[folder.name] = len(html_files)
                total_files += len(html_files)
                print(f"  {folder.name}: {len(html_files)}개")
    
    print(f"\n총 HTML 파일: {total_files}개")
    
    return folder_stats

def generate_complete_report(product_brands, reorg_stats, folder_stats):
    """완전한 재분류 리포트 생성"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_path = Path(f"C:\\Users\\8899y\\CUA-MASTER\\modules\\cafe24\\complete_content\\reports\\complete_reclassification_{timestamp}.json")
    report_path.parent.mkdir(exist_ok=True)
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'csv_file': 'manwonyori_20250901_301_e68d.csv',
        'total_products_in_csv': len(product_brands),
        'reorganization_stats': dict(reorg_stats),
        'final_folder_structure': folder_stats,
        'movements': dict(reorg_stats.get('movements', {}))
    }
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n[REPORT] {report_path}")
    
    # 텍스트 리포트
    txt_report_path = report_path.with_suffix('.txt')
    with open(txt_report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("완전한 재분류 리포트\n")
        f.write(f"생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"CSV 파일: manwonyori_20250901_301_e68d.csv\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("[재분류 통계]\n")
        f.write(f"총 파일: {reorg_stats['total_files']}개\n")
        f.write(f"이동된 파일: {reorg_stats['moved_files']}개\n")
        f.write(f"올바른 위치: {reorg_stats['already_correct']}개\n")
        f.write(f"CSV에 없음: {reorg_stats['not_in_csv']}개\n")
        f.write(f"오류: {reorg_stats['errors']}개\n\n")
        
        if reorg_stats.get('movements'):
            f.write("[파일 이동 내역]\n")
            for from_folder, to_folders in reorg_stats['movements'].items():
                for to_folder, count in to_folders.items():
                    f.write(f"  {from_folder} → {to_folder}: {count}개\n")
            f.write("\n")
        
        f.write("[최종 폴더 구조]\n")
        for folder, count in sorted(folder_stats.items()):
            f.write(f"  {folder}: {count}개\n")
        f.write(f"\n총 HTML 파일: {sum(folder_stats.values())}개\n")
    
    print(f"[REPORT] {txt_report_path}")

if __name__ == "__main__":
    print("CSV 기반 완전한 재분류 시작\n")
    
    # 1. CSV 완전 파싱
    product_brands = parse_csv_complete()
    
    if not product_brands:
        print("[ERROR] CSV 파싱 실패")
        exit(1)
    
    # 2. HTML 파일 재분류
    reorg_stats = clean_and_reorganize_html(product_brands)
    
    # 3. 빈 폴더 정리
    deleted_folders = remove_empty_folders()
    
    # 4. 최종 구조 검증
    folder_stats = verify_final_structure()
    
    # 5. 리포트 생성
    generate_complete_report(product_brands, reorg_stats, folder_stats)
    
    print("\n[COMPLETE] 완전한 재분류 완료!")
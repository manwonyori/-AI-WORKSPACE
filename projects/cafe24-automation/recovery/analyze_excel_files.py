import pandas as pd
import os
from pathlib import Path

def analyze_excel_file(file_path):
    """엑셀 파일을 분석하여 컬럼 구조와 데이터 패턴을 파악"""
    try:
        # 파일 존재 여부 확인
        if not os.path.exists(file_path):
            return {"error": f"파일을 찾을 수 없습니다: {file_path}"}
        
        # 엑셀 파일 읽기 (첫 번째 시트)
        df = pd.read_excel(file_path)
        
        analysis = {
            "file_name": os.path.basename(file_path),
            "file_path": file_path,
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "columns": list(df.columns),
            "sample_data": {},
            "data_types": {},
            "null_counts": {},
            "has_order_product_name_with_options": False
        }
        
        # 컬럼별 데이터 타입과 null 개수
        for col in df.columns:
            analysis["data_types"][col] = str(df[col].dtype)
            analysis["null_counts"][col] = df[col].isnull().sum()
            
            # 샘플 데이터 (첫 3개 값)
            sample_values = df[col].dropna().head(3).tolist()
            analysis["sample_data"][col] = sample_values
        
        # "주문상품명(옵션포함)" 컬럼 존재 여부 확인
        order_product_columns = [col for col in df.columns if "주문상품명" in col and "옵션" in col]
        if order_product_columns:
            analysis["has_order_product_name_with_options"] = True
            analysis["order_product_column_name"] = order_product_columns[0]
        
        return analysis
        
    except Exception as e:
        return {"error": f"파일 분석 중 오류 발생: {str(e)}"}

def main():
    # 분석할 파일 목록
    file_paths = [
        r"D:\주문취합\주문_배송\20250812\만원요리_취영루_20250812.xlsx",
        r"D:\주문취합\주문_배송\20250812\[인생]_만원요리_인생_20250812.xlsx",
        r"D:\주문취합\주문_배송\20250812\만원요리_BS_20250812.xlsx",
        r"D:\주문취합\주문_배송\20250812\만원요리_모비딕_20250812.xlsx",
        r"D:\주문취합\주문_배송\20250812\만원요리_반찬단지_20250812.xlsx",
        r"D:\주문취합\주문_배송\20250812\만원요리_최씨남매_20250812.xlsx",
        r"D:\주문취합\주문_배송\20250812\만원요리_최씨남매제조_20250812.xlsx"
    ]
    
    print("=" * 80)
    print("엑셀 파일 분석 시작")
    print("=" * 80)
    
    all_analyses = []
    
    for file_path in file_paths:
        print(f"\n분석 중: {os.path.basename(file_path)}")
        analysis = analyze_excel_file(file_path)
        all_analyses.append(analysis)
        
        if "error" in analysis:
            print(f"ERROR: {analysis['error']}")
            continue
        
        print(f"OK 파일명: {analysis['file_name']}")
        print(f"   행 수: {analysis['total_rows']}")
        print(f"   열 수: {analysis['total_columns']}")
        print(f"   주문상품명(옵션포함) 컬럼: {'있음' if analysis['has_order_product_name_with_options'] else '없음'}")
        
        print(f"   컬럼 목록:")
        for i, col in enumerate(analysis['columns'], 1):
            print(f"     {i:2d}. {col}")
    
    # 상세 분석 결과 출력
    print("\n" + "=" * 80)
    print("상세 분석 결과")
    print("=" * 80)
    
    for analysis in all_analyses:
        if "error" in analysis:
            continue
            
        print(f"\n[FILE] {analysis['file_name']}")
        print(f"   경로: {analysis['file_path']}")
        print(f"   데이터 크기: {analysis['total_rows']}행 x {analysis['total_columns']}열")
        
        if analysis['has_order_product_name_with_options']:
            print(f"   OK 주문상품명(옵션포함) 컬럼: {analysis.get('order_product_column_name', '찾음')}")
        else:
            print(f"   NO 주문상품명(옵션포함) 컬럼: 없음")
        
        print(f"   컬럼별 정보:")
        for col in analysis['columns']:
            null_count = analysis['null_counts'][col]
            data_type = analysis['data_types'][col]
            sample_data = analysis['sample_data'][col]
            
            null_info = f"(null: {null_count})" if null_count > 0 else ""
            sample_info = f" | 샘플: {sample_data[:2]}" if sample_data else ""
            
            print(f"     - {col} [{data_type}]{null_info}{sample_info}")
    
    # 컬럼 비교 분석
    print(f"\n" + "=" * 80)
    print("업체별 컬럼 구조 비교")
    print("=" * 80)
    
    # 모든 컬럼 수집
    all_columns = set()
    for analysis in all_analyses:
        if "error" not in analysis:
            all_columns.update(analysis['columns'])
    
    print(f"전체 발견된 컬럼 수: {len(all_columns)}")
    print(f"업체별 컬럼 존재 여부:")
    
    for col in sorted(all_columns):
        print(f"\n[COLUMN] {col}:")
        for analysis in all_analyses:
            if "error" not in analysis:
                exists = "O" if col in analysis['columns'] else "X"
                company = analysis['file_name'].replace('만원요리_', '').replace('_20250812.xlsx', '')
                print(f"   {exists} {company}")
    
    print(f"\n" + "=" * 80)
    print("분석 완료")
    print("=" * 80)

if __name__ == "__main__":
    main()
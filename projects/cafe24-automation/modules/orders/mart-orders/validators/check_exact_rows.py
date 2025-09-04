"""
정확한 10번과 11번 행 확인
엑셀 행 번호 기준
"""

import pandas as pd

def check_exact_rows():
    file_path = 'tests/ccw 발주.xlsx'
    df = pd.read_excel(file_path, sheet_name='CCW B2B수급', header=None)
    
    print("=" * 60)
    print(" CCW B2B수급 - 엑셀 10행과 11행 확인")
    print("=" * 60)
    
    # 엑셀의 10행 = 파이썬 인덱스 9
    # 엑셀의 11행 = 파이썬 인덱스 10
    
    excel_row_10 = 9   # 엑셀 10행
    excel_row_11 = 10  # 엑셀 11행
    
    print("\n[엑셀 10행 데이터]")
    print("-" * 40)
    row_10 = df.iloc[excel_row_10]
    print(f"A열 (번호): {row_10.iloc[0]}")
    print(f"B열 (상품명): {row_10.iloc[1]}")
    print(f"N열 (상품명2): {row_10.iloc[13]}")
    print(f"U열 (주문수량): {row_10.iloc[20] if len(row_10) > 20 else 'N/A'}")
    
    print("\n[엑셀 11행 데이터]")
    print("-" * 40)
    row_11 = df.iloc[excel_row_11]
    print(f"A열 (번호): {row_11.iloc[0]}")
    print(f"B열 (상품명): {row_11.iloc[1]}")
    print(f"N열 (상품명2): {row_11.iloc[13]}")
    print(f"U열 (주문수량): {row_11.iloc[20] if len(row_11) > 20 else 'N/A'}")
    
    print("\n" + "=" * 60)
    print(" 이태원 햄폭탄과 힘찬 장어탕 검색")
    print("=" * 60)
    
    # 모든 행에서 검색
    for i in range(len(df)):
        row = df.iloc[i]
        # B열과 N열 확인
        b_col = str(row.iloc[1]) if pd.notna(row.iloc[1]) else ""
        n_col = str(row.iloc[13]) if len(row) > 13 and pd.notna(row.iloc[13]) else ""
        
        if '이태원' in b_col or '이태원' in n_col:
            print(f"\n'이태원' 발견 - 엑셀 {i+1}행:")
            print(f"  B열: {b_col}")
            print(f"  N열: {n_col}")
            print(f"  U열 (주문수): {row.iloc[20] if len(row) > 20 else 'N/A'}")
            
        if '장어탕' in b_col or '장어탕' in n_col:
            print(f"\n'장어탕' 발견 - 엑셀 {i+1}행:")
            print(f"  B열: {b_col}")
            print(f"  N열: {n_col}")
            print(f"  U열 (주문수): {row.iloc[20] if len(row) > 20 else 'N/A'}")
    
    # 실제 주문이 있는 행만 확인 (U열이 0이 아닌 경우)
    print("\n" + "=" * 60)
    print(" 실제 주문이 있는 품목 (U열 > 0)")
    print("=" * 60)
    
    for i in range(len(df)):
        row = df.iloc[i]
        if len(row) > 20 and pd.notna(row.iloc[20]) and row.iloc[20] > 0:
            print(f"\n엑셀 {i+1}행:")
            print(f"  B열 상품명: {row.iloc[1]}")
            print(f"  N열 상품명: {row.iloc[13]}")
            print(f"  U열 주문수: {row.iloc[20]}")

if __name__ == "__main__":
    check_exact_rows()
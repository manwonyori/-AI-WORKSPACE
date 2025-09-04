"""
B열과 N열 확인 - 10번과 11번 행
"""

import pandas as pd
import string

def check_b_n_columns():
    # CCW B2B수급 시트 읽기
    file_path = 'tests/ccw 발주.xlsx'
    df = pd.read_excel(file_path, sheet_name='CCW B2B수급', header=None)
    
    print("=" * 60)
    print(" CCW B2B수급 - B열과 N열 확인")
    print("=" * 60)
    
    # 엑셀 컬럼 인덱스: A=0, B=1, C=2... N=13
    col_b_idx = 1  # B열
    col_n_idx = 13 # N열
    
    print("\n열 인덱스 매핑:")
    print("  B열 = 인덱스 1")
    print("  N열 = 인덱스 13")
    
    print("\n" + "=" * 60)
    print(" 10번과 11번 행 데이터")
    print("=" * 60)
    
    # 10번 행 (엑셀은 1부터 시작, 파이썬은 0부터 시작)
    # 엑셀의 10번 행 = 파이썬 인덱스 9
    row_10_idx = 9
    row_11_idx = 10
    
    if len(df) > row_10_idx:
        print("\n[10번 행] (엑셀 행번호 10, 파이썬 인덱스 9)")
        print("-" * 40)
        row_10 = df.iloc[row_10_idx]
        print(f"A열 (번호): {row_10.iloc[0]}")
        print(f"B열 (상품명): {row_10.iloc[col_b_idx]}")
        print(f"N열: {row_10.iloc[col_n_idx] if len(row_10) > col_n_idx else 'N/A'}")
        
        # 주변 열도 확인
        print("\n주변 데이터:")
        for i in range(max(0, col_n_idx-2), min(len(row_10), col_n_idx+3)):
            col_letter = string.ascii_uppercase[i] if i < 26 else f"A{string.ascii_uppercase[i-26]}"
            print(f"  {col_letter}열 (인덱스 {i}): {row_10.iloc[i]}")
    
    if len(df) > row_11_idx:
        print("\n[11번 행] (엑셀 행번호 11, 파이썬 인덱스 10)")
        print("-" * 40)
        row_11 = df.iloc[row_11_idx]
        print(f"A열 (번호): {row_11.iloc[0]}")
        print(f"B열 (상품명): {row_11.iloc[col_b_idx]}")
        print(f"N열: {row_11.iloc[col_n_idx] if len(row_11) > col_n_idx else 'N/A'}")
        
        # 주변 열도 확인
        print("\n주변 데이터:")
        for i in range(max(0, col_n_idx-2), min(len(row_11), col_n_idx+3)):
            col_letter = string.ascii_uppercase[i] if i < 26 else f"A{string.ascii_uppercase[i-26]}"
            print(f"  {col_letter}열 (인덱스 {i}): {row_11.iloc[i]}")
    
    print("\n" + "=" * 60)
    print(" 주문 수량 컬럼 찾기")
    print("=" * 60)
    
    # 헤더 행 확인 (보통 1행 또는 2행)
    header_row = df.iloc[1]  # 2번째 행이 헤더
    print("\n헤더 행 (2번째 행):")
    for i in range(min(len(header_row), 22)):
        if pd.notna(header_row.iloc[i]):
            col_letter = string.ascii_uppercase[i] if i < 26 else f"A{string.ascii_uppercase[i-26]}"
            print(f"  {col_letter}열 (인덱스 {i}): {header_row.iloc[i]}")
    
    print("\n" + "=" * 60)
    print(" 최종 확인")
    print("=" * 60)
    
    if len(df) > row_10_idx:
        row_10 = df.iloc[row_10_idx]
        print(f"\n10번 행:")
        print(f"  B열 상품명: {row_10.iloc[col_b_idx]}")
        print(f"  N열 데이터: {row_10.iloc[col_n_idx] if len(row_10) > col_n_idx else 'N/A'}")
        
    if len(df) > row_11_idx:
        row_11 = df.iloc[row_11_idx]
        print(f"\n11번 행:")
        print(f"  B열 상품명: {row_11.iloc[col_b_idx]}")
        print(f"  N열 데이터: {row_11.iloc[col_n_idx] if len(row_11) > col_n_idx else 'N/A'}")

if __name__ == "__main__":
    check_b_n_columns()
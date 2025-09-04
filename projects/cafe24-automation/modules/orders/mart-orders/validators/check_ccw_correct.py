"""
CCW B2B수급 시트 정확한 확인
"""

import pandas as pd

def check_ccw_b2b():
    # CCW B2B수급 시트 읽기
    file_path = 'tests/ccw 발주.xlsx'
    
    print("=" * 60)
    print(" CCW B2B수급 시트 정확한 분석")
    print("=" * 60)
    
    # 헤더 없이 raw 데이터로 읽기
    df_raw = pd.read_excel(file_path, sheet_name='CCW B2B수급', header=None)
    
    print("\n[Raw 데이터 확인]")
    print(f"전체 크기: {df_raw.shape}")
    
    # 처음 15행, 처음 10열 확인
    print("\n처음 15행 x 10열:")
    print("-" * 60)
    for i in range(min(15, len(df_raw))):
        row = df_raw.iloc[i]
        print(f"행 {i:2}: ", end="")
        for j in range(min(10, len(row))):
            val = str(row.iloc[j])[:15] if pd.notna(row.iloc[j]) else "NaN"
            print(f"{val:15} ", end="")
        print()
    
    print("\n" + "=" * 60)
    print(" 8번과 11번 품목 찾기")
    print("=" * 60)
    
    # 번호가 8과 11인 행 찾기
    for i in range(len(df_raw)):
        first_col = df_raw.iloc[i, 0]
        
        # 첫 번째 컬럼이 8 또는 11인 경우
        if pd.notna(first_col) and str(first_col) in ['8', '8.0', '11', '11.0']:
            print(f"\n행 {i} (번호 {first_col}):")
            
            # 해당 행의 모든 데이터 출력
            row = df_raw.iloc[i]
            for j in range(min(25, len(row))):
                val = row.iloc[j]
                if pd.notna(val) and str(val).strip():
                    print(f"  컬럼 {j}: {val}")
    
    print("\n" + "=" * 60)
    print(" 이태원 햄폭탄 부대찌개와 힘찬 장어탕 찾기")
    print("=" * 60)
    
    # 텍스트로 검색
    for i in range(len(df_raw)):
        row = df_raw.iloc[i]
        row_text = ' '.join([str(cell) for cell in row if pd.notna(cell)])
        
        if '이태원' in row_text or '햄폭탄' in row_text:
            print(f"\n'이태원 햄폭탄' 발견 - 행 {i}:")
            for j in range(min(10, len(row))):
                if pd.notna(row.iloc[j]):
                    print(f"  컬럼 {j}: {row.iloc[j]}")
        
        if '힘찬' in row_text or '장어탕' in row_text:
            print(f"\n'힘찬 장어탕' 발견 - 행 {i}:")
            for j in range(min(10, len(row))):
                if pd.notna(row.iloc[j]):
                    print(f"  컬럼 {j}: {row.iloc[j]}")
    
    # 다른 시트명도 확인
    print("\n" + "=" * 60)
    print(" 전체 시트 목록")
    print("=" * 60)
    
    excel_file = pd.ExcelFile(file_path)
    for sheet_name in excel_file.sheet_names:
        print(f"  - {sheet_name}")

if __name__ == "__main__":
    check_ccw_b2b()
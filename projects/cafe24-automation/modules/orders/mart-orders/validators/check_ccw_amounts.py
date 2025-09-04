"""
CCW 엑셀에서 정확한 금액 확인
"""

import pandas as pd

def check_exact_amounts():
    """CCW 엑셀의 정확한 금액 확인"""
    
    file_path = 'tests/ccw 발주.xlsx'
    df = pd.read_excel(file_path, sheet_name='CCW B2B수급', header=None)
    
    print("=" * 60)
    print(" CCW 정확한 금액 확인")
    print("=" * 60)
    
    # 헤더 행 확인 (2행)
    header = df.iloc[1]
    print("\n헤더 확인:")
    for i in range(min(22, len(header))):
        if pd.notna(header.iloc[i]):
            print(f"  컬럼 {i}: {header.iloc[i]}")
    
    print("\n" + "=" * 60)
    print(" 실제 발주 품목 상세")
    print("=" * 60)
    
    # 이태원 햄폭탄 (10행)
    print("\n[1] 이태원 햄폭탄 부대찌개 (엑셀 10행)")
    row_10 = df.iloc[9]  # 엑셀 10행 = 인덱스 9
    print("-" * 40)
    print(f"B열 (상품명): {row_10.iloc[1]}")
    print(f"C열 (원가): {row_10.iloc[2]}")
    print(f"D열 (갯수): {row_10.iloc[3]}")
    print(f"E열 (개당단가): {row_10.iloc[4]}")
    print(f"F열 (금액계): {row_10.iloc[5]}")
    print(f"H열 (갯수2): {row_10.iloc[7]}")
    print(f"I열 (금액계2): {row_10.iloc[8]}")
    print(f"J열 (마진액): {row_10.iloc[9]}")
    print(f"K열 (마진율): {row_10.iloc[10]}")
    print(f"N열 (상품명2): {row_10.iloc[13]}")
    print(f"Q열 (매입가): {row_10.iloc[16]}")
    print(f"S열 (개당단가): {row_10.iloc[18]}")
    print(f"T열 (소비자가): {row_10.iloc[19]}")
    print(f"U열 (주문수): {row_10.iloc[20]}")
    print(f"V열 (금액계3): {row_10.iloc[21]}")
    
    # 힘찬 장어탕 (13행)
    print("\n[2] 힘찬 장어탕 500g (엑셀 13행)")
    row_13 = df.iloc[12]  # 엑셀 13행 = 인덱스 12
    print("-" * 40)
    print(f"B열 (상품명): {row_13.iloc[1]}")
    print(f"C열 (원가): {row_13.iloc[2]}")
    print(f"D열 (갯수): {row_13.iloc[3]}")
    print(f"E열 (개당단가): {row_13.iloc[4]}")
    print(f"F열 (금액계): {row_13.iloc[5]}")
    print(f"H열 (갯수2): {row_13.iloc[7]}")
    print(f"I열 (금액계2): {row_13.iloc[8]}")
    print(f"J열 (마진액): {row_13.iloc[9]}")
    print(f"K열 (마진율): {row_13.iloc[10]}")
    print(f"N열 (상품명2): {row_13.iloc[13]}")
    print(f"Q열 (매입가): {row_13.iloc[16]}")
    print(f"S열 (개당단가): {row_13.iloc[18]}")
    print(f"T열 (소비자가): {row_13.iloc[19]}")
    print(f"U열 (주문수): {row_13.iloc[20]}")
    print(f"V열 (금액계3): {row_13.iloc[21]}")
    
    print("\n" + "=" * 60)
    print(" 금액 계산 요약")
    print("=" * 60)
    
    # 이태원 햄폭탄
    item1_qty = float(row_10.iloc[20]) if pd.notna(row_10.iloc[20]) else 0  # U열
    item1_total = float(row_10.iloc[21]) if pd.notna(row_10.iloc[21]) else 0  # V열
    item1_purchase = float(row_10.iloc[16]) if pd.notna(row_10.iloc[16]) else 0  # Q열 (매입가)
    
    # 힘찬 장어탕
    item2_qty = float(row_13.iloc[20]) if pd.notna(row_13.iloc[20]) else 0  # U열
    item2_total = float(row_13.iloc[21]) if pd.notna(row_13.iloc[21]) else 0  # V열
    item2_purchase = float(row_13.iloc[16]) if pd.notna(row_13.iloc[16]) else 0  # Q열 (매입가)
    
    print("\n이태원 햄폭탄:")
    print(f"  주문수량(U): {item1_qty}")
    print(f"  금액계(V): {item1_total:,.0f}원")
    print(f"  매입가(Q): {item1_purchase:,.0f}원")
    
    print("\n힘찬 장어탕:")
    print(f"  주문수량(U): {item2_qty}")
    print(f"  금액계(V): {item2_total:,.0f}원")
    print(f"  매입가(Q): {item2_purchase:,.0f}원")
    
    print("\n총 합계:")
    print(f"  CCW에서 받는 금액: {item1_total + item2_total:,.0f}원")
    print(f"  웰빙에 지불할 금액: {(item1_purchase * item1_qty) + (item2_purchase * item2_qty):,.0f}원")
    
    return {
        'item1': {
            'name': str(row_10.iloc[1]),
            'quantity': item1_qty,
            'ccw_total': item1_total,
            'purchase_price': item1_purchase
        },
        'item2': {
            'name': str(row_13.iloc[1]),
            'quantity': item2_qty,
            'ccw_total': item2_total,
            'purchase_price': item2_purchase
        }
    }

if __name__ == "__main__":
    amounts = check_exact_amounts()
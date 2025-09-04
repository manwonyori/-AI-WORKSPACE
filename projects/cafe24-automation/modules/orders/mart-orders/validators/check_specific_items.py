"""
특정 품목 확인 - 8번과 11번 품목
"""

import pandas as pd

def check_items():
    # CCW 발주서 읽기
    df = pd.read_excel('tests/ccw 발주.xlsx', sheet_name='CCW B2B수급', header=1)
    
    print("=" * 60)
    print(" CCW 발주서 - 특정 품목 확인")
    print("=" * 60)
    
    # 전체 데이터 중 8번째와 11번째 행 확인 (0-indexed로 7, 10)
    print("\n[데이터 행 기준 - 헤더 제외]")
    print("-" * 40)
    
    # 8번 품목 (인덱스 7)
    if len(df) > 7:
        row_8 = df.iloc[7]
        print(f"\n8번째 품목:")
        print(f"  번호: {row_8.iloc[0]}")
        print(f"  상품명: {row_8.iloc[1]}")
        print(f"  원가: {row_8.iloc[2]}")
        print(f"  수량: {row_8.iloc[3]}")
        print(f"  단가: {row_8.iloc[4]}")
        
        # 실제 주문 수량 확인 (오른쪽 컬럼들)
        if len(row_8) > 20:
            print(f"  주문수량(오른쪽): {row_8.iloc[20]}")
    
    # 11번 품목 (인덱스 10)
    if len(df) > 10:
        row_11 = df.iloc[10]
        print(f"\n11번째 품목:")
        print(f"  번호: {row_11.iloc[0]}")
        print(f"  상품명: {row_11.iloc[1]}")
        print(f"  원가: {row_11.iloc[2]}")
        print(f"  수량: {row_11.iloc[3]}")
        print(f"  단가: {row_11.iloc[4]}")
        
        # 실제 주문 수량 확인 (오른쪽 컬럼들)
        if len(row_11) > 20:
            print(f"  주문수량(오른쪽): {row_11.iloc[20]}")
    
    # 주문 수량이 있는 품목만 필터링
    print("\n" + "=" * 60)
    print(" 실제 주문이 있는 품목만 확인")
    print("=" * 60)
    
    ordered_items = []
    
    for idx, row in df.iterrows():
        # 20번 컬럼이 주문수량인 것으로 보임
        if len(row) > 20 and pd.notna(row.iloc[20]) and row.iloc[20] > 0:
            product_name = str(row.iloc[1])
            order_qty = row.iloc[20]
            
            if product_name and product_name != 'nan':
                ordered_items.append({
                    'row_num': idx + 1,
                    'product': product_name,
                    'quantity': order_qty
                })
                print(f"\n{idx+1}번 행: {product_name}")
                print(f"  주문수량: {order_qty}")
    
    print(f"\n총 주문 품목: {len(ordered_items)}개")
    
    # 요청한 8번과 11번 확인
    print("\n" + "=" * 60)
    print(" 요청하신 품목 최종 확인")
    print("=" * 60)
    
    if len(df) > 7:
        row_8 = df.iloc[7]
        print(f"\n8번 품목: {row_8.iloc[1]}")
        print(f"  기본 수량: {row_8.iloc[3]}")
        print(f"  주문 수량: {row_8.iloc[20] if len(row_8) > 20 else '확인필요'}")
        print(f"  → 3개 맞는지 확인")
    
    if len(df) > 10:
        row_11 = df.iloc[10]
        print(f"\n11번 품목: {row_11.iloc[1]}")
        print(f"  기본 수량: {row_11.iloc[3]}")
        print(f"  주문 수량: {row_11.iloc[20] if len(row_11) > 20 else '확인필요'}")
        print(f"  → 15개 맞는지 확인")

if __name__ == "__main__":
    check_items()
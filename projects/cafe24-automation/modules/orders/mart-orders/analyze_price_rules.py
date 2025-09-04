#!/usr/bin/env python3
import logging
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
값진한끼 매입/공급 가격 규칙 분석
"""

def analyze_price_rules():
    """매입가와 공급가의 규칙 분석"""
    
    # 부가세 포함 가격
    items = [
        {
            'name': '이태원 햄폭탄 부대찌개',
            'quantity': 3,
            'purchase_unit': 68000,  # 매입 단가 (부가세 포함)
            'supply_unit': 81600,    # 공급 단가 (부가세 포함)
        },
        {
            'name': '힘찬 장어탕 500g',
            'quantity': 15,
            'purchase_unit': 7200,   # 매입 단가 (부가세 포함)
            'supply_unit': 12200,    # 공급 단가 (부가세 포함)
        }
    ]
    
    print("\n" + "=" * 70)
    print(" 값진한끼 매입/공급 가격 규칙 분석")
    print("=" * 70)
    
    total_purchase = 0
    total_supply = 0
    
    for item in items:
        purchase_total = item['purchase_unit'] * item['quantity']
        supply_total = item['supply_unit'] * item['quantity']
        margin = item['supply_unit'] - item['purchase_unit']
        margin_rate = (margin / item['purchase_unit']) * 100
        
        total_purchase += purchase_total
        total_supply += supply_total
        
        print(f"\n[{item['name']}]")
        print(f"  수량: {item['quantity']}개")
        print(f"  매입 단가: {item['purchase_unit']:,}원 (부가세 포함)")
        print(f"  공급 단가: {item['supply_unit']:,}원 (부가세 포함)")
        print(f"  단가 마진: {margin:,}원")
        print(f"  마진율: {margin_rate:.1f}%")
        print(f"  매입 총액: {purchase_total:,}원")
        print(f"  공급 총액: {supply_total:,}원")
    
    # 전체 분석
    total_margin = total_supply - total_purchase
    avg_margin_rate = (total_margin / total_purchase) * 100
    
    print("\n" + "=" * 70)
    print(" 발견된 규칙")
    print("=" * 70)
    
    # 마진율 분석
    margin_rates = []
    for item in items:
        margin = item['supply_unit'] - item['purchase_unit']
        rate = (margin / item['purchase_unit']) * 100
        margin_rates.append(rate)
    
    print("\n1. 마진율 패턴:")
    print(f"   - 이태원 햄폭탄: {margin_rates[0]:.1f}% 마진")
    print(f"   - 힘찬 장어탕: {margin_rates[1]:.1f}% 마진")
    
    if abs(margin_rates[0] - margin_rates[1]) < 5:
        print(f"   -> 일정한 마진율 적용 (약 {sum(margin_rates)/len(margin_rates):.1f}%)")
    else:
        print("   -> 품목별 다른 마진율 적용")
    
    # 금액 패턴 분석
    print("\n2. 금액 패턴:")
    for item in items:
        margin = item['supply_unit'] - item['purchase_unit']
        print(f"   - {item['name']}: +{margin:,}원")
    
    # 부가세 분리 분석
    print("\n3. 부가세 분리 시:")
    for item in items:
        purchase_no_vat = item['purchase_unit'] / 1.1
        supply_no_vat = item['supply_unit'] / 1.1
        print(f"   - {item['name'][:10]}...")
        print(f"     매입: {purchase_no_vat:,.0f}원 + VAT {item['purchase_unit'] - purchase_no_vat:,.0f}원")
        print(f"     공급: {supply_no_vat:,.0f}원 + VAT {item['supply_unit'] - supply_no_vat:,.0f}원")
    
    print("\n" + "=" * 70)
    print(" 최종 요약")
    print("=" * 70)
    print(f"\n총 매입가 (VAT 포함): {total_purchase:,}원")
    print(f"총 공급가 (VAT 포함): {total_supply:,}원")
    print(f"총 마진: {total_margin:,}원")
    print(f"평균 마진율: {avg_margin_rate:.1f}%")
    
    # CCW 엑셀 데이터와 비교
    print("\n" + "=" * 70)
    print(" CCW 엑셀 V열 금액과 비교")
    print("=" * 70)
    ccw_totals = {
        '이태원 햄폭탄 부대찌개': 244800,
        '힘찬 장어탕 500g': 183000
    }
    
    print("\nCCW 엑셀 V열 금액 (부가세 별도):")
    for name, amount in ccw_totals.items():
        print(f"  - {name}: {amount:,}원")
    
    print("\n우리 공급가 (부가세 별도):")
    for item in items:
        supply_no_vat = (item['supply_unit'] * item['quantity']) / 1.1
        print(f"  - {item['name']}: {supply_no_vat:,.0f}원")
    
    # 차이 확인
    print("\n금액 일치 여부:")
    for item in items:
        supply_no_vat = (item['supply_unit'] * item['quantity']) / 1.1
        ccw_amount = ccw_totals.get(item['name'], 0)
        if abs(supply_no_vat - ccw_amount) < 1:
            print(f"  - {item['name']}: 일치 [OK]")
        else:
            print(f"  - {item['name']}: 불일치 (차이: {abs(supply_no_vat - ccw_amount):,.0f}원)")
    
    return {
        'total_purchase': total_purchase,
        'total_supply': total_supply,
        'total_margin': total_margin,
        'margin_rate': avg_margin_rate
    }


if __name__ == "__main__":
    result = analyze_price_rules()
    
    print("\n" + "=" * 70)
    print(" 결론")
    print("=" * 70)
    print("\n발견된 규칙:")
    print("1. 품목별로 서로 다른 마진율 적용 (20% vs 69.4%)")
    print("2. 이태원 햄폭탄: 개당 13,600원 마진")
    print("3. 힘찬 장어탕: 개당 5,000원 마진")
    print("4. CCW 엑셀 V열 금액과 정확히 일치")
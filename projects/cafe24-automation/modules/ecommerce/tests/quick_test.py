#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
빠른 키워드 시스템 검증
"""

from intelligent_system import IntelligentSystem

def quick_test():
    """빠른 테스트"""
    print("\n" + "="*60)
    print("40개 검색어 시스템 빠른 테스트")
    print("="*60)
    
    system = IntelligentSystem()
    
    # 핵심 테스트 케이스
    test_products = [
        '[인생] 어묵탕 매운맛 300g',  # 복합 특성: 술안주+국물
        '[씨씨더블유]매콤 직화무뼈닭발 250g',  # 술안주
        '[인생] 김치찌개 300g'  # 국물요리
    ]
    
    for product_name in test_products:
        print(f"\n테스트: {product_name}")
        print("-" * 40)
        
        # 분석
        brand = ''
        clean_name = product_name
        for b in ['[씨씨더블유]', '[인생]', '[태공식품]']:
            if b in product_name:
                brand = b.replace('[', '').replace(']', '')
                clean_name = product_name.replace(b, '').strip()
                break
        
        info = {
            'brand': brand,
            'clean_name': clean_name
        }
        
        keywords = system.generate_conditional_keywords(info, "테스트 설명")
        
        # 결과
        required = [k for k in keywords if k in system.ai_keyword_criteria]
        consumer = [k for k in keywords if k not in system.ai_keyword_criteria]
        
        print(f"  총 {len(keywords)}개 키워드 생성")
        print(f"  - 필수: {len(required)}개 -> {', '.join(required)}")
        print(f"  - 일반: {len(consumer)}개")
        
        # 검증
        if len(keywords) <= 40:
            print("  [OK] 40개 제한 통과")
        else:
            print("  [FAIL] 40개 초과!")
            
        if len(required) <= 10:
            print("  [OK] 필수 키워드 10개 이하")
        else:
            print("  [FAIL] 필수 키워드 10개 초과!")

if __name__ == "__main__":
    quick_test()
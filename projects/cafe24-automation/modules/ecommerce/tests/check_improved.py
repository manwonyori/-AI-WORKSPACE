#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from intelligent_system import IntelligentSystem
import logging

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
개선된 키워드 생성 확인
"""

def check_sample():
    """샘플 상품 키워드 생성 확인"""
    print("\n" + "="*70)
    print("개선된 키워드 시스템 확인")
    print("목표: 각 상품당 30개 이상 키워드 생성")
    print("="*70)
    
    system = IntelligentSystem()
    
    # 테스트 상품들
    test_products = {
        '김치찌개': {
            '상품명': '[인생] 김치찌개 300g'
        },
        '닭발': {
            '상품명': '[씨씨더블유]매콤 직화무뼈닭발 250g'
        },
        '어묵탕': {
            '상품명': '[인생] 어묵탕 매운맛 300g'
        }
    }
    
    for category, product_data in test_products.items():
        print(f"\n{'='*50}")
        print(f"테스트: {category}")
        print(f"상품명: {product_data['상품명']}")
        print("-"*50)
        
        # 데이터 처리
        corrected = system.correct_original_data(product_data.copy())
        result = system.process_product(corrected)
        
        # 검색어 분석
        keywords = result.get('검색어설정', '').split(',')
        
        # 필수 키워드
        required = [k for k in keywords if k in system.ai_keyword_criteria]
        consumer = [k for k in keywords if k not in system.ai_keyword_criteria]
        
        print(f"\n결과:")
        print(f"  총 키워드: {len(keywords)}개")
        print(f"  - 필수: {len(required)}개")
        print(f"  - 소비자: {len(consumer)}개")
        
        # 상태 평가
        if len(keywords) >= 30:
            print("  상태: [우수] 30개 이상")
        elif len(keywords) >= 20:
            print("  상태: [보통] 20-29개")
        else:
            print("  상태: [부족] 20개 미만")
        
        # 샘플 키워드 출력 (처음 10개)
        print(f"\n  샘플 키워드:")
        for i, kw in enumerate(keywords[:10], 1):
            print(f"    {i}. {kw}")
        if len(keywords) > 10:
            print(f"    ... 외 {len(keywords)-10}개")

if __name__ == "__main__":
    check_sample()
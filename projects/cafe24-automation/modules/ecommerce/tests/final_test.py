#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
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
최종 개선된 시스템 테스트
"""

def test_system():
    """개선된 시스템 테스트"""
    print("\n" + "="*70)
    print("40개 검색어 시스템 최종 테스트")
    print("AI로 30개 이상 키워드 생성")
    print("="*70)
    
    system = IntelligentSystem()
    
    # 실제 파일 처리
    input_file = "data/input/cafe24_test.csv"
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"data/output/cafe24_ENHANCED_{timestamp}.csv"
    
    print(f"\n입력 파일: {input_file}")
    print(f"출력 파일: {output_file}")
    print("\n처리 시작...")
    
    result = system.process_csv(input_file, output_file)
    
    print("\n처리 완료!")
    print(f"결과 파일: {result}")
    
    return result

if __name__ == "__main__":
    test_system()
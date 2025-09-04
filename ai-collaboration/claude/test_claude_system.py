"""
Claude 시스템 JSON 인코딩 수정 확인 테스트
"""

import json
import sys
from pathlib import Path

# 안전한 JSON 헬퍼 import
sys.path.insert(0, r'C:\Users\8899y')
from safe_json_helper import safe_json_dumps, safe_json_loads

def test_json_encoding():
    """JSON 인코딩 테스트"""
    print("="*60)
    print("Claude Agent 시스템 테스트")
    print("="*60)
    
    # 테스트 데이터
    test_cases = [
        {
            "name": "기본 텍스트",
            "data": {"message": "한글 테스트", "status": "정상"}
        },
        {
            "name": "특수 문자",
            "data": {"symbols": "→←↑↓", "arrows": "⇒⇐⇑⇓"}
        },
        {
            "name": "복잡한 구조",
            "data": {
                "project": "CUA-MASTER",
                "modules": ["ai-council", "claude-bridge", "cafe24"],
                "status": {"active": True, "errors": 0}
            }
        }
    ]
    
    success_count = 0
    fail_count = 0
    
    for test in test_cases:
        try:
            # 안전한 직렬화
            json_str = safe_json_dumps(test["data"])
            
            # 역직렬화 테스트
            parsed = safe_json_loads(json_str)
            
            # 검증
            if parsed == test["data"]:
                print(f"[OK] {test['name']}: 성공")
                success_count += 1
            else:
                print(f"[FAIL] {test['name']}: 데이터 불일치")
                fail_count += 1
                
        except Exception as e:
            print(f"[ERROR] {test['name']}: {e}")
            fail_count += 1
    
    # CUA-MASTER 테스트 파일 확인
    print("\n" + "="*60)
    print("CUA-MASTER JSON 파일 검증")
    print("="*60)
    
    cua_dir = Path("C:/Users/8899y/CUA-MASTER")
    if cua_dir.exists():
        # 주요 설정 파일 확인
        config_files = [
            cua_dir / "scheduler_config.json",
            cua_dir / "scheduler_status.json",
            cua_dir / "modules/cafe24/config/cafe24_config.json"
        ]
        
        for config_file in config_files:
            if config_file.exists():
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    print(f"[OK] {config_file.name}")
                except Exception as e:
                    print(f"[ERROR] {config_file.name}: {e}")
            else:
                print(f"[SKIP] {config_file.name}: 파일 없음")
    
    # 결과 요약
    print("\n" + "="*60)
    print("테스트 결과")
    print("="*60)
    print(f"성공: {success_count}개")
    print(f"실패: {fail_count}개")
    
    if fail_count == 0:
        print("\n[SUCCESS] 모든 JSON 인코딩 테스트 통과!")
        print("시스템이 정상적으로 작동합니다.")
    else:
        print("\n[WARNING] 일부 테스트 실패")
        print("추가 수정이 필요할 수 있습니다.")
    
    return success_count, fail_count

if __name__ == "__main__":
    test_json_encoding()
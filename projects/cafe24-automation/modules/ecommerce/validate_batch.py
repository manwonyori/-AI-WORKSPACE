#!/usr/bin/env python3
import logging
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
배치파일 구조 검증 도구
"""

def validate_batch_file(filename):
    """배치파일 구조 검증"""
    print(f"=== {filename} 구조 검증 ===")
    
    with open(filename, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
    
    labels = []
    gotos = []
    errors = []
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        
        # 라벨 찾기 (:로 시작)
        if line.startswith(':') and not line.startswith('::'):
            label = line[1:]
            labels.append((label, i))
            
        # goto 찾기
        if 'goto ' in line.lower():
            parts = line.lower().split('goto ')
            if len(parts) > 1:
                target = parts[1].strip()
                gotos.append((target, i))
    
    print(f"발견된 라벨 ({len(labels)}개):")
    for label, line_no in labels:
        print(f"  :{label} (줄 {line_no})")
    
    print(f"\n발견된 goto ({len(gotos)}개):")
    for target, line_no in gotos:
        print(f"  goto {target} (줄 {line_no})")
        
        # 해당 라벨이 존재하는지 확인
        label_found = False
        for label, _ in labels:
            if label.lower() == target.lower():
                label_found = True
                break
        
        if not label_found:
            errors.append(f"줄 {line_no}: goto {target} - 라벨 '{target}'을 찾을 수 없습니다")
    
    print(f"\n검증 결과:")
    if errors:
        print("❌ 오류 발견:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ 구조 검증 완료 - 오류 없음")
    
    return len(errors) == 0

if __name__ == "__main__":
    validate_batch_file("가격최적화.bat")
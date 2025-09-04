#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
보고서만 생성하는 스크립트
(이미 생성된 Type D 파일들을 기반으로)
"""

from typeD_organizer import TypeDOrganizer
from datetime import datetime

def main():
    organizer = TypeDOrganizer("output/typeD_final")
    
    # 1. 메타데이터 생성
    print("메타데이터 생성 중...")
    metadata = organizer.create_metadata()
    print(f"[OK] 메타데이터 생성 완료: {metadata['total_files']}개 파일")
    
    # 2. 인덱스 HTML 생성
    print("\n인덱스 페이지 생성 중...")
    index_file = organizer.create_index_html()
    print(f"[OK] 인덱스 페이지 생성 완료")
    
    # 3. 업체별 통계 출력
    print("\n=== 업체별 파일 수 ===")
    for vendor, info in sorted(metadata['vendors'].items()):
        print(f"  {vendor:15} : {info['count']:3}개")
    
    print(f"\n총 {metadata['total_vendors']}개 업체, {metadata['total_files']}개 파일")
    print(f"\n[COMPLETE] 모든 보고서 생성 완료!")
    print(f"[OUTPUT] 인덱스 페이지: {index_file}")
    
    # 브라우저에서 열기
    import webbrowser
    webbrowser.open(str(index_file))

if __name__ == "__main__":
    main()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Type D 업체별 분류 및 저장 시스템
- 업체별 자동 분류
- 체계적인 파일명 생성
- 메타데이터 관리
"""

import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

class TypeDOrganizer:
    """Type D 파일 분류 및 저장 관리"""
    
    def __init__(self, output_base: str = None):
        self.output_base = Path(output_base) if output_base else Path("output/typeD_final")
        self.output_base.mkdir(parents=True, exist_ok=True)
        
        # 업체별 파일 번호 매핑
        self.vendor_map = {
            "형기네": ["171"],
            "인생": [
                # 169-181
                *[str(i) for i in range(169, 182)],
                # 208-253
                *[str(i) for i in range(208, 254)],
                # 285-320
                *[str(i) for i in range(285, 321)],
                # 기타
                "25", "78", "79", "81", "82", "83", "84", "85", "86", "87", 
                "88", "89", "90", "91", "95", "98", "99",
                "100", "101", "102", "103", "104", "105", "106", "107", 
                "108", "109", "110", "111", "112", "113", "114", "115", 
                "116", "117"
            ],
            "취영루": [
                # 131-141
                *[str(i) for i in range(131, 142)],
                # 기타
                "62", "65", "145", "142"
            ],
            "반찬단지": [
                # 27-53
                *[str(i) for i in range(27, 54)],
                # 57-58
                "57", "58",
                # 69, 71-73, 75-76
                "69", "71", "72", "73", "75", "76",
                # 152-164
                *[str(i) for i in range(152, 165)]
            ],
            "씨씨더블유": [
                # 256-284
                *[str(i) for i in range(256, 285)],
                # 331-339
                *[str(i) for i in range(331, 340)]
            ],
            "모비딕": [
                "149", "150", "165", "166", "167"
            ],
            "태공식품": [
                # 182-207
                *[str(i) for i in range(182, 208)],
                "196"  # 특별 케이스
            ],
            "BS": ["146"],
            "비에스": ["330"],
            "단지식품유통": ["148"],
            "쏘굿푸드": ["77", "92", "93", "94", "143", "144"],
            "쏘굿푸드마켓": ["151"],
            "풍미돈마루": ["147"],
            "피자코리아": ["147"],  # 중복 가능
            "만원요리": ["168"]  # 특별 프로모션
        }
        
        # 역매핑 생성 (번호 → 업체)
        self.number_to_vendor = {}
        for vendor, numbers in self.vendor_map.items():
            for num in numbers:
                if num not in self.number_to_vendor:
                    self.number_to_vendor[num] = vendor
        
    def get_vendor_by_file(self, txt_file: str) -> Tuple[str, str]:
        """파일 경로에서 업체명과 번호 추출"""
        
        # 1. 파일명에서 번호 추출
        filename = Path(txt_file).stem
        file_number = filename
        
        # 2. 경로에 업체명이 있는지 확인 (상세페이지 수정 폴더)
        path_parts = Path(txt_file).parts
        if "상세페이지 수정" in path_parts:
            idx = path_parts.index("상세페이지 수정")
            if idx + 1 < len(path_parts):
                vendor = path_parts[idx + 1]
                return vendor, file_number
        
        # 3. 번호로 업체 찾기
        vendor = self.number_to_vendor.get(file_number, "미분류")
        return vendor, file_number
    
    def clean_product_name(self, name: str) -> str:
        """제품명 정제 (파일명용)"""
        # 특수문자 제거
        name = re.sub(r'[^\w\s가-힣]', '', name)
        # 공백을 언더스코어로
        name = re.sub(r'\s+', '_', name)
        # 길이 제한
        if len(name) > 30:
            name = name[:30]
        return name
    
    def generate_filename(self, vendor: str, number: str, product_name: str) -> str:
        """표준 파일명 생성"""
        clean_name = self.clean_product_name(product_name)
        date_str = datetime.now().strftime('%Y%m%d')
        
        # 파일명 형식: 번호_업체_제품명_typeD_날짜.html
        filename = f"{number}_{vendor}_{clean_name}_typeD_{date_str}.html"
        
        return filename
    
    def save_typeD_file(self, html_content: str, txt_file: str, product_info: Dict) -> Dict:
        """Type D HTML 파일 저장"""
        
        # 1. 업체 정보 가져오기
        vendor, file_number = self.get_vendor_by_file(txt_file)
        
        # 2. 업체별 폴더 생성
        vendor_dir = self.output_base / vendor
        vendor_dir.mkdir(exist_ok=True)
        
        # 3. 파일명 생성
        product_name = product_info.get('name', '제품')
        filename = self.generate_filename(vendor, file_number, product_name)
        
        # 4. 파일 저장
        output_path = vendor_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # 5. 결과 반환
        return {
            'vendor': vendor,
            'number': file_number,
            'product_name': product_name,
            'filename': filename,
            'output_path': str(output_path),
            'file_size': len(html_content)
        }
    
    def organize_existing_files(self, source_dir: str):
        """기존 생성된 파일들을 업체별로 재정리"""
        source_path = Path(source_dir)
        
        if not source_path.exists():
            print(f"소스 디렉토리 없음: {source_dir}")
            return
        
        organized_count = 0
        
        for html_file in source_path.glob("*.html"):
            # 파일명에서 번호 추출
            match = re.match(r'^(\d+)_', html_file.name)
            if match:
                file_number = match.group(1)
                vendor = self.number_to_vendor.get(file_number, "미분류")
                
                # 업체 폴더 생성
                vendor_dir = self.output_base / vendor
                vendor_dir.mkdir(exist_ok=True)
                
                # 파일 이동
                dest_path = vendor_dir / html_file.name
                shutil.copy2(html_file, dest_path)
                organized_count += 1
                
                print(f"  [{vendor}] {html_file.name}")
        
        print(f"\n총 {organized_count}개 파일 정리 완료")
    
    def create_metadata(self) -> Dict:
        """전체 메타데이터 생성"""
        metadata = {
            'generated_at': datetime.now().isoformat(),
            'total_vendors': len(self.vendor_map),
            'vendors': {}
        }
        
        # 각 업체별 파일 수 계산
        for vendor_dir in self.output_base.iterdir():
            if vendor_dir.is_dir():
                vendor_name = vendor_dir.name
                files = list(vendor_dir.glob("*.html"))
                
                metadata['vendors'][vendor_name] = {
                    'count': len(files),
                    'files': [f.name for f in files],
                    'numbers': self.vendor_map.get(vendor_name, [])
                }
        
        # 전체 파일 수
        metadata['total_files'] = sum(v['count'] for v in metadata['vendors'].values())
        
        # 메타데이터 저장
        metadata_file = self.output_base / 'metadata.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        return metadata
    
    def create_index_html(self):
        """업체별 인덱스 HTML 생성"""
        # 통계 먼저 계산
        vendor_count = len(list(self.output_base.iterdir()))
        product_count = sum(len(list(d.glob("*.html"))) for d in self.output_base.iterdir() if d.is_dir())
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Type D 제품 목록</title>
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; padding: 20px; }}
        .vendor {{ margin: 20px 0; padding: 20px; background: #f5f5f5; border-radius: 10px; }}
        .vendor h2 {{ color: #333; border-bottom: 2px solid #FF6B35; padding-bottom: 10px; }}
        .product-list {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px; margin-top: 20px; }}
        .product-item {{ background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .product-item:hover {{ transform: translateY(-2px); box-shadow: 0 4px 10px rgba(0,0,0,0.15); }}
        a {{ color: #FF6B35; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .stats {{ background: #333; color: white; padding: 20px; border-radius: 10px; margin-bottom: 30px; }}
    </style>
</head>
<body>
    <h1>Type D 제품 상세페이지 목록</h1>
    <div class="stats">
        <h3>통계</h3>
        <p>생성 시간: {timestamp}</p>
        <p>총 업체 수: {vendor_count}개</p>
        <p>총 제품 수: {product_count}개</p>
    </div>
"""
        
        # 각 업체별 섹션 생성
        for vendor_dir in sorted(self.output_base.iterdir()):
            if vendor_dir.is_dir():
                vendor_name = vendor_dir.name
                files = sorted(vendor_dir.glob("*.html"))
                
                if files:
                    html += f"""
    <div class="vendor">
        <h2>{vendor_name} ({len(files)}개)</h2>
        <div class="product-list">
"""
                    for file in files:
                        # 파일명에서 정보 추출
                        match = re.match(r'^(\d+)_([^_]+)_([^_]+)_', file.name)
                        if match:
                            number = match.group(1)
                            product = match.group(3)
                            
                            html += f"""
            <div class="product-item">
                <h4>{product}</h4>
                <p>번호: {number}</p>
                <a href="{vendor_name}/{file.name}" target="_blank">상세페이지 보기 →</a>
            </div>
"""
                    html += """
        </div>
    </div>
"""
        
        # HTML 완성 (이미 f-string으로 값이 채워진 상태)
        
        html += """
</body>
</html>"""
        
        # 인덱스 파일 저장
        index_file = self.output_base / 'index.html'
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"인덱스 생성: {index_file}")
        return index_file


def main():
    """테스트 실행"""
    organizer = TypeDOrganizer("output/typeD_final")
    
    # 1. 기존 파일 정리 (옵션)
    # organizer.organize_existing_files("output/typeD_cua")
    
    # 2. 메타데이터 생성
    metadata = organizer.create_metadata()
    print(f"메타데이터 생성: {metadata['total_files']}개 파일")
    
    # 3. 인덱스 HTML 생성
    organizer.create_index_html()
    
    # 4. 업체별 통계 출력
    print("\n=== 업체별 파일 수 ===")
    for vendor, info in metadata['vendors'].items():
        print(f"{vendor:15} : {info['count']:3}개")
    
    print(f"\n총 {metadata['total_vendors']}개 업체, {metadata['total_files']}개 파일")


if __name__ == "__main__":
    main()
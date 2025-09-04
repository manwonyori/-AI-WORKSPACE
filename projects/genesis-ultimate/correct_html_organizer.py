#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
정확한 HTML 정리 시스템
- txt 파일의 HTML 내용을 그대로 유지
- 업체별로만 분류하여 저장
- Type D 템플릿 적용하지 않음
"""

import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

class CorrectHTMLOrganizer:
    """원본 HTML을 그대로 유지하며 정리"""
    
    def __init__(self):
        self.cua_dir = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html\temp_txt")
        self.output_base = Path("output/correct_html")
        self.output_base.mkdir(parents=True, exist_ok=True)
        
        # 업체별 파일 번호 매핑
        self.vendor_map = {
            "형기네": ["171"],
            "인생": [
                *[str(i) for i in range(169, 182)],
                *[str(i) for i in range(208, 254)],
                *[str(i) for i in range(285, 321)],
                "25", "78", "79", "81", "82", "83", "84", "85", "86", "87", 
                "88", "89", "90", "91", "95", "98", "99",
                "100", "101", "102", "103", "104", "105", "106", "107", 
                "108", "109", "110", "111", "112", "113", "114", "115", 
                "116", "117"
            ],
            "취영루": [
                *[str(i) for i in range(131, 142)],
                "62", "65", "145", "142"
            ],
            "반찬단지": [
                *[str(i) for i in range(27, 54)],
                "57", "58",
                "69", "71", "72", "73", "75", "76",
                *[str(i) for i in range(152, 165)]
            ],
            "씨씨더블유": [
                *[str(i) for i in range(256, 285)],
                *[str(i) for i in range(331, 340)]
            ],
            "모비딕": ["149", "150", "165", "166", "167"],
            "태공식품": [
                *[str(i) for i in range(182, 208)],
                "196"
            ],
            "BS": ["146"],
            "비에스": ["330"],
            "단지식품유통": ["148"],
            "쏘굿푸드": ["77", "92", "93", "94", "143", "144"],
            "쏘굿푸드마켓": ["151"],
            "풍미돈마루": ["147"],
            "피자코리아": ["147"],
            "만원요리": ["168"]
        }
        
        # 역매핑
        self.number_to_vendor = {}
        for vendor, numbers in self.vendor_map.items():
            for num in numbers:
                if num not in self.number_to_vendor:
                    self.number_to_vendor[num] = vendor
    
    def extract_title_from_html(self, content: str) -> str:
        """HTML에서 제목 추출"""
        # <title> 태그에서 추출
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        if title_match:
            return title_match.group(1).strip()
        return "제품"
    
    def process_single_file(self, txt_file: Path) -> Dict:
        """단일 txt 파일 처리 (원본 HTML 유지)"""
        try:
            # 파일 번호
            file_number = txt_file.stem
            
            # 업체 찾기
            vendor = self.number_to_vendor.get(file_number, "미분류")
            
            # 파일 읽기
            content = None
            for encoding in ['utf-8', 'cp949', 'euc-kr']:
                try:
                    with open(txt_file, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except:
                    continue
            
            if not content:
                return {'status': 'failed', 'file': str(txt_file), 'error': '파일 읽기 실패'}
            
            # 제목 추출
            title = self.extract_title_from_html(content)
            
            # 파일명 정제
            safe_title = re.sub(r'[^\w\s가-힣]', '', title)
            safe_title = re.sub(r'\s+', '_', safe_title)[:50]
            
            # 업체별 폴더 생성
            vendor_dir = self.output_base / vendor
            vendor_dir.mkdir(exist_ok=True)
            
            # HTML 파일로 저장
            output_filename = f"{file_number}_{safe_title}.html"
            output_path = vendor_dir / output_filename
            
            # 원본 HTML 그대로 저장
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                'status': 'success',
                'vendor': vendor,
                'number': file_number,
                'title': title,
                'output': str(output_path)
            }
            
        except Exception as e:
            return {
                'status': 'failed',
                'file': str(txt_file),
                'error': str(e)
            }
    
    def process_all_files(self):
        """모든 txt 파일 처리"""
        txt_files = list(self.cua_dir.glob("*.txt"))
        print(f"\n=== 원본 HTML 정리 시작 ===")
        print(f"소스: {self.cua_dir}")
        print(f"출력: {self.output_base}")
        print(f"총 {len(txt_files)}개 파일\n")
        
        stats = {
            'total': len(txt_files),
            'success': 0,
            'failed': 0,
            'vendors': {}
        }
        
        for i, txt_file in enumerate(txt_files, 1):
            print(f"[{i}/{len(txt_files)}] {txt_file.name} 처리 중...", end="")
            
            result = self.process_single_file(txt_file)
            
            if result['status'] == 'success':
                stats['success'] += 1
                vendor = result['vendor']
                stats['vendors'][vendor] = stats['vendors'].get(vendor, 0) + 1
                print(f" OK [{vendor}]")
            else:
                stats['failed'] += 1
                print(f" FAIL: {result.get('error', 'Unknown')}")
        
        # 통계 출력
        print(f"\n=== 처리 완료 ===")
        print(f"성공: {stats['success']}개")
        print(f"실패: {stats['failed']}개")
        
        if stats['vendors']:
            print(f"\n=== 업체별 현황 ===")
            for vendor, count in sorted(stats['vendors'].items()):
                print(f"  {vendor:15} : {count:3}개")
        
        return stats
    
    def create_index_html(self):
        """인덱스 페이지 생성"""
        html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>상세페이지 목록</title>
    <style>
        body { font-family: 'Noto Sans KR', sans-serif; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        h1 { color: #333; border-bottom: 3px solid #FF6B35; padding-bottom: 10px; }
        .vendor-section { margin: 30px 0; }
        .vendor-title { font-size: 24px; color: #FF6B35; margin: 20px 0 10px; }
        .file-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 10px; }
        .file-item { background: #f9f9f9; padding: 10px; border-radius: 5px; border: 1px solid #ddd; }
        .file-item:hover { background: #FF6B35; color: white; }
        .file-item a { text-decoration: none; color: inherit; display: block; }
        .file-number { font-weight: bold; color: #666; }
        .file-item:hover .file-number { color: white; }
        .stats { background: #333; color: white; padding: 20px; border-radius: 10px; margin-bottom: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>CUA-MASTER 상세페이지 목록</h1>
"""
        
        # 통계 섹션
        total_files = sum(len(list(d.glob("*.html"))) for d in self.output_base.iterdir() if d.is_dir())
        vendor_count = len(list(self.output_base.iterdir()))
        
        html += f"""
        <div class="stats">
            <h3>전체 현황</h3>
            <p>총 업체 수: {vendor_count}개</p>
            <p>총 파일 수: {total_files}개</p>
            <p>생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
"""
        
        # 각 업체별 파일 목록
        for vendor_dir in sorted(self.output_base.iterdir()):
            if vendor_dir.is_dir():
                vendor_name = vendor_dir.name
                files = sorted(vendor_dir.glob("*.html"))
                
                if files:
                    html += f"""
        <div class="vendor-section">
            <h2 class="vendor-title">{vendor_name} ({len(files)}개)</h2>
            <div class="file-grid">
"""
                    for file in files:
                        # 파일명에서 번호와 제목 추출
                        match = re.match(r'^(\d+)_(.*)\.html$', file.name)
                        if match:
                            number = match.group(1)
                            title = match.group(2).replace('_', ' ')
                            
                            html += f"""
                <div class="file-item">
                    <a href="{vendor_name}/{file.name}" target="_blank">
                        <span class="file-number">[{number}]</span> {title}
                    </a>
                </div>
"""
                    html += """
            </div>
        </div>
"""
        
        html += """
    </div>
</body>
</html>"""
        
        # 인덱스 파일 저장
        index_file = self.output_base / 'index.html'
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"\n인덱스 생성: {index_file}")
        return index_file


def main():
    """메인 실행"""
    organizer = CorrectHTMLOrganizer()
    
    # 1. 모든 파일 처리
    stats = organizer.process_all_files()
    
    # 2. 인덱스 생성
    index_file = organizer.create_index_html()
    
    print(f"\n[COMPLETE] 처리 완료!")
    print(f"[OUTPUT] {organizer.output_base}")
    
    # 브라우저에서 열기
    import webbrowser
    webbrowser.open(str(index_file))


if __name__ == "__main__":
    main()
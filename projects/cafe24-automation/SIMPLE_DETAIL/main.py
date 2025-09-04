"""
심플 상세페이지 시스템
완전히 새로운 구조로 간단하게
"""

import os
import json
from pathlib import Path
from datetime import datetime

class SimpleDetailSystem:
    def __init__(self):
        # 핵심 경로만
        self.ftp_dir = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\ftp_mirror")
        self.txt_dir = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html\temp_txt")
        
        # 새로운 출력 경로
        self.base_dir = Path(r"C:\Users\8899y\CUA-MASTER\SIMPLE_DETAIL")
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"[초기화] Simple Detail System")
        print(f"  FTP: {self.ftp_dir}")
        print(f"  TXT: {self.txt_dir}")
        print(f"  출력: {self.output_dir}")
    
    def check_sources(self):
        """소스 데이터 확인"""
        print("\n[데이터 확인]")
        
        # FTP 폴더 확인
        if self.ftp_dir.exists():
            files = list(self.ftp_dir.glob("*"))
            print(f"  FTP 파일: {len(files)}개")
        else:
            print(f"  FTP 폴더 없음")
        
        # TXT 폴더 확인
        if self.txt_dir.exists():
            txt_files = list(self.txt_dir.glob("*.txt"))
            print(f"  TXT 파일: {len(txt_files)}개")
            if txt_files:
                print(f"    샘플: {txt_files[0].name}, {txt_files[1].name if len(txt_files) > 1 else ''}")
        else:
            print(f"  TXT 폴더 없음")
    
    def process_txt_file(self, txt_file: Path):
        """TXT 파일 처리"""
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 제품 번호 추출
            product_id = txt_file.stem
            
            # 간단한 HTML 생성
            html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>제품 {product_id}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .content {{
            background: #f5f5f5;
            padding: 20px;
            border-radius: 10px;
        }}
    </style>
</head>
<body>
    <div class="content">
        <h1>제품 번호: {product_id}</h1>
        <div class="detail">
            {content}
        </div>
    </div>
</body>
</html>"""
            
            return product_id, html
        except Exception as e:
            print(f"  [오류] {txt_file.name}: {e}")
            return None, None
    
    def generate_all(self):
        """모든 파일 처리"""
        print("\n[처리 시작]")
        
        if not self.txt_dir.exists():
            print("  TXT 폴더가 없습니다.")
            return
        
        txt_files = list(self.txt_dir.glob("*.txt"))
        success = 0
        
        for txt_file in txt_files[:10]:  # 먼저 10개만 테스트
            product_id, html = self.process_txt_file(txt_file)
            
            if html:
                output_file = self.output_dir / f"{product_id}.html"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(html)
                success += 1
                print(f"  [OK] {product_id}.html")
        
        print(f"\n[완료] {success}개 생성")
    
    def run(self):
        """실행"""
        print("="*60)
        print("SIMPLE DETAIL SYSTEM")
        print("="*60)
        
        self.check_sources()
        self.generate_all()
        
        print("\n완료!")
        print(f"결과: {self.output_dir}")

# 진입점
def main():
    system = SimpleDetailSystem()
    system.run()

if __name__ == "__main__":
    main()
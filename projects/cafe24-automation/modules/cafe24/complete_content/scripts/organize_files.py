"""
파일 정리 및 구조 관리 스크립트
브랜드별 HTML 파일 정리
"""
import shutil
from pathlib import Path
from datetime import datetime
import json

def organize_html_files():
    """HTML 파일을 브랜드별로 정리"""
    
    base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html")
    
    print("HTML 파일 정리 시작")
    
    # 현재 구조 확인
    for folder in base_path.iterdir():
        if folder.is_dir() and folder.name != 'temp_txt':
            html_files = list(folder.glob("*.html"))
            print(f"{folder.name}: {len(html_files)}개 파일")
    
    print("정리 완료")

if __name__ == "__main__":
    organize_html_files()
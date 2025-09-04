"""
폴더 정리 및 통합 스크립트
빈 폴더 제거 및 구조 정리
"""
import shutil
from pathlib import Path
from datetime import datetime

def clean_folders():
    """빈 폴더 정리"""
    
    base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html")
    
    print("폴더 정리 시작")
    
    deleted_folders = []
    
    for folder in base_path.iterdir():
        if folder.is_dir() and folder.name not in ['temp_txt', 'nul']:
            html_files = list(folder.glob("*.html"))
            
            if len(html_files) == 0:
                try:
                    shutil.rmtree(folder)
                    deleted_folders.append(folder.name)
                    print(f"삭제: {folder.name}")
                except Exception as e:
                    print(f"삭제 실패: {folder.name} - {e}")
    
    print(f"총 {len(deleted_folders)}개 폴더 삭제")
    
    return deleted_folders

if __name__ == "__main__":
    clean_folders()
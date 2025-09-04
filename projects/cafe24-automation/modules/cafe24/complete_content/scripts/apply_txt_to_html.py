"""
TXT 파일 내용을 HTML 파일에 적용하는 스크립트
temp_txt의 내용을 각 브랜드 폴더의 HTML에 적용
"""
from pathlib import Path
import json
from datetime import datetime

def apply_txt_content_to_html():
    """TXT 내용을 HTML 파일에 적용"""
    
    base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html")
    txt_path = base_path / "temp_txt"
    
    applied_count = 0
    error_count = 0
    
    print("TXT → HTML 내용 적용 시작")
    
    # 모든 브랜드 폴더의 HTML 파일 처리
    for brand_folder in base_path.iterdir():
        if brand_folder.is_dir() and brand_folder.name not in ['temp_txt', 'nul']:
            for html_file in brand_folder.glob("*.html"):
                product_no = html_file.stem
                txt_file = txt_path / f"{product_no}.txt"
                
                if txt_file.exists():
                    try:
                        # TXT 내용 읽기
                        with open(txt_file, 'r', encoding='utf-8') as f:
                            txt_content = f.read()
                        
                        # HTML 템플릿에 적용
                        html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Product {product_no}</title>
</head>
<body>
{txt_content}
</body>
</html>'''
                        
                        # HTML 파일에 쓰기
                        with open(html_file, 'w', encoding='utf-8') as f:
                            f.write(html_content)
                        
                        applied_count += 1
                        
                    except Exception as e:
                        print(f"ERROR {product_no}: {e}")
                        error_count += 1
    
    print(f"적용 완료: {applied_count}개")
    print(f"오류: {error_count}개")
    
    return applied_count, error_count

if __name__ == "__main__":
    apply_txt_content_to_html()
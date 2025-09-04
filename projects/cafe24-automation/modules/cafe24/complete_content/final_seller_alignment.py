import re
from pathlib import Path

def final_seller_alignment():
    """판매자 정보 타이틀에 padding-left 추가"""
    output_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\output\content_only")
    
    files = [
        '131_final_clean.html',
        '133_final_clean.html', 
        '134_final_clean.html',
        '135_final_clean.html',
        '140_final_clean.html'
    ]
    
    for file_name in files:
        file_path = output_path / file_name
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # padding-left: 8px; 추가
            content = re.sub(
                r'(\.section-title\.seller-title \{[^}]*?)(\n            margin-bottom: 25px;)',
                r'\1\n            padding-left: 8px;\2',
                content
            )
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"완료: {file_name}")
        else:
            print(f"없음: {file_name}")
    
    print("\n최종 정렬 완료!")
    print("판매자 정보에 padding-left: 8px; 추가")

if __name__ == "__main__":
    final_seller_alignment()
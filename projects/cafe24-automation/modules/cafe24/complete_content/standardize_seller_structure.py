import re
from pathlib import Path

def standardize_seller_structure():
    """판매자 정보를 영양성분과 동일한 구조로 표준화"""
    output_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\output\content_only")
    
    files = [
        '131_final_clean.html',
        '132_final_clean.html',  # 이미 수정했지만 CSS 정리를 위해 포함
        '133_final_clean.html', 
        '134_final_clean.html',
        '135_final_clean.html',
        '140_final_clean.html'
    ]
    
    print("판매자 정보 구조를 영양성분과 동일하게 표준화...")
    
    for file_name in files:
        file_path = output_path / file_name
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 1. HTML에서 seller-title 클래스 제거
            content = re.sub(
                r'<h2 class="section-title seller-title">',
                '<h2 class="section-title">',
                content
            )
            
            # 2. CSS에서 seller-title 관련 모든 스타일 제거
            content = re.sub(
                r'\.section-title\.seller-title \{[^}]*\}.*?(?=\n\s*\.|\n\s*@|\n\s*\}|\n\s*/\*|\Z)',
                '',
                content,
                flags=re.DOTALL
            )
            
            # 3. seller-title::after 스타일도 제거
            content = re.sub(
                r'\.section-title\.seller-title::after \{[^}]*\}.*?(?=\n\s*\.|\n\s*@|\n\s*\}|\n\s*/\*|\Z)',
                '',
                content,
                flags=re.DOTALL
            )
            
            # 4. 빈 줄 정리
            content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"표준화 완료: {file_name}")
        else:
            print(f"파일 없음: {file_name}")
    
    print("\n✅ 모든 템플릿 구조 표준화 완료!")
    print("변경사항:")
    print("- 판매자 정보 → 일반 section-title 사용")
    print("- 영양성분과 동일한 구조")
    print("- 불필요한 seller-title CSS 제거")
    print("- 완벽한 정렬 일관성 확보")

if __name__ == "__main__":
    standardize_seller_structure()
import re
from pathlib import Path

def unify_seller_structure():
    """판매자 정보 구조를 영양성분과 완전히 동일하게 통일"""
    output_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\output\content_only")
    
    files = [
        '131_final_clean.html',
        '133_final_clean.html', 
        '134_final_clean.html',
        '135_final_clean.html',
        '140_final_clean.html'
    ]
    
    print("판매자 정보 하위 구조를 영양성분과 완전히 동일하게 통일...")
    
    for file_name in files:
        file_path = output_path / file_name
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 1. 회사 정보 섹션 구조 변경
            content = re.sub(
                r'<!-- 회사 정보 -->\s*<div class="seller-info-section">\s*<h3>회사 정보</h3>',
                '<!-- 회사 정보 -->\n            <div style="background: #f8f9fa; padding: 25px; border-radius: 8px; margin: 20px 0;">\n                <h3 style="color: #333; font-size: 18px; font-weight: 600; margin-bottom: 15px; text-align: center;">회사 정보</h3>',
                content
            )
            
            # 2. 연락처 정보 섹션 구조 변경
            content = re.sub(
                r'<!-- 연락처 정보 -->\s*<div class="seller-info-section">\s*<h3>연락처</h3>',
                '<!-- 연락처 정보 -->\n            <div style="background: #f8f9fa; padding: 25px; border-radius: 8px; margin: 20px 0;">\n                <h3 style="color: #333; font-size: 18px; font-weight: 600; margin-bottom: 15px; text-align: center;">연락처</h3>',
                content
            )
            
            # 3. CSS에서 seller-info-section 클래스 제거
            content = re.sub(
                r'\.seller-info-section \{[^}]*\}.*?(?=\n\s*\.|\n\s*@|\n\s*\}|\n\s*/\*|\Z)',
                '',
                content,
                flags=re.DOTALL
            )
            
            # 4. seller-info-section h3 스타일도 제거
            content = re.sub(
                r'\.seller-info-section h3 \{[^}]*\}.*?(?=\n\s*\.|\n\s*@|\n\s*\}|\n\s*/\*|\Z)',
                '',
                content,
                flags=re.DOTALL
            )
            
            # 5. 빈 줄 정리
            content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"구조 통일 완료: {file_name}")
        else:
            print(f"파일 없음: {file_name}")
    
    print("\n모든 파일 판매자 정보 구조 통일 완료!")
    print("영양성분과 완전히 동일한 구조:")
    print("- 동일한 배경색: #f8f9fa")
    print("- 동일한 패딩: 25px")  
    print("- 동일한 h3 스타일")
    print("- 완벽한 구조 일관성 확보")

if __name__ == "__main__":
    unify_seller_structure()
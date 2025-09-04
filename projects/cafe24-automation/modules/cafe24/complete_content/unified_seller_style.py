import re
from pathlib import Path

def unify_seller_style():
    """모든 파일의 판매자 정보 스타일을 132번과 동일하게 통일"""
    output_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\output\content_only")
    
    files = [
        '131_final_clean.html',
        '133_final_clean.html', 
        '134_final_clean.html',
        '135_final_clean.html',
        '140_final_clean.html'
    ]
    
    # 132번과 동일한 깔끔한 스타일
    unified_seller_style = '''        .section-title.seller-title {
            border-bottom: 2px solid #2c2c2c;
            background: none;
            color: #2c2c2c;
            padding-bottom: 8px;
            padding-left: 8px;
            margin-bottom: 25px;
            font-size: 24px;
            font-weight: 600;
            letter-spacing: -0.5px;
            text-transform: none;
            position: relative;
        }
        
        .section-title.seller-title::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 8px;
            width: 40px;
            height: 2px;
            background: #2c2c2c;
        }'''
    
    print("모든 템플릿의 판매자 정보 스타일 통일...")
    
    for file_name in files:
        file_path = output_path / file_name
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 기존 seller-title 스타일 모두 제거하고 새것으로 교체
            # 1. 기존 스타일 제거
            content = re.sub(
                r'\.section-title\.seller-title \{[^}]*\}.*?(?=\n\s*\.|\n\s*@|\n\s*\}|\Z)',
                '',
                content,
                flags=re.DOTALL
            )
            
            # 2. shimmer 애니메이션도 제거
            content = re.sub(
                r'@keyframes shimmer \{[^}]*\}.*?(?=\n\s*\.|\n\s*@|\n\s*\}|\Z)',
                '',
                content,
                flags=re.DOTALL
            )
            
            # 3. 새 스타일을 .section-title 뒤에 추가
            content = re.sub(
                r'(\.section-title \{[^}]*\})',
                r'\1\n        \n' + unified_seller_style,
                content
            )
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"통일완료: {file_name}")
        else:
            print(f"없음: {file_name}")
    
    print("\n모든 템플릿 판매자 정보 스타일 통일 완료!")
    print("132번과 동일한 깔끔한 디자인 적용")

if __name__ == "__main__":
    unify_seller_style()
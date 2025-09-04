import re
from pathlib import Path

def align_seller_title():
    """판매자 정보 타이틀을 다른 섹션과 동일하게 정렬"""
    output_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\output\content_only")
    
    files = [
        '131_final_clean.html',
        '133_final_clean.html', 
        '134_final_clean.html',
        '135_final_clean.html',
        '140_final_clean.html'
    ]
    
    # 수정된 정렬 스타일
    aligned_seller_style = '''        .section-title.seller-title {
            border-bottom: 2px solid #2c2c2c;
            background: none;
            color: #2c2c2c;
            padding-bottom: 8px;
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
    
    print("판매자 정보 타이틀 정렬 수정중...")
    
    for file_name in files:
        file_path = output_path / file_name
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 기존 스타일 교체
            content = re.sub(
                r'\.section-title\.seller-title \{.*?\}.*?\.section-title\.seller-title::after \{.*?\}',
                aligned_seller_style,
                content,
                flags=re.DOTALL
            )
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"완료: {file_name}")
        else:
            print(f"없음: {file_name}")
    
    print("\n판매자 정보 타이틀 정렬 완료!")
    print("변경사항:")
    print("- text-align: left 제거 (기본값 사용)")
    print("- padding-left 8px 추가하여 다른 섹션과 일치")
    print("- 포인트 라인 위치도 8px 조정")

if __name__ == "__main__":
    align_seller_title()
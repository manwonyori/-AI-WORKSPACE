import re
from pathlib import Path

def fix_seller_section_design():
    """판매자 정보 섹션을 더 세련되게 변경"""
    output_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\output\content_only")
    
    files = [
        '131_final_clean.html',
        '133_final_clean.html', 
        '134_final_clean.html',
        '135_final_clean.html',
        '140_final_clean.html'
    ]
    
    # 새로운 세련된 스타일
    new_seller_style = '''        .section-title.seller-title {
            text-align: left;
            border-bottom: 2px solid #2c2c2c;
            background: none;
            color: #2c2c2c;
            padding: 0 0 8px 0;
            margin-bottom: 25px;
            font-size: 22px;
            font-weight: 600;
            letter-spacing: -0.3px;
            text-transform: none;
            position: relative;
        }
        
        .section-title.seller-title::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 40px;
            height: 2px;
            background: #2c2c2c;
        }'''
    
    print("판매자 정보 섹션 디자인을 세련되게 변경중...")
    
    for file_name in files:
        file_path = output_path / file_name
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 기존 촌스러운 스타일 제거
            content = re.sub(
                r'\.section-title\.seller-title \{.*?\}.*?@keyframes shimmer \{.*?\}',
                new_seller_style,
                content,
                flags=re.DOTALL
            )
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"✓ {file_name} 업데이트 완료")
        else:
            print(f"✗ {file_name} 파일 없음")
    
    print("\n🎨 판매자 정보 섹션 디자인 개선 완료!")
    print("변경사항:")
    print("- 큰 차콜 배경 제거")
    print("- Shimmer 애니메이션 제거") 
    print("- 깔끔한 보더라인으로 변경")
    print("- 왼쪽 정렬로 자연스럽게")
    print("- 폰트 크기 적당하게 조정")

if __name__ == "__main__":
    fix_seller_section_design()
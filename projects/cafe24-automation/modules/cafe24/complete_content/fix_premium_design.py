"""
프리미엄 미니멀 디자인 적용 스크립트
- 131_final_clean.html을 기준으로 다른 파일들 업데이트
"""

import os
import re
from pathlib import Path

def get_premium_css():
    """프리미엄 미니멀 CSS 스타일 반환"""
    return """        /* 기본 스타일 */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            color: #333;
            background: #fff;
        }
        
        .product-content-wrapper {
            max-width: 860px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .content-section {
            margin-bottom: 40px;
        }
        
        .section-title {
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 1px solid #e8e8e8;
            color: #2c2c2c;
            padding-left: 0;
            letter-spacing: -0.5px;
        }
        
        .section-title.seller-title {
            text-align: center;
            border-bottom: none;
            background: linear-gradient(135deg, #2c2c2c 0%, #4a4a4a 100%);
            color: #ffffff;
            padding: 20px 30px;
            margin-bottom: 30px;
            font-size: 20px;
            font-weight: 500;
            letter-spacing: 1px;
            text-transform: uppercase;
            position: relative;
            overflow: hidden;
        }
        
        .section-title.seller-title::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
            animation: shimmer 3s infinite;
        }
        
        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        .highlight-box {
            background: #fafafa;
            padding: 25px;
            margin: 25px 0;
            border-left: 2px solid #2c2c2c;
            border-radius: 0;
            position: relative;
        }
        
        .highlight-box::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 2px;
            height: 100%;
            background: linear-gradient(to bottom, #2c2c2c, #888888);
        }
        
        .highlight-box ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .detail-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .detail-table th,
        .detail-table td {
            padding: 15px 12px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .detail-table th {
            width: 140px;
            background: #fafafa;
            font-weight: 500;
            color: #2c2c2c;
            font-size: 14px;
            letter-spacing: 0.5px;
        }
        
        .detail-table td {
            color: #555555;
            font-size: 14px;
        }
        
        .seller-info-section {
            background: #ffffff;
            padding: 30px;
            border: 1px solid #e8e8e8;
            margin-bottom: 25px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        
        .seller-info-section h3 {
            color: #2c2c2c;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 20px;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            position: relative;
            padding-bottom: 10px;
        }
        
        .seller-info-section h3::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 30px;
            height: 1px;
            background: #2c2c2c;
        }
        
        /* 모바일 최적화 */
        @media (max-width: 768px) {
            .product-content-wrapper {
                padding: 15px;
            }
            
            .section-title {
                font-size: 22px;
            }
            
            .highlight-box li {
                font-size: 16px;
                padding: 8px 0;
            }
            
            .detail-table th,
            .detail-table td {
                padding: 12px 8px;
                font-size: 16px;
            }
            
            .detail-table th {
                width: 100px;
            }
        }"""

def fix_file(file_path):
    """단일 파일의 CSS와 알레르기 태그 수정"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # CSS 전체 교체 (style 태그 내용만)
        css_pattern = r'(<style>)(.*?)(</style>)'
        new_css = f'\\1\\n{get_premium_css()}\\n    \\3'
        
        content = re.sub(css_pattern, new_css, content, flags=re.DOTALL)
        
        # 알레르기 태그 스타일 교체
        old_allergen_style = r'background: #dc3545; color: white; padding: 8px 12px; border-radius: 20px; font-size: 14px; font-weight: 600; margin: 4px;'
        new_allergen_style = 'background: linear-gradient(135deg, #2c2c2c 0%, #555555 100%); color: white; padding: 6px 14px; font-size: 13px; font-weight: 500; box-shadow: 0 1px 3px rgba(44,44,44,0.2); letter-spacing: 0.5px; margin: 4px;'
        
        content = content.replace(old_allergen_style, new_allergen_style)
        
        # 파일 저장
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return True
        
    except Exception as e:
        print(f"오류 발생 {file_path}: {e}")
        return False

def main():
    """메인 함수"""
    base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\output\content_only")
    
    files_to_fix = [
        '132_final_clean.html',
        '133_final_clean.html', 
        '134_final_clean.html',
        '135_final_clean.html',
        '140_final_clean.html'
    ]
    
    print("=" * 60)
    print("프리미엄 미니멀 디자인 적용")
    print("=" * 60)
    
    success_count = 0
    
    for file_name in files_to_fix:
        file_path = base_path / file_name
        if file_path.exists():
            if fix_file(file_path):
                print(f"✅ {file_name} - 완료")
                success_count += 1
            else:
                print(f"❌ {file_name} - 실패")
        else:
            print(f"⚠️ {file_name} - 파일 없음")
    
    print(f"\n완료: {success_count}/{len(files_to_fix)} 파일")
    print("🎨 프리미엄 미니멀 디자인 적용 완료!")

if __name__ == "__main__":
    main()
import os
from pathlib import Path

def verify_improved_files():
    """개선된 파일들 품질 검증"""
    improved_path = Path("C:/Users/8899y/CUA-MASTER/modules/cafe24/complete_content/output/chuyoungru_improved")
    
    print("[검증] 개선된 HTML 파일 품질 검증 중...")
    
    html_files = list(improved_path.glob("*_improved.html"))
    print(f"[확인] {len(html_files)}개 개선된 파일 발견")
    
    quality_score = 0
    total_checks = 0
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 품질 검사 항목들
            checks = [
                ('UTF-8 인코딩', 'charset="UTF-8"' in content),
                ('반응형 메타태그', 'viewport' in content),
                ('브랜드 스토리', '브랜드 스토리' in content),
                ('취영루 브랜드', '취영루' in content),
                ('구조화된 HTML', '<div class="content-section">' in content),
                ('완성된 HTML', '</html>' in content)
            ]
            
            file_score = 0
            for check_name, result in checks:
                if result:
                    file_score += 1
                total_checks += 1
            
            quality_score += file_score
            print(f"[품질] {html_file.name}: {file_score}/6 ({file_score/6*100:.0f}%)")
            
        except Exception as e:
            print(f"[오류] {html_file.name} 검증 실패: {e}")
    
    overall_quality = (quality_score / total_checks) * 100 if total_checks > 0 else 0
    print(f"\n[결과] 전체 품질 점수: {overall_quality:.1f}%")
    print(f"[통계] {quality_score}/{total_checks} 검사 통과")
    
    return overall_quality

if __name__ == "__main__":
    verify_improved_files()
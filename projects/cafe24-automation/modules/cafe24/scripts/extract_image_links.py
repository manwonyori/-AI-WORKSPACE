"""
HTML 파일에서 이미지 URL 추출 및 분석
"""
import os
import re
from bs4 import BeautifulSoup
import json
from collections import defaultdict

def extract_images_from_html():
    html_folder = r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html"
    
    results = {
        'total_files': 0,
        'files_with_images': 0,
        'files_without_images': 0,
        'empty_files': 0,
        'total_images': 0,
        'image_domains': defaultdict(int),
        'file_details': {},
        'empty_html_list': [],
        'no_image_list': []
    }
    
    # 모든 HTML 파일 검사
    for root, dirs, files in os.walk(html_folder):
        for file in files:
            if file.endswith('.html'):
                results['total_files'] += 1
                file_path = os.path.join(root, file)
                supplier = os.path.basename(root)
                product_no = file.replace('.html', '')
                
                # 파일 읽기
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 빈 파일 체크
                if len(content) < 20 or content.strip() == '<p><br></p>':
                    results['empty_files'] += 1
                    results['empty_html_list'].append(f"{supplier}/{product_no}")
                    continue
                
                # BeautifulSoup으로 파싱
                soup = BeautifulSoup(content, 'html.parser')
                
                # 이미지 태그 찾기
                images = []
                
                # img 태그
                for img in soup.find_all('img'):
                    src = img.get('src', '')
                    if src:
                        images.append(src)
                
                # background-image 스타일
                style_pattern = r'background-image:\s*url\([\'"]?([^\'"]+)[\'"]?\)'
                for match in re.finditer(style_pattern, content):
                    images.append(match.group(1))
                
                # 이미지 URL 분석
                if images:
                    results['files_with_images'] += 1
                    results['total_images'] += len(images)
                    
                    # 도메인 추출
                    for img_url in images:
                        if img_url.startswith('http'):
                            domain = img_url.split('/')[2]
                            results['image_domains'][domain] += 1
                        elif img_url.startswith('//'):
                            domain = img_url[2:].split('/')[0]
                            results['image_domains'][domain] += 1
                        else:
                            results['image_domains']['relative'] += 1
                    
                    results['file_details'][f"{supplier}/{product_no}"] = {
                        'image_count': len(images),
                        'images': images[:5]  # 처음 5개만 샘플로 저장
                    }
                else:
                    results['files_without_images'] += 1
                    results['no_image_list'].append(f"{supplier}/{product_no}")
    
    return results

def save_report(results):
    """분석 결과 저장"""
    
    # JSON 저장
    with open(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\image_analysis_report.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 텍스트 리포트
    report = f"""
===========================================
    이미지 링크 추출 분석 리포트
===========================================

[전체 현황]
-------------------------------------------
총 HTML 파일: {results['total_files']}개
이미지 있는 파일: {results['files_with_images']}개 ({results['files_with_images']/results['total_files']*100:.1f}%)
이미지 없는 파일: {results['files_without_images']}개 ({results['files_without_images']/results['total_files']*100:.1f}%)
빈 HTML 파일: {results['empty_files']}개 ({results['empty_files']/results['total_files']*100:.1f}%)

[이미지 통계]
-------------------------------------------
총 이미지 수: {results['total_images']}개
평균 이미지/파일: {results['total_images']/results['files_with_images'] if results['files_with_images'] > 0 else 0:.1f}개 (이미지 있는 파일 기준)

[이미지 도메인 분포]
-------------------------------------------"""
    
    for domain, count in sorted(results['image_domains'].items(), key=lambda x: x[1], reverse=True)[:10]:
        report += f"\n{domain}: {count}개"
    
    report += f"""

[문제 파일들]
-------------------------------------------
빈 HTML: {results['empty_files']}개
이미지 없음: {results['files_without_images']}개

[샘플 데이터]
-------------------------------------------
이미지 있는 파일 예시:"""
    
    # 샘플 5개만 출력
    for file_path, details in list(results['file_details'].items())[:5]:
        report += f"\n\n{file_path}:"
        report += f"\n  이미지 {details['image_count']}개"
        for img in details['images'][:2]:
            if len(img) > 60:
                img = img[:60] + "..."
            report += f"\n  - {img}"
    
    report += "\n\n" + "="*43
    
    # 텍스트 파일 저장
    with open(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\image_analysis_report.txt", 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)
    return results

if __name__ == "__main__":
    print("이미지 링크 추출 시작...")
    results = extract_images_from_html()
    save_report(results)
    print("\n[OK] 분석 완료!")
    print(f"결과 저장: image_analysis_report.json / .txt")
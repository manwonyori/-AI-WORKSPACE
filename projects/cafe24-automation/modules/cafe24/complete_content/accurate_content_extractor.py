"""
정확한 제품 정보 추출 및 검수 시스템
- temp_txt 원본에서 실제 제품 정보 추출
- 제품명, 특징, 설명 문구 등을 정확히 파싱
- 기존 템플릿과 비교하여 차이점 분석
"""

import re
import json
from pathlib import Path
from bs4 import BeautifulSoup

class AccurateContentExtractor:
    def __init__(self):
        self.temp_txt_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html\temp_txt")
        self.output_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\output\content_only")
        
    def extract_product_info(self, product_number):
        """원본 TXT에서 정확한 제품 정보 추출"""
        txt_file = self.temp_txt_path / f"{product_number}.txt"
        
        if not txt_file.exists():
            return None
            
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # BeautifulSoup으로 HTML 파싱
            soup = BeautifulSoup(content, 'html.parser')
            
            product_info = {
                'product_number': product_number,
                'title': '',
                'main_copy': '',
                'features': [],
                'images': [],
                'why_section': '',
                'special_features': []
            }
            
            # 1. 제품 타이틀 추출
            title_tag = soup.find('title')
            if title_tag:
                product_info['title'] = title_tag.text.strip()
            
            # 2. 메인 카피 추출 (header-main-copy)
            main_copy = soup.find(class_='header-main-copy')
            if main_copy:
                product_info['main_copy'] = main_copy.get_text().strip()
            
            # 3. 애니메이션 텍스트 추출 (핵심 메시지)
            animated_text = soup.find(class_='animated-text')
            if animated_text:
                product_info['animated_text'] = animated_text.get_text().strip()
            
            # 4. Why 섹션 추출
            why_section = soup.find(class_='section-title')
            if why_section and 'Why?' in why_section.text:
                product_info['why_section'] = why_section.get_text().strip()
            
            # 5. 카드 섹션들 추출 (특징들)
            why_cards = soup.find_all(class_='why-card')
            for card in why_cards:
                card_title = card.find('h3')
                card_desc = card.find('p')
                if card_title and card_desc:
                    product_info['features'].append({
                        'title': card_title.get_text().strip(),
                        'description': card_desc.get_text().strip()
                    })
            
            # 6. 이미지 링크 추출
            images = soup.find_all('img')
            for img in images:
                src = img.get('src', '')
                if 'ecimg.cafe24img.com' in src:
                    alt_text = img.get('alt', '')
                    product_info['images'].append({
                        'url': src,
                        'alt': alt_text
                    })
            
            # 7. 특별 섹션들 추출 (feature-highlight 등)
            highlights = soup.find_all(class_='feature-highlight')
            for highlight in highlights:
                h3_tag = highlight.find('h3')
                if h3_tag:
                    product_info['special_features'].append(h3_tag.get_text().strip())
            
            return product_info
            
        except Exception as e:
            print(f"오류 발생 {product_number}: {e}")
            return None
    
    def analyze_current_template(self, product_number):
        """현재 템플릿의 내용 분석"""
        template_file = self.output_path / f"{product_number}_final_clean.html"
        
        if not template_file.exists():
            return None
            
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            template_info = {
                'product_number': product_number,
                'features': [],
                'title': ''
            }
            
            # 타이틀 추출
            title_match = re.search(r'<title>(.*?)</title>', content)
            if title_match:
                template_info['title'] = title_match.group(1)
            
            # 상품설명 리스트 추출
            feature_matches = re.findall(r'<li[^>]*>✓\s*(.*?)</li>', content)
            template_info['features'] = feature_matches
            
            return template_info
            
        except Exception as e:
            print(f"템플릿 분석 오류 {product_number}: {e}")
            return None
    
    def compare_and_report(self, product_numbers):
        """원본과 템플릿 비교 분석 리포트"""
        comparison_report = {
            'timestamp': str(Path().resolve()),
            'products': []
        }
        
        print("=" * 80)
        print("제품 정보 정확성 검수 리포트")
        print("=" * 80)
        
        for product_number in product_numbers:
            print(f"\n[분석중] 제품 {product_number}")
            
            # 원본 정보 추출
            original = self.extract_product_info(product_number)
            template = self.analyze_current_template(product_number)
            
            if not original:
                print(f"  ❌ 원본 파일 없음: {product_number}.txt")
                continue
                
            if not template:
                print(f"  ❌ 템플릿 파일 없음: {product_number}_final_clean.html")
                continue
            
            # 비교 분석
            comparison = {
                'product_number': product_number,
                'original': original,
                'template': template,
                'issues': [],
                'accuracy_score': 0
            }
            
            # 1. 제품명 일치 여부
            if original['title'] != template['title']:
                comparison['issues'].append({
                    'type': 'title_mismatch',
                    'original': original['title'],
                    'template': template['title']
                })
                print(f"  ⚠️ 제품명 불일치")
                print(f"     원본: {original['title']}")
                print(f"     템플릿: {template['title']}")
            
            # 2. 특징 일치 여부
            if original['main_copy']:
                print(f"  📝 원본 메인 카피: {original['main_copy'][:50]}...")
                
            if original['animated_text']:
                print(f"  ✨ 핵심 메시지: {original['animated_text']}")
                
            # 3. 특징 리스트 분석
            if original['features']:
                print(f"  🎯 원본 특징: {len(original['features'])}개")
                for i, feature in enumerate(original['features'][:3]):
                    print(f"     {i+1}. {feature['title']}: {feature['description'][:30]}...")
            
            if template['features']:
                print(f"  📋 템플릿 특징: {len(template['features'])}개")
                for i, feature in enumerate(template['features']):
                    print(f"     {i+1}. {feature[:50]}...")
                    
            # 정확성 점수 계산
            score = 100
            if comparison['issues']:
                score -= len(comparison['issues']) * 20
            comparison['accuracy_score'] = max(0, score)
            
            print(f"  📊 정확성 점수: {comparison['accuracy_score']}/100")
            
            comparison_report['products'].append(comparison)
        
        # 리포트 저장
        report_file = self.output_path / "accuracy_comparison_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(comparison_report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📋 상세 리포트 저장: {report_file}")
        
        # 요약 통계
        total_products = len(comparison_report['products'])
        accurate_products = len([p for p in comparison_report['products'] if p['accuracy_score'] >= 80])
        
        print(f"\n📊 검수 결과 요약:")
        print(f"   총 제품 수: {total_products}")
        print(f"   정확한 제품: {accurate_products}")
        print(f"   정확도: {accurate_products/total_products*100:.1f}%" if total_products > 0 else "   정확도: 0%")
        
        return comparison_report

def main():
    extractor = AccurateContentExtractor()
    
    # 테스트할 제품 번호들
    test_products = ['131', '132', '133', '134', '135', '140']
    
    print("🔍 제품 정보 정확성 검수를 시작합니다...")
    report = extractor.compare_and_report(test_products)
    
    print("\n✅ 검수 완료! 이제 정확한 내용으로 업데이트할 수 있습니다.")

if __name__ == "__main__":
    main()
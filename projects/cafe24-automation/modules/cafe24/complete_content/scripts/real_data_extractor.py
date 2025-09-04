import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

class RealDataExtractor:
    """temp_txt 파일에서 실제 제품 데이터 추출"""
    
    def __init__(self):
        self.base_path = Path("C:/Users/8899y/CUA-MASTER/modules/cafe24/complete_content")
        self.temp_txt_path = self.base_path / "html" / "temp_txt"
        
        # 취영루 제품 ID
        self.chuyoungru_ids = [131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 145, 62, 65]
    
    def extract_product_data(self, product_id):
        """개별 제품 데이터 추출"""
        txt_file = self.temp_txt_path / f"{product_id}.txt"
        
        if not txt_file.exists():
            print(f"[경고] {product_id}.txt 파일 없음")
            return None
        
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # BeautifulSoup으로 파싱
        soup = BeautifulSoup(content, 'html.parser')
        
        data = {
            'product_id': product_id,
            'title': None,
            'main_copy': None,
            'images': [],
            'features': [],
            'description': None
        }
        
        # 제목 추출
        title_tag = soup.find('title')
        if title_tag:
            data['title'] = title_tag.text.strip()
        
        # 메인 카피 추출
        main_copy = soup.find('h1', class_='header-main-copy')
        if main_copy:
            data['main_copy'] = main_copy.get_text(strip=True)
        
        # 이미지 URL 추출
        images = soup.find_all('img')
        for img in images:
            src = img.get('src')
            if src and 'cafe24img.com' in src:
                data['images'].append({
                    'src': src,
                    'alt': img.get('alt', '')
                })
        
        # 특징 추출 (Why Section)
        why_cards = soup.find_all('div', class_='why-card')
        for card in why_cards:
            title = card.find('h3', class_='why-card-title')
            desc = card.find('p', class_='why-card-desc')
            if title and desc:
                data['features'].append({
                    'title': title.get_text(strip=True),
                    'desc': desc.get_text(strip=True)
                })
        
        # 상품 설명 추출
        desc_sections = soup.find_all('p', class_='why-card-desc')
        if desc_sections:
            data['description'] = ' '.join([p.get_text(strip=True) for p in desc_sections])
        
        return data
    
    def extract_all_chuyoungru(self):
        """모든 취영루 제품 데이터 추출"""
        all_data = {}
        
        for product_id in self.chuyoungru_ids:
            print(f"[추출] {product_id}번 제품 데이터 추출 중...")
            data = self.extract_product_data(product_id)
            if data:
                all_data[product_id] = data
                
                # 주요 정보 출력
                print(f"  제목: {data['title']}")
                print(f"  이미지: {len(data['images'])}개")
                print(f"  특징: {len(data['features'])}개")
        
        return all_data
    
    def analyze_image_patterns(self):
        """이미지 URL 패턴 분석"""
        patterns = {}
        
        for product_id in self.chuyoungru_ids:
            data = self.extract_product_data(product_id)
            if data and data['images']:
                patterns[product_id] = {
                    'product_name': data['title'],
                    'images': []
                }
                
                for img in data['images']:
                    src = img['src']
                    # URL 패턴 분석
                    if 'kyoja' in src:
                        patterns[product_id]['type'] = '교자만두'
                    elif 'kimchi' in src:
                        patterns[product_id]['type'] = '김치왕만두'
                    elif 'gokiking' in src:
                        patterns[product_id]['type'] = '고기왕만두'
                    elif 'sugan' in src or 'water' in src:
                        patterns[product_id]['type'] = '물만두'
                    elif 'gun' in src:
                        patterns[product_id]['type'] = '군만두'
                    elif 'fried' in src or 'fry' in src:
                        patterns[product_id]['type'] = '튀김만두'
                    
                    patterns[product_id]['images'].append(src)
        
        return patterns

def main():
    """메인 실행"""
    extractor = RealDataExtractor()
    
    print("=" * 60)
    print("   실제 제품 데이터 추출 시작")
    print("=" * 60)
    
    # 전체 데이터 추출
    all_data = extractor.extract_all_chuyoungru()
    
    print("\n=== 이미지 패턴 분석 ===")
    patterns = extractor.analyze_image_patterns()
    
    for product_id, pattern in patterns.items():
        print(f"\n[{product_id}] {pattern.get('product_name', 'Unknown')}")
        print(f"  타입: {pattern.get('type', '미분류')}")
        for i, img in enumerate(pattern.get('images', [])[:3], 1):
            # URL에서 파일명만 추출
            filename = img.split('/')[-1] if '/' in img else img
            print(f"  이미지{i}: {filename}")
    
    # 데이터 저장
    import json
    output_file = Path("C:/Users/8899y/CUA-MASTER/modules/cafe24/complete_content/research/real_product_data.json")
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n[저장] {output_file}")
    
    return all_data

if __name__ == "__main__":
    main()
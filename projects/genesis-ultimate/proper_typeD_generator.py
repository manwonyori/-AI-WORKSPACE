#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
올바른 Type D 생성기 - 템플릿 매니저 활용
- template_manager.py 사용
- typeD_genspark_style.html 템플릿 적용
- 원본 txt에서 정보 추출하여 변수 매핑
"""

import os
import sys
import re
import json
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
from typing import Dict, List
import random

# 현재 디렉토리를 sys.path에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from template_manager import TemplateManager
from typeD_organizer import TypeDOrganizer

class ProperTypeDGenerator:
    """템플릿 매니저를 활용한 올바른 Type D 생성"""
    
    def __init__(self):
        self.cua_dir = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html\temp_txt")
        self.output_base = Path("output/typeD_proper")
        self.output_base.mkdir(parents=True, exist_ok=True)
        
        # 템플릿 매니저와 오거나이저 초기화
        self.template_manager = TemplateManager()
        self.organizer = TypeDOrganizer(str(self.output_base))
        
        # AI 생성 문구 템플릿
        self.headlines = [
            "드디어 만나는 진짜 {product}",
            "\"이거 먹고 인생 바뀜\" 그 순간, {product}",
            "{product}, 왜 이제야 알았을까",
            "38만 구독자가 숨기고 싶어했던 {product}",
            "한 번 먹으면 못 끊는 {product}의 비밀"
        ]
        
        self.sub_headlines = [
            "매일 먹어도 질리지 않는 특별한 맛",
            "38만 구독자가 숨기고 싶어했던 바로 그 제품의 비밀",
            "최씨남매가 직접 검증한 진짜 맛",
            "한 번 먹으면 다시 찾게 되는 마법의 맛",
            "이미 아는 사람들은 재주문 중"
        ]
    
    def extract_from_txt(self, txt_file: Path) -> Dict:
        """txt 파일에서 정보 추출"""
        try:
            # 파일 읽기
            content = None
            for encoding in ['utf-8', 'cp949', 'euc-kr']:
                try:
                    with open(txt_file, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except:
                    continue
            
            if not content:
                return None
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # 제품명 추출
            product_name = "제품"
            title_tag = soup.find('title')
            if title_tag:
                product_name = title_tag.text.strip()
            
            # 가격 정보 추출
            price_info = self.extract_price(soup)
            
            # 이미지 URL 추출
            images = []
            for img in soup.find_all('img', src=True):
                img_url = img['src']
                if 'ecimg.cafe24img.com' in img_url or 'cafe24' in img_url:
                    images.append(img_url)
            
            # 주요 텍스트 추출 (WHY, STORY 섹션용)
            key_texts = []
            for tag in soup.find_all(['h2', 'h3', 'strong', 'p']):
                text = tag.get_text(strip=True)
                if text and 10 < len(text) < 200:
                    key_texts.append(text)
            
            return {
                'name': product_name,
                'price': price_info,
                'images': images[:5],
                'key_texts': key_texts[:20],
                'number': txt_file.stem
            }
            
        except Exception as e:
            print(f"추출 오류: {e}")
            return None
    
    def extract_price(self, soup) -> Dict:
        """가격 정보 추출"""
        price_info = {'original': '', 'sale': '', 'discount': ''}
        
        # 가격 관련 클래스나 텍스트 찾기
        price_elements = soup.find_all(string=re.compile(r'\d{1,3}[,\d]*\s*원'))
        
        if price_elements:
            prices = []
            for elem in price_elements[:5]:
                match = re.search(r'(\d{1,3}[,\d]*)\s*원', elem)
                if match:
                    price = match.group(1)
                    prices.append(price)
            
            if len(prices) >= 2:
                price_info['original'] = prices[0]
                price_info['sale'] = prices[1]
                
                # 할인율 계산
                try:
                    orig = int(prices[0].replace(',', ''))
                    sale = int(prices[1].replace(',', ''))
                    if orig > sale:
                        discount = int((1 - sale/orig) * 100)
                        price_info['discount'] = f"{discount}%"
                except:
                    pass
            elif prices:
                price_info['sale'] = prices[0]
        
        return price_info
    
    def generate_template_variables(self, product_data: Dict) -> Dict:
        """템플릿 변수 생성"""
        
        name = product_data.get('name', '제품')
        price = product_data.get('price', {})
        images = product_data.get('images', [])
        key_texts = product_data.get('key_texts', [])
        
        # 헤드라인 선택
        main_headline = random.choice(self.headlines).format(product=name)
        sub_headline = random.choice(self.sub_headlines)
        
        # WHY 섹션 생성
        why_points = [
            {"title": "최고급 원재료", "description": "엄선된 국내산 재료만을 사용하여 믿고 드실 수 있습니다"},
            {"title": "전통 제조방식", "description": "79년 전통의 노하우로 정성껏 만들었습니다"},
            {"title": "합리적인 가격", "description": "최상의 품질을 가장 합리적인 가격으로 제공합니다"}
        ]
        
        # STORY 섹션 생성
        story_intro = f"{name}의 특별한 이야기를 들려드립니다"
        story_content = []
        
        if key_texts:
            # 실제 텍스트에서 스토리 추출
            for text in key_texts[:5]:
                if '만두' in text or '교자' in text or '맛' in text or '전통' in text:
                    story_content.append(text)
        
        if not story_content:
            story_content = [
                "오랜 시간 연구 개발을 통해 완성된 레시피입니다",
                "고객님의 건강한 식탁을 위해 최선을 다합니다",
                "한 입 베어물면 느껴지는 깊고 풍부한 맛의 조화"
            ]
        
        # HOW 섹션 생성
        how_steps = [
            {"icon": "🍳", "title": "조리법 1", "description": "팬에 기름을 두르고 중불에서 3-4분간 구워주세요"},
            {"icon": "🔥", "title": "조리법 2", "description": "에어프라이어 180도에서 10-12분간 조리하세요"},
            {"icon": "💧", "title": "조리법 3", "description": "찜기에 넣고 8-10분간 쪄주세요"},
            {"icon": "🍽️", "title": "조리법 4", "description": "간장 소스와 함께 곁들이면 더욱 맛있습니다"}
        ]
        
        # TRUST 섹션 생성
        trust_points = [
            {"icon": "🏆", "text": "HACCP 인증 시설"},
            {"icon": "✅", "text": "100% 국내산 원재료"},
            {"icon": "⭐", "text": "고객 만족도 98%"}
        ]
        
        # 템플릿 변수 매핑
        template_vars = {
            'product_name': name,
            'main_headline': main_headline,
            'sub_headline': sub_headline,
            
            # 가격 정보
            'original_price': price.get('original', ''),
            'sale_price': price.get('sale', ''),
            'discount_rate': price.get('discount', ''),
            
            # WHY 섹션
            'why_title': f"왜 {name}를 선택해야 할까요?",
            'why_points': why_points,
            
            # STORY 섹션
            'story_title': "우리의 이야기",
            'story_intro': story_intro,
            'story_content': story_content[:3],
            
            # HOW 섹션
            'how_title': "이렇게 활용하세요",
            'how_steps': how_steps,
            
            # TRUST 섹션
            'trust_title': "믿을 수 있는 이유",
            'trust_points': trust_points,
            
            # 이미지
            'product_images': images,
            'main_image': images[0] if images else '',
            
            # 기타
            'generated_date': datetime.now().strftime('%Y년 %m월 %d일')
        }
        
        return template_vars
    
    def process_file(self, txt_file: Path) -> Dict:
        """단일 파일 처리"""
        try:
            # 1. txt에서 정보 추출
            product_data = self.extract_from_txt(txt_file)
            if not product_data:
                return {'status': 'failed', 'error': '정보 추출 실패'}
            
            # 2. 템플릿 변수 생성
            template_vars = self.generate_template_variables(product_data)
            
            # 3. 템플릿 렌더링
            html_content = self.template_manager.render_template('typeD', template_vars)
            
            # 4. 업체별 분류 및 저장
            save_result = self.organizer.save_typeD_file(
                html_content,
                str(txt_file),
                {'name': product_data['name']}
            )
            
            return {
                'status': 'success',
                'vendor': save_result['vendor'],
                'file': save_result['filename'],
                'product': product_data['name']
            }
            
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}
    
    def process_all(self):
        """모든 파일 처리"""
        txt_files = list(self.cua_dir.glob("*.txt"))
        
        print(f"\n=== Type D 템플릿 기반 생성 시작 ===")
        print(f"템플릿: typeD_genspark_style.html")
        print(f"소스: {self.cua_dir}")
        print(f"출력: {self.output_base}")
        print(f"총 {len(txt_files)}개 파일\n")
        
        success = 0
        failed = 0
        vendors = {}
        
        for i, txt_file in enumerate(txt_files, 1):
            print(f"[{i}/{len(txt_files)}] {txt_file.name} 처리 중...", end="")
            
            result = self.process_file(txt_file)
            
            if result['status'] == 'success':
                success += 1
                vendor = result['vendor']
                vendors[vendor] = vendors.get(vendor, 0) + 1
                print(f" OK [{vendor}]")
            else:
                failed += 1
                print(f" FAIL: {result.get('error', 'Unknown')}")
        
        # 메타데이터 생성
        self.organizer.create_metadata()
        
        # 인덱스 생성
        index_file = self.organizer.create_index_html()
        
        print(f"\n=== 처리 완료 ===")
        print(f"성공: {success}개")
        print(f"실패: {failed}개")
        
        if vendors:
            print(f"\n=== 업체별 현황 ===")
            for vendor, count in sorted(vendors.items()):
                print(f"  {vendor:15} : {count:3}개")
        
        print(f"\n[COMPLETE] Type D 생성 완료!")
        print(f"[INDEX] {index_file}")
        
        # 브라우저에서 열기
        import webbrowser
        webbrowser.open(str(index_file))


def main():
    """메인 실행"""
    generator = ProperTypeDGenerator()
    
    # 샘플 테스트
    print("샘플 파일 테스트 중...")
    sample = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html\temp_txt\131.txt")
    if sample.exists():
        result = generator.process_file(sample)
        if result['status'] == 'success':
            print(f"[OK] 샘플 생성 성공: {result['file']}")
            
            # 전체 처리 여부 확인
            answer = input("\n전체 274개 파일을 처리하시겠습니까? (y/n): ")
            if answer.lower() == 'y':
                generator.process_all()
        else:
            print(f"[FAIL] 샘플 생성 실패: {result.get('error')}")
    else:
        print("샘플 파일을 찾을 수 없습니다")


if __name__ == "__main__":
    main()
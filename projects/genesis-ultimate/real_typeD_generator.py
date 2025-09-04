#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
진짜 Type D 상세페이지 생성기
- txt 파일에서 제품 정보 추출
- AI 스타일로 완전히 새로운 상세페이지 생성
- Genspark 2025 Type D 형식
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
from typing import Dict, List
import random

class RealTypeDGenerator:
    """진짜 Type D 상세페이지 생성"""
    
    def __init__(self):
        self.cua_dir = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content\html\temp_txt")
        self.output_base = Path("output/real_typeD")
        self.output_base.mkdir(parents=True, exist_ok=True)
        
        # 감성 문구 템플릿
        self.headlines = [
            "드디어 찾았다! {product}의 진짜를",
            "이거 먹고 인생 바뀜... {product}",
            "{product}, 왜 이제야 알았을까",
            "38만 구독자가 인정한 {product}",
            "한 번 먹으면 못 끊는 {product}의 비밀"
        ]
        
        self.why_templates = [
            "최고급 원재료만 사용한 프리미엄 품질",
            "전문가가 인정한 맛과 영양",
            "까다로운 제조 과정을 거친 완벽함",
            "합리적인 가격의 최상급 퀄리티",
            "한 번 먹으면 다른 건 못 먹는 중독성"
        ]
    
    def extract_product_info(self, txt_file: Path) -> Dict:
        """txt/HTML에서 제품 정보 추출"""
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
            price_info = self.extract_price(content)
            
            # 이미지 추출
            images = []
            for img in soup.find_all('img', src=True):
                img_url = img['src']
                if 'cafe24' in img_url or 'ecimg' in img_url:
                    images.append(img_url)
            
            # 주요 텍스트 추출
            key_points = []
            for elem in soup.find_all(['h2', 'h3', 'strong']):
                text = elem.get_text(strip=True)
                if text and len(text) > 5 and len(text) < 100:
                    key_points.append(text)
            
            return {
                'name': product_name,
                'price': price_info,
                'images': images[:5],
                'key_points': key_points[:10],
                'number': txt_file.stem
            }
            
        except Exception as e:
            print(f"추출 실패: {e}")
            return None
    
    def extract_price(self, content: str) -> Dict:
        """가격 정보 추출"""
        price_info = {
            'original': None,
            'sale': None,
            'discount': None
        }
        
        # 가격 패턴 찾기
        price_pattern = r'(\d{1,3}[,\d]*)\s*원'
        prices = re.findall(price_pattern, content)
        
        if prices:
            # 숫자만 추출
            price_nums = []
            for p in prices[:5]:  # 상위 5개만
                num = int(p.replace(',', ''))
                if 1000 <= num <= 1000000:  # 합리적인 가격 범위
                    price_nums.append(num)
            
            if len(price_nums) >= 2:
                price_info['original'] = max(price_nums)
                price_info['sale'] = min(price_nums)
                if price_info['original'] > price_info['sale']:
                    discount = int((1 - price_info['sale']/price_info['original']) * 100)
                    price_info['discount'] = discount
        
        return price_info
    
    def generate_typeD_html(self, product_info: Dict) -> str:
        """Type D 형식 HTML 생성"""
        
        name = product_info.get('name', '제품')
        price = product_info.get('price', {})
        images = product_info.get('images', [])
        key_points = product_info.get('key_points', [])
        
        # 헤드라인 선택
        headline = random.choice(self.headlines).format(product=name)
        
        html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Type D 상세페이지</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Pretendard', -apple-system, sans-serif;
            line-height: 1.6;
            color: #1a1a1a;
            background: #fff;
        }}
        .container {{
            max-width: 860px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        /* Hero Section */
        .hero {{
            text-align: center;
            padding: 60px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 20px;
            margin-bottom: 40px;
        }}
        .hero h1 {{
            font-size: clamp(28px, 5vw, 48px);
            font-weight: 900;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }}
        .hero .subtitle {{
            font-size: 20px;
            opacity: 0.95;
            margin-bottom: 30px;
        }}
        .price-box {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 20px 40px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }}
        .original-price {{
            text-decoration: line-through;
            opacity: 0.7;
            font-size: 18px;
        }}
        .sale-price {{
            font-size: 36px;
            font-weight: 900;
            color: #FFD700;
        }}
        .discount {{
            display: inline-block;
            background: #FF6B6B;
            padding: 5px 15px;
            border-radius: 20px;
            margin-left: 10px;
            font-size: 18px;
        }}
        
        /* Why Section */
        .why-section {{
            background: #f8f9fa;
            padding: 60px 20px;
            border-radius: 20px;
            margin-bottom: 40px;
        }}
        .section-title {{
            font-size: 32px;
            font-weight: 800;
            text-align: center;
            margin-bottom: 40px;
            color: #333;
        }}
        .why-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }}
        .why-card {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            transition: transform 0.3s;
        }}
        .why-card:hover {{
            transform: translateY(-5px);
        }}
        .why-number {{
            display: inline-block;
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 50%;
            text-align: center;
            line-height: 40px;
            font-weight: bold;
            margin-bottom: 15px;
        }}
        .why-title {{
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 10px;
            color: #333;
        }}
        .why-desc {{
            color: #666;
            line-height: 1.8;
        }}
        
        /* Story Section */
        .story-section {{
            padding: 60px 20px;
            text-align: center;
        }}
        .story-content {{
            font-size: 18px;
            line-height: 2;
            color: #555;
            max-width: 700px;
            margin: 0 auto;
        }}
        .highlight {{
            background: linear-gradient(to right, #FFD700 0%, #FFD700 100%);
            background-position: 0 85%;
            background-size: 100% 15%;
            background-repeat: no-repeat;
            padding: 2px 0;
            font-weight: 600;
        }}
        
        /* How Section */
        .how-section {{
            background: #2d3748;
            color: white;
            padding: 60px 20px;
            border-radius: 20px;
            margin-bottom: 40px;
        }}
        .how-steps {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 30px;
            margin-top: 40px;
        }}
        .step {{
            text-align: center;
        }}
        .step-icon {{
            font-size: 48px;
            margin-bottom: 15px;
        }}
        .step-title {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        .step-desc {{
            font-size: 14px;
            opacity: 0.9;
            line-height: 1.6;
        }}
        
        /* Trust Section */
        .trust-section {{
            padding: 60px 20px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 20px;
        }}
        .trust-badges {{
            display: flex;
            justify-content: center;
            gap: 40px;
            flex-wrap: wrap;
            margin-top: 40px;
        }}
        .badge {{
            text-align: center;
        }}
        .badge-icon {{
            font-size: 64px;
            color: #667eea;
            margin-bottom: 10px;
        }}
        .badge-text {{
            font-size: 16px;
            font-weight: 600;
            color: #333;
        }}
        
        /* CTA Section */
        .cta-section {{
            text-align: center;
            padding: 80px 20px;
        }}
        .cta-button {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 60px;
            font-size: 20px;
            font-weight: 700;
            border-radius: 50px;
            text-decoration: none;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
            transition: transform 0.3s;
        }}
        .cta-button:hover {{
            transform: translateY(-3px);
        }}
        
        /* Images */
        .image-gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 40px 20px;
        }}
        .product-image {{
            width: 100%;
            height: 250px;
            object-fit: cover;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Hero Section -->
        <section class="hero">
            <h1>{headline}</h1>
            <p class="subtitle">최씨남매가 직접 검증한 진짜 맛</p>
            {self.generate_price_html(price)}
        </section>
        
        <!-- Why Section -->
        <section class="why-section">
            <h2 class="section-title">🤔 왜 이 제품이어야 할까요?</h2>
            <div class="why-grid">
                {self.generate_why_cards()}
            </div>
        </section>
        
        <!-- Story Section -->
        <section class="story-section">
            <h2 class="section-title">💬 우리의 이야기</h2>
            <div class="story-content">
                <p>
                    처음 <span class="highlight">{name}</span>을 만났을 때의 그 충격을 아직도 잊을 수 없습니다.
                    "이게 정말 같은 제품이 맞나?" 싶을 정도로 <span class="highlight">차원이 다른 맛</span>이었죠.
                </p>
                <p style="margin-top: 20px;">
                    38만 구독자 여러분께 자신있게 추천드립니다.
                    이미 수많은 분들이 재구매하시며 <span class="highlight">인생 제품</span>으로 인정해주셨습니다.
                </p>
                {self.generate_key_points(key_points)}
            </div>
        </section>
        
        <!-- How Section -->
        <section class="how-section">
            <h2 class="section-title">🍳 이렇게 즐기세요</h2>
            <div class="how-steps">
                <div class="step">
                    <div class="step-icon">📦</div>
                    <div class="step-title">Step 1. 개봉</div>
                    <div class="step-desc">신선도를 유지하는 특수 포장으로 안전하게 배송됩니다</div>
                </div>
                <div class="step">
                    <div class="step-icon">🔥</div>
                    <div class="step-title">Step 2. 조리</div>
                    <div class="step-desc">간편하게 데우기만 하면 전문점 못지않은 맛</div>
                </div>
                <div class="step">
                    <div class="step-icon">🍽️</div>
                    <div class="step-title">Step 3. 플레이팅</div>
                    <div class="step-desc">예쁘게 담아내면 근사한 한 끼 완성</div>
                </div>
                <div class="step">
                    <div class="step-icon">😋</div>
                    <div class="step-title">Step 4. 즐기기</div>
                    <div class="step-desc">가족, 친구와 함께 특별한 시간을</div>
                </div>
            </div>
        </section>
        
        <!-- Trust Section -->
        <section class="trust-section">
            <h2 class="section-title">✅ 믿고 구매하세요</h2>
            <div class="trust-badges">
                <div class="badge">
                    <div class="badge-icon">🏆</div>
                    <div class="badge-text">HACCP 인증</div>
                </div>
                <div class="badge">
                    <div class="badge-icon">🥇</div>
                    <div class="badge-text">프리미엄 원재료</div>
                </div>
                <div class="badge">
                    <div class="badge-icon">💯</div>
                    <div class="badge-text">만족도 98%</div>
                </div>
                <div class="badge">
                    <div class="badge-icon">🚚</div>
                    <div class="badge-text">안전 배송</div>
                </div>
            </div>
        </section>
        
        {self.generate_image_gallery(images)}
        
        <!-- CTA Section -->
        <section class="cta-section">
            <h2 class="section-title">🎯 지금이 기회입니다!</h2>
            <p style="font-size: 18px; color: #666; margin: 20px 0;">
                한정 수량 특가! 놓치면 후회하는 그 맛
            </p>
            <a href="#" class="cta-button">지금 바로 구매하기 →</a>
        </section>
    </div>
</body>
</html>"""
        return html
    
    def generate_price_html(self, price: Dict) -> str:
        """가격 표시 HTML"""
        if not price or not price.get('sale'):
            return ""
        
        html = '<div class="price-box">'
        
        if price.get('original'):
            html += f'<div class="original-price">{price["original"]:,}원</div>'
        
        html += f'<div class="sale-price">{price["sale"]:,}원'
        
        if price.get('discount'):
            html += f'<span class="discount">{price["discount"]}% OFF</span>'
        
        html += '</div></div>'
        
        return html
    
    def generate_why_cards(self) -> str:
        """Why 카드 생성"""
        cards = [
            ("최고급 원재료", "엄선된 국내산 재료만을 사용하여 안심하고 드실 수 있습니다"),
            ("전통 제조방식", "오랜 노하우와 정성으로 만든 진짜 맛을 경험하세요"),
            ("합리적 가격", "최상의 품질을 가장 합리적인 가격으로 제공합니다"),
            ("검증된 맛", "38만 구독자가 인정한 믿을 수 있는 제품입니다")
        ]
        
        html = ""
        for i, (title, desc) in enumerate(cards, 1):
            html += f"""
                <div class="why-card">
                    <div class="why-number">{i}</div>
                    <div class="why-title">{title}</div>
                    <div class="why-desc">{desc}</div>
                </div>
            """
        
        return html
    
    def generate_key_points(self, points: List[str]) -> str:
        """핵심 포인트 생성"""
        if not points:
            return ""
        
        html = '<div style="margin-top: 40px; text-align: left; max-width: 600px; margin-left: auto; margin-right: auto;">'
        html += '<h3 style="font-size: 20px; margin-bottom: 20px;">✨ 핵심 포인트</h3>'
        html += '<ul style="list-style: none; padding: 0;">'
        
        for point in points[:5]:
            html += f'<li style="padding: 10px 0; border-bottom: 1px solid #eee;">✓ {point}</li>'
        
        html += '</ul></div>'
        
        return html
    
    def generate_image_gallery(self, images: List[str]) -> str:
        """이미지 갤러리 생성"""
        if not images:
            return ""
        
        html = '<section class="image-gallery">'
        
        for img_url in images[:4]:
            html += f'<img src="{img_url}" alt="제품 이미지" class="product-image" />'
        
        html += '</section>'
        
        return html
    
    def process_sample(self):
        """샘플 파일 처리"""
        # 샘플로 131번 파일 처리
        sample_file = self.cua_dir / "131.txt"
        
        if not sample_file.exists():
            print(f"샘플 파일 없음: {sample_file}")
            return
        
        # 제품 정보 추출
        product_info = self.extract_product_info(sample_file)
        
        if not product_info:
            print("제품 정보 추출 실패")
            return
        
        # Type D HTML 생성
        html_content = self.generate_typeD_html(product_info)
        
        # 파일 저장
        output_file = self.output_base / f"sample_typeD_{product_info['number']}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n=== Type D 상세페이지 생성 완료 ===")
        print(f"제품명: {product_info['name']}")
        print(f"파일: {output_file}")
        
        # 브라우저에서 열기
        import webbrowser
        webbrowser.open(str(output_file))


def main():
    generator = RealTypeDGenerator()
    generator.process_sample()


if __name__ == "__main__":
    main()
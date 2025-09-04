#!/usr/bin/env python
"""
CUA 상세페이지 이미지 자동 생성 시스템
나노바나나 + 템플릿 기반 이미지 생성
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging
import requests
from io import BytesIO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('DetailImageGenerator')

class DetailPageImageGenerator:
    """상세페이지 이미지 생성기"""
    
    def __init__(self):
        self.base_path = Path("C:/Users/8899y/CUA-MASTER")
        self.template_path = self.base_path / "templates/images"
        self.output_path = self.base_path / "output/images"
        self.font_path = self.base_path / "assets/fonts"
        
        # 디렉토리 생성
        self.template_path.mkdir(parents=True, exist_ok=True)
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # 카페24 표준 너비
        self.CANVAS_WIDTH = 860
        
        # 브랜드 색상
        self.BRAND_COLORS = {
            '만원요리': {
                'primary': '#FF6B6B',
                'secondary': '#4ECDC4',
                'accent': '#FFE66D',
                'text': '#2D3436',
                'bg': '#FFFFFF'
            },
            '씨씨더블유': {
                'primary': '#2E86AB',
                'secondary': '#A23B72',
                'accent': '#F18F01',
                'text': '#1A1A2E',
                'bg': '#F7F7F7'
            },
            '인생': {
                'primary': '#6C5CE7',
                'secondary': '#A29BFE',
                'accent': '#FDCB6E',
                'text': '#2D3436',
                'bg': '#FFFFFF'
            }
        }
        
        # 기본 폰트 설정
        self.fonts = self.load_fonts()
        
    def load_fonts(self) -> Dict:
        """폰트 로드"""
        fonts = {}
        try:
            # Windows 기본 폰트 사용
            fonts['title'] = ImageFont.truetype("arial.ttf", 48)
            fonts['subtitle'] = ImageFont.truetype("arial.ttf", 36)
            fonts['body'] = ImageFont.truetype("arial.ttf", 24)
            fonts['caption'] = ImageFont.truetype("arial.ttf", 18)
        except:
            # 폰트 로드 실패시 기본 폰트
            fonts['title'] = ImageFont.load_default()
            fonts['subtitle'] = ImageFont.load_default()
            fonts['body'] = ImageFont.load_default()
            fonts['caption'] = ImageFont.load_default()
            
        return fonts
        
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """HEX 색상을 RGB로 변환"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
    def create_header_section(self, product_data: Dict, brand: str = '만원요리') -> Image.Image:
        """헤더 섹션 생성"""
        
        # 캔버스 생성
        header_height = 400
        header = Image.new('RGB', (self.CANVAS_WIDTH, header_height), 'white')
        draw = ImageDraw.Draw(header)
        
        # 브랜드 색상
        colors = self.BRAND_COLORS.get(brand, self.BRAND_COLORS['만원요리'])
        
        # 상단 배너
        draw.rectangle(
            [(0, 0), (self.CANVAS_WIDTH, 80)],
            fill=self.hex_to_rgb(colors['primary'])
        )
        
        # 브랜드 텍스트
        brand_text = f"{brand} X 최씨남매"
        draw.text(
            (self.CANVAS_WIDTH // 2, 40),
            brand_text,
            fill='white',
            font=self.fonts['subtitle'],
            anchor='mm'
        )
        
        # 상품명
        product_name = product_data.get('name', '프리미엄 상품')
        draw.text(
            (self.CANVAS_WIDTH // 2, 150),
            product_name,
            fill=self.hex_to_rgb(colors['text']),
            font=self.fonts['title'],
            anchor='mm'
        )
        
        # 캐치프레이즈
        catchphrase = product_data.get('catchphrase', '특별한 맛의 경험')
        draw.text(
            (self.CANVAS_WIDTH // 2, 220),
            catchphrase,
            fill=self.hex_to_rgb(colors['secondary']),
            font=self.fonts['subtitle'],
            anchor='mm'
        )
        
        # 구분선
        draw.line(
            [(100, 280), (self.CANVAS_WIDTH - 100, 280)],
            fill=self.hex_to_rgb(colors['accent']),
            width=3
        )
        
        # 핵심 특징 3가지
        features = product_data.get('features', ['프리미엄 재료', '간편 조리', '맛있는 한끼'])
        feature_y = 320
        feature_width = self.CANVAS_WIDTH // 3
        
        for i, feature in enumerate(features[:3]):
            x = feature_width * i + feature_width // 2
            
            # 아이콘 배경
            draw.ellipse(
                [(x - 30, feature_y - 30), (x + 30, feature_y + 30)],
                fill=self.hex_to_rgb(colors['accent'])
            )
            
            # 특징 텍스트
            draw.text(
                (x, feature_y + 50),
                feature,
                fill=self.hex_to_rgb(colors['text']),
                font=self.fonts['body'],
                anchor='mm'
            )
            
        return header
        
    def create_product_showcase(self, product_data: Dict, image_path: Optional[str] = None) -> Image.Image:
        """상품 쇼케이스 섹션"""
        
        showcase_height = 600
        showcase = Image.new('RGB', (self.CANVAS_WIDTH, showcase_height), 'white')
        draw = ImageDraw.Draw(showcase)
        
        # 배경 그라데이션 효과
        for i in range(showcase_height):
            gray = 255 - int((i / showcase_height) * 20)
            draw.line([(0, i), (self.CANVAS_WIDTH, i)], fill=(gray, gray, gray))
            
        # 상품 이미지 영역
        if image_path and Path(image_path).exists():
            product_img = Image.open(image_path)
            # 리사이즈
            product_img.thumbnail((500, 400), Image.Resampling.LANCZOS)
            # 중앙 배치
            x = (self.CANVAS_WIDTH - product_img.width) // 2
            y = (showcase_height - product_img.height) // 2
            showcase.paste(product_img, (x, y))
        else:
            # 플레이스홀더
            draw.rectangle(
                [(180, 100), (680, 500)],
                fill=(240, 240, 240),
                outline=(200, 200, 200),
                width=2
            )
            draw.text(
                (self.CANVAS_WIDTH // 2, 300),
                "상품 이미지",
                fill=(150, 150, 150),
                font=self.fonts['title'],
                anchor='mm'
            )
            
        return showcase
        
    def create_cooking_guide(self, product_data: Dict) -> Image.Image:
        """조리 가이드 섹션"""
        
        guide_height = 500
        guide = Image.new('RGB', (self.CANVAS_WIDTH, guide_height), (250, 250, 250))
        draw = ImageDraw.Draw(guide)
        
        # 제목
        draw.text(
            (self.CANVAS_WIDTH // 2, 50),
            "간편 조리법",
            fill=(50, 50, 50),
            font=self.fonts['title'],
            anchor='mm'
        )
        
        # 조리 단계
        steps = product_data.get('cooking_steps', [
            "1. 포장을 개봉합니다",
            "2. 팬에 기름을 두릅니다",
            "3. 중불에서 5-7분 조리합니다",
            "4. 맛있게 즐깁니다"
        ])
        
        step_height = 80
        start_y = 120
        
        for i, step in enumerate(steps):
            y = start_y + (i * step_height)
            
            # 단계 번호 원
            draw.ellipse(
                [(50, y - 25), (100, y + 25)],
                fill=(255, 107, 107),
                outline='white',
                width=3
            )
            draw.text(
                (75, y),
                str(i + 1),
                fill='white',
                font=self.fonts['subtitle'],
                anchor='mm'
            )
            
            # 단계 설명
            draw.text(
                (130, y),
                step.split('. ', 1)[1] if '. ' in step else step,
                fill=(80, 80, 80),
                font=self.fonts['body'],
                anchor='lm'
            )
            
        # 조리 시간 정보
        info_y = start_y + (len(steps) * step_height) + 30
        
        cooking_time = product_data.get('cooking_time', '10분')
        difficulty = product_data.get('difficulty', '쉬움')
        servings = product_data.get('servings', '2인분')
        
        info_items = [
            f"조리시간: {cooking_time}",
            f"난이도: {difficulty}",
            f"분량: {servings}"
        ]
        
        for i, info in enumerate(info_items):
            x = 200 + (i * 200)
            draw.text(
                (x, info_y),
                info,
                fill=(100, 100, 100),
                font=self.fonts['body'],
                anchor='mm'
            )
            
        return guide
        
    def create_nutrition_info(self, product_data: Dict) -> Image.Image:
        """영양 정보 섹션"""
        
        nutrition_height = 400
        nutrition = Image.new('RGB', (self.CANVAS_WIDTH, nutrition_height), 'white')
        draw = ImageDraw.Draw(nutrition)
        
        # 제목
        draw.text(
            (self.CANVAS_WIDTH // 2, 40),
            "영양 정보",
            fill=(50, 50, 50),
            font=self.fonts['subtitle'],
            anchor='mm'
        )
        
        # 영양 정보 테이블
        nutrition_data = product_data.get('nutrition', {
            '열량': '250kcal',
            '탄수화물': '30g',
            '단백질': '15g',
            '지방': '10g',
            '나트륨': '500mg'
        })
        
        # 테이블 그리기
        table_x = 100
        table_y = 100
        row_height = 40
        
        # 헤더
        draw.rectangle(
            [(table_x, table_y), (self.CANVAS_WIDTH - table_x, table_y + row_height)],
            fill=(240, 240, 240),
            outline=(200, 200, 200)
        )
        
        col_width = (self.CANVAS_WIDTH - 2 * table_x) // 2
        
        for i, (key, value) in enumerate(nutrition_data.items()):
            y = table_y + (i + 1) * row_height
            
            # 행 배경 (짝수 행)
            if i % 2 == 0:
                draw.rectangle(
                    [(table_x, y), (self.CANVAS_WIDTH - table_x, y + row_height)],
                    fill=(250, 250, 250)
                )
                
            # 테두리
            draw.rectangle(
                [(table_x, y), (self.CANVAS_WIDTH - table_x, y + row_height)],
                outline=(200, 200, 200)
            )
            
            # 영양소명
            draw.text(
                (table_x + 20, y + row_height // 2),
                key,
                fill=(80, 80, 80),
                font=self.fonts['body'],
                anchor='lm'
            )
            
            # 함량
            draw.text(
                (table_x + col_width + 20, y + row_height // 2),
                value,
                fill=(100, 100, 100),
                font=self.fonts['body'],
                anchor='lm'
            )
            
        return nutrition
        
    def create_footer_section(self, brand: str = '만원요리') -> Image.Image:
        """푸터 섹션"""
        
        footer_height = 200
        footer = Image.new('RGB', (self.CANVAS_WIDTH, footer_height), (50, 50, 50))
        draw = ImageDraw.Draw(footer)
        
        # 브랜드 정보
        draw.text(
            (self.CANVAS_WIDTH // 2, 50),
            f"{brand} X 최씨남매",
            fill='white',
            font=self.fonts['subtitle'],
            anchor='mm'
        )
        
        # 문의 정보
        contact_info = [
            "고객센터: 1588-0000",
            "운영시간: 평일 09:00 - 18:00",
            "www.manwonyori.com"
        ]
        
        for i, info in enumerate(contact_info):
            draw.text(
                (self.CANVAS_WIDTH // 2, 90 + i * 30),
                info,
                fill=(200, 200, 200),
                font=self.fonts['caption'],
                anchor='mm'
            )
            
        return footer
        
    def combine_sections(self, sections: List[Image.Image]) -> Image.Image:
        """섹션들을 하나의 이미지로 결합"""
        
        # 전체 높이 계산
        total_height = sum(section.height for section in sections)
        
        # 캔버스 생성
        combined = Image.new('RGB', (self.CANVAS_WIDTH, total_height), 'white')
        
        # 섹션 붙이기
        current_y = 0
        for section in sections:
            combined.paste(section, (0, current_y))
            current_y += section.height
            
        return combined
        
    def generate_detail_page(self, product_data: Dict, output_filename: str = None) -> Path:
        """상세페이지 전체 이미지 생성"""
        
        logger.info(f"Generating detail page for: {product_data.get('name', 'Unknown')}")
        
        # 브랜드 추출
        brand = product_data.get('brand', '만원요리')
        
        # 각 섹션 생성
        sections = []
        
        # 1. 헤더
        header = self.create_header_section(product_data, brand)
        sections.append(header)
        
        # 2. 상품 쇼케이스
        showcase = self.create_product_showcase(product_data)
        sections.append(showcase)
        
        # 3. 조리 가이드
        cooking = self.create_cooking_guide(product_data)
        sections.append(cooking)
        
        # 4. 영양 정보
        nutrition = self.create_nutrition_info(product_data)
        sections.append(nutrition)
        
        # 5. 푸터
        footer = self.create_footer_section(brand)
        sections.append(footer)
        
        # 섹션 결합
        detail_page = self.combine_sections(sections)
        
        # 저장
        if not output_filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            product_name = product_data.get('name', 'product').replace(' ', '_')
            output_filename = f"detail_{product_name}_{timestamp}.jpg"
            
        output_path = self.output_path / output_filename
        detail_page.save(output_path, 'JPEG', quality=90)
        
        logger.info(f"Detail page saved: {output_path}")
        
        # 메타데이터 저장
        metadata = {
            'product': product_data,
            'generated_at': datetime.now().isoformat(),
            'dimensions': {
                'width': detail_page.width,
                'height': detail_page.height
            },
            'sections': len(sections),
            'file': str(output_path)
        }
        
        metadata_path = output_path.with_suffix('.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
            
        return output_path
        
    def batch_generate(self, products: List[Dict]) -> List[Path]:
        """여러 상품 일괄 처리"""
        
        generated_files = []
        
        for product in products:
            try:
                output_path = self.generate_detail_page(product)
                generated_files.append(output_path)
            except Exception as e:
                logger.error(f"Error generating detail page for {product.get('name')}: {e}")
                
        logger.info(f"Generated {len(generated_files)} detail pages")
        
        return generated_files


class NanoBananaImageEnhancer:
    """나노바나나 이미지 향상 시스템"""
    
    def __init__(self):
        self.styles = {
            'korean_traditional': {
                'prompt_prefix': '한국 전통 스타일, 한정식, 놋그릇,',
                'color_filter': 'warm'
            },
            'modern_minimal': {
                'prompt_prefix': '모던 미니멀, 깔끔한, 고급 레스토랑,',
                'color_filter': 'cool'
            },
            'home_style': {
                'prompt_prefix': '집밥 스타일, 따뜻한, 가정적인,',
                'color_filter': 'natural'
            },
            'premium': {
                'prompt_prefix': '프리미엄, 럭셔리, 고급,',
                'color_filter': 'vibrant'
            }
        }
        
    def generate_prompt(self, product_name: str, style: str = 'korean_traditional') -> str:
        """AI 이미지 생성용 프롬프트 생성"""
        
        style_config = self.styles.get(style, self.styles['korean_traditional'])
        
        prompt = f"{style_config['prompt_prefix']} {product_name}, "
        prompt += "food photography, professional lighting, 8k, ultra detailed, "
        prompt += "appetizing, delicious looking, commercial quality"
        
        return prompt
        
    def apply_style_filter(self, image: Image.Image, style: str) -> Image.Image:
        """스타일 필터 적용"""
        
        style_config = self.styles.get(style, {})
        filter_type = style_config.get('color_filter', 'natural')
        
        if filter_type == 'warm':
            # 따뜻한 톤
            r, g, b = image.split()
            r = r.point(lambda i: i * 1.1)
            g = g.point(lambda i: i * 1.05)
            image = Image.merge('RGB', (r, g, b))
            
        elif filter_type == 'cool':
            # 차가운 톤
            r, g, b = image.split()
            b = b.point(lambda i: i * 1.1)
            g = g.point(lambda i: i * 1.05)
            image = Image.merge('RGB', (r, g, b))
            
        elif filter_type == 'vibrant':
            # 선명한 톤
            from PIL import ImageEnhance
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(1.3)
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.1)
            
        return image


if __name__ == "__main__":
    # 테스트
    generator = DetailPageImageGenerator()
    
    # 테스트 상품 데이터
    test_product = {
        'name': '[씨씨더블유]명품 양념LA꽃갈비 500g',
        'brand': '씨씨더블유',
        'catchphrase': '프리미엄 양념의 깊은 맛',
        'features': ['24시간 숙성', '특제 양념', '간편 조리'],
        'cooking_steps': [
            '1. 포장을 개봉합니다',
            '2. 팬을 달군 후 기름을 두릅니다',
            '3. 중불에서 5-7분간 굽습니다',
            '4. 노릇하게 구워지면 완성'
        ],
        'cooking_time': '10분',
        'difficulty': '쉬움',
        'servings': '2-3인분',
        'nutrition': {
            '열량': '380kcal',
            '탄수화물': '25g',
            '단백질': '28g',
            '지방': '18g',
            '나트륨': '680mg'
        }
    }
    
    # 상세페이지 생성
    output = generator.generate_detail_page(test_product)
    print(f"Generated detail page: {output}")
    
    # 나노바나나 프롬프트 생성
    enhancer = NanoBananaImageEnhancer()
    prompt = enhancer.generate_prompt(test_product['name'], 'premium')
    print(f"AI Image Prompt: {prompt}")
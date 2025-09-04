"""
템플릿 매니저 - AI 시스템과 완벽 연동
3가지 템플릿 자동 선택 및 렌더링
"""
import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib
from jinja2 import Environment, FileSystemLoader

class TemplateManager:
    """템플릿 매니저 - AI 생성 콘텐츠를 템플릿에 자동 적용"""
    
    def __init__(self, template_dir: str = None):
        if template_dir is None:
            template_dir = Path(__file__).parent / "templates"
        
        self.template_dir = Path(template_dir)
        self.template_dir.mkdir(exist_ok=True, parents=True)
        
        # Jinja2 환경 설정
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=True
        )
        
        # 템플릿 정보
        self.templates = {
            'typeA': {
                'name': '감정 임팩트형',
                'file': 'typeA_emotional_impact.html',
                'description': '첫 3초에 감정적 충격으로 시선 집중',
                'best_for': ['신제품', '트렌디한 상품', '충동구매 유도'],
                'target_customer': '충동구매형 고객',
                'difficulty': 'easy'
            },
            'typeB': {
                'name': '신뢰 구축형',
                'file': 'typeB_trust_building.html', 
                'description': '만원요리 브랜드 신뢰도 극대화',
                'best_for': ['베스트셀러', '검증된 상품', '신뢰도 중요'],
                'target_customer': '신중한 구매 성향',
                'difficulty': 'medium'
            },
            'typeC': {
                'name': '스토리텔링형',
                'file': 'typeC_storytelling.html',
                'description': '감정적 여정을 시각적으로 표현',
                'best_for': ['프리미엄 제품', '스토리 있는 상품', '감동 마케팅'],
                'target_customer': '감정적 구매 성향',
                'difficulty': 'hard'
            },
            'typeD': {
                'name': 'Genspark 스타일 2025형',
                'file': 'typeD_genspark_style.html',
                'description': '섹션별 구성의 현대적 디자인 (Why/Story/How/Trust)',
                'best_for': ['모든 제품', '종합적 정보 전달', '전문적 프레젠테이션'],
                'target_customer': '정보 중심 구매자',
                'difficulty': 'premium'
            }
        }
        
    def recommend_template(self, product_info: Dict[str, Any]) -> str:
        """제품 정보 기반 템플릿 추천"""
        
        # 제품 특성 분석
        name = product_info.get('name', '').lower()
        description = product_info.get('description', '').lower()
        price = product_info.get('price', 0)
        
        # 추천 점수 계산
        scores = {'typeA': 0, 'typeB': 0, 'typeC': 0, 'typeD': 0}
        
        # 신제품/트렌디 키워드 → Type A
        trendy_keywords = ['신상', '신제품', '한정', '특별', '핫한', '화제', '인기', '신선']
        for keyword in trendy_keywords:
            if keyword in name or keyword in description:
                scores['typeA'] += 2
                
        # 검증/인증 키워드 → Type B  
        trust_keywords = ['인증', '검증', '베스트', '1위', '추천', '만원요리', '최씨남매']
        for keyword in trust_keywords:
            if keyword in name or keyword in description:
                scores['typeB'] += 2
                
        # 스토리/감정 키워드 → Type C
        story_keywords = ['전통', '수제', '정성', '엄마', '할머니', '비법', '특별한', '진짜']
        for keyword in story_keywords:
            if keyword in name or keyword in description:
                scores['typeC'] += 2
        
        # 종합/전문 키워드 → Type D (Genspark 스타일)
        professional_keywords = ['프리미엄', '종합', '세트', '구성', '패키지', '완벽', '전문', '최고급']
        for keyword in professional_keywords:
            if keyword in name or keyword in description:
                scores['typeD'] += 2
        
        # Type D는 모든 제품에 기본 점수 부여 (범용성)
        scores['typeD'] += 1
        
        # 가격대별 추천
        if isinstance(price, (int, str)):
            try:
                price_num = int(str(price).replace(',', '').replace('원', ''))
                if price_num < 10000:
                    scores['typeA'] += 1  # 저가 → 임팩트형
                elif price_num > 30000:
                    scores['typeC'] += 1  # 고가 → 스토리텔링형
                else:
                    scores['typeB'] += 1  # 중가 → 신뢰형
            except:
                pass
        
        # 최고 점수 템플릿 선택 (동점이면 typeB 기본)
        max_score = max(scores.values())
        if max_score == 0:
            return 'typeB'  # 기본값
            
        for template_type, score in scores.items():
            if score == max_score:
                return template_type
                
        return 'typeB'
    
    def prepare_template_data(self, product_info: Dict[str, Any], 
                            ai_content: Dict[str, Any],
                            template_type: str = None) -> Dict[str, Any]:
        """AI 생성 콘텐츠를 템플릿 데이터로 변환"""
        
        if template_type is None:
            template_type = self.recommend_template(product_info)
        
        # 기본 데이터
        base_data = {
            'product_name': product_info.get('name', ''),
            'product_description': product_info.get('description', ''),
            'main_image_url': self._get_main_image(product_info),
            'additional_images': product_info.get('images', []),
            'final_price': product_info.get('price', ''),
            'original_price': product_info.get('original_price'),
            'discount_rate': product_info.get('discount_rate'),
            'generated_at': datetime.now().isoformat(),
            'template_type': template_type
        }
        
        # 템플릿별 특화 데이터
        if template_type == 'typeA':
            return self._prepare_typeA_data(base_data, ai_content)
        elif template_type == 'typeB':
            return self._prepare_typeB_data(base_data, ai_content)
        elif template_type == 'typeC':
            return self._prepare_typeC_data(base_data, ai_content)
        elif template_type == 'typeD':
            return self._prepare_typeD_data(base_data, ai_content)
        else:
            return base_data
    
    def _prepare_typeA_data(self, base_data: Dict, ai_content: Dict) -> Dict:
        """Type A 감정 임팩트형 데이터 준비"""
        typeA_data = base_data.copy()
        
        typeA_data.update({
            # 감정 임팩트 요소
            'emotional_headline': ai_content.get('emotional_headline', f"🔥 {base_data['product_name']}"),
            'emotional_hook': ai_content.get('emotional_hook', '이거 먹고 인생 바뀜'),
            'emotion_quote': ai_content.get('emotion_quote', '"진짜 놀랐어요..."'),
            'impact_message': ai_content.get('impact_message', '✨ 한 번 맛보면 잊을 수 없어요'),
            'trust_badge': '38만 구독자 인증',
            'verification_badge': '최씨남매 인증',
            'subscriber_count': '38만 검증',
            
            # 콘텐츠 섹션
            'why_title': ai_content.get('why_title', 'Why? 왜 이 제품인가요?'),
            'why_content': ai_content.get('why_content', ''),
            'story_title': ai_content.get('story_title', '감정 스토리'),
            'story_content': ai_content.get('story_content', ''),
            'shipping_title': ai_content.get('shipping_title', '배송정보'),
            'shipping_info': ai_content.get('shipping_info', ''),
            
            # CTA
            'cta_text': ai_content.get('cta_text', '지금 바로 경험하기'),
            'cta_action': 'window.open("https://manwonyori.com", "_blank")'
        })
        
        return typeA_data
    
    def _prepare_typeB_data(self, base_data: Dict, ai_content: Dict) -> Dict:
        """Type B 신뢰 구축형 데이터 준비"""
        typeB_data = base_data.copy()
        
        typeB_data.update({
            # 신뢰 요소
            'brand_logo_url': ai_content.get('brand_logo_url', base_data['main_image_url']),
            'subscriber_count': '38만 구독자가',
            'subscriber_count_short': '38만',
            'video_views_short': '1200만',
            'satisfaction_rate': ai_content.get('satisfaction_rate', '95'),
            'trust_percentage': ai_content.get('trust_percentage', '98'),
            
            # 정보 카드
            'why_title': ai_content.get('why_title', 'Why? 왜 이 제품인가요?'),
            'why_content': ai_content.get('why_content', ''),
            'story_title': ai_content.get('story_title', '실제 후기'),
            'story_content': ai_content.get('story_content', ''),
            'shipping_title': ai_content.get('shipping_title', '배송 안내'),
            'shipping_info': ai_content.get('shipping_info', ''),
            'additional_benefits': ai_content.get('additional_benefits'),
            
            # CTA
            'guarantee_text': ai_content.get('guarantee_text', '38만 구독자가 검증한 신뢰도'),
            'cta_text': ai_content.get('cta_text', '검증된 맛 경험하기'),
            'cta_action': 'window.open("https://manwonyori.com", "_blank")'
        })
        
        return typeB_data
    
    def _prepare_typeC_data(self, base_data: Dict, ai_content: Dict) -> Dict:
        """Type C 스토리텔링형 데이터 준비"""
        typeC_data = base_data.copy()
        
        # 스토리 챕터별 데이터
        typeC_data.update({
            # Chapter 1: 문제
            'chapter1_title': ai_content.get('chapter1_title', '그 날의 고민'),
            'chapter1_emotion': ai_content.get('chapter1_emotion', '"또 뭘 먹지?"'),
            'chapter1_content': ai_content.get('chapter1_content', ''),
            'chapter1_image': ai_content.get('chapter1_image'),
            
            # Chapter 2: 발견
            'chapter2_title': ai_content.get('chapter2_title', '운명적 만남'),
            'chapter2_emotion': ai_content.get('chapter2_emotion', '"이거다!"'),
            'chapter2_content': ai_content.get('chapter2_content', ''),
            'discovery_moment': ai_content.get('discovery_moment', '완벽한 맛을'),
            
            # Chapter 3: 경험
            'chapter3_title': ai_content.get('chapter3_title', '첫 경험'),
            'chapter3_emotion': ai_content.get('chapter3_emotion', '"진짜 놀랐어요!"'),
            'chapter3_content': ai_content.get('chapter3_content', ''),
            'experience_images': ai_content.get('experience_images', []),
            
            # Chapter 4: 변화 (선택적)
            'chapter4_title': ai_content.get('chapter4_title'),
            'chapter4_emotion': ai_content.get('chapter4_emotion'),
            'chapter4_content': ai_content.get('chapter4_content'),
            
            # Ending
            'ending_title': ai_content.get('ending_title', '행복한 결말'),
            'ending_emotion': ai_content.get('ending_emotion', '"이제 내 최애!"'),
            'ending_content': ai_content.get('ending_content', ''),
            'testimonial_quote': ai_content.get('testimonial_quote', '정말 만족해요!'),
            
            # 가격 스토리
            'price_narrative': ai_content.get('price_narrative', '이 모든 감동을 경험할 수 있는 기회'),
            'price_context': ai_content.get('price_context', '특별한 가격으로 만나보세요'),
            
            # 최종 CTA
            'final_cta_headline': ai_content.get('final_cta_headline', '나도 이 스토리의 주인공 되기'),
            'final_cta_subtext': ai_content.get('final_cta_subtext', '당신만의 감동 스토리를 시작하세요'),
            'cta_text': ai_content.get('cta_text', '내 스토리 시작하기'),
            'cta_action': 'window.open("https://manwonyori.com", "_blank")'
        })
        
        return typeC_data
    
    def _prepare_typeD_data(self, base_data: Dict, ai_content: Dict) -> Dict:
        """Type D Genspark 스타일 2025형 데이터 준비"""
        typeD_data = base_data.copy()
        
        # Genspark 스타일 섹션별 데이터
        typeD_data.update({
            # Header Section
            'main_headline': ai_content.get('main_headline', f'"이거 먹고 인생 바뀜" {base_data["product_name"]}의 이야기'),
            'sub_headline': ai_content.get('sub_headline', '38만 구독자들이 숨기고 싶어한 바로 그 제품'),
            
            # Why Section
            'why_title': ai_content.get('why_title', 'Why? 왜 이 제품이어야 할까요?'),
            'why_reason1_title': ai_content.get('why_reason1_title', '첫 번째 이유'),
            'why_reason1_content': ai_content.get('why_reason1_content', ''),
            'why_reason2_title': ai_content.get('why_reason2_title', '두 번째 이유'),
            'why_reason2_content': ai_content.get('why_reason2_content', ''),
            
            # Story Section
            'story_title': ai_content.get('story_title', '그날, 진짜 충격이었어요'),
            'story_intro': ai_content.get('story_intro', ''),
            'story_highlight1': ai_content.get('story_highlight1', ''),
            'story_middle': ai_content.get('story_middle', ''),
            'story_experience': ai_content.get('story_experience', ''),
            'story_highlight2': ai_content.get('story_highlight2', ''),
            'story_conclusion': ai_content.get('story_conclusion', ''),
            
            # Shipping Section
            'shipping_title': ai_content.get('shipping_title', '배송비 절약의 기회!'),
            'shipping_benefit1_title': ai_content.get('shipping_benefit1_title', '합배송 혜택'),
            'shipping_benefit1_desc': ai_content.get('shipping_benefit1_desc', '최씨남매 다른 상품과 함께 구매시 배송비 절약'),
            'shipping_benefit2_title': ai_content.get('shipping_benefit2_title', '카카오채널 할인'),
            'shipping_benefit2_desc': ai_content.get('shipping_benefit2_desc', '친구 추가하고 추가 할인 혜택 받기'),
            
            # How Section
            'how_title': ai_content.get('how_title', 'How? 이렇게 즐기세요!'),
            'how_prepare_title': ai_content.get('how_prepare_title', '간편 조리법'),
            'how_step1': ai_content.get('how_step1', '해동하기'),
            'how_step2': ai_content.get('how_step2', '조리하기'),
            'how_step3': ai_content.get('how_step3', '완성!'),
            'how_usage_title': ai_content.get('how_usage_title', '완벽한 활용법'),
            'usage_case1_title': ai_content.get('usage_case1_title', '혼술 야식'),
            'usage_case1_desc': ai_content.get('usage_case1_desc', '1인분 완벽'),
            'usage_case2_title': ai_content.get('usage_case2_title', '가족 모임'),
            'usage_case2_desc': ai_content.get('usage_case2_desc', '함께 나눠먹기'),
            'usage_case3_title': ai_content.get('usage_case3_title', '홈파티'),
            'usage_case3_desc': ai_content.get('usage_case3_desc', '손님 접대용'),
            
            # Trust Section
            'trust_title': ai_content.get('trust_title', 'Trust! 믿을 수 있는 이유'),
            'trust_icon1': ai_content.get('trust_icon1', 'fas fa-cog'),
            'trust_point1_title': ai_content.get('trust_point1_title', '전문 기술'),
            'trust_point1_desc': ai_content.get('trust_point1_desc', '특별한 제조 공법'),
            'trust_icon2': ai_content.get('trust_icon2', 'fas fa-award'),
            'trust_point2_title': ai_content.get('trust_point2_title', '검증된 맛'),
            'trust_point2_desc': ai_content.get('trust_point2_desc', '수많은 리뷰어 인증'),
            'trust_icon3': ai_content.get('trust_icon3', 'fas fa-youtube'),
            'trust_point3_title': ai_content.get('trust_point3_title', '38만 구독자 인증'),
            'trust_point3_desc': ai_content.get('trust_point3_desc', '만원요리 최씨남매 검증'),
            
            # Product Info
            'product_images': base_data.get('additional_images', []),
            'product_spec1_title': ai_content.get('product_spec1_title', '용량'),
            'product_spec1_value': ai_content.get('product_spec1_value', ''),
            'product_spec2_title': ai_content.get('product_spec2_title', '보관방법'),
            'product_spec2_value': ai_content.get('product_spec2_value', '냉동보관'),
            'product_spec3_title': ai_content.get('product_spec3_title', '유통기한'),
            'product_spec3_value': ai_content.get('product_spec3_value', '제조일로부터 1년')
        })
        
        return typeD_data
    
    def _get_main_image(self, product_info: Dict) -> str:
        """메인 이미지 URL 추출"""
        images = product_info.get('images', [])
        if images and len(images) > 0:
            return images[0]
        
        # 기본 이미지 (만원요리 로고 등)
        return "https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/default.jpg"
    
    def render_template(self, template_type: str, data: Dict[str, Any]) -> str:
        """템플릿 렌더링"""
        try:
            template_file = self.templates[template_type]['file']
            template = self.env.get_template(template_file)
            return template.render(**data)
        except Exception as e:
            print(f"Template rendering error: {e}")
            return self._generate_fallback_html(data)
    
    def _generate_fallback_html(self, data: Dict) -> str:
        """폴백 HTML (템플릿 로딩 실패시)"""
        return f"""
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <title>{data.get('product_name', '제품')}</title>
        </head>
        <body>
            <h1>{data.get('product_name', '제품')}</h1>
            <p>{data.get('product_description', '')}</p>
            <p>가격: {data.get('final_price', '')}원</p>
        </body>
        </html>
        """
    
    def generate_complete_page(self, product_info: Dict[str, Any], 
                             ai_content: Dict[str, Any],
                             template_type: str = None) -> Dict[str, Any]:
        """완전한 페이지 생성 (통합 함수)"""
        
        # 1. 템플릿 추천
        if template_type is None:
            template_type = self.recommend_template(product_info)
        
        print(f"Recommended template: {template_type} ({self.templates[template_type]['name']})")
        
        # 2. 템플릿 데이터 준비
        template_data = self.prepare_template_data(product_info, ai_content, template_type)
        
        # 3. HTML 렌더링
        html_content = self.render_template(template_type, template_data)
        
        # 4. 결과 반환
        result = {
            'html': html_content,
            'template_type': template_type,
            'template_name': self.templates[template_type]['name'],
            'template_data': template_data,
            'recommendation_reason': self._get_recommendation_reason(product_info, template_type),
            'generated_at': datetime.now().isoformat(),
            'file_size_kb': len(html_content.encode('utf-8')) / 1024
        }
        
        return result
    
    def _get_recommendation_reason(self, product_info: Dict, template_type: str) -> str:
        """템플릿 추천 이유"""
        name = product_info.get('name', '').lower()
        
        if template_type == 'typeA':
            return "신제품 또는 트렌디한 특성으로 감정 임팩트형 추천"
        elif template_type == 'typeB':
            return "검증된 상품 또는 신뢰도 중요으로 신뢰 구축형 추천"
        elif template_type == 'typeC':
            return "스토리 요소 또는 프리미엄 특성으로 스토리텔링형 추천"
        else:
            return "기본 추천"
    
    def get_template_info(self) -> Dict[str, Any]:
        """템플릿 정보 반환"""
        return {
            'templates': self.templates,
            'template_dir': str(self.template_dir),
            'available_templates': list(self.templates.keys()),
            'total_templates': len(self.templates)
        }
    
    def save_generated_page(self, result: Dict, output_dir: str = None) -> str:
        """생성된 페이지를 파일로 저장"""
        if output_dir is None:
            output_dir = Path(__file__).parent / "output" / "template_generated"
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True, parents=True)
        
        # 파일명 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        product_name = result['template_data'].get('product_name', 'product').replace(' ', '_')
        template_type = result['template_type']
        
        filename = f"{product_name}_{template_type}_{timestamp}.html"
        filepath = output_path / filename
        
        # HTML 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(result['html'])
        
        # 메타데이터 저장
        meta_filename = f"{product_name}_{template_type}_{timestamp}_meta.json"
        meta_filepath = output_path / meta_filename
        
        meta_data = {
            'template_type': result['template_type'],
            'template_name': result['template_name'],
            'recommendation_reason': result['recommendation_reason'],
            'file_size_kb': result['file_size_kb'],
            'generated_at': result['generated_at'],
            'html_file': filename
        }
        
        with open(meta_filepath, 'w', encoding='utf-8') as f:
            json.dump(meta_data, f, ensure_ascii=False, indent=2)
        
        print(f"Generated: {filename} ({result['file_size_kb']:.1f}KB)")
        return str(filepath)


# 테스트 함수
def test_template_manager():
    """템플릿 매니저 테스트"""
    manager = TemplateManager()
    
    # 테스트 데이터
    test_product = {
        'name': '취영루 오리지널 교자만두',
        'description': '79년 전통의 정통 중화요리 전문점 취영루의 시그니처 교자만두',
        'price': '15,900',
        'images': [
            'https://ecimg.cafe24img.com/pg1966b42244249021/manwonyori/web/product/life/gambas336g/gambas336g-1.jpg'
        ]
    }
    
    test_ai_content = {
        'emotional_headline': '🔥 79년 전통의 진짜 맛이 이거구나!',
        'emotional_hook': '첫 맛에 반한 그 순간...',
        'emotion_quote': '"이게 진짜 교자만두구나..."',
        'why_content': '79년 노하우가 만든 차별화된 맛과 식감',
        'story_content': '할아버지 대부터 전해져 내려온 비법 레시피로 만든 정통 교자만두',
        'shipping_info': '전국 배송 가능 • 냉동 포장 • 당일 출고'
    }
    
    # 템플릿 생성 테스트
    result = manager.generate_complete_page(test_product, test_ai_content)
    
    print(f"Template: {result['template_name']}")
    print(f"Reason: {result['recommendation_reason']}")
    print(f"Size: {result['file_size_kb']:.1f}KB")
    
    # 파일 저장
    saved_file = manager.save_generated_page(result)
    print(f"Saved: {saved_file}")
    
    return result

if __name__ == "__main__":
    test_template_manager()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
지능형 상품 분류 시스템
- 조건부 키워드 적용
- AI 기반 카테고리 분석
- 원본 데이터 오타 수정
"""

import os
import csv
import json
from datetime import datetime
from typing import Dict, List
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv('../../../shared/config/.env')

class IntelligentSystem:
    """지능형 상품 분류 시스템"""
    
    def __init__(self):
        self.setup_apis()
        
        # 조건부 필수 키워드 (특성에 맞을 때만 적용)
        # AI 기반 조건부 키워드 판단 기준
        self.ai_keyword_criteria = {
            "만원요리": {
                "type": "brand_price",
                "description": "1만원 내외의 가성비 좋은 요리",
                "criteria": "가격이 합리적이고 가성비가 좋은 제품, 서민적인 음식"
            },
            "최씨남매": {
                "type": "brand_target", 
                "description": "젊은 남매가 즐길 만한 트렌디한 음식",
                "criteria": "젊은층 타겟, 트렌디한 음식, SNS용 음식"
            },
            "집밥각": {
                "type": "home_cooking",
                "description": "집에서 편안하게 먹을 수 있는 가정식",
                "criteria": "가정식, 집밥, 편안한 식사, 일상식, 반찬류, 찌개류"
            },
            "술한잔": {
                "type": "alcohol_pairing",
                "description": "술과 함께 즐기기 좋은 안주류",
                "criteria": "안주, 야식, 술안주, 맥주안주, 소주안주, 치킨, 구이류, 매운맛"
            },
            "반찬고민끝": {
                "type": "side_dish",
                "description": "밥과 함께 먹는 반찬이나 밑반찬",
                "criteria": "반찬, 밑반찬, 나물, 김치, 젓갈, 장아찌, 무침류"
            },
            "국물땡김": {
                "type": "soup_dish",
                "description": "국물이 있는 따뜻한 음식",
                "criteria": "국, 찌개, 탕, 스프, 국물요리, 라면, 우동"
            },
            "혼밥만세": {
                "type": "single_meal",
                "description": "혼자 먹기 좋은 1인분 요리",
                "criteria": "1인분, 혼밥, 개별포장, 소용량, 간편식"
            },
            "시간없어": {
                "type": "quick_cook",
                "description": "빠르고 간편하게 조리할 수 있는 음식",
                "criteria": "즉석, 간편조리, 전자레인지, 에어프라이어, 3분요리"
            },
            "힘내자": {
                "type": "nutritious",
                "description": "영양가 있고 건강에 좋은 보양식",
                "criteria": "영양, 건강식, 보양, 단백질, 비타민, 웰빙, 보양식"
            },
            "모임각": {
                "type": "party_food",
                "description": "여러 명이 함께 나눠 먹기 좋은 음식",
                "criteria": "파티용, 대용량, 세트, 모임, 회식, 여러명, 나눠먹기"
            }
        }
        
        # 카테고리별 특성 데이터 (AI 분석 기준)
        self.category_characteristics = {
            53: {  # 육류가공품
                "keywords": ["닭발", "막창", "갈비", "삼겹살", "육류", "고기"],
                "description_patterns": ["직화", "숯불", "바삭", "쫄깃", "육즙", "프리미엄"],
                "cooking_methods": ["구이", "튀김", "볶음"]
            },
            95: {  # 안주류
                "keywords": ["안주", "술안주", "맥주안주", "야식"],
                "description_patterns": ["매콤", "칼칼", "짭조름", "고소"],
                "occasions": ["술자리", "파티", "모임"]
            },
            56: {  # 간편식품
                "keywords": ["간편", "즉석", "혼밥", "1인분"],
                "description_patterns": ["전자레인지", "에어프라이어", "간단조리"],
                "target": ["혼밥족", "바쁜직장인", "학생"]
            },
            97: {  # 수산물가공품
                "keywords": ["갈치", "고등어", "꽃맛살", "어묵", "수산물"],
                "description_patterns": ["오메가3", "DHA", "바다", "신선"],
                "origin": ["해산물", "수산물"]
            },
            98: {  # 냉동피자
                "keywords": ["피자", "포카치아", "치즈"],
                "description_patterns": ["이탈리아", "치즈", "토핑"],
                "cooking": ["오븐", "에어프라이어"]
            },
            102: {  # 반찬류
                "keywords": ["반찬", "밑반찬", "깻잎", "알마늘", "간장"],
                "description_patterns": ["집밥", "전통", "엄마손맛"],
                "purpose": ["밑반찬", "반찬"]
            },
            103: {  # 젓갈류
                "keywords": ["젓갈", "젓", "발효"],
                "description_patterns": ["발효", "숙성", "전통"],
                "preservation": ["발효식품"]
            },
            109: {  # 국물요리
                "keywords": ["찌개", "국", "탕", "국밥"],
                "description_patterns": ["뜨끈", "국물", "든든", "해장"],
                "cooking": ["끓임", "우림"]
            },
            110: {  # 프리미엄
                "keywords": ["프리미엄", "최고급", "특선"],
                "description_patterns": ["최고급", "프리미엄", "특별한"],
                "price_range": ["고가", "프리미엄"]
            }
        }
        
        # 공급사별 우선 규칙 (브랜드 직거래)
        self.supplier_priority_rules = {
            '씨씨더블유': [53, 95, 99, 103, 56, 110],  # 프리미엄 육류안주
            '인생': [56, 97, 102],  # 간편식 가성비
            '태공식품': [97, 99, 103, 56],  # 수산물 전통
            '최씨남매': [56, 97, 102, 109],  # 종합식품
            '피자코리아': [56, 98, 102],  # 피자전문
            '모비딕': [53, 95, 99, 103, 56],  # 육류가공
            '취영루': [56, 97, 102],  # 만두전문  
            '반찬단지': [56, 102, 109]  # 반찬전문
        }
        
        # 원본 데이터 수정 규칙
        self.data_corrections = {
            '꾸븐': '구운',
            '오뎅': '어묵',
            '까망콩': '검은콩',
            '깐마늘': '깐 마늘'
        }
    
    def setup_apis(self):
        """API 설정"""
        self.openai_key = os.getenv('OPENAI_API_KEY')
        if self.openai_key:
            print("OpenAI 키 설정됨")
    
    def correct_original_data(self, product_data: Dict) -> Dict:
        """원본 데이터 오타 수정"""
        corrected_data = product_data.copy()
        
        # 모든 텍스트 필드에서 오타 수정
        text_fields = [
            '상품명', '영문 상품명', '상품명(관리용)', '공급사 상품명',
            '검색엔진최적화(SEO) Title', '검색엔진최적화(SEO) Description', 
            '검색엔진최적화(SEO) Keywords', '검색엔진최적화(SEO) 상품 이미지 Alt 텍스트',
            '상품 요약설명', '상품 간략설명'
        ]
        
        for field in text_fields:
            if field in corrected_data and corrected_data[field]:
                original_text = corrected_data[field]
                current_text = original_text
                
                # 모든 수정 규칙 적용
                for wrong, correct in self.data_corrections.items():
                    if wrong in current_text:
                        current_text = current_text.replace(wrong, correct)
                        print(f"    원본 수정 [{field}]: '{wrong}' → '{correct}'")
                
                corrected_data[field] = current_text
        
        return corrected_data
    
    def generate_consumer_search_keywords_with_ai(self, product_info: Dict, description: str) -> List[str]:
        """AI로 일반 소비자 검색 키워드 생성"""
        if not self.openai_key:
            return []
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_key)
            
            prompt = f"""
            다음 상품에 대해 일반 소비자들이 실제로 검색할 만한 키워드들을 생성해주세요:
            
            상품명: {product_info['clean_name']}
            브랜드: {product_info['brand']}
            설명: {description}
            
            키워드 생성 원칙:
            1. 실제 검색 패턴 반영: 소비자가 네이버, 쿠팡, 구글에서 검색할 만한 모든 키워드
            2. 필수 포함 카테고리 (각 3-5개씩):
               - 제품명 변형: 전체명, 축약, 오타, 유사어 (김치찌개, 김치, 찌개, 김치탕)
               - 재료/성분: 모든 주재료와 부재료 (돼지고기, 두부, 김치, 양파)
               - 조리방법: 전자레인지, 에어프라이어, 끓이기만, 데우기만, 3분조리
               - 용도: 안주, 반찬, 간식, 야식, 도시락, 캠핑, 등산
               - 상황: 혼밥, 가족식사, 술자리, 파티, 모임, 집들이
               - 맛/특성: 매운맛, 순한맛, 얼큰한, 시원한, 진한맛
               - 용량: 1인분, 2인분, 대용량, 소포장, 300g, 500g
               - 브랜드: 브랜드명, 브랜드특성
               - 가격: 가성비, 저렴한, 만원이하, 특가, 할인
               - 트렌드: 인기, 베스트, 추천, 신상품, 화제
            3. SEO 최적화: 실제 검색량 높은 키워드 우선
            4. 최소 35개 키워드 생성 (풍부한 검색 커버리지)
            
            JSON 형식으로만 응답:
            {{
                "consumer_keywords": ["키워드1", "키워드2", "키워드3", ...]
            }}
            """
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "한국 이커머스 검색어 최적화 전문가. 실제 소비자 검색 패턴을 분석하여 키워드 생성."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.85,
                max_tokens=700
            )
            
            content = response.choices[0].message.content.strip()
            if '{' in content and '}' in content:
                json_str = content[content.find('{'):content.rfind('}')+1]
                result = json.loads(json_str)
                keywords = result.get('consumer_keywords', [])
                print(f"    일반 검색어 {len(keywords)}개 AI 생성 완료")
                return keywords[:30]  # 최대 30개
            return []
        except Exception as e:
            print(f"  일반 검색어 AI 생성 오류: {e}")
            return []
    
    def analyze_keyword_suitability_with_ai(self, product_info: Dict, description: str) -> Dict:
        """AI로 키워드 적합성 분석"""
        if not self.openai_key:
            return {}
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_key)
            
            # 키워드 기준 정리
            criteria_text = "\n".join([
                f"- {keyword}: {info['description']} (판단기준: {info['criteria']})"
                for keyword, info in self.ai_keyword_criteria.items()
            ])
            
            prompt = f"""
            다음 상품에 대해 각 키워드의 적합성을 분석해주세요:
            
            상품명: {product_info['clean_name']}
            브랜드: {product_info['brand']}
            설명: {description}
            
            키워드 판단 기준:
            {criteria_text}
            
            중요한 판단 원칙:
            1. 복합적 용도 고려: 하나의 상품이 여러 용도로 사용될 수 있음
            2. 키워드 중복 허용: 여러 키워드가 동시에 적합할 수 있음
            3. 실제 사용 맥락 반영: 
               - 어묵탕/국물요리도 술안주로 많이 사용됨
               - 안주류도 집밥 반찬이 될 수 있음
               - 소용량도 모임때 여러개 주문 가능
               - 반찬류도 술안주가 될 수 있음
            4. 한국 음식 문화 특성 반영
            
            각 키워드별 세부 판단 기준:
            - 술한잔: 술과 함께 먹을 수 있는 모든 음식 (국물요리, 반찬 포함)
            - 반찬고민끝: 밥과 함께 먹을 수 있는 모든 음식
            - 국물땡김: 국물이 있는 모든 음식
            - 집밥각: 집에서 먹을 수 있는 모든 음식 (안주도 포함)
            - 혼밥만세: 1인 적정량이거나 개별 포장된 음식
            - 모임각: 여러명이 함께 먹거나, 여러개 주문할 수 있는 음식
            
            JSON 형식으로만 응답:
            {{
                "suitable_keywords": ["적합한키워드1", "적합한키워드2", ...],
                "reasoning": "전체적인 판단 근거"
            }}
            """
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "한국 음식 키워드 분석 전문가. 상품 특성을 정확히 분석하여 적합한 키워드만 선택."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=400
            )
            
            content = response.choices[0].message.content.strip()
            if '{' in content and '}' in content:
                json_str = content[content.find('{'):content.rfind('}')+1]
                result = json.loads(json_str)
                print(f"    AI 키워드 분석: {result.get('reasoning', '')[:50]}...")
                return result
            return {}
        except Exception as e:
            print(f"  키워드 분석 AI 오류: {e}")
            return {}
    
    def analyze_product_with_ai(self, product_info: Dict) -> Dict:
        """AI를 이용한 상품 분석"""
        if not self.openai_key:
            return None
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_key)
            
            prompt = f"""
            상품 분석 요청:
            
            상품명: {product_info['clean_name']}
            브랜드: {product_info['brand']}
            
            다음 카테고리들 중에서 이 상품에 가장 적합한 카테고리를 분석해주세요:
            
            53: 육류가공품 (닭발, 막창, 갈비 등)
            95: 안주류 (술안주, 맥주안주)
            56: 간편식품 (즉석식품, 혼밥용)
            97: 수산물가공품 (갈치, 고등어, 어묵 등)
            98: 냉동피자류
            102: 반찬류 (깻잎, 알마늘, 전통반찬)
            103: 젓갈류 (발효식품)
            109: 국물요리 (찌개, 탕, 국밥)
            110: 프리미엄 (고급, 특선)
            
            분석 결과를 JSON 형태로 응답:
            {{
                "primary_categories": [가장 적합한 카테고리 번호들],
                "confidence": "높음/중간/낮음",
                "reasoning": "분류 근거 설명"
            }}
            """
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "상품 카테고리 분류 전문가. JSON만 응답."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            content = response.choices[0].message.content.strip()
            if '{' in content and '}' in content:
                json_str = content[content.find('{'):content.rfind('}')+1]
                result = json.loads(json_str)
                return result
            return None
        except Exception as e:
            print(f"  AI 분석 오류: {e}")
            return None
    
    def determine_categories(self, product_info: Dict) -> List[int]:
        """카테고리 결정 - 이중 시스템"""
        brand = product_info.get('brand', '')
        
        # 1단계: 브랜드별 우선 규칙 (직거래 브랜드)
        if brand and brand in self.supplier_priority_rules:
            categories = self.supplier_priority_rules[brand]
            print(f"    브랜드 우선 규칙: {brand} → {categories}")
            return categories
        
        # 2단계: AI 기반 카테고리 분석
        print(f"    AI 카테고리 분석 시작...")
        ai_analysis = self.analyze_product_with_ai(product_info)
        
        if ai_analysis and ai_analysis.get('primary_categories'):
            categories = ai_analysis['primary_categories']
            confidence = ai_analysis.get('confidence', '알수없음')
            reasoning = ai_analysis.get('reasoning', '')
            print(f"    AI 분석 결과: {categories} (신뢰도: {confidence})")
            print(f"    분석 근거: {reasoning}")
            return categories
        
        # 3단계: 기본값
        print(f"    기본 카테고리 적용")
        return [56]
    
    def generate_conditional_keywords(self, product_info: Dict, description: str) -> List[str]:
        """40개 검색어 통합 시스템 - 필수 10개 + 소비자 검색어 30개"""
        print("    40개 검색어 통합 시스템 시작...")
        
        # 1단계: AI 기반 필수 키워드 분석 (최대 10개)
        print("      1단계: 필수 키워드 AI 분석...")
        ai_analysis = self.analyze_keyword_suitability_with_ai(product_info, description)
        
        required_keywords = []
        if ai_analysis and 'suitable_keywords' in ai_analysis:
            required_keywords = ai_analysis['suitable_keywords']
            print(f"        AI 분석 필수 키워드: {len(required_keywords)}개")
            for keyword in required_keywords:
                if keyword in self.ai_keyword_criteria:
                    print(f"          + '{keyword}' (AI분석: 적합)")
        else:
            # AI 실패시 기본 키워드
            required_keywords = ["만원요리", "최씨남매"]
            print("        AI 분석 실패, 기본 키워드 적용")
        
        # 2단계: 소비자 검색 키워드 AI 생성 (최대 30개)
        print("      2단계: 소비자 검색 키워드 AI 생성...")
        consumer_keywords = self.generate_consumer_search_keywords_with_ai(product_info, description)
        
        if consumer_keywords:
            print(f"        AI 생성 소비자 검색어: {len(consumer_keywords)}개")
        else:
            # AI 실패시 기본 소비자 키워드 생성
            print("        AI 실패, 기본 소비자 키워드 생성...")
            consumer_keywords = self.generate_basic_consumer_keywords(product_info, description)
        
        # 3단계: 키워드 통합 및 중복 제거
        all_keywords = required_keywords + consumer_keywords
        
        # 중복 제거하면서 순서 유지
        unique_keywords = []
        seen = set()
        for keyword in all_keywords:
            if keyword not in seen:
                unique_keywords.append(keyword)
                seen.add(keyword)
        
        # 40개 제한
        final_keywords = unique_keywords[:40]
        
        print(f"      최종 통합: {len(final_keywords)}개 키워드")
        print(f"        - 필수 키워드: {len([k for k in final_keywords if k in self.ai_keyword_criteria])}개")
        print(f"        - 소비자 검색어: {len([k for k in final_keywords if k not in self.ai_keyword_criteria])}개")
        
        return final_keywords
    
    def generate_basic_consumer_keywords(self, product_info: Dict, description: str) -> List[str]:
        """AI 실패시 기본 소비자 검색어 생성 - 대폭 확대"""
        product_text = f"{product_info['clean_name']} {description}".lower()
        basic_keywords = []
        
        # 제품명에서 키워드 추출
        name_parts = product_info['clean_name'].replace(',', ' ').replace('(', ' ').replace(')', ' ').split()
        basic_keywords.extend([p for p in name_parts if len(p) > 1])
        
        # 제품 특성별 상세 키워드
        if '매운' in product_text or '매콤' in product_text:
            basic_keywords.extend(['매운맛', '매콤한', '칼칼한', '스파이시', '불닭', '핫', '얼큰한', '화끈한'])
        if '구운' in product_text or '직화' in product_text:
            basic_keywords.extend(['구운', '직화구이', '바삭한', '그릴', '숯불', '바베큐', 'BBQ', '로스트'])
        if any(x in product_text for x in ['찌개', '탕', '국밥']):
            basic_keywords.extend(['국물요리', '뜨끈한', '든든한', '따뜻한', '국', '찌개', '탕', '스프', '수프'])
        if '닭발' in product_text:
            basic_keywords.extend(['닭발', '족발', '쫄깃한', '콜라겐', '무뼈닭발', '닭발볶음', '매운닭발', '닭발요리'])
        if '막창' in product_text:
            basic_keywords.extend(['막창', '곱창', '내장', '술안주', '양념막창', '소막창', '돼지막창', '막창구이'])
        if '어묵' in product_text or '오뎅' in product_text:
            basic_keywords.extend(['어묵', '오뎅', '국물', '간식', '어묵탕', '오뎅탕', '부산어묵', '생선살'])
        if '김치' in product_text:
            basic_keywords.extend(['김치', '발효식품', '한국음식', '배추김치', '숙성', '신김치', '묵은지'])
        if '돼지' in product_text or '소' in product_text:
            basic_keywords.extend(['고기', '육류', '단백질', '불고기', '구이', '삼겹살', '목살'])
        
        # 브랜드별 상세 키워드
        brand = product_info.get('brand', '')
        if brand == '씨씨더블유':
            basic_keywords.extend(['프리미엄', '최고급', '고급', '특급', '명품', 'VIP', '품격', '퀄리티'])
        elif brand == '인생':
            basic_keywords.extend(['가성비', '실용적', '저렴한', '합리적', '알뜰', '혜자', '착한가격', '인생템'])
        elif brand == '태공식품':
            basic_keywords.extend(['전통', '건강식', '국산', '웰빙', '자연', '무첨가', '유기농', '친환경'])
        
        # 용도별 키워드
        basic_keywords.extend([
            '간편요리', '간편식', '간단요리', '빠른조리', '즉석조리',
            '밥반찬', '집반찬', '기본반찬', '밑반찬', '메인반찬',
            '술안주', '맥주안주', '소주안주', '와인안주', '안주추천',
            '야식', '야참', '간식', '분식', '주전부리',
            '도시락', '도시락반찬', '직장인도시락', '학생도시락',
            '캠핑요리', '캠핑음식', '아웃도어', '등산음식',
            '혼밥', '혼술', '자취요리', '1인가구', '싱글라이프'
        ])
        
        # 조리방법 키워드
        basic_keywords.extend([
            '전자레인지', '전자렌지', '렌지조리', '마이크로웨이브',
            '에어프라이어', '에프', '에어프라이', '오븐',
            '끓이기만', '데우기만', '3분요리', '5분요리', '간단조리'
        ])
        
        # 포장/용량 키워드
        basic_keywords.extend([
            '1인분', '2인분', '3인분', '대용량', '소용량',
            '개별포장', '소포장', '낱개포장', '진공포장',
            '냉동', '냉장', '상온', '보관편리'
        ])
        
        # 트렌드 키워드
        basic_keywords.extend([
            '인기상품', '베스트', '추천', '신제품', '신상품',
            '품절대란', '화제상품', '맛집', '유명한', '대박상품'
        ])
        
        # 중복 제거
        seen = set()
        unique = []
        for k in basic_keywords:
            if k not in seen and len(unique) < 35:
                seen.add(k)
                unique.append(k)
        
        return unique
    
    def generate_description_with_ai(self, product_info: Dict) -> Dict:
        """AI로 상품 설명 생성"""
        if not self.openai_key:
            return None
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_key)
            
            prompt = f"""
            한국 이커머스 상품 설명 생성:
            
            상품명: {product_info['clean_name']}
            브랜드: {product_info['brand']}
            
            요구사항:
            - 요약설명: 정확히 40자
            - 간략설명: 정확히 50자
            - 브랜드명 제외
            - 자연스럽고 매력적인 표현
            
            JSON만 응답: {{"요약설명": "텍스트", "간략설명": "텍스트"}}
            """
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "한국 이커머스 상품 설명 전문가"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            content = response.choices[0].message.content.strip()
            if '{' in content and '}' in content:
                json_str = content[content.find('{'):content.rfind('}')+1]
                return json.loads(json_str)
            return None
        except Exception as e:
            print(f"  설명 생성 오류: {e}")
            return None
    
    def process_product(self, product_data: Dict) -> Dict:
        """상품 처리 - 지능형 시스템"""
        # 1. 원본 데이터 오타 수정
        corrected_data = self.correct_original_data(product_data)
        
        # 2. 상품 분석
        product_name = corrected_data.get('상품명', '')
        brand = ''
        clean_name = product_name
        
        # 브랜드 추출
        brand_patterns = ['[씨씨더블유]', '[인생]', '[태공식품]', '[최씨남매]', '[피자코리아]', '[모비딕]', '[취영루]', '[반찬단지]']
        for b in brand_patterns:
            if b in product_name:
                brand = b.replace('[', '').replace(']', '')
                clean_name = product_name.replace(b, '').strip()
                break
        
        product_info = {
            'brand': brand,
            'clean_name': clean_name
        }
        
        print(f"\n처리중: {clean_name} (브랜드: {brand})")
        
        # 3. 지능형 카테고리 결정
        categories = self.determine_categories(product_info)
        
        # 4. AI 설명 생성
        print(f"  AI 설명 생성...")
        ai_result = self.generate_description_with_ai(product_info)
        
        if ai_result:
            summary = ai_result.get('요약설명', '')[:40]
            brief = ai_result.get('간략설명', '')[:50]
            corrected_data['상품 요약설명'] = summary
            corrected_data['상품 간략설명'] = brief
            print(f"    요약({len(summary)}자): {summary}")
            print(f"    간략({len(brief)}자): {brief}")
        else:
            corrected_data['상품 요약설명'] = f"{clean_name[:35]}..."
            corrected_data['상품 간략설명'] = f"{clean_name[:45]}..."
        
        # 5. 조건부 키워드 생성
        print(f"  조건부 키워드 생성...")
        keywords = self.generate_conditional_keywords(product_info, corrected_data.get('상품 요약설명', ''))
        corrected_data['검색어설정'] = ','.join(keywords)
        
        # 6. 카테고리 설정
        corrected_data['상품분류 번호'] = '|'.join(map(str, categories))
        corrected_data['상품분류 신상품영역'] = '|'.join(['N'] * len(categories))
        corrected_data['상품분류 추천상품영역'] = '|'.join(['Y'] * len(categories))
        
        return corrected_data
    
    def process_csv(self, input_file: str, output_file: str = None):
        """CSV 파일 처리"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = input_file.replace('.csv', f'_INTELLIGENT_{timestamp}.csv')
        
        # CSV 읽기
        with open(input_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            fieldnames = reader.fieldnames
        
        print(f"\n총 {len(rows)}개 상품 지능형 처리 시작")
        
        # 처리
        processed = []
        
        for i, row in enumerate(rows, 1):
            print(f"\n[{i}/{len(rows)}]")
            result = self.process_product(row)
            processed.append(result)
        
        # 저장
        with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(processed)
        
        print(f"\n\n" + "="*60)
        print(f"지능형 처리 완료!")
        print(f"결과 파일: {output_file}")
        print("="*60)
        
        return output_file

def main():
    """메인 실행"""
    print("\n" + "="*60)
    print("지능형 상품 분류 시스템")
    print("조건부 키워드 + AI 카테고리 분석")
    print("="*60)
    
    system = IntelligentSystem()
    
    # 테스트 파일 처리
    test_file = "data/input/cafe24_test.csv"
    
    if os.path.exists(test_file):
        output = system.process_csv(test_file)
    else:
        print("테스트 파일이 없습니다.")

if __name__ == "__main__":
    main()
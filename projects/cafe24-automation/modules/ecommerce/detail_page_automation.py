#!/usr/bin/env python
"""
CUA 상세페이지 자동화 시스템
카페24/만원요리 상품 상세페이지 지능형 생성
"""

import re
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging
from collections import Counter
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('DetailPageAutomation')

class DetailPageAutomation:
    """상세페이지 자동화 메인 클래스"""
    
    def __init__(self):
        self.base_path = Path("C:/Users/8899y/CUA-MASTER")
        self.data_path = self.base_path / "data/ecommerce"
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        # 카테고리 매핑
        self.category_map = {
            53: {'name': '만원요리 PICK', 'keywords': ['메인', '전체', '인기', '공식']},
            61: {'name': '영상 속 그 요리', 'keywords': ['유튜브', '영상', '레시피']},
            60: {'name': '만원요리 추천', 'keywords': ['추천', '베스트', '인기']},
            59: {'name': '전체상품 보기', 'keywords': ['전체', 'All', '모든']},
            95: {'name': '고기/생선/달걀', 'keywords': ['육류', '고기', '소고기', '돼지고기', '생선', '달걀', '갈비', '대창']},
            96: {'name': '채소/과일', 'keywords': ['채소', '야채', '과일', '신선']},
            97: {'name': '쌀/면/잡곡', 'keywords': ['쌀', '면', '잡곡', '곡물', '오징어']},
            98: {'name': '양념/조미료', 'keywords': ['양념', '조미료', '소스', '간장']},
            99: {'name': '냉동/간편식', 'keywords': ['냉동', '간편', '밀키트', '즉석', '레토르트']},
            100: {'name': '반찬', 'keywords': ['반찬', '밑반찬', '김치']},
            103: {'name': '안주 추천', 'keywords': ['안주', '술안주', '맥주']},
            104: {'name': '캠핑 갈 때', 'keywords': ['캠핑', '바베큐', 'BBQ']},
            56: {'name': '직거래 브랜드', 'keywords': ['브랜드', '직거래', '정품']},
            110: {'name': '씨씨더블유', 'keywords': ['씨씨더블유', 'CCW']},
            109: {'name': '인생', 'keywords': ['인생']},
            108: {'name': '모비딕', 'keywords': ['모비딕']},
        }
        
        # 상황 키워드
        self.situation_keywords = [
            '집밥각', '술한잔', '반찬고민끝', '국물땡김', 
            '혼밥만세', '시간없어', '힘내자', '모임각'
        ]
        
        # 인기 검색어
        self.hot_keywords = [
            '토마토소스', '족발', '김치', '부대찌개', '떡',
            '밀키트', '냉면', '인절미', '해물', '간편식'
        ]
        
        # 브랜드 키워드
        self.brand_keywords = [
            '최씨남매', '만원요리', '전체상품', '공식몰',
            '추천', '정품', '직거래'
        ]
        
        # 중복 체크용 해시 세트
        self.used_hashes = set()
        
    def extract_brand(self, product_name: str) -> Optional[str]:
        """브랜드 추출"""
        pattern = r'\[(.*?)\]'
        match = re.search(pattern, product_name)
        if match:
            return match.group(1)
        return None
        
    def extract_product_features(self, product_name: str) -> Dict:
        """상품 특징 추출"""
        features = {
            'brand': self.extract_brand(product_name),
            'weight': None,
            'type': None,
            'main_ingredient': None
        }
        
        # 중량 추출 (예: 200g, 1kg)
        weight_pattern = r'(\d+(?:\.\d+)?)\s*(g|kg|ml|L)'
        weight_match = re.search(weight_pattern, product_name, re.IGNORECASE)
        if weight_match:
            features['weight'] = weight_match.group(0)
            
        # 주요 재료 추출
        ingredients = ['갈비', '대창', '오징어', '소고기', '돼지고기', '닭고기']
        for ingredient in ingredients:
            if ingredient in product_name:
                features['main_ingredient'] = ingredient
                break
                
        # 조리 타입
        types = ['양념', '소금구이', '불갈비', '구이', '찜', '볶음']
        for cook_type in types:
            if cook_type in product_name:
                features['type'] = cook_type
                break
                
        return features
        
    def auto_categorize(self, product_name: str, features: Dict) -> List[int]:
        """자동 카테고리 분류"""
        categories = []
        
        # 메인 카테고리 (만원요리 PICK) 기본 추가
        categories.append(53)
        
        # 브랜드별 카테고리
        brand = features.get('brand')
        if brand:
            if '씨씨더블유' in brand or 'CCW' in brand:
                categories.extend([56, 110])  # 직거래 브랜드 + 씨씨더블유
            elif '인생' in brand:
                categories.extend([56, 109])  # 직거래 브랜드 + 인생
            elif '모비딕' in brand:
                categories.extend([56, 108])  # 직거래 브랜드 + 모비딕
                
        # 재료별 카테고리
        ingredient = features.get('main_ingredient')
        if ingredient:
            if ingredient in ['갈비', '대창', '소고기', '돼지고기']:
                categories.append(95)  # 고기/생선/달걀
            elif ingredient in ['오징어']:
                categories.append(97)  # 오징어는 면/잡곡 카테고리에
                
        # 용도별 카테고리
        if '안주' in product_name or '술' in product_name:
            categories.append(103)  # 안주 추천
            
        # 간편식 카테고리
        if any(keyword in product_name for keyword in ['간편', '즉석', '밀키트']):
            categories.append(99)  # 냉동/간편식
            
        # 중복 제거
        categories = list(dict.fromkeys(categories))
        
        return categories
        
    def generate_keywords(self, product_name: str, features: Dict, categories: List[int]) -> str:
        """검색어 생성 (200byte 제한)"""
        keywords = []
        
        # 1. 상품명 기반 키워드
        # 브랜드 제거한 순수 상품명
        clean_name = re.sub(r'\[.*?\]', '', product_name).strip()
        
        # 상품명 단어 분리
        words = clean_name.split()
        for word in words:
            if len(word) > 1:  # 1글자 제외
                keywords.append(word)
                
        # 띄어쓰기 제거 버전
        no_space = clean_name.replace(' ', '')
        if no_space not in keywords:
            keywords.append(no_space)
            
        # 2. 브랜드 키워드
        if features['brand']:
            keywords.append(features['brand'])
            # 영문 변환
            if 'CCW' in features['brand']:
                keywords.append('씨씨더블유')
            elif '씨씨더블유' in features['brand']:
                keywords.append('CCW')
                
        # 3. 특징 키워드
        if features['weight']:
            keywords.append(features['weight'])
        if features['type']:
            keywords.append(features['type'])
        if features['main_ingredient']:
            keywords.append(features['main_ingredient'])
            
        # 4. 상황 키워드 (랜덤 3-4개)
        import random
        selected_situations = random.sample(self.situation_keywords, min(3, len(self.situation_keywords)))
        keywords.extend(selected_situations)
        
        # 5. 브랜드 관련 키워드
        keywords.extend(['만원요리', '최씨남매', '정품', '직거래'])
        
        # 6. 카테고리 기반 키워드
        for cat_id in categories:
            if cat_id in self.category_map:
                cat_keywords = self.category_map[cat_id]['keywords']
                keywords.extend(cat_keywords[:2])  # 각 카테고리에서 2개씩
                
        # 중복 제거 및 순서 유지
        seen = set()
        unique_keywords = []
        for k in keywords:
            if k not in seen:
                seen.add(k)
                unique_keywords.append(k)
                
        # 200byte 제한 체크
        result = ','.join(unique_keywords)
        while len(result.encode('utf-8')) > 200:
            unique_keywords.pop()
            result = ','.join(unique_keywords)
            
        return result
        
    def generate_unique_summary(self, product_name: str, features: Dict) -> str:
        """고유한 요약설명 생성 (30자 제한)"""
        templates = [
            "{ingredient}의 깊은 맛을 느껴보세요",
            "특제 {type}의 완벽한 조화",
            "{brand} 시그니처 레시피",
            "프리미엄 {ingredient} {weight}",
            "{type}으로 완성한 특별한 맛",
            "정성 가득 {brand} {ingredient}",
            "{weight} 실속 만점 구성"
        ]
        
        # 사용 가능한 템플릿 선택
        valid_templates = []
        for template in templates:
            required = re.findall(r'\{(\w+)\}', template)
            if all(features.get(r) for r in required):
                valid_templates.append(template)
                
        if valid_templates:
            import random
            template = random.choice(valid_templates)
            summary = template.format(**features)
        else:
            # 기본 템플릿
            summary = "프리미엄 품질의 특별한 맛"
            
        # 30자 제한
        if len(summary) > 30:
            summary = summary[:27] + "..."
            
        return summary
        
    def generate_unique_brief(self, product_name: str, features: Dict, situations: List[str]) -> str:
        """고유한 간략설명 생성 (30자 제한)"""
        templates = [
            "{situation}에 딱! {type} 강추",
            "간편하게 즐기는 {ingredient}",
            "{situation} {brand} 추천",
            "집에서 즐기는 {type} {ingredient}",
            "{weight} 가성비 최고!",
            "{situation}용 베스트 선택"
        ]
        
        # 상황 선택
        if situations:
            import random
            situation = random.choice(situations)
        else:
            situation = "집밥"
            
        features['situation'] = situation
        
        # 템플릿 선택
        valid_templates = []
        for template in templates:
            required = re.findall(r'\{(\w+)\}', template)
            if all(features.get(r) for r in required):
                valid_templates.append(template)
                
        if valid_templates:
            import random
            template = random.choice(valid_templates)
            brief = template.format(**features)
        else:
            brief = f"{situation}에 추천!"
            
        # 30자 제한
        if len(brief) > 30:
            brief = brief[:27] + "..."
            
        return brief
        
    def generate_seo_fields(self, product_name: str, features: Dict, keywords: str) -> Dict:
        """SEO 필드 생성"""
        
        seo = {
            'title': f"{product_name} | 만원요리 최씨남매 공식",
            'author': features.get('brand', '만원요리'),
            'description': f"만원요리 최씨남매 {product_name}. {features.get('type', '')} {features.get('main_ingredient', '')} 프리미엄 상품. 정품 보장, 빠른 배송.",
            'keywords': keywords,
            'alt': f"{product_name} 상품 이미지"
        }
        
        # 길이 제한
        if len(seo['description']) > 90:
            seo['description'] = seo['description'][:87] + "..."
        if len(seo['alt']) > 60:
            seo['alt'] = seo['alt'][:57] + "..."
            
        return seo
        
    def check_uniqueness(self, text: str) -> bool:
        """중복 체크"""
        text_hash = hashlib.md5(text.encode()).hexdigest()
        if text_hash in self.used_hashes:
            return False
        self.used_hashes.add(text_hash)
        return True
        
    def process_product(self, product_data: Dict) -> Dict:
        """상품 데이터 처리"""
        
        product_name = product_data.get('상품명', '')
        
        # 특징 추출
        features = self.extract_product_features(product_name)
        
        # 카테고리 자동 분류
        categories = self.auto_categorize(product_name, features)
        category_str = '|'.join(map(str, categories))
        
        # 신상품/추천 영역 N 설정
        new_product_area = '|'.join(['N'] * len(categories))
        recommend_area = '|'.join(['N'] * len(categories))
        
        # 키워드 생성
        keywords = self.generate_keywords(product_name, features, categories)
        
        # 요약/간략 설명 생성
        summary = self.generate_unique_summary(product_name, features)
        brief = self.generate_unique_brief(product_name, features, self.situation_keywords[:3])
        
        # 중복 체크 및 재생성
        attempts = 0
        while not self.check_uniqueness(summary + brief) and attempts < 5:
            summary = self.generate_unique_summary(product_name, features)
            brief = self.generate_unique_brief(product_name, features, self.situation_keywords[:3])
            attempts += 1
            
        # SEO 필드 생성
        seo = self.generate_seo_fields(product_name, features, keywords)
        
        # 결과 반환
        result = {
            '상품명': product_name,
            '상품분류 번호': category_str,
            '상품분류 신상품영역': new_product_area,
            '상품분류 추천상품영역': recommend_area,
            '검색어설정': keywords,
            '상품 요약설명': summary,
            '상품 간략설명': brief,
            'SEO Title': seo['title'],
            'SEO Author': seo['author'],
            'SEO Description': seo['description'],
            'SEO Keywords': seo['keywords'],
            'SEO Alt': seo['alt']
        }
        
        return result
        
    def process_csv(self, input_file: Path, output_file: Path = None) -> pd.DataFrame:
        """CSV 파일 처리"""
        
        logger.info(f"Processing CSV: {input_file}")
        
        # CSV 읽기
        df = pd.read_csv(input_file, encoding='utf-8-sig')
        
        # 각 상품 처리
        results = []
        for idx, row in df.iterrows():
            try:
                processed = self.process_product(row.to_dict())
                
                # 기존 데이터 업데이트
                for key, value in processed.items():
                    if key in df.columns:
                        df.at[idx, key] = value
                        
                results.append(processed)
                logger.info(f"Processed: {processed['상품명']}")
                
            except Exception as e:
                logger.error(f"Error processing row {idx}: {e}")
                
        # 결과 저장
        if output_file:
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            logger.info(f"Saved to: {output_file}")
            
        # 보고서 생성
        self.generate_report(results)
        
        return df
        
    def generate_report(self, results: List[Dict]):
        """처리 보고서 생성"""
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_products': len(results),
            'categories_used': Counter(),
            'keywords_stats': {
                'avg_length': 0,
                'max_length': 0,
                'min_length': 999
            },
            'uniqueness': {
                'summaries': len(set(r['상품 요약설명'] for r in results)),
                'briefs': len(set(r['상품 간략설명'] for r in results))
            }
        }
        
        # 통계 계산
        for result in results:
            # 카테고리 통계
            categories = result['상품분류 번호'].split('|')
            for cat in categories:
                report['categories_used'][cat] = report['categories_used'].get(cat, 0) + 1
                
            # 키워드 길이 통계
            keyword_length = len(result['검색어설정'].encode('utf-8'))
            report['keywords_stats']['avg_length'] += keyword_length
            report['keywords_stats']['max_length'] = max(report['keywords_stats']['max_length'], keyword_length)
            report['keywords_stats']['min_length'] = min(report['keywords_stats']['min_length'], keyword_length)
            
        report['keywords_stats']['avg_length'] //= len(results)
        
        # 보고서 저장
        report_file = self.data_path / f"detail_page_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
            
        logger.info(f"Report saved: {report_file}")
        
        # 콘솔 출력
        print("\n" + "="*50)
        print("상세페이지 자동화 처리 완료")
        print("="*50)
        print(f"처리 상품: {report['total_products']}개")
        print(f"고유 요약설명: {report['uniqueness']['summaries']}개")
        print(f"고유 간략설명: {report['uniqueness']['briefs']}개")
        print(f"평균 키워드 길이: {report['keywords_stats']['avg_length']}bytes")
        print("="*50)

if __name__ == "__main__":
    import sys
    
    automation = DetailPageAutomation()
    
    if len(sys.argv) > 1:
        input_file = Path(sys.argv[1])
        
        if len(sys.argv) > 2:
            output_file = Path(sys.argv[2])
        else:
            output_file = input_file.parent / f"{input_file.stem}_processed.csv"
            
        automation.process_csv(input_file, output_file)
    else:
        # 테스트 데이터
        test_product = {
            '상품명': '[씨씨더블유]명품 양념LA꽃갈비 500g'
        }
        
        result = automation.process_product(test_product)
        print(json.dumps(result, ensure_ascii=False, indent=2))
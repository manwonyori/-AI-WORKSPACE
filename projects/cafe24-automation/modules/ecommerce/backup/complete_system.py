#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from anthropic import Anthropic
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, List
import csv
import json
import logging
import os

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
완전한 AI 시스템
공급사별 카테고리 규칙 포함
"""

# 환경변수 로드
load_dotenv()

class CompleteAISystem:
    """공급사별 규칙을 포함한 완전한 AI 시스템"""
    
    def __init__(self):
        # API 키 설정
        self.setup_apis()
        
        # 필수 키워드 (정확히 이 10개가 모든 상품에 포함되어야 함)
        self.required_keywords = [
            "만원요리", "최씨남매", "집밥각", "술한잔",
            "반찬고민끝", "국물땡김", "혼밥만세", "시간없어",
            "힘내자", "모임각"
        ]
        
        # 공급사별 카테고리 규칙 (우선 적용)
        self.supplier_rules = {
            # 씨씨더블유 - 프리미엄 육류/안주류
            '씨씨더블유': {
                '닭발': [53, 95, 99, 103, 56, 110],
                '무뼈닭발': [53, 95, 99, 103, 56, 110],
                '직화닭발': [53, 95, 99, 103, 56, 110],
                '막창': [53, 95, 98, 99, 103, 56, 110],
                '돼지막창': [53, 95, 98, 99, 103, 56, 110],
                '소막창': [53, 95, 98, 99, 103, 56, 110],
                '불막창': [53, 95, 98, 99, 103, 56, 110],
                '갈비': [53, 95, 99, 103, 56],
                '삼겹살': [53, 95, 99, 103, 56],
                'default': [53, 95, 99, 103, 56]  # 씨씨더블유 기본값
            },
            
            # 인생 - 간편식/가성비
            '인생': {
                '찌개': [56, 97, 102, 109],
                '탕': [56, 97, 102, 109],  
                '오뎅': [56, 97, 102, 109],
                '어묵': [56, 97, 102, 109],
                '피자': [56, 98, 102],
                '라면': [56, 97, 102],
                'default': [56, 97, 102]  # 인생 기본값
            },
            
            # 태공식품 - 수산물/전통식품
            '태공식품': {
                '갈치': [97, 99, 103, 56],
                '고등어': [97, 99, 103, 56],
                '꽃맛살': [97, 99, 103, 56],
                '어묵바': [97, 99, 103, 56],
                '수산물': [97, 99, 103, 56],
                'default': [97, 99, 103, 56]  # 태공식품 기본값
            },
            
            # 최씨남매 - 종합식품
            '최씨남매': {
                '김치찜': [56, 97, 102, 109],
                '국밥': [56, 97, 102, 109],
                '갈비탕': [56, 97, 102, 109],
                '떡갈비': [53, 95, 99, 103, 56],
                '삼겹살': [53, 95, 99, 103, 56],
                'default': [56, 97, 102]  # 최씨남매 기본값
            },
            
            # 피자코리아 - 피자전문
            '피자코리아': {
                'default': [56, 98, 102]  # 피자코리아 모든 제품
            },
            
            # 모비딕 - 육류가공
            '모비딕': {
                'default': [53, 95, 99, 103, 56]  # 모비딕 육류
            },
            
            # 취영루 - 만두전문
            '취영루': {
                'default': [56, 97, 102]  # 취영루 만두류
            },
            
            # 반찬단지 - 반찬전문
            '반찬단지': {
                'default': [56, 102, 109]  # 반찬단지 반찬류
            }
        }
        
        # 제품명 키워드 규칙 (공급사 규칙 보완)
        self.product_rules = {
            # 육류/안주
            '닭발': [53, 95, 99, 103, 56, 110],
            '무뼈닭발': [53, 95, 99, 103, 56, 110],
            '직화닭발': [53, 95, 99, 103, 56, 110],
            '막창': [53, 95, 98, 99, 103, 56, 110],
            '돼지막창': [53, 95, 98, 99, 103, 56, 110],
            '소막창': [53, 95, 98, 99, 103, 56, 110],
            '불막창': [53, 95, 98, 99, 103, 56, 110],
            
            # 국물요리
            '찌개': [56, 97, 102, 109],
            '국밥': [56, 97, 102, 109],
            '탕': [56, 97, 102, 109],
            '김치찜': [56, 97, 102, 109],
            '갈비탕': [56, 97, 102, 109],
            '오뎅': [56, 97, 102, 109],
            '어묵': [56, 97, 102, 109],
            
            # 수산물
            '갈치': [97, 99, 103],
            '고등어': [97, 99, 103],
            '꽃맛살': [97, 99, 103],
            '어묵바': [97, 99, 103],
            
            # 만두/간편식
            '만두': [56, 97],
            '왕만두': [56, 97],
            
            # 피자
            '피자': [56, 98],
            '포카치아': [56, 98],
            
            # 반찬
            '깻잎': [56, 102],
            '알마늘': [56, 102],
            '간장': [56, 102]
        }
        
        # 오타 수정
        self.corrections = {
            '꾸븐': '구운',
            '오뎅': '어묵'
        }
    
    def setup_apis(self):
        """API 설정"""
        # OpenAI
        self.openai_key = os.getenv('OPENAI_API_KEY')
        if self.openai_key:
            print("OpenAI 키 설정됨")
        
        # Anthropic Claude
        self.claude_key = os.getenv('ANTHROPIC_API_KEY')
        if self.claude_key:
            try:
                self.claude = Anthropic(api_key=self.claude_key)
                print("Claude 클라이언트 생성 성공")
            except Exception as e:
                print(f"Claude 설정 오류: {e}")
                self.claude = None
        else:
            self.claude = None
    
    def analyze_product(self, product_name: str) -> Dict:
        """상품 분석 - 공급사별 규칙 우선 적용"""
        # 브랜드 추출
        brand = ''
        clean_name = product_name
        
        brand_patterns = ['[씨씨더블유]', '[인생]', '[태공식품]', '[최씨남매]', '[피자코리아]', '[모비딕]', '[취영루]', '[반찬단지]']
        for b in brand_patterns:
            if b in product_name:
                brand = b.replace('[', '').replace(']', '')
                clean_name = product_name.replace(b, '').strip()
                break
        
        # 오타 수정
        for wrong, correct in self.corrections.items():
            clean_name = clean_name.replace(wrong, correct)
        
        # 카테고리 결정 - 공급사별 규칙 우선
        categories = []
        matched_rule = ''
        
        # 1단계: 공급사별 규칙 확인
        if brand and brand in self.supplier_rules:
            supplier_rules = self.supplier_rules[brand]
            
            # 공급사 내 제품별 규칙 확인
            for keyword in supplier_rules:
                if keyword != 'default' and keyword in clean_name:
                    categories = supplier_rules[keyword]
                    matched_rule = f"공급사({brand})-{keyword}"
                    break
            
            # 공급사 기본값 적용
            if not categories and 'default' in supplier_rules:
                categories = supplier_rules['default']
                matched_rule = f"공급사({brand})-기본값"
        
        # 2단계: 제품명 키워드 규칙 (공급사 규칙 없을 때)
        if not categories:
            priority_order = [
                '무뼈닭발', '직화닭발', '닭발',
                '돼지막창', '소막창', '불막창', '막창', 
                '갈비탕', '김치찜', '국밥', '찌개', '탕',
                '왕만두', '만두',
                '포카치아', '피자',
                '갈치', '고등어', '꽃맛살', '어묵바',
                '오뎅', '어묵',
                '깻잎', '알마늘', '간장'
            ]
            
            for keyword in priority_order:
                if keyword in clean_name and keyword in self.product_rules:
                    categories = self.product_rules[keyword]
                    matched_rule = f"제품키워드-{keyword}"
                    break
        
        # 3단계: 기본값
        if not categories:
            categories = [56]
            matched_rule = "기본값"
        
        print(f"    카테고리 규칙: {matched_rule} → {categories}")
        
        return {
            'brand': brand,
            'clean_name': clean_name,
            'categories': categories,
            'matched_rule': matched_rule
        }
    
    def generate_with_openai(self, product_info: Dict) -> Dict:
        """OpenAI API로 생성"""
        if not self.openai_key:
            return None
        
        try:
            client = OpenAI(api_key=self.openai_key)
            
            prompt = f"""
            한국 이커머스 상품 설명 생성:
            
            상품명: {product_info['clean_name']}
            브랜드: {product_info['brand']}
            
            요구사항:
            - 요약설명: 정확히 40자
            - 간략설명: 정확히 50자
            - 브랜드명 제외
            - 매력적이고 구매욕구 자극
            
            브랜드 톤:
            - 씨씨더블유: 프리미엄, 고급
            - 인생: 가성비, 혼밥족
            - 태공식품: 전통, 건강
            - 최씨남매: 인기, 검증된맛
            
            JSON만 응답: {{"요약설명": "텍스트", "간략설명": "텍스트"}}
            """
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "한국 이커머스 상품 설명 전문가. JSON만 응답."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            content = response.choices[0].message.content.strip()
            if '{' in content and '}' in content:
                json_str = content[content.find('{'):content.rfind('}')+1]
                result = json.loads(json_str)
                print(f"  OpenAI 생성 성공: {result}")
                return result
            return None
        except Exception as e:
            print(f"  OpenAI API 오류: {e}")
            return None
    
    def generate_keywords(self, product_info: Dict, description: str) -> List[str]:
        """키워드 생성"""
        # 1. 필수 키워드
        keywords = self.required_keywords.copy()
        
        # 2. 공급사별 키워드
        brand = product_info.get('brand', '')
        if brand == '씨씨더블유':
            keywords.extend(['프리미엄', '최고급', '특별한날', '고품질', '직화', '숯불'])
        elif brand == '인생':
            keywords.extend(['가성비', '혼밥', '간편식', '실용적', '경제적'])
        elif brand == '태공식품':
            keywords.extend(['전통', '건강식', '웰빙', '자연', '수산물'])
        elif brand == '최씨남매':
            keywords.extend(['인기상품', '베스트셀러', '검증된맛', '믿을만한'])
        elif brand == '피자코리아':
            keywords.extend(['피자', '치즈', '이탈리아', '파티'])
        elif brand == '모비딕':
            keywords.extend(['육류', '고기', '단백질', '영양'])
        elif brand == '취영루':
            keywords.extend(['만두', '중식', '간식', '든든한'])
        elif brand == '반찬단지':
            keywords.extend(['반찬', '밑반찬', '전통', '집밥'])
        
        # 3. 제품 특성 키워드
        clean_name = product_info['clean_name'].lower()
        if '매운' in clean_name or '매콤' in clean_name:
            keywords.extend(['매운맛', '매콤한', '칼칼한', '불맛'])
        if '직화' in clean_name or '구운' in clean_name:
            keywords.extend(['직화구이', '바삭한', '노릇노릇', '숯불향'])
        if '무뼈' in clean_name or '순살' in clean_name:
            keywords.extend(['무뼈', '순살', '먹기편한'])
        if any(x in clean_name for x in ['찌개', '탕', '국밥']):
            keywords.extend(['국물요리', '뜨끈한', '든든한', '해장'])
        if any(x in clean_name for x in ['갈치', '고등어', '오징어', '새우']):
            keywords.extend(['수산물', '해산물', '오메가3', 'DHA'])
        
        # 4. 일반 키워드
        keywords.extend([
            '간편요리', '전자레인지', '에어프라이어', '안주', '밑반찬',
            '술안주', '맥주안주', '야식', '간식', '든든한',
            '건강한', '맛있는', '정품', '신선한', '품질보장'
        ])
        
        # 5. 상품명 단어
        name_parts = product_info['clean_name'].replace(',', '').replace('(', ' ').replace(')', ' ').split()
        keywords.extend([p for p in name_parts if len(p) > 1 and not p.isdigit()])
        
        # 6. 중복 제거, 40개 제한
        seen = set()
        unique = []
        for k in keywords:
            clean_k = k.strip()
            if clean_k and clean_k not in seen and len(unique) < 40:
                seen.add(clean_k)
                unique.append(clean_k)
        
        return unique
    
    def process_product(self, product_data: Dict) -> Dict:
        """상품 처리"""
        product_name = product_data.get('상품명', '')
        
        # 1. 상품 분석 (공급사별 규칙 적용)
        analysis = self.analyze_product(product_name)
        print(f"\n처리중: {analysis['clean_name']} (브랜드: {analysis['brand']})")
        
        # 2. AI 생성
        result = self.generate_with_openai(analysis)
        
        # 3. 결과 처리
        if result:
            summary = result.get('요약설명', '')
            brief = result.get('간략설명', '')
            
            # 길이 조정
            if len(summary) > 40:
                summary = summary[:40]
            if len(brief) > 50:
                brief = brief[:50]
            
            product_data['상품 요약설명'] = summary
            product_data['상품 간략설명'] = brief
            
            print(f"  AI 생성 완료")
            print(f"    요약({len(summary)}자): {summary}")
            print(f"    간략({len(brief)}자): {brief}")
        else:
            print("  AI API 실패, 기본값 사용")
            product_data['상품 요약설명'] = f"{analysis['clean_name'][:35]}..."
            product_data['상품 간략설명'] = f"{analysis['clean_name'][:45]}..."
        
        # 4. 키워드 생성
        keywords = self.generate_keywords(analysis, product_data.get('상품 요약설명', ''))
        product_data['검색어설정'] = ','.join(keywords)
        
        # 5. 카테고리 설정 (공급사별 규칙 적용됨)
        categories = analysis['categories']
        product_data['상품분류 번호'] = '|'.join(map(str, categories))
        product_data['상품분류 신상품영역'] = '|'.join(['N'] * len(categories))
        product_data['상품분류 추천상품영역'] = '|'.join(['Y'] * len(categories))
        
        return product_data
    
    def process_csv(self, input_file: str, output_file: str = None):
        """CSV 파일 처리"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = input_file.replace('.csv', f'_COMPLETE_{timestamp}.csv')
        
        # CSV 읽기
        with open(input_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            fieldnames = reader.fieldnames
        
        print(f"\n총 {len(rows)}개 상품 처리 시작")
        
        # 처리
        processed = []
        supplier_stats = {}
        category_stats = {}
        
        for i, row in enumerate(rows, 1):
            print(f"\n[{i}/{len(rows)}]")
            result = self.process_product(row)
            processed.append(result)
            
            # 통계 수집
            product_name = result.get('상품명', '')
            supplier = ''
            for brand in ['씨씨더블유', '인생', '태공식품', '최씨남매', '피자코리아', '모비딕', '취영루', '반찬단지']:
                if brand in product_name:
                    supplier = brand
                    break
            
            if supplier:
                supplier_stats[supplier] = supplier_stats.get(supplier, 0) + 1
            
            categories = result.get('상품분류 번호', '56')
            category_stats[categories] = category_stats.get(categories, 0) + 1
        
        # 저장
        with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(processed)
        
        print(f"\n\n" + "="*60)
        print(f"처리 완료!")
        print(f"총 상품: {len(rows)}개")
        print(f"\n공급사별 분포:")
        for supplier, count in sorted(supplier_stats.items()):
            print(f"  {supplier}: {count}개")
        print(f"\n카테고리 분포:")
        for cat, count in sorted(category_stats.items()):
            print(f"  {cat}: {count}개")
        print(f"\n결과 파일: {output_file}")
        print("="*60)
        
        return output_file

def main():
    """메인 실행"""
    print("\n" + "="*60)
    print("완전한 AI 시스템")
    print("공급사별 카테고리 규칙 적용")
    print("="*60)
    
    system = CompleteAISystem()
    
    # 테스트 파일 처리
    test_file = "data/input/cafe24_test.csv"
    
    if os.path.exists(test_file):
        print(f"\n파일 처리: {test_file}")
        output = system.process_csv(test_file)
    else:
        print("테스트 파일이 없습니다.")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from anthropic import Anthropic
import google.generativeai as genai
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
최종 수정된 AI 시스템
카테고리 매칭 및 검색어 생성 개선
"""

# 환경변수 로드
load_dotenv()

class FinalFixedAISystem:
    """최종 수정된 실제 AI API 시스템"""
    
    def __init__(self):
        # API 키 설정
        self.setup_apis()
        
        # 필수 키워드 (정확히 이 10개가 모든 상품에 포함되어야 함)
        self.required_keywords = [
            "만원요리", "최씨남매", "집밥각", "술한잔",
            "반찬고민끝", "국물땡김", "혼밥만세", "시간없어",
            "힘내자", "모임각"
        ]
        
        # 카테고리 규칙 (개선된 매칭)
        self.category_rules = {
            # 닭발 관련
            '닭발': [53, 95, 99, 103, 56, 110],
            '무뼈닭발': [53, 95, 99, 103, 56, 110],
            '직화닭발': [53, 95, 99, 103, 56, 110],
            
            # 막창 관련  
            '막창': [53, 95, 98, 99, 103, 56, 110],
            '돼지막창': [53, 95, 98, 99, 103, 56, 110],
            '소막창': [53, 95, 98, 99, 103, 56, 110],
            '불막창': [53, 95, 98, 99, 103, 56, 110],
            
            # 찌개/국물 관련
            '찌개': [56, 97, 102, 109],
            '국밥': [56, 97, 102, 109],
            '탕': [56, 97, 102, 109],
            '김치찜': [56, 97, 102, 109],
            '갈비탕': [56, 97, 102, 109],
            '오뎅': [56, 97, 102, 109],
            '어묵': [56, 97, 102, 109],
            
            # 수산물 관련
            '갈치': [97, 99, 103],
            '고등어': [97, 99, 103], 
            '오징어': [97, 99, 103],
            '새우': [97, 99, 103],
            '꽃맛살': [97, 99, 103],
            '어묵바': [97, 99, 103],
            
            # 만두 관련
            '만두': [56, 97],
            '왕만두': [56, 97],
            
            # 피자 관련
            '피자': [56, 98],
            '포카치아': [56, 98],
            
            # 반찬 관련
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
        """API 설정 - 수정된 버전"""
        # OpenAI 최신 버전
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
        
        # Google Gemini
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        if self.gemini_key:
            try:
                genai.configure(api_key=self.gemini_key)
                # 최신 모델 사용
                self.gemini = genai.GenerativeModel('gemini-1.5-flash')
                print("Gemini 클라이언트 생성 성공")
            except Exception as e:
                print(f"Gemini 설정 오류: {e}")
                self.gemini = None
        else:
            self.gemini = None
    
    def analyze_product(self, product_name: str) -> Dict:
        """상품 분석 - 개선된 카테고리 매칭"""
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
        
        # 카테고리 결정 (개선된 매칭)
        categories = []
        matched_keyword = ''
        
        # 우선순위 매칭 (더 구체적인 키워드 먼저)
        priority_order = [
            '무뼈닭발', '직화닭발', '닭발',
            '돼지막창', '소막창', '불막창', '막창', 
            '갈비탕', '김치찜', '국밥', '찌개', '탕',
            '왕만두', '만두',
            '포카치아', '피자',
            '갈치', '고등어', '오징어', '새우', '꽃맛살', '어묵바',
            '오뎅', '어묵',
            '깻잎', '알마늘', '간장'
        ]
        
        for keyword in priority_order:
            if keyword in clean_name:
                categories = self.category_rules[keyword]
                matched_keyword = keyword
                print(f"    카테고리 매칭: '{keyword}' → {categories}")
                break
        
        if not categories:
            categories = [56]  # 기본값
            print(f"    기본 카테고리 적용: {categories}")
        
        return {
            'brand': brand,
            'clean_name': clean_name,
            'categories': categories,
            'matched_keyword': matched_keyword
        }
    
    def generate_with_claude(self, product_info: Dict) -> Dict:
        """Claude API로 생성 - 수정된 버전"""
        if not self.claude:
            return None
        
        prompt = f"""
        한국 이커머스 상품 설명 생성:
        
        상품명: {product_info['clean_name']}
        브랜드: {product_info['brand']}
        
        다음 형식으로 창의적이고 매력적인 설명을 생성해주세요:
        1. 요약설명: 정확히 40자로 핵심 특징과 매력을 전달
        2. 간략설명: 정확히 50자로 구매욕구를 자극하는 설명
        
        브랜드별 톤:
        - 씨씨더블유: 프리미엄, 고급스러운
        - 인생: 가성비, 실용적, 혼밥족 타겟
        - 태공식품: 전통적, 건강한
        
        브랜드명은 설명에서 제외하고, 제품 특징을 생동감 있게 표현하세요.
        
        JSON 형식으로만 응답:
        {{"요약설명": "40자 설명", "간략설명": "50자 설명"}}
        """
        
        try:
            response = self.claude.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text.strip()
            # JSON 추출 및 파싱
            if '{' in content and '}' in content:
                json_str = content[content.find('{'):content.rfind('}')+1]
                result = json.loads(json_str)
                print(f"  Claude 생성 성공: {result}")
                return result
            return None
        except Exception as e:
            print(f"  Claude API 오류: {e}")
            return None
    
    def generate_with_openai(self, product_info: Dict) -> Dict:
        """OpenAI API로 생성 - 수정된 버전"""
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
            - 씨씨더블유: 프리미엄
            - 인생: 가성비, 혼밥족
            - 태공식품: 전통, 건강
            
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
        """키워드 생성 - 개선된 버전"""
        # 1. 필수 키워드 (반드시 포함)
        keywords = self.required_keywords.copy()
        
        # 2. 상품명에서 의미 있는 키워드 추출
        clean_name = product_info['clean_name'].lower()
        
        # 제품 특성 키워드
        if '매운' in clean_name or '매콤' in clean_name:
            keywords.extend(['매운맛', '매콤한', '칼칼한', '불맛'])
        if '직화' in clean_name or '구운' in clean_name:
            keywords.extend(['직화구이', '바삭한', '노릇노릇', '숯불향'])
        if '무뼈' in clean_name or '순살' in clean_name:
            keywords.extend(['무뼈', '순살', '먹기편한'])
        if '찌개' in clean_name or '탕' in clean_name or '국밥' in clean_name:
            keywords.extend(['국물요리', '뜨끈한', '든든한', '해장'])
        if any(x in clean_name for x in ['갈치', '고등어', '오징어', '새우']):
            keywords.extend(['수산물', '해산물', '오메가3', 'DHA', '바다'])
        if '만두' in clean_name:
            keywords.extend(['만두', '간식', '든든한', '간편식'])
        if '피자' in clean_name:
            keywords.extend(['피자', '치즈', '간편식', '파티'])
        if any(x in clean_name for x in ['깻잎', '알마늘', '간장']):
            keywords.extend(['반찬', '밑반찬', '전통', '집밥'])
        
        # 3. 브랜드별 키워드
        brand = product_info.get('brand', '')
        if brand == '씨씨더블유':
            keywords.extend(['프리미엄', '최고급', '특별한날', '고품질'])
        elif brand == '인생':
            keywords.extend(['가성비', '혼밥', '간편식', '실용적'])
        elif brand == '태공식품':
            keywords.extend(['전통', '건강식', '웰빙', '자연'])
        elif brand == '최씨남매':
            keywords.extend(['인기상품', '베스트셀러', '검증된맛'])
        
        # 4. 용도별 키워드
        keywords.extend([
            '간편요리', '전자레인지', '에어프라이어', '안주', '밑반찬',
            '술안주', '맥주안주', '야식', '간식', '든든한',
            '건강한', '맛있는', '정품', '신선한', '품질보장'
        ])
        
        # 5. 상품명 단어 추가
        name_parts = product_info['clean_name'].replace(',', '').replace('(', ' ').replace(')', ' ').split()
        keywords.extend([p for p in name_parts if len(p) > 1 and not p.isdigit()])
        
        # 6. 중복 제거하고 40개로 제한
        seen = set()
        unique = []
        for k in keywords:
            clean_k = k.strip()
            if clean_k and clean_k not in seen and len(unique) < 40:
                seen.add(clean_k)
                unique.append(clean_k)
        
        print(f"    키워드({len(unique)}개): {', '.join(unique[:10])}...")
        return unique
    
    def process_product(self, product_data: Dict) -> Dict:
        """상품 처리 - AI 생성"""
        product_name = product_data.get('상품명', '')
        
        # 1. 상품 분석 (개선된 카테고리 매칭)
        analysis = self.analyze_product(product_name)
        print(f"\n처리중: {analysis['clean_name']}")
        
        # 2. AI 생성 (우선순위: Claude > OpenAI > Gemini)
        result = None
        
        # Claude 시도
        if self.claude and not result:
            print("  Claude API 호출...")
            result = self.generate_with_claude(analysis)
        
        # OpenAI 시도
        if not result and self.openai_key:
            print("  OpenAI API 호출...")
            result = self.generate_with_openai(analysis)
        
        # 3. 결과 처리
        if result:
            # AI 생성 결과 사용
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
            # API 실패시 기본값
            print("  모든 AI API 실패, 기본값 사용")
            product_data['상품 요약설명'] = f"{analysis['clean_name'][:35]}..."
            product_data['상품 간략설명'] = f"{analysis['clean_name'][:45]}..."
        
        # 4. 개선된 키워드 생성
        keywords = self.generate_keywords(analysis, product_data.get('상품 요약설명', ''))
        product_data['검색어설정'] = ','.join(keywords)
        
        # 5. 정확한 카테고리 설정
        categories = analysis['categories']
        product_data['상품분류 번호'] = '|'.join(map(str, categories))
        product_data['상품분류 신상품영역'] = '|'.join(['N'] * len(categories))
        product_data['상품분류 추천상품영역'] = '|'.join(['Y'] * len(categories))
        
        return product_data
    
    def process_csv(self, input_file: str, output_file: str = None):
        """CSV 파일 처리"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = input_file.replace('.csv', f'_FINAL_FIXED_{timestamp}.csv')
        
        # CSV 읽기
        with open(input_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            fieldnames = reader.fieldnames
        
        print(f"\n총 {len(rows)}개 상품 AI 처리 시작")
        
        # 처리
        processed = []
        success_count = 0
        category_stats = {}
        
        for i, row in enumerate(rows, 1):
            print(f"\n[{i}/{len(rows)}]")
            result = self.process_product(row)
            processed.append(result)
            
            # 통계 수집
            categories = result.get('상품분류 번호', '56')
            if categories in category_stats:
                category_stats[categories] += 1
            else:
                category_stats[categories] = 1
            
            # AI 성공 카운트
            if '...' not in result.get('상품 요약설명', ''):
                success_count += 1
        
        # 저장
        with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(processed)
        
        print(f"\n\n" + "="*60)
        print(f"처리 완료!")
        print(f"총 상품: {len(rows)}개")
        print(f"AI 성공: {success_count}개 ({success_count/len(rows)*100:.1f}%)")
        print(f"\n카테고리 분포:")
        for cat, count in sorted(category_stats.items()):
            print(f"  {cat}: {count}개")
        print(f"\n결과 파일: {output_file}")
        print("="*60)
        
        return output_file

def main():
    """메인 실행"""
    print("\n" + "="*60)
    print("최종 수정된 AI 시스템")
    print("카테고리 매칭 및 검색어 생성 개선")
    print("="*60)
    
    system = FinalFixedAISystem()
    
    # 테스트 파일 처리
    test_file = "data/input/cafe24_test.csv"
    
    if os.path.exists(test_file):
        print(f"\n파일 처리: {test_file}")
        output = system.process_csv(test_file)
    else:
        # 단일 테스트
        test = {
            '상품명': '[씨씨더블유]매콤 직화무뼈닭발 250g'
        }
        result = system.process_product(test)
        print("\n테스트 결과:")
        print(f"요약: {result.get('상품 요약설명', '')}")
        print(f"간략: {result.get('상품 간략설명', '')}")
        print(f"카테고리: {result.get('상품분류 번호', '')}")

if __name__ == "__main__":
    main()
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
실제 AI API 협업 시스템 (수정된 버전)
API 호출 오류 수정
"""

# 환경변수 로드
load_dotenv()

class FixedAISystem:
    """수정된 실제 AI API 시스템"""
    
    def __init__(self):
        # API 키 설정
        self.setup_apis()
        
        # 필수 키워드
        self.required_keywords = [
            "만원요리", "최씨남매", "집밥각", "술한잔",
            "반찬고민끝", "국물땡김", "혼밥만세", "시간없어",
            "힘내자", "모임각"
        ]
        
        # 카테고리 규칙
        self.category_rules = {
            '닭발': [53, 95, 99, 103, 56, 110],
            '막창': [53, 95, 98, 99, 103, 56, 110],
            '찌개': [56, 97, 102, 109],
            '수산물': [97, 99, 103]
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
        """상품 분석"""
        # 브랜드 추출
        brand = ''
        clean_name = product_name
        
        for b in ['[씨씨더블유]', '[인생]', '[태공식품]']:
            if b in product_name:
                brand = b.replace('[', '').replace(']', '')
                clean_name = product_name.replace(b, '').strip()
                break
        
        # 오타 수정
        for wrong, correct in self.corrections.items():
            clean_name = clean_name.replace(wrong, correct)
        
        # 카테고리 결정
        categories = []
        for keyword, cat_list in self.category_rules.items():
            if keyword in clean_name:
                categories = cat_list
                break
        if not categories:
            categories = [56]  # 기본값
        
        return {
            'brand': brand,
            'clean_name': clean_name,
            'categories': categories
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
    
    def generate_with_gemini(self, product_info: Dict) -> Dict:
        """Gemini API로 생성 - 수정된 버전"""
        if not self.gemini:
            return None
        
        prompt = f"""
        한국 이커머스 상품 설명 생성:
        상품: {product_info['clean_name']}
        브랜드: {product_info['brand']}
        
        요구사항:
        - 요약설명: 40자
        - 간략설명: 50자
        - 브랜드명 제외
        - 매력적인 표현
        
        JSON만 응답: {{"요약설명": "텍스트", "간략설명": "텍스트"}}
        """
        
        try:
            response = self.gemini.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.7,
                    'max_output_tokens': 200,
                }
            )
            
            content = response.text.strip()
            if '{' in content and '}' in content:
                json_str = content[content.find('{'):content.rfind('}')+1]
                result = json.loads(json_str)
                print(f"  Gemini 생성 성공: {result}")
                return result
            return None
        except Exception as e:
            print(f"  Gemini API 오류: {e}")
            return None
    
    def generate_keywords(self, product_info: Dict, description: str) -> List[str]:
        """키워드 생성"""
        keywords = self.required_keywords.copy()
        
        # 제품명에서 키워드 추출
        name_parts = product_info['clean_name'].replace(',', '').split()
        keywords.extend([p for p in name_parts if len(p) > 1])
        
        # 브랜드별 키워드
        if product_info['brand'] == '씨씨더블유':
            keywords.extend(['프리미엄', '최고급', '특별한날'])
        elif product_info['brand'] == '인생':
            keywords.extend(['가성비', '혼밥', '간편식'])
        elif product_info['brand'] == '태공식품':
            keywords.extend(['전통', '건강식', '웰빙'])
        
        # 일반 키워드
        keywords.extend(['간편요리', '에어프라이어', '전자레인지', '안주', '밑반찬'])
        
        # 중복 제거, 40개 제한
        seen = set()
        unique = []
        for k in keywords:
            if k not in seen and len(unique) < 40:
                seen.add(k)
                unique.append(k)
        
        return unique
    
    def process_product(self, product_data: Dict) -> Dict:
        """상품 처리 - AI 생성"""
        product_name = product_data.get('상품명', '')
        
        # 1. 상품 분석
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
        
        # Gemini 시도
        if not result and self.gemini:
            print("  Gemini API 호출...")
            result = self.generate_with_gemini(analysis)
        
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
        
        # 4. 키워드 생성
        keywords = self.generate_keywords(analysis, product_data.get('상품 요약설명', ''))
        product_data['검색어설정'] = ','.join(keywords)
        
        # 5. 카테고리 설정
        categories = analysis['categories']
        product_data['상품분류 번호'] = '|'.join(map(str, categories))
        product_data['상품분류 신상품영역'] = '|'.join(['N'] * len(categories))
        product_data['상품분류 추천상품영역'] = '|'.join(['Y'] * len(categories))
        
        return product_data
    
    def process_csv(self, input_file: str, output_file: str = None):
        """CSV 파일 처리"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = input_file.replace('.csv', f'_FIXED_AI_{timestamp}.csv')
        
        # CSV 읽기
        with open(input_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            fieldnames = reader.fieldnames
        
        print(f"\n총 {len(rows)}개 상품 AI 처리 시작")
        
        # 처리
        processed = []
        success_count = 0
        for i, row in enumerate(rows, 1):
            print(f"\n[{i}/{len(rows)}]")
            result = self.process_product(row)
            processed.append(result)
            
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
        print(f"결과 파일: {output_file}")
        print("="*60)
        
        return output_file

def main():
    """메인 실행"""
    print("\n" + "="*60)
    print("수정된 실제 AI API 협업 시스템")
    print("API 오류 수정 완료 버전")
    print("="*60)
    
    system = FixedAISystem()
    
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

if __name__ == "__main__":
    main()
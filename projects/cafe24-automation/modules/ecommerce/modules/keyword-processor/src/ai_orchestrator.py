#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI 오케스트레이터 시스템
Claude가 지휘하고 여러 AI를 활용하는 고급 시스템
"""

import os
import csv
import json
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

# AI 라이브러리들
import anthropic  # Claude
import openai  # GPT
import google.generativeai as genai  # Gemini

load_dotenv('../../../shared/config/.env')

class AIOrchestrator:
    """Claude가 지휘하는 멀티 AI 시스템"""
    
    def __init__(self):
        # Claude (지휘자)
        self.claude_key = os.getenv('ANTHROPIC_API_KEY')
        if self.claude_key:
            self.claude = anthropic.Anthropic(api_key=self.claude_key)
        
        # OpenAI (실행자 1)
        self.openai_key = os.getenv('OPENAI_API_KEY')
        if self.openai_key:
            openai.api_key = self.openai_key
            self.openai_client = openai.OpenAI()
        
        # Gemini (실행자 2)
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)
            self.gemini = genai.GenerativeModel('gemini-1.5-flash')
        
        # Perplexity (검증자)
        self.perplexity_key = os.getenv('PERPLEXITY_API_KEY')
        if self.perplexity_key:
            # Perplexity는 OpenAI 호환 API 사용
            from openai import OpenAI
            self.perplexity = OpenAI(
                api_key=self.perplexity_key,
                base_url="https://api.perplexity.ai"
            )
        
        print("\n=== AI 오케스트레이터 초기화 ===")
        print(f"Claude: {'활성화' if self.claude_key else '비활성'}")
        print(f"OpenAI: {'활성화' if self.openai_key else '비활성'}")
        print(f"Gemini: {'활성화' if self.gemini_key else '비활성'}")
        print(f"Perplexity: {'활성화' if self.perplexity_key else '비활성'}")
    
    def claude_orchestrate(self, product_info: Dict) -> Dict:
        """멀티 AI 오케스트레이션"""
        
        product_name = product_info.get('상품명', '')
        
        # 1단계: 전략 수립
        strategy = self._claude_strategy(product_name)
        
        # 2단계: 각 AI에게 작업 할당
        results = {
            'strategy': strategy,
            'keywords': [],
            'description': ''
        }
        
        # OpenAI로 키워드 생성
        if hasattr(self, 'openai_client'):
            openai_keywords = self._openai_generate_keywords(product_name)
            results['keywords'].extend(openai_keywords)
        
        # Gemini로 추가 키워드 생성
        if hasattr(self, 'gemini'):
            gemini_keywords = self._gemini_generate_keywords(product_name)
            results['keywords'].extend(gemini_keywords)
        
        # Perplexity는 제외 (조사 목적으로만 사용)
        
        # 3단계: 최종 검토 및 조정
        final_keywords = self._claude_finalize(results['keywords'], product_name)
        
        # 상품명에서 공급사 제거
        clean_name = product_name
        if '[' in clean_name and ']' in clean_name:
            # [공급사명] 부분 제거
            start = clean_name.find('[')
            end = clean_name.find(']') + 1
            supplier = clean_name[start:end]
            clean_name = clean_name.replace(supplier, '').strip()
        
        # 카테고리별 설명 생성
        if any(word in product_name for word in ['닭발', '막창', '오돌뼈', '족발', '곱창']):
            summary = f"{clean_name} - 술안주 베스트"
            brief = f"{clean_name} - 인기 술안주 간편조리"
        elif any(word in product_name for word in ['국', '탕', '찌개']):
            summary = f"{clean_name} - 든든한 한끼"
            brief = f"{clean_name} - 집밥 스타일 국물요리"
        elif any(word in product_name for word in ['반찬', '김치']):
            summary = f"{clean_name} - 밥상 필수 반찬"
            brief = f"{clean_name} - 매일 먹는 기본 반찬"
        elif '밀키트' in product_name:
            summary = f"{clean_name} - 간편 밀키트"
            brief = f"{clean_name} - 10분 완성 간편조리"
        else:
            summary = f"{clean_name} - 만원요리 인기상품"
            brief = f"{clean_name} - 최씨남매 추천 맛보장"
        
        # SEO 최적화 필드 생성
        seo_title = f"{clean_name[:30]} - 만원요리 최씨남매 추천 프리미엄 상품"
        seo_author = "만원요리 최씨남매"
        seo_description = f"만원요리 최씨남매에서 엄선한 {clean_name[:40]}. {brief[:20]}. 정품 보장, 프리미엄 품질로 집에서 간편하게 즐기세요."
        seo_keywords = ','.join(final_keywords[:30])  # 상위 30개만 사용
        seo_alt = f"만원요리 최씨남매 {clean_name[:40]} 상품 이미지"
        
        return {
            '검색어설정': ','.join(final_keywords[:40]),
            '상품 요약설명': summary[:50],
            '상품 간략설명': brief[:100],
            '검색엔진최적화(SEO) Title': seo_title[:100],
            '검색엔진최적화(SEO) Author': seo_author,
            '검색엔진최적화(SEO) Description': seo_description[:200],
            '검색엔진최적화(SEO) Keywords': seo_keywords,
            '검색엔진최적화(SEO) 상품 이미지 Alt 텍스트': seo_alt[:80]
        }
    
    def _claude_strategy(self, product_name: str) -> str:
        """Claude 역할 - 규칙 기반 전략 수립"""
        # Claude API 없이 규칙 기반으로 전략 결정
        strategy = "기본 전략: "
        
        if any(word in product_name for word in ['닭발', '막창', '곱창', '소대창']):
            strategy = "술안주 전략: 맥주, 소주와 어울리는 키워드 강화"
        elif any(word in product_name for word in ['찌개', '국', '탕']):
            strategy = "집밥 전략: 가정식, 든든한 한끼 키워드 강화"
        elif any(word in product_name for word in ['갈비', '삼겹살', '목살']):
            strategy = "프리미엄 전략: 고급, 특별한 날 키워드 강화"
        else:
            strategy = "만능 전략: 간편, 맛있는, 인기 키워드 균형"
        
        return strategy
    
    def _openai_generate_keywords(self, product_name: str) -> List[str]:
        """OpenAI로 키워드 생성"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": "한국 이커머스 키워드 전문가"
                }, {
                    "role": "user",
                    "content": f"'{product_name}' 상품의 검색 키워드 20개를 쉼표로 구분하여 제시하세요."
                }],
                temperature=0.7,
                max_tokens=200
            )
            keywords = response.choices[0].message.content.split(',')
            return [k.strip() for k in keywords if k.strip()][:20]
        except:
            return []
    
    def _gemini_generate_keywords(self, product_name: str) -> List[str]:
        """Gemini로 키워드 생성"""
        try:
            response = self.gemini.generate_content(
                f"한국 이커머스 상품 '{product_name}'의 인기 검색 키워드 20개를 쉼표로 구분하여 나열하세요."
            )
            keywords = response.text.split(',')
            return [k.strip() for k in keywords if k.strip()][:20]
        except:
            return []
    
    def _perplexity_generate_keywords(self, product_name: str) -> List[str]:
        """Perplexity로 최신 트렌드 키워드 검색"""
        try:
            response = self.perplexity.chat.completions.create(
                model="sonar",  # Perplexity 기본 모델
                messages=[{
                    "role": "system",
                    "content": "최신 한국 이커머스 트렌드 전문가"
                }, {
                    "role": "user",
                    "content": f"'{product_name}' 관련 2024-2025년 최신 트렌드 키워드 15개를 쉼표로 구분하여 제시하세요. 실시간 검색 트렌드를 반영해주세요."
                }],
                temperature=0.7,
                max_tokens=200
            )
            keywords = response.choices[0].message.content.split(',')
            return [k.strip() for k in keywords if k.strip()][:15]
        except Exception as e:
            print(f"Perplexity 오류: {e}")
            return []
    
    def _claude_finalize(self, keywords: List[str], product_name: str) -> List[str]:
        """Claude가 최종 키워드 선별 및 필수 키워드 추가"""
        # 필수 키워드 추가
        essential_keywords = self._get_essential_keywords(product_name)
        
        # 기존 키워드와 필수 키워드 병합
        all_keywords = essential_keywords + keywords
        
        # 중복 제거하면서 순서 유지
        seen = set()
        final_keywords = []
        for k in all_keywords:
            if k not in seen:
                seen.add(k)
                final_keywords.append(k)
        
        return final_keywords[:40]
    
    def _get_essential_keywords(self, product_name: str) -> List[str]:
        """상품명에 따른 필수 키워드 매칭"""
        essential = []
        
        # 1. 브랜드 필수 (항상 포함)
        essential.extend(['만원요리', '최씨남매'])
        
        # 2. 상품별 매칭
        name_lower = product_name.lower()
        
        # 술안주류
        if any(word in product_name for word in ['닭발', '막창', '오돌뼈', '족발', '곱창', '순대']):
            essential.extend(['술한잔', '모임각', '술안주'])
        
        # 국/탕/찌개류
        if any(word in product_name for word in ['국', '탕', '찌개', '전골']):
            essential.extend(['국물땡김', '집밥각'])
            if '부대찌개' in product_name:
                essential.append('부대찌개')
        
        # 반찬류
        if any(word in product_name for word in ['반찬', '김치', '장아찌', '젓갈']):
            essential.extend(['반찬고민끝', '집밥각'])
            if '김치' in product_name:
                essential.append('김치')
        
        # 1인/간편식
        if any(word in product_name for word in ['도시락', '볶음밥', '덮밥', '간편']):
            essential.extend(['혼밥만세', '시간없어', '간편식'])
        
        # 밀키트
        if '밀키트' in product_name or 'KIT' in product_name.upper():
            essential.extend(['밀키트', '간편식'])
        
        # 해물류
        if any(word in product_name for word in ['해물', '새우', '오징어', '낙지', '문어']):
            essential.append('해물')
        
        # 떡/떡볶이
        if '떡' in product_name:
            essential.append('떡')
            if '떡볶이' in product_name:
                essential.append('떡볶이')
        
        # 면류
        if any(word in product_name for word in ['냉면', '국수', '라면', '우동', '파스타']):
            if '냉면' in product_name:
                essential.append('냉면')
        
        # 캠핑
        if any(word in product_name for word in ['캠핑', 'BBQ', '바베큐']):
            essential.append('캠핑')
        
        # 토마토 소스
        if '토마토' in product_name:
            essential.append('토마토소스')
        
        # 인절미/디저트
        if any(word in product_name for word in ['인절미', '떡', '디저트', '케이크']):
            if '인절미' in product_name:
                essential.append('인절미')
        
        # 에너지/보양식
        if any(word in product_name for word in ['삼계탕', '보양', '갈비', '추어탕']):
            essential.append('힘내자')
        
        return essential
    
    def _generate_basic_keywords(self, product_name: str):
        """기본 키워드 생성 (API 실패시)"""
        keywords = []
        
        # 필수 키워드
        keywords.extend(['만원요리', '최씨남매', '집밥각', '술한잔'])
        
        # 상품명 분해
        name_parts = product_name.replace('[', ' ').replace(']', ' ').split()
        keywords.extend([p for p in name_parts if len(p) > 1][:10])
        
        # 카테고리 키워드
        keywords.extend([
            '간편요리', '간편식', '밀키트', '혼밥', '자취요리',
            '맛집', '인기상품', '베스트', '추천', '신상품',
            '할인', '특가', '무료배송', '당일배송', '새벽배송'
        ])
        
        return keywords[:40]
    
    def process_csv(self, input_file: str, output_file: str):
        """CSV 파일 처리"""
        print(f"\n입력 파일: {input_file}")
        
        # 읽기
        with open(input_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            fieldnames = reader.fieldnames
        
        print(f"총 {len(rows)}개 상품 처리 시작")
        print("Claude 오케스트레이터가 지휘합니다...")
        
        # 처리
        processed = []
        for i, row in enumerate(rows, 1):
            print(f"[{i}/{len(rows)}] AI 처리 중...")
            
            # AI 오케스트레이션
            result = self.claude_orchestrate(row)
            
            # 결과 병합
            for key, value in result.items():
                if key in row:
                    row[key] = value
            
            processed.append(row)
            
            # 10개마다 진행상황 표시
            if i % 10 == 0:
                print(f"  - {i}개 완료")
        
        # 저장
        with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(processed)
        
        print(f"\n처리 완료: {output_file}")
        return output_file

def main():
    """메인 실행"""
    orchestrator = AIOrchestrator()
    
    # input 폴더에서 CSV 파일 찾기
    input_dir = "../../../data/input"
    csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"오류: {input_dir} 폴더에 CSV 파일이 없습니다!")
        return
    
    # 메인 처리 파일 우선 선택
    main_files = [f for f in csv_files if 'manwonyori_20250828_284_4600' in f]
    if main_files:
        input_file = os.path.join(input_dir, main_files[0])
    else:
        input_file = os.path.join(input_dir, csv_files[0])
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = os.path.splitext(csv_files[0])[0]
    output_file = f"../../../data/output/{base_name}_AI멀티_{timestamp}.csv"
    
    print("\n" + "="*60)
    print("Claude AI 오케스트레이터 시스템")
    print("Claude 지휘 + OpenAI + Gemini (안정화 버전)")
    print("="*60)
    
    result = orchestrator.process_csv(input_file, output_file)
    
    if result:
        print("\n" + "="*60)
        print("멀티 AI 처리 완료!")
        print(f"결과: {result}")
        print("="*60)

if __name__ == "__main__":
    main()
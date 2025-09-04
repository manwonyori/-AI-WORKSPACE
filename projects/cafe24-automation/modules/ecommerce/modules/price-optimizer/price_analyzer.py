#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
가격 최적화 분석 시스템
경쟁업체 가격 분석 및 최적 가격 제안
"""

import csv
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional
import sys
import os

# 공통 설정 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))
from dotenv import load_dotenv

load_dotenv('../../shared/config/.env')

class PriceOptimizer:
    def __init__(self):
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.competitors = {
            '쿠팡': 'coupang.com',
            '11번가': '11st.co.kr', 
            '지마켓': 'gmarket.co.kr',
            '옥션': 'auction.co.kr',
            '인터파크': 'interpark.com'
        }
        
        print("=== 가격 최적화 시스템 초기화 ===")
        print(f"OpenAI API: {'활성화' if self.openai_key else '비활성'}")
        print(f"경쟁업체: {len(self.competitors)}개 모니터링")
    
    def _safe_int_convert(self, value):
        """안전한 정수 변환 헬퍼 메소드"""
        try:
            if value is None or value == '':
                return 0
            # 문자열 변환 후 쉼표와 공백 제거
            cleaned = str(value).replace(',', '').replace(' ', '').strip()
            return int(cleaned) if cleaned else 0
        except (ValueError, TypeError):
            return 0
    
    def analyze_price_strategy(self, product_info: Dict) -> Dict:
        """가격 전략 분석 - 개선된 버전"""
        """가격 전략 분석"""
        product_name = product_info.get('상품명', '')
        # 실제 CSV 필드명에 맞게 수정 - 공급가가 실제 원가
        # 안전한 숫자 변환
        current_price = self._safe_int_convert(product_info.get('판매가', 0))
        supply_price = self._safe_int_convert(product_info.get('공급가', 0))
        
        print(f"상품명: {product_name}")
        print(f"판매가: {current_price}, 공급가(원가): {supply_price}")
        
        # 1. 마진율 계산 (올바른 공식: (판매가-공급가)/판매가*100)
        if current_price > 0 and supply_price >= 0:
            margin_rate = round(((current_price - supply_price) / current_price) * 100, 2)
            margin_rate = max(0.0, min(100.0, margin_rate))  # 0-100% 범위 제한
        else:
            margin_rate = 0.0
        
        # 2. 가격대 분석
        price_tier = self._classify_price_tier(current_price)
        
        # 3. 경쟁 가격 추정 (실제 API 연동 시 대체)
        estimated_competitor_price = self._estimate_competitor_price(product_name, current_price)
        
        # 4. 최적 가격 제안
        optimal_prices = self._suggest_optimal_prices(supply_price, current_price, estimated_competitor_price)
        
        return {
            '현재가격': current_price,
            '공급가격': supply_price,
            '마진율': round(margin_rate, 2),
            '가격대': price_tier,
            '경쟁가격_추정': estimated_competitor_price,
            '최적가격_제안': optimal_prices,
            '가격전략': self._generate_price_strategy(margin_rate, price_tier)
        }
    
    def _classify_price_tier(self, price: int) -> str:
        """가격대 분류"""
        if price < 3000:
            return "저가형"
        elif price < 8000:
            return "중저가형"  
        elif price < 15000:
            return "중가형"
        elif price < 30000:
            return "중고가형"
        else:
            return "고가형"
    
    def _estimate_competitor_price(self, product_name: str, current_price: int) -> Dict:
        """경쟁업체 가격 추정 (AI 기반)"""
        if not self.openai_key:
            return {"추정불가": "API 키 필요"}
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": "한국 이커머스 가격 분석 전문가"
                }, {
                    "role": "user", 
                    "content": f"""
                    상품: {product_name}
                    현재가격: {current_price:,}원
                    
                    주요 온라인 쇼핑몰에서의 예상 가격대를 분석해주세요:
                    - 쿠팡, 11번가, 지마켓, 옥션 기준
                    - JSON 형식으로 응답
                    
                    {{
                        "쿠팡_예상가": 가격,
                        "11번가_예상가": 가격,
                        "지마켓_예상가": 가격,
                        "옥션_예상가": 가격,
                        "평균가": 가격,
                        "최저가": 가격,
                        "최고가": 가격
                    }}
                    """
                }],
                temperature=0.3,
                max_tokens=300
            )
            
            content = response.choices[0].message.content
            if '{' in content:
                json_str = content[content.find('{'):content.rfind('}')+1]
                return json.loads(json_str)
            
        except Exception as e:
            import logging
            logging.error(f"AI 가격 분석 오류: {e}")
            print(f"AI 가격 분석 오류: {e}")
        
        # AI 실패시 기본 추정
        return {
            "쿠팡_예상가": int(current_price * 0.95),
            "11번가_예상가": int(current_price * 0.98),
            "지마켓_예상가": int(current_price * 1.02),
            "옥션_예상가": int(current_price * 0.97),
            "평균가": int(current_price * 0.98),
            "최저가": int(current_price * 0.90),
            "최고가": int(current_price * 1.05)
        }
    
    def _suggest_optimal_prices(self, cost_price: int, current_price: int, competitor_data: Dict) -> Dict:
        """최적 가격 제안"""
        if isinstance(competitor_data, dict) and '평균가' in competitor_data:
            avg_competitor = competitor_data['평균가']
            min_competitor = competitor_data['최저가']
        else:
            avg_competitor = int(current_price * 0.98)
            min_competitor = int(current_price * 0.90)
        
        # 최소 마진 20% 보장
        min_selling_price = int(cost_price * 1.25)
        
        suggestions = {
            "공격적_가격": max(min_selling_price, int(min_competitor * 0.98)),
            "경쟁적_가격": max(min_selling_price, int(avg_competitor * 0.99)),
            "안전적_가격": max(min_selling_price, int(avg_competitor * 1.02)),
            "프리미엄_가격": max(min_selling_price, int(avg_competitor * 1.08))
        }
        
        return suggestions
    
    def _generate_price_strategy(self, margin_rate: float, price_tier: str) -> str:
        """가격 전략 생성"""
        if margin_rate < 15:
            return f"{price_tier} 상품 - 마진 개선 필요 (현재 {margin_rate:.1f}%)"
        elif margin_rate < 25:
            return f"{price_tier} 상품 - 적정 마진 유지 (현재 {margin_rate:.1f}%)" 
        elif margin_rate < 40:
            return f"{price_tier} 상품 - 양호한 마진 (현재 {margin_rate:.1f}%)"
        else:
            return f"{price_tier} 상품 - 높은 마진, 가격 경쟁력 검토 필요 (현재 {margin_rate:.1f}%)"
    
    def process_csv(self, input_file: str, output_file: str):
        """CSV 파일 가격 분석"""
        print(f"\n가격 분석 시작: {input_file}")
        
        # 읽기
        with open(input_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            fieldnames = list(reader.fieldnames) + [
                '마진율(%)', '가격대', '경쟁가격_평균', '최적가격_제안', '가격전략'
            ]
        
        print(f"총 {len(rows)}개 상품 가격 분석")
        
        # 처리
        processed = []
        for i, row in enumerate(rows, 1):
            print(f"[{i}/{len(rows)}] 가격 분석 중...")
            
            analysis = self.analyze_price_strategy(row)
            
            # 결과 추가
            row['마진율(%)'] = analysis['마진율']
            row['가격대'] = analysis['가격대']
            row['경쟁가격_평균'] = analysis['경쟁가격_추정'].get('평균가', 0)
            row['최적가격_제안'] = str(analysis['최적가격_제안'])
            row['가격전략'] = analysis['가격전략']
            
            processed.append(row)
            
            if i % 10 == 0:
                print(f"  - {i}개 완료")
        
        # 저장
        with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(processed)
        
        print(f"\n가격 분석 완료: {output_file}")
        return output_file

def main():
    """메인 실행"""
    optimizer = PriceOptimizer()
    
    # input 폴더에서 CSV 파일 찾기
    input_dir = "../../data/output"  # 키워드 처리된 파일 사용
    print(f"입력 폴더 확인: {os.path.abspath(input_dir)}")
    
    if os.path.exists(input_dir):
        csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
        print(f"발견된 CSV 파일: {csv_files}")
        if csv_files:
            input_file = os.path.join(input_dir, csv_files[-1])  # 최신 파일
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            base_name = os.path.splitext(csv_files[-1])[0]
            output_file = f"../../data/output/{base_name}_가격분석_{timestamp}.csv"
            
            print("\n" + "="*60)
            print("가격 최적화 분석 시스템")
            print("경쟁업체 가격 분석 및 최적 가격 제안")
            print("="*60)
            
            result = optimizer.process_csv(input_file, output_file)
            
            if result:
                print("\n" + "="*60)
                print("가격 분석 완료!")
                print(f"결과: {result}")
                print("="*60)
        else:
            print("처리할 CSV 파일이 없습니다!")
    else:
        print("input 폴더를 찾을 수 없습니다!")

if __name__ == "__main__":
    main()
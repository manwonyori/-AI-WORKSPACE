#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from anthropic import Anthropic
from dotenv import load_dotenv
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import google.generativeai as genai
import openai
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import asyncio
import csv
import json
import logging
import os
import shutil
import sys
import time

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
카페24 AI 협업 시스템 - 올인원 솔루션
실시간 폴더 감시 + AI 처리 + 가격 분석
"""

# API 관련 imports
try:
    OPENAI_AVAILABLE = True
except:
    OPENAI_AVAILABLE = False

try:
    CLAUDE_AVAILABLE = True
except:
    CLAUDE_AVAILABLE = False

try:
    GEMINI_AVAILABLE = True
except:
    GEMINI_AVAILABLE = False

# 폴더 감시
try:
    WATCHDOG_AVAILABLE = True
except:
    WATCHDOG_AVAILABLE = False
    print("watchdog 설치 필요: pip install watchdog")

# 환경변수 로드
try:
    load_dotenv()
except:
    print(".env 파일 직접 로드")

# ============================================
# 설정
# ============================================

class Config:
    """시스템 설정"""
    
    # 폴더 경로
    BASE_DIR = Path(__file__).parent
    INPUT_DIR = BASE_DIR / "data" / "input"
    OUTPUT_DIR = BASE_DIR / "data" / "output"
    
    # API 키 (환경변수에서 로드)
    OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    PERPLEXITY_KEY = os.getenv("PERPLEXITY_API_KEY", "")
    GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # 카페24 설정
    CAFE24_MALL_ID = os.getenv("CAFE24_MALL_ID", "manwonyori")
    CAFE24_ACCESS_TOKEN = os.getenv("CAFE24_ACCESS_TOKEN", "")
    
    # 필수 링크 키워드
    REQUIRED_KEYWORDS = [
        "만원요리", "최씨남매",
        "집밥각", "술한잔", "반찬고민끝",
        "국물땡김", "혼밥만세", "시간없어",
        "힘내자", "모임각"
    ]
    
    # 마진 그룹
    MARGIN_GROUPS = {
        "초저마진": (0, 5),
        "저마진": (5, 10),
        "표준마진": (10, 15),
        "고마진": (15, 20),
        "프리미엄": (20, 100)
    }
    
    # 브랜드 톤
    BRAND_TONES = {
        "씨씨더블유": {"tone": "프리미엄", "target": "30-40대 가정"},
        "인생": {"tone": "가성비", "target": "20-30대 1인가구"},
        "태공식품": {"tone": "전통", "target": "건강 중시 고객"}
    }

# ============================================
# AI 처리 엔진
# ============================================

class AIEngine:
    """다중 AI API 처리 엔진"""
    
    def __init__(self):
        self.apis = self._init_apis()
        
    def _init_apis(self):
        """사용 가능한 API 초기화"""
        apis = []
        
        if CLAUDE_AVAILABLE and Config.ANTHROPIC_KEY:
            apis.append("claude")
        if GEMINI_AVAILABLE and Config.GEMINI_KEY:
            apis.append("gemini")
        if OPENAI_AVAILABLE and Config.OPENAI_KEY:
            apis.append("openai")
            
        if not apis:
            print("경고: API가 설정되지 않음. 로컬 처리 모드")
            apis.append("local")
            
        return apis
    
    async def process_product(self, product_data: Dict) -> Dict:
        """상품 데이터 AI 처리"""
        
        # API 우선순위대로 시도
        for api_name in self.apis:
            try:
                if api_name == "claude":
                    return await self._claude_process(product_data)
                elif api_name == "gemini":
                    return await self._gemini_process(product_data)
                elif api_name == "openai":
                    return await self._openai_process(product_data)
                else:
                    return self._local_process(product_data)
            except Exception as e:
                print(f"{api_name} 실패: {e}")
                continue
        
        return self._local_process(product_data)
    
    def _local_process(self, product_data: Dict) -> Dict:
        """로컬 처리 (API 없을 때) - 창의적 처리"""
        # 카페24 필드명 읽기
        name = product_data.get('상품명', '')
        
        # 브랜드 추출 및 정리
        brand = ''
        clean_name = name
        if '[씨씨더블유]' in name:
            brand = '씨씨더블유'
            clean_name = name.replace('[씨씨더블유]', '').strip()
        elif '[인생]' in name:
            brand = '인생'
            clean_name = name.replace('[인생]', '').strip()
        elif '[태공식품]' in name:
            brand = '태공식품'
            clean_name = name.replace('[태공식품]', '').strip()
        
        # 상품 특성 분석
        is_spicy = '매콤' in clean_name or '매운' in clean_name
        is_grilled = '직화' in clean_name or '구이' in clean_name
        is_boneless = '무뼈' in clean_name
        is_stew = '찌개' in clean_name or '조림' in clean_name
        
        # 용량 추출
        weight_match = re.search(r'(\d+)(g|kg|ml|L)', clean_name)
        weight = weight_match.group() if weight_match else ''
        
        # 브랜드별 창의적 설명 생성
        if brand == '씨씨더블유':
            if '닭발' in clean_name:
                if is_spicy and is_grilled:
                    summary = f"씨씨더블유가 엄선한 국내산 닭발을 특제 매운 양념에 12시간 숙성 후 250도 직화로 구워낸 프리미엄 무뼈닭발로, 쫄깃한 콜라겐과 매콤한 불맛이 일품인 최고급 안주입니다"
                    brief = f"250도 직화로 매콤하게 구워낸 쫄깃한 무뼈닭발 {weight}, 전자레인지 2분이면 완성되는 프리미엄 안주"
                else:
                    summary = f"씨씨더블유 특제 양념으로 정성껏 조리한 프리미엄 닭발로, 쫄깃한 식감과 깊은 맛이 일품인 고단백 안주입니다"
                    brief = f"쫄깃하고 담백한 프리미엄 닭발 {weight}, 간편하게 데워먹는 최고급 안주"
            elif '갈비' in clean_name:
                summary = f"씨씨더블유가 엄선한 최상급 갈비를 48시간 저온 숙성하여 육즙과 부드러움을 극대화한 프리미엄 양념갈비로, 특제 과일 소스가 더해져 단짠의 조화가 일품입니다"
                brief = f"48시간 숙성 프리미엄 양념갈비 {weight}, 에어프라이어로 바삭하게 즐기는 특별한 맛"
            else:
                summary = f"씨씨더블유의 장인정신으로 만든 {clean_name}, 엄선된 재료와 정성스런 조리로 프리미엄 맛을 구현했습니다"
                brief = f"프리미엄 {clean_name} {weight}, 특별한 날을 위한 최고의 선택"
                
        elif brand == '인생':
            if is_stew:
                if '김치' in clean_name:
                    summary = f"진짜 묵은지로 끓여낸 깊고 진한 김치찌개, 3년 숙성 김치와 국내산 돼지고기가 어우러져 집밥 그 이상의 감동을 선사합니다"
                    brief = f"묵은지 김치찌개 {weight}, 밥 한공기 뚝딱! 혼밥족 인생 찌개"
                elif '된장' in clean_name:
                    summary = f"3년 발효 재래식 된장으로 끓여낸 구수한 된장찌개, 건강한 집밥의 정석을 간편하게 즐기는 가성비 최고의 선택입니다"
                    brief = f"구수한 된장찌개 {weight}, 엄마 손맛 그대로 3분 완성"
                else:
                    summary = f"정성껏 끓여낸 {clean_name}, 집밥 그리운 날 딱 좋은 든든한 한 끼"
                    brief = f"든든한 {clean_name} {weight}, 혼밥족을 위한 가성비 최고 선택"
            else:
                summary = f"인생 최고의 가성비 {clean_name}, 부담 없는 가격에 만족스러운 맛으로 일상을 특별하게 만들어드립니다"
                brief = f"가성비 갑 {clean_name} {weight}, 매일 먹어도 부담 없는 실속 만점"
                
        elif brand == '태공식품':
            if '갈치' in clean_name:
                summary = f"제주 은갈치를 전통 비법으로 조린 깊은 맛의 갈치조림, 신선한 해산물과 20년 전통 양념이 어우러진 바다의 진미입니다"
                brief = f"제주 은갈치조림 {weight}, 밥도둑 인증! 바다 내음 가득한 전통의 맛"
            elif '고등어' in clean_name:
                summary = f"노르웨이산 특대 고등어를 참숯으로 구워낸 고소한 고등어구이, 오메가3 가득한 건강식으로 온 가족이 즐기는 웰빙 수산물입니다"
                brief = f"참숯 고등어구이 {weight}, DHA 가득! 노릇노릇 바삭한 건강 밥상"
            else:
                summary = f"태공식품 20년 전통의 {clean_name}, 신선한 해산물과 정직한 조리법으로 바다의 참맛을 전합니다"
                brief = f"신선한 {clean_name} {weight}, 바다에서 온 건강한 단백질"
        else:
            # 브랜드 없는 경우
            summary = f"정성껏 준비한 {clean_name}, 품질과 맛으로 승부하는 실속 만점 제품입니다"
            brief = f"{clean_name} {weight}, 간편하게 즐기는 맛있는 한 끼"
        
        # 카페24 필드에 적용
        if '상품 요약설명' in product_data:
            product_data['상품 요약설명'] = summary
        
        if '상품 간략설명' in product_data:
            product_data['상품 간략설명'] = brief
        
        if '상품 상세설명' in product_data:
            product_data['상품 상세설명'] = summary + " " + brief  # 상세설명은 요약+간략 조합
        
        # 검색어설정 - 우리가 논의한 대로
        if '검색어설정' in product_data:
            keywords = []
            # 필수 키워드
            keywords.extend(["만원요리", "최씨남매"])
            # 링크 키워드 (정확히)
            keywords.extend(["집밥각", "술한잔", "반찬고민끝", "국물땡김", "혼밥만세", "시간없어", "힘내자", "모임각"])
            
            # 상품 특성 키워드
            if is_spicy:
                keywords.extend(["매콤한", "매운맛", "불맛"])
            if is_grilled:
                keywords.extend(["직화구이", "숯불구이", "바베큐"])
            if is_boneless:
                keywords.extend(["무뼈", "순살", "먹기편한"])
            if is_stew:
                keywords.extend(["찌개", "국물요리", "뜨끈한"])
            
            # 브랜드별 키워드
            if brand == "씨씨더블유":
                keywords.extend(["프리미엄", "최고급", "특별한날"])
            elif brand == "인생":
                keywords.extend(["가성비", "혼밥", "간편식"])
            elif brand == "태공식품":
                keywords.extend(["전통", "건강식", "수산물"])
            
            # 상품명 키워드
            product_keywords = clean_name.replace(',', '').split()
            keywords.extend([k for k in product_keywords if len(k) > 1])
            
            # 추가 일반 키워드
            keywords.extend(["간편요리", "집밥", "안주", "밑반찬", "도시락"])
            
            # 중복 제거 및 40개 제한
            seen = set()
            unique_keywords = []
            for k in keywords:
                if k not in seen and len(unique_keywords) < 40:
                    seen.add(k)
                    unique_keywords.append(k)
            
            product_data['검색어설정'] = ','.join(unique_keywords)
        
        return product_data
    
    async def _claude_process(self, product_data: Dict) -> Dict:
        """Claude API 처리"""
        # TODO: Claude API 구현
        return self._local_process(product_data)
    
    async def _gemini_process(self, product_data: Dict) -> Dict:
        """Gemini API 처리"""
        # TODO: Gemini API 구현
        return self._local_process(product_data)
    
    async def _openai_process(self, product_data: Dict) -> Dict:
        """OpenAI API 처리"""
        # TODO: OpenAI API 구현
        return self._local_process(product_data)

# ============================================
# 가격/마진 분석
# ============================================

class PriceAnalyzer:
    """가격 및 마진 분석기"""
    
    def analyze_file(self, file_path: str) -> Dict:
        """CSV 파일 마진 분석"""
        products = []
        
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # 카페24 필드명 처리
                    supply_price = float(row.get('공급가', row.get('supply_price', 0)))
                    selling_price = float(row.get('판매가', row.get('selling_price', 0)))
                    
                    if supply_price > 0:
                        margin = ((selling_price - supply_price) / supply_price) * 100
                        row['margin_rate'] = margin
                        products.append(row)
                except:
                    continue
        
        # 마진 그룹별 분류
        groups = {name: [] for name in Config.MARGIN_GROUPS}
        
        for product in products:
            margin = product['margin_rate']
            for group_name, (min_rate, max_rate) in Config.MARGIN_GROUPS.items():
                if min_rate <= margin < max_rate:
                    groups[group_name].append(product)
                    break
        
        # 분석 결과
        return {
            'total': len(products),
            'groups': {name: len(items) for name, items in groups.items()},
            'products_by_group': groups,
            'has_issues': groups['초저마진'] or groups['저마진']
        }
    
    def adjust_prices(self, products: List[Dict], new_margin: float) -> List[Dict]:
        """가격 일괄 조정"""
        for product in products:
            supply_price = float(product.get('supply_price', 0))
            if supply_price > 0:
                product['selling_price'] = supply_price * (1 + new_margin / 100)
                product['margin_rate'] = new_margin
        return products

# ============================================
# 폴더 감시
# ============================================

class FileWatcher(FileSystemEventHandler):
    """폴더 감시 및 자동 처리"""
    
    def __init__(self, processor):
        self.processor = processor
        
    def on_created(self, event):
        """새 파일 감지"""
        if event.is_directory:
            return
            
        if event.src_path.endswith('.csv'):
            print(f"\n[감지] 새 파일: {event.src_path}")
# #             time.sleep(1)  # 파일 쓰기 완료 대기
            self.processor.auto_process(event.src_path)

# ============================================
# 메인 프로세서
# ============================================

class Cafe24Processor:
    """카페24 통합 프로세서"""
    
    def __init__(self):
        self.ai_engine = AIEngine()
        self.price_analyzer = PriceAnalyzer()
        self._ensure_directories()
        
    def _ensure_directories(self):
        """필수 디렉토리 생성"""
        Config.INPUT_DIR.mkdir(parents=True, exist_ok=True)
        Config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    def auto_process(self, file_path: str):
        """자동 처리 (AI + 가격 체크)"""
        print(f"처리 시작: {file_path}")
        
        # 1. AI 처리
        asyncio.run(self._process_with_ai(file_path))
        
        # 2. 가격 분석
        analysis = self.price_analyzer.analyze_file(file_path)
        
        # 3. 문제 있으면 알림
        if analysis['has_issues']:
            print("\n" + "="*50)
            print("[경고] 마진 문제 발견!")
            print(f"초저마진: {analysis['groups']['초저마진']}개")
            print(f"저마진: {analysis['groups']['저마진']}개")
            print("메인 메뉴에서 '2. 가격/마진 분석'으로 처리하세요")
            print("="*50)
            
    async def _process_with_ai(self, file_path: str):
        """AI로 파일 처리"""
        output_name = f"{Path(file_path).stem}_AI처리_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        output_path = Config.OUTPUT_DIR / output_name
        
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            original_fieldnames = list(reader.fieldnames)  # 원본 필드명 그대로 유지
        
        processed_rows = []
        for i, row in enumerate(rows, 1):
            print(f"AI 처리 중... [{i}/{len(rows)}]", end='\r')
            processed = await self.ai_engine.process_product(row)
            processed_rows.append(processed)
        
        # 저장 (원본 필드명 그대로 사용)
        with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=original_fieldnames)
            writer.writeheader()
            writer.writerows(processed_rows)
        
        print(f"\n저장 완료: {output_path}")
    
    def interactive_price_adjustment(self):
        """대화형 가격 조정"""
        # 파일 선택
        csv_files = list(Config.OUTPUT_DIR.glob("*.csv"))
        if not csv_files:
            csv_files = list(Config.INPUT_DIR.glob("*.csv"))
        
        if not csv_files:
            print("CSV 파일이 없습니다")
            return
        
        print("\n파일 목록:")
        for i, f in enumerate(csv_files, 1):
            print(f"{i}. {f.name}")
        
        choice = input("\n파일 선택: ")
        try:
            file_path = csv_files[int(choice) - 1]
        except:
            print("잘못된 선택")
            return
        
        # 분석
        analysis = self.price_analyzer.analyze_file(file_path)
        
        print("\n" + "="*50)
        print("마진 분석 결과")
        print("="*50)
        for group_name, count in analysis['groups'].items():
            status = "" if group_name in ["초저마진", "저마진"] else ""
            print(f"{group_name}: {count}개 {status}")
        
        # 조정
        print("\n1. 그룹별 일괄 조정")
        print("2. 개별 조정")
        print("3. 취소")
        
        action = input("\n선택: ")
        
        if action == "1":
            print("\n조정할 그룹:")
            for i, name in enumerate(Config.MARGIN_GROUPS.keys(), 1):
                print(f"{i}. {name}")
            
            group_choice = input("\n선택: ")
            group_names = list(Config.MARGIN_GROUPS.keys())
            
            try:
                group_name = group_names[int(group_choice) - 1]
                new_margin = float(input(f"\n새 마진율(%): "))
                
                # 조정
                products = analysis['products_by_group'][group_name]
                adjusted = self.price_analyzer.adjust_prices(products, new_margin)
                
                print(f"\n{len(adjusted)}개 상품 조정 완료")
                
                # 저장
                save = input("저장하시겠습니까? (y/n): ")
                if save.lower() == 'y':
                    self._save_adjusted_prices(file_path, adjusted)
                    
            except Exception as e:
                print(f"오류: {e}")

    def _save_adjusted_prices(self, original_file: Path, adjusted_products: List[Dict]):
        """조정된 가격 저장"""
        output_name = f"{original_file.stem}_가격조정_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        output_path = Config.OUTPUT_DIR / output_name
        
        # 원본 파일 읽기
        with open(original_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            all_products = list(reader)
            fieldnames = reader.fieldnames
        
        # 조정된 가격 반영
        adjusted_dict = {p['product_name']: p for p in adjusted_products}
        
        for product in all_products:
            if product['product_name'] in adjusted_dict:
                product.update(adjusted_dict[product['product_name']])
        
        # 저장
        with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_products)
        
        print(f"저장 완료: {output_path}")

# ============================================
# 메인 실행
# ============================================

def main():
    """메인 실행 함수"""
    
    processor = Cafe24Processor()
    
    while True:
        print("\n" + "="*50)
        print("카페24 AI 협업 시스템")
        print("="*50)
        print("1. CSV 파일 AI 처리")
        print("2. 가격/마진 분석")
        print("3. 마진 그룹별 가격 조정")
        print("4. 카페24 업로드 (준비중)")
        print("5. 자동 감시 모드")
        print("6. 종료")
        print("-"*50)
        
        choice = input("선택: ").strip()
        
        if choice == "1":
            # 수동 AI 처리
            file_path = input("CSV 파일 경로: ").strip()
            if os.path.exists(file_path):
                processor.auto_process(file_path)
            else:
                print("파일을 찾을 수 없습니다")
                
        elif choice == "2":
            # 가격 분석
            processor.interactive_price_adjustment()
            
        elif choice == "3":
            # 가격 조정
            processor.interactive_price_adjustment()
            
        elif choice == "4":
            print("카페24 업로드 기능 준비중...")
            
        elif choice == "5":
            # 자동 감시 모드
            if not WATCHDOG_AVAILABLE:
                print("watchdog 설치 필요: pip install watchdog")
                continue
                
            print(f"\n폴더 감시 시작: {Config.INPUT_DIR}")
            print("파일을 input 폴더에 넣으면 자동 처리됩니다")
            print("중지: Ctrl+C")
            
            event_handler = FileWatcher(processor)
            observer = Observer()
            observer.schedule(event_handler, str(Config.INPUT_DIR), recursive=False)
            observer.start()
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
                print("\n감시 중지")
            observer.join()
            
        elif choice == "6":
            print("프로그램을 종료합니다")
            break
        else:
            print("잘못된 선택입니다")

if __name__ == "__main__":
    print("\n카페24 AI 협업 시스템 시작...")
    print(f"사용 가능 API: {', '.join(AIEngine().apis)}")
    main()
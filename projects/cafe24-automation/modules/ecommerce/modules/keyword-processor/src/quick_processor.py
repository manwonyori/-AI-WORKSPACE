#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
빠른 처리 스크립트
최소한의 처리로 빠르게 결과 생성
"""

import csv
from datetime import datetime
import json
import os
import sys

class QuickProcessor:
    def __init__(self):
        self.required_keywords = [
            "만원요리", "최씨남매", "집밥각", "술한잔", 
            "반찬고민끝", "국물땡김", "혼밥만세", "시간없어", 
            "힘내자", "모임각"
        ]
    
    def process_row(self, row):
        """행 처리"""
        product_name = row.get('상품명', '')
        
        # 오타 수정
        for field in row:
            if isinstance(row[field], str):
                row[field] = row[field].replace('꾸븐', '구운')
        
        # 공급사 제거하여 깔끔한 이름 생성
        clean_name = product_name
        if '[' in clean_name and ']' in clean_name:
            start = clean_name.find('[')
            end = clean_name.find(']') + 1
            clean_name = clean_name.replace(clean_name[start:end], '').strip()
        
        # 카테고리별 설명 생성
        if any(word in product_name for word in ['닭발', '막창', '오돌뼈', '족발', '곱창']):
            row['상품 요약설명'] = f"{clean_name[:30]} - 술안주 베스트"
            row['상품 간략설명'] = f"{clean_name[:40]} - 인기 술안주"
        elif any(word in product_name for word in ['국', '탕', '찌개']):
            row['상품 요약설명'] = f"{clean_name[:30]} - 든든한 한끼"
            row['상품 간략설명'] = f"{clean_name[:40]} - 집밥 국물요리"
        elif any(word in product_name for word in ['반찬', '김치']):
            row['상품 요약설명'] = f"{clean_name[:30]} - 밥상 필수 반찬"
            row['상품 간략설명'] = f"{clean_name[:40]} - 매일 먹는 기본 반찬"
        elif '밀키트' in product_name:
            row['상품 요약설명'] = f"{clean_name[:30]} - 간편 밀키트"
            row['상품 간략설명'] = f"{clean_name[:40]} - 10분 완성"
        else:
            row['상품 요약설명'] = f"{clean_name[:30]} - 인기상품"
            row['상품 간략설명'] = f"{clean_name[:40]} - 맛보장 상품"
        
        # 키워드 생성 (40개)
        keywords = []
        
        # 1. 브랜드 필수 키워드 (항상 포함)
        keywords.extend(['만원요리', '최씨남매'])
        
        # 2. 상품별 매칭 필수 키워드
        if any(word in product_name for word in ['닭발', '막창', '오돌뼈', '족발', '곱창']):
            keywords.extend(['술한잔', '모임각', '술안주'])
        elif any(word in product_name for word in ['국', '탕', '찌개']):
            keywords.extend(['국물땡김', '집밥각'])
        elif any(word in product_name for word in ['반찬', '김치']):
            keywords.extend(['반찬고민끝', '집밥각'])
        elif any(word in product_name for word in ['간편', '도시락', '볶음밥']):
            keywords.extend(['혼밥만세', '시간없어', '간편식'])
        elif '밀키트' in product_name:
            keywords.extend(['밀키트', '간편식'])
        elif any(word in product_name for word in ['해물', '새우', '오징어']):
            keywords.append('해물')
        elif '떡' in product_name:
            keywords.append('떡')
        elif '냉면' in product_name:
            keywords.append('냉면')
        elif '토마토' in product_name:
            keywords.append('토마토소스')
        elif '인절미' in product_name:
            keywords.append('인절미')
        elif any(word in product_name for word in ['삼계탕', '갈비']):
            keywords.append('힘내자')
        
        # 제품명 키워드
        name_parts = clean_name.replace(',', ' ').replace('(', ' ').replace(')', ' ').split()
        keywords.extend([p for p in name_parts if len(p) > 1][:10])
        
        # 특성별 키워드
        if '매운' in clean_name or '매콤' in clean_name:
            keywords.extend(['매운맛', '매콤한', '칼칼한', '얼큰한', '불닭'])
        if '구운' in clean_name or '직화' in clean_name:
            keywords.extend(['구운', '직화구이', '바삭한', 'BBQ', '숯불'])
        if '김치' in clean_name:
            keywords.extend(['김치', '발효식품', '한국음식', '배추김치'])
        
        # 용도 키워드
        keywords.extend([
            '간편요리', '간편식', '간단조리', '빠른조리',
            '밥반찬', '집반찬', '밑반찬', '메인반찬',
            '술안주', '맥주안주', '소주안주', '와인안주',
            '야식', '야참', '간식', '분식',
            '도시락', '도시락반찬', '캠핑요리',
            '혼밥', '혼술', '자취요리', '1인가구'
        ])
        
        # 조리법 키워드
        keywords.extend([
            '전자레인지', '에어프라이어', '끓이기만', '데우기만',
            '3분요리', '5분요리', '간단조리'
        ])
        
        # 트렌드 키워드
        keywords.extend([
            '인기상품', '베스트', '추천', '신상품',
            '품절대란', '화제상품', '맛집'
        ])
        
        # 중복 제거하고 40개 제한
        unique_keywords = []
        seen = set()
        for k in keywords:
            if k not in seen and len(unique_keywords) < 40:
                seen.add(k)
                unique_keywords.append(k)
        
        # CSV 파일의 실제 필드명 사용
        if '검색어설정' in row:
            row['검색어설정'] = ','.join(unique_keywords)
        elif '상품 검색어' in row:
            row['상품 검색어'] = ','.join(unique_keywords)
        
        # SEO 최적화 필드 생성
        if '검색엔진최적화(SEO) Title' in row:
            row['검색엔진최적화(SEO) Title'] = f"{clean_name[:30]} - 만원요리 최씨남매 추천 프리미엄 상품"
        if '검색엔진최적화(SEO) Author' in row:
            row['검색엔진최적화(SEO) Author'] = "만원요리 최씨남매"
        if '검색엔진최적화(SEO) Description' in row:
            row['검색엔진최적화(SEO) Description'] = f"만원요리 최씨남매에서 엄선한 {clean_name[:40]}. {row['상품 간략설명'][:20]}. 정품 보장, 프리미엄 품질로 집에서 간편하게 즐기세요."
        if '검색엔진최적화(SEO) Keywords' in row:
            row['검색엔진최적화(SEO) Keywords'] = ','.join(unique_keywords[:30])  # 상위 30개만
        if '검색엔진최적화(SEO) 상품 이미지 Alt 텍스트' in row:
            row['검색엔진최적화(SEO) 상품 이미지 Alt 텍스트'] = f"만원요리 최씨남매 {clean_name[:40]} 상품 이미지"
        
        return row
    
    def process_file(self, input_file, output_file):
        """파일 처리"""
        print(f"처리 시작: {input_file}")
        
        # 읽기
        with open(input_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            fieldnames = reader.fieldnames
        
        print(f"총 {len(rows)}개 상품 처리")
        
        # 처리
        processed = []
        for i, row in enumerate(rows, 1):
            try:
                print(f"  [{i}/{len(rows)}] 처리 중...")
            except:
                pass  # 인코딩 오류 무시
            processed.append(self.process_row(row))
        
        # 저장
        with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(processed)
        
        print(f"\n처리 완료: {output_file}")
        return output_file

def main():
    processor = QuickProcessor()
    
    # 명령줄 인수 처리
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        # input 폴더에서 CSV 파일 자동 탐색 (모듈 구조 반영)
        input_dir = "../../../data/input"
        csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
        
        if not csv_files:
            print(f"오류: {input_dir} 폴더에 CSV 파일이 없습니다!")
            return None
        
        input_file = os.path.join(input_dir, csv_files[0])
    
    # 출력 파일명 생성
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = f"../../../data/output/{base_name}_처리완료_{timestamp}.csv"
    
    # 파일 존재 확인
    if not os.path.exists(input_file):
        print(f"오류: 입력 파일이 없습니다: {input_file}")
        return None
    
    result = processor.process_file(input_file, output_file)
    
    print("\n" + "="*60)
    print("빠른 처리 완료!")
    print(f"결과 파일: {result}")
    print("="*60)
    
    return result

if __name__ == "__main__":
    main()
#!/usr/bin/env python
"""
CUA 대화형 상세페이지 이미지 생성 시스템
사용자와 대화를 통해 상품 정보를 수집하고 이미지 생성
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Optional

# 시스템 경로 추가
sys.path.append('C:/Users/8899y/CUA-MASTER')

from modules.nano_banana.detail_page_image_generator import DetailPageImageGenerator, NanoBananaImageEnhancer


class InteractiveImageCreator:
    """대화형 이미지 생성기"""
    
    def __init__(self):
        self.generator = DetailPageImageGenerator()
        self.enhancer = NanoBananaImageEnhancer()
        self.product_data = {}
        
    def collect_product_info(self) -> Dict:
        """대화형으로 상품 정보 수집"""
        
        print("\n=== CUA 상세페이지 이미지 생성 시스템 ===")
        print("상품 정보를 입력해주세요.\n")
        
        # 기본 정보
        self.product_data['name'] = input("상품명: ").strip() or "프리미엄 상품"
        
        # 브랜드 선택
        print("\n브랜드 선택:")
        print("1. 만원요리")
        print("2. 씨씨더블유")
        print("3. 인생")
        brand_choice = input("선택 (1-3): ").strip()
        
        brand_map = {'1': '만원요리', '2': '씨씨더블유', '3': '인생'}
        self.product_data['brand'] = brand_map.get(brand_choice, '만원요리')
        
        # 캐치프레이즈
        self.product_data['catchphrase'] = input("\n캐치프레이즈 (예: 특별한 맛의 경험): ").strip() or "특별한 맛의 경험"
        
        # 주요 특징 3가지
        print("\n주요 특징 3가지를 입력하세요:")
        features = []
        for i in range(3):
            feature = input(f"특징 {i+1}: ").strip()
            if feature:
                features.append(feature)
        
        self.product_data['features'] = features if features else ['프리미엄 재료', '간편 조리', '맛있는 한끼']
        
        # 조리 방법
        print("\n조리 단계를 입력하세요 (빈 줄 입력시 종료):")
        steps = []
        step_num = 1
        while True:
            step = input(f"단계 {step_num}: ").strip()
            if not step:
                break
            steps.append(f"{step_num}. {step}")
            step_num += 1
            
        self.product_data['cooking_steps'] = steps if steps else [
            "1. 포장을 개봉합니다",
            "2. 팬에 기름을 두릅니다",
            "3. 중불에서 5-7분 조리합니다",
            "4. 맛있게 즐깁니다"
        ]
        
        # 조리 정보
        self.product_data['cooking_time'] = input("\n조리 시간 (예: 10분): ").strip() or "10분"
        self.product_data['difficulty'] = input("난이도 (쉬움/보통/어려움): ").strip() or "쉬움"
        self.product_data['servings'] = input("분량 (예: 2인분): ").strip() or "2인분"
        
        # 영양 정보
        print("\n영양 정보 (선택사항, Enter로 스킵):")
        nutrition = {}
        
        nutrition_items = [
            ('열량', 'kcal'),
            ('탄수화물', 'g'),
            ('단백질', 'g'),
            ('지방', 'g'),
            ('나트륨', 'mg')
        ]
        
        for item, unit in nutrition_items:
            value = input(f"{item} ({unit}): ").strip()
            if value:
                nutrition[item] = f"{value}{unit}"
                
        if nutrition:
            self.product_data['nutrition'] = nutrition
        else:
            self.product_data['nutrition'] = {
                '열량': '250kcal',
                '탄수화물': '30g',
                '단백질': '15g',
                '지방': '10g',
                '나트륨': '500mg'
            }
            
        return self.product_data
        
    def confirm_data(self) -> bool:
        """입력 데이터 확인"""
        
        print("\n=== 입력하신 정보 확인 ===")
        print(f"상품명: {self.product_data['name']}")
        print(f"브랜드: {self.product_data['brand']}")
        print(f"캐치프레이즈: {self.product_data['catchphrase']}")
        print(f"특징: {', '.join(self.product_data['features'])}")
        print(f"조리시간: {self.product_data['cooking_time']}")
        print(f"난이도: {self.product_data['difficulty']}")
        print(f"분량: {self.product_data['servings']}")
        
        confirm = input("\n이대로 진행하시겠습니까? (y/n): ").strip().lower()
        return confirm == 'y'
        
    def select_style(self) -> str:
        """이미지 스타일 선택"""
        
        print("\n=== 이미지 스타일 선택 ===")
        print("1. 한국 전통 (한정식 스타일)")
        print("2. 모던 미니멀 (깔끔한 스타일)")
        print("3. 홈스타일 (집밥 느낌)")
        print("4. 프리미엄 (고급 레스토랑)")
        
        choice = input("스타일 선택 (1-4): ").strip()
        
        style_map = {
            '1': 'korean_traditional',
            '2': 'modern_minimal',
            '3': 'home_style',
            '4': 'premium'
        }
        
        return style_map.get(choice, 'korean_traditional')
        
    def generate_image(self) -> Optional[Path]:
        """이미지 생성"""
        
        try:
            # 상세페이지 생성
            print("\n이미지를 생성중입니다...")
            output_path = self.generator.generate_detail_page(self.product_data)
            
            print(f"\n✅ 상세페이지 생성 완료!")
            print(f"📁 저장 위치: {output_path}")
            
            # AI 프롬프트 생성
            style = self.select_style()
            prompt = self.enhancer.generate_prompt(
                self.product_data['name'], 
                style
            )
            
            print(f"\n💡 AI 이미지 프롬프트:")
            print(f"   {prompt}")
            
            # 추가 옵션
            print("\n=== 추가 작업 ===")
            print("1. 다른 스타일로 재생성")
            print("2. 새 상품 생성")
            print("3. 종료")
            
            choice = input("선택: ").strip()
            
            if choice == '1':
                return self.generate_image()
            elif choice == '2':
                self.product_data = {}
                return self.run()
            else:
                return output_path
                
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            return None
            
    def run(self) -> Optional[Path]:
        """메인 실행"""
        
        # 상품 정보 수집
        self.collect_product_info()
        
        # 확인
        if not self.confirm_data():
            print("취소되었습니다.")
            return None
            
        # 이미지 생성
        return self.generate_image()
        
    def batch_mode(self, csv_file: str):
        """CSV 파일로 일괄 처리"""
        
        import csv
        
        print(f"\n=== CSV 일괄 처리 모드 ===")
        print(f"파일: {csv_file}")
        
        generated = []
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    product = {
                        'name': row.get('상품명', '상품'),
                        'brand': row.get('브랜드', '만원요리'),
                        'catchphrase': row.get('캐치프레이즈', '특별한 맛'),
                        'features': row.get('특징', '').split(',')[:3],
                        'cooking_time': row.get('조리시간', '10분'),
                        'difficulty': row.get('난이도', '쉬움'),
                        'servings': row.get('분량', '2인분')
                    }
                    
                    print(f"\n처리중: {product['name']}")
                    output = self.generator.generate_detail_page(product)
                    generated.append(output)
                    
            print(f"\n✅ 총 {len(generated)}개 이미지 생성 완료")
            
            # 결과 저장
            result_file = Path(csv_file).stem + '_result.json'
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump([str(p) for p in generated], f, ensure_ascii=False, indent=2)
                
            print(f"📊 결과 파일: {result_file}")
            
        except Exception as e:
            print(f"❌ 오류: {e}")
            
        return generated


def main():
    """메인 실행 함수"""
    
    creator = InteractiveImageCreator()
    
    # 인자 확인
    if len(sys.argv) > 1:
        if sys.argv[1].endswith('.csv'):
            # CSV 일괄 처리
            creator.batch_mode(sys.argv[1])
        else:
            print("사용법: python interactive_image_creator.py [products.csv]")
    else:
        # 대화형 모드
        creator.run()


if __name__ == "__main__":
    main()
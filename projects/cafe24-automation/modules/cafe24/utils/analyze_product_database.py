# -*- coding: utf-8 -*-
"""
manwonyori CSV 데이터베이스 분석 및 CUA Agent 통합 시스템
"""
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

import pandas as pd
import json
import re
from pathlib import Path
from datetime import datetime

class ManwonyoriDataAnalyzer:
    """만원요리 상품 데이터 분석 클래스"""
    
    def __init__(self, csv_file_path):
        """초기화"""
        self.csv_file_path = csv_file_path
        self.df = None
        self.analysis_results = {}
        self.product_mapping = {}
        
        # 출력 디렉토리 생성
        self.output_dir = Path("product_database_analysis")
        self.output_dir.mkdir(exist_ok=True)
    
    def load_csv_data(self):
        """CSV 데이터 로드"""
        print("[DATA] CSV 데이터 로딩 중...")
        
        try:
            # UTF-8로 먼저 시도
            self.df = pd.read_csv(self.csv_file_path, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                # cp949로 시도
                self.df = pd.read_csv(self.csv_file_path, encoding='cp949')
            except UnicodeDecodeError:
                # utf-8-sig로 시도
                self.df = pd.read_csv(self.csv_file_path, encoding='utf-8-sig')
        
        print(f"[OK] 데이터 로딩 완료: {len(self.df)}개 상품")
        return True
    
    def analyze_basic_structure(self):
        """기본 데이터 구조 분석"""
        print("\n[ANALYSIS] 기본 데이터 구조 분석...")
        
        # 기본 정보
        total_products = len(self.df)
        total_columns = len(self.df.columns)
        
        print(f"   총 상품 수: {total_products:,}개")
        print(f"   총 컬럼 수: {total_columns}개")
        
        # 주요 컬럼 확인
        key_columns = ['상품코드', '상품번호', '상품명', '판매가', '공급가', '상품가']
        available_key_columns = [col for col in key_columns if col in self.df.columns]
        
        print(f"   주요 컬럼 보유: {len(available_key_columns)}/{len(key_columns)}개")
        print(f"   컬럼 목록: {available_key_columns}")
        
        # 결과 저장
        self.analysis_results['basic_info'] = {
            'total_products': total_products,
            'total_columns': total_columns,
            'key_columns': available_key_columns,
            'all_columns': list(self.df.columns)
        }
        
        return self.analysis_results['basic_info']
    
    def extract_product_mapping(self):
        """상품코드-상품번호 매핑 추출"""
        print("\n[TARGET] 상품코드-상품번호 매핑 추출...")
        
        # 상품코드와 상품번호 추출
        if '상품코드' in self.df.columns and '상품번호' in self.df.columns:
            mapping_data = self.df[['상품코드', '상품번호']].copy()
            
            # 결측값 제거
            mapping_data = mapping_data.dropna()
            
            # 딕셔너리로 변환
            product_mapping = {}
            code_to_number = {}
            number_to_code = {}
            
            for _, row in mapping_data.iterrows():
                product_code = str(row['상품코드']).strip()
                product_number = str(row['상품번호']).strip()
                
                if product_code and product_number:
                    code_to_number[product_code] = product_number
                    number_to_code[product_number] = product_code
            
            self.product_mapping = {
                'code_to_number': code_to_number,
                'number_to_code': number_to_code,
                'total_mappings': len(code_to_number)
            }
            
            print(f"   [OK] 매핑 완료: {len(code_to_number)}개 상품")
            
            # P00000NB 확인
            if 'P00000NB' in code_to_number:
                print(f"   [TARGET] P00000NB → 상품번호: {code_to_number['P00000NB']}")
            
            return self.product_mapping
        else:
            print("   [ERROR] 상품코드 또는 상품번호 컬럼을 찾을 수 없음")
            return None
    
    def analyze_product_categories(self):
        """상품 분류 분석"""
        print("\n[DATA] 상품 분류 분석...")
        
        category_analysis = {}
        
        # 상품코드 패턴 분석
        if '상품코드' in self.df.columns:
            product_codes = self.df['상품코드'].dropna().astype(str)
            
            # P로 시작하는 상품코드 분석
            p_codes = product_codes[product_codes.str.startswith('P')]
            print(f"   P로 시작하는 상품코드: {len(p_codes)}개")
            
            # 상품코드 패턴 분석 (P00000XX 형식)
            pattern_match = p_codes.str.match(r'P\d{5}[A-Z]{1,2}')
            valid_pattern_codes = p_codes[pattern_match]
            print(f"   P00000XX 패턴 매칭: {len(valid_pattern_codes)}개")
            
            # 상품코드 범위 분석
            if len(valid_pattern_codes) > 0:
                # 알파벳 부분 추출
                alpha_parts = valid_pattern_codes.str.extract(r'P\d{5}([A-Z]{1,2})')[0]
                unique_alpha = alpha_parts.value_counts()
                
                print(f"   알파벳 접미사 종류: {len(unique_alpha)}가지")
                print(f"   가장 많은 접미사: {unique_alpha.head(3).to_dict()}")
                
                category_analysis['product_code_patterns'] = {
                    'total_p_codes': len(p_codes),
                    'valid_pattern_codes': len(valid_pattern_codes),
                    'alpha_suffix_distribution': unique_alpha.head(10).to_dict()
                }
        
        # 브랜드 분석
        if '브랜드' in self.df.columns:
            brands = self.df['브랜드'].dropna()
            brand_counts = brands.value_counts()
            print(f"   브랜드 종류: {len(brand_counts)}개")
            print(f"   주요 브랜드: {brand_counts.head(3).to_dict()}")
            
            category_analysis['brands'] = brand_counts.head(10).to_dict()
        
        # 가격 분석
        price_columns = ['판매가', '상품가', '공급가']
        for price_col in price_columns:
            if price_col in self.df.columns:
                prices = pd.to_numeric(self.df[price_col], errors='coerce').dropna()
                if len(prices) > 0:
                    price_stats = {
                        'count': len(prices),
                        'min': int(prices.min()),
                        'max': int(prices.max()),
                        'mean': int(prices.mean()),
                        'median': int(prices.median())
                    }
                    print(f"   {price_col} 통계: 평균 {price_stats['mean']:,}원, 범위 {price_stats['min']:,}~{price_stats['max']:,}원")
                    category_analysis[f'{price_col}_stats'] = price_stats
        
        self.analysis_results['category_analysis'] = category_analysis
        return category_analysis
    
    def find_bulk_processing_targets(self):
        """대량 처리 대상 상품 식별"""
        print("\n[BULK] 대량 처리 대상 상품 식별...")
        
        if '상품번호' not in self.df.columns:
            print("   [ERROR] 상품번호 컬럼을 찾을 수 없음")
            return None
        
        # 상품번호를 숫자로 변환
        product_numbers = pd.to_numeric(self.df['상품번호'], errors='coerce').dropna()
        
        if len(product_numbers) == 0:
            print("   [ERROR] 유효한 상품번호를 찾을 수 없음")
            return None
        
        # 범위 분석
        min_number = int(product_numbers.min())
        max_number = int(product_numbers.max())
        total_numbers = len(product_numbers)
        
        print(f"   상품번호 범위: {min_number} ~ {max_number}")
        print(f"   총 상품 수: {total_numbers}개")
        
        # 연속된 구간 찾기
        sorted_numbers = sorted(product_numbers.astype(int))
        continuous_ranges = []
        
        start = sorted_numbers[0]
        current = start
        
        for num in sorted_numbers[1:]:
            if num != current + 1:
                # 구간 완료
                if current != start:
                    continuous_ranges.append((start, current, current - start + 1))
                start = num
            current = num
        
        # 마지막 구간 추가
        if current != start:
            continuous_ranges.append((start, current, current - start + 1))
        
        # 큰 연속 구간 찾기 (20개 이상)
        large_ranges = [r for r in continuous_ranges if r[2] >= 20]
        
        print(f"   20개 이상 연속 구간: {len(large_ranges)}개")
        for start, end, count in large_ranges[:5]:  # 상위 5개만 출력
            print(f"     {start}~{end}: {count}개")
        
        # P00000NB (339번) 주변 분석
        if 339 in sorted_numbers:
            nearby_start = max(min_number, 339 - 50)
            nearby_end = min(max_number, 339 + 50)
            nearby_numbers = [n for n in sorted_numbers if nearby_start <= n <= nearby_end]
            print(f"   P00000NB(339) 주변 {nearby_start}~{nearby_end}: {len(nearby_numbers)}개 상품")
        
        bulk_targets = {
            'total_products': total_numbers,
            'number_range': (min_number, max_number),
            'continuous_ranges': continuous_ranges[:10],  # 상위 10개
            'large_ranges': large_ranges,
            'recommended_batch_size': 50,
            'p00000nb_nearby': nearby_numbers if 339 in sorted_numbers else []
        }
        
        self.analysis_results['bulk_targets'] = bulk_targets
        return bulk_targets
    
    def create_cua_integration_config(self):
        """CUA Agent 통합을 위한 설정 생성"""
        print("\n[CONFIG] CUA Agent 통합 설정 생성...")
        
        # 상품 매핑 정보를 CUA용 설정으로 변환
        cua_config = {
            'product_database': {
                'source_file': str(self.csv_file_path),
                'total_products': len(self.df) if self.df is not None else 0,
                'last_updated': datetime.now().isoformat()
            },
            'automation_targets': {},
            'bulk_processing': {
                'batch_size': 50,
                'delay_between_requests': 2,
                'retry_attempts': 3
            }
        }
        
        # 상품 매핑 정보 추가
        if hasattr(self, 'product_mapping') and self.product_mapping:
            cua_config['product_mapping'] = self.product_mapping
        
        # 대량 처리 타겟 추가
        if 'bulk_targets' in self.analysis_results:
            cua_config['automation_targets']['bulk_ranges'] = self.analysis_results['bulk_targets']['large_ranges']
        
        # 주요 상품 정보 추가 (샘플링)
        if self.df is not None and len(self.df) > 0:
            # 상위 10개 상품 샘플
            sample_products = []
            for _, row in self.df.head(10).iterrows():
                product_info = {
                    'product_code': str(row.get('상품코드', '')),
                    'product_number': str(row.get('상품번호', '')),
                    'product_name': str(row.get('상품명', '')),
                    'price': str(row.get('판매가', ''))
                }
                sample_products.append(product_info)
            
            cua_config['sample_products'] = sample_products
        
        # 설정 저장
        config_file = self.output_dir / "cua_integration_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(cua_config, f, ensure_ascii=False, indent=2)
        
        print(f"   [OK] CUA 통합 설정 저장: {config_file}")
        return cua_config
    
    def save_analysis_results(self):
        """분석 결과 저장"""
        print("\n[SAVE] 분석 결과 저장...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. 전체 분석 결과 JSON
        analysis_file = self.output_dir / f"product_analysis_{timestamp}.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, ensure_ascii=False, indent=2)
        
        # 2. 상품 매핑 CSV (상품코드-상품번호만)
        if hasattr(self, 'product_mapping') and self.product_mapping:
            mapping_df = pd.DataFrame([
                {'상품코드': code, '상품번호': number}
                for code, number in self.product_mapping['code_to_number'].items()
            ])
            mapping_csv = self.output_dir / f"product_mapping_{timestamp}.csv"
            mapping_df.to_csv(mapping_csv, index=False, encoding='utf-8-sig')
            print(f"   [DATA] 상품 매핑 CSV: {mapping_csv}")
        
        # 3. 대량 처리용 상품번호 리스트
        if 'bulk_targets' in self.analysis_results:
            bulk_targets = self.analysis_results['bulk_targets']
            
            # 연속 구간별 파일 생성
            for i, (start, end, count) in enumerate(bulk_targets['large_ranges'][:5]):
                range_numbers = list(range(start, end + 1))
                range_df = pd.DataFrame({'상품번호': range_numbers})
                range_file = self.output_dir / f"bulk_range_{start}_{end}_{timestamp}.csv"
                range_df.to_csv(range_file, index=False, encoding='utf-8-sig')
                print(f"   [BULK] 대량처리 범위 #{i+1}: {range_file}")
        
        print(f"   [OK] 분석 결과 저장: {analysis_file}")
        
        return {
            'analysis_file': analysis_file,
            'output_directory': self.output_dir
        }
    
    def run_full_analysis(self):
        """전체 분석 실행"""
        print("[TARGET] 만원요리 상품 데이터베이스 전체 분석 시작")
        print("=" * 80)
        
        try:
            # 1. 데이터 로딩
            self.load_csv_data()
            
            # 2. 기본 구조 분석
            self.analyze_basic_structure()
            
            # 3. 상품 매핑 추출
            self.extract_product_mapping()
            
            # 4. 상품 분류 분석
            self.analyze_product_categories()
            
            # 5. 대량 처리 대상 식별
            self.find_bulk_processing_targets()
            
            # 6. CUA 통합 설정 생성
            self.create_cua_integration_config()
            
            # 7. 결과 저장
            saved_files = self.save_analysis_results()
            
            print("\n" + "=" * 80)
            print("[COMPLETE] 분석 완료!")
            print(f"[FOLDER] 출력 디렉토리: {self.output_dir}")
            print("=" * 80)
            
            return saved_files
            
        except Exception as e:
            print(f"\n[ERROR] 분석 중 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            return None

def main():
    """메인 실행 함수"""
    csv_file = "C:\\Users\\8899y\\CUA-MASTER\\manwonyori_20250831_288_0347.csv"
    
    analyzer = ManwonyoriDataAnalyzer(csv_file)
    results = analyzer.run_full_analysis()
    
    if results:
        print(f"\n[NEXT] 다음 단계:")
        print(f"1. 분석 결과 확인: {results['analysis_file']}")
        print(f"2. CUA Agent 설정: {results['output_directory']}/cua_integration_config.json")
        print(f"3. 대량 처리 실행: bulk_range_*.csv 파일들 활용")

if __name__ == "__main__":
    main()
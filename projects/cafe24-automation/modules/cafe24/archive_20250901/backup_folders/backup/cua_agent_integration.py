# -*- coding: utf-8 -*-
"""
CUA Agent 통합 시스템
만원요리 상품 데이터베이스와 Cafe24 자동화를 연동하는 통합 시스템
"""
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

import json
import time
import pandas as pd
from pathlib import Path
from datetime import datetime

# 기존 모듈 임포트
from bulk_product_processor import CafeBulkProcessor
from analyze_product_database import ManwonyoriDataAnalyzer

class CUAAgentIntegration:
    """CUA Agent 통합 클래스"""
    
    def __init__(self):
        """초기화"""
        self.config = self.load_cua_config()
        self.product_mapping = {}
        self.automation_results = []
        
        # 출력 디렉토리
        self.output_dir = Path("cua_integration_output")
        self.output_dir.mkdir(exist_ok=True)
        
        print("[CUA-INIT] CUA Agent 통합 시스템 초기화 완료")
    
    def load_cua_config(self):
        """CUA 통합 설정 로드"""
        config_file = Path("product_database_analysis/cua_integration_config.json")
        
        if not config_file.exists():
            print(f"[WARNING] CUA 설정 파일이 없습니다: {config_file}")
            return None
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print(f"[CONFIG] CUA 설정 로드 완료: {config['product_database']['total_products']}개 상품")
        return config
    
    def get_product_info_by_code(self, product_code):
        """상품코드로 상품 정보 조회"""
        if not self.config or 'product_mapping' not in self.config:
            return None
        
        code_to_number = self.config['product_mapping']['code_to_number']
        
        if product_code in code_to_number:
            product_number = code_to_number[product_code]
            
            # 샘플 상품에서 추가 정보 찾기
            for sample in self.config.get('sample_products', []):
                if sample['product_code'] == product_code:
                    return {
                        'product_code': product_code,
                        'product_number': product_number,
                        'product_name': sample['product_name'],
                        'price': sample['price']
                    }
            
            return {
                'product_code': product_code,
                'product_number': product_number,
                'product_name': 'Unknown',
                'price': 'Unknown'
            }
        
        return None
    
    def get_bulk_processing_recommendations(self):
        """대량 처리 권장 사항 분석"""
        if not self.config or 'automation_targets' not in self.config:
            return []
        
        bulk_ranges = self.config['automation_targets']['bulk_ranges']
        recommendations = []
        
        for i, (start, end, count) in enumerate(bulk_ranges):
            recommendation = {
                'range_id': f'range_{i+1}',
                'start_number': start,
                'end_number': end,
                'product_count': count,
                'estimated_time_minutes': count * 0.12,  # 7초/상품 기준
                'priority': 'high' if count > 50 else 'medium',
                'description': f"상품번호 {start}~{end} ({count}개 상품)"
            }
            recommendations.append(recommendation)
        
        return recommendations
    
    def execute_targeted_automation(self, target_range, max_products=20):
        """특정 범위 자동화 실행"""
        print(f"\n[AUTOMATION] 타겟 범위 자동화 실행: {target_range['description']}")
        
        # CafeBulkProcessor 인스턴스 생성
        processor = CafeBulkProcessor()
        
        try:
            # 자동화 실행
            result = processor.run_bulk_processing_test(
                start_product_no=target_range['start_number'],
                max_products=min(max_products, target_range['product_count'])
            )
            
            automation_result = {
                'range_id': target_range['range_id'],
                'execution_time': datetime.now().isoformat(),
                'target_range': target_range,
                'max_products': max_products,
                'success': True if result else False,
                'notes': f"Processing completed for range {target_range['start_number']}-{target_range['end_number']}"
            }
            
            self.automation_results.append(automation_result)
            return automation_result
            
        except Exception as e:
            error_result = {
                'range_id': target_range['range_id'],
                'execution_time': datetime.now().isoformat(),
                'target_range': target_range,
                'max_products': max_products,
                'success': False,
                'error': str(e)
            }
            
            self.automation_results.append(error_result)
            return error_result
    
    def generate_automation_plan(self):
        """자동화 실행 계획 생성"""
        print("\n[PLANNING] 자동화 실행 계획 생성...")
        
        recommendations = self.get_bulk_processing_recommendations()
        
        if not recommendations:
            print("   [WARNING] 대량 처리 권장사항이 없습니다")
            return None
        
        # 계획 생성
        plan = {
            'plan_id': f"automation_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'created_at': datetime.now().isoformat(),
            'total_ranges': len(recommendations),
            'estimated_total_products': sum(r['product_count'] for r in recommendations),
            'estimated_total_time_hours': sum(r['estimated_time_minutes'] for r in recommendations) / 60,
            'phases': []
        }
        
        # 단계별 계획
        for i, rec in enumerate(recommendations, 1):
            phase = {
                'phase_number': i,
                'range_info': rec,
                'recommended_batch_size': 25 if rec['product_count'] > 25 else rec['product_count'],
                'estimated_batches': (rec['product_count'] + 24) // 25,
                'priority': rec['priority']
            }
            plan['phases'].append(phase)
        
        # 계획 저장
        plan_file = self.output_dir / f"automation_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(plan_file, 'w', encoding='utf-8') as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)
        
        print(f"   [PLAN] 자동화 계획 생성 완료: {plan_file}")
        print(f"   총 {plan['total_ranges']}개 범위, {plan['estimated_total_products']}개 상품")
        print(f"   예상 소요시간: {plan['estimated_total_time_hours']:.1f}시간")
        
        return plan
    
    def create_product_dashboard_data(self):
        """상품 대시보드 데이터 생성"""
        print("\n[DASHBOARD] 상품 대시보드 데이터 생성...")
        
        if not self.config:
            return None
        
        # 대시보드 데이터 구조
        dashboard_data = {
            'summary': {
                'total_products': self.config['product_database']['total_products'],
                'last_updated': self.config['product_database']['last_updated'],
                'automation_ready': len(self.config['automation_targets']['bulk_ranges']),
                'p00000nb_status': 'identified' if 'P00000NB' in self.config['product_mapping']['code_to_number'] else 'not_found'
            },
            'product_ranges': [],
            'sample_products': self.config.get('sample_products', []),
            'automation_status': {
                'completed_ranges': len([r for r in self.automation_results if r['success']]),
                'failed_ranges': len([r for r in self.automation_results if not r['success']]),
                'total_executions': len(self.automation_results)
            }
        }
        
        # 상품 범위 정보
        for i, (start, end, count) in enumerate(self.config['automation_targets']['bulk_ranges']):
            range_info = {
                'range_id': f'range_{i+1}',
                'start': start,
                'end': end,
                'count': count,
                'status': 'pending',
                'coverage_percent': (count / dashboard_data['summary']['total_products']) * 100
            }
            dashboard_data['product_ranges'].append(range_info)
        
        # 대시보드 데이터 저장
        dashboard_file = self.output_dir / f"product_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            json.dump(dashboard_data, f, ensure_ascii=False, indent=2)
        
        print(f"   [DASHBOARD] 대시보드 데이터 저장: {dashboard_file}")
        return dashboard_data
    
    def run_comprehensive_analysis(self):
        """종합 분석 실행"""
        print("\n" + "="*80)
        print("[CUA-MASTER] 종합 CUA Agent 통합 분석 시작")
        print("="*80)
        
        analysis_results = {
            'execution_time': datetime.now().isoformat(),
            'config_status': 'loaded' if self.config else 'missing',
            'analysis_phases': []
        }
        
        try:
            # Phase 1: 설정 검증
            print("\n[PHASE 1] 설정 및 데이터 검증...")
            if self.config:
                print(f"   [OK] 총 {self.config['product_database']['total_products']}개 상품 데이터 로드됨")
                print(f"   [OK] {len(self.config['automation_targets']['bulk_ranges'])}개 자동화 범위 식별됨")
                
                # P00000NB 확인
                p00000nb_info = self.get_product_info_by_code('P00000NB')
                if p00000nb_info:
                    print(f"   [TARGET] P00000NB 상품 확인: {p00000nb_info['product_name']} ({p00000nb_info['product_number']}번)")
                
                analysis_results['analysis_phases'].append({
                    'phase': 'configuration_validation',
                    'status': 'success',
                    'details': 'All configuration data loaded successfully'
                })
            else:
                print("   [ERROR] 설정 파일을 찾을 수 없습니다")
                analysis_results['analysis_phases'].append({
                    'phase': 'configuration_validation',
                    'status': 'failed',
                    'details': 'Configuration file not found'
                })
                return analysis_results
            
            # Phase 2: 자동화 계획 생성
            print("\n[PHASE 2] 자동화 계획 생성...")
            automation_plan = self.generate_automation_plan()
            if automation_plan:
                analysis_results['automation_plan'] = automation_plan
                analysis_results['analysis_phases'].append({
                    'phase': 'automation_planning',
                    'status': 'success',
                    'details': f"Generated plan for {automation_plan['total_ranges']} ranges"
                })
            
            # Phase 3: 대시보드 데이터 생성
            print("\n[PHASE 3] 대시보드 데이터 생성...")
            dashboard_data = self.create_product_dashboard_data()
            if dashboard_data:
                analysis_results['dashboard_data'] = dashboard_data
                analysis_results['analysis_phases'].append({
                    'phase': 'dashboard_creation',
                    'status': 'success',
                    'details': 'Dashboard data created successfully'
                })
            
            # Phase 4: 권장사항 생성
            print("\n[PHASE 4] CUA Agent 활용 권장사항 생성...")
            recommendations = self.generate_cua_recommendations()
            if recommendations:
                analysis_results['recommendations'] = recommendations
                analysis_results['analysis_phases'].append({
                    'phase': 'recommendations',
                    'status': 'success',
                    'details': f"Generated {len(recommendations)} recommendations"
                })
            
            # 결과 저장
            results_file = self.output_dir / f"cua_comprehensive_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(analysis_results, f, ensure_ascii=False, indent=2)
            
            print(f"\n[SAVE] 종합 분석 결과 저장: {results_file}")
            
            return analysis_results
            
        except Exception as e:
            print(f"\n[ERROR] 분석 중 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            return analysis_results
    
    def generate_cua_recommendations(self):
        """CUA Agent 활용 권장사항 생성"""
        recommendations = [
            {
                'category': '단계적 자동화 실행',
                'priority': 'high',
                'description': '131~253번 상품 범위 (123개)를 우선 처리하여 시스템 안정성 검증',
                'action_items': [
                    '25개씩 배치 처리로 시작',
                    '각 배치 후 2초 대기로 서버 부하 방지',
                    '오류 발생 시 자동 재시도 (최대 3회)',
                    '처리 결과를 CSV/JSON으로 저장'
                ]
            },
            {
                'category': '데이터 품질 관리',
                'priority': 'medium',
                'description': '상품 데이터 일관성 검증 및 누락 데이터 보완',
                'action_items': [
                    '가격 데이터 0원 상품 식별 및 검토',
                    '상품명 길이 및 특수문자 검증',
                    '이미지 URL 유효성 검사',
                    'SEO 키워드 최적화 상태 점검'
                ]
            },
            {
                'category': 'CUA Agent 확장',
                'priority': 'medium',
                'description': 'Cafe24 자동화를 다른 업무와 연동',
                'action_items': [
                    '주문 처리 자동화와 연결',
                    '재고 관리 시스템 통합',
                    '고객 문의 자동 응답 시스템',
                    '매출 분석 및 리포팅 자동화'
                ]
            },
            {
                'category': '모니터링 및 알림',
                'priority': 'low',
                'description': '자동화 프로세스 모니터링 체계 구축',
                'action_items': [
                    '처리 진행률 실시간 모니터링',
                    '오류 발생 시 이메일 알림',
                    '일일/주간 처리 결과 보고서',
                    '시스템 성능 지표 추적'
                ]
            }
        ]
        
        return recommendations

def main():
    """메인 실행 함수"""
    print("CUA Agent 통합 시스템 시작")
    
    # 통합 시스템 초기화
    cua_system = CUAAgentIntegration()
    
    # 종합 분석 실행
    results = cua_system.run_comprehensive_analysis()
    
    if results:
        print("\n" + "="*80)
        print("[CUA-SUCCESS] 종합 분석 완료!")
        print(f"실행된 분석 단계: {len(results['analysis_phases'])}개")
        print(f"결과 저장 위치: {cua_system.output_dir}")
        
        # 다음 단계 안내
        if 'automation_plan' in results:
            plan = results['automation_plan']
            print(f"\n[NEXT-STEPS] 다음 실행 권장사항:")
            print(f"1. 우선 처리 범위: Phase 1 ({plan['phases'][0]['range_info']['description']})")
            print(f"2. 배치 크기: {plan['phases'][0]['recommended_batch_size']}개씩")
            print(f"3. 예상 소요시간: {plan['estimated_total_time_hours']:.1f}시간")
        
        print("="*80)

if __name__ == "__main__":
    main()
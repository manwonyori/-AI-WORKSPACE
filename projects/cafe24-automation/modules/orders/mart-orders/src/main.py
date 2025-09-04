"""
Mart Supply Manager 메인 시스템
"""

import sys
import logging
from pathlib import Path

# 프로젝트 루트 디렉토리 추가
sys.path.append(str(Path(__file__).parent.parent))

from src.supplier_manager import SupplierManager
from src.inventory_tracker import InventoryTracker
from src.document_generator import DocumentGenerator
from src.data_analyzer import DataAnalyzer

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mart_system.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class MartSupplySystem:
    """통합 공급망 관리 시스템"""
    
    def __init__(self):
        logger.info("Mart Supply System 초기화 중...")
        
        # 각 모듈 초기화
        self.supplier_manager = SupplierManager()
        self.inventory_tracker = InventoryTracker()
        self.document_generator = DocumentGenerator()
        self.data_analyzer = DataAnalyzer()
        
        logger.info("시스템 초기화 완료")
    
    def run(self):
        """메인 실행 함수"""
        print("\n" + "="*50)
        print(" Mart Supply Manager 시스템")
        print("="*50)
        
        while True:
            print("\n메뉴를 선택하세요:")
            print("1. 공급업체 관리")
            print("2. 재고 관리")
            print("3. 문서 생성")
            print("4. 데이터 분석")
            print("5. 시스템 상태 확인")
            print("0. 종료")
            
            choice = input("\n선택: ").strip()
            
            if choice == "1":
                self.manage_suppliers()
            elif choice == "2":
                self.manage_inventory()
            elif choice == "3":
                self.generate_documents()
            elif choice == "4":
                self.analyze_data()
            elif choice == "5":
                self.check_status()
            elif choice == "0":
                print("\n시스템을 종료합니다.")
                break
            else:
                print("\n잘못된 선택입니다. 다시 선택해주세요.")
    
    def manage_suppliers(self):
        """공급업체 관리"""
        print("\n[공급업체 관리]")
        print("1. 신규 공급업체 등록")
        print("2. 공급업체 목록 조회")
        print("3. 공급업체 정보 수정")
        print("4. 사업자등록증 스캔")
        
        sub_choice = input("선택: ").strip()
        
        if sub_choice == "1":
            self.supplier_manager.register_new_supplier()
        elif sub_choice == "2":
            self.supplier_manager.list_suppliers()
        elif sub_choice == "3":
            self.supplier_manager.update_supplier()
        elif sub_choice == "4":
            self.supplier_manager.scan_business_license()
    
    def manage_inventory(self):
        """재고 관리"""
        print("\n[재고 관리]")
        print("1. 현재 재고 조회")
        print("2. 재고 입고 등록")
        print("3. 재고 출고 등록")
        print("4. 자동 발주 설정")
        
        sub_choice = input("선택: ").strip()
        
        if sub_choice == "1":
            self.inventory_tracker.show_current_inventory()
        elif sub_choice == "2":
            self.inventory_tracker.register_incoming()
        elif sub_choice == "3":
            self.inventory_tracker.register_outgoing()
        elif sub_choice == "4":
            self.inventory_tracker.setup_auto_order()
    
    def generate_documents(self):
        """문서 생성"""
        print("\n[문서 생성]")
        print("1. 발주서 생성")
        print("2. 거래명세서 생성")
        print("3. 월간 보고서 생성")
        
        sub_choice = input("선택: ").strip()
        
        if sub_choice == "1":
            self.document_generator.create_purchase_order()
        elif sub_choice == "2":
            self.document_generator.create_transaction_statement()
        elif sub_choice == "3":
            self.document_generator.create_monthly_report()
    
    def analyze_data(self):
        """데이터 분석"""
        print("\n[데이터 분석]")
        print("1. 공급 패턴 분석")
        print("2. 가격 동향 분석")
        print("3. 품질 지표 분석")
        
        sub_choice = input("선택: ").strip()
        
        if sub_choice == "1":
            self.data_analyzer.analyze_supply_patterns()
        elif sub_choice == "2":
            self.data_analyzer.analyze_price_trends()
        elif sub_choice == "3":
            self.data_analyzer.analyze_quality_metrics()
    
    def check_status(self):
        """시스템 상태 확인"""
        print("\n[시스템 상태]")
        print(f"공급업체 수: {self.supplier_manager.get_supplier_count()}")
        print(f"재고 품목 수: {self.inventory_tracker.get_item_count()}")
        print(f"이번 달 거래 건수: {self.document_generator.get_monthly_transactions()}")
        print(f"시스템 상태: 정상")


def main():
    """메인 함수"""
    try:
        system = MartSupplySystem()
        system.run()
    except KeyboardInterrupt:
        print("\n\n프로그램이 중단되었습니다.")
    except Exception as e:
        logger.error(f"시스템 오류 발생: {str(e)}")
        print(f"\n오류가 발생했습니다: {str(e)}")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from pathlib import Path
import logging
import pandas as pd

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
값진한끼 발주/공급 엑셀 생성 시스템
1. 웰빙신선식품에 발주서 (매입)
2. CCW에 공급확인서 (판매)
"""

class ExcelOrderGenerator:
    """엑셀 발주서 생성기"""
    
    def __init__(self):
        self.company_info = {
            "company_name": "주식회사 값진한끼",
            "business_number": "123-45-67890",  # 실제 사업자번호로 변경 필요
            "address": "경기도 시흥시",  # 실제 주소로 변경 필요
            "contact": "010-XXXX-XXXX"  # 실제 연락처로 변경 필요
        }
        
        self.wellbeing_info = {
            "company_name": "주식회사 웰빙신선식품",
            "business_number": "813-81-02169",
            "contact_name": "윤철",
            "contact_position": "대리",
            "contact_phone": "010-7727-8009",
            "address": "경기 시흥시 장현능곡로 155 시흥 플랑드르 지하 1층"
        }
        
        self.ccw_info = {
            "company_name": "CCW",
            "address": "CCW 주소",
            "contact": "CCW 담당자"
        }
    
    def create_wellbeing_purchase_order(self, items):
        """웰빙신선식품에 보낼 발주서 생성 (매입)"""
        
        # 발주번호 생성
        order_number = f"PO-WB-{datetime.now().strftime('%Y%m%d-%H%M')}"
        order_date = datetime.now().strftime("%Y-%m-%d")
        
        # 데이터 준비
        order_data = []
        for i, item in enumerate(items, 1):
            order_data.append({
                '번호': i,
                '상품명': item['product_name'],
                '수량': item['quantity'],
                '단위': '개',
                '단가': item['purchase_price'],  # 매입 단가
                '금액': item['quantity'] * item['purchase_price']
            })
        
        # DataFrame 생성
        df_items = pd.DataFrame(order_data)
        
        # 합계 계산
        subtotal = df_items['금액'].sum()
        vat = subtotal * 0.1
        total = subtotal + vat
        
        # 엑셀 파일 생성
        output_dir = Path("docs/excel_orders")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = output_dir / f"웰빙_발주서_{order_number}.xlsx"
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # 시트1: 발주서
            # 헤더 정보
            header_data = pd.DataFrame([
                ['발주서'],
                [''],
                [f'발주번호: {order_number}', '', '', f'발주일자: {order_date}'],
                [''],
                ['수신: 주식회사 웰빙신선식품'],
                [f'담당: {self.wellbeing_info["contact_name"]} {self.wellbeing_info["contact_position"]}'],
                [f'연락처: {self.wellbeing_info["contact_phone"]}'],
                [''],
                ['발신: 주식회사 값진한끼'],
                ['']
            ])
            
            # 헤더 쓰기
            header_data.to_excel(writer, sheet_name='발주서', index=False, header=False)
            
            # 품목 데이터 쓰기
            df_items.to_excel(writer, sheet_name='발주서', index=False, startrow=10)
            
            # 합계 정보
            summary_data = pd.DataFrame([
                [''],
                ['', '', '', '', '공급가액:', subtotal],
                ['', '', '', '', '부가세:', vat],
                ['', '', '', '', '합계:', total],
                [''],
                ['결제조건: 월말정산'],
                ['납기일: 발주 후 3일 이내'],
                ['배송지: ' + self.wellbeing_info['address']]
            ])
            
            summary_data.to_excel(writer, sheet_name='발주서', 
                                 index=False, header=False, 
                                 startrow=10 + len(df_items) + 2)
            
            # 워크시트 포맷팅
            worksheet = writer.sheets['발주서']
            worksheet.column_dimensions['A'].width = 10
            worksheet.column_dimensions['B'].width = 30
            worksheet.column_dimensions['C'].width = 10
            worksheet.column_dimensions['D'].width = 10
            worksheet.column_dimensions['E'].width = 15
            worksheet.column_dimensions['F'].width = 15
        
        print(f"웰빙 발주서 생성: {filename}")
        return filename
    
    def create_ccw_supply_statement(self, items):
        """CCW에 보낼 공급 확인서/거래명세서 생성 (판매)"""
        
        # 문서번호 생성
        doc_number = f"SUP-CCW-{datetime.now().strftime('%Y%m%d-%H%M')}"
        doc_date = datetime.now().strftime("%Y-%m-%d")
        
        # 데이터 준비
        supply_data = []
        for i, item in enumerate(items, 1):
            supply_data.append({
                '번호': i,
                '상품명': item['product_name'],
                '수량': item['quantity'],
                '단위': '개',
                '단가': item['sale_price'],  # 판매 단가
                '금액': item['quantity'] * item['sale_price']
            })
        
        # DataFrame 생성
        df_items = pd.DataFrame(supply_data)
        
        # 합계 계산
        subtotal = df_items['금액'].sum()
        vat = subtotal * 0.1
        total = subtotal + vat
        
        # 엑셀 파일 생성
        output_dir = Path("docs/excel_orders")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = output_dir / f"CCW_거래명세서_{doc_number}.xlsx"
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # 시트1: 거래명세서
            # 헤더 정보
            header_data = pd.DataFrame([
                ['거래명세서'],
                [''],
                [f'문서번호: {doc_number}', '', '', f'거래일자: {doc_date}'],
                [''],
                ['수신: CCW'],
                [''],
                ['발신: 주식회사 값진한끼'],
                [f'사업자번호: {self.company_info["business_number"]}'],
                ['']
            ])
            
            # 헤더 쓰기
            header_data.to_excel(writer, sheet_name='거래명세서', index=False, header=False)
            
            # 품목 데이터 쓰기
            df_items.to_excel(writer, sheet_name='거래명세서', index=False, startrow=9)
            
            # 합계 정보
            summary_data = pd.DataFrame([
                [''],
                ['', '', '', '', '공급가액:', subtotal],
                ['', '', '', '', '부가세:', vat],
                ['', '', '', '', '합계:', total],
                [''],
                ['결제조건: 월말정산'],
                ['비고: 상기 물품을 정히 납품함']
            ])
            
            summary_data.to_excel(writer, sheet_name='거래명세서', 
                                 index=False, header=False, 
                                 startrow=9 + len(df_items) + 2)
            
            # 워크시트 포맷팅
            worksheet = writer.sheets['거래명세서']
            worksheet.column_dimensions['A'].width = 10
            worksheet.column_dimensions['B'].width = 30
            worksheet.column_dimensions['C'].width = 10
            worksheet.column_dimensions['D'].width = 10
            worksheet.column_dimensions['E'].width = 15
            worksheet.column_dimensions['F'].width = 15
        
        print(f"CCW 거래명세서 생성: {filename}")
        return filename
    
    def process_ccw_order(self):
        """CCW 발주 처리 - 양방향 문서 생성"""
        
        # CCW 발주 품목 (실제 데이터)
        items = [
            {
                'product_name': '이태원 햄폭탄 부대찌개',
                'quantity': 3,
                'purchase_price': 8500,  # 웰빙에서 매입하는 가격
                'sale_price': 10200       # CCW에 판매하는 가격 (CCW 엑셀 S열)
            },
            {
                'product_name': '힘찬 장어탕 500g',
                'quantity': 15,
                'purchase_price': 3600,   # 웰빙에서 매입하는 가격
                'sale_price': 6100        # CCW에 판매하는 가격 (CCW 엑셀 S열)
            }
        ]
        
        print("\n" + "="*60)
        print(" 값진한끼 발주/공급 문서 생성")
        print("="*60)
        
        # 1. 웰빙 발주서 생성 (매입)
        print("\n[1] 웰빙신선식품 발주서 생성 중...")
        wellbeing_file = self.create_wellbeing_purchase_order(items)
        
        # 매입 합계
        purchase_total = sum(item['quantity'] * item['purchase_price'] for item in items)
        purchase_vat = purchase_total * 0.1
        print(f"  매입 금액: {purchase_total:,}원 (VAT 별도)")
        print(f"  매입 총액: {purchase_total + purchase_vat:,}원 (VAT 포함)")
        
        # 2. CCW 거래명세서 생성 (판매)
        print("\n[2] CCW 거래명세서 생성 중...")
        ccw_file = self.create_ccw_supply_statement(items)
        
        # 판매 합계
        sale_total = sum(item['quantity'] * item['sale_price'] for item in items)
        sale_vat = sale_total * 0.1
        print(f"  판매 금액: {sale_total:,}원 (VAT 별도)")
        print(f"  판매 총액: {sale_total + sale_vat:,}원 (VAT 포함)")
        
        # 마진 계산
        margin = sale_total - purchase_total
        margin_rate = (margin / purchase_total) * 100 if purchase_total > 0 else 0
        
        print("\n" + "="*60)
        print(" 거래 요약")
        print("="*60)
        print(f"매입액: {purchase_total:,}원")
        print(f"판매액: {sale_total:,}원")
        print(f"마진: {margin:,}원 ({margin_rate:.1f}%)")
        
        return {
            'wellbeing_file': wellbeing_file,
            'ccw_file': ccw_file,
            'purchase_total': purchase_total + purchase_vat,
            'sale_total': sale_total + sale_vat,
            'margin': margin
        }

if __name__ == "__main__":
    generator = ExcelOrderGenerator()
    result = generator.process_ccw_order()
    
    print("\n문서 생성 완료!")
    print(f"1. 웰빙 발주서: {result['wellbeing_file']}")
    print(f"2. CCW 거래명세서: {result['ccw_file']}")
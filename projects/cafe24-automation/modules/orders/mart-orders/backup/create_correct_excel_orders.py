#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from pathlib import Path
import logging
import numpy as np
import pandas as pd

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
값진한끼 발주/공급 엑셀 생성 시스템 (수정본)
- CCW V열 금액계 사용
- 웰빙 직배송 정보 포함
"""

class CorrectExcelOrderGenerator:
    """수정된 엑셀 발주서 생성기"""
    
    def __init__(self):
        self.company_info = {
            "company_name": "주식회사 값진한끼",
            "business_number": "123-45-67890",  # 실제 사업자번호로 변경 필요
            "address": "경기도 시흥시",  # 실제 주소로 변경 필요
            "contact": "담당자",
            "phone": "010-XXXX-XXXX"  # 실제 연락처로 변경 필요
        }
        
        self.wellbeing_info = {
            "company_name": "주식회사 웰빙신선식품",
            "business_number": "813-81-02169",
            "contact_name": "윤철",
            "contact_position": "대리",
            "contact_phone": "010-7727-8009",
            "address": "경기 시흥시 장현능곡로 155 시흥 플랑드르 지하 1층 웰빙 푸드마켓"
        }
        
        # CCW 엑셀에서 확인한 정확한 데이터
        self.items = [
            {
                'product_name': '이태원 햄폭탄 부대찌개',
                'quantity': 3,
                'ccw_total_amount': 244800,  # V열 금액계
                'ccw_unit_price': 81600,     # 244800 / 3 = 81600
                'wellbeing_purchase_price': 81600,  # Q열 매입가(총액)
                'wellbeing_unit_price': 27200  # 81600 / 3 = 27200
            },
            {
                'product_name': '힘찬 장어탕 500g',
                'quantity': 15,
                'ccw_total_amount': 183000,  # V열 금액계
                'ccw_unit_price': 12200,     # 183000 / 15 = 12200
                'wellbeing_purchase_price': 12200,  # Q열 매입가(총액)
                'wellbeing_unit_price': 813.33  # 12200 / 15 = 813.33
            }
        ]
    
    def create_wellbeing_purchase_order(self):
        """웰빙신선식품에 보낼 발주서 (값진한끼가 웰빙에서 매입)"""
        
        order_number = f"PO-WB-{datetime.now().strftime('%Y%m%d-%H%M')}"
        order_date = datetime.now().strftime("%Y년 %m월 %d일")
        delivery_date = (datetime.now() + timedelta(days=2)).strftime("%Y년 %m월 %d일")
        
        # 데이터 준비
        order_data = []
        for i, item in enumerate(self.items, 1):
            order_data.append({
                '번호': i,
                '상품명': item['product_name'],
                '수량': item['quantity'],
                '단위': '개',
                '단가': item['wellbeing_unit_price'],
                '공급가액': item['wellbeing_purchase_price']
            })
        
        df_items = pd.DataFrame(order_data)
        
        # 합계
        subtotal = df_items['공급가액'].sum()
        vat = subtotal * 0.1
        total = subtotal + vat
        
        # 엑셀 생성
        output_dir = Path("docs/excel_orders")
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = output_dir / f"웰빙_발주서_{order_number}.xlsx"
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # 발주서 헤더
            header_data = [
                ['발 주 서'],
                [''],
                [f'발주번호: {order_number}', '', '', '', f'발주일: {order_date}'],
                [''],
                ['[ 수신 ]'],
                [f'업체명: {self.wellbeing_info["company_name"]}'],
                [f'담당자: {self.wellbeing_info["contact_name"]} {self.wellbeing_info["contact_position"]} ({self.wellbeing_info["contact_phone"]})'],
                [f'주소: {self.wellbeing_info["address"]}'],
                [''],
                ['[ 발신 ]'],
                [f'업체명: {self.company_info["company_name"]}'],
                [f'담당자: {self.company_info["contact"]} ({self.company_info["phone"]})'],
                [''],
                ['']
            ]
            
            # 헤더 DataFrame으로 변환하여 쓰기
            for idx, row in enumerate(header_data):
                pd.DataFrame([row]).to_excel(writer, sheet_name='발주서', 
                                            startrow=idx, index=False, header=False)
            
            # 품목 데이터
            df_items.to_excel(writer, sheet_name='발주서', startrow=15, index=False)
            
            # 합계 정보
            summary_start_row = 15 + len(df_items) + 2
            summary_data = [
                ['', '', '', '', '공급가액:', f'{subtotal:,.0f}'],
                ['', '', '', '', '부가세(10%):', f'{vat:,.0f}'],
                ['', '', '', '', '합계금액:', f'{total:,.0f}'],
                [''],
                [f'납기일: {delivery_date}'],
                ['결제조건: 월말정산'],
                ['비고: 납품 전 연락 요망']
            ]
            
            for idx, row in enumerate(summary_data):
                pd.DataFrame([row]).to_excel(writer, sheet_name='발주서', 
                                            startrow=summary_start_row + idx, 
                                            index=False, header=False)
            
            # 서식 조정
            worksheet = writer.sheets['발주서']
            worksheet.column_dimensions['A'].width = 10
            worksheet.column_dimensions['B'].width = 35
            worksheet.column_dimensions['C'].width = 10
            worksheet.column_dimensions['D'].width = 10
            worksheet.column_dimensions['E'].width = 15
            worksheet.column_dimensions['F'].width = 15
        
        print(f"웰빙 발주서 생성: {filename}")
        print(f"  매입액(공급가): {subtotal:,.0f}원")
        print(f"  VAT: {vat:,.0f}원")
        print(f"  총액: {total:,.0f}원")
        
        return filename, total
    
    def create_ccw_supply_statement(self):
        """CCW에 보낼 거래명세서 (값진한끼가 CCW에 판매)"""
        
        doc_number = f"SUP-CCW-{datetime.now().strftime('%Y%m%d-%H%M')}"
        doc_date = datetime.now().strftime("%Y년 %m월 %d일")
        delivery_date = (datetime.now() + timedelta(days=2)).strftime("%Y년 %m월 %d일")
        
        # 데이터 준비
        supply_data = []
        for i, item in enumerate(self.items, 1):
            supply_data.append({
                '번호': i,
                '상품명': item['product_name'],
                '수량': item['quantity'],
                '단위': '개',
                '단가': item['ccw_unit_price'],
                '공급가액': item['ccw_total_amount']
            })
        
        df_items = pd.DataFrame(supply_data)
        
        # 합계
        subtotal = df_items['공급가액'].sum()
        vat = subtotal * 0.1
        total = subtotal + vat
        
        # 엑셀 생성
        output_dir = Path("docs/excel_orders")
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = output_dir / f"CCW_거래명세서_{doc_number}.xlsx"
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # 거래명세서 헤더
            header_data = [
                ['거 래 명 세 서'],
                [''],
                [f'문서번호: {doc_number}', '', '', '', f'거래일: {doc_date}'],
                [''],
                ['[ 공급받는자 ]'],
                ['업체명: CCW'],
                [''],
                ['[ 공급자 ]'],
                [f'업체명: {self.company_info["company_name"]}'],
                [f'사업자번호: {self.company_info["business_number"]}'],
                [f'담당자: {self.company_info["contact"]} ({self.company_info["phone"]})'],
                [''],
                ['★ 배송 정보 ★'],
                [f'배송지: {self.wellbeing_info["address"]}'],
                [f'수령인: {self.wellbeing_info["contact_name"]} {self.wellbeing_info["contact_position"]} ({self.wellbeing_info["contact_phone"]})'],
                ['배송방법: 웰빙푸드마켓으로 직접 배송'],
                [f'배송요청일: {delivery_date}'],
                [''],
                ['']
            ]
            
            # 헤더 쓰기
            for idx, row in enumerate(header_data):
                pd.DataFrame([row]).to_excel(writer, sheet_name='거래명세서', 
                                            startrow=idx, index=False, header=False)
            
            # 품목 데이터
            df_items.to_excel(writer, sheet_name='거래명세서', startrow=19, index=False)
            
            # 합계 정보
            summary_start_row = 19 + len(df_items) + 2
            summary_data = [
                ['', '', '', '', '공급가액:', f'{subtotal:,.0f}'],
                ['', '', '', '', '부가세(10%):', f'{vat:,.0f}'],
                ['', '', '', '', '합계금액:', f'{total:,.0f}'],
                [''],
                ['결제조건: 월말정산'],
                [''],
                ['※ 중요 안내사항 ※'],
                ['1. 상기 물품은 웰빙푸드마켓(시흥 플랑드르 지하 1층)으로 직접 배송됩니다.'],
                ['2. 배송 전 반드시 수령인에게 연락 부탁드립니다.'],
                ['3. 배송 완료 후 인수증을 받아주시기 바랍니다.']
            ]
            
            for idx, row in enumerate(summary_data):
                pd.DataFrame([row]).to_excel(writer, sheet_name='거래명세서', 
                                            startrow=summary_start_row + idx, 
                                            index=False, header=False)
            
            # 서식 조정
            worksheet = writer.sheets['거래명세서']
            worksheet.column_dimensions['A'].width = 10
            worksheet.column_dimensions['B'].width = 35
            worksheet.column_dimensions['C'].width = 10
            worksheet.column_dimensions['D'].width = 10
            worksheet.column_dimensions['E'].width = 15
            worksheet.column_dimensions['F'].width = 15
        
        print(f"CCW 거래명세서 생성: {filename}")
        print(f"  판매액(공급가): {subtotal:,.0f}원")
        print(f"  VAT: {vat:,.0f}원")
        print(f"  총액: {total:,.0f}원")
        
        return filename, total
    
    def process_orders(self):
        """전체 프로세스 실행"""
        
        print("\n" + "="*60)
        print(" 값진한끼 발주/공급 문서 생성 (수정본)")
        print("="*60)
        
        print("\n[CCW 엑셀 데이터 기준]")
        print("-" * 40)
        total_from_ccw = sum(item['ccw_total_amount'] for item in self.items)
        total_to_wellbeing = sum(item['wellbeing_purchase_price'] for item in self.items)
        
        print(f"CCW V열 금액계 총합: {total_from_ccw:,.0f}원")
        print(f"웰빙 Q열 매입가 총합: {total_to_wellbeing:,.0f}원")
        
        # 1. 웰빙 발주서
        print("\n[1] 웰빙신선식품 발주서 생성...")
        wb_file, wb_total = self.create_wellbeing_purchase_order()
        
        # 2. CCW 거래명세서
        print("\n[2] CCW 거래명세서 생성...")
        ccw_file, ccw_total = self.create_ccw_supply_statement()
        
        # 요약
        print("\n" + "="*60)
        print(" 거래 요약")
        print("="*60)
        
        print("\n수익 구조:")
        print(f"  CCW에서 받는 금액: {total_from_ccw:,.0f}원 (VAT 별도)")
        print(f"  웰빙에 지불할 금액: {total_to_wellbeing:,.0f}원 (VAT 별도)")
        print(f"  마진: {total_from_ccw - total_to_wellbeing:,.0f}원")
        print(f"  마진율: 0% (금액이 동일)")
        
        print("\n배송 정보:")
        print(f"  배송지: {self.wellbeing_info['address']}")
        print(f"  수령인: {self.wellbeing_info['contact_name']} {self.wellbeing_info['contact_position']}")
        print(f"  연락처: {self.wellbeing_info['contact_phone']}")
        
        return {
            'wellbeing_file': wb_file,
            'ccw_file': ccw_file,
            'wellbeing_total': wb_total,
            'ccw_total': ccw_total
        }

if __name__ == "__main__":
    generator = CorrectExcelOrderGenerator()
    result = generator.process_orders()
    
    print("\n문서 생성 완료!")
    print(f"1. 웰빙 발주서: {result['wellbeing_file']}")
    print(f"2. CCW 거래명세서: {result['ccw_file']}")
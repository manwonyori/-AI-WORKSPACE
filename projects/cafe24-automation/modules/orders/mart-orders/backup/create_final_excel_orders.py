#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from pathlib import Path
import logging
import pandas as pd

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
값진한끼 발주/공급 엑셀 최종본
1. 값진한끼 → CCW: 발주서 (웰빙 직배송 명시)
2. 값진한끼 → 웰빙: 공급 요청서
"""

class FinalExcelOrderGenerator:
    """최종 엑셀 발주서 생성기"""
    
    def __init__(self):
        self.company_info = {
            "company_name": "주식회사 값진한끼",
            "business_number": "123-45-67890",  
            "address": "경기도 시흥시",  
            "contact": "담당자",
            "phone": "010-XXXX-XXXX"
        }
        
        self.wellbeing_info = {
            "company_name": "주식회사 웰빙신선식품",
            "business_number": "813-81-02169",
            "contact_name": "윤철",
            "contact_position": "대리",
            "contact_phone": "010-7727-8009",
            "address": "경기 시흥시 장현능곡로 155 시흥 플랑드르 지하 1층 웰빙 푸드마켓"
        }
        
        # CCW 엑셀 데이터 재확인
        # V열(금액계) = 출고수량 × 출고단가
        self.items = [
            {
                'product_name': '이태원 햄폭탄 부대찌개',
                'quantity': 3,  # U열
                'ccw_unit_price': 81600,  # 244800 / 3 = 81600 (출고단가)
                'ccw_total': 244800,  # V열 (출고금액)
            },
            {
                'product_name': '힘찬 장어탕 500g',
                'quantity': 15,  # U열
                'ccw_unit_price': 12200,  # 183000 / 15 = 12200 (출고단가)
                'ccw_total': 183000,  # V열 (출고금액)
            }
        ]
    
    def create_ccw_purchase_order(self):
        """값진한끼 → CCW 발주서 (웰빙 직배송 요청)"""
        
        order_number = f"PO-CCW-{datetime.now().strftime('%Y%m%d-%H%M')}"
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
                '단가': item['ccw_unit_price'],
                '금액': item['ccw_total']
            })
        
        df_items = pd.DataFrame(order_data)
        
        # 합계
        subtotal = df_items['금액'].sum()
        vat = subtotal * 0.1
        total = subtotal + vat
        
        # 엑셀 생성
        output_dir = Path("docs/excel_orders")
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = output_dir / f"CCW_발주서_{order_number}.xlsx"
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # 발주서 헤더
            header_data = [
                ['발 주 서'],
                [''],
                [f'발주번호: {order_number}', '', '', '', f'발주일: {order_date}'],
                [''],
                ['[ 수신 ] CCW'],
                [''],
                ['[ 발신 ]'],
                [f'업체명: {self.company_info["company_name"]}'],
                [f'담당자: {self.company_info["contact"]} ({self.company_info["phone"]})'],
                [''],
                ['━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'],
                ['★★★ 배송 요청 사항 (중요) ★★★'],
                ['━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'],
                [''],
                ['배송지: 경기 시흥시 장현능곡로 155 시흥 플랑드르 지하 1층 웰빙 푸드마켓'],
                ['수령인: 윤철 대리'],
                ['연락처: 010-7727-8009'],
                ['배송 요청일: ' + delivery_date],
                ['※ 상기 주소로 직접 배송 부탁드립니다.'],
                ['━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'],
                [''],
                ['']
            ]
            
            # 헤더 쓰기
            for idx, row in enumerate(header_data):
                pd.DataFrame([row]).to_excel(writer, sheet_name='발주서', 
                                            startrow=idx, index=False, header=False)
            
            # 품목 데이터
            df_items.to_excel(writer, sheet_name='발주서', startrow=22, index=False)
            
            # 합계 정보
            summary_start_row = 22 + len(df_items) + 2
            summary_data = [
                ['', '', '', '', '공급가액:', f'{subtotal:,.0f}'],
                ['', '', '', '', '부가세(10%):', f'{vat:,.0f}'],
                ['', '', '', '', '합계금액:', f'{total:,.0f}'],
                [''],
                ['결제조건: 월말정산'],
                [''],
                ['※ 배송 관련 문의: 웰빙푸드마켓 윤철 대리 (010-7727-8009)']
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
        
        print(f"CCW 발주서 생성: {filename}")
        print(f"  발주금액(공급가): {subtotal:,.0f}원")
        print(f"  VAT: {vat:,.0f}원")
        print(f"  총액: {total:,.0f}원")
        
        return filename, subtotal
    
    def create_wellbeing_supply_request(self):
        """값진한끼 → 웰빙 공급 요청서"""
        
        doc_number = f"SR-WB-{datetime.now().strftime('%Y%m%d-%H%M')}"
        doc_date = datetime.now().strftime("%Y년 %m월 %d일")
        delivery_date = (datetime.now() + timedelta(days=2)).strftime("%Y년 %m월 %d일")
        
        # 우리 매입가 = CCW 출고가 × 수량
        supply_data = []
        for i, item in enumerate(self.items, 1):
            supply_data.append({
                '번호': i,
                '상품명': item['product_name'],
                '수량': item['quantity'],
                '단위': '개',
                '단가': item['ccw_unit_price'],  # 우리가 웰빙에서 매입하는 단가
                '금액': item['ccw_total']  # 우리가 웰빙에 지불할 금액
            })
        
        df_items = pd.DataFrame(supply_data)
        
        # 합계
        subtotal = df_items['금액'].sum()
        vat = subtotal * 0.1
        total = subtotal + vat
        
        # 엑셀 생성
        output_dir = Path("docs/excel_orders")
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = output_dir / f"웰빙_공급요청서_{doc_number}.xlsx"
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # 공급요청서 헤더
            header_data = [
                ['공 급 요 청 서'],
                [''],
                [f'문서번호: {doc_number}', '', '', '', f'요청일: {doc_date}'],
                [''],
                ['[ 수신 ]'],
                [f'업체명: {self.wellbeing_info["company_name"]}'],
                [f'담당자: {self.wellbeing_info["contact_name"]} {self.wellbeing_info["contact_position"]}'],
                [f'연락처: {self.wellbeing_info["contact_phone"]}'],
                [''],
                ['[ 발신 ]'],
                [f'업체명: {self.company_info["company_name"]}'],
                [''],
                ['[ 배송 정보 ]'],
                ['최종 배송지: CCW 지정 주소 (상기 웰빙 푸드마켓으로 직배송)'],
                [f'납품 요청일: {delivery_date}'],
                [''],
                ['']
            ]
            
            # 헤더 쓰기
            for idx, row in enumerate(header_data):
                pd.DataFrame([row]).to_excel(writer, sheet_name='공급요청서', 
                                            startrow=idx, index=False, header=False)
            
            # 품목 데이터
            df_items.to_excel(writer, sheet_name='공급요청서', startrow=17, index=False)
            
            # 합계 정보
            summary_start_row = 17 + len(df_items) + 2
            summary_data = [
                ['', '', '', '', '공급가액:', f'{subtotal:,.0f}'],
                ['', '', '', '', '부가세(10%):', f'{vat:,.0f}'],
                ['', '', '', '', '합계금액:', f'{total:,.0f}'],
                [''],
                ['결제조건: 월말정산'],
                [''],
                ['※ CCW 발주 건으로 웰빙 푸드마켓으로 직접 납품 부탁드립니다.']
            ]
            
            for idx, row in enumerate(summary_data):
                pd.DataFrame([row]).to_excel(writer, sheet_name='공급요청서', 
                                            startrow=summary_start_row + idx, 
                                            index=False, header=False)
            
            # 서식 조정
            worksheet = writer.sheets['공급요청서']
            worksheet.column_dimensions['A'].width = 10
            worksheet.column_dimensions['B'].width = 35
            worksheet.column_dimensions['C'].width = 10
            worksheet.column_dimensions['D'].width = 10
            worksheet.column_dimensions['E'].width = 15
            worksheet.column_dimensions['F'].width = 15
        
        print(f"웰빙 공급요청서 생성: {filename}")
        print(f"  매입금액(공급가): {subtotal:,.0f}원")
        print(f"  VAT: {vat:,.0f}원")
        print(f"  총액: {total:,.0f}원")
        
        return filename, subtotal
    
    def process_all_orders(self):
        """전체 프로세스 실행"""
        
        print("\n" + "="*60)
        print(" 값진한끼 발주/공급 문서 생성 (최종본)")
        print("="*60)
        
        print("\n[CCW 엑셀 데이터]")
        print("-" * 40)
        for item in self.items:
            print(f"{item['product_name']}: {item['quantity']}개 × {item['ccw_unit_price']:,}원 = {item['ccw_total']:,}원")
        
        total_amount = sum(item['ccw_total'] for item in self.items)
        print(f"\n총 금액: {total_amount:,}원")
        
        # 1. CCW 발주서 (웰빙 직배송 요청)
        print("\n[1] CCW 발주서 생성 (웰빙 직배송 명시)...")
        ccw_file, ccw_amount = self.create_ccw_purchase_order()
        
        # 2. 웰빙 공급요청서
        print("\n[2] 웰빙 공급요청서 생성...")
        wb_file, wb_amount = self.create_wellbeing_supply_request()
        
        # 요약
        print("\n" + "="*60)
        print(" 거래 요약")
        print("="*60)
        
        print("\n거래 흐름:")
        print("  1. 값진한끼 → CCW: 발주 (웰빙으로 직배송 요청)")
        print(f"     금액: {ccw_amount:,.0f}원")
        
        print("\n  2. 값진한끼 → 웰빙: 공급 요청")
        print(f"     금액: {wb_amount:,.0f}원")
        
        print("\n  3. 웰빙 → CCW(웰빙 푸드마켓): 직접 배송")
        print("     배송지: 시흥 플랑드르 지하 1층")
        print("     수령인: 윤철 대리 (010-7727-8009)")
        
        print("\n※ 금액은 동일 (마진 없음)")
        
        return {
            'ccw_file': ccw_file,
            'wellbeing_file': wb_file,
            'amount': ccw_amount
        }

if __name__ == "__main__":
    generator = FinalExcelOrderGenerator()
    result = generator.process_all_orders()
    
    print("\n문서 생성 완료!")
    print(f"1. CCW 발주서: {result['ccw_file']}")
    print(f"2. 웰빙 공급요청서: {result['wellbeing_file']}")
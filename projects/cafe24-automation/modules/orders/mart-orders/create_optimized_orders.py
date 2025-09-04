#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from pathlib import Path
import json
import logging
import pandas as pd

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python3

#!/usr/bin/env python3

#!/usr/bin/env python3

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
값진한끼 최적화된 발주서/거래명세서 생성 시스템
명확한 비즈니스 흐름 반영
"""

class OptimizedOrderGenerator:
    """최적화된 발주서/거래명세서 생성기"""
    
    def __init__(self):
        # 회사 정보
        self.company_info = {
            "company_name": "주식회사 값진한끼",
            "business_number": "123-45-67890",  # TODO: 실제 사업자번호
            "address": "경기도 시흥시",  # TODO: 실제 주소
            "contact": "담당자",
            "phone": "010-XXXX-XXXX"  # TODO: 실제 연락처
        }
        
        # 웰빙신선식품 정보
        self.wellbeing_info = {
            "company_name": "주식회사 웰빙신선식품",
            "business_number": "813-81-02169",
            "contact_name": "윤철",
            "contact_position": "대리",
            "contact_phone": "010-7727-8009",
            "address": "경기 시흥시 장현능곡로 155 시흥 플랑드르 지하 1층 웰빙 푸드마켓"
        }
        
        # CCW 정보
        self.ccw_info = {
            "company_name": "CCW",
            "contact": "담당자"
        }
        
        # 가격 체계 (부가세 포함)
        self.pricing = [
            {
                'product_name': '이태원 햄폭탄 부대찌개',
                'quantity': 3,
                'purchase_price_vat': 68000,  # 웰빙에서 매입 (VAT 포함)
                'sale_price_vat': 81600,      # CCW에 판매 (VAT 포함)
            },
            {
                'product_name': '힘찬 장어탕 500g',
                'quantity': 15,
                'purchase_price_vat': 7200,   # 웰빙에서 매입 (VAT 포함)
                'sale_price_vat': 12200,      # CCW에 판매 (VAT 포함)
            }
        ]
    
    def create_wellbeing_purchase_order(self):
        """웰빙신선식품 발주서 - 값진한끼가 웰빙에서 매입"""
        
        order_number = f"PO-WB-{datetime.now().strftime('%Y%m%d-%H%M')}"
        order_date = datetime.now().strftime("%Y년 %m월 %d일")
        delivery_date = (datetime.now() + timedelta(days=2)).strftime("%Y년 %m월 %d일")
        
        print("\n" + "="*60)
        print(" [1] 웰빙신선식품 발주서 생성")
        print("="*60)
        
        order_data = []
        total_amount = 0
        
        for i, item in enumerate(self.pricing, 1):
            # 부가세 포함 가격으로 계산
            unit_price = item['purchase_price_vat']
            total_price = unit_price * item['quantity']
            total_amount += total_price
            
            order_data.append({
                '번호': i,
                '상품명': item['product_name'],
                '수량': item['quantity'],
                '단위': '개',
                '단가(VAT포함)': unit_price,
                '금액(VAT포함)': total_price
            })
        
        df_items = pd.DataFrame(order_data)
        
        # 부가세 역산
        supply_value = total_amount / 1.1
        vat = total_amount - supply_value
        
        # 엑셀 생성
        output_dir = Path("docs/excel_orders")
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = output_dir / f"웰빙_발주서_{order_number}.xlsx"
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # 헤더 정보
            header_data = [
                ['발 주 서'],
                [''],
                [f'발주번호: {order_number}', '', '', '', f'발주일: {order_date}'],
                [''],
                ['[ 수신 ]'],
                [f'업체명: {self.wellbeing_info["company_name"]}'],
                [f'담당자: {self.wellbeing_info["contact_name"]} {self.wellbeing_info["contact_position"]}'],
                [f'연락처: {self.wellbeing_info["contact_phone"]}'],
                [''],
                ['[ 발신 ]'],
                [f'업체명: {self.company_info["company_name"]}'],
                [f'담당자: {self.company_info["contact"]} ({self.company_info["phone"]})'],
                [''],
                ['[ 품목 내역 ]'],
                ['']
            ]
            
            for idx, row in enumerate(header_data):
                pd.DataFrame([row]).to_excel(writer, sheet_name='발주서', 
                                            startrow=idx, index=False, header=False)
            
            # 품목 데이터
            df_items.to_excel(writer, sheet_name='발주서', startrow=15, index=False)
            
            # 합계 정보
            summary_start_row = 15 + len(df_items) + 2
            summary_data = [
                ['', '', '', '', '공급가액:', f'{supply_value:,.0f}'],
                ['', '', '', '', '부가세(10%):', f'{vat:,.0f}'],
                ['', '', '', '', '합계금액:', f'{total_amount:,.0f}'],
                [''],
                [f'납기일: {delivery_date}'],
                ['결제조건: 월말정산'],
                ['납품장소: CCW에서 웰빙 푸드마켓으로 직배송']
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
            worksheet.column_dimensions['E'].width = 20
            worksheet.column_dimensions['F'].width = 20
        
        print(f"  파일: {filename}")
        print(f"  매입금액: {total_amount:,.0f}원 (VAT 포함)")
        print(f"  공급가액: {supply_value:,.0f}원")
        print(f"  부가세: {vat:,.0f}원")
        
        return filename, total_amount
    
    def create_ccw_transaction_statement(self):
        """CCW 거래명세서 - 값진한끼가 CCW에 판매"""
        
        doc_number = f"TS-CCW-{datetime.now().strftime('%Y%m%d-%H%M')}"
        doc_date = datetime.now().strftime("%Y년 %m월 %d일")
        delivery_date = (datetime.now() + timedelta(days=2)).strftime("%Y년 %m월 %d일")
        
        print("\n" + "="*60)
        print(" [2] CCW 거래명세서 생성")
        print("="*60)
        
        supply_data = []
        total_amount = 0
        
        for i, item in enumerate(self.pricing, 1):
            # 부가세 포함 가격으로 계산
            unit_price = item['sale_price_vat']
            total_price = unit_price * item['quantity']
            total_amount += total_price
            
            supply_data.append({
                '번호': i,
                '상품명': item['product_name'],
                '수량': item['quantity'],
                '단위': '개',
                '단가(VAT포함)': unit_price,
                '금액(VAT포함)': total_price
            })
        
        df_items = pd.DataFrame(supply_data)
        
        # 부가세 역산
        supply_value = total_amount / 1.1
        vat = total_amount - supply_value
        
        # 엑셀 생성
        output_dir = Path("docs/excel_orders")
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = output_dir / f"CCW_거래명세서_{doc_number}.xlsx"
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # 헤더 정보
            header_data = [
                ['거 래 명 세 서'],
                [''],
                [f'문서번호: {doc_number}', '', '', '', f'거래일: {doc_date}'],
                [''],
                ['[ 공급받는자 ]'],
                [f'업체명: {self.ccw_info["company_name"]}'],
                [''],
                ['[ 공급자 ]'],
                [f'업체명: {self.company_info["company_name"]}'],
                [f'사업자번호: {self.company_info["business_number"]}'],
                [f'담당자: {self.company_info["contact"]} ({self.company_info["phone"]})'],
                [''],
                ['※ 배송 안내 ※'],
                ['CCW에서 아래 주소로 직접 배송 부탁드립니다.'],
                [f'배송지: {self.wellbeing_info["address"]}'],
                [f'수령인: {self.wellbeing_info["contact_name"]} {self.wellbeing_info["contact_position"]} ({self.wellbeing_info["contact_phone"]})'],
                [''],
                ['[ 품목 내역 ]'],
                ['']
            ]
            
            for idx, row in enumerate(header_data):
                pd.DataFrame([row]).to_excel(writer, sheet_name='거래명세서', 
                                            startrow=idx, index=False, header=False)
            
            # 품목 데이터
            df_items.to_excel(writer, sheet_name='거래명세서', startrow=19, index=False)
            
            # 합계 정보
            summary_start_row = 19 + len(df_items) + 2
            summary_data = [
                ['', '', '', '', '공급가액:', f'{supply_value:,.0f}'],
                ['', '', '', '', '부가세(10%):', f'{vat:,.0f}'],
                ['', '', '', '', '합계금액:', f'{total_amount:,.0f}'],
                [''],
                ['결제조건: 월말정산'],
                [f'납기일: {delivery_date}'],
                [''],
                ['※ 중요 안내 ※'],
                ['1. 상품은 CCW에서 직접 배송 부탁드립니다.'],
                ['2. 배송 관련 문의는 웰빙신선식품 윤철 대리에게 연락 바랍니다.']
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
            worksheet.column_dimensions['E'].width = 20
            worksheet.column_dimensions['F'].width = 20
        
        print(f"  파일: {filename}")
        print(f"  판매금액: {total_amount:,.0f}원 (VAT 포함)")
        print(f"  공급가액: {supply_value:,.0f}원")
        print(f"  부가세: {vat:,.0f}원")
        
        return filename, total_amount
    
    def generate_summary_report(self):
        """거래 요약 보고서 생성"""
        
        print("\n" + "="*60)
        print(" 거래 흐름 요약")
        print("="*60)
        
        # 매입/판매 계산
        total_purchase = sum(item['purchase_price_vat'] * item['quantity'] 
                           for item in self.pricing)
        total_sale = sum(item['sale_price_vat'] * item['quantity'] 
                        for item in self.pricing)
        total_margin = total_sale - total_purchase
        margin_rate = (total_margin / total_purchase) * 100
        
        print("\n[비즈니스 흐름]")
        print("1. 값진한끼 → 웰빙신선식품: 발주서 (매입)")
        print(f"   금액: {total_purchase:,.0f}원 (VAT 포함)")
        
        print("\n2. 값진한끼 → CCW: 거래명세서 (판매)")
        print(f"   금액: {total_sale:,.0f}원 (VAT 포함)")
        
        print("\n3. CCW → 웰빙 푸드마켓: 직접 배송")
        print(f"   배송지: {self.wellbeing_info['address']}")
        
        print("\n[수익 구조]")
        print(f"매입액: {total_purchase:,.0f}원")
        print(f"판매액: {total_sale:,.0f}원")
        print(f"마진: {total_margin:,.0f}원")
        print(f"마진율: {margin_rate:.1f}%")
        
        print("\n[품목별 마진 분석]")
        for item in self.pricing:
            purchase_total = item['purchase_price_vat'] * item['quantity']
            sale_total = item['sale_price_vat'] * item['quantity']
            item_margin = sale_total - purchase_total
            item_margin_rate = (item_margin / purchase_total) * 100
            
            print(f"\n{item['product_name']}:")
            print(f"  수량: {item['quantity']}개")
            print(f"  매입: {purchase_total:,}원 (개당 {item['purchase_price_vat']:,}원)")
            print(f"  판매: {sale_total:,}원 (개당 {item['sale_price_vat']:,}원)")
            print(f"  마진: {item_margin:,}원 ({item_margin_rate:.1f}%)")
        
        # JSON 보고서 저장
        report = {
            "generated_at": datetime.now().isoformat(),
            "business_flow": {
                "purchase_from": "웰빙신선식품",
                "sell_to": "CCW",
                "delivery_by": "CCW",
                "delivery_to": "웰빙 푸드마켓"
            },
            "financials": {
                "total_purchase": total_purchase,
                "total_sale": total_sale,
                "total_margin": total_margin,
                "margin_rate": margin_rate
            },
            "items": []
        }
        
        for item in self.pricing:
            report["items"].append({
                "product_name": item['product_name'],
                "quantity": item['quantity'],
                "purchase_price": item['purchase_price_vat'],
                "sale_price": item['sale_price_vat'],
                "margin": item['sale_price_vat'] - item['purchase_price_vat']
            })
        
        report_file = Path("docs/generated") / f"order_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n요약 보고서 저장: {report_file}")
        
        return report
    
    def process_all(self):
        """전체 프로세스 실행"""
        
        print("\n" + "="*70)
        print(" 값진한끼 발주/거래명세서 생성 시스템")
        print("="*70)
        
        # 1. 웰빙 발주서
        wb_file, wb_amount = self.create_wellbeing_purchase_order()
        
        # 2. CCW 거래명세서
        ccw_file, ccw_amount = self.create_ccw_transaction_statement()
        
        # 3. 요약 보고서
        summary = self.generate_summary_report()
        
        print("\n" + "="*70)
        print(" 프로세스 완료")
        print("="*70)
        print("\n생성된 문서:")
        print(f"1. 웰빙 발주서: {wb_file}")
        print(f"2. CCW 거래명세서: {ccw_file}")
        
        return {
            'wellbeing_order': wb_file,
            'ccw_statement': ccw_file,
            'summary': summary
        }

if __name__ == "__main__":
    generator = OptimizedOrderGenerator()
    result = generator.process_all()
    
    print("\n모든 문서가 성공적으로 생성되었습니다!")
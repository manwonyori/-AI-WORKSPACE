"""
문서 생성 모듈
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)


class DocumentGenerator:
    """문서 생성 클래스"""
    
    def __init__(self, data_dir: str = "data", docs_dir: str = "docs"):
        self.data_dir = Path(data_dir)
        self.docs_dir = Path(docs_dir)
        self.docs_dir.mkdir(exist_ok=True)
        
        # 문서 템플릿 디렉토리
        self.templates_dir = self.docs_dir / "templates"
        self.templates_dir.mkdir(exist_ok=True)
        
        # 생성된 문서 디렉토리
        self.generated_dir = self.docs_dir / "generated"
        self.generated_dir.mkdir(exist_ok=True)
    
    def create_purchase_order(self):
        """발주서 생성"""
        print("\n[발주서 생성]")
        
        # 발주 정보 입력
        order_number = f"PO-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        supplier_name = input("공급업체명: ").strip()
        
        print("\n발주 품목을 입력하세요 (빈 줄 입력시 종료):")
        items = []
        while True:
            item_name = input("품목명: ").strip()
            if not item_name:
                break
            
            quantity = input("수량: ").strip()
            unit = input("단위: ").strip()
            unit_price = input("단가: ").strip()
            
            items.append({
                "name": item_name,
                "quantity": quantity,
                "unit": unit,
                "unit_price": float(unit_price),
                "total_price": float(quantity) * float(unit_price)
            })
        
        if not items:
            print("발주 품목이 없습니다.")
            return
        
        # 발주서 데이터 생성
        total_amount = sum(item['total_price'] for item in items)
        
        purchase_order = {
            "order_number": order_number,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "supplier": supplier_name,
            "items": items,
            "total_amount": total_amount,
            "delivery_date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
            "payment_terms": "월말 정산",
            "notes": "배송 전 연락 요망"
        }
        
        # HTML 형식으로 발주서 생성
        html_content = self._generate_purchase_order_html(purchase_order)
        
        # 파일 저장
        filename = self.generated_dir / f"{order_number}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # JSON 백업
        json_filename = self.generated_dir / f"{order_number}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(purchase_order, f, ensure_ascii=False, indent=2)
        
        logger.info(f"발주서 생성: {order_number}")
        print(f"\n발주서가 생성되었습니다.")
        print(f"발주번호: {order_number}")
        print(f"총액: {total_amount:,.0f}원")
        print(f"파일 위치: {filename}")
    
    def _generate_purchase_order_html(self, data: Dict) -> str:
        """발주서 HTML 생성"""
        items_html = ""
        for idx, item in enumerate(data['items'], 1):
            items_html += f"""
            <tr>
                <td style="text-align: center;">{idx}</td>
                <td>{item['name']}</td>
                <td style="text-align: center;">{item['quantity']}</td>
                <td style="text-align: center;">{item['unit']}</td>
                <td style="text-align: right;">{item['unit_price']:,.0f}</td>
                <td style="text-align: right;">{item['total_price']:,.0f}</td>
            </tr>
            """
        
        html = f"""
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <title>발주서 - {data['order_number']}</title>
            <style>
                body {{ font-family: 'Malgun Gothic', sans-serif; margin: 20px; }}
                h1 {{ text-align: center; color: #333; }}
                .header {{ margin-bottom: 30px; }}
                .info {{ margin-bottom: 20px; }}
                .info-row {{ display: flex; justify-content: space-between; margin: 5px 0; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 10px; }}
                th {{ background-color: #f4f4f4; font-weight: bold; }}
                .total {{ font-size: 1.2em; font-weight: bold; text-align: right; margin-top: 20px; }}
                .footer {{ margin-top: 50px; padding-top: 20px; border-top: 2px solid #333; }}
            </style>
        </head>
        <body>
            <h1>발 주 서</h1>
            
            <div class="header">
                <div class="info">
                    <div class="info-row">
                        <span><strong>발주번호:</strong> {data['order_number']}</span>
                        <span><strong>발주일자:</strong> {data['date']}</span>
                    </div>
                    <div class="info-row">
                        <span><strong>공급업체:</strong> {data['supplier']}</span>
                        <span><strong>납품예정일:</strong> {data['delivery_date']}</span>
                    </div>
                </div>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th width="50">번호</th>
                        <th>품목명</th>
                        <th width="80">수량</th>
                        <th width="60">단위</th>
                        <th width="100">단가</th>
                        <th width="120">금액</th>
                    </tr>
                </thead>
                <tbody>
                    {items_html}
                </tbody>
            </table>
            
            <div class="total">
                총 발주금액: {data['total_amount']:,.0f}원
            </div>
            
            <div class="footer">
                <p><strong>결제조건:</strong> {data['payment_terms']}</p>
                <p><strong>비고:</strong> {data['notes']}</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def create_transaction_statement(self):
        """거래명세서 생성"""
        print("\n[거래명세서 생성]")
        
        # 거래 정보 입력
        statement_number = f"TS-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        supplier_name = input("공급업체명: ").strip()
        
        print("\n거래 내역을 입력하세요:")
        transaction_type = input("거래 유형 (납품/반품): ").strip()
        
        items = []
        print("\n품목 입력 (빈 줄 입력시 종료):")
        while True:
            item_name = input("품목명: ").strip()
            if not item_name:
                break
            
            quantity = input("수량: ").strip()
            unit = input("단위: ").strip()
            unit_price = input("단가: ").strip()
            
            items.append({
                "name": item_name,
                "quantity": quantity,
                "unit": unit,
                "unit_price": float(unit_price),
                "total_price": float(quantity) * float(unit_price)
            })
        
        if not items:
            print("거래 품목이 없습니다.")
            return
        
        # 거래명세서 데이터
        total_amount = sum(item['total_price'] for item in items)
        
        statement_data = {
            "statement_number": statement_number,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M"),
            "supplier": supplier_name,
            "type": transaction_type,
            "items": items,
            "total_amount": total_amount
        }
        
        # 파일 저장
        filename = self.generated_dir / f"{statement_number}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(statement_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"거래명세서 생성: {statement_number}")
        print(f"\n거래명세서가 생성되었습니다.")
        print(f"명세서 번호: {statement_number}")
        print(f"거래금액: {total_amount:,.0f}원")
    
    def create_monthly_report(self):
        """월간 보고서 생성"""
        print("\n[월간 보고서 생성]")
        
        # 보고서 기간 설정
        year = input("년도 (YYYY): ").strip() or datetime.now().year
        month = input("월 (MM): ").strip() or datetime.now().month
        
        report_date = f"{year}-{month:02d}" if isinstance(month, int) else f"{year}-{month}"
        
        # 데이터 집계 (실제로는 데이터베이스에서 조회)
        report_data = {
            "period": report_date,
            "generated_date": datetime.now().strftime("%Y-%m-%d"),
            "summary": {
                "total_suppliers": 15,
                "active_suppliers": 12,
                "total_items": 45,
                "total_transactions": 127,
                "total_purchase_amount": 15750000,
                "total_sales_amount": 21340000
            },
            "top_suppliers": [
                {"name": "신선식품유통", "amount": 3200000},
                {"name": "농산물직거래", "amount": 2850000},
                {"name": "수산물공급센터", "amount": 2100000}
            ],
            "top_items": [
                {"name": "양파", "quantity": "500kg"},
                {"name": "당근", "quantity": "350kg"},
                {"name": "감자", "quantity": "420kg"}
            ],
            "inventory_status": {
                "total_items": 45,
                "in_stock": 38,
                "low_stock": 5,
                "out_of_stock": 2
            }
        }
        
        # HTML 보고서 생성
        html_content = self._generate_monthly_report_html(report_data)
        
        # 파일 저장
        report_filename = f"monthly_report_{report_date}.html"
        filename = self.generated_dir / report_filename
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # JSON 백업
        json_filename = self.generated_dir / f"monthly_report_{report_date}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"월간 보고서 생성: {report_date}")
        print(f"\n월간 보고서가 생성되었습니다.")
        print(f"기간: {report_date}")
        print(f"파일 위치: {filename}")
    
    def _generate_monthly_report_html(self, data: Dict) -> str:
        """월간 보고서 HTML 생성"""
        
        top_suppliers_html = ""
        for supplier in data['top_suppliers']:
            top_suppliers_html += f"""
            <tr>
                <td>{supplier['name']}</td>
                <td style="text-align: right;">{supplier['amount']:,.0f}원</td>
            </tr>
            """
        
        top_items_html = ""
        for item in data['top_items']:
            top_items_html += f"""
            <tr>
                <td>{item['name']}</td>
                <td style="text-align: right;">{item['quantity']}</td>
            </tr>
            """
        
        html = f"""
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <title>월간 보고서 - {data['period']}</title>
            <style>
                body {{ font-family: 'Malgun Gothic', sans-serif; margin: 20px; }}
                h1 {{ text-align: center; color: #333; }}
                h2 {{ color: #555; border-bottom: 2px solid #ddd; padding-bottom: 5px; }}
                .summary {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 20px 0; }}
                .summary-item {{ background: #f9f9f9; padding: 15px; border-radius: 5px; }}
                .summary-item h3 {{ margin: 0 0 10px 0; color: #666; font-size: 14px; }}
                .summary-item .value {{ font-size: 24px; font-weight: bold; color: #333; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 10px; }}
                th {{ background-color: #f4f4f4; }}
                .section {{ margin: 30px 0; }}
            </style>
        </head>
        <body>
            <h1>월간 운영 보고서</h1>
            <p style="text-align: center;">기간: {data['period']} | 생성일: {data['generated_date']}</p>
            
            <div class="section">
                <h2>운영 요약</h2>
                <div class="summary">
                    <div class="summary-item">
                        <h3>총 거래처</h3>
                        <div class="value">{data['summary']['total_suppliers']}개</div>
                    </div>
                    <div class="summary-item">
                        <h3>총 거래건수</h3>
                        <div class="value">{data['summary']['total_transactions']}건</div>
                    </div>
                    <div class="summary-item">
                        <h3>총 매입액</h3>
                        <div class="value">{data['summary']['total_purchase_amount']:,.0f}원</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>주요 거래처</h2>
                <table>
                    <thead>
                        <tr>
                            <th>거래처명</th>
                            <th>거래금액</th>
                        </tr>
                    </thead>
                    <tbody>
                        {top_suppliers_html}
                    </tbody>
                </table>
            </div>
            
            <div class="section">
                <h2>인기 품목</h2>
                <table>
                    <thead>
                        <tr>
                            <th>품목명</th>
                            <th>거래량</th>
                        </tr>
                    </thead>
                    <tbody>
                        {top_items_html}
                    </tbody>
                </table>
            </div>
            
            <div class="section">
                <h2>재고 현황</h2>
                <p>총 품목: {data['inventory_status']['total_items']}개</p>
                <p>정상 재고: {data['inventory_status']['in_stock']}개</p>
                <p>재고 부족: {data['inventory_status']['low_stock']}개</p>
                <p>품절: {data['inventory_status']['out_of_stock']}개</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def get_monthly_transactions(self) -> int:
        """이번 달 거래 건수 반환"""
        # 실제로는 데이터베이스에서 조회
        return 42
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
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
CCW 발주서 자동 처리 시스템
실제 주문만 추출하여 웰빙신선식품 발주서 생성
"""

class CCWOrderProcessor:
    """CCW 발주서 전용 처리기"""
    
    def __init__(self):
        self.supplier_info = {
            "company_name": "주식회사 웰빙신선식품",
            "business_number": "813-81-02169",
            "contact": {
                "name": "윤철",
                "position": "대리",
                "phone": "010-7727-8009"
            },
            "address": "경기 시흥시 장현능곡로 155 시흥 플랑드르 지하 1층"
        }
        
    def extract_orders(self, file_path):
        """CCW 엑셀에서 실제 주문만 추출"""
        
        print("\n" + "="*60)
        print(" CCW 발주서 처리")
        print("="*60)
        
        # 엑셀 읽기
        df = pd.read_excel(file_path, sheet_name='CCW B2B수급', header=None)
        
        orders = []
        
        # U열(인덱스 20)에 주문수량이 있는 행만 추출
        for i, row in df.iterrows():
            if len(row) > 20:
                try:
                    order_qty = float(row.iloc[20])
                    
                    if order_qty > 0:
                        product_name = str(row.iloc[1]).strip()  # B열
                        
                        # 헤더나 잘못된 행 제외
                        if '상품명' in product_name or '매입가' in product_name or '최씨남매' in product_name:
                            continue
                            
                        unit_price = float(row.iloc[4]) if pd.notna(row.iloc[4]) else 0  # E열
                        
                        orders.append({
                            'row_num': i + 1,  # 엑셀 행 번호
                            'product_name': product_name,
                            'quantity': order_qty,
                            'unit_price': unit_price,
                            'total_price': order_qty * unit_price
                        })
                        
                        print(f"\n발견: {product_name}")
                        print(f"  수량: {order_qty:.0f}개")
                        print(f"  단가: {unit_price:,.0f}원")
                        
                except (ValueError, TypeError):
                    continue
        
        print(f"\n총 {len(orders)}개 품목 발주")
        return orders
    
    def create_purchase_order(self, orders, output_dir="docs/generated"):
        """웰빙신선식품 발주서 생성"""
        
        if not orders:
            print("발주할 품목이 없습니다.")
            return None
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 발주서 번호 생성
        order_number = f"PO-CCW-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # 합계 계산
        subtotal = sum(order['total_price'] for order in orders)
        vat = subtotal * 0.1
        total = subtotal + vat
        
        # HTML 발주서 생성
        html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>발주서 - {order_number}</title>
    <style>
        body {{ 
            font-family: 'Malgun Gothic', sans-serif; 
            margin: 40px;
            line-height: 1.6;
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 3px solid #333;
            padding-bottom: 20px;
        }}
        h1 {{ 
            font-size: 32px; 
            margin: 0;
            color: #333;
        }}
        .order-info {{
            background: #f5f5f5;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        .info-item {{
            padding: 10px;
        }}
        .info-label {{
            font-weight: bold;
            color: #555;
            margin-bottom: 5px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 30px 0;
        }}
        th {{
            background: #2c3e50;
            color: white;
            padding: 12px;
            text-align: left;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }}
        tr:hover {{
            background: #f9f9f9;
        }}
        .number {{ text-align: center; }}
        .quantity {{ text-align: center; }}
        .price {{ text-align: right; }}
        .total-section {{
            margin-top: 30px;
            padding: 20px;
            background: #f0f0f0;
            border-radius: 5px;
        }}
        .total-row {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
        }}
        .grand-total {{
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
            border-top: 2px solid #333;
            padding-top: 10px;
            margin-top: 10px;
        }}
        .footer {{
            margin-top: 50px;
            padding: 20px;
            background: #f9f9f9;
            border-left: 4px solid #2c3e50;
        }}
        .stamp-area {{
            margin-top: 50px;
            display: flex;
            justify-content: space-around;
            text-align: center;
        }}
        .stamp-box {{
            width: 150px;
            padding: 20px;
            border: 2px solid #ccc;
        }}
        @media print {{
            body {{ margin: 20px; }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>발 주 서</h1>
        <p style="margin-top: 10px; color: #666;">Purchase Order</p>
    </div>
    
    <div class="order-info">
        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">발주번호</div>
                <div>{order_number}</div>
            </div>
            <div class="info-item">
                <div class="info-label">발주일자</div>
                <div>{datetime.now().strftime('%Y년 %m월 %d일')}</div>
            </div>
            <div class="info-item">
                <div class="info-label">공급업체</div>
                <div>{self.supplier_info['company_name']}</div>
            </div>
            <div class="info-item">
                <div class="info-label">사업자번호</div>
                <div>{self.supplier_info['business_number']}</div>
            </div>
            <div class="info-item">
                <div class="info-label">담당자</div>
                <div>{self.supplier_info['contact']['name']} {self.supplier_info['contact']['position']}</div>
            </div>
            <div class="info-item">
                <div class="info-label">연락처</div>
                <div>{self.supplier_info['contact']['phone']}</div>
            </div>
        </div>
        <div class="info-item" style="margin-top: 20px;">
            <div class="info-label">배송지</div>
            <div>{self.supplier_info['address']}</div>
        </div>
    </div>
    
    <table>
        <thead>
            <tr>
                <th width="60" class="number">번호</th>
                <th>품목명</th>
                <th width="100" class="quantity">수량</th>
                <th width="120" class="price">단가</th>
                <th width="150" class="price">금액</th>
            </tr>
        </thead>
        <tbody>
"""
        
        # 품목 추가
        for i, order in enumerate(orders, 1):
            html_content += f"""
            <tr>
                <td class="number">{i}</td>
                <td>{order['product_name']}</td>
                <td class="quantity">{order['quantity']:.0f}</td>
                <td class="price">{order['unit_price']:,.0f}원</td>
                <td class="price">{order['total_price']:,.0f}원</td>
            </tr>
"""
        
        html_content += f"""
        </tbody>
    </table>
    
    <div class="total-section">
        <div class="total-row">
            <span>공급가액</span>
            <span>{subtotal:,.0f}원</span>
        </div>
        <div class="total-row">
            <span>부가세 (10%)</span>
            <span>{vat:,.0f}원</span>
        </div>
        <div class="total-row grand-total">
            <span>합계금액</span>
            <span>{total:,.0f}원</span>
        </div>
    </div>
    
    <div class="footer">
        <h3>비고</h3>
        <p>• 납품 전 사전 연락 요망</p>
        <p>• 결제조건: 월말 정산</p>
        <p>• 문의: 웰빙 푸드마켓</p>
    </div>
    
    <div class="stamp-area">
        <div class="stamp-box">
            <p>발주담당</p>
            <br><br><br>
            <p>(인)</p>
        </div>
        <div class="stamp-box">
            <p>검토</p>
            <br><br><br>
            <p>(인)</p>
        </div>
        <div class="stamp-box">
            <p>승인</p>
            <br><br><br>
            <p>(인)</p>
        </div>
    </div>
    
    <div style="margin-top: 30px; text-align: center; color: #999; font-size: 12px;">
        생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | CCW 발주 시스템
    </div>
</body>
</html>"""
        
        # HTML 파일 저장
        html_file = output_dir / f"{order_number}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # JSON 백업 저장
        json_data = {
            "order_number": order_number,
            "date": datetime.now().isoformat(),
            "supplier": self.supplier_info,
            "items": orders,
            "summary": {
                "subtotal": subtotal,
                "vat": vat,
                "total": total
            }
        }
        
        json_file = output_dir / f"{order_number}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n발주서 생성 완료:")
        print(f"  HTML: {html_file}")
        print(f"  JSON: {json_file}")
        
        return order_number
    
    def process_ccw_file(self, file_path):
        """CCW 파일 처리 메인 함수"""
        
        # 1. 주문 추출
        orders = self.extract_orders(file_path)
        
        if not orders:
            print("\n발주할 품목이 없습니다.")
            return None
        
        # 2. 확인
        print("\n" + "="*60)
        print(" 발주 내역 확인")
        print("="*60)
        
        total = 0
        for order in orders:
            print(f"{order['product_name']}: {order['quantity']:.0f}개")
            total += order['total_price']
        
        print(f"\n총액: {total:,.0f}원 (VAT 별도)")
        
        confirm = input("\n이 내용으로 발주서를 생성하시겠습니까? (y/n): ").strip().lower()
        
        if confirm == 'y':
            # 3. 발주서 생성
            order_number = self.create_purchase_order(orders)
            
            print(f"\n발주서 번호: {order_number}")
            print(f"공급업체: {self.supplier_info['company_name']}")
            print(f"담당자: {self.supplier_info['contact']['name']} {self.supplier_info['contact']['position']}")
            
            return order_number
        else:
            print("발주서 생성이 취소되었습니다.")
            return None

if __name__ == "__main__":
    # 테스트 실행
    processor = CCWOrderProcessor()
    
    # CCW 파일 처리
    ccw_file = "tests/ccw 발주.xlsx"
    
    if Path(ccw_file).exists():
        result = processor.process_ccw_file(ccw_file)
        
        if result:
            print(f"\n발주 처리 완료: {result}")
    else:
        print(f"파일을 찾을 수 없습니다: {ccw_file}")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict
import json
import logging

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
발주서 작성 시스템
"""

class PurchaseOrderSystem:
    """발주서 생성 시스템"""
    
    def __init__(self):
        self.data_dir = Path("data")
        self.docs_dir = Path("docs/generated")
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        
        # 공급업체 데이터 로드
        self.suppliers = self.load_suppliers()
        
    def load_suppliers(self) -> Dict:
        """공급업체 정보 로드"""
        suppliers_file = self.data_dir / "suppliers.json"
        if suppliers_file.exists():
            with open(suppliers_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def create_interactive_order(self):
        """대화형 발주서 작성"""
        print("\n" + "="*60)
        print(" 발주서 작성 - 주식회사 웰빙신선식품")
        print("="*60)
        
        # 웰빙신선식품 정보 가져오기
        supplier = None
        for biz_num, info in self.suppliers.items():
            if "웰빙신선" in info.get('company_name', ''):
                supplier = info
                supplier['business_number'] = biz_num
                break
        
        if not supplier:
            print("웰빙신선식품 정보를 찾을 수 없습니다.")
            return
        
        # 공급업체 정보 표시
        print(f"\n[공급업체 정보]")
        print(f"업체명: {supplier['company_name']}")
        print(f"사업자번호: {supplier['business_number']}")
        print(f"대표자: {supplier['representative']}")
        print(f"담당자: {supplier['delivery_contact']['name']} {supplier['delivery_contact']['position']}")
        print(f"연락처: {supplier['delivery_contact']['phone']}")
        print(f"배송지: {supplier['delivery_contact']['address']}")
        
        # 발주번호 생성
        order_number = f"PO-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        print(f"\n발주번호: {order_number}")
        
        # 납기일 설정
        delivery_days = input("\n납기일 (며칠 후, 기본 3일): ").strip() or "3"
        delivery_date = datetime.now() + timedelta(days=int(delivery_days))
        
        # 발주 품목 입력
        print("\n" + "-"*50)
        print(" 발주 품목 입력 (빈 줄 입력시 종료)")
        print("-"*50)
        
        items = []
        item_no = 1
        
        # 자주 주문하는 품목 예시
        print("\n[자주 주문하는 품목 예시]")
        print("1. 양파 (10kg 박스)")
        print("2. 당근 (10kg 박스)")
        print("3. 감자 (20kg 박스)")
        print("4. 대파 (3kg 단)")
        print("5. 양배추 (8kg 박스)")
        
        while True:
            print(f"\n품목 {item_no}:")
            item_name = input("  품목명: ").strip()
            if not item_name:
                break
            
            quantity = input("  수량: ").strip()
            unit = input("  단위 (박스/kg/개 등): ").strip()
            unit_price = input("  단가 (원): ").strip()
            
            # 금액 계산
            try:
                qty = float(quantity)
                price = float(unit_price)
                total = qty * price
                
                items.append({
                    "no": item_no,
                    "name": item_name,
                    "quantity": qty,
                    "unit": unit,
                    "unit_price": price,
                    "total_price": total
                })
                
                print(f"  → 소계: {total:,.0f}원")
                item_no += 1
                
            except ValueError:
                print("  ❌ 숫자를 올바르게 입력해주세요.")
        
        if not items:
            print("\n발주 품목이 없습니다.")
            return
        
        # 합계 계산
        total_amount = sum(item['total_price'] for item in items)
        vat = total_amount * 0.1
        grand_total = total_amount + vat
        
        # 발주서 데이터
        order_data = {
            "order_number": order_number,
            "order_date": datetime.now().strftime("%Y-%m-%d"),
            "delivery_date": delivery_date.strftime("%Y-%m-%d"),
            "supplier": {
                "company_name": supplier['company_name'],
                "business_number": supplier['business_number'],
                "representative": supplier['representative'],
                "address": supplier['business_address']
            },
            "delivery": {
                "address": supplier['delivery_contact']['address'],
                "contact_name": supplier['delivery_contact']['name'],
                "contact_position": supplier['delivery_contact']['position'],
                "contact_phone": supplier['delivery_contact']['phone']
            },
            "items": items,
            "summary": {
                "subtotal": total_amount,
                "vat": vat,
                "total": grand_total
            },
            "payment_terms": "월말 정산",
            "notes": "배송 전 연락 요망"
        }
        
        # 발주서 확인
        print("\n" + "="*60)
        print(" 발주서 내역 확인")
        print("="*60)
        print(f"\n발주번호: {order_data['order_number']}")
        print(f"발주일: {order_data['order_date']}")
        print(f"납기일: {order_data['delivery_date']}")
        print(f"\n[발주 품목]")
        print("-"*60)
        print(f"{'번호':<5} {'품목명':<20} {'수량':<10} {'단가':<12} {'금액':<12}")
        print("-"*60)
        
        for item in items:
            print(f"{item['no']:<5} {item['name']:<20} {item['quantity']:.0f} {item['unit']:<7} "
                  f"{item['unit_price']:>10,.0f}원  {item['total_price']:>10,.0f}원")
        
        print("-"*60)
        print(f"{'공급가액:':<40} {total_amount:>15,.0f}원")
        print(f"{'부가세:':<40} {vat:>15,.0f}원")
        print(f"{'합계:':<40} {grand_total:>15,.0f}원")
        print("="*60)
        
        # 확인 및 저장
        confirm = input("\n이 내용으로 발주서를 생성하시겠습니까? (y/n): ").strip().lower()
        
        if confirm == 'y':
            # JSON 저장
            json_file = self.docs_dir / f"{order_number}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(order_data, f, ensure_ascii=False, indent=2)
            
            # HTML 발주서 생성
            html_file = self.generate_html_order(order_data)
            
            print(f"\n✅ 발주서가 생성되었습니다!")
            print(f"  - JSON: {json_file}")
            print(f"  - HTML: {html_file}")
            print(f"\n발주서를 {supplier['delivery_contact']['name']} {supplier['delivery_contact']['position']}님께 전송하시겠습니까?")
            print(f"연락처: {supplier['delivery_contact']['phone']}")
            
            return order_data
        else:
            print("\n발주서 작성이 취소되었습니다.")
            return None
    
    def generate_html_order(self, order_data: Dict) -> Path:
        """HTML 발주서 생성"""
        
        items_html = ""
        for item in order_data['items']:
            items_html += f"""
            <tr>
                <td style="text-align: center;">{item['no']}</td>
                <td>{item['name']}</td>
                <td style="text-align: center;">{item['quantity']:.0f}</td>
                <td style="text-align: center;">{item['unit']}</td>
                <td style="text-align: right;">{item['unit_price']:,.0f}</td>
                <td style="text-align: right;">{item['total_price']:,.0f}</td>
            </tr>"""
        
        html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>발주서 - {order_data['order_number']}</title>
    <style>
        body {{ font-family: 'Malgun Gothic', sans-serif; margin: 40px; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        h1 {{ font-size: 28px; margin: 0; }}
        .info-box {{ border: 1px solid #ddd; padding: 15px; margin: 20px 0; }}
        .info-row {{ display: flex; justify-content: space-between; margin: 8px 0; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; }}
        th {{ background-color: #f0f0f0; font-weight: bold; }}
        .summary {{ margin-top: 20px; }}
        .summary-row {{ display: flex; justify-content: space-between; margin: 5px 0; font-size: 14px; }}
        .total-row {{ font-size: 18px; font-weight: bold; border-top: 2px solid #333; padding-top: 10px; }}
        .footer {{ margin-top: 40px; padding: 20px; background-color: #f9f9f9; }}
        @media print {{ body {{ margin: 20px; }} }}
    </style>
</head>
<body>
    <div class="header">
        <h1>발 주 서</h1>
    </div>
    
    <div class="info-box">
        <div class="info-row">
            <span><strong>발주번호:</strong> {order_data['order_number']}</span>
            <span><strong>발주일:</strong> {order_data['order_date']}</span>
        </div>
        <div class="info-row">
            <span><strong>납기일:</strong> {order_data['delivery_date']}</span>
            <span><strong>결제조건:</strong> {order_data['payment_terms']}</span>
        </div>
    </div>
    
    <div class="info-box">
        <h3>공급업체 정보</h3>
        <div class="info-row">
            <span><strong>업체명:</strong> {order_data['supplier']['company_name']}</span>
            <span><strong>사업자번호:</strong> {order_data['supplier']['business_number']}</span>
        </div>
        <div class="info-row">
            <span><strong>대표자:</strong> {order_data['supplier']['representative']}</span>
        </div>
        <div class="info-row">
            <span><strong>주소:</strong> {order_data['supplier']['address']}</span>
        </div>
    </div>
    
    <div class="info-box">
        <h3>배송 정보</h3>
        <div class="info-row">
            <span><strong>배송지:</strong> {order_data['delivery']['address']}</span>
        </div>
        <div class="info-row">
            <span><strong>담당자:</strong> {order_data['delivery']['contact_name']} {order_data['delivery']['contact_position']}</span>
            <span><strong>연락처:</strong> {order_data['delivery']['contact_phone']}</span>
        </div>
    </div>
    
    <table>
        <thead>
            <tr>
                <th width="60">번호</th>
                <th>품목명</th>
                <th width="80">수량</th>
                <th width="80">단위</th>
                <th width="120">단가</th>
                <th width="120">금액</th>
            </tr>
        </thead>
        <tbody>
            {items_html}
        </tbody>
    </table>
    
    <div class="summary">
        <div class="summary-row">
            <span>공급가액</span>
            <span>{order_data['summary']['subtotal']:,.0f}원</span>
        </div>
        <div class="summary-row">
            <span>부가세</span>
            <span>{order_data['summary']['vat']:,.0f}원</span>
        </div>
        <div class="summary-row total-row">
            <span>합계금액</span>
            <span>{order_data['summary']['total']:,.0f}원</span>
        </div>
    </div>
    
    <div class="footer">
        <p><strong>비고:</strong> {order_data['notes']}</p>
        <p style="text-align: center; margin-top: 30px;">
            웰빙 푸드마켓<br>
            경기 시흥시 장현능곡로 155 시흥 플랑드르 지하 1층
        </p>
    </div>
</body>
</html>"""
        
        html_file = self.docs_dir / f"{order_data['order_number']}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_file

if __name__ == "__main__":
    system = PurchaseOrderSystem()
    order = system.create_interactive_order()
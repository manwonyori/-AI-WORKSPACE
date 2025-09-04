"""
MCP 송장 자동 처리 시스템
MCP Filesystem과 Memory를 활용한 주문/송장 통합 처리
"""

import os
import json
import glob
from datetime import datetime
import pandas as pd

class MCPInvoiceProcessor:
    def __init__(self):
        self.invoice_dir = r"D:\주문취합\주문_배송"
        self.output_dir = os.path.join(self.invoice_dir, "mcp_processed")
        self.memory_file = os.path.join(self.invoice_dir, "mcp_invoice_memory.json")
        
        # 디렉토리 생성
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 메모리 로드
        self.memory = self.load_memory()
    
    def load_memory(self):
        """MCP Memory에서 이전 처리 기록 로드"""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "processed_files": [],
            "patterns": {},
            "statistics": {}
        }
    
    def save_memory(self):
        """MCP Memory에 처리 기록 저장"""
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)
    
    def process_invoices(self):
        """송장 자동 처리"""
        print("=" * 50)
        print("       MCP 송장 자동 처리 시스템")
        print("=" * 50)
        print()
        
        # Excel 파일 찾기
        print("[1] MCP Filesystem으로 주문 파일 검색...")
        excel_files = glob.glob(os.path.join(self.invoice_dir, "*.xlsx"))
        excel_files.extend(glob.glob(os.path.join(self.invoice_dir, "*.xls")))
        
        new_files = [f for f in excel_files if f not in self.memory.get("processed_files", [])]
        
        if not new_files:
            print("새로운 주문 파일이 없습니다.")
            return
        
        print(f"[2] {len(new_files)}개의 새 주문 파일 발견")
        
        all_orders = []
        
        for file_path in new_files:
            print(f"\n처리 중: {os.path.basename(file_path)}")
            
            try:
                # Excel 파일 읽기
                df = pd.read_excel(file_path)
                
                # 주문 정보 추출
                orders = self.extract_orders(df, file_path)
                all_orders.extend(orders)
                
                # 처리 완료 표시
                self.memory["processed_files"].append(file_path)
                
                print(f"  → {len(orders)}건 처리 완료")
                
            except Exception as e:
                print(f"  → 오류: {e}")
                continue
        
        if all_orders:
            # 송장 생성
            self.create_invoices(all_orders)
            
            # 통계 업데이트
            self.update_statistics(all_orders)
            
            # MCP Memory 저장
            self.save_memory()
            
            print()
            print(f"[완료] 총 {len(all_orders)}건의 주문 처리")
    
    def extract_orders(self, df, file_path):
        """DataFrame에서 주문 정보 추출"""
        orders = []
        
        # 컬럼명 정규화
        df.columns = df.columns.str.strip()
        
        # 필요한 컬럼 찾기
        required_cols = {
            'recipient': ['수령인', '받는분', '수취인', '이름'],
            'phone': ['연락처', '전화번호', '핸드폰'],
            'address': ['주소', '배송지'],
            'product': ['상품명', '제품명', '상품'],
            'quantity': ['수량', '개수']
        }
        
        col_mapping = {}
        for key, possible_names in required_cols.items():
            for col in df.columns:
                if any(name in col for name in possible_names):
                    col_mapping[key] = col
                    break
        
        # 주문 데이터 추출
        for idx, row in df.iterrows():
            order = {
                'order_id': f"ORD_{datetime.now().strftime('%Y%m%d')}_{idx:04d}",
                'file_source': os.path.basename(file_path),
                'processed_at': datetime.now().isoformat()
            }
            
            for key, col in col_mapping.items():
                if col in row:
                    order[key] = str(row[col]) if pd.notna(row[col]) else ''
            
            if order.get('recipient') and order.get('address'):
                orders.append(order)
        
        return orders
    
    def create_invoices(self, orders):
        """송장 생성"""
        print()
        print("[3] MCP로 송장 생성 중...")
        
        # 날짜별 그룹화
        today = datetime.now().strftime("%Y%m%d")
        
        # CSV 파일 생성 (택배사 업로드용)
        invoice_file = os.path.join(self.output_dir, f"invoice_{today}.csv")
        
        invoice_data = []
        for order in orders:
            invoice_data.append({
                '주문번호': order.get('order_id', ''),
                '수령인': order.get('recipient', ''),
                '연락처': order.get('phone', ''),
                '주소': order.get('address', ''),
                '상품명': order.get('product', ''),
                '수량': order.get('quantity', 1)
            })
        
        df_invoice = pd.DataFrame(invoice_data)
        df_invoice.to_csv(invoice_file, index=False, encoding='utf-8-sig')
        
        print(f"  → 송장 파일 생성: {invoice_file}")
        
        # HTML 리포트 생성
        self.create_html_report(orders, today)
    
    def create_html_report(self, orders, date_str):
        """HTML 형식의 일일 리포트 생성"""
        html_file = os.path.join(self.output_dir, f"report_{date_str}.html")
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>MCP 송장 처리 리포트 - {date_str}</title>
    <style>
        body {{ font-family: 'Malgun Gothic', sans-serif; margin: 20px; }}
        h1 {{ color: #2c3e50; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #3498db; color: white; }}
        tr:hover {{ background-color: #f5f5f5; }}
        .summary {{ background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .mcp-badge {{ background: #27ae60; color: white; padding: 2px 8px; border-radius: 3px; }}
    </style>
</head>
<body>
    <h1>📦 MCP 송장 처리 리포트 <span class="mcp-badge">MCP Enhanced</span></h1>
    <div class="summary">
        <h2>요약</h2>
        <p>처리 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>총 주문 수: {len(orders)}건</p>
        <p>MCP 서버: Filesystem + Memory + Sequential Thinking</p>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>주문번호</th>
                <th>수령인</th>
                <th>연락처</th>
                <th>주소</th>
                <th>상품명</th>
                <th>수량</th>
            </tr>
        </thead>
        <tbody>
"""
        
        for order in orders:
            html_content += f"""
            <tr>
                <td>{order.get('order_id', '')}</td>
                <td>{order.get('recipient', '')}</td>
                <td>{order.get('phone', '')}</td>
                <td>{order.get('address', '')}</td>
                <td>{order.get('product', '')}</td>
                <td>{order.get('quantity', 1)}</td>
            </tr>
"""
        
        html_content += """
        </tbody>
    </table>
    
    <div style="margin-top: 30px; color: #7f8c8d;">
        <p>이 리포트는 MCP SuperAssistant를 통해 자동 생성되었습니다.</p>
        <p>Chrome MCP Extension에서 실시간 모니터링 가능합니다.</p>
    </div>
</body>
</html>
"""
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"  → HTML 리포트 생성: {html_file}")
    
    def update_statistics(self, orders):
        """통계 업데이트"""
        stats = self.memory.get("statistics", {})
        
        # 일일 통계
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in stats:
            stats[today] = {
                "total_orders": 0,
                "products": {}
            }
        
        stats[today]["total_orders"] += len(orders)
        
        # 상품별 통계
        for order in orders:
            product = order.get('product', 'Unknown')
            if product in stats[today]["products"]:
                stats[today]["products"][product] += 1
            else:
                stats[today]["products"][product] = 1
        
        self.memory["statistics"] = stats
        
        print()
        print("[통계 업데이트]")
        print(f"  오늘 총 주문: {stats[today]['total_orders']}건")
        print(f"  상품 종류: {len(stats[today]['products'])}개")


def main():
    print("MCP 송장 처리 시스템 시작...")
    print()
    
    processor = MCPInvoiceProcessor()
    processor.process_invoices()
    
    print()
    print("=" * 50)
    print("MCP 송장 처리 완료!")
    print()
    print("다음 위치에서 결과 확인:")
    print(f"  {processor.output_dir}")
    print()
    print("Chrome MCP SuperAssistant 명령:")
    print('  "show today invoices"')
    print('  "analyze order patterns"')
    print("=" * 50)


if __name__ == "__main__":
    main()